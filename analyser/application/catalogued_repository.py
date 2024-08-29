from dataclasses import dataclass


@dataclass
class CataloguedRepository:
    """A GitHub repository."""

    name: str
    description: str
    file_count: int
    commit_count: int
