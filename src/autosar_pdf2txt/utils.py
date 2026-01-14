"""
Utility functions for pdf2txt using class-based approach
"""

import os
from pathlib import Path
import re


class FileUtils:
    """
    File utilities class for file system operations and PDF file handling.

    This class provides methods for file validation, path manipulation,
    and PDF-specific file operations.
    """

    def validate_pdf_path(self, pdf_path: str) -> bool:
        """
        Validate if the given path is a valid PDF file.

        Args:
            pdf_path (str): Path to validate

        Returns:
            bool: True if path is a valid PDF file, False otherwise
        """
        path = Path(pdf_path)
        return path.exists() and path.is_file() and path.suffix.lower() == ".pdf"

    def sanitize_filename(self, filename: str) -> str:
        """
        Remove invalid characters from filename.

        Args:
            filename (str): Original filename

        Returns:
            str: Sanitized filename
        """
        sanitized = re.sub(r'[<>:"/\\|?*]', "_", filename)
        return sanitized

    def get_pdf_info(self, pdf_path: str) -> dict:
        """
        Get basic information about a PDF file.

        Args:
            pdf_path (str): Path to the PDF file

        Returns:
            dict: Dictionary containing file info (size, page count, etc.)

        Raises:
            ImportError: If PyMuPDF (fitz) is not installed
        """
        try:
            import fitz
        except ImportError:
            raise ImportError(
                "PyMuPDF (fitz) is not installed. Install it with: pip install pymupdf"
            )

        file_size = os.path.getsize(pdf_path)
        doc = fitz.open(pdf_path)

        info = {
            "file_path": pdf_path,
            "file_size_bytes": file_size,
            "file_size_mb": round(file_size / (1024 * 1024), 2),
            "page_count": doc.page_count,
            "metadata": doc.metadata,
        }

        doc.close()
        return info

    def format_file_size(self, size_bytes: int) -> str:
        """
        Format file size in human readable format.

        Args:
            size_bytes (int): File size in bytes

        Returns:
            str: Formatted file size
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{round(size_bytes / 1024, 2)} KB"
        elif size_bytes < 1024**3:
            return f"{round(size_bytes / (1024**2), 2)} MB"
        else:
            return f"{round(size_bytes / (1024**3), 2)} GB"

    def create_output_directory(self, output_path: str) -> Path:
        """
        Create output directory if it doesn't exist.

        Args:
            output_path (str): Path for output

        Returns:
            Path: Path object of the output directory
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path.parent


def validate_pdf_path(pdf_path: str) -> bool:
    """
    Validate if the given path is a valid PDF file (backward compatibility function).

    Args:
        pdf_path (str): Path to validate

    Returns:
        bool: True if path is a valid PDF file, False otherwise
    """
    utils = FileUtils()
    return utils.validate_pdf_path(pdf_path)


def sanitize_filename(filename: str) -> str:
    """
    Remove invalid characters from filename (backward compatibility function).

    Args:
        filename (str): Original filename

    Returns:
        str: Sanitized filename
    """
    utils = FileUtils()
    return utils.sanitize_filename(filename)


def get_pdf_info(pdf_path: str) -> dict:
    """
    Get basic information about a PDF file (backward compatibility function).

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        dict: Dictionary containing file info (size, page count, etc.)
    """
    utils = FileUtils()
    return utils.get_pdf_info(pdf_path)


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format (backward compatibility function).

    Args:
        size_bytes (int): File size in bytes

    Returns:
        str: Formatted file size
    """
    utils = FileUtils()
    return utils.format_file_size(size_bytes)


def create_output_directory(output_path: str) -> Path:
    """
    Create output directory if it doesn't exist (backward compatibility function).

    Args:
        output_path (str): Path for output

    Returns:
        Path: Path object of the output directory
    """
    utils = FileUtils()
    return utils.create_output_directory(output_path)
