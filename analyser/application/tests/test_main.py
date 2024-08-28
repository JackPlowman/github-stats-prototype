from unittest.mock import MagicMock, patch

from application.main import main
from application.repository import Repository

FILE_PATH = "application.main"


@patch(f"{FILE_PATH}.set_up_index_page")
@patch(f"{FILE_PATH}.analyse_repository")
@patch(f"{FILE_PATH}.retrieve_repositories")
def test_main(
    mock_retrieve_repositories: MagicMock,
    mock_analyse_repository: MagicMock,
    mock_set_up_index_page: MagicMock,
) -> None:
    # Arrange
    full_name = "JackPlowman/github-stats"
    description = "A test repository"
    mock_retrieve_repositories.return_value = [MagicMock(full_name=full_name, description=description)]
    mock_analyse_repository.return_value = total = 100
    # Act
    main()
    # Assert
    mock_retrieve_repositories.assert_called_once_with()
    mock_analyse_repository.assert_called_once_with(full_name)
    mock_set_up_index_page.assert_called_once_with([Repository(full_name, "A test repository", total)])
