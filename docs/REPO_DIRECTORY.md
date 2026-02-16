# Using Custom Repository Directories

This guide explains how to use the `--repo-dir` parameter to organize your generated courses in a specific directory.

## Why Use --repo-dir?

By default, the agent creates courses in the `outputs/` directory. Using `--repo-dir` allows you to:

✅ **Organize all courses in one place** - Keep your generated content organized
✅ **Use existing repositories** - Update courses in existing git repos
✅ **Custom storage location** - Store courses anywhere on your system
✅ **Multiple collections** - Separate personal vs work courses, etc.

## Basic Usage

```bash
uv run python main.py --topic "Your Topic" --repo-dir /path/to/directory
```

## Examples

### Example 1: Create a Courses Directory

```bash
# Create your courses directory
mkdir -p ~/my-courses

# Generate courses there
uv run python main.py \
  --topic "Introduction to LangGraph" \
  --repo-dir ~/my-courses

uv run python main.py \
  --topic "Python Async Programming" \
  --repo-dir ~/my-courses

uv run python main.py \
  --topic "Docker Basics" \
  --repo-dir ~/my-courses
```

This creates:
```
~/my-courses/
├── introduction-to-langgraph/
│   ├── README.md
│   └── lessons/
├── python-async-programming/
│   ├── README.md
│   └── lessons/
└── docker-basics/
    ├── README.md
    └── lessons/
```

### Example 2: Separate Collections

```bash
# Personal learning
mkdir -p ~/personal-courses
uv run python main.py \
  --topic "Advanced TypeScript" \
  --repo-dir ~/personal-courses

# Work training materials
mkdir -p ~/work-training
uv run python main.py \
  --topic "Internal API Documentation" \
  --repo-dir ~/work-training
```

### Example 3: Update Existing Repository

If you already have a repository and want to regenerate/update the lessons:

```bash
# First run creates the repository
uv run python main.py \
  --topic "Git Basics" \
  --repo-dir ~/courses

# Later, regenerate with updated content
uv run python main.py \
  --topic "Git Basics" \
  --repo-dir ~/courses
```

The agent will:
- Use the existing `~/courses/git-basics/` directory
- Keep existing git history
- Overwrite lesson files with new content
- Create a new commit with the updates

### Example 4: Shared Team Directory

```bash
# Shared directory (network drive, Dropbox, etc.)
uv run python main.py \
  --topic "Team Onboarding" \
  --repo-dir /mnt/shared/training-materials
```

## How It Works

### Without --repo-dir (Default)

```bash
uv run python main.py --topic "Python Basics"
```

Creates:
```
vegapunk-agent/
└── outputs/
    └── python-basics/
        ├── README.md
        └── lessons/
```

### With --repo-dir

```bash
uv run python main.py --topic "Python Basics" --repo-dir ~/courses
```

Creates:
```
~/courses/
└── python-basics/
    ├── README.md
    └── lessons/
```

## Directory Naming

The agent creates a subdirectory based on the topic name:

| Topic | Directory Name |
|-------|---------------|
| "Introduction to LangGraph" | `introduction-to-langgraph` |
| "Python Async Programming" | `python-async-programming` |
| "Docker Basics" | `docker-basics` |
| "Advanced TypeScript" | `advanced-typescript` |

The conversion:
1. Converts to lowercase
2. Replaces spaces with hyphens
3. Replaces slashes with hyphens

## Git Repository Behavior

### New Directory
If the course directory doesn't exist:
```
[Step 1] Setting up repository and folders...
  → Using repository directory: /home/user/courses
  ✓ Created repository: /home/user/courses/python-basics
  ✓ Created lessons directory
  ✓ Initialized git repository
  ✓ Setup complete
```

### Existing Directory (No Git)
If directory exists but isn't a git repository:
```
[Step 1] Setting up repository and folders...
  → Using repository directory: /home/user/courses
  ✓ Found existing repository: /home/user/courses/python-basics
  ✓ Created lessons directory
  ✓ Initialized git repository
  ✓ Setup complete
```

### Existing Git Repository
If directory exists and is already a git repo:
```
[Step 1] Setting up repository and folders...
  → Using repository directory: /home/user/courses
  ✓ Found existing repository: /home/user/courses/python-basics
  ✓ Created lessons directory
  ✓ Using existing git repository
  ✓ Setup complete
```

## Error Handling

### Directory Doesn't Exist

```bash
uv run python main.py \
  --topic "Python Basics" \
  --repo-dir /nonexistent/path
```

