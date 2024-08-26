from github import Github

from analyser.markdown import add_languages_sloc_table, create_markdown_file, set_up_markdown_file


def main() -> None:
    """Entrypoint for Application."""
    try:
        github = Github()
        markdown_file = set_up_markdown_file("index", "GitHub Stats Repository")
        markdown_file = add_languages_sloc_table(github, markdown_file)
        create_markdown_file(markdown_file)
    except Exception as e:  # noqa: BLE001 - Log out errors before exiting
        print(e)
    finally:
        github.close()


if __name__ == "__main__":
    main()
