from unittest.mock import MagicMock, patch

from analyser.main import main

FILE_PATH = "analyser.main"


@patch(f"{FILE_PATH}.Github")
def test_main(mock_github: MagicMock) -> None:
    # Act
    main()
    # Assert
    mock_github.assert_called_once()
