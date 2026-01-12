"""
pdf2txt - A Python package to convert PDF files to text format

This package provides functionality to extract text from PDF files using 
different backend libraries like PyMuPDF and pdfplumber.
"""

from .core import convert_pdf_to_text, convert_pdf_to_text_advanced
from .utils import validate_pdf_path, sanitize_filename, get_pdf_info

__version__ = "0.1.0"
__author__ = "Your Name"
__license__ = "MIT"

__all__ = [
    "convert_pdf_to_text",
    "convert_pdf_to_text_advanced",
    "validate_pdf_path",
    "sanitize_filename",
    "get_pdf_info"
]