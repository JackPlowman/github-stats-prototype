from unittest.mock import MagicMock

from application.repository_analysis.languages import (
    add_to_catalogued_files,
    count_files_per_language,
    determine_file_language,
    language_match,
    select_best_match,
)

FILE_PATH = "application.repository_analysis.languages"


def test_determine_file_language() -> None:
    # Arrange
    mock_path = MagicMock()
    mock_file_name = "file.py"
    mock_catalogued_files = {}
    mock_language = MagicMock()
    mock_language.extensions = [".py"]
    mock_language.name = "Python"
    # Act
    response = determine_file_language(mock_path, mock_file_name, mock_catalogued_files, [mock_language])
    # Assert
    assert response == {mock_language.name: [f"{mock_path}/{mock_file_name}"]}


def test_add_to_catalogued_files() -> None:
    # Arrange
    mock_catalogued_files = "test.py"
    mock_language = MagicMock()
    mock_language.extensions = [".py"]
    mock_language.name = "Python"
    catalogued_files = {"Markdown": ["file1.md", "file2.md"]}
    # Act
    response = add_to_catalogued_files(mock_catalogued_files, catalogued_files, mock_language)
    # Assert
    assert response == catalogued_files | {mock_language.name: ["test.py"]}


def test_count_files_per_language() -> None:
    # Arrange
    file_types = {"Python": ["file1.py", "file2.py"]}
    # Act
    response = count_files_per_language(file_types)
    # Assert
    assert response == {"Python": 2}


def test_select_best_match() -> None:
    # Arrange
    mock_file_name = "file.py"
    mock_possible_matches = [MagicMock(), MagicMock()]
    mock_possible_matches[0].name = "Python"
    mock_possible_matches[1].name = "Javascript"
    # Act
    response = select_best_match(mock_file_name, mock_possible_matches)
    # Assert
    assert response == mock_possible_matches[0]


def test_language_match() -> None:
    # Arrange
    mock_language = MagicMock()
    mock_language.name = "Python"
    mock_prioritised_languages = ["Python", "Javascript"]
    # Act
    response = language_match(mock_language, mock_prioritised_languages)
    # Assert
    assert response is True


def test_language_match__no_match() -> None:
    # Arrange
    mock_language = MagicMock()
    mock_language.name = "Java"
    mock_prioritised_languages = ["Python", "Javascript"]
    # Act
    response = language_match(mock_language, mock_prioritised_languages)
    # Assert
    assert response is False
