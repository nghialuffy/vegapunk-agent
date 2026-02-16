# Directory Structure

The agent creates a single folder for each topic using a sanitized slug.

## Structure

```
repo-dir/
├── ai/                    # "AI"
├── memory-of-ai/          # "Memory of AI"
├── transformers-in-ai/    # "Transformers in AI"
├── docker/                # "Docker"
├── docker-basics/         # "Docker basics"
├── containers-in-docker/  # "Containers in Docker"
└── python-async/          # "Python async"
```

## Topic to Directory Mapping

The agent converts topics into directory-safe slugs:

### Examples
```
"AI" → ai/
"Memory of AI" → memory-of-ai/
"Transformers of AI" → transformers-of-ai/
"Docker basics" → docker-basics/
"Containers in Docker" → containers-in-docker/
"Python async" → python-async/
"AWS SAA" → aws-saa/
```

### Sanitization Rules
- Convert to lowercase
- Replace spaces with hyphens
- Replace underscores and slashes with hyphens
- Remove multiple consecutive hyphens
- Trim leading/trailing hyphens

## Examples

### Example 1: AI Topics

```bash
# General AI
uv run python main.py --topic "AI" --repo-dir ~/Git
# → ~/Git/ai/

# Memory in AI
uv run python main.py --topic "Memory of AI" --repo-dir ~/Git
# → ~/Git/memory-of-ai/

# Transformers
uv run python main.py --topic "Transformers in AI" --repo-dir ~/Git
# → ~/Git/transformers-in-ai/

# Result:
~/Git/
├── ai/
│   ├── lessons/
│   └── README.md
├── memory-of-ai/
│   ├── lessons/
│   └── README.md
└── transformers-in-ai/
    ├── lessons/
    └── README.md
```

### Example 2: Docker Topics

```bash
# General Docker
uv run python main.py --topic "Docker" --repo-dir ~/Git
# → ~/Git/docker/

# Docker basics
uv run python main.py --topic "Docker basics" --repo-dir ~/Git
# → ~/Git/docker-basics/

# Containers
uv run python main.py --topic "Containers in Docker" --repo-dir ~/Git
# → ~/Git/containers-in-docker/

# Result:
~/Git/
├── docker/
├── docker-basics/
└── containers-in-docker/
```

### Example 3: Python Topics

```bash
uv run python main.py --topic "Python" --repo-dir ~/Git
# → ~/Git/python/

uv run python main.py --topic "Python basics" --repo-dir ~/Git
# → ~/Git/python-basics/

uv run python main.py --topic "Python async" --repo-dir ~/Git
# → ~/Git/python-async/

# Result:
~/Git/
├── python/
├── python-basics/
└── python-async/
```

## Console Output

When you run the agent, you'll see the directory created:

```bash
uv run python main.py --topic "Memory of AI" --repo-dir ~/Git

# Output:
[Step 1] Setting up repository and folders...
  → Topic: 'Memory of AI'
    Directory: memory-of-ai
  → Using repository directory: /home/user/Git
  ✓ Created directory: /home/user/Git/memory-of-ai
  ✓ Created lessons directory
  ✓ Initialized git repository
  ✓ Setup complete
  → Repository: /home/user/Git/memory-of-ai
```

## Directory Structure

Each topic directory is a complete course:

```
{topic-slug}/
├── .git/                    # Git repository
├── README.md                # Course overview
└── lessons/                 # Lesson files
    ├── lesson_01_*.md
    ├── lesson_02_*.md
    └── lesson_03_*.md
```

## Benefits

### 1. Simple and Clear
Each topic gets its own folder with a descriptive name.

### 2. Easy Navigation
```bash
cd ~/Git
ls
# ai/  docker/  memory-of-ai/  python-async/

cd memory-of-ai
ls
# lessons/  README.md
```

### 3. Independent Git Repositories
Each topic has its own git history:
```bash
cd memory-of-ai
git log  # Only commits for this topic

cd ../python-async
git log  # Only commits for Python async
```

### 4. Flexible Organization
Organize topics however you want:
```
~/Git/
├── ai/
├── docker/
├── python/
├── memory-of-ai/
├── docker-basics/
├── python-async/
└── aws-saa/
```

## Topic Naming Tips

### Topic Examples

```bash
--topic "AI"
--topic "Memory of AI"
--topic "Docker basics"
--topic "Python async"
--topic "Containers in Docker"
--topic "AWS SAA"
```

All topics are converted to directory-safe slugs automatically.

## Updating Existing Topics

Regenerate content for a specific topic:

```bash
# First generation
uv run python main.py --topic "Memory of AI" --repo-dir ~/Git
# → memory-of-ai/ created

# Later: update with new content
uv run python main.py --topic "Memory of AI" --repo-dir ~/Git
# → memory-of-ai/ updated (keeps git history)
```

## Complete Example Workflow

```bash
# Start with empty directory
cd ~/Git
ls
# (empty)

# Create AI courses
uv run python main.py --topic "AI" --repo-dir ~/Git
uv run python main.py --topic "Memory of AI" --repo-dir ~/Git
uv run python main.py --topic "Transformers in AI" --repo-dir ~/Git

# Check structure
ls
# ai/  memory-of-ai/  transformers-in-ai/

# Add Docker courses
uv run python main.py --topic "Docker" --repo-dir ~/Git
uv run python main.py --topic "Docker basics" --repo-dir ~/Git
uv run python main.py --topic "Containers in Docker" --repo-dir ~/Git

# Final structure
ls
# ai/  docker/  docker-basics/  containers-in-docker/  memory-of-ai/  transformers-in-ai/
```

## Topic to Directory Reference

Quick reference for common topics:

| Input | Directory Path |
|-------|----------------|
| "AI" | ai/ |
| "Memory of AI" | memory-of-ai/ |
| "Transformers in AI" | transformers-in-ai/ |
| "Docker" | docker/ |
| "Docker basics" | docker-basics/ |
| "Containers in Docker" | containers-in-docker/ |
| "Python" | python/ |
| "Python async" | python-async/ |
| "AWS SAA" | aws-saa/ |
| "Security" | security/ |

## Directory Naming

The agent automatically converts your topic into a safe directory name.

All spaces are converted to hyphens, and special characters are removed.

```bash
# Examples
"Memory of AI" → memory-of-ai/
"Docker Basics" → docker-basics/
"AWS SAA" → aws-saa/
"My Cool Topic!" → my-cool-topic/
```
