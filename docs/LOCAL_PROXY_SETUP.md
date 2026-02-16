# Quick Setup: Local GitHub Copilot Proxy

This is the **easiest and recommended** way to use the Research & Teaching Agent with your local GitHub Copilot proxy.

## What is This?

Your local GitHub Copilot proxy at `http://localhost:4141` provides an OpenAI-compatible API that routes requests to both OpenAI and Claude models - **without requiring any API tokens!**

## Setup (3 Simple Steps)

### Step 1: Ensure Your Copilot Proxy is Running

Make sure your GitHub Copilot proxy is running on `localhost:4141`:

```bash
# Test if it's running (should respond)
curl http://localhost:4141/v1/models
```

### Step 2: Configure Environment

Create/edit your `.env` file:

```bash
cp .env.example .env
nano .env
```

Add these lines (uncomment in .env.example):

```env
# Enable GitHub Copilot proxy
USE_GITHUB_COPILOT=true
COPILOT_BASE_URL=http://localhost:4141

# Still need Tavily for web research
TAVILY_API_KEY=your_tavily_key_here

# Optional: Specify models (defaults are fine)
OPENAI_MODEL=gpt-4o
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

**That's it!** No OpenAI or Anthropic API keys needed!

### Step 3: Validate

```bash
uv run python main.py --validate-only
```

Expected output:
```
✓ Environment configuration validated

Configuration:
  Mode: GitHub Copilot API Routing
  Base URL: http://localhost:4141
  OpenAI Model: gpt-4o
  Claude Model: claude-3-5-sonnet-20241022
  Output Directory: /path/to/vegapunk-agent/outputs
```

## Run the Agent

```bash
# Quick test
uv run python main.py --topic "Introduction to LangGraph"

# Or use the convenience script
./run.sh --topic "Python Async Programming"
```

## Complete .env Example

```env
# Local Copilot Proxy (No token needed!)
USE_GITHUB_COPILOT=true
COPILOT_BASE_URL=http://localhost:4141

# Tavily for web research (required)
TAVILY_API_KEY=tvly_xxxxxxxxxxxxx

# Model selection (optional, these are defaults)
OPENAI_MODEL=gpt-4o
CLAUDE_MODEL=claude-3-5-sonnet-20241022

# Git config (optional)
GIT_USER_NAME=Your Name
GIT_USER_EMAIL=your@email.com
```

## Why This is Great

✅ **No API keys needed** - Proxy handles authentication
✅ **Works offline** - Local proxy, no external auth calls
✅ **Fast** - No network latency for auth
✅ **Free** - Uses your existing Copilot subscription
✅ **Simple** - Just 3 lines of config

## Troubleshooting

### Error: "Connection refused"
- Make sure your Copilot proxy is running
- Check it's on port 4141: `curl http://localhost:4141/v1/models`
- Restart your proxy if needed

### Error: "Model not found"
- Check which models your proxy supports
- Try: `curl http://localhost:4141/v1/models`
- Update `OPENAI_MODEL` or `CLAUDE_MODEL` if needed

### Different Port?
If your proxy runs on a different port:
```env
COPILOT_BASE_URL=http://localhost:YOUR_PORT
```

### HTTPS Proxy?
If using HTTPS:
```env
COPILOT_BASE_URL=https://localhost:4141
```

## Advanced: Custom Model Names

If your proxy uses different model names:

```env
# Example: Proxy maps models differently
OPENAI_MODEL=gpt-4-turbo
CLAUDE_MODEL=claude-3.5-sonnet
```

Check available models:
```bash
curl http://localhost:4141/v1/models | jq '.data[].id'
```

## Switching Back to Direct APIs

To use direct OpenAI/Anthropic APIs instead:

1. Edit `.env`:
   ```env
   # Comment out or remove:
   # USE_GITHUB_COPILOT=true
   # COPILOT_BASE_URL=http://localhost:4141

   # Add:
   OPENAI_API_KEY=sk-xxxxx
   ANTHROPIC_API_KEY=sk-ant-xxxxx
   TAVILY_API_KEY=tvly-xxxxx
   ```

2. Validate: `uv run python main.py --validate-only`

## What Happens Under the Hood

```
Your Agent
    ↓
call_openai("Research this topic...")
    ↓
OpenAI Client (base_url=http://localhost:4141)
    ↓
Local Copilot Proxy
    ↓
GitHub Copilot API → GPT-4o response
```

```
Your Agent
    ↓
call_claude("Write this lesson...")
    ↓
OpenAI Client (base_url=http://localhost:4141)
    ↓
Local Copilot Proxy
    ↓
GitHub Copilot API → Claude response
```

## Cost Comparison

| Setup | Research | Synthesis | Writing | Total/Course |
|-------|----------|-----------|---------|--------------|
| Direct APIs | ~$0.10 | ~$1.00 | ~$1.00 | ~$2.10 |
| **Local Proxy** | **$0** | **$0** | **$0** | **$0*** |

\* Included with Copilot subscription

## Getting Help

If you have issues:

1. **Check proxy is running**: `curl http://localhost:4141/v1/models`
2. **Validate config**: `uv run python main.py --validate-only`
3. **Check logs**: Look at your proxy logs for errors
4. **Test directly**: `curl http://localhost:4141/v1/chat/completions -X POST -H "Content-Type: application/json" -d '{"model":"gpt-4o","messages":[{"role":"user","content":"hi"}]}'`

## Next Steps

1. ✅ Set up `.env` with the 3 config lines above
2. ✅ Validate with `--validate-only`
3. ✅ Generate your first course!

That's it! You're ready to create amazing educational content. 🚀
