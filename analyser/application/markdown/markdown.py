from __future__ import annotations

from mdutils.mdutils import MdUtils
from structlog import get_logger, stdlib

logger: stdlib.BoundLogger = get_logger()


def set_up_markdown_file(file_path: str, title: str) -> MdUtils:
    """Set up the markdown file.

    Args:
        file_path (str): The file path to the markdown file.
        title (str): The title of the markdown file.

    Returns:
        MdUtils: The markdown file object.
    """
    return MdUtils(file_name=f"generated_markdown/{file_path}", title=title)


def create_markdown_file(markdown_file: MdUtils) -> None:
    """Create the markdown file.

    Args:
        markdown_file (MdUtils): The markdown file object.
    """
    markdown_file.create_md_file()
