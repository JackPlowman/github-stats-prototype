from structlog import get_logger, stdlib
from structlog.contextvars import bind_contextvars, unbind_contextvars

from .catalogued_repository import CataloguedRepository
from .custom_logging import set_up_custom_logging
from .github_interactions import retrieve_repositories
from .markdown.markdown import set_up_index_page
from .repository_analysis.repository_analysis import analyse_repository

logger: stdlib.BoundLogger = get_logger()


def main() -> None:
    """Entrypoint for Application."""
    set_up_custom_logging()
    try:
        repositories = retrieve_repositories()
        repositories_stats = []
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

        set_up_index_page(repositories_stats)
    except Exception:
        logger.exception("An error occurred during the execution of the analyser.")
        raise
