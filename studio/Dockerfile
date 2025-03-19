# Use a minimal Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements first (for better Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose LangGraph Studio port
EXPOSE 2024

# Run LangGraph dev command
CMD ["langgraph", "dev"]
