from unittest.mock import MagicMock, patch

from application.repository_analysis.repository_analysis import (
    add_language_summary_stats,
    analyse_repository,
    get_language_summary_stats,
)

FILE_PATH = "application.repository_analysis.repository_analysis"


@patch(f"{FILE_PATH}.create_markdown_file")
@patch(f"{FILE_PATH}.add_language_summary_stats")
@patch(f"{FILE_PATH}.set_up_markdown_file")
@patch(f"{FILE_PATH}.clone_repo")
def test_analyse_repository(
    _mock_clone_repo: MagicMock,
    _mock_set_up_markdown_file: MagicMock,
    mock_add_language_summary_stats: MagicMock,
    _mock_create_markdown_file: MagicMock,
) -> None:
    total = 100
    mock_add_language_summary_stats.return_value = MagicMock(), total
    repository = "JackPlowman/github-stats-prototype"

    # Act
    result = analyse_repository(repository)

    # Assert
    assert result == total


@patch(f"{FILE_PATH}.sorted")
@patch(f"{FILE_PATH}.get_language_summary_stats")
def test_add_language_summary_stats(mock_get_language_summary_stats: MagicMock, _mock_sorted: MagicMock) -> None:
    # Arrange
    markdown_file = MagicMock()
    path_to_repo = "path/to/repo"
    repository_name = "repo"
    mock_get_language_summary_stats.return_value = mock_get_language_return = MagicMock()
    mock_get_language_return.total_file_count = 100
    mock_get_language_return.language_to_language_summary_map.values.return_value = [  # noqa: PD011
        MagicMock(language="Python", file_count=10, source_count=100, code_count=100),
        MagicMock(language="JavaScript", file_count=10, source_count=100, code_count=100),
    ]
    # Act
    response_markdown_file, total_files = add_language_summary_stats(markdown_file, path_to_repo, repository_name)
    # Assert
    assert response_markdown_file == markdown_file
    assert total_files == 100


@patch(f"{FILE_PATH}.ProjectSummary")
def test_get_language_summary_stats(
    mock_project_summary: MagicMock,
) -> None:
    # Arrange
    path_to_repo = "path/to/repo"
    repository_name = "repo"
    mock_project_summary.total_file_count = 100
    mock_project_summary.language_to_language_summary_map.values.return_value = [  # noqa: PD011
        MagicMock(language="Python", file_count=10, source_count=100, code_count=100),
        MagicMock(language="JavaScript", file_count=10, source_count=100, code_count=100),
    ]
    # Act
    result = get_language_summary_stats(path_to_repo, repository_name)
    # Assert
    assert result == mock_project_summary.return_value
