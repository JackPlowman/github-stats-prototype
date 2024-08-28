from structlog import get_logger, stdlib, contextvars

from .custom_logging import set_up_custom_logging
from .markdown.markdown import set_up_index_page
from .repository import Repository
from .repository_analysis.repository_analysis import analyse_repository

logger: stdlib.BoundLogger = get_logger()

def main() -> None:
    """Entrypoint for Application."""
    set_up_custom_logging()
    try:
        repositories = ["JackPlowman/github-stats"]
        repositories_stats = []
        for repository in repositories:
            contextvars.bind_contextvars(repository=repository)
            logger.info("Analysing repository", repository=repository)
            total_files = analyse_repository(repository)
            repositories_stats.extend(
                [Repository(repository, "A repository for analysing GitHub repositories.", total_files)]
            )
        set_up_index_page(repositories_stats)
    except Exception:
        logger.exception("An error occurred during the execution of the analyser.")
        raise
