from __future__ import annotations

from requests import get
from yaml import safe_load

from .language import Language


def get_languages() -> list[Language]:
    """Get the list of programming languages.

    Args:
        languages (list[dict]): The list of languages.

    Returns:
        list[Language]: The list of languages.
    """
    languages_file = get_languages_file()
    languages: dict[str, dict] = safe_load(languages_file)
    return [
        Language(
            name=key,
            language_type=language["type"],
            colour=language.get("color", ""),
            extensions=language.get("extensions", []),
            language_id=language["language_id"],
            filenames=language.get("filenames", []),
            group=language.get("group", None),
        )
        for key, language in languages.items()
    ]


def get_languages_file() -> str:
    """Get the languages file.

    Returns:
        str: contents of the languages file.
    """
    # Built using v7.30.0 of github-linguist
    response = get(
        url="https://raw.githubusercontent.com/github-linguist/linguist/master/lib/linguist/languages.yml", timeout=10
    )
    return response.text
