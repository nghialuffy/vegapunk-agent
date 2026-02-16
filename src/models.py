from typing import TypedDict, Dict, List, Any, Optional


class AgentState(TypedDict):
    """
    State schema for the Research & Teaching Agent.
    This follows the exact structure defined in CLAUDE.md.
    """
    # Input
    topic: str
    target_audience: str
    repo_dir: Optional[str]  # Optional: directory containing repositories to use

    # Step 1: Repo setup
    repo_info: Dict[str, Any]

    # Step 2: Research
    research_sources: List[Dict[str, str]]
    raw_notes: str

    # Step 3: Knowledge synthesis
    knowledge_base: str
    lesson_outline: List[str]

    # Step 4: Lecture writing
    lessons: Dict[str, str]

    # Step 5: GitHub push
    github_repo_url: str
