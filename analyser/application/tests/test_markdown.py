from unittest.mock import MagicMock

from application.markdown import add_languages_sloc_table, create_markdown_file, set_up_markdown_file


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


def test_add_languages_sloc_table() -> None:
    # Arrange
    github = MagicMock()
    markdown_file = MagicMock()
    github.get_repo.return_value.get_languages.return_value = {
        "Python": 100,
        "JavaScript": 200,
    }
    # Act
    add_languages_sloc_table(github, markdown_file)
    # Assert
    github.get_repo.assert_called_once_with("JackPlowman/github-stats")
    github.get_repo.return_value.get_languages.assert_called_once()
    markdown_file.new_table.assert_called_once_with(
        rows=3, columns=2, text=["Language", "Software Bytes of Code", "Python", 100, "JavaScript", 200]
    )
