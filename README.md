# LangGraph Seminar: ToDo List Agent with Memory

## Introduction

LangGraph is a powerful framework designed to enhance the development of AI-driven applications by providing structured workflows and agent interactions. This seminar focuses on building a ToDo List Agent with memory capabilities using LangGraph. The agent will be able to maintain both short-term context and long-term memory, allowing it to remember user preferences, tasks, and instructions across multiple interactions.

## 1. Agent & Agent with Memory

### Understanding the Role of Agents in LangGraph

Agents in LangGraph are autonomous entities that can perform tasks, make decisions, and interact with users or other agents. They are designed to handle complex workflows and can be enhanced with memory to maintain context across interactions.

### Implementing Agents with Memory

To implement an agent with memory, we need to:

1. **Define the Memory Structure**: Create schemas to store different types of memories (e.g., user profile, tasks, instructions).
2. **Integrate Memory into the Agent**: Modify the agent to read from and write to memory during interactions.
3. **Manage Memory Updates**: Implement logic to decide when to save or update memories based on the conversation context.

## 2. States Schema & Multiple Schema

### Defining Structured State Schemas

State schemas are used to manage the flow of data within the agent. For our ToDo List Agent, we will define the following schemas:

* **User Profile Schema**: Stores personal information about the user.
* **ToDo Collection Schema**: Maintains a list of tasks with details like deadlines and status.
* **Instructions Schema**: Stores user preferences for how to manage the ToDo list.

### Using Multiple Schemas

By using multiple schemas, we can handle diverse use cases and ensure that the agent can manage different types of information effectively. For example, the agent can update the user profile when the user provides personal information, add tasks to the ToDo collection, and store specific instructions for task management.

## 3. Human in the Loop

### Integrating Human Input

Human input is crucial for enhancing the decision-making process of the agent. By integrating human input, we can:

* **Refine Task Details**: Allow users to provide additional details or modify tasks.
* **Update Preferences**: Let users change their preferences or instructions for task management.
* **Correct Errors**: Enable users to correct any mistakes made by the agent.

### Enhancing Decision-Making

Combining human expertise with AI automation ensures that the agent can make more informed decisions. For example, the agent can suggest deadlines for tasks based on user preferences and allow the user to adjust them if necessary.

## 4. Long - Short Term Memory

### Building Agents with Memory

To build an agent that can maintain both short-term context and long-term memory, we need to:

1. **Implement Semantic Memory**: Use schemas and collections to store and retrieve information.
2. **Create a ToDo List Agent**: Develop an agent that can manage tasks and remember user preferences.
3. **Manage Different Types of Memory**: Handle user profiles, tasks, and instructions separately to ensure efficient memory management.

### Implementation of Semantic Memory

Semantic memory allows the agent to understand and store information in a structured way. For example, the agent can remember that a user prefers to have deadlines for all tasks and apply this preference when adding new tasks.

## 5. Demo: A ToDo List Agent with Memory

### Features

The ToDo List Agent demo showcases the following capabilities:

* **Long-term Memory Management**: Stores information about the user profile, ToDo items, and customized instructions.
* **Intelligent Memory Updates**: The agent decides when to save memories based on the conversation context.
* **Multiple Memory Types**:
  * **User Profile**: Remembers personal information about the user.
  * **ToDo Collection**: Maintains a list of tasks with details like deadlines and status.
  * **Instructions**: Stores user preferences for how to manage the ToDo list.

### Running the Demo

To run the demo, follow these steps:

1. Install LangGraph CLI:
   ```bash
   pip install --upgrade "langgraph-cli[inmem]"
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   export LANGSMITH_API_KEY=lsv2...
   export TAVILY_API_KEY=tvly-...
   export ANTHROPIC_API_KEY=sk-...
   export OPENAI_API_KEY=sk-...
   ```

4. Start LangGraph development server:
   ```bash
   langgraph dev
   ```

5. **Run Docker**: Ensure Docker is running before launching LangGraph Studio.

### Example Interactions

Try the following interactions to test the agent's capabilities:

<<<<<<< HEAD
* Này, em thêm "Nộp báo cáo dự án trước thứ Sáu" vào danh sách công việc giúp anh nhé.

* Nhắc anh vào sáng thứ Năm nha.

* Cho anh xem danh sách công việc của anh đi.

* Anh muốn phân loại công việc thành "Công việc" và "Cá nhân".

* À, anh đã hoàn thành báo cáo dự án rồi. Đánh dấu là đã hoàn thành nhé.

* Em nhớ giúp anh là anh thường nộp báo cáo vào thứ Sáu nha.

* Thêm "Mua đồ ăn" vào danh sách công việc của anh dưới mục "Cá nhân" và nhắc anh vào sáng thứ Bảy.

* Anh thích nhận nhắc nhở qua email hơn là thông báo.

* Hiện tại, cho anh xem danh sách chỉ bao gồm các công việc thuộc mục "Công việc" thôi.
=======
* My name is Alex and I live in New York
* I need to finish my presentation by Friday
* Please add 'Buy groceries' to my todo list
* What tasks do I have pending?
* When adding tasks, please always include a deadline
>>>>>>> a88b9c3f4611a8f7145668a4b89673d4b5cf47fb

### Demo Graph
![Demo Graph](assets/demo_graph.png)

## Conclusion

The LangGraph framework provides a robust foundation for building AI-driven applications with structured workflows and agent interactions. By implementing a ToDo List Agent with memory, we can create a powerful tool that helps users manage their tasks efficiently while maintaining context across interactions. This seminar has covered the key concepts and steps required to build such an agent, from defining state schemas to integrating human input and managing long-short term memory.

## Future Work

* **Enhance Memory Management**: Explore more advanced memory management techniques to improve the agent's ability to recall and utilize information.
* **Expand Use Cases**: Apply the LangGraph framework to other domains, such as customer support or project management, to demonstrate its versatility.
* **Improve User Interaction**: Develop more intuitive interfaces for interacting with the agent, such as voice commands or natural language processing.

## References

* LangGraph Documentation: [https://langgraph.ai/docs](https://langgraph.ai/docs)
* LangGraph GitHub Repository: [https://github.com/langgraph/langgraph](https://github.com/langgraph/langgraph)
<<<<<<< HEAD
* LangGraph CLI Installation Guide: [https://langgraph.ai/docs/cli](https://langgraph.ai/docs/cli)
=======
* LangGraph CLI Installation Guide: [https://langgraph.ai/docs/cli](https://langgraph.ai/docs/cli)
>>>>>>> a88b9c3f4611a8f7145668a4b89673d4b5cf47fb
