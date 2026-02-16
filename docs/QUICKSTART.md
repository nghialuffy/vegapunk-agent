# Quick Start Guide - Using uv

This guide shows you how to get started with the Research & Teaching Agent using `uv`.

## Prerequisites

Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Setup Steps

### 1. Install Dependencies

```bash
# uv will automatically create a virtual environment and install all dependencies
uv sync
```

This will:
- Create a `.venv` directory with a Python virtual environment
- Install all required packages (LangGraph, OpenAI, Anthropic, Tavily, etc.)
- Install the project in editable mode

### 2. Configure API Keys

You have three options (choose the easiest for you):

#### Option A: Local Copilot Proxy (EASIEST - No tokens needed!)

If you have a local GitHub Copilot proxy running at `http://localhost:4141`:

```bash
cp .env.example .env
nano .env
```

Add these 3 lines:
```env
USE_GITHUB_COPILOT=true
COPILOT_BASE_URL=http://localhost:4141
TAVILY_API_KEY=tvly-xxxxx
```

**That's it!** No OpenAI or Anthropic keys needed.

📖 **See [LOCAL_PROXY_SETUP.md](LOCAL_PROXY_SETUP.md) for details.**

#### Option B: GitHub Copilot Cloud API

Use GitHub Copilot's cloud API:

```bash
cp .env.example .env
nano .env
```

Example `.env`:
```env
USE_GITHUB_COPILOT=true
GITHUB_COPILOT_TOKEN=ghp_xxxxx
COPILOT_BASE_URL=https://api.githubcopilot.com
TAVILY_API_KEY=tvly-xxxxx
OPENAI_MODEL=gpt-4o
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

📖 **See [GITHUB_COPILOT.md](GITHUB_COPILOT.md) for detailed instructions.**

#### Option C: Direct API Access

```bash
cp .env.example .env
nano .env
```

Required API keys:
- **OPENAI_API_KEY**: Get from https://platform.openai.com/api-keys
- **ANTHROPIC_API_KEY**: Get from https://console.anthropic.com/
- **TAVILY_API_KEY**: Get from https://tavily.com/

Example `.env`:
```env
OPENAI_API_KEY=sk-xxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxx
TAVILY_API_KEY=tvly-xxxxx
```

### 3. Validate Setup

```bash
uv run python main.py --validate-only
```

You should see:
```
✓ Environment configuration validated

Configuration:
  OpenAI Model: gpt-4o
  Claude Model: claude-sonnet-4-20250514
  Output Directory: /path/to/vegapunk-agent/outputs
```

## Running the Agent

### Basic Usage

```bash
uv run python main.py --topic "Introduction to LangGraph"
```

### With Custom Audience

```bash
uv run python main.py \
  --topic "Python Async Programming" \
  --audience "intermediate Python developers"
```

### Using Existing Repository Directory

If you want to organize all your generated courses in a specific directory:

```bash
# Create a directory for your courses
mkdir -p ~/my-courses

# Generate course in that directory
uv run python main.py \
  --topic "Git Basics" \
  --repo-dir ~/my-courses
```

This will create `~/my-courses/git-basics/` instead of using the default `outputs/` directory.

### Using the Convenience Script

```bash
./run.sh --topic "Docker Basics" --audience "DevOps beginners"
```

## What Happens When You Run It

1. **Step 1 - Setup**: Creates `outputs/<topic-name>/` directory
2. **Step 2 - Research**: Searches web via Tavily, synthesizes with OpenAI
3. **Step 3 - Synthesis**: Claude creates knowledge base and lesson outline
4. **Step 4 - Writing**: Claude writes each lesson
5. **Step 5 - Publish**: Saves to markdown files and commits to git

## Example Output

```
outputs/introduction-to-langgraph/
├── README.md
└── lessons/
    ├── lesson_01_fundamentals.md
    ├── lesson_02_core_concepts.md
    ├── lesson_03_practical_applications.md
    └── lesson_04_advanced_topics.md
```

## Troubleshooting

### "Missing required environment variables"
- Make sure you've copied `.env.example` to `.env`
- Ensure all API keys are set correctly in `.env`
- Don't use quotes around the API keys

### "Module not found" errors
- Run `uv sync` to ensure all dependencies are installed
- Make sure you're using `uv run python main.py` not just `python main.py`

### Rate limiting errors
- The agent makes multiple API calls
- Make sure you have sufficient credits/quota on your API accounts
- Consider adding delays between lessons if needed

## Advanced Usage

### Custom Models

Edit `src/config.py` to change the default models:
```python
OPENAI_MODEL = "gpt-4o-mini"  # Use cheaper model
CLAUDE_MODEL = "claude-sonnet-4-20250514"  # Latest Claude
```

### Custom Prompts

Edit `src/prompts.py` to modify how the agent writes lessons.

### Development Mode

```bash
# Install with dev dependencies
uv sync --all-extras

# Run tests (when added)
uv run pytest

# Type check
uv run mypy src/
```

## Cost Estimation

For a typical 4-lesson course:
- **Tavily**: ~$0.01 (5 searches)
- **OpenAI GPT-4o**: ~$0.10 (research synthesis)
- **Claude Sonnet-4**: ~$2.00 (knowledge synthesis + 4 lessons)
- **Total**: ~$2.11 per course

Costs vary based on topic complexity and lesson length.

## Next Steps

1. Try generating a course on a topic you're interested in
2. Review the generated lessons in the `outputs/` directory
3. Customize prompts in `src/prompts.py` for your preferred teaching style
4. Share your feedback and contribute improvements!
