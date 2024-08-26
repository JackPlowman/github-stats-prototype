from unittest.mock import MagicMock, patch

from application.repository_analysis.languages import (
    add_languages_sloc_table,
    check_for_excluded_dirs,
    clone_repo,
    count_files_per_language,
    determine_file_language,
)

FILE_PATH = "application.repository_analysis.languages"


@patch(f"{FILE_PATH}.count_files_per_language")
@patch(f"{FILE_PATH}.catalogue_repository")
@patch(f"{FILE_PATH}.get_languages")
@patch(f"{FILE_PATH}.clone_repo")
def test_add_languages_sloc_table(
    mock_clone_repo: MagicMock,
    mock_get_languages: MagicMock,
    mock_catalogue_repository: MagicMock,
    mock_count_files_per_language: MagicMock,
) -> None:
    # Arrange
    markdown_file = MagicMock()
    mock_count_files_per_language.return_value = {"Python": 100, "Javascript": 200}
    # Act
    add_languages_sloc_table(markdown_file)
    # Assert
    markdown_file.new_table.assert_called_once_with(
        columns=2, rows=3, text=["Language", "File Count", "Python", 100, "Javascript", 200]
    )
    mock_clone_repo.assert_called_once_with("JackPlowman", "github-stats")
    mock_get_languages.assert_called_once_with()
    mock_catalogue_repository.assert_called_once_with(mock_clone_repo.return_value, mock_get_languages.return_value)
    mock_count_files_per_language.assert_called_once_with(mock_catalogue_repository.return_value)


@patch(f"{FILE_PATH}.Path")
@patch(f"{FILE_PATH}.Repo")
def test_clone_repo(mock_repo: MagicMock, mock_path: MagicMock) -> None:
    # Arrange
    mock_path.exists.return_value = False
    # Act
    clone_repo("JackPlowman", "github-stats")
    # Assert
    mock_repo.clone_from.assert_called_once_with(
        "https://github.com/JackPlowman/github-stats.git", mock_path.return_value
    )


@patch(f"{FILE_PATH}.Path")
@patch(f"{FILE_PATH}.Repo")
def test_clone_repo_exists(mock_repo: MagicMock, mock_path: MagicMock) -> None:
    # Arrange
    mock_path.exists.return_value = True
    # Act
    clone_repo("JackPlowman", "github-stats")
    # Assert
    mock_repo.clone_from.assert_not_called()


def test_determine_file_language() -> None:
    # Arrange
    mock_path = MagicMock()
    mock_file_name = "file.py"
    mock_catalogued_files = {}
    mock_language = MagicMock()
    mock_language.extensions = [".py"]
    mock_language.name = "Python"
    # Act
    response = determine_file_language(mock_path, mock_file_name, mock_catalogued_files, [mock_language])
    # Assert
    assert response == {mock_language.name : [f"{mock_path}/{mock_file_name}"]}


def test_check_for_excluded_dirs() -> None:
    # Arrange
    mock_path = MagicMock()
    # Act
    check_for_excluded_dirs(mock_path, ["excluded"])
    # Assert

    mock_path.assert_not_called()


def test_count_files_per_language() -> None:
    # Arrange
    file_types = {"Python": ["file1.py", "file2.py"]}
    # Act
    response = count_files_per_language(file_types)
    # Assert
    assert response == {"Python": 2}


