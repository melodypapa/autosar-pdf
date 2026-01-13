"""
pdf2txt - A Python package to convert PDF files to text format

This package provides functionality to extract text from PDF files using
different backend libraries like pypdf and pdfplumber.
"""

from .core import (
    convert_pdf_to_text,
    convert_pdf_to_text_advanced,
    extract_tables_from_pdf,
    convert_table_to_markdown,
    convert_pdf_with_tables,
    clean_special_characters,
    convert_to_markdown,
)
from .core.converter import PdfConverter
from .core.cleaner import TextCleaner
from .core.table import TableExtractor, TableConverter
from .core.markdown import MarkdownConverter
from .core.integration import PdfConverterWithTables
from .utils import validate_pdf_path, sanitize_filename, get_pdf_info
from .extractor import (
    extract_package_and_class_info,
    build_package_hierarchy,
    write_markdown_hierarchy,
    write_text_summary,
    extract_from_pdf,
)
from .extractor.models import Package, Class
from .extractor.parser import AutosarParser
from .extractor.hierarchy import PackageHierarchyBuilder
from .extractor.writer import OutputWriter
from .extractor.integration import AutosarExtractor

__version__ = "0.2.0"
__author__ = "Your Name"
__license__ = "MIT"

__all__ = [
    "convert_pdf_to_text",
    "convert_pdf_to_text_advanced",
    "convert_to_markdown",
    "clean_special_characters",
    "extract_tables_from_pdf",
    "convert_table_to_markdown",
    "convert_pdf_with_tables",
    "validate_pdf_path",
    "sanitize_filename",
    "get_pdf_info",
    "extract_package_and_class_info",
    "build_package_hierarchy",
    "write_markdown_hierarchy",
    "write_text_summary",
    "extract_from_pdf",
    "PdfConverter",
    "TextCleaner",
    "TableExtractor",
    "TableConverter",
    "MarkdownConverter",
    "PdfConverterWithTables",
    "Package",
    "Class",
    "AutosarParser",
    "PackageHierarchyBuilder",
    "OutputWriter",
    "AutosarExtractor",
]
