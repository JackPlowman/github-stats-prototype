from unittest.mock import MagicMock, patch

from application.catalogued_repository import CataloguedRepository
from application.main import main

FILE_PATH = "application.main"

@patch(f"{FILE_PATH}.set_up_custom_logging")
@patch(f"{FILE_PATH}.create_markdown_pages")
def test_main(mock_create_markdown_pages: MagicMock, mock_set_up_custom_logging: MagicMock) -> None:
    # Act
    main()


# @patch(f"{FILE_PATH}.set_up_index_page")
# @patch(f"{FILE_PATH}.analyse_repository")
# @patch(f"{FILE_PATH}.retrieve_repositories")
# def test_main(
#     mock_retrieve_repositories: MagicMock,
#     mock_analyse_repository: MagicMock,
#     mock_set_up_index_page: MagicMock,
# ) -> None:
#     # Arrange
#     full_name = "JackPlowman/github-stats"
#     description = "A test repository"
#     mock_repository = MagicMock(full_name=full_name, description=description)
#     mock_repository.get_commits.return_value.totalCount = commit_count = 10
#     mock_retrieve_repositories.return_value = [mock_repository]
#     mock_analyse_repository.return_value = total = 100
#     # Act
#     main()
#     # Assert
#     mock_retrieve_repositories.assert_called_once_with()
#     mock_analyse_repository.assert_called_once_with(full_name)
#     mock_set_up_index_page.assert_called_once_with(
#         [CataloguedRepository(full_name, "A test repository", total, commit_count)]
#     )
