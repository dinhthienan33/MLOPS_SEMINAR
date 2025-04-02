FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt 

EXPOSE 2024

CMD ["langgraph", "dev"]

