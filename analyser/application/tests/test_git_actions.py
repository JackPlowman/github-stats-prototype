from unittest.mock import MagicMock, patch

from application.git_actions import clone_repo

FILE_PATH = "application.git_actions"


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
