# Research & Teaching Agent

A LangGraph-based AI agent that automatically creates high-quality educational courses by researching topics and writing pedagogical content.

## Overview

This agent implements a deterministic 5-step pipeline:

1. **Repo & Folder Setup** - Create local directory structure
2. **Web Research** - Search and gather information via Tavily API
3. **Knowledge Synthesis** - Use Claude to organize research into teachable structure
4. **Lecture Writing** - Use Claude to write complete lessons
5. **GitHub Push** - Commit and push content using Git

## Key Design Principles

- **Intentional LLM Usage**: OpenAI GPT-4o handles planning/structuring, Claude Sonnet-4 handles deep synthesis and pedagogical writing
- **Deterministic Pipeline**: LangGraph provides predictable state management
- **Quality-First**: Claude's output must meet professional teaching standards (see CLAUDE.md)

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for fast, reliable Python package management.

### Option 1: Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone <your-repo-url>
cd vegapunk-agent

# Install dependencies (uv will auto-create venv and install everything)
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### Option 2: Using pip

```bash
# Clone the repository
git clone <your-repo-url>
cd vegapunk-agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys
```

## Configuration

### Option 1: Local GitHub Copilot Proxy (Recommended - Easiest!)

**No API tokens needed!** Use your local Copilot proxy at `http://localhost:4141`:

```env
USE_GITHUB_COPILOT=true
COPILOT_BASE_URL=http://localhost:4141
TAVILY_API_KEY=your_tavily_key_here
```

📖 **See [LOCAL_PROXY_SETUP.md](LOCAL_PROXY_SETUP.md) for quick 3-step setup.**

### Option 2: GitHub Copilot Cloud API

Use GitHub Copilot's cloud API with a token:

```env
USE_GITHUB_COPILOT=true
GITHUB_COPILOT_TOKEN=ghp_your_token_here
COPILOT_BASE_URL=https://api.githubcopilot.com
TAVILY_API_KEY=your_tavily_key_here
OPENAI_MODEL=gpt-4o
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

📖 **See [GITHUB_COPILOT.md](GITHUB_COPILOT.md) for detailed setup.**

### Option 3: Direct API Access

Use separate API keys for OpenAI and Anthropic:

```env
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
TAVILY_API_KEY=your_tavily_key_here
```

### Getting API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/
- **Tavily**: https://tavily.com/
- **GitHub Copilot**: https://github.com/settings/tokens (requires active Copilot subscription)

## Usage

### Using uv (Recommended)

```bash
# Basic usage
uv run python main.py --topic "Introduction to LangGraph"

# Or use the convenience script
./run.sh --topic "Introduction to LangGraph"

# Specify target audience
uv run python main.py \
  --topic "Python Async Programming" \
  --audience "intermediate Python developers"

# Use existing repository directory
uv run python main.py \
  --topic "Docker Basics" \
  --repo-dir ~/my-courses

# Validate configuration
uv run python main.py --validate-only
```

### Resume from Interruptions

The agent automatically saves progress and can resume:

```bash
# First run - crashes after 2 lessons
uv run python main.py --topic "Memory of AI" --repo-dir ~/Git

# Second run - automatically resumes, skips completed work
uv run python main.py --topic "Memory of AI" --repo-dir ~/Git
# → Skips research (already done)
# → Skips synthesis (already done)
# → Skips completed lessons
# → Only writes missing lessons
```

📖 **See [RESUME.md](RESUME.md) for automatic resume and crash recovery.**

📖 **See [REPO_DIRECTORY.md](REPO_DIRECTORY.md) for organizing courses in custom directories.**

### Using pip/venv

```bash
# Activate virtual environment first
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Basic usage
python main.py --topic "Introduction to LangGraph"

# Specify target audience
python main.py \
  --topic "Python Async Programming" \
  --audience "intermediate Python developers"

# Validate configuration
python main.py --validate-only
```

## Example Output

The agent creates a **two-level directory structure**: `learn-{main-topic}/{subtopic}/`

```
~/Git/
├── learn-ai/
│   ├── general/              # Topic: "AI"
│   │   ├── lessons/
│   │   └── README.md
│   ├── memory/               # Topic: "Memory of AI"
│   │   ├── lessons/
│   │   └── README.md
│   └── transformers/         # Topic: "Transformers in AI"
│       ├── lessons/
│       └── README.md
│
└── learn-docker/
    ├── general/              # Topic: "Docker"
    ├── basics/               # Topic: "Docker basics"
    └── containers/           # Topic: "Containers in Docker"
```

### Topic Parsing Examples

| Topic Input | Directory Created |
|------------|-------------------|
| "AI" | `learn-ai/general/` |
| "Memory of AI" | `learn-ai/memory/` |
| "Docker basics" | `learn-docker/basics/` |
| "Containers in Docker" | `learn-docker/containers/` |

📖 **See [TWO_LEVEL_STRUCTURE.md](TWO_LEVEL_STRUCTURE.md) for complete directory structure guide.**

Each lesson includes:
- Learning Objectives
- Core Theory
- Intuition & Examples
- Common Pitfalls
- Exercises
- Further Reading

## Architecture

```
src/
├── config.py              # Environment configuration
├── models.py              # AgentState TypedDict
├── prompts.py             # LLM prompts
├── graph.py               # LangGraph workflow
├── nodes/                 # Pipeline steps
│   ├── setup_node.py      # Step 1: Repo setup
│   ├── research_node.py   # Step 2: Web research
│   ├── synthesis_node.py  # Step 3: Knowledge synthesis (Claude)
│   ├── writing_node.py    # Step 4: Lecture writing (Claude)
│   └── publish_node.py    # Step 5: Git publish
└── tools/                 # Utility modules
    ├── llm_client.py      # OpenAI + Anthropic clients
    ├── tavily_client.py   # Tavily search wrapper
    └── git_operations.py  # Git CLI operations
```

## Development

### Project Structure

- **CLAUDE.md** - Detailed documentation for Claude's role in the system
- **src/prompts.py** - All LLM prompts are centralized here for easy iteration
- **src/models.py** - AgentState schema (do not modify without updating CLAUDE.md)

### Running Tests

```bash
# Validate environment setup
python main.py --validate-only

# Test with a simple topic
python main.py --topic "Git Basics" --audience "beginners"
```

## How It Works

### Step 1: Setup
Creates output directory structure and initializes a git repository.

### Step 2: Research
- Searches the topic using Tavily API
- Uses OpenAI GPT-4o to synthesize search results into research notes

### Step 3: Knowledge Synthesis (Claude)
- Calls Claude Sonnet-4 to transform research into structured knowledge
- Builds concept maps and learning progressions
- Generates a lesson outline

### Step 4: Lecture Writing (Claude)
- For each lesson in the outline:
  - Calls Claude Sonnet-4 to write a complete, pedagogical lesson
  - Ensures professional teaching quality

### Step 5: Publishing
- Writes lessons to markdown files
- Creates a README
- Commits to git repository
- (Optional) Pushes to remote if configured

## License

MIT

## Credits

Built with:
- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent orchestration
- [OpenAI GPT-4o](https://openai.com/) - Planning and structuring
- [Anthropic Claude](https://www.anthropic.com/) - Knowledge synthesis and writing
- [Tavily](https://tavily.com/) - Web research
