from functools import reduce

from github import Github
from mdutils.mdutils import MdUtils


def set_up_markdown_file(file_path: str, title: str) -> MdUtils:
    """Set up the markdown file.

    Args:
        file_path (str): The file path to the markdown file.
        title (str): The title of the markdown file.

    Returns:
        MdUtils: The markdown file object.
    """
    build_directory = "application/generated_markdown"
    return MdUtils(file_name=f"{build_directory}/{file_path}", title=title)


def create_markdown_file(markdown_file: MdUtils) -> None:
    """Create the markdown file.

    Args:
        markdown_file (MdUtils): The markdown file object.
    """
    markdown_file.create_md_file()


def add_languages_sloc_table(github: Github, markdown_file: MdUtils) -> MdUtils:
    """Add languages sloc table to the markdown file.

    Args:
        github (Github): The github object.
        markdown_file (MdUtils): The markdown file object.

    Returns:
        MdUtils: The markdown file object.
    """
    github_stats = github.get_repo("JackPlowman/github-stats")  # Get Repository class
    languages = github_stats.get_languages()  # Interpret repository data
    table_headers = ["Language", "Software Bytes of Code"]
    languages_list = list(reduce(lambda x, y: x + y, languages.items()))
    markdown_file.new_table(
        rows=int(len(languages_list) / 2) + 1,
        columns=len(table_headers),
        text=table_headers + languages_list,
    )
    return markdown_file
