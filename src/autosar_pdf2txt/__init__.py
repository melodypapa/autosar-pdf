"""AUTOSAR package and class hierarchy management with markdown output."""

__version__ = "0.1.0"

from autosar_pdf2txt.models import (
    AutosarAttribute,
    AutosarClass,
    AutosarEnumLiteral,
    AutosarEnumeration,
    AutosarPackage,
)
from autosar_pdf2txt.parser import PdfParser
from autosar_pdf2txt.writer import MarkdownWriter

__all__ = [
    "AutosarAttribute",
    "AutosarClass",
    "AutosarEnumLiteral",
    "AutosarEnumeration",
    "AutosarPackage",
    "PdfParser",
    "MarkdownWriter",
    "__version__",
]
