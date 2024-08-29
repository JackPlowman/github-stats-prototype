from unittest.mock import MagicMock, patch

from application.pages.pages import create_markdown_pages

FILE_PATH = "application.pages.pages"


@patch(f"{FILE_PATH}.set_up_index_page")
@patch(f"{FILE_PATH}.set_up_repository_pages")
@patch(f"{FILE_PATH}.retrieve_repositories")
def test_create_markdown_pages(
    mock_retrieve_repositories: MagicMock, mock_set_up_repository_pages: MagicMock, mock_set_up_index_page: MagicMock
) -> None:
    # Act
    create_markdown_pages()
    # Assert
    mock_retrieve_repositories.assert_called_once_with()
    mock_set_up_repository_pages.assert_called_once_with(mock_retrieve_repositories.return_value, [])
    mock_set_up_index_page.assert_called_once_with(mock_set_up_repository_pages.return_value)
