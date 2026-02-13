"""Validator module for AUTOSAR class definitions.

This module provides XSD-based validation and auto-correction
for parsed AUTOSAR classes, enumerations, and primitives.

Requirements:
    SWR_PARSER_00031: XSD-based validation of parsed types
"""

from autosar_pdf2txt.validator.xsd_parser import (
    XsdAttribute,
    XsdClass,
    XsdParser,
)
from autosar_pdf2txt.validator.xsd_validator import XsdValidator

# Export static methods from XsdParser for convenience
xsd_to_camel_case = XsdParser.xsd_to_camel_case
camel_to_xsd_case = XsdParser.camel_to_xsd_case

__all__ = [
    "XsdParser",
    "XsdValidator",
    "XsdClass",
    "XsdAttribute",
    "xsd_to_camel_case",
    "camel_to_xsd_case",
]