from structlog import get_logger, stdlib
from structlog.contextvars import bind_contextvars, unbind_contextvars

from .custom_logging import set_up_custom_logging
from .github_interactions import retrieve_repositories
from .markdown.markdown import set_up_index_page
from .repository import Repository
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
            logger.info("Analysing repository", repository=repository)
            total_files = analyse_repository(repository)
            repositories_stats.extend(
                [Repository(repository, "A repository for analysing GitHub repositories.", total_files)]
            )
        unbind_contextvars("repository")

        set_up_index_page(repositories_stats)
    except Exception:
        logger.exception("An error occurred during the execution of the analyser.")
        raise

