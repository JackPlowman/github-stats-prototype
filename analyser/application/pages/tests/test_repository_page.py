from unittest.mock import MagicMock, patch

from application.catalogued_repository import CataloguedRepository
from application.pages.repository_page import set_up_repository_pages

FILE_PATH = "application.pages.repository_page"


@patch(f"{FILE_PATH}.analyse_repository")
def test_set_up_repository_pages(
    mock_analyse_repository: MagicMock,
) -> None:
    # Arrange
    mock_repository = MagicMock()
    mock_repository.full_name = "JackPlowman/github-stats"
    mock_repository.description = "A test repository"
    mock_repository.get_commits.return_value.totalCount = commit_count = 10
    repositories = [mock_repository]
    mock_analyse_repository.return_value = total = 100
    # Act
    repositories_stats = set_up_repository_pages(repositories, [])
    # Assert
    assert repositories_stats == [
        CataloguedRepository(
            name=mock_repository.full_name,
            description=mock_repository.description,
            file_count=total,
            commit_count=commit_count,
        )
    ]
    mock_analyse_repository.assert_called_once_with(mock_repository.full_name)
