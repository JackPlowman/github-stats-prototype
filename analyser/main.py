from github import Github
from mdutils.mdutils import MdUtils


def main() -> None:
    """Entrypoint for Application."""
    try:
        github = Github()
        github_stats = github.get_repo("JackPlowman/github-stats")
        print(github_stats.get_languages())
        create_markdown_file()
    except Exception as e:  # noqa: BLE001 - Log out errors before exiting
        print(e)
    finally:
        github.close()


def create_markdown_file() -> None:
    """Create the markdown file."""
    markdown_file = MdUtils(file_name="markdown/index.md", title="GitHub Stats Repository")
    markdown_file.create_md_file()


if __name__ == "__main__":
    main()
