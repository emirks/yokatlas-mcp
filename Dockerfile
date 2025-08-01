# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies with better error handling
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && echo "✓ System dependencies installed"

# Copy requirements and install Python dependencies
COPY requirements.txt .

# Install Python dependencies with error handling and fallback
RUN echo "Installing Python dependencies..." && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt || \
    (echo "Standard install failed, trying git dependency..." && \
    pip install --no-cache-dir fastmcp>=2.10.5 && \
    pip install --no-cache-dir "git+https://github.com/emirks/yokatlas-py.git" && \
    pip install --no-cache-dir beautifulsoup4>=4.12.3 setuptools>=80.9.0 pydantic>=2.0.0 requests>=2.31.0) && \
    echo "✓ Dependencies installed successfully!"

# Copy the MCP server code
COPY yokatlas_mcp_server.py .

# Test that the server can import properly with better error reporting
RUN echo "Testing server imports..." && \
    python -c "import yokatlas_mcp_server; print('✓ Server imports successfully')" && \
    echo "✓ All imports working!"

# Health check to ensure server can start
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)" || exit 1

# Expose the port (will be set by Smithery via PORT env var)
EXPOSE 8000

# Set the command to run the server
CMD ["python", "yokatlas_mcp_server.py"] 