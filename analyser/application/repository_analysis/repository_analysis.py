from __future__ import annotations

from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING

from application.git_actions import clone_repo
from application.markdown import create_markdown_file, set_up_markdown_file
from application.programming_languages import get_languages

from .languages import count_files_per_language, determine_file_language

if TYPE_CHECKING:
    from mdutils.mdutils import MdUtils

    from application.programming_languages.language import Language


def analyse_repository(repository: str) -> int:
    """Analyse the repository.

    Args:
        repository (str): The repository name to analyse.

    Returns:
        int: The number of files in the repository.
    """
    owner_name, repository_name = repository.split("/", maxsplit=1)
    path = clone_repo(owner_name, repository_name)
    markdown_file = set_up_markdown_file(repository_name, f"{repository} Stats")
    markdown_file, total_files = add_file_counts(markdown_file, path)
    create_markdown_file(markdown_file)
    return total_files


def add_file_counts(markdown_file: MdUtils, path_to_repo: str) -> tuple[MdUtils, int]:
    """Add file counts to the markdown file.

    Args:
        markdown_file (MdUtils): The markdown file object.
        path_to_repo (str): The path to the repository (already cloned).

    Returns:
        MdUtils: The markdown file object.
        int: The total number of files in the repository.
    """
    # Get the list of programming languages
    languages = get_languages()
    # Catalogue the repository
    file_types = catalogue_repository(path_to_repo, languages)
    print(file_types)
    # Count the files per language
    file_counts = count_files_per_language(file_types)
    # Add the table of languages and file counts
    list_of_counts = zip(file_counts.keys(), file_counts.values())
    merged = list(chain.from_iterable(list_of_counts))
    file_count_headers = ["Language", "File Count"]
    markdown_file.new_table(columns=2, rows=len(file_counts) + 1, text=file_count_headers + merged)
    return markdown_file, sum(file_counts.values())


def catalogue_repository(file_path: str, languages: list[Language]) -> dict[str, list[str]]:
    """Catalogue the repository.

    Args:
        file_path (str): The path to the repository.
        exclude_paths (list[str]): The list of excluded paths.
        languages (list[Language]): The list of languages.

    Returns:
        file_types (dict[str, list[str]]): File type is the key and the list of file paths is the value.
    """
    catalogued_files = {}
    iterator = Path(file_path).walk()
    for root, _dirs, files in iterator:
        if check_for_excluded_dirs(root, []):
            continue
        for file in files:
            catalogued_files = determine_file_language(root, file, catalogued_files, languages)
    return catalogued_files


def check_for_excluded_dirs(root: Path, exclude_dirs: list[str]) -> bool:
    """Check if the root directory is excluded.

    Args:
        root (Path): The root directory.
        exclude_dirs (list[str]): The list of excluded directories.

    Returns:
        bool: True if the root directory is excluded, False otherwise.
    """
    return any(exclude_dir in root.__str__() for exclude_dir in exclude_dirs)
