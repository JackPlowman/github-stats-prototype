from structlog import get_logger, stdlib

from application.github_interactions import retrieve_repositories

from .index_page import set_up_index_page
from .repository_page import set_up_repository_pages

logger: stdlib.BoundLogger = get_logger()


def create_markdown_pages() -> None:
    """Create the markdown pages."""
    repositories = retrieve_repositories()
    repositories_stats = []
    repositories_stats = set_up_repository_pages(repositories, repositories_stats)
    set_up_index_page(repositories_stats)
