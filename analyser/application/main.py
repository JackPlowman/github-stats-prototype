from github import Github

from .markdown import create_markdown_file, set_up_markdown_file
from .software_lines_of_code.sloc import add_languages_sloc_table


def main() -> None:
    """Entrypoint for Application."""
    try:
        github = Github()
        markdown_file = set_up_markdown_file("index", "GitHub Stats Repository")
        markdown_file = add_languages_sloc_table(markdown_file)
        create_markdown_file(markdown_file)
    except Exception as e:  # - Log out errors before exiting
        print(e)
        raise
    finally:
        github.close()
