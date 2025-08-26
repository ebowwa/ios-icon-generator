#!/bin/bash

# iOS Icon Generator MCP Server Launcher

echo "🚀 iOS Icon Generator MCP Server"
echo "================================"

# Check for OPENAI_API_KEY
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY not set"
    echo "   Please set it with: export OPENAI_API_KEY='your-key-here'"
    echo ""
fi

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
echo "📦 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Run the MCP server
echo "🎯 Starting MCP server on http://localhost:3000"
echo ""
python mcp_server.py "$@"