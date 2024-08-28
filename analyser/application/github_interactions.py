from __future__ import annotations
from pathlib import Path

from git import Repo
from structlog import get_logger, stdlib
from os import getenv
from github import Github
logger: stdlib.BoundLogger = get_logger()



def clone_repo(owner_name: str, repository_name: str) -> str:
    """Clone the repository and return the path to the repository.

    Uses existing clone if available in application/repos.

    Args:
        owner_name (str): The owner name of the repository.
        repository_name (str): The repository name.

    Returns:
        str: The path to the repository.
    """
    file_path = f"application/repos/{repository_name}"
    if not Path.exists(Path(file_path)):
        repo_url = f"https://github.com/{owner_name}/{repository_name}.git"
        Repo.clone_from(repo_url, Path(file_path))
        logger.debug("Cloned repository", path=file_path)

    return file_path

def retrieve_repositories() -> list[str]:
    """Retrieve the list of repositories to analyse."""
    user = getenv("REPOSITORY_OWNER", "")
    if user == "":
        msg = "REPOSITORY_OWNER environment variable is not set."
        raise ValueError(msg)
    token = getenv("GITHUB_TOKEN", "")
    if token == "":
        github = Github()
        logger.debug("Using unauthenticated GitHub API")
    else:
        github = Github(token)
        logger.debug("Using authenticated GitHub API")
    repositories_search = github.search_repositories(query=f"user:{user} archived:false")
    repositories = [repository.full_name for repository in repositories_search]
    logger.info("Repositories found", repositories_count=len(repositories), repositories=repositories)
    return repositories
