from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from pygount import ProjectSummary, SourceAnalysis
from structlog import get_logger, stdlib
from itertools import chain
from application.github_interactions import clone_repo
from application.markdown.markdown import create_markdown_file, set_up_markdown_file

if TYPE_CHECKING:
    from mdutils.mdutils import MdUtils


logger: stdlib.BoundLogger = get_logger()


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
    markdown_file, total_files = add_language_summary_stats(markdown_file, path, repository_name)
    create_markdown_file(markdown_file)
    return total_files


def add_language_summary_stats(
    markdown_file: MdUtils, path_to_repo: str, repository_name: str
) -> tuple[MdUtils, int]:
    """Add language summary stats to the markdown file.

    Args:
        markdown_file (MdUtils): The markdown file object to add the stats to.
        path_to_repo (str): The path to the repository (already cloned).
        repository_name (str): The name of the repository.
    """
    # Get the project summary
    project_summary = get_language_summary_stats(path_to_repo, repository_name)
    # Set up table data
    headers = ["Language", "File Count", "SLOC", "Code Percentage"]
    # total_without_uncountable = project_summary.total_code_count - project_summary._language_to_language_summary_map["__unknown__"].code_count  # noqa: ERA001
    text_content = [
        (
            language_summary.language,
            language_summary.file_count,
            language_summary.source_count,
            round(language_summary.code_count/project_summary.total_code_count*100 if  language_summary.code_count != 0 else 0, 2),
        )
        for language_summary in project_summary.language_to_language_summary_map.values()
    ]
    sorted_languages = sorted(text_content, key=lambda text: text[3],reverse=True)
    table_content = headers + list(chain.from_iterable(sorted_languages))
    # Add the table
    markdown_file.new_header(level=1, title="Language Summary")
    markdown_file.new_table(columns=len(headers), rows=len(text_content) + 1, text=table_content, text_align="center")
    return markdown_file, project_summary.total_file_count


def get_language_summary_stats(path_to_repo: str, repository_name: str) -> ProjectSummary:
    """Add the language summary stats to the markdown file.

    Args:
        path_to_repo (str): The path to the repository (already cloned).
        repository_name (str): The name of the repository.
    """
    # Set up the project summary
    project_summary = ProjectSummary()
    # Scan the repository
    iterator = Path(path_to_repo).walk()
    for _root, _dirs, files in iterator:
        for file in files:
            file_path = f"{_root.__str__()}/{file}"
            logger.debug("Analysing file", file=file_path)
            project_summary.add(SourceAnalysis.from_file(file_path, repository_name))
    logger.info("Finished analysing", total_files=project_summary.total_file_count)
    # Return the project summary
    return project_summary
