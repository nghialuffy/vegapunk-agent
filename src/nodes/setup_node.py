"""
Step 1: Repository and Folder Setup

Creates the local directory structure and initializes git.
Can use existing repositories from a specified directory.

Supports two-level structure:
- "AI" → learn-ai/general/
- "Memory of AI" → learn-ai/memory/
- "Docker basics" → learn-docker/basics/
"""

from pathlib import Path
from src.models import AgentState
from src.config import Config
from src.tools.git_operations import init_repo, get_repo_info
from src.tools.state_persistence import check_resume_capability, load_state, load_existing_lessons
import re


def parse_topic(topic: str) -> tuple[str, str]:
    """
    Parse topic into main topic and subtopic.

    Examples:
        "AI" → ("ai", "general")
        "Memory of AI" → ("ai", "memory")
        "Docker basics" → ("docker", "basics")
        "AWS SAA" → ("aws-saa", "general")
        "Containers in Docker" → ("docker", "containers")

    Returns:
        (main_topic, subtopic)
    """
    topic_lower = topic.lower()

    # Patterns to detect main topic
    # Look for "X of Y" or "X in Y" patterns
    of_pattern = r'^(.+?)\s+of\s+(.+)$'
    in_pattern = r'^(.+?)\s+in\s+(.+)$'

    match = re.match(of_pattern, topic_lower)
    if match:
        subtopic = match.group(1).strip()
        main_topic = match.group(2).strip()
        return (sanitize_slug(main_topic), sanitize_slug(subtopic))

    match = re.match(in_pattern, topic_lower)
    if match:
        subtopic = match.group(1).strip()
        main_topic = match.group(2).strip()
        return (sanitize_slug(main_topic), sanitize_slug(subtopic))

    # Check if topic has multiple words - first word might be main topic
    # e.g., "Docker basics" → ("docker", "basics")
    words = topic_lower.split()
    if len(words) >= 2:
        # Common main topics (can be expanded)
        known_topics = {
            'ai', 'docker', 'kubernetes', 'k8s', 'aws', 'python', 'go', 'rust',
            'devops', 'security', 'algorithm', 'design', 'refactoring', 'pytest',
            'toeic', 'htb', 'prompt'
        }

        # Check if first word is a known topic
        first_word = words[0]
        if first_word in known_topics:
            main_topic = first_word
            subtopic = ' '.join(words[1:])
            return (sanitize_slug(main_topic), sanitize_slug(subtopic))

        # Check for compound topics like "AWS SAA"
        if len(words) == 2 and words[0] in known_topics:
            # This is likely a single topic, not main+sub
            return (sanitize_slug(topic_lower), "general")

    # Single word or unknown pattern - treat as main topic with "general" subtopic
    return (sanitize_slug(topic_lower), "general")


def sanitize_slug(text: str) -> str:
    """Convert text to a valid directory slug."""
    slug = text.lower()
    slug = slug.replace(' ', '-').replace('_', '-').replace('/', '-')
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug


def setup_node(state: AgentState) -> dict:
    """
    Create output directory and initialize git repository.

    Creates two-level structure: learn-{main-topic}/{subtopic}/

    Examples:
        "AI" → learn-ai/general/
        "Memory of AI" → learn-ai/memory/
        "Docker basics" → learn-docker/basics/

    Args:
        state: Current agent state

    Returns:
        Dictionary with repo_info update
    """
    print("\n[Step 1] Setting up repository and folders...")

    topic = state['topic']
    repo_dir = state.get('repo_dir')

    # Parse topic into main topic and subtopic
    main_topic, subtopic = parse_topic(topic)
    main_dir = f"learn-{main_topic}"

    print(f"  → Parsed topic: '{topic}'")
    print(f"    Main topic: {main_topic}")
    print(f"    Subtopic: {subtopic}")

    if repo_dir:
        # Use existing repository directory
        base_path = Path(repo_dir).expanduser().resolve()

        if not base_path.exists():
            raise ValueError(f"Repository directory does not exist: {base_path}")

        print(f"  → Using repository directory: {base_path}")

        # Create learn-{main-topic}/{subtopic} structure
        main_path = base_path / main_dir
        repo_path = main_path / subtopic

        # Create main topic directory if it doesn't exist
        if not main_path.exists():
            main_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Created main directory: {main_path}")
        else:
            print(f"  ✓ Using existing main directory: {main_path}")

        # Create subtopic directory
        if repo_path.exists():
            print(f"  ✓ Found existing subtopic: {repo_path}")
        else:
            repo_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Created subtopic directory: {repo_path}")
    else:
        # Use default output directory with same structure
        main_path = Config.OUTPUT_DIR / main_dir
        repo_path = main_path / subtopic

        main_path.mkdir(parents=True, exist_ok=True)
        repo_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created directory: {repo_path}")

    # Create subdirectories
    (repo_path / "lessons").mkdir(exist_ok=True)
    print(f"  ✓ Created lessons directory")

    # Initialize git repository if not already initialized
    if not (repo_path / ".git").exists():
        try:
            init_repo(repo_path)
            print(f"  ✓ Initialized git repository")
        except Exception as e:
            print(f"  ⚠ Git init warning: {e}")
    else:
        print(f"  ✓ Using existing git repository")

    # Get repository information
    repo_info = get_repo_info(repo_path)
    repo_info['lessons_dir'] = str(repo_path / "lessons")
    repo_info['main_topic'] = main_topic
    repo_info['subtopic'] = subtopic

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
