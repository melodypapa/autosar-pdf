"""AUTOSAR package and class hierarchy management with markdown output."""

__version__ = "0.14.0"

from autosar_pdf2txt.models import (
    AttributeKind,
    AutosarAttribute,
    AutosarClass,
    AutosarDoc,
    AutosarEnumLiteral,
    AutosarEnumeration,
    AutosarPackage,
    AutosarPrimitive,
)
from autosar_pdf2txt.parser import PdfParser
from autosar_pdf2txt.writer import MarkdownWriter

__all__ = [
    "AttributeKind",
    "AutosarAttribute",
    "AutosarClass",
    "AutosarDoc",
    "AutosarEnumLiteral",
    "AutosarEnumeration",
    "AutosarPackage",
    "AutosarPrimitive",
    "PdfParser",
    "MarkdownWriter",
    "__version__",
]
