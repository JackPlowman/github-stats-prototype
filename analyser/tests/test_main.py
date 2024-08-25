from analyser.main import main
from unittest.mock import patch, MagicMock

FILE_PATH = "analyser.main"


@patch(f"{FILE_PATH}.Github")
def test_main(mock_github: MagicMock):
    # Act
    main()
    # Assert
    mock_github.assert_called_once()

