# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
COPY pyproject.toml .

# Install Python dependencies (including yokatlas-py from GitHub)
RUN echo "Installing Python dependencies..." && \
    pip install --no-cache-dir --verbose -r requirements.txt && \
    echo "Dependencies installed successfully!"

# Copy the MCP server code
COPY yokatlas_mcp_server.py .

# Test that the server can import properly
RUN echo "Testing server imports..." && \
    python -c "import yokatlas_mcp_server; print('✓ Server imports successfully')" && \
    echo "✓ All imports working!"

# Expose the port (will be set by Smithery via PORT env var)
EXPOSE 8000

# Set the command to run the server
CMD ["python", "yokatlas_mcp_server.py"] 