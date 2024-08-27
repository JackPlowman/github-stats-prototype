from unittest.mock import MagicMock, patch

from application.main import main
from application.repository import Repository

FILE_PATH = "application.main"


@patch(f"{FILE_PATH}.set_up_index_page")
@patch(f"{FILE_PATH}.analyse_repository")
def test_main(
    mock_analyse_repository: MagicMock,
    mock_set_up_index_page: MagicMock,
) -> None:
    # Arrange
    mock_analyse_repository.return_value = total = 100
    # Act
    main()
    # Assert
    mock_analyse_repository.assert_called_once_with("JackPlowman/github-stats")
    mock_set_up_index_page.assert_called_once_with(
        [Repository("JackPlowman/github-stats", "A repository for analysing GitHub repositories.", total)]
    )
