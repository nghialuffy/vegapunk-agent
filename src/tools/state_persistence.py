"""
State persistence for resuming agent execution.

Saves and loads agent state to allow resuming from interruptions.
"""

import json
from pathlib import Path
from typing import Dict, Any


def save_state(repo_path: Path, state: Dict[str, Any]) -> None:
    """
    Save agent state to a JSON file.

    Args:
        repo_path: Path to the repository
        state: Agent state dictionary
    """
    state_file = repo_path / ".agent_state.json"

    # Create a serializable version of state
    # Handle both dict and list for lessons
    lessons_data = state.get("lessons", [])
    if isinstance(lessons_data, dict):
        completed_lessons = list(lessons_data.keys())
    elif isinstance(lessons_data, list):
        completed_lessons = lessons_data
    else:
        completed_lessons = []

    serializable_state = {
        "topic": state.get("topic"),
        "target_audience": state.get("target_audience"),
        "research_sources": state.get("research_sources", []),
        "raw_notes": state.get("raw_notes", ""),
        "knowledge_base": state.get("knowledge_base", ""),
        "lesson_outline": state.get("lesson_outline", []),
        "completed_lessons": completed_lessons,
    }

    state_file.write_text(json.dumps(serializable_state, indent=2), encoding='utf-8')


def load_state(repo_path: Path) -> Dict[str, Any]:
    """
    Load agent state from a JSON file.

    Args:
        repo_path: Path to the repository

    Returns:
        Dictionary with saved state, or empty dict if no state exists
    """
    state_file = repo_path / ".agent_state.json"

    if not state_file.exists():
        return {}

    try:
        return json.loads(state_file.read_text(encoding='utf-8'))
    except Exception as e:
        print(f"  ⚠ Warning: Could not load saved state: {e}")
        return {}


def check_resume_capability(repo_path: Path) -> Dict[str, bool]:
    """
    Check what can be resumed from existing state.

    Args:
        repo_path: Path to the repository

    Returns:
        Dictionary with flags for what can be resumed:
        {
            "has_state": bool,
            "can_skip_research": bool,
            "can_skip_synthesis": bool,
            "completed_lessons": list
        }
    """
    state_file = repo_path / ".agent_state.json"
    lessons_dir = repo_path / "lessons"

    resume_info = {
        "has_state": state_file.exists(),
        "can_skip_research": False,
        "can_skip_synthesis": False,
        "completed_lessons": []
    }

    if not state_file.exists():
        return resume_info

    try:
        saved_state = load_state(repo_path)

        # Can skip research if we have raw notes
        if saved_state.get("raw_notes"):
            resume_info["can_skip_research"] = True

        # Can skip synthesis if we have knowledge base
        if saved_state.get("knowledge_base"):
            resume_info["can_skip_synthesis"] = True

        # Find completed lessons
        if lessons_dir.exists():
            existing_lessons = [f.stem for f in lessons_dir.glob("lesson_*.md")]
            resume_info["completed_lessons"] = existing_lessons

        return resume_info

    except Exception:
        return resume_info


def load_existing_lessons(repo_path: Path) -> Dict[str, str]:
    """
    Load existing lesson files from disk.

    Args:
        repo_path: Path to the repository

    Returns:
        Dictionary mapping lesson keys to content
    """
    lessons_dir = repo_path / "lessons"
    lessons = {}

    if not lessons_dir.exists():
        return lessons

    for lesson_file in sorted(lessons_dir.glob("lesson_*.md")):
        lesson_key = lesson_file.stem
        content = lesson_file.read_text(encoding='utf-8')
        lessons[lesson_key] = content

    return lessons
