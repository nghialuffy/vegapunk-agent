# Directory Naming Pattern

The agent creates directories using the pattern: `learn-{topic}`

## Naming Convention

The agent automatically converts your topic into a directory name:

| Topic | Directory Name |
|-------|---------------|
| "AI" | `learn-ai` |
| "Algorithm" | `learn-algorithm` |
| "AWS SAA" | `learn-aws-saa` |
| "Design Pattern" | `learn-design-pattern` |
| "Prompt Engineering" | `learn-prompt-engineering` |
| "Python Basics" | `learn-python-basics` |

## How It Works

The conversion process:
1. Convert to lowercase
2. Replace spaces, underscores, and slashes with hyphens
3. Remove consecutive hyphens
4. Prefix with `learn-`

Examples:
```
"AI" → "ai" → "learn-ai"
"AWS SAA" → "aws-saa" → "learn-aws-saa"
"Design Pattern" → "design-pattern" → "learn-design-pattern"
"Python / Basics" → "python-basics" → "learn-python-basics"
```

## Using with --repo-dir

When you specify a repository directory, the agent creates/uses the `learn-{topic}` directory inside it:

```bash
# Your existing structure
~/courses/
├── learn-ai/
├── learn-algorithm/
├── learn-aws-saa/
└── learn-design-pattern/

# Generate new course
uv run python main.py --topic "Docker" --repo-dir ~/courses

# Creates
~/courses/
├── learn-ai/
├── learn-algorithm/
├── learn-aws-saa/
├── learn-design-pattern/
└── learn-docker/          # ← New!
    ├── lessons/
    │   ├── lesson_01_*.md
    │   └── lesson_02_*.md
    └── README.md
```

## Updating Existing Courses

The agent will use existing directories if they match:

```bash
# First time - creates directory
uv run python main.py --topic "AI" --repo-dir ~/courses
# Creates: ~/courses/learn-ai/

# Later - updates existing
uv run python main.py --topic "AI" --repo-dir ~/courses
# Uses: ~/courses/learn-ai/ (existing)
# Keeps git history, updates content
```

## Examples

### Example 1: Match Your Existing Structure

```bash
# You have:
~/Git/
├── learn-ai/
├── learn-algorithm/
├── learn-docker/
└── learn-security/

# Generate course
uv run python main.py --topic "Kubernetes" --repo-dir ~/Git

# Result:
~/Git/
├── learn-ai/
├── learn-algorithm/
├── learn-docker/
├── learn-kubernetes/  # ← Created with learn- prefix
└── learn-security/
```

### Example 2: Multiple Related Topics

```bash
uv run python main.py --topic "Python Basics" --repo-dir ~/courses
# → ~/courses/learn-python-basics/

uv run python main.py --topic "Python Advanced" --repo-dir ~/courses
# → ~/courses/learn-python-advanced/

uv run python main.py --topic "Python Async" --repo-dir ~/courses
# → ~/courses/learn-python-async/
```

### Example 3: Update Existing

```bash
# You already have ~/Git/learn-docker/
# Want to regenerate content

uv run python main.py --topic "Docker" --repo-dir ~/Git
# Uses existing: ~/Git/learn-docker/
# Keeps .git history
# Updates lessons
```

## Directory Structure

Each `learn-{topic}` directory contains:

```
learn-{topic}/
├── .git/              # Git repository
├── README.md          # Course overview
└── lessons/           # Lesson files
    ├── lesson_01_*.md
    ├── lesson_02_*.md
    └── lesson_03_*.md
```

## Tips

### 1. Consistent Naming

Keep topic names consistent to reuse directories:

```bash
# First generation
uv run python main.py --topic "AI" --repo-dir ~/courses
# → learn-ai/

# Update later (same topic name)
uv run python main.py --topic "AI" --repo-dir ~/courses
# → Reuses learn-ai/
```

### 2. Avoid Special Characters

For best results, use simple topic names:

```bash
# Good
--topic "Docker"
--topic "AWS SAA"
--topic "Design Pattern"

# Works but creates longer names
--topic "Advanced Docker Orchestration"
# → learn-advanced-docker-orchestration/
```

### 3. Check Existing Directories

Before generating, see what you already have:

```bash
ls -d ~/courses/learn-*/
```

## Complete Example

```bash
# Your current structure
cd ~/Git
ls -d learn-*/
# learn-ai
# learn-algorithm
# learn-docker

# Add new course
uv run python main.py --topic "Kubernetes" --repo-dir ~/Git

# Output shows:
# [Step 1] Setting up repository and folders...
#   → Using repository directory: /home/user/Git
#   ✓ Created repository: /home/user/Git/learn-kubernetes
#   ✓ Created lessons directory
#   ✓ Initialized git repository
#   ✓ Setup complete
#   → Repository: /home/user/Git/learn-kubernetes

# New structure
ls -d learn-*/
# learn-ai
# learn-algorithm
# learn-docker
# learn-kubernetes  ← New!

# Check the new course
ls learn-kubernetes/
# lessons/  README.md
```

## Naming Reference

Quick reference for common topics:

| Input Topic | Output Directory |
|------------|------------------|
| AI | learn-ai |
| Docker | learn-docker |
| Kubernetes | learn-kubernetes |
| AWS SAA | learn-aws-saa |
| Python Basics | learn-python-basics |
| Design Pattern | learn-design-pattern |
| DevOps | learn-devops |
| Security | learn-security |
| Algorithm | learn-algorithm |
| Go | learn-go |
| Pytest | learn-pytest |
| Refactoring | learn-refactoring |
| Prompt Engineering | learn-prompt-engineering |
