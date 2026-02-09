"""AUTOSAR package and class hierarchy management with markdown output.

Requirements:
    SWR_PACKAGE_00001: Package API Export
    SWR_PACKAGE_00002: Python Version Support
    SWR_PACKAGE_00003: Package Metadata
"""

__version__ = "1.0.0"

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
from autosar_pdf2txt.writer import MarkdownWriter, MappingWriter

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
    "MappingWriter",
    "__version__",
]
