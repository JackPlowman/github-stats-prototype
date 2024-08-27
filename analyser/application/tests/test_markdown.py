from unittest.mock import MagicMock, patch

from application.markdown import create_markdown_file, set_up_markdown_file, set_up_index_page
from application.repository import Repository
FILE_PATH = "application.markdown"
def test_set_up_markdown_file() -> None:
    # Arrange
    file_path = "index"
    title = "GitHub Stats Repository"
    # Act
    markdown_file = set_up_markdown_file(file_path, title)
    # Assert
    assert markdown_file.file_name == f"application/generated_markdown/{file_path}"
    assert markdown_file.title == f"\n{title}\n=======================\n"


def test_create_markdown_file() -> None:
    # Arrange
    markdown_file = MagicMock()
    # Act
    create_markdown_file(markdown_file)
    # Assert
    markdown_file.create_md_file.assert_called_once()

@patch(f"{FILE_PATH}.set_up_markdown_file")
@patch(f"{FILE_PATH}.create_markdown_file")
def test_set_up_index_page(
    mock_create_markdown_file: MagicMock,
    mock_set_up_markdown_file: MagicMock,
) -> None:
    # Arrange
    repositories = [Repository("JackPlowman/github-stats", "A repository for analysing GitHub repositories.", 100)]
    # Act
    set_up_index_page(repositories)
    # Assert
    mock_set_up_markdown_file.assert_called_once_with("index", "GitHub Stats")
    mock_create_markdown_file.assert_called_once_with(mock_set_up_markdown_file.return_value)
