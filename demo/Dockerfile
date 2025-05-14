FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt 

# Build the LangGraph application
RUN langgraph build -t demo

EXPOSE 2024

# Run the development server
CMD ["langgraph", "dev"]

