from github import Github


def main() -> None:
    """Entrypoint for Application."""
    try:
        github = Github()
        github_stats = github.get_repo("JackPlowman/github-stats")
        print(github_stats.get_languages())
    except Exception as e:
        print(e)
    finally:
        github.close()


if __name__ == "__main__":
    main()
