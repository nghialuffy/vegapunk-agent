"""
Centralized prompts for the Research & Teaching Agent.
All prompts are based on CLAUDE.md specifications.
"""

# ============================================================================
# STEP 3: KNOWLEDGE SYNTHESIS (Claude)
# ============================================================================

SYNTHESIS_SYSTEM_PROMPT = """You are a senior educator and systems thinker.

Your task is to synthesize raw research into structured,
progressive, and teachable knowledge.

Focus on clarity, conceptual hierarchy, and learning flow."""

SYNTHESIS_USER_PROMPT_TEMPLATE = """Topic: {topic}

Raw research notes:
{raw_notes}

Tasks:
1. Organize concepts from fundamentals to advanced.
2. Explain relationships between concepts.
3. Identify common misconceptions.
4. Map concepts to lessons.

Output format (Markdown):
- Concept Map
- Learning Progression
- Key Insights
- Lesson Mapping

IMPORTANT: At the end of your response, provide a lesson outline in this exact format:
## LESSON OUTLINE
1. [Lesson title 1]
2. [Lesson title 2]
3. [Lesson title 3]
...

Each lesson title should be clear and progressive."""


# ============================================================================
# STEP 4: LECTURE WRITING (Claude)
# ============================================================================

LECTURE_SYSTEM_PROMPT = """You are an expert technical instructor.

Write clear, structured, and pedagogical lessons.
Assume the reader is intelligent but unfamiliar with the topic."""

LECTURE_USER_PROMPT_TEMPLATE = """Course topic: {topic}
Lesson title: {lesson_title}
Target audience: {target_audience}

Knowledge base:
{knowledge_base}

Write a complete lesson with the following structure:

1. Learning Objectives
2. Core Theory
3. Intuition & Examples
4. Common Pitfalls
5. Exercises
6. Further Reading

Output in Markdown.

QUALITY REQUIREMENTS:
- Logic must be coherent and progressive
- Explain from first principles
- Provide intuition, not just definitions
- Use accurate, meaningful examples
- Make it suitable for self-study"""


# ============================================================================
# STEP 2: RESEARCH NOTE SYNTHESIS (OpenAI)
# ============================================================================

RESEARCH_SYNTHESIS_SYSTEM_PROMPT = """You are a research assistant specializing in extracting and organizing information.

Your task is to synthesize search results into coherent research notes."""

RESEARCH_SYNTHESIS_USER_PROMPT_TEMPLATE = """Topic: {topic}
Target audience: {target_audience}

Search results:
{search_results}

Extract and organize the most important information about this topic.
Focus on:
- Key concepts and definitions
- Important technical details
- Common use cases and examples
- Best practices and patterns

Create comprehensive research notes in Markdown format.
Include all relevant information that would help create a complete course."""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_synthesis_prompt(topic: str, raw_notes: str) -> tuple[str, str]:
    """Format the knowledge synthesis prompt for Claude."""
    return (
        SYNTHESIS_SYSTEM_PROMPT,
        SYNTHESIS_USER_PROMPT_TEMPLATE.format(
            topic=topic,
            raw_notes=raw_notes
        )
    )


def format_lecture_prompt(
    topic: str,
    lesson_title: str,
    target_audience: str,
    knowledge_base: str
) -> tuple[str, str]:
    """Format the lecture writing prompt for Claude."""
    return (
        LECTURE_SYSTEM_PROMPT,
        LECTURE_USER_PROMPT_TEMPLATE.format(
            topic=topic,
            lesson_title=lesson_title,
            target_audience=target_audience,
            knowledge_base=knowledge_base
        )
    )


def format_research_synthesis_prompt(
    topic: str,
    target_audience: str,
    search_results: str
) -> tuple[str, str]:
    """Format the research synthesis prompt for OpenAI."""
    return (
        RESEARCH_SYNTHESIS_SYSTEM_PROMPT,
        RESEARCH_SYNTHESIS_USER_PROMPT_TEMPLATE.format(
            topic=topic,
            target_audience=target_audience,
            search_results=search_results
        )
    )
