import uuid
from datetime import datetime
import os
from dotenv import load_dotenv

from pydantic import BaseModel, Field

from trustcall import create_extractor

from typing import Literal, Optional, TypedDict

from langchain_core.runnables import RunnableConfig
from langchain_core.messages import merge_message_runs
from langchain_core.messages import SystemMessage, HumanMessage

from langchain_groq import ChatGroq

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore

import configuration

# Load environment variables from .env file
load_dotenv()

# Get Groq API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please add it to your .env file.")

## Utilities 

# Inspect the tool calls for Trustcall
class Spy:
    def __init__(self):
        self.called_tools = []

    def __call__(self, run):
        q = [run]
        while q:
            r = q.pop()
            if r.child_runs:
                q.extend(r.child_runs)
            if r.run_type == "chat_model":
                self.called_tools.append(
                    r.outputs["generations"][0][0]["message"]["kwargs"]["tool_calls"]
                )

# Extract information from tool calls for both patches and new memories in Trustcall
def extract_tool_info(tool_calls, schema_name="Memory"):
    """Extract information from tool calls for both patches and new memories.
    
    Args:
        tool_calls: List of tool calls from the model
        schema_name: Name of the schema tool (e.g., "Memory", "ToDo", "Profile")
    """

    # Initialize list of changes
    changes = []
    
    for call_group in tool_calls:
        for call in call_group:
            if call['name'] == 'PatchDoc':
                changes.append({
                    'type': 'update',
                    'doc_id': call['args']['json_doc_id'],
                    'planned_edits': call['args']['planned_edits'],
                    'value': call['args']['patches'][0]['value']
                })
            elif call['name'] == schema_name:
                changes.append({
                    'type': 'new',
                    'value': call['args']
                })

    # Format results as a single string
    result_parts = []
    for change in changes:
        if change['type'] == 'update':
            result_parts.append(
                f"Document {change['doc_id']} updated:\n"
                f"Plan: {change['planned_edits']}\n"
                f"Added content: {change['value']}"
            )
        else:
            result_parts.append(
                f"New {schema_name} created:\n"
                f"Content: {change['value']}"
            )
    
    return "\n\n".join(result_parts)

## Schema definitions

# User profile schema
class Profile(BaseModel):
    """This is the profile of the user you are chatting with"""
    name: Optional[str] = Field(description="The user's name", default=None)
    location: Optional[str] = Field(description="The user's location", default=None)
    job: Optional[str] = Field(description="The user's job", default=None)
    connections: list[str] = Field(
        description="Personal connection of the user, such as family members, friends, or coworkers",
        default_factory=list
    )
    interests: list[str] = Field(
        description="Interests that the user has", 
        default_factory=list
    )

# ToDo schema
class ToDo(BaseModel):
    task: str = Field(description="The task to be completed.")
    time_to_complete: Optional[int] = Field(description="Estimated time to complete the task (minutes).")
    deadline: Optional[datetime] = Field(
        description="When the task needs to be completed by (if applicable)",
        default=None
    )
    solutions: list[str] = Field(
        description="List of specific, actionable solutions for completing the task",
        min_items=1,
        default_factory=list
    )
    status: Literal["not started", "in progress", "done", "archived"] = Field(
        description="Current status of the task",
        default="not started"
    )

## Initialize the model and tools

# Update memory tool
class UpdateMemory(TypedDict):
    """ Decision on what memory type to update """
    update_type: Literal['user', 'todo', 'instructions']

# Initialize the model
model = ChatGroq(
    api_key=groq_api_key,
    model_name="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=32768,
    top_p=1,
    verbose=True
)

## Create the Trustcall extractors for updating the user profile and ToDo list
profile_extractor = create_extractor(
    model,
    tools=[Profile],
    tool_choice="Profile",
)

todo_extractor = create_extractor(
    model,
    tools=[ToDo],
    tool_choice="ToDo",
)

## Prompts 

