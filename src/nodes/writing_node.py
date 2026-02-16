"""
Step 4: Lecture Writing

Uses Claude to write complete, high-quality lessons.
This is one of the two main Claude nodes.

Writes lessons to files immediately as they are generated.
Can resume from existing lessons - only writes missing ones.
"""

from pathlib import Path
from src.models import AgentState
from src.tools.llm_client import call_claude
from src.prompts import format_lecture_prompt
from src.tools.state_persistence import load_existing_lessons, save_state


def writing_node(state: AgentState) -> dict:
    """
    Write complete lessons using Claude.

    This is a CORE CLAUDE TASK - pedagogical writing at the highest quality.

    Writes each lesson to a file immediately after generation so progress is saved.
    Skips lessons that already exist on disk.

    Args:
        state: Current agent state

    Returns:
        Dictionary with lessons update
    """
    print("\n[Step 4] Writing lessons with Claude...")

    topic = state['topic']
    target_audience = state['target_audience']
    knowledge_base = state['knowledge_base']
    lesson_outline = state['lesson_outline']
    repo_info = state['repo_info']

    # Get lessons directory from repo_info
    lessons_dir = Path(repo_info['lessons_dir'])
    repo_path = Path(repo_info['path'])

    # Load existing lessons
    existing_lessons = load_existing_lessons(repo_path)

    if existing_lessons:
        print(f"  → Found {len(existing_lessons)} existing lessons")
        for lesson_key in sorted(existing_lessons.keys()):
            print(f"     ✓ {lesson_key}")

    lessons = {}
    skipped_count = 0
    written_count = 0

    for i, lesson_title in enumerate(lesson_outline, 1):
        lesson_key = f"lesson_{i:02d}_{sanitize_filename(lesson_title)}"

        # Check if lesson already exists
        if lesson_key in existing_lessons:
            print(f"  → Skipping lesson {i}/{len(lesson_outline)}: {lesson_title} (already exists)")
            lessons[lesson_key] = existing_lessons[lesson_key]
            skipped_count += 1
            continue

        # Write new lesson
        print(f"  → Writing lesson {i}/{len(lesson_outline)}: {lesson_title}")

        # Call Claude for each lesson
        system_prompt, user_prompt = format_lecture_prompt(
            topic=topic,
            lesson_title=lesson_title,
            target_audience=target_audience,
            knowledge_base=knowledge_base
        )

        lesson_content = call_claude(
            system_prompt,
            user_prompt,
            temperature=1.0,
            max_tokens=16000
        )

        # Store lesson
        lessons[lesson_key] = lesson_content

        # Write to file immediately
        lesson_path = lessons_dir / f"{lesson_key}.md"
        lesson_path.write_text(lesson_content, encoding='utf-8')

        print(f"  ✓ Completed: {lesson_title} ({len(lesson_content)} chars)")
        print(f"  ✓ Saved to: {lesson_path}")
        written_count += 1

        # Save state after each lesson
        current_state = {
            "topic": topic,
            "target_audience": target_audience,
            "research_sources": state.get('research_sources', []),
            "raw_notes": state.get('raw_notes', ''),
            "knowledge_base": knowledge_base,
            "lesson_outline": lesson_outline,
            "lessons": list(lessons.keys())
        }
        save_state(repo_path, current_state)

    print(f"\n  ✓ Summary:")
    if skipped_count > 0:
        print(f"     Skipped: {skipped_count} existing lessons")
    if written_count > 0:
        print(f"     Written: {written_count} new lessons")
    print(f"     Total: {len(lessons)} lessons\n")

    return {
        "lessons": lessons
    }


def sanitize_filename(title: str) -> str:
    """Convert lesson title to a valid filename."""
    # Replace spaces and special characters
    filename = title.lower()
    filename = filename.replace(' ', '_')
    filename = ''.join(c for c in filename if c.isalnum() or c == '_')
    return filename[:50]  # Limit length
