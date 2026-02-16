"""
LLM client wrappers for OpenAI and Anthropic.
Provides unified interface for calling different models.

Supports both direct API access and GitHub Copilot API routing.
"""

from openai import OpenAI
from anthropic import Anthropic
from src.config import Config


# Lazy initialization of clients
_openai_client = None
_anthropic_client = None
_claude_via_openai_client = None


def get_openai_client() -> OpenAI:
    """Get or create the OpenAI client singleton."""
    global _openai_client
    if _openai_client is None:
        base_url = Config.get_base_url_for_openai()
        api_key = Config.get_api_key_for_openai()

        if base_url:
            _openai_client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            _openai_client = OpenAI(api_key=api_key)
    return _openai_client


def get_anthropic_client() -> Anthropic:
    """Get or create the Anthropic client singleton."""
    global _anthropic_client
    if _anthropic_client is None:
        api_key = Config.get_api_key_for_claude()
        _anthropic_client = Anthropic(api_key=api_key)
    return _anthropic_client


def get_claude_via_openai_client() -> OpenAI:
    """
    Get OpenAI client configured for Claude via GitHub Copilot API.

    GitHub Copilot API supports Claude models through OpenAI-compatible endpoints.
    """
    global _claude_via_openai_client
    if _claude_via_openai_client is None:
        base_url = Config.get_base_url_for_claude()
        api_key = Config.get_api_key_for_claude()
        _claude_via_openai_client = OpenAI(api_key=api_key, base_url=base_url)
    return _claude_via_openai_client


def call_openai(system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
    """
    Call OpenAI GPT-4o for planning and structuring tasks.

    Works with both direct OpenAI API and GitHub Copilot API routing.

    Args:
        system_prompt: System message defining the role
        user_prompt: User message with the task
        temperature: Sampling temperature (0.0 to 1.0)

    Returns:
        The model's response as a string
    """
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"OpenAI API call failed: {str(e)}")


def call_claude(system_prompt: str, user_prompt: str, temperature: float = 1.0, max_tokens: int = 16000) -> str:
    """
    Call Claude Sonnet-4 for knowledge synthesis and lecture writing.

    This is used ONLY for Steps 3 and 4 where deep thinking and
    pedagogical writing are required.

    Supports both:
    - Direct Anthropic API
    - GitHub Copilot API (via OpenAI-compatible endpoint)

    Args:
        system_prompt: System message defining the role
        user_prompt: User message with the task
        temperature: Sampling temperature (0.0 to 1.0)
        max_tokens: Maximum tokens to generate

    Returns:
        The model's response as a string
    """
    try:
        if Config.USE_GITHUB_COPILOT:
            # Use OpenAI-compatible client for GitHub Copilot routing
            client = get_claude_via_openai_client()
            response = client.chat.completions.create(
                model=Config.CLAUDE_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        else:
            # Use direct Anthropic API
            client = get_anthropic_client()
            response = client.messages.create(
                model=Config.CLAUDE_MODEL,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.content[0].text

    except Exception as e:
        raise RuntimeError(f"Claude API call failed: {str(e)}")


def extract_lesson_outline(synthesis_output: str) -> list[str]:
    """
    Extract the lesson outline from Claude's synthesis output.

    The synthesis prompt instructs Claude to include a section like:
    ## LESSON OUTLINE
    1. Lesson title 1
    2. Lesson title 2
    ...

    Args:
        synthesis_output: The full output from the synthesis step

    Returns:
        List of lesson titles
    """
    lessons = []

    # Find the LESSON OUTLINE section
    lines = synthesis_output.split('\n')
    in_outline_section = False

    for line in lines:
        if '## LESSON OUTLINE' in line or '## Lesson Outline' in line:
            in_outline_section = True
            continue

        if in_outline_section:
            # Stop at next section header or empty line after content
            if line.strip().startswith('##') and 'lesson' not in line.lower():
                break

            # Extract numbered items
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove number/bullet and clean up
                lesson_title = line.lstrip('0123456789.-) ').strip()
                if lesson_title:
                    lessons.append(lesson_title)

    if not lessons:
        # Fallback: create a default outline
        lessons = [
            "Introduction and Fundamentals",
            "Core Concepts",
            "Practical Applications",
            "Advanced Topics"
        ]

    return lessons
