from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from structlog import get_logger, stdlib

from yaml import safe_load

if TYPE_CHECKING:
    from application.programming_languages.language import Language

logger: stdlib.BoundLogger = get_logger()

def determine_file_language(
    root: Path, file_name: str, catalogued_files: dict[str, list[str]], languages: list[Language]
) -> dict[str, list[str]]:
    """Determine the language of a file.

    Args:
        root (Path): The root directory.
        file_name (str): The file name.
        catalogued_files (dict[str, list[str]]): File type is the key and the list of file paths is the value.
        languages (list[Language]): The list of languages.

    Returns:
        dict[str, list[str]]: File type is the key and the list of file paths is the value.
    """
    possible_matches = []
    shortened_file_path = f"{root.__str__()}/{file_name}".removeprefix("application/repos/")
    for language in languages:
        if file_name in language.filenames:
            catalogued_files = add_to_catalogued_files(shortened_file_path, catalogued_files, language)
            logger.debug("Catalogued file", language=language.name, file=file_name)
            break
        if any(file_name.endswith(extension) for extension in language.extensions):
            possible_matches.append(language)
    if len(possible_matches) == 0:
        return catalogued_files
    if len(possible_matches) == 1:
        add_to_catalogued_files(shortened_file_path, catalogued_files, possible_matches[0])
        logger.debug("Catalogued file", language=possible_matches[0].name, file=file_name)
    else:
        logger.debug("Multiple matches for file", file=file_name, matches=possible_matches)
        best_match_language = select_best_match(file_name, possible_matches)
        catalogued_files = add_to_catalogued_files(shortened_file_path, catalogued_files, best_match_language)
    return catalogued_files


def add_to_catalogued_files(
    file_name: str, catalogued_files: dict[str, list[str]], language: Language
) -> dict[str, list[str]]:
    """Add a file to the catalogued files.

    Args:
        file_name (str): The file name.
        catalogued_files (dict[str, list[str]]): File type is the key and the list of file paths is the value.
        language (Language): The language of the file.

    Returns:
        dict[str, list[str]]: File type is the key and the list of file paths is the value.
    """
    if language.name in catalogued_files:
        catalogued_files[language.name].append(file_name)
    else:
        catalogued_files[language.name] = [file_name]
    return catalogued_files


def count_files_per_language(file_types: dict[str, list[str]]) -> dict[str, int]:
    """Count the files per language.

    Args:
        file_types (dict[str, list[str]]): File type is the key and the list of file paths is the value.

    Returns:
        dict[str, int]: Language name is the key and the file count is the value.
    """
    file_counts = {}
    for language in file_types:
        file_counts[language] = len(file_types[language])
    return file_counts


def select_best_match(file_name: str, possible_matches: list[Language]) -> Language:
    """Select the best match for a file.

    Args:
        file_name (str): The file name.
        possible_matches (list[Language]): The list of possible matches.

    Returns:
        str: The best match for the file.
    """
    with Path.open("application/repository_analysis/prioritised_languages.yml") as file:
        prioritised_languages = safe_load(file)["languages"]
    best_matches = [
        possible_match for possible_match in possible_matches if language_match(possible_match, prioritised_languages)
    ]
    logger.debug("Best matches for file", file=file_name, matches=best_matches)

    if len(best_matches) == 0:
        return possible_matches[0]  # We have no prioritised languages, so just return the first match

    if len(best_matches) == 1:
        return best_matches[0]  # We have only one best match, perfect

    # We have multiple best matches, so we select the first best match
    return best_matches[0]


def language_match(language: Language, prioritised_languages: list[str]) -> bool:
    """Check if the language is in the prioritised languages.

    Args:
        language (Language): The language to check.
        prioritised_languages (list[str]): The list of prioritised languages.

    Returns:
        bool: True if the language is in the prioritised languages, False otherwise.
    """
    language_name = language.name.lower()
    prioritised_languages = [language.lower() for language in prioritised_languages]
    return language_name in prioritised_languages
