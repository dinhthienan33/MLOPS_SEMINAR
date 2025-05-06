# LangGraph ToDo Agent

A ToDo list management agent with long-term memory capabilities built using LangGraph and Groq LLM API.

## Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the LangGraph app:
   ```bash
   cd studio
   langgraph dev
   ```

3. Access the application at http://localhost:8000

## Docker Deployment

### Option 1: Build and Run Locally

1. Build and run using Docker Compose:
   ```bash
   cd studio
   docker-compose up -d
   ```

2. Access the application at http://localhost:8000

### Option 2: Pull from DockerHub and Run

1. Update the docker-compose.yml file to use the DockerHub image by uncommenting the image line and commenting out the build section.

2. Pull and run:
   ```bash
   docker-compose up -d
   ```

## Publishing to DockerHub

1. Build the Docker image:
   ```bash
   docker build -t yourusername/langgraph-todo-agent:latest .
   ```

2. Push to DockerHub:
   ```bash
   docker login
   docker push yourusername/langgraph-todo-agent:latest
   ```

## Environment Configuration

Create a `.env` file in the studio directory with:
```
GROQ_API_KEY=your_groq_api_key_here
```

## Features

- Manage user profiles with personal information
- Create and manage ToDo items
- Store custom instructions for ToDo creation
- Persistent memory across conversations 