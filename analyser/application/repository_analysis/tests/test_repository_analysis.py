from unittest.mock import MagicMock, patch

from application.repository_analysis.repository_analysis import (
    add_file_counts,
    analyse_repository,
    catalogue_repository,
    check_for_excluded_dirs,
)

FILE_PATH = "application.repository_analysis.repository_analysis"


@patch(f"{FILE_PATH}.clone_repo")
@patch(f"{FILE_PATH}.set_up_markdown_file")
@patch(f"{FILE_PATH}.add_file_counts")
@patch(f"{FILE_PATH}.create_markdown_file")
def test_analyse_repository(
    mock_create_markdown_file: MagicMock,
    mock_add_file_counts: MagicMock,
    mock_set_up_markdown_file: MagicMock,
    mock_clone_repo: MagicMock,
) -> None:
    # Arrange
    mock_clone_repo.return_value = repo_name = "JackPlowman/github-stats"
    mock_set_up_markdown_file.return_value = markdown_file = MagicMock()
    markdown_file_two = MagicMock()
    mock_add_file_counts.return_value = (markdown_file_two, 100)
    # Act
    response = analyse_repository(repo_name)
    # Assert
    assert response == 100
    mock_clone_repo.assert_called_once_with("JackPlowman", "github-stats")
    mock_set_up_markdown_file.assert_called_once_with("github-stats", f"{repo_name} Stats")
    mock_add_file_counts.assert_called_once_with(markdown_file, repo_name)
    mock_create_markdown_file.assert_called_once_with(markdown_file_two)


@patch(f"{FILE_PATH}.count_files_per_language")
@patch(f"{FILE_PATH}.catalogue_repository")
@patch(f"{FILE_PATH}.get_languages")
def test_add_file_counts(
    mock_get_languages: MagicMock,
    mock_catalogue_repository: MagicMock,
    mock_count_files_per_language: MagicMock,
) -> None:
    # Arrange
    markdown_file = MagicMock()
    mock_count_files_per_language.return_value = {"Python": 100, "Javascript": 200}
    path_to_repo = "application/repos/github-stats"
    # Act
    add_file_counts(markdown_file, "application/repos/github-stats")
    # Assert
    markdown_file.new_table.assert_called_once_with(
        columns=2, rows=3, text=["Language", "File Count", "Python", 100, "Javascript", 200]
    )
    mock_get_languages.assert_called_once_with()
    mock_catalogue_repository.assert_called_once_with(path_to_repo, mock_get_languages.return_value)
    mock_count_files_per_language.assert_called_once_with(mock_catalogue_repository.return_value)


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
