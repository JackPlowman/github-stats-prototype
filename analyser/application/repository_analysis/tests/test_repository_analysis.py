from unittest.mock import MagicMock, patch

from application.repository_analysis.repository_analysis import (
    add_languages_sloc_table,
    catalogue_repository,
    check_for_excluded_dirs,
    clone_repo,
)

FILE_PATH = "application.repository_analysis.repository_analysis"


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


@patch(f"{FILE_PATH}.determine_file_language")
@patch(f"{FILE_PATH}.check_for_excluded_dirs")
@patch(f"{FILE_PATH}.Path")
def test_catalogue_repository(
    mock_path: MagicMock, mock_check_for_excluded_dirs: MagicMock, mock_determine_file_language: MagicMock
) -> None:
    # Arrange
    mock_languages = []
    file_path = "application/repos/github-stats"
    mock_path.return_value.walk.return_value = [(mock_path, [], ["file1.py", "file2.py"])]
    mock_check_for_excluded_dirs.return_value = False
    mock_determine_file_language.return_value = expected = {"Python": ["file1.py", "file2.py"]}
    # Act
    response = catalogue_repository(file_path, mock_languages)
    # Assert
    assert response == expected


def test_check_for_excluded_dirs() -> None:
    # Arrange
    mock_path = MagicMock()
    # Act
    check_for_excluded_dirs(mock_path, ["excluded"])
    # Assert

    mock_path.assert_not_called()
