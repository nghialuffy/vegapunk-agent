#!/usr/bin/env bash
# Quick start script for running the agent with uv

set -e

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo ""
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "✅ Created .env file"
    echo ""
    echo "Please edit .env and add your API keys:"
    echo "  - OPENAI_API_KEY"
    echo "  - ANTHROPIC_API_KEY"
    echo "  - TAVILY_API_KEY"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Check if all required keys are set
if ! grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null && \
   ! grep -q "ANTHROPIC_API_KEY=sk-ant-" .env 2>/dev/null && \
   ! grep -q "TAVILY_API_KEY=tvly-" .env 2>/dev/null; then
    echo "⚠️  API keys not configured in .env"
    echo ""
    echo "Please edit .env and add your API keys."
    exit 1
fi

# Run with uv
echo "🚀 Running Research & Teaching Agent..."
echo ""
uv run python main.py "$@"
