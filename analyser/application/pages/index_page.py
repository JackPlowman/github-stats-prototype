from __future__ import annotations

from typing import TYPE_CHECKING

from structlog import get_logger, stdlib

from application.markdown.components.link import Link
from application.markdown.markdown import create_markdown_file, set_up_markdown_file

logger: stdlib.BoundLogger = get_logger()
if TYPE_CHECKING:
    from application.catalogued_repository import CataloguedRepository


def set_up_index_page(repositories: list[CataloguedRepository]) -> None:
    """Set up the index page. Once all the repositories have been processed.

    Args:
        repositories (list[CataloguedRepository]): The list of repositories.
    """
    index_page = set_up_markdown_file("index", "Active Repository Statistics")
    table_contents = ["Name", "Description", "Identified Files count", "Commit count"]
    sorted_repositories: list[CataloguedRepository] = sorted(
        repositories, key=lambda repository: repository.file_count, reverse=True
    )
    logger.debug("Sorted table contents", sorted_repositories=sorted_repositories)
    for repository in sorted_repositories:
        table_contents.extend(
            [
                Link(repository.name, repository.name.split("/", maxsplit=1)[1]),
                repository.description,
                repository.file_count,
                repository.commit_count,
            ]
        )
    index_page.new_table(columns=4, rows=len(repositories) + 1, text=table_contents, text_align="left")
    create_markdown_file(index_page)
