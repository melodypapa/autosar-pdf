"""
AUTOSAR metadata extraction module
"""

from .parser import extract_package_and_class_info
from .hierarchy import build_package_hierarchy
from .writer import write_markdown_hierarchy, write_text_summary
from .integration import extract_from_pdf, extract_from_multiple_pdfs
from .models import Package, Class

__all__ = [
    "extract_package_and_class_info",
    "build_package_hierarchy",
    "write_markdown_hierarchy",
    "write_text_summary",
    "extract_from_pdf",
    "extract_from_multiple_pdfs",
    "Package",
    "Class",
]
