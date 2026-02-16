# Two-Level Directory Structure

The agent uses a two-level directory structure: `learn-{main-topic}/{subtopic}/`

This allows you to organize related courses under a main topic.

## Structure

```
repo-dir/
├── learn-ai/
│   ├── general/           # "AI"
│   ├── memory/            # "Memory of AI"
│   └── transformers/      # "Transformers in AI"
│
├── learn-docker/
│   ├── general/           # "Docker"
│   ├── basics/            # "Docker basics"
│   └── containers/        # "Containers in Docker"
│
└── learn-python/
    ├── general/           # "Python"
    ├── basics/            # "Python basics"
    └── async/             # "Python async"
```

## Topic Parsing

The agent automatically parses your topic into main topic and subtopic:

### Pattern 1: "X of Y"
```
"Memory of AI" → learn-ai/memory/
"Transformers of AI" → learn-ai/transformers/
"Basics of Docker" → learn-docker/basics/
```

### Pattern 2: "X in Y"
```
"Containers in Docker" → learn-docker/containers/
"Memory in AI" → learn-ai/memory/
"Async in Python" → learn-python/async/
```

### Pattern 3: "Known-Topic Subtopic"
```
"Docker basics" → learn-docker/basics/
"Python async" → learn-python/async/
"AI transformers" → learn-ai/transformers/
```

Known topics include: `ai`, `docker`, `kubernetes`, `aws`, `python`, `go`, `rust`, `devops`, `security`, etc.

### Pattern 4: Single Word/General
```
"AI" → learn-ai/general/
"Docker" → learn-docker/general/
"Kubernetes" → learn-kubernetes/general/
```

## Examples

### Example 1: AI Topics

```bash
# General AI
uv run python main.py --topic "AI" --repo-dir ~/Git
# → ~/Git/learn-ai/general/

# Memory in AI
uv run python main.py --topic "Memory of AI" --repo-dir ~/Git
# → ~/Git/learn-ai/memory/

# Transformers
uv run python main.py --topic "Transformers in AI" --repo-dir ~/Git
# → ~/Git/learn-ai/transformers/

# Result:
~/Git/learn-ai/
├── general/
│   ├── lessons/
│   └── README.md
├── memory/
│   ├── lessons/
│   └── README.md
└── transformers/
    ├── lessons/
    └── README.md
```

### Example 2: Docker Topics

```bash
# General Docker
uv run python main.py --topic "Docker" --repo-dir ~/Git
# → ~/Git/learn-docker/general/

# Docker basics
uv run python main.py --topic "Docker basics" --repo-dir ~/Git
# → ~/Git/learn-docker/basics/

# Containers
uv run python main.py --topic "Containers in Docker" --repo-dir ~/Git
# → ~/Git/learn-docker/containers/

# Result:
~/Git/learn-docker/
├── general/
├── basics/
└── containers/
```

### Example 3: Python Topics

```bash
uv run python main.py --topic "Python" --repo-dir ~/Git
# → ~/Git/learn-python/general/

uv run python main.py --topic "Python basics" --repo-dir ~/Git
# → ~/Git/learn-python/basics/

uv run python main.py --topic "Python async" --repo-dir ~/Git
# → ~/Git/learn-python/async/

# Result:
~/Git/learn-python/
├── general/
├── basics/
└── async/
```

## Console Output

When you run the agent, you'll see the parsing:

```bash
uv run python main.py --topic "Memory of AI" --repo-dir ~/Git

# Output:
[Step 1] Setting up repository and folders...
  → Parsed topic: 'Memory of AI'
    Main topic: ai
    Subtopic: memory
  → Using repository directory: /home/user/Git
  ✓ Using existing main directory: /home/user/Git/learn-ai
  ✓ Created subtopic directory: /home/user/Git/learn-ai/memory
  ✓ Created lessons directory
  ✓ Initialized git repository
  ✓ Setup complete
  → Repository: /home/user/Git/learn-ai/memory
```

## Directory Structure

Each subtopic directory is a complete course:

```
learn-{main-topic}/{subtopic}/
├── .git/                    # Git repository (per subtopic)
├── README.md                # Course overview
└── lessons/                 # Lesson files
    ├── lesson_01_*.md
    ├── lesson_02_*.md
    └── lesson_03_*.md
```

## Benefits

### 1. Organized by Main Topic
```
learn-ai/
├── general/
├── memory/
├── transformers/
├── nlp/
└── computer-vision/
```

All AI-related courses in one place!

