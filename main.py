#!/usr/bin/env python3
"""
Research & Teaching Agent - Main CLI Entry Point

This agent creates high-quality educational content by:
1. Setting up a local repository
2. Researching the topic via web search
3. Synthesizing knowledge with Claude
4. Writing complete lessons with Claude
5. Publishing to a git repository

Usage:
    python main.py --topic "Introduction to LangGraph" --audience "Python developers"
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.graph import run_agent


def main():
    parser = argparse.ArgumentParser(
        description="Research & Teaching Agent - Generate educational courses automatically",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --topic "Introduction to LangGraph"
  python main.py --topic "Python Async Programming" --audience "intermediate Python developers"
  python main.py --topic "Docker Basics" --audience "DevOps beginners"
  python main.py --topic "Git Basics" --repo-dir ~/my-courses
        """
    )

    parser.add_argument(
        "--topic",
        required=False,
        help="The topic to create a course about"
    )

    parser.add_argument(
        "--audience",
        default="intermediate developers",
        help="Description of the target audience (default: intermediate developers)"
    )

    parser.add_argument(
        "--repo-dir",
        type=str,
        help="Directory containing existing repositories to use (instead of creating new ones)"
    )

    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate environment configuration without running the agent"
    )

    args = parser.parse_args()

    # Validate that topic is provided unless validate-only
    if not args.validate_only and not args.topic:
        parser.error("--topic is required unless using --validate-only")

    # Validate configuration
    try:
        Config.validate()
        print("✓ Environment configuration validated")

        if args.validate_only:
            print("\nConfiguration:")
            if Config.USE_GITHUB_COPILOT:
                print(f"  Mode: GitHub Copilot API Routing")
                print(f"  Base URL: {Config.COPILOT_BASE_URL}")
            else:
                print(f"  Mode: Direct API Access")
            print(f"  OpenAI Model: {Config.OPENAI_MODEL}")
            print(f"  Claude Model: {Config.CLAUDE_MODEL}")
            print(f"  Output Directory: {Config.OUTPUT_DIR}")
            return 0

    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease create a .env file with your API keys.")
        print("See .env.example for the required variables.")
        return 1

    # Run the agent
    print("\n" + "="*70)
    print(f"  Research & Teaching Agent")
    print("="*70)
    print(f"\nTopic: {args.topic}")
    print(f"Audience: {args.audience}")
    if args.repo_dir:
        print(f"Repository Directory: {args.repo_dir}")
    print()

    try:
        final_state = run_agent(
            topic=args.topic,
            target_audience=args.audience,
            repo_dir=args.repo_dir
        )

        # Print summary
        print("\n" + "="*70)
        print("  COURSE GENERATION COMPLETE")
        print("="*70)
        print(f"\n✓ Topic: {final_state['topic']}")
        print(f"✓ Lessons: {len(final_state['lessons'])}")
        print(f"✓ Location: {final_state['repo_info']['path']}")
        print(f"✓ Repository: {final_state['github_repo_url']}")

        print("\nLesson Outline:")
        for i, lesson_title in enumerate(final_state['lesson_outline'], 1):
            print(f"  {i}. {lesson_title}")

        print("\n✅ Success! Your course is ready.\n")
        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
