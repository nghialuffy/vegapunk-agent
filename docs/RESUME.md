# Resume Functionality

The agent can automatically resume from interruptions, skipping already completed steps and reusing existing content.

## How It Works

The agent saves its state to `.agent_state.json` in each course directory. When you re-run with the same topic, it automatically:

1. **Skips completed research** (Step 2) - Reuses saved Tavily results and OpenAI synthesis
2. **Skips completed synthesis** (Step 3) - Reuses saved Claude knowledge base
3. **Skips completed lessons** (Step 4) - Only writes missing lessons

## Automatic Resume

Just run the same command again:

```bash
# First run - generates 4 lessons, but crashes after lesson 2
uv run python main.py --topic "Memory of AI" --repo-dir ~/Git

# Second run - automatically resumes
uv run python main.py --topic "Memory of AI" --repo-dir ~/Git
```

The agent automatically detects what's already done and skips it!

## What Gets Saved

### After Step 2 (Research)
```json
{
  "topic": "Memory of AI",
  "target_audience": "intermediate developers",
  "research_sources": [...],
  "raw_notes": "..."
}
```

### After Step 3 (Synthesis)
```json
{
  "topic": "Memory of AI",
  "research_sources": [...],
  "raw_notes": "...",
  "knowledge_base": "...",
  "lesson_outline": ["Lesson 1", "Lesson 2", ...]
}
```

### After Each Lesson (Step 4)
```json
{
  "topic": "Memory of AI",
  "research_sources": [...],
  "raw_notes": "...",
  "knowledge_base": "...",
  "lesson_outline": [...],
  "completed_lessons": ["lesson_01_...", "lesson_02_..."]
}
```

## Example Scenarios

### Scenario 1: Interrupted During Lesson Writing

```bash
# First run - completes 2 out of 4 lessons, then crashes
uv run python main.py --topic "Docker basics" --repo-dir ~/Git

# Output:
# [Step 1] Setting up...
# [Step 2] Conducting research... ✓
# [Step 3] Synthesizing... ✓
# [Step 4] Writing lessons...
#   ✓ Completed lesson 1
#   ✓ Completed lesson 2
#   ✗ CRASH!

# Files created:
~/Git/learn-docker/basics/
├── .agent_state.json           # State saved
└── lessons/
    ├── lesson_01_introduction.md  # ✓ Exists
    └── lesson_02_containers.md    # ✓ Exists

# Second run - resumes automatically
uv run python main.py --topic "Docker basics" --repo-dir ~/Git

# Output:
# [Step 1] Setting up...
#   → Found existing state - checking what can be resumed...
#   ✓ Can resume: Skip research
#   ✓ Can resume: Skip synthesis
#   ✓ Can resume: Skip 2 completed lessons
#
# [Step 2] Conducting web research...
#   → Resuming: Using existing research notes
#   ✓ Loaded 5 sources
#   → Skipping Tavily search
#
# [Step 3] Synthesizing knowledge...
#   → Resuming: Using existing knowledge base
#   ✓ Loaded lesson outline (4 lessons)
#   → Skipping Claude synthesis
#
# [Step 4] Writing lessons...
#   → Found 2 existing lessons
#      ✓ lesson_01_introduction
#      ✓ lesson_02_containers
#   → Skipping lesson 1: Introduction (already exists)
#   → Skipping lesson 2: Containers (already exists)
#   → Writing lesson 3: Networking           # ← Continues here!
#   ✓ Completed lesson 3
#   → Writing lesson 4: Best Practices
#   ✓ Completed lesson 4
#
#   ✓ Summary:
#      Skipped: 2 existing lessons
#      Written: 2 new lessons
#      Total: 4 lessons
```

### Scenario 2: Update Specific Lessons

If you want to regenerate specific lessons, delete them and re-run:

