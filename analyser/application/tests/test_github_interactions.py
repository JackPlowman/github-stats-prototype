from unittest.mock import MagicMock, call, patch

from application.github_interactions import clone_repo, retrieve_repositories

FILE_PATH = "application.github_interactions"


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


@patch(f"{FILE_PATH}.Github")
@patch(f"{FILE_PATH}.getenv")
def test_retrieve_repositories__unauthenticated(mock_getenv: MagicMock, mock_github: MagicMock) -> None:
    # Arrange
    mock_getenv.side_effect = ["Test", ""]
    full_name = "Test1/Test2"
    mock_github.return_value.search_repositories.return_value = [MagicMock(full_name=full_name)]
    # Act
    repositories = retrieve_repositories()
    # Assert
    mock_github.assert_called_once_with()
    mock_getenv.assert_has_calls([call("REPOSITORY_OWNER", ""), call("GITHUB_TOKEN", "")])
    assert repositories == [full_name]


@patch(f"{FILE_PATH}.Github")
@patch(f"{FILE_PATH}.getenv")
def test_retrieve_repositories__authenticated(mock_getenv: MagicMock, mock_github: MagicMock) -> None:
    # Arrange
    token = "TestToken"  # noqa: S105
    mock_getenv.side_effect = ["Test", token]
    full_name = "Test3/Test4"
    mock_github.return_value.search_repositories.return_value = [MagicMock(full_name=full_name)]
    # Act
    repositories = retrieve_repositories()
    # Assert
    mock_github.assert_called_once_with(token)
    mock_getenv.assert_has_calls([call("REPOSITORY_OWNER", ""), call("GITHUB_TOKEN", "")])
    assert repositories == [full_name]
