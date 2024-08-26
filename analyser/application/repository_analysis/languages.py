from __future__ import annotations

from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING

from git import Repo

from application.programming_languages import get_languages

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
    file_types = catalogue_repository(path)
    # Count the files per language
    file_counts = count_files_per_language(file_types, languages)
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


def catalogue_repository(file_path: str) -> dict[str, list[str]]:
    """Catalogue the repository.

    Args:
        file_path (str): The path to the repository.
        exclude_paths (list[str]): The list of excluded paths.

    Returns:
        file_types (dict[str, list[str]]): File type is the key and the list of file paths is the value.
    """
    file_types = {}

    iterator = Path(file_path).walk()
    for root, _dirs, files in iterator:
        if check_for_excluded_dirs(root, []):
            continue
        for file in files:
            file_types = tally_file_types(root, file, file_types)
    return file_types


def check_for_excluded_dirs(root: Path, exclude_dirs: list[str]) -> bool:
    """Check if the root directory is excluded.

    Args:
        root (Path): The root directory.
        exclude_dirs (list[str]): The list of excluded directories.

    Returns:
        bool: True if the root directory is excluded, False otherwise.
    """
    return any(exclude_dir in root.__str__() for exclude_dir in exclude_dirs)


def tally_file_types(root: Path, file_name: str, file_types: dict[str, list[str]]) -> dict[str, list[str]]:
    """Tally the file types in the repository.

    Args:
        root (Path): The root directory.
        file_name (str): The file name.
        file_types (dict[str, list[str]]): File type is the key and the list of file paths is the value.

    Returns:
        dict[str, int]: File type is the key and the list of file paths is the value.
    """
    shortened_file_path = f"{root.__str__()}/{file_name}".removeprefix("application/repos/")
    file_extension = Path(file_name).suffix
    if file_extension == "":
        return file_types
    if file_extension in file_types:
        file_types[file_extension].append(shortened_file_path)
    else:
        file_types[file_extension] = [shortened_file_path]
    return file_types


def count_files_per_language(file_types: dict[str, list[str]], languages: list[Language]) -> dict[str, int]:
    """Count the files per language.

    Args:
        file_types (dict[str, list[str]]): File type is the key and the list of file paths is the value.
        languages (list[Language]): The list of languages.

    Returns:
        dict[str, int]: Language name is the key and the file count is the value.
    """
    file_counts = {}
    for file_type, file_paths in file_types.items():
        file_count = len(file_paths)
        for language in languages:
            if file_type in language.extensions:
                # Can't handle multiple matches on extensions, so just take the first one
                # TODO: Handle multiple matches on extensions, use GitHub API to get/confirm the language  # noqa: E501, FIX002, TD002
                # https://github.com/JackPlowman/github-stats/issues/35
                file_counts[language.name] = file_count
                break
    return file_counts
