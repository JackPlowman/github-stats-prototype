from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .language import Language


class Languages:
    """A class to represent a list of programming languages."""

    _languages: list[Language]

    def __init__(self) -> None:
        """Initialize the class."""

    @property
    def languages(self) -> list[Language]:
        """Get the list of languages.

        Returns:
            List[Language]: The list of languages.
        """
        return self._languages
