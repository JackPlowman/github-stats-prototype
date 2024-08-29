from __future__ import annotations

from typing import TYPE_CHECKING

from structlog import get_logger, stdlib
from structlog.contextvars import bind_contextvars, unbind_contextvars

from application.catalogued_repository import CataloguedRepository
from application.repository_analysis.repository_analysis import analyse_repository

if TYPE_CHECKING:
    from github import PaginatedList, Repository

logger: stdlib.BoundLogger = get_logger()


def set_up_repository_pages(
    repositories: PaginatedList[Repository], repositories_stats: list[CataloguedRepository]
) -> list[CataloguedRepository]:
    """Set up the repository page.

    Args:
        repositories (PaginatedList[Repository]): The list of repositories.
        repositories_stats (list[CataloguedRepository]): The list of repositories stats.

    Returns:
        list[CataloguedRepository]: The list of repositories stats.
    """
    for repository in repositories:
        bind_contextvars(repository=repository)
        logger.info("Analysing repository")
        total_files = analyse_repository(repository.full_name)
        repositories_stats.extend(
            [
                CataloguedRepository(
                    name=repository.full_name,
                    description=repository.description or "",
                    file_count=total_files,
                    commit_count=repository.get_commits().totalCount,
                )
            ]
        )
    unbind_contextvars("repository")
    return repositories_stats