```bash
# Delete lesson 3 to regenerate it
rm ~/Git/learn-docker/basics/lessons/lesson_03_*.md

# Run again
uv run python main.py --topic "Docker basics" --repo-dir ~/Git

# Output:
# [Step 4] Writing lessons...
#   → Found 3 existing lessons
#   → Skipping lesson 1: Introduction (already exists)
#   → Skipping lesson 2: Containers (already exists)
#   → Writing lesson 3: Networking           # ← Regenerated!
#   → Skipping lesson 4: Best Practices (already exists)
```

### Scenario 3: Fresh Start (Force Regeneration)

To start completely fresh, delete the state file:

```bash
# Delete state file
rm ~/Git/learn-docker/basics/.agent_state.json

# Run again - starts from scratch
uv run python main.py --topic "Docker basics" --repo-dir ~/Git

# Output:
# [Step 1] Setting up...
#   (no resume messages)
# [Step 2] Conducting web research...      # ← Starts fresh
#   → Searching for: Docker basics
#   ✓ Found 5 sources
```

## Console Output Examples

### With Resume Available

```bash
[Step 1] Setting up repository and folders...
  → Parsed topic: 'Memory of AI'
    Main topic: ai
    Subtopic: memory
  → Using repository directory: /home/user/Git
  ✓ Found existing repository: /home/user/Git/learn-ai/memory
  ✓ Created lessons directory
  ✓ Using existing git repository
  → Found existing state - checking what can be resumed...
  ✓ Can resume: Skip research (found saved notes)
  ✓ Can resume: Skip synthesis (found knowledge base)
  ✓ Can resume: Skip 2 completed lessons
  ✓ Setup complete

[Step 2] Conducting web research...
  → Resuming: Using existing research notes
  ✓ Loaded 5 sources
  ✓ Loaded research notes (4523 chars)
  → Skipping Tavily search and OpenAI synthesis

[Step 3] Synthesizing knowledge with Claude...
  → Resuming: Using existing knowledge base
  ✓ Loaded knowledge base (8234 chars)
  ✓ Loaded lesson outline (4 lessons):
     1. Introduction to Memory Systems
     2. Short-term vs Long-term Memory
     3. Memory Architectures
     4. Practical Applications
  → Skipping Claude synthesis

[Step 4] Writing lessons with Claude...
  → Found 2 existing lessons
     ✓ lesson_01_introduction_to_memory_systems
     ✓ lesson_02_short_term_vs_long_term_memory
  → Skipping lesson 1/4: Introduction to Memory Systems (already exists)
  → Skipping lesson 2/4: Short-term vs Long-term Memory (already exists)
  → Writing lesson 3/4: Memory Architectures
  ✓ Completed: Memory Architectures (6234 chars)
  ✓ Saved to: /home/user/Git/learn-ai/memory/lessons/lesson_03_memory_architectures.md
  → Writing lesson 4/4: Practical Applications
  ✓ Completed: Practical Applications (5823 chars)
  ✓ Saved to: /home/user/Git/learn-ai/memory/lessons/lesson_04_practical_applications.md

  ✓ Summary:
     Skipped: 2 existing lessons
     Written: 2 new lessons
     Total: 4 lessons
```

### Without Resume (Fresh Start)

```bash
[Step 1] Setting up repository and folders...
  → Parsed topic: 'Docker basics'
    Main topic: docker
    Subtopic: basics
  → Using repository directory: /home/user/Git
  ✓ Created repository: /home/user/Git/learn-docker/basics
  ✓ Created lessons directory
  ✓ Initialized git repository
  ✓ Setup complete

[Step 2] Conducting web research...
  → Searching for: Docker basics
  ✓ Found 5 sources
  → Synthesizing research notes with OpenAI...
  ✓ Generated research notes (5234 chars)

[Step 3] Synthesizing knowledge with Claude...
  → Calling Claude Sonnet-4 for synthesis...
  ✓ Generated knowledge base (8456 chars)
  ✓ Extracted lesson outline (4 lessons):
     1. Introduction
     2. Containers
     3. Images
     4. Docker Compose

[Step 4] Writing lessons with Claude...
  → Writing lesson 1/4: Introduction
  ✓ Completed: Introduction (5234 chars)
  ✓ Saved to: .../lesson_01_introduction.md
  ...
```

