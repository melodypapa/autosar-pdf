"""
Text cleaning using class-based approach
"""

import re


class TextCleaner:
    """
    Text cleaner class for handling special characters and formatting.

    This class provides methods to clean and normalize text extracted
    from PDF files, removing special characters and normalizing formatting.
    """

    def __init__(self):
        """
        Initialize text cleaner.
        """
        self.control_pattern = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
        self.bullet_pattern = re.compile(r"[\x95\u2022\u2023\u25e6\u2043]")
        self.whitespace_pattern = re.compile(r"[\u00a0\u2000-\u200a\u202f\u205f\u3000]")

    def clean(self, text: str) -> str:
        """
        Clean special characters from text.

        Args:
            text (str): Text to clean

        Returns:
            str: Cleaned text with special characters removed or replaced
        """
        # Remove control characters (except common ones like \n, \r, \t)
        # Keep: \n (10), \r (13), \t (9)
        # Remove: other control characters (0-8, 11, 12, 14-31, 127)
        text = self.control_pattern.sub("", text)

        # Replace bullet-like characters with standard bullet
        text = self.bullet_pattern.sub("•", text)

        # Replace common special quotes with standard quotes
        text = text.replace("\u2018", "'").replace("\u2019", "'")
        text = text.replace("\u201c", '"').replace("\u201d", '"')
        text = text.replace("\u2013", "-").replace("\u2014", "--")

        # Replace common whitespace characters with standard space
        text = self.whitespace_pattern.sub(" ", text)

        return text

    @staticmethod
    def remove_extra_whitespace(text: str) -> str:
        """
        Remove extra whitespace from text.

        Args:
            text (str): Text to normalize

        Returns:
            str: Text with normalized whitespace
        """
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def normalize_newlines(text: str) -> str:
        """
        Normalize newlines in text.

        Args:
            text (str): Text to normalize

        Returns:
            str: Text with normalized newlines
        """
        text = re.sub(r"\r\n", "\n", text)
        text = re.sub(r"\r", "\n", text)
        return re.sub(r"\n{3,}", "\n\n", text)


def clean_special_characters(text: str) -> str:
    """
    Clean special characters from text (backward compatibility function).

    Args:
        text (str): Text to clean

    Returns:
        str: Cleaned text with special characters removed or replaced
    """
    cleaner = TextCleaner()
    return cleaner.clean(text)
