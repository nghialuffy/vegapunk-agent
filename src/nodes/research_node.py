"""
Step 2: Web Research

Uses Tavily to search for information and OpenAI to synthesize research notes.
Can resume from saved state to skip research if already completed.
"""

from src.models import AgentState
from src.tools.tavily_client import search_topic, format_search_results, extract_sources
from src.tools.llm_client import call_openai
from src.prompts import format_research_synthesis_prompt
from src.tools.state_persistence import save_state
from src.tools.token_utils import smart_truncate_for_prompt
from src.config import Config
from pathlib import Path


def research_node(state: AgentState) -> dict:
    """
    Perform web research using Tavily and synthesize notes using OpenAI.

    If saved state exists with research notes, skip this step.

    Args:
        state: Current agent state

    Returns:
        Dictionary with research_sources and raw_notes updates
    """
    print("\n[Step 2] Conducting web research...")

    topic = state['topic']
    target_audience = state['target_audience']
    repo_info = state['repo_info']

    # Check if we can resume from saved state
    resume_info = repo_info.get('resume_info', {})
    saved_state = repo_info.get('saved_state', {})

    if resume_info.get('can_skip_research'):
        print(f"  → Resuming: Using existing research notes")
        print(f"  ✓ Loaded {len(saved_state.get('research_sources', []))} sources")
        print(f"  ✓ Loaded research notes ({len(saved_state.get('raw_notes', ''))} chars)")
        print(f"  → Skipping Tavily search and OpenAI synthesis\n")

        return {
            "research_sources": saved_state.get('research_sources', []),
            "raw_notes": saved_state.get('raw_notes', '')
        }

    # Perform new research
    print(f"  → Searching for: {topic}")
    search_response = search_topic(topic)

    # Extract sources
    sources = extract_sources(search_response)
    print(f"  ✓ Found {len(sources)} sources")

    # Format search results
    formatted_results = format_search_results(search_response)

    # Truncate if needed to fit token limits
    formatted_results, was_truncated = smart_truncate_for_prompt(
        formatted_results,
        Config.MAX_TOKENS_FOR_RAW_NOTES,
        "Search results"
    )

    # Synthesize research notes using OpenAI
    print(f"  → Synthesizing research notes with OpenAI...")
    system_prompt, user_prompt = format_research_synthesis_prompt(
        topic=topic,
        target_audience=target_audience,
        search_results=formatted_results
    )

    raw_notes = call_openai(system_prompt, user_prompt, temperature=0.7)
    print(f"  ✓ Generated research notes ({len(raw_notes)} chars)\n")

    # Save state for resume
    repo_path = Path(repo_info['path'])
    save_state(repo_path, {
        "topic": topic,
        "target_audience": target_audience,
        "research_sources": sources,
        "raw_notes": raw_notes
    })

    return {
        "research_sources": sources,
        "raw_notes": raw_notes
    }
