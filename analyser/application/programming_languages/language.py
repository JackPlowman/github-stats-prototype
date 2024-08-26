from __future__ import annotations

from dataclasses import dataclass


@dataclass(repr=True)
class Language:
    """A class to represent a programming language."""

    name: str
    language_type: str
    colour: str  # Should be hex colour code
    extensions: list[str]
    language_id: int
