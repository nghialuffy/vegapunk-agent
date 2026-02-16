import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration for the Research & Teaching Agent"""

    # ========================================================================
    # GitHub Copilot API Support
    # ========================================================================
    USE_GITHUB_COPILOT = os.getenv("USE_GITHUB_COPILOT", "false").lower() == "true"
    GITHUB_COPILOT_TOKEN = os.getenv("GITHUB_COPILOT_TOKEN", "dummy")  # Default to "dummy" for local proxy
    COPILOT_BASE_URL = os.getenv("COPILOT_BASE_URL", "http://localhost:4141")

    # ========================================================================
    # API Keys (Direct API access)
    # ========================================================================
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    # ========================================================================
    # Git configuration
    # ========================================================================
    GIT_USER_NAME = os.getenv("GIT_USER_NAME", "Teaching Agent")
    GIT_USER_EMAIL = os.getenv("GIT_USER_EMAIL", "agent@example.com")

    # ========================================================================
    # LLM Models
    # ========================================================================
    # Allow custom model names from environment variables
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
    CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")

    # ========================================================================
    # Paths
    # ========================================================================
    BASE_DIR = Path(__file__).parent.parent
    OUTPUT_DIR = BASE_DIR / "outputs"

    # ========================================================================
    # Tavily search settings
    # ========================================================================
    TAVILY_MAX_RESULTS = 5
    TAVILY_SEARCH_DEPTH = "advanced"

    @classmethod
    def validate(cls):
        """Validate that required API keys are set"""
        # Always need Tavily for research
        if not cls.TAVILY_API_KEY:
            raise ValueError(
                "Missing TAVILY_API_KEY. "
                "Please set it in your .env file."
            )

        # Check API keys based on mode
        if cls.USE_GITHUB_COPILOT:
            # Using GitHub Copilot API routing - token not required for local proxy
            # Local proxy at localhost:4141 doesn't need authentication
            pass
        else:
            # Using direct API access
            missing = []
            if not cls.OPENAI_API_KEY:
                missing.append("OPENAI_API_KEY")
            if not cls.ANTHROPIC_API_KEY:
                missing.append("ANTHROPIC_API_KEY")

            if missing:
                raise ValueError(
                    f"Missing required environment variables: {', '.join(missing)}. "
                    f"Please set them in your .env file, or enable USE_GITHUB_COPILOT=true "
                    f"to use GitHub Copilot API routing."
                )

    @classmethod
    def get_api_key_for_openai(cls) -> str:
        """Get the appropriate API key for OpenAI client"""
        return cls.GITHUB_COPILOT_TOKEN if cls.USE_GITHUB_COPILOT else cls.OPENAI_API_KEY

    @classmethod
    def get_api_key_for_claude(cls) -> str:
        """Get the appropriate API key for Claude client"""
        return cls.GITHUB_COPILOT_TOKEN if cls.USE_GITHUB_COPILOT else cls.ANTHROPIC_API_KEY

    @classmethod
    def get_base_url_for_openai(cls) -> str:
        """Get the base URL for OpenAI client"""
        return cls.COPILOT_BASE_URL if cls.USE_GITHUB_COPILOT else None

    @classmethod
    def get_base_url_for_claude(cls) -> str:
        """Get the base URL for Claude client (via OpenAI-compatible endpoint)"""
        return cls.COPILOT_BASE_URL if cls.USE_GITHUB_COPILOT else None
