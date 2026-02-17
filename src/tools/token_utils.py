"""
Utility functions for handling token limits.

Provides intelligent truncation to stay within Claude's 64k token limit.
"""

import tiktoken


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """
    Count the number of tokens in a text string.

    Uses tiktoken for accurate token counting.
    Defaults to gpt-4 encoding which is close enough for Claude.

    Args:
        text: The text to count tokens for
        model: The model name (default: gpt-4)

    Returns:
        Number of tokens
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback to cl100k_base for unknown models
        encoding = tiktoken.get_encoding("cl100k_base")

    return len(encoding.encode(text))


def truncate_to_token_limit(text: str, max_tokens: int, model: str = "gpt-4") -> str:
    """
    Truncate text to fit within a token limit.

    Truncates from the middle to preserve both beginning and end context.
    This is better than truncating from the end because:
    - Beginning has important setup/context
    - End often has conclusions/summaries

    Args:
        text: The text to truncate
        max_tokens: Maximum number of tokens allowed
        model: The model name for token counting

    Returns:
        Truncated text that fits within the token limit
    """
    current_tokens = count_tokens(text, model)

    if current_tokens <= max_tokens:
        return text

    # Calculate how much to keep (80% to be safe)
    keep_ratio = (max_tokens * 0.8) / current_tokens

    # Split into lines for better truncation
    lines = text.split('\n')
    total_lines = len(lines)

    # Keep first and last 40% of lines, remove middle 20%
    keep_start = int(total_lines * keep_ratio * 0.5)
    keep_end = int(total_lines * keep_ratio * 0.5)

    truncated_lines = (
        lines[:keep_start] +
        ["\n\n[... CONTENT TRUNCATED TO FIT TOKEN LIMIT ...]\n\n"] +
        lines[-keep_end:] if keep_end > 0 else []
    )

    truncated_text = '\n'.join(truncated_lines)

    # Verify it fits now
    final_tokens = count_tokens(truncated_text, model)
    if final_tokens > max_tokens:
        # If still too long, do a hard character truncation
        char_ratio = (max_tokens * 0.7) / final_tokens
        char_limit = int(len(truncated_text) * char_ratio)
        truncated_text = truncated_text[:char_limit] + "\n\n[... TRUNCATED ...]"

    return truncated_text


def smart_truncate_for_prompt(
    content: str,
    max_tokens: int,
    content_name: str = "content"
) -> tuple[str, bool]:
    """
    Smart truncation with logging.

    Args:
        content: The content to potentially truncate
        max_tokens: Maximum tokens allowed
        content_name: Name of the content for logging

    Returns:
        Tuple of (truncated_content, was_truncated)
    """
    original_tokens = count_tokens(content)

    if original_tokens <= max_tokens:
        return content, False

    print(f"  ⚠️  {content_name} has {original_tokens:,} tokens (limit: {max_tokens:,})")
    print(f"  → Truncating to fit within limit...")

    truncated = truncate_to_token_limit(content, max_tokens)
    final_tokens = count_tokens(truncated)

    print(f"  ✓ Truncated to {final_tokens:,} tokens")

    return truncated, True
