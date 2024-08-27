from __future__ import annotations

from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING

from git import Repo

from application.programming_languages import get_languages

from .languages import count_files_per_language, determine_file_language

if TYPE_CHECKING:
    from mdutils.mdutils import MdUtils

    from application.programming_languages.language import Language


def add_languages_sloc_table(markdown_file: MdUtils) -> MdUtils:
    """Add languages sloc table to the markdown file.

    Args:
        markdown_file (MdUtils): The markdown file object.

    Returns:
        MdUtils: The markdown file object.
    """
    # Clone the target repository
    path = clone_repo("JackPlowman", "github-stats")
    # Get the list of programming languages
    languages = get_languages()
    # Catalogue the repository
    file_types = catalogue_repository(path, languages)
    print(file_types)
    # Count the files per language
    file_counts = count_files_per_language(file_types)
    # Add the table of languages and file counts
    list_of_counts = zip(file_counts.keys(), file_counts.values())
    merged = list(chain.from_iterable(list_of_counts))
    headers = ["Language", "File Count"]
    markdown_file.new_table(columns=2, rows=len(file_counts) + 1, text=headers + merged)
    return markdown_file


def clone_repo(owner_name: str, repository_name: str) -> str:
    """Clone the repository and return the path to the repository.

    Uses existing clone if available in application/repos.

    Args:
        owner_name (str): The owner name of the repository.
        repository_name (str): The repository name.

    Returns:
        str: The path to the repository.
    """
    file_path = f"application/repos/{repository_name}"
    if not Path.exists(Path(file_path)):
        repo_url = f"https://github.com/{owner_name}/{repository_name}.git"
        Repo.clone_from(repo_url, Path(file_path))
    return file_path


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
