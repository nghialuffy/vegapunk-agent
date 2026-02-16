"""
Git operations for version control and publishing.
"""

import subprocess
from pathlib import Path
from src.config import Config


def init_repo(repo_path: Path) -> None:
    """
    Initialize a git repository at the given path.

    Args:
        repo_path: Path to the repository directory
    """
    try:
        # Initialize git repo
        subprocess.run(
            ['git', 'init'],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )

        # Configure git user if not already set
        _configure_git_user(repo_path)

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to initialize git repo: {e.stderr}")


def _configure_git_user(repo_path: Path) -> None:
    """Configure git user name and email for the repository."""
    try:
        subprocess.run(
            ['git', 'config', 'user.name', Config.GIT_USER_NAME],
            cwd=repo_path,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ['git', 'config', 'user.email', Config.GIT_USER_EMAIL],
            cwd=repo_path,
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError:
        # If config fails, it's not critical
        pass


def commit_changes(repo_path: Path, message: str) -> None:
    """
    Stage all changes and create a commit.

    Args:
        repo_path: Path to the repository directory
        message: Commit message
    """
    try:
        # Add all files
        subprocess.run(
            ['git', 'add', '.'],
            cwd=repo_path,
            check=True,
            capture_output=True
        )

        # Commit
        subprocess.run(
            ['git', 'commit', '-m', message],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to commit changes: {e.stderr}")


def push_to_remote(repo_path: Path, remote_url: str = None) -> None:
    """
    Push commits to a remote repository.

    Args:
        repo_path: Path to the repository directory
        remote_url: URL of the remote repository (optional)
    """
    try:
        # Add remote if URL is provided
        if remote_url:
            # Check if remote 'origin' exists
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                cwd=repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                # Add remote
                subprocess.run(
                    ['git', 'remote', 'add', 'origin', remote_url],
                    cwd=repo_path,
                    check=True,
                    capture_output=True
                )

        # Get current branch name
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        branch = result.stdout.strip() or 'main'

        # Rename to main if on master
        if branch == 'master':
            subprocess.run(
                ['git', 'branch', '-M', 'main'],
                cwd=repo_path,
                check=True,
                capture_output=True
            )
            branch = 'main'

        # Push
        subprocess.run(
            ['git', 'push', '-u', 'origin', branch],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to push to remote: {e.stderr}")


def get_repo_info(repo_path: Path) -> dict:
    """
    Get information about the git repository.

    Args:
        repo_path: Path to the repository directory

    Returns:
        Dictionary with repository information
    """
    try:
        # Get current branch
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        branch = result.stdout.strip() or 'main'

        # Get remote URL if it exists
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        remote_url = result.stdout.strip() if result.returncode == 0 else None

        return {
            'path': str(repo_path),
            'branch': branch,
            'remote_url': remote_url
        }

    except Exception as e:
        return {
            'path': str(repo_path),
            'error': str(e)
        }
