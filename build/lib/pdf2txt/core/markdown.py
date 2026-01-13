"""
Markdown format conversion using class-based approach
"""

from typing import Optional
from .cleaner import TextCleaner


class MarkdownConverter:
    """
    Markdown converter class for converting plain text to Markdown format.

    This class provides methods to convert plain text to Markdown,
    with optional structure preservation for headings and formatting.
    """

    def __init__(self, text_cleaner: Optional[TextCleaner] = None):
        """
        Initialize Markdown converter.

        Args:
            text_cleaner (Optional[TextCleaner]): Text cleaner instance for preprocessing
        """
        self.text_cleaner = text_cleaner or TextCleaner()

    def convert(self, text: str, preserve_structure: bool = True) -> str:
        """
        Convert plain text to markdown format.

        Args:
            text (str): Plain text to convert
            preserve_structure (bool): Whether to preserve document structure with headings

        Returns:
            str: Markdown formatted text
        """
        text = self.text_cleaner.clean(text)

        lines = text.split("\n")
        markdown_lines = []

        for line in lines:
            stripped = line.strip()

            if not stripped:
                markdown_lines.append("")
                continue

            if preserve_structure:
                markdown_line = self._convert_with_structure(stripped)
            else:
                markdown_line = self._convert_simple(stripped)

            markdown_lines.append(markdown_line)

        return "\n".join(markdown_lines)

    def _convert_with_structure(self, line: str) -> str:
        """
        Convert line with structure detection.

        Args:
            line (str): Line to convert

        Returns:
            str: Converted line
        """
        is_heading, heading_level = self._detect_heading(line)

        if is_heading:
            return "#" * heading_level + " " + line
        else:
            return self._escape_markdown(line)

    def _convert_simple(self, line: str) -> str:
        """
        Convert line without structure detection.

        Args:
            line (str): Line to convert

        Returns:
            str: Converted line
        """
        return self._escape_markdown(line)

    def _detect_heading(self, line: str) -> tuple[bool, int]:
        """
        Detect if line is a heading and determine level.

        Args:
            line (str): Line to analyze

        Returns:
            tuple[bool, int]: (is_heading, heading_level)
        """
        # Detect numbered sections (e.g., "1. Introduction", "2.1 Overview")
        if len(line) < 100 and line[0].isdigit() and "." in line[:10]:
            heading_level = line[:10].count(".") + 2
            heading_level = min(heading_level, 6)
            return True, heading_level

        # Detect all caps headings (short, all uppercase)
        if len(line) < 80 and line.isupper() and len(line.split()) >= 2:
            return True, 2

        # Detect centered-like headings (short, not ending with punctuation)
        if len(line) < 80 and not line.endswith((".", ",", ";", ":")):
            if line[0].isupper() and len(line.split()) >= 2:
                return True, 2

        return False, 0

    @staticmethod
    def _escape_markdown(text: str) -> str:
        """
        Escape special markdown characters.

        Args:
            text (str): Text to escape

        Returns:
            str: Escaped text
        """
        escaped = text.replace("*", "\\*")
        escaped = escaped.replace("_", "\\_")
        escaped = escaped.replace("[", "\\[")
        escaped = escaped.replace("]", "\\]")
        return escaped


def convert_to_markdown(text: str, preserve_structure: bool = True) -> str:
    """
    Convert plain text to markdown (backward compatibility function).

    Args:
        text (str): Plain text to convert
        preserve_structure (bool): Whether to preserve document structure

    Returns:
        str: Markdown formatted text
    """
    converter = MarkdownConverter()
    return converter.convert(text, preserve_structure)