# Chatbot instruction for choosing what to update and what tools to call 
MODEL_SYSTEM_MESSAGE = """You are a helpful chatbot. 

You are designed to be a companion to a user, helping them keep track of their ToDo list.

You have a long term memory which keeps track of three things:
1. The user's profile (general information about them) 
2. The user's ToDo list
3. General instructions for updating the ToDo list

Here is the current User Profile (may be empty if no information has been collected yet):
<user_profile>
{user_profile}
</user_profile>

Here is the current ToDo List (may be empty if no tasks have been added yet):
<todo>
{todo}
</todo>

Here are the current user-specified preferences for updating the ToDo list (may be empty if no preferences have been specified yet):
<instructions>
{instructions}
</instructions>

Here are your instructions for reasoning about the user's messages:

1. Reason carefully about the user's messages as presented below. 

2. Decide whether any of the your long-term memory should be updated:
- If personal information was provided about the user, update the user's profile by calling UpdateMemory tool with type `user`
- If tasks are mentioned, update the ToDo list by calling UpdateMemory tool with type `todo`
- If the user has specified preferences for how to update the ToDo list, update the instructions by calling UpdateMemory tool with type `instructions`

3. Tell the user that you have updated your memory, if appropriate:
- Do not tell the user you have updated the user's profile
- Tell the user them when you update the todo list
- Do not tell the user that you have updated instructions

4. Err on the side of updating the todo list. No need to ask for explicit permission.

5. Respond naturally to user user after a tool call was made to save memories, or if no tool call was made."""

# Trustcall instruction
TRUSTCALL_INSTRUCTION = """Reflect on following interaction. 

Use the provided tools to retain any necessary memories about the user. 

Use parallel tool calling to handle updates and insertions simultaneously.

System Time: {time}"""

# Instructions for updating the ToDo list
CREATE_INSTRUCTIONS = """Reflect on the following interaction.

Based on this interaction, update your instructions for how to update ToDo list items. Use any feedback from the user to update how they like to have items added, etc.

Your current instructions are:

<current_instructions>
{current_instructions}
</current_instructions>"""

## Node definitions

