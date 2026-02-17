"""
Step 1: Repository and Folder Setup

Creates the local directory structure. Assumes git repository is already initialized.
Can use existing repositories from a specified directory.

Creates a single folder based on topic:
- "AI" → ai/
- "Memory of AI" → memory-of-ai/
- "Docker basics" → docker-basics/

Note: Does NOT run 'git init'. If you need git, run 'git init' in the target directory first.
"""

from pathlib import Path
from src.models import AgentState
from src.config import Config
from src.tools.git_operations import get_repo_info
from src.tools.state_persistence import check_resume_capability, load_state, load_existing_lessons
import re


def create_topic_slug(topic: str) -> str:
    """
    Convert topic into a sanitized directory slug.

    Examples:
        "AI" → "ai"
        "Memory of AI" → "memory-of-ai"
        "Docker basics" → "docker-basics"
        "AWS SAA" → "aws-saa"
        "Containers in Docker" → "containers-in-docker"

    Returns:
        Sanitized slug for the topic
    """
    return sanitize_slug(topic.lower())


def sanitize_slug(text: str) -> str:
    """Convert text to a valid directory slug."""
    slug = text.lower()
    slug = slug.replace(' ', '-').replace('_', '-').replace('/', '-')
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug


def setup_node(state: AgentState) -> dict:
    """
    Create output directory and prepare for git operations.

    Creates single-level structure based on topic slug.
    Does NOT run 'git init' - assumes repository is already initialized.

    Examples:
        "AI" → ai/
        "Memory of AI" → memory-of-ai/
        "Docker basics" → docker-basics/

    Args:
        state: Current agent state

    Returns:
        Dictionary with repo_info update
    """
    print("\n[Step 1] Setting up repository and folders...")

    topic = state['topic']
    repo_dir = state.get('repo_dir')

    # Create topic slug for directory name
    topic_slug = create_topic_slug(topic)

    print(f"  → Topic: '{topic}'")
    print(f"    Directory: {topic_slug}")

    if repo_dir:
        # Use existing repository directory
        base_path = Path(repo_dir).expanduser().resolve()

        if not base_path.exists():
            raise ValueError(f"Repository directory does not exist: {base_path}")

        print(f"  → Using repository directory: {base_path}")

        # Create topic directory
        repo_path = base_path / topic_slug

        if repo_path.exists():
            print(f"  ✓ Found existing directory: {repo_path}")
        else:
            repo_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Created directory: {repo_path}")
    else:
        # Use default output directory
        repo_path = Config.OUTPUT_DIR / topic_slug

        repo_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created directory: {repo_path}")

    # Create subdirectories
    (repo_path / "lessons").mkdir(exist_ok=True)
    print(f"  ✓ Created lessons directory")

    # Check if we're in a git repository
    if not (repo_path / ".git").exists():
        print(f"  ⚠ Warning: Not in a git repository. Commits will be skipped.")
        print(f"    To use git, run 'git init' in: {repo_path}")
    else:
        print(f"  ✓ Using existing git repository")

    # Get repository information
    repo_info = get_repo_info(repo_path)
    repo_info['lessons_dir'] = str(repo_path / "lessons")
    repo_info['topic_slug'] = topic_slug

    # Check if we can resume from existing state
    resume_info = check_resume_capability(repo_path)

    if resume_info["has_state"]:
        print(f"  → Found existing state - checking what can be resumed...")

        saved_state = load_state(repo_path)

        if resume_info["can_skip_research"]:
            print(f"  ✓ Can resume: Skip research (found saved notes)")

        if resume_info["can_skip_synthesis"]:
            print(f"  ✓ Can resume: Skip synthesis (found knowledge base)")

        if resume_info["completed_lessons"]:
            print(f"  ✓ Can resume: Skip {len(resume_info['completed_lessons'])} completed lessons")

        repo_info['resume_info'] = resume_info
        repo_info['saved_state'] = saved_state
    else:
        repo_info['resume_info'] = resume_info
        repo_info['saved_state'] = {}

    print(f"  ✓ Setup complete")
    print(f"  → Repository: {repo_path}\n")

    return {
        "repo_info": repo_info
    }