## Benefits

### 1. **Save Time**
- Skip expensive Tavily API calls (already done)
- Skip expensive Claude synthesis (already done)
- Only write missing lessons

### 2. **Save Money**
- No duplicate Tavily searches
- No duplicate Claude API calls
- Minimal token usage on resume

### 3. **Crash Protection**
- Internet disconnected? Resume where you left off
- Laptop battery died? Continue from last saved state
- API rate limit? Try again later, keep progress

### 4. **Iterative Development**
- Add more lessons to outline? Only new ones generated
- Update one lesson? Delete it and regenerate
- Refine knowledge base? Delete state and retry

## State File Location

```
learn-{topic}/{subtopic}/
├── .agent_state.json       # ← Resume state
├── README.md
└── lessons/
    ├── lesson_01_*.md
    └── lesson_02_*.md
```

The `.agent_state.json` file is:
- **Automatically created** after each step
- **Automatically loaded** when you re-run
- **JSON format** - human readable
- **Gitignored** - won't be committed
- **Safe to delete** - agent will start fresh

## Manual State Management

### View State

```bash
# Check what's saved
cat ~/Git/learn-ai/memory/.agent_state.json | jq
```

### Delete State (Fresh Start)

```bash
# Remove state file
rm ~/Git/learn-ai/memory/.agent_state.json

# Run again - starts from scratch
uv run python main.py --topic "Memory of AI" --repo-dir ~/Git
```

### Delete Specific Lesson

```bash
# Remove lesson 3
rm ~/Git/learn-ai/memory/lessons/lesson_03_*.md

# Run again - regenerates only lesson 3
uv run python main.py --topic "Memory of AI" --repo-dir ~/Git
```

### Regenerate Synthesis Only

```bash
# Keep research, regenerate synthesis and lessons
rm ~/Git/learn-ai/memory/.agent_state.json
rm ~/Git/learn-ai/memory/lessons/*.md

# Edit .agent_state.json to keep only research_sources and raw_notes
# Then run again
```

## Cost Savings Example

### Without Resume
```
First run (crashes after 2 lessons):
- Tavily: $0.01
- OpenAI: $0.10
- Claude synthesis: $0.50
- Claude lessons (2): $1.00
Total: $1.61

Second run (to finish):
- Tavily: $0.01        ← Duplicate!
- OpenAI: $0.10        ← Duplicate!
- Claude synthesis: $0.50  ← Duplicate!
- Claude lessons (2): $1.00
Total: $1.61

Grand total: $3.22
```

### With Resume
```
First run (crashes after 2 lessons):
- Tavily: $0.01
- OpenAI: $0.10
- Claude synthesis: $0.50
- Claude lessons (2): $1.00
Total: $1.61

Second run (resumes):
- Tavily: $0          ← Skipped!
- OpenAI: $0          ← Skipped!
- Claude synthesis: $0    ← Skipped!
- Claude lessons (2): $1.00
Total: $1.00

Grand total: $2.61 (saves $0.61 / 19%)
```

## Tips

### 1. **Let It Resume Automatically**
Don't delete state unless you specifically want to regenerate.

### 2. **Check Existing Lessons**
```bash
ls ~/Git/learn-docker/basics/lessons/
```

### 3. **Regenerate One Lesson**
```bash
rm ~/Git/learn-docker/basics/lessons/lesson_03_*.md
# Run again
```

### 4. **Fresh Start**
```bash
rm ~/Git/learn-docker/basics/.agent_state.json
# Run again
```

### 5. **Update Research Only**
```bash
# Keep lessons, regenerate research and synthesis
rm ~/Git/learn-docker/basics/.agent_state.json
# Research will be fresh, but existing lessons are preserved
```

## Summary

The resume feature:
- ✅ **Automatic** - Detects what can be skipped
- ✅ **Smart** - Only does necessary work
- ✅ **Safe** - Preserves existing content
- ✅ **Cost-effective** - Saves API calls
- ✅ **Transparent** - Shows what's being skipped

Just run the same command again, and the agent picks up where it left off!
