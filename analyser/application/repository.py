from dataclasses import dataclass


@dataclass
class Repository:
    """A GitHub repository."""

    name: str
    description: str
    file_count: int
