"""Pytest configuration and fixtures for integration tests.

This module provides session-scoped fixtures for caching parsed PDF data,
significantly improving integration test performance by avoiding redundant
PDF parsing across multiple tests.
"""

import os
from typing import Dict, List

import pytest

from autosar_pdf2txt.models import AutosarDoc, AutosarPackage
from autosar_pdf2txt.parser import PdfParser


@pytest.fixture(scope="session")
def parser() -> PdfParser:
    """Create a single PdfParser instance for the entire test session.

    This fixture is session-scoped to avoid creating multiple parser instances.

    Returns:
        Shared PdfParser instance for all tests.
    """
    return PdfParser()


@pytest.fixture(scope="session")
def bsw_template_pdf(parser: PdfParser) -> AutosarDoc:
    """Parse and cache the BSW Module Template PDF.

    This fixture parses the PDF once per session and caches the result.
    All tests using this fixture share the same parsed data, avoiding
    redundant I/O and parsing operations.

    Args:
        parser: Shared PdfParser instance.

    Returns:
        AutosarDoc containing parsed packages and root classes.

    Skips:
        If the PDF file is not found.
    """
    pdf_path = "examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf"

    if not os.path.exists(pdf_path):
        pytest.skip(f"PDF file not found: {pdf_path}")

    return parser.parse_pdf(pdf_path)


@pytest.fixture(scope="session")
def ecu_configuration_pdf(parser: PdfParser) -> AutosarDoc:
    """Parse and cache the ECU Configuration PDF.

    This fixture parses the PDF once per session and caches the result.

    Args:
        parser: Shared PdfParser instance.

    Returns:
        AutosarDoc containing parsed packages and root classes.

    Skips:
        If the PDF file is not found.
    """
    pdf_path = "examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf"

    if not os.path.exists(pdf_path):
        pytest.skip(f"PDF file not found: {pdf_path}")

    return parser.parse_pdf(pdf_path)


@pytest.fixture(scope="session")
def pdf_cache(parser: PdfParser) -> Dict[str, AutosarDoc]:
    """Parse and cache all available AUTOSAR PDF files.

    This fixture provides a dictionary mapping PDF filenames to their
    parsed document structures. All PDFs are parsed once per session,
    enabling tests to access any PDF without redundant parsing.

    Args:
        parser: Shared PdfParser instance.

    Returns:
        Dictionary with PDF filenames as keys and AutosarDoc objects as values.

    Skips:
        If no PDF files are found.
    """
    pdf_dir = "examples/pdf"
    cache: Dict[str, AutosarDoc] = {}

    if not os.path.exists(pdf_dir):
        pytest.skip(f"PDF directory not found: {pdf_dir}")

    # Find all PDF files
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]

    if not pdf_files:
        pytest.skip(f"No PDF files found in {pdf_dir}")

    # Parse each PDF and cache the results
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        try:
            cache[pdf_file] = parser.parse_pdf(pdf_path)
        except Exception:
            # If parsing fails for one PDF, continue with others
            # Tests that need the failed PDF will be skipped
            pass

    return cache


def find_first_class(packages: List[AutosarPackage]) -> tuple[AutosarPackage | None, AutosarPackage | None]:
    """Find the first class with actual data in a package hierarchy.

    This is a helper function for tests that need to locate the first
    class in a parsed PDF.

    Args:
        packages: List of AutosarPackage objects to search.

    Returns:
        Tuple of (package, class) or (None, None) if no class is found.
    """
    for pkg in packages:
        # Check M2 top-level package (may not have classes directly)
        if pkg.types:
            return pkg, pkg.types[0]

        # Check subpackages
        for subpkg in pkg.subpackages:
            if subpkg.types:
                return subpkg, subpkg.types[0]

            # Check nested subpackages
            for subsubpkg in subpkg.subpackages:
                if subsubpkg.types:
                    return subsubpkg, subsubpkg.types[0]

    return None, None


def count_classes(packages: List[AutosarPackage]) -> int:
    """Count total classes across all packages recursively.

    Args:
        packages: List of AutosarPackage objects.

    Returns:
        Total number of classes.
    """
    def count(pkg: AutosarPackage) -> int:
        total = len(pkg.types)
        for subpkg in pkg.subpackages:
            total += count(subpkg)
        return total

    return sum(count(pkg) for pkg in packages)
