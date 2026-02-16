# Using GitHub Copilot API

This guide explains how to use GitHub Copilot API to route both OpenAI and Claude model calls through a unified endpoint.

## Two Options

### Option 1: Local Copilot Proxy (Easiest!)

If you have a local GitHub Copilot proxy running at `http://localhost:4141`, this is the **easiest setup** - no API tokens needed!

📖 **See [LOCAL_PROXY_SETUP.md](LOCAL_PROXY_SETUP.md) for quick 3-step setup.**

Quick config:
```env
USE_GITHUB_COPILOT=true
COPILOT_BASE_URL=http://localhost:4141
TAVILY_API_KEY=tvly_xxxxx
```

### Option 2: GitHub Copilot Cloud API

Use GitHub's cloud API with a token. Continue reading this guide for details.

## What is GitHub Copilot API Routing?

GitHub Copilot provides an OpenAI-compatible API that can route requests to multiple LLM providers including:
- OpenAI models (GPT-4o, GPT-4, etc.)
- Anthropic Claude models (Claude 3.5 Sonnet, etc.)
- Other supported models

This allows you to use a single API token and endpoint for all LLM calls.

## Benefits

1. **Single API Token**: Only need one token instead of separate OpenAI and Anthropic keys
2. **Unified Billing**: All usage tracked through GitHub
3. **Cost Savings**: Potentially lower costs for GitHub Copilot subscribers
4. **Simplified Management**: One place to manage API access

## Setup Instructions

### Step 1: Get GitHub Copilot API Token

1. Ensure you have an active GitHub Copilot subscription
2. Generate a personal access token with Copilot access:
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `copilot` (and `read:org` if using organization)
   - Copy the token (starts with `ghp_` or similar)

Alternatively, if using the Copilot CLI:
```bash
# Get token from copilot-cli
copilot-api token
```

### Step 2: Configure Environment

Edit your `.env` file:

```env
# Enable GitHub Copilot API routing
USE_GITHUB_COPILOT=true
GITHUB_COPILOT_TOKEN=ghp_your_token_here

# Still need Tavily for web research
TAVILY_API_KEY=tvly_your_key_here

# Configure models (use Copilot-compatible model names)
OPENAI_MODEL=gpt-4o
CLAUDE_MODEL=claude-3-5-sonnet-20241022

# Optional: Custom base URL (default is https://api.githubcopilot.com)
# COPILOT_BASE_URL=https://api.githubcopilot.com
```

### Step 3: Validate Configuration

```bash
uv run python main.py --validate-only
```

You should see:
```
✓ Environment configuration validated

Configuration:
  Mode: GitHub Copilot API Routing
  Base URL: https://api.githubcopilot.com
  OpenAI Model: gpt-4o
  Claude Model: claude-3-5-sonnet-20241022
  Output Directory: /path/to/outputs
```

## Supported Models

### OpenAI Models (via Copilot)
- `gpt-4o` - Latest GPT-4 Omni
- `gpt-4o-mini` - Smaller, faster GPT-4 Omni
- `gpt-4-turbo` - GPT-4 Turbo
- `gpt-4` - Standard GPT-4
- `gpt-3.5-turbo` - GPT-3.5

### Claude Models (via Copilot)
- `claude-3-5-sonnet-20241022` - Claude 3.5 Sonnet (recommended)
- `claude-3-opus-20240229` - Claude 3 Opus
- `claude-3-sonnet-20240229` - Claude 3 Sonnet
- `claude-3-haiku-20240307` - Claude 3 Haiku

**Note**: Model availability may vary. Check GitHub Copilot documentation for current list.

## Example Configurations

### Configuration 1: Default (Recommended)
```env
USE_GITHUB_COPILOT=true
GITHUB_COPILOT_TOKEN=ghp_xxxxx
TAVILY_API_KEY=tvly_xxxxx
OPENAI_MODEL=gpt-4o
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

### Configuration 2: Cost-Optimized
```env
USE_GITHUB_COPILOT=true
GITHUB_COPILOT_TOKEN=ghp_xxxxx
TAVILY_API_KEY=tvly_xxxxx
OPENAI_MODEL=gpt-4o-mini
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

### Configuration 3: Maximum Quality
```env
USE_GITHUB_COPILOT=true
GITHUB_COPILOT_TOKEN=ghp_xxxxx
TAVILY_API_KEY=tvly_xxxxx
OPENAI_MODEL=gpt-4o
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

## Switching Between Direct API and Copilot API

You can easily switch between modes by changing `USE_GITHUB_COPILOT`:

### Using Direct APIs
```env
USE_GITHUB_COPILOT=false
OPENAI_API_KEY=sk-xxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxx
TAVILY_API_KEY=tvly_xxxxx
```

### Using GitHub Copilot API
```env
USE_GITHUB_COPILOT=true
GITHUB_COPILOT_TOKEN=ghp_xxxxx
TAVILY_API_KEY=tvly_xxxxx
```

## Troubleshooting

### Error: "Invalid authentication credentials"
- Check that your GitHub token is valid and has Copilot scope
- Ensure token starts with correct prefix (usually `ghp_`)
- Verify your Copilot subscription is active

### Error: "Model not found"
- Check that the model name is exactly correct
- Some models may require specific Copilot subscription tiers
- Try using standard model names (e.g., `gpt-4o` instead of version-specific names)

### Rate Limiting
- GitHub Copilot API has its own rate limits
- If you hit limits, consider:
  - Adding delays between requests
  - Using smaller models for research step
  - Spreading work across multiple runs

### Performance Issues
- First request may be slower (cold start)
- Subsequent requests should be faster
- API routing adds minimal latency (typically <100ms)

## Cost Comparison

| Provider | Research (GPT-4o) | Synthesis (Claude) | Writing (Claude) | Total/Course |
|----------|-------------------|-------------------|------------------|--------------|
| Direct APIs | ~$0.10 | ~$1.00 | ~$1.00 | ~$2.10 |
| GitHub Copilot | Included* | Included* | Included* | $0-10/month** |

\* With active Copilot subscription
\** Depends on subscription tier and usage limits

## Advanced: Custom Base URL

If using a custom Copilot-compatible endpoint:

```env
USE_GITHUB_COPILOT=true
GITHUB_COPILOT_TOKEN=your_token
COPILOT_BASE_URL=https://your-custom-endpoint.com
TAVILY_API_KEY=tvly_xxxxx
```

## FAQ

**Q: Do I still need OpenAI/Anthropic API keys?**
A: No, when `USE_GITHUB_COPILOT=true`, only the Copilot token is used.

**Q: Can I mix Copilot for one model and direct API for another?**
A: Not currently. It's either all through Copilot or all through direct APIs.

**Q: Does this work with other OpenAI-compatible APIs?**
A: Yes! You can set `COPILOT_BASE_URL` to any OpenAI-compatible endpoint.

**Q: What about Tavily API?**
A: Tavily is still required for web research. It's not routed through Copilot.

**Q: Is response quality different?**
A: No, the models respond identically. GitHub Copilot just routes the requests.

## Getting Help

If you encounter issues:

1. Check GitHub Copilot API documentation: https://docs.github.com/en/copilot
2. Verify your token and subscription status
3. Try validating with: `uv run python main.py --validate-only`
4. Check model names against supported list
5. Review error messages carefully - they often indicate the exact issue

## Additional Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Anthropic Claude Documentation](https://docs.anthropic.com/)