def task_mAIstro(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Load memories from the store and use them to personalize the chatbot's response."""
    
    # Get the user ID from the config
    configurable = configuration.Configuration.from_runnable_config(config)
    user_id = configurable.user_id

   # Retrieve profile memory from the store
    namespace = ("profile", user_id)
    memories = store.search(namespace)
    if memories:
        user_profile = memories[0].value
    else:
        user_profile = None

    # Retrieve todo memory from the store
    namespace = ("todo", user_id)
    memories = store.search(namespace)
    todo = "\n".join(f"{mem.value}" for mem in memories)

    # Retrieve custom instructions
    namespace = ("instructions", user_id)
    memories = store.search(namespace)
    if memories:
        instructions = memories[0].value
    else:
        instructions = ""
    
    system_msg = MODEL_SYSTEM_MESSAGE.format(user_profile=user_profile, todo=todo, instructions=instructions)

    # Respond using memory as well as the chat history
    response = model.bind_tools([UpdateMemory], parallel_tool_calls=False).invoke([SystemMessage(content=system_msg)]+state["messages"])

    return {"messages": [response]}

def update_profile(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Update the user profile in memory."""
    
    # Get the user ID from the config
    configurable = configuration.Configuration.from_runnable_config(config)
    user_id = configurable.user_id

    # Define the namespace for the memories
    namespace = ("profile", user_id)

    # Combine all messages to provide context
    merged_messages = []
    for message in state["messages"]:
        if message.type == "human":
            merged_messages.append(f"User: {message.content}")
        elif message.type == "ai":
            merged_messages.append(f"Assistant: {message.content}")
    
    merged_content = "\n".join(merged_messages)

    # Use the profile extractor to extract profile information
    extraction_prompt = TRUSTCALL_INSTRUCTION.format(time=datetime.now())
    result = profile_extractor.invoke({"input": merged_content, "instruction": extraction_prompt})

    # Get existing profile
    memories = store.search(namespace)
    
    # Update existing profile or create new one
    if memories:
        # Extract the UUID of the existing document
        doc_id = memories[0].id
        existing_profile = memories[0].value
        
        # Prepare the prompt for updating the document
        extraction_prompt = f"The existing profile is: {existing_profile}\n\n{extraction_prompt}"
        
        # Use the profile extractor to update the existing profile
        result = profile_extractor.invoke({"input": merged_content, "instruction": extraction_prompt})
        
        # Update the existing profile
        store.put(namespace, doc_id, result, {"updated": datetime.now().isoformat()})
    else:
        # Create new profile
        store.put(namespace, str(uuid.uuid4()), result, {"created": datetime.now().isoformat()})
    
    return {"messages": state["messages"]}

def update_todos(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Update the todo list in memory."""
    
    # Get the user ID from the config
    configurable = configuration.Configuration.from_runnable_config(config)
    user_id = configurable.user_id

    # Define the namespace for the memories
    namespace = ("todo", user_id)

    # Combine all messages to provide context
    merged_messages = []
    for message in state["messages"]:
        if message.type == "human":
            merged_messages.append(f"User: {message.content}")
        elif message.type == "ai":
            merged_messages.append(f"Assistant: {message.content}")
    
    merged_content = "\n".join(merged_messages)

    # Get custom instructions if any
    instructions_namespace = ("instructions", user_id)
    instructions_memories = store.search(instructions_namespace)
    custom_instructions = ""
    if instructions_memories:
        custom_instructions = f"Follow these custom instructions when creating ToDo items: {instructions_memories[0].value}"

    # Use the todo extractor to extract todo information
    extraction_prompt = f"{TRUSTCALL_INSTRUCTION.format(time=datetime.now())}\n{custom_instructions}"
    result = todo_extractor.invoke({"input": merged_content, "instruction": extraction_prompt})
    
    # Create new todo
    store.put(namespace, str(uuid.uuid4()), result, {"created": datetime.now().isoformat()})
    
    return {"messages": state["messages"]}

def update_instructions(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Update the instructions for how to create todos."""
    
    # Get the user ID from the config
    configurable = configuration.Configuration.from_runnable_config(config)
    user_id = configurable.user_id
    
    # Define the namespace for the memories
    namespace = ("instructions", user_id)

    # Get existing instructions
    memories = store.search(namespace)
    current_instructions = ""
    if memories:
        current_instructions = memories[0].value
        doc_id = memories[0].id
    else:
        doc_id = str(uuid.uuid4())

    # Combine all messages to provide context
    merged_messages = []
    for message in state["messages"]:
        if message.type == "human":
            merged_messages.append(f"User: {message.content}")
        elif message.type == "ai":
            merged_messages.append(f"Assistant: {message.content}")
    
    merged_content = "\n".join(merged_messages)

    # Create a prompt for updating instructions
    extraction_prompt = CREATE_INSTRUCTIONS.format(current_instructions=current_instructions)
    
    # Use the LLM to generate new instructions
    response = model.invoke(f"{extraction_prompt}\n\nInteraction:\n{merged_content}")
    
    # Update the instructions
    store.put(namespace, doc_id, response.content, {"updated": datetime.now().isoformat()})
    
    return {"messages": state["messages"]}

def route_message(state: MessagesState, config: RunnableConfig, store: BaseStore) -> Literal[END, "update_todos", "update_instructions", "update_profile"]:
    """Route the message to the appropriate update function based on the tool call."""
    
    # Process the last message
    try:
        last_message = state["messages"][-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            tool_call = last_message.tool_calls[0]
            args = tool_call.get("args", {})
            update_type = args.get("update_type", "")
            
            if update_type == "todo":
                return "update_todos"
            elif update_type == "user":
                return "update_profile"
            elif update_type == "instructions":
                return "update_instructions"
        return END
    except (IndexError, AttributeError):
        return END

# Create a workflow graph
workflow = StateGraph(MessagesState)

# Initialize an in-memory store
store = InMemoryStore()

# Configure memory saver
memory_saver = MemorySaver()

# Add nodes to the graph
workflow.add_node("task_mAIstro", task_mAIstro)
workflow.add_node("update_todos", update_todos)
workflow.add_node("update_profile", update_profile)
workflow.add_node("update_instructions", update_instructions)

# Connect the nodes
workflow.set_entry_point("task_mAIstro")
workflow.add_conditional_edges("task_mAIstro", route_message)
workflow.add_edge("update_todos", "task_mAIstro")
workflow.add_edge("update_profile", "task_mAIstro")  
workflow.add_edge("update_instructions", "task_mAIstro")

# Create a runnable from the graph
graph = workflow.compile()
graph_with_memory = graph.with_config({"configurable": {"memory_saver": memory_saver}})

# Add metadata for LangGraph Studio
graph_with_memory.metadata = {
    "name": "ToDo Agent",
    "description": "A ToDo list management agent with long-term memory"
}