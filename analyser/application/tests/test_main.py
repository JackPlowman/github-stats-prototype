from unittest.mock import MagicMock, patch

from application.main import main

FILE_PATH = "application.main"


@patch(f"{FILE_PATH}.create_markdown_file")
@patch(f"{FILE_PATH}.add_languages_sloc_table")
@patch(f"{FILE_PATH}.set_up_markdown_file")
@patch(f"{FILE_PATH}.Github")
def test_main(
    mock_github: MagicMock,
    mock_set_up_markdown_file: MagicMock,
    mock_add_languages_sloc_table: MagicMock,
    mock_create_markdown_file: MagicMock,
) -> None:
    # Act
    main()
    # Assert
    mock_github.assert_called_once()
    mock_set_up_markdown_file.assert_called_once_with("index", "GitHub Stats Repository")
    mock_add_languages_sloc_table.assert_called_once_with(
        mock_github.return_value, mock_set_up_markdown_file.return_value
    )
    mock_create_markdown_file.assert_called_once_with(mock_add_languages_sloc_table.return_value)
