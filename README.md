# LangGraph Seminar 
This is mini project (seminar) for **CS317.P22** about **LangGraph**.
## Members: 
| Họ và Tên            | MSSV      |
|----------------------|-----------|
| Đinh Thiên Ân       | 22520010  |
| Huỳnh Trọng Nghĩa   | 22520003  |
| Lê Trần Gia Bảo     | 22520105  |
| Bùi Gia Khánh       | 22520630  |
| Nguyễn Hồ Nam       | 22520915  |

[Canva link slides](https://www.canva.com/design/DAGhm-rYgK8/at8laquRDgwGl2qJahMhRw/view?utm_content=DAGhm-rYgK8&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hcd167de6e4)
## 1. Introduction
An overview of LangGraph, its purpose, and how it enhances the development of AI-driven applications with structured workflows and agent interactions.

## 2. Agent & Agent with Memory
- Understanding the role of agents in LangGraph.
- Implementing agents with memory to maintain context across interactions.

## 3. States Schema & Multiple Schema
- Defining structured state schemas to manage data flow.
- Using multiple schemas to handle diverse use cases.

## 4. Human in the Loop
- Integrating human input into AI workflows.
- Enhancing decision-making by combining human expertise with AI automation.

## 5. Long - Short Term Memory
- Building agents that can maintain both short-term context and long-term memory
- Implementation of semantic memory using schemas and collections
- Creating a ToDo list agent with memory persistence
- Managing different types of memory (profile, tasks, instructions)

## 6. Demo: A ToDo List Agent with Memory
The demo showcases a task management agent that helps users maintain a ToDo list with the following capabilities:

- **Long-term memory management**: Stores information about the user profile, ToDo items, and customized instructions
- **Intelligent memory updates**: The agent decides when to save memories based on conversation context
- **Multiple memory types**:
  - User Profile: Remembers personal information about the user
  - ToDo Collection: Maintains a list of tasks with details like deadlines and status
  - Instructions: Stores user preferences for how to manage the ToDo list

# LangGraph ToDo Agent Demo

This demo showcases a ToDo list management agent built with LangGraph that utilizes long-short term memory to maintain context and information across conversations.

## Features

- **Intelligent Memory Management**: The agent automatically decides when to save information as memories
- **Multiple Memory Types**:
  - User Profile: Remembers personal information about the user
  - ToDo Collection: Maintains a list of tasks with details
  - Instructions: Stores user preferences for ToDo list management


## Running the Demo

Integrate into demo
```bash
cd studio
```
### Prerequisites

1. Install the LangGraph CLI:
```bash
pip install --upgrade "langgraph-cli[inmem]"
```
2. Install Dependencies
```bash
pip install -r requirements.txt
```
3. Create a .env file
  You will find a `.env.example` in the root of your new LangGraph app. Create a `.env` file in the root of your new LangGraph app and copy the contents of the `.env.example` file into it, filling in the necessary API keys:  

  ```env
  LANGSMITH_API_KEY=lsv2...
  TAVILY_API_KEY=tvly-...
  ANTHROPIC_API_KEY=sk-...
  GROQ_API_KEY=sk-...
```

4, Launch LangGraph Server
```bash
langgraph dev
```

Note : Run docker before run Langgraph studio


## Demo Graph
![](assets\demo_graph.png)
### Example Interactions

Try the following interactions to test the agent's capabilities:

- "My name is Alex and I live in New York" (updates user profile)
- "I need to finish my presentation by Friday" (adds a task)
- "Please add 'Buy groceries' to my todo list" (adds another task)
- "What tasks do I have pending?" (retrieves tasks)
- "When adding tasks, please always include a deadline" (updates instructions)
