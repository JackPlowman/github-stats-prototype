from unittest.mock import MagicMock

from application.markdown.markdown import create_markdown_file, set_up_markdown_file


def test_set_up_markdown_file() -> None:
    # Arrange
    file_path = "index"
    title = "GitHub Stats Repository"
    # Act
    markdown_file = set_up_markdown_file(file_path, title)
    # Assert
    assert markdown_file.file_name == f"generated_markdown/{file_path}"
    assert markdown_file.title == f"\n{title}\n=======================\n"


def test_create_markdown_file() -> None:
    # Arrange
    markdown_file = MagicMock()
    # Act
    create_markdown_file(markdown_file)
    # Assert
    markdown_file.create_md_file.assert_called_once()
