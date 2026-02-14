"""Utility functions for autosar-pdf2txt."""

from pathlib import Path


def detect_format(filepath: str) -> str:
    """
    Detect output format from file extension.

    Args:
        filepath: Path to output file

    Returns:
        "markdown" or "json"

    Raises:
        ValueError: If file extension is not supported

    Requirements:
        SWR_CLI_00019: Format auto-detection from file extension
    """
    path = Path(filepath)
    extension = path.suffix.lower()

    format_map = {
        ".md": "markdown",
        ".markdown": "markdown",
        ".json": "json",
    }

    if extension in format_map:
        return format_map[extension]

    if not extension:
        # No extension, default to markdown
        return "markdown"

    raise ValueError(
        f"Unknown format {extension} (supported: .md, .markdown, .json)"
    )