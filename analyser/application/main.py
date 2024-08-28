from .markdown.markdown import set_up_index_page
from .repository import Repository
from .repository_analysis.repository_analysis import analyse_repository


def main() -> None:
    """Entrypoint for Application."""
    try:
        repositories = ["JackPlowman/github-stats"]
        repositories_stats = []
        for repository in repositories:
            total_files = analyse_repository(repository)
            repositories_stats.extend(
                [Repository(repository, "A repository for analysing GitHub repositories.", total_files)]
            )
        set_up_index_page(repositories_stats)
    except Exception as e:  # - Log out errors before exiting
        print(e)
        raise