Error:
```
Repository directory does not exist: /nonexistent/path
```

**Solution**: Create the directory first:
```bash
mkdir -p /path/to/directory
uv run python main.py --topic "Python Basics" --repo-dir /path/to/directory
```

### Permission Issues

If you don't have write permissions:
```
Permission denied: /path/to/directory
```

**Solution**: Use a directory you have write access to, or fix permissions:
```bash
chmod u+w /path/to/directory
```

## Best Practices

### 1. Use Absolute Paths

```bash
# Good - absolute path
uv run python main.py --topic "Topic" --repo-dir /home/user/courses

# Also good - uses ~ expansion
uv run python main.py --topic "Topic" --repo-dir ~/courses

# Avoid - relative paths can be confusing
uv run python main.py --topic "Topic" --repo-dir ../courses
```

### 2. Create Directory First

```bash
# Create parent directory before first use
mkdir -p ~/my-courses

# Then generate courses
uv run python main.py --topic "Topic 1" --repo-dir ~/my-courses
uv run python main.py --topic "Topic 2" --repo-dir ~/my-courses
```

### 3. Consistent Directory Structure

Use the same `--repo-dir` for related courses:

```bash
# All Python courses in one place
PYTHON_DIR=~/courses/python

mkdir -p $PYTHON_DIR
uv run python main.py --topic "Python Basics" --repo-dir $PYTHON_DIR
uv run python main.py --topic "Python Advanced" --repo-dir $PYTHON_DIR
uv run python main.py --topic "Python Async" --repo-dir $PYTHON_DIR
```

### 4. Environment Variable

Set a default repository directory:

```bash
# In your .bashrc or .zshrc
export COURSE_DIR=~/my-courses

# Then use it
uv run python main.py --topic "Topic" --repo-dir $COURSE_DIR
```

Or create a wrapper script:

```bash
#!/bin/bash
# ~/bin/gen-course

COURSE_DIR=~/my-courses
uv run python /path/to/vegapunk-agent/main.py \
  --repo-dir "$COURSE_DIR" \
  "$@"
```

Usage:
```bash
gen-course --topic "Docker Basics"
```

## Combining with Other Options

```bash
# Custom directory + custom audience
uv run python main.py \
  --topic "Advanced Docker" \
  --audience "DevOps engineers" \
  --repo-dir ~/courses/devops

# Multiple options
uv run python main.py \
  --topic "React Hooks" \
  --audience "frontend developers" \
  --repo-dir ~/courses/frontend
```

## File Structure Example

After generating multiple courses:

```
~/my-courses/
├── introduction-to-langgraph/
│   ├── .git/
│   ├── README.md
│   └── lessons/
│       ├── lesson_01_fundamentals.md
│       ├── lesson_02_core_concepts.md
│       └── lesson_03_advanced_topics.md
│
├── python-async-programming/
│   ├── .git/
│   ├── README.md
│   └── lessons/
│       ├── lesson_01_introduction.md
│       ├── lesson_02_async_await.md
│       └── lesson_03_asyncio.md
│
└── docker-basics/
    ├── .git/
    ├── README.md
    └── lessons/
        ├── lesson_01_containers.md
        ├── lesson_02_images.md
        └── lesson_03_docker_compose.md
```

Each course is:
- A separate git repository
- Self-contained with its own README
- Independently versioned
- Organized under one parent directory

## Advanced: Scripted Course Generation

Generate multiple courses at once:

```bash
#!/bin/bash
# generate-course-series.sh

REPO_DIR=~/courses/python-fundamentals

topics=(
  "Python Basics"
  "Python Data Structures"
  "Python Functions"
  "Python OOP"
  "Python Modules"
)

for topic in "${topics[@]}"; do
  echo "Generating: $topic"
  uv run python main.py \
    --topic "$topic" \
    --audience "Python beginners" \
    --repo-dir "$REPO_DIR"
  echo "---"
done
```

## Summary

The `--repo-dir` parameter gives you complete control over where your generated courses are stored:

- ✅ Organize courses in custom directories
- ✅ Update existing repositories
- ✅ Separate different course collections
- ✅ Use network/shared storage
- ✅ Keep consistent project structure

**Quick Reference:**
```bash
# Default (outputs directory)
uv run python main.py --topic "Topic"

# Custom directory
uv run python main.py --topic "Topic" --repo-dir ~/courses

# Update existing
uv run python main.py --topic "Topic" --repo-dir ~/courses
```