### 2. Easy Navigation
```bash
cd ~/Git/learn-ai
ls
# general/  memory/  transformers/

cd memory
ls
# lessons/  README.md
```

### 3. Separate Git Repositories
Each subtopic has its own git history:
```bash
cd learn-ai/memory
git log  # Only commits for memory topic

cd ../transformers
git log  # Only commits for transformers topic
```

### 4. Scalable Structure
```
learn-docker/
├── general/
├── basics/
├── containers/
├── networking/
├── volumes/
├── compose/
├── swarm/
└── kubernetes/
```

## Topic Naming Tips

### Good Topic Names

For "X of Y" pattern:
```bash
--topic "Memory of AI"
--topic "Transformers of AI"
--topic "Basics of Docker"
--topic "Networking of Docker"
```

For "X in Y" pattern:
```bash
--topic "Memory in AI"
--topic "Containers in Docker"
--topic "Async in Python"
```

For known topic + subtopic:
```bash
--topic "Docker basics"
--topic "Python async"
--topic "AI transformers"
```

### Be Specific

Instead of:
```bash
--topic "Docker course"  # → learn-docker/course/
```

Use:
```bash
--topic "Docker basics"  # → learn-docker/basics/
--topic "Basics of Docker"  # → learn-docker/basics/
```

## Updating Existing Subtopics

Regenerate content for a specific subtopic:

```bash
# First generation
uv run python main.py --topic "Memory of AI" --repo-dir ~/Git
# → learn-ai/memory/ created

# Later: update with new content
uv run python main.py --topic "Memory of AI" --repo-dir ~/Git
# → learn-ai/memory/ updated (keeps git history)
```

## Complete Example Workflow

```bash
# Start with empty directory
cd ~/Git
mkdir -p ~/Git
ls
# (empty)

# Create AI courses
uv run python main.py --topic "AI" --repo-dir ~/Git
uv run python main.py --topic "Memory of AI" --repo-dir ~/Git
uv run python main.py --topic "Transformers in AI" --repo-dir ~/Git

# Check structure
tree -L 2 learn-ai
# learn-ai/
# ├── general/
# │   ├── lessons/
# │   └── README.md
# ├── memory/
# │   ├── lessons/
# │   └── README.md
# └── transformers/
#     ├── lessons/
#     └── README.md

# Add Docker courses
uv run python main.py --topic "Docker" --repo-dir ~/Git
uv run python main.py --topic "Docker basics" --repo-dir ~/Git
uv run python main.py --topic "Containers in Docker" --repo-dir ~/Git

# Final structure
ls -d learn-*/
# learn-ai/  learn-docker/

ls learn-ai/
# general/  memory/  transformers/

ls learn-docker/
# basics/  containers/  general/
```

## Parsing Reference

Quick reference for common topics:

| Input | Main Topic | Subtopic | Path |
|-------|-----------|----------|------|
| "AI" | ai | general | learn-ai/general/ |
| "Memory of AI" | ai | memory | learn-ai/memory/ |
| "Transformers in AI" | ai | transformers | learn-ai/transformers/ |
| "Docker" | docker | general | learn-docker/general/ |
| "Docker basics" | docker | basics | learn-docker/basics/ |
| "Containers in Docker" | docker | containers | learn-docker/containers/ |
| "Python" | python | general | learn-python/general/ |
| "Python async" | python | async | learn-python/async/ |
| "AWS SAA" | aws-saa | general | learn-aws-saa/general/ |
| "Security" | security | general | learn-security/general/ |

## Advanced: Custom Parsing

If the automatic parsing doesn't work as expected, use explicit patterns:

```bash
# Use "X of Y" pattern
--topic "Basics of Docker"    # → learn-docker/basics/
--topic "Memory of AI"         # → learn-ai/memory/

# Use "X in Y" pattern
--topic "Async in Python"      # → learn-python/async/
--topic "Volumes in Docker"    # → learn-docker/volumes/
```

## Migrating Existing Structure

If you have existing `learn-*` directories:

```bash
# Old structure
learn-docker/
├── lessons/
└── README.md

# Migrate to new structure
mkdir -p learn-docker/general
mv learn-docker/lessons learn-docker/general/
mv learn-docker/README.md learn-docker/general/

# New structure
learn-docker/
└── general/
    ├── lessons/
    └── README.md

# Now add more subtopics
uv run python main.py --topic "Docker basics" --repo-dir ~/Git
# → learn-docker/basics/
```
