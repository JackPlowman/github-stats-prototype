from unittest.mock import MagicMock, patch

import pytest

from application.main import main

FILE_PATH = "application.main"


@patch(f"{FILE_PATH}.set_up_custom_logging")
@patch(f"{FILE_PATH}.create_markdown_pages")
def test_main(mock_create_markdown_pages: MagicMock, mock_set_up_custom_logging: MagicMock) -> None:
    # Act
    main()
    # Assert
    mock_set_up_custom_logging.assert_called_once_with()
    mock_create_markdown_pages.assert_called_once_with()


@patch(f"{FILE_PATH}.set_up_custom_logging")
@patch(f"{FILE_PATH}.create_markdown_pages")
def test_main__exception(mock_create_markdown_pages: MagicMock, mock_set_up_custom_logging: MagicMock) -> None:
    # Arrange
    mock_create_markdown_pages.side_effect = Exception("Test exception")
    # Act
    with pytest.raises(Exception, match="Test exception"):
        main()
    # Assert
    mock_set_up_custom_logging.assert_called_once_with()
    mock_create_markdown_pages.assert_called_once_with()
