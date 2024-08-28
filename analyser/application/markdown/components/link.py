from dataclasses import dataclass


@dataclass
class Link:
    """A link to a file.

    Attributes:
        file_path (str): The path to the file.
        title (str): The title of the file.
    """

    title: str
    file_path: str

    def __str__(self) -> str:
        """Return the link as a string.

        Returns:
            str: The link as a string.
        """
        return f"[{self.title}]({self.file_path})"
