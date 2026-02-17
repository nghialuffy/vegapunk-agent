"""
Step 3: Knowledge Synthesis

Uses Claude to transform raw research into structured, teachable knowledge.
This is one of the two main Claude nodes.
Can resume from saved state to skip synthesis if already completed.
"""

from src.models import AgentState
from src.tools.llm_client import call_claude, extract_lesson_outline
from src.prompts import format_synthesis_prompt
from src.tools.state_persistence import save_state
from src.tools.token_utils import smart_truncate_for_prompt
from src.config import Config
from pathlib import Path


def synthesis_node(state: AgentState) -> dict:
    """
    Synthesize research into structured knowledge base using Claude.

    This is a CORE CLAUDE TASK - deep thinking and structuring.

    If saved state exists with knowledge base, skip this step.

    Args:
        state: Current agent state

    Returns:
        Dictionary with knowledge_base and lesson_outline updates
    """
    print("\n[Step 3] Synthesizing knowledge with Claude...")

    topic = state['topic']
    raw_notes = state['raw_notes']
    repo_info = state['repo_info']

    # Check if we can resume from saved state
    resume_info = repo_info.get('resume_info', {})
    saved_state = repo_info.get('saved_state', {})

    if resume_info.get('can_skip_synthesis'):
        print(f"  → Resuming: Using existing knowledge base")
        print(f"  ✓ Loaded knowledge base ({len(saved_state.get('knowledge_base', ''))} chars)")

        outline = saved_state.get('lesson_outline', [])
        print(f"  ✓ Loaded lesson outline ({len(outline)} lessons):")
        for i, lesson in enumerate(outline, 1):
            print(f"     {i}. {lesson}")
        print(f"  → Skipping Claude synthesis\n")

        return {
            "knowledge_base": saved_state.get('knowledge_base', ''),
            "lesson_outline": outline
        }

    # Perform new synthesis
    print(f"  → Calling Claude Sonnet-4 for synthesis...")

    # Truncate raw notes if needed
    truncated_notes, was_truncated = smart_truncate_for_prompt(
        raw_notes,
        Config.MAX_TOKENS_FOR_RAW_NOTES,
        "Raw research notes"
    )

    system_prompt, user_prompt = format_synthesis_prompt(
        topic=topic,
        raw_notes=truncated_notes
    )

    knowledge_base = call_claude(
        system_prompt,
        user_prompt,
        temperature=1.0,
        max_tokens=16000
    )

    print(f"  ✓ Generated knowledge base ({len(knowledge_base)} chars)")

    # Extract lesson outline from the synthesis
    lesson_outline = extract_lesson_outline(knowledge_base)
    print(f"  ✓ Extracted lesson outline ({len(lesson_outline)} lessons):")
    for i, lesson in enumerate(lesson_outline, 1):
        print(f"     {i}. {lesson}")

    print()

    # Save state for resume
    repo_path = Path(repo_info['path'])
    current_state = {
        "topic": state['topic'],
        "target_audience": state['target_audience'],
        "research_sources": state.get('research_sources', []),
        "raw_notes": raw_notes,
        "knowledge_base": knowledge_base,
        "lesson_outline": lesson_outline
    }
    save_state(repo_path, current_state)

    return {
        "knowledge_base": knowledge_base,
        "lesson_outline": lesson_outline
    }
