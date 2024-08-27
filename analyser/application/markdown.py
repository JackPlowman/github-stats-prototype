from __future__ import annotations

from typing import TYPE_CHECKING

from mdutils.mdutils import MdUtils

if TYPE_CHECKING:
    from .repository import Repository


def set_up_markdown_file(file_path: str, title: str) -> MdUtils:
    """Set up the markdown file.

    Args:
        file_path (str): The file path to the markdown file.
        title (str): The title of the markdown file.

    Returns:
        MdUtils: The markdown file object.
    """
    build_directory = "application/generated_markdown"
    return MdUtils(file_name=f"{build_directory}/{file_path}", title=title)


def create_markdown_file(markdown_file: MdUtils) -> None:
    """Create the markdown file.

    Args:
        markdown_file (MdUtils): The markdown file object.
    """
    markdown_file.create_md_file()


def set_up_index_page(repositories: list[Repository]) -> None:
    """Set up the index page.

    Args:
        repositories (list[str]): The list of repositories.
    """
    index_page = set_up_markdown_file("index", "GitHub Stats")
    table_contents = ["Name", "Description", "Identified Files count"]
    for repository in repositories:
        table_contents.extend([repository.name, repository.description, repository.file_count])
    print(f"Table contents: {table_contents}")
    index_page.new_table(columns=3, rows=len(repositories) + 1, text=table_contents)
    create_markdown_file(index_page)
