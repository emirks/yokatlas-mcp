# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
COPY pyproject.toml .

# Copy the local yokatlas-py package
COPY yokatlas-py/ ./yokatlas-py/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the MCP server code
COPY yokatlas_mcp_server.py .

# Expose the port (will be set by Smithery via PORT env var)
EXPOSE 8000

# Set the command to run the server
CMD ["python", "yokatlas_mcp_server.py"] 