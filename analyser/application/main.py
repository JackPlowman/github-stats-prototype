from structlog import get_logger, stdlib

from .custom_logging import set_up_custom_logging
from .pages.pages import create_markdown_pages

logger: stdlib.BoundLogger = get_logger()


def main() -> None:
    """Entrypoint for Application."""
    set_up_custom_logging()
    try:
        create_markdown_pages()
    except Exception:
        logger.exception("An error occurred during the execution of the analyser.")
        raise
