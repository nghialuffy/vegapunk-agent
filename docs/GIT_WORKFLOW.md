# Git Workflow Changes

## Summary

Updated the agent to **NOT run `git init`**. It now only performs `git add` and `git commit`.

## What Changed

### Before
```python
# setup_node.py automatically ran git init
if not (repo_path / ".git").exists():
    init_repo(repo_path)  # ← Ran 'git init'
    print(f"  ✓ Initialized git repository")
```

### After
```python
# setup_node.py only checks if git exists
if not (repo_path / ".git").exists():
    print(f"  ⚠ Warning: Not in a git repository. Commits will be skipped.")
    print(f"    To use git, run 'git init' in: {repo_path}")
else:
    print(f"  ✓ Using existing git repository")
```

## How to Use

### Option 1: Use existing git repository

If your `repo_dir` is already a git repository (has `.git/`), the agent will:
- ✅ Create the topic folder inside it
- ✅ Add files with `git add .`
- ✅ Commit with `git commit -m "..."`
- ✅ Push if remote is configured

Example:
```bash
# repo_dir is already a git repository
python main.py --repo-dir ~/Git/learn-ai
```

The agent creates `~/Git/learn-ai/my-topic/` and commits to the existing repo.

---

### Option 2: Initialize git manually

If the directory is NOT a git repository, you need to run `git init` first:

```bash
# Create the target directory
mkdir -p ~/Git/learn-ai
cd ~/Git/learn-ai

# Initialize git
git init

# Now run the agent
python main.py --repo-dir ~/Git/learn-ai
```

---

### Option 3: No git at all

If you don't want git:
```bash
python main.py
```

The agent will:
- ✅ Create files in `outputs/{topic}/`
- ⚠️ Skip git operations (just a warning, not an error)
- ✅ Files are still created normally

---

## Git Operations Flow

### In `setup_node.py` (Step 1)
```
1. Create directory structure
2. Check if .git exists
   - If YES → Print "Using existing git repository"
   - If NO → Print warning, continue anyway
```

### In `publish_node.py` (Step 5)
```
1. Write README.md
2. Run 'git add .'
3. Run 'git commit -m "..."'
4. If remote configured:
   - Run 'git push'
```

---

## Files Modified

- **src/nodes/setup_node.py**
  - Removed `init_repo()` call
  - Added warning if no git repository
  - Updated docstrings

- **src/tools/git_operations.py**
  - No changes (still has `init_repo()` function, just not called)

---

## Testing

### Test 1: Existing git repo
```bash
cd ~/Git/learn-ai
git init  # Only once
python /path/to/vegapunk-agent/main.py --repo-dir ~/Git/learn-ai
```

Expected:
```
[Step 1] Setting up repository and folders...
  ✓ Using existing git repository
...
[Step 5] Publishing to repository...
  ✓ Committed changes
```

---

### Test 2: No git repo
```bash
python main.py
```

Expected:
```
[Step 1] Setting up repository and folders...
  ⚠ Warning: Not in a git repository. Commits will be skipped.
    To use git, run 'git init' in: /path/to/outputs/topic
...
[Step 5] Publishing to repository...
  ⚠ Commit warning: [git error]
  → Files created but not committed
```

Files are still created, just not committed.

---

## Recommended Workflow

### For learn-ai repository

```bash
# 1. Navigate to your learn-ai directory
cd ~/Git/learn-ai

# 2. Make sure it's a git repo (only needed once)
git init
git remote add origin <your-github-url>

# 3. Run the agent
python /path/to/vegapunk-agent/main.py --repo-dir ~/Git/learn-ai

# 4. Agent will:
#    - Create topic folder
#    - Generate lessons
#    - git add .
#    - git commit -m "Add course: {topic}"
#    - git push (if remote configured)
```

---

## Benefits

✅ **No accidental git init** in wrong directories
✅ **Works with existing repos** (like learn-ai)
✅ **Cleaner control** over git operations
✅ **Still automatic commit/push** for convenience
✅ **Graceful degradation** if no git repo

---

## Migration Notes

If you were relying on automatic `git init`:

**Old workflow:**
```bash
python main.py  # Auto-created git repo
```

**New workflow:**
```bash
mkdir -p outputs/my-topic
cd outputs/my-topic
git init  # Manual init
cd ../..
python main.py
```

Or just use `--repo-dir` with an existing git repository.
