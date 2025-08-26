#!/bin/bash
cd /Users/ebowwa/apps/ios-icon-generator
export OPENAI_API_KEY="$OPENAI_API_KEY"
exec uv run python mcp_server.py