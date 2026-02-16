"""
Tavily search client for web research.
"""

from tavily import TavilyClient
from src.config import Config


_tavily_client = None


def get_tavily_client() -> TavilyClient:
    """Get or create the Tavily client singleton."""
    global _tavily_client
    if _tavily_client is None:
        _tavily_client = TavilyClient(api_key=Config.TAVILY_API_KEY)
    return _tavily_client


def search_topic(topic: str, max_results: int = None) -> dict:
    """
    Search for information about a topic using Tavily API.

    Args:
        topic: The topic to search for
        max_results: Maximum number of results (default from config)

    Returns:
        Dictionary with search results including:
        - results: List of search result dictionaries
        - query: The search query used
    """
    if max_results is None:
        max_results = Config.TAVILY_MAX_RESULTS

    try:
        client = get_tavily_client()
        response = client.search(
            query=topic,
            max_results=max_results,
            search_depth=Config.TAVILY_SEARCH_DEPTH,
            include_raw_content=True
        )
        print(response)
        return response

    except Exception as e:
        raise RuntimeError(f"Tavily search failed: {str(e)}")


def format_search_results(search_response: dict) -> str:
    """
    Format Tavily search results into a readable string.

    Args:
        search_response: Response from Tavily API

    Returns:
        Formatted string with all search results
    """
    results = search_response.get('results', [])

    if not results:
        return "No search results found."

    formatted = []
    for i, result in enumerate(results, 1):
        title = result.get('title', 'Untitled')
        url = result.get('url', '')
        content = result.get('content', '')
        raw_content = result.get('raw_content', '')

        # Use raw content if available, otherwise use snippet
        text = raw_content if raw_content else content

        formatted.append(f"""
=== Result {i}: {title} ===
URL: {url}

{text}

---
""")

    return '\n'.join(formatted)


def extract_sources(search_response: dict) -> list[dict[str, str]]:
    """
    Extract source information from search results.

    Args:
        search_response: Response from Tavily API

    Returns:
        List of dictionaries with 'title' and 'url'
    """
    results = search_response.get('results', [])

    sources = []
    for result in results:
        sources.append({
            'title': result.get('title', 'Untitled'),
            'url': result.get('url', ''),
            'score': result.get('score', 0.0)
        })

    return sources
