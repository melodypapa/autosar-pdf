"""
PDF conversion using class-based approach
"""

import pypdf
import pdfplumber
from typing import Union, List, Optional, TypedDict, Any
from pathlib import Path


class ConversionResult(TypedDict, total=False):
    text: str
    page_count: int
    pages_extracted: int
    images: Optional[List[dict[str, Any]]]


class PdfConverter:
    """
    PDF converter class supporting multiple backends.

    This class provides methods to convert PDF files to text using
    either pypdf or pdfplumber as the backend.
    """

    def __init__(self, method: str = "pypdf2", progress_callback=None):
        """
        Initialize PDF converter.

        Args:
            method (str): Backend method to use ("pypdf2" or "pdfplumber", default: "pypdf2")
            progress_callback: Optional callback function for progress updates

        Raises:
            ValueError: If method is not supported
        """
        if method not in ["pypdf2", "pdfplumber"]:
            raise ValueError(
                f"Unsupported method: {method}. Use 'pypdf2' or 'pdfplumber'."
            )
        self.method = method
        self.progress_callback = progress_callback

    def _extract_page_text_pypdf2(
        self,
        page: pypdf.PageObject,
        skip_header_lines: int = 0,
        skip_footer_lines: int = 0,
    ) -> str:
        """
        Extract text from a single page using pypdf.

        Args:
            page (pypdf.PageObject): Page object to extract text from
            skip_header_lines (int): Number of lines to skip at beginning
            skip_footer_lines (int): Number of lines to skip at end

        Returns:
            str: Extracted text from the page
        """
        page_text = page.extract_text()

        if not page_text:
            return ""

        lines = page_text.split("\n")
        if skip_header_lines > 0:
            lines = lines[skip_header_lines:]
        if skip_footer_lines > 0:
            lines = lines[:-skip_footer_lines] if len(lines) > skip_footer_lines else []

        return "\n".join(lines) + "\n"

    def _extract_page_text_pdfplumber(
        self, page: Any, skip_header_lines: int = 0, skip_footer_lines: int = 0
    ) -> str:
        """
        Extract text from a single page using pdfplumber.

        Args:
            page: pdfplumber page object
            skip_header_lines (int): Number of lines to skip at beginning
            skip_footer_lines (int): Number of lines to skip at end

        Returns:
            str: Extracted text from the page
        """
        page_text = page.extract_text()

        if not page_text:
            return ""

        lines = page_text.split("\n")
        if skip_header_lines > 0:
            lines = lines[skip_header_lines:]
        if skip_footer_lines > 0:
            lines = lines[:-skip_footer_lines] if len(lines) > skip_footer_lines else []

        return "\n".join(lines) + "\n"

    def convert(
        self, pdf_path: str, skip_header_lines: int = 0, skip_footer_lines: int = 0
    ) -> str:
        """
        Convert PDF to text using configured method.

        Args:
            pdf_path (str): Path to PDF file
            skip_header_lines (int): Number of lines to skip at beginning of each page
            skip_footer_lines (int): Number of lines to skip at end of each page

        Returns:
            str: Extracted text from the PDF

        Raises:
            FileNotFoundError: If PDF file does not exist
        """
        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        text = ""

        if self.method == "pypdf2":
            with open(pdf_path, "rb") as file:
                pdf_reader = pypdf.PdfReader(file)
                total_pages = len(pdf_reader.pages)

                for idx, page in enumerate(pdf_reader.pages):
                    text += self._extract_page_text_pypdf2(
                        page, skip_header_lines, skip_footer_lines
                    )
                    if self.progress_callback:
                        self.progress_callback(idx, total_pages)
        elif self.method == "pdfplumber":
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)

                for idx, page in enumerate(pdf.pages):  # type: ignore
                    text += self._extract_page_text_pdfplumber(
                        page, skip_header_lines, skip_footer_lines
                    )
                    if self.progress_callback:
                        self.progress_callback(idx, total_pages)

        return text

    def convert_advanced(
        self,
        pdf_path: str,
        page_range: Optional[List[int]] = None,
        include_images: bool = False,
        skip_header_lines: int = 0,
        skip_footer_lines: int = 0,
    ) -> ConversionResult:
        """
        Advanced PDF to text conversion with additional options.

        Args:
            pdf_path (str): Path to PDF file
            page_range (Optional[List[int]]): List of specific page numbers (0-indexed)
            include_images (bool): Whether to extract image information
            skip_header_lines (int): Number of lines to skip at beginning
            skip_footer_lines (int): Number of lines to skip at end

        Returns:
            dict: Dictionary containing extracted text and metadata

        Raises:
            FileNotFoundError: If PDF file does not exist
        """
        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        with open(pdf_path, "rb") as file:
            pdf_reader = pypdf.PdfReader(file)

            if page_range is None:
                page_range = list(range(len(pdf_reader.pages)))
            else:
                page_range = [p for p in page_range if 0 <= p < len(pdf_reader.pages)]

            result: ConversionResult = {
                "text": "",
                "page_count": len(pdf_reader.pages),
                "pages_extracted": len(page_range),
                "images": [] if include_images else None,
            }

            for page_num in page_range:
                page = pdf_reader.pages[page_num]
                page_text = self._extract_page_text_pypdf2(
                    page, skip_header_lines, skip_footer_lines
                )
                result["text"] += page_text

        return result

    @staticmethod
    def get_page_count(pdf_path: str) -> int:
        """
        Get the number of pages in a PDF file.

        Args:
            pdf_path (str): Path to PDF file

        Returns:
            int: Number of pages in the PDF

        Raises:
            FileNotFoundError: If PDF file does not exist
        """
        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        with open(pdf_path, "rb") as file:
            pdf_reader = pypdf.PdfReader(file)
            return len(pdf_reader.pages)


def convert_pdf_to_text(
    pdf_path: str,
    method: str = "pypdf2",
    skip_header_lines: int = 0,
    skip_footer_lines: int = 0,
    progress_callback=None,
) -> str:
    """
    Convert PDF to text using specified method (backward compatibility function).

    Args:
        pdf_path (str): Path to PDF file
        method (str): Method to use for conversion ("pypdf2" or "pdfplumber")
        skip_header_lines (int): Number of lines to skip at beginning
        skip_footer_lines (int): Number of lines to skip at end
        progress_callback: Optional callback function for progress updates

    Returns:
        str: Extracted text from the PDF
    """
    converter = PdfConverter(method=method, progress_callback=progress_callback)
    return converter.convert(pdf_path, skip_header_lines, skip_footer_lines)


def convert_pdf_to_text_advanced(
    pdf_path: str,
    page_range: Union[list, None] = None,
    include_images: bool = False,
    skip_header_lines: int = 0,
    skip_footer_lines: int = 0,
) -> ConversionResult:
    """
    Advanced PDF to text conversion (backward compatibility function).

    Args:
        pdf_path (str): Path to PDF file
        page_range (list, optional): List of specific page numbers
        include_images (bool): Whether to extract image information
        skip_header_lines (int): Number of lines to skip at beginning
        skip_footer_lines (int): Number of lines to skip at end

    Returns:
        dict: Dictionary containing extracted text and metadata
    """
    converter = PdfConverter(method="pypdf2")
    return converter.convert_advanced(
        pdf_path, page_range, include_images, skip_header_lines, skip_footer_lines
    )
