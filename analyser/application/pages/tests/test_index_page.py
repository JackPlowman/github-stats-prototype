from unittest.mock import MagicMock, patch

from application.catalogued_repository import CataloguedRepository
from application.pages.index_page import set_up_index_page

FILE_PATH = "application.pages.index_page"


@patch(f"{FILE_PATH}.set_up_markdown_file")
@patch(f"{FILE_PATH}.create_markdown_file")
def test_set_up_index_page(
    mock_create_markdown_file: MagicMock,
    mock_set_up_markdown_file: MagicMock,
) -> None:
    # Arrange
    repositories = [
        CataloguedRepository("JackPlowman/github-stats", "A repository for analysing GitHub repositories.", 100, 10)
    ]
    # Act
    set_up_index_page(repositories)
    # Assert
    mock_set_up_markdown_file.assert_called_once_with("index", "Active Repository Statistics")
    mock_create_markdown_file.assert_called_once_with(mock_set_up_markdown_file.return_value)
