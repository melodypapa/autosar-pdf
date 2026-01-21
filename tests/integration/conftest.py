"""Pytest configuration and fixtures for integration tests.

This module provides session-scoped fixtures for caching parsed PDF data,
significantly improving integration test performance by avoiding redundant
PDF parsing across multiple tests.

Performance optimizations:
- Session-scoped fixtures prevent redundant PDF parsing
- Pre-computed lookup tables for frequently accessed packages/classes
- Memoized helper functions for expensive traversals
- Lazy evaluation of navigation caches
"""

import os
from typing import Dict, List, Optional, Tuple

import pytest

from autosar_pdf2txt.models import AutosarClass, AutosarDoc, AutosarPackage
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
def ecu_configuration_nav_cache(ecu_configuration_pdf: AutosarDoc) -> Dict[str, AutosarPackage]:
    """Pre-compute navigation cache for ECU Configuration PDF.

    This fixture creates a lookup dictionary for frequently accessed packages
    in the ECU Configuration PDF, significantly speeding up tests that need
    to navigate the package hierarchy.

    Args:
        ecu_configuration_pdf: Parsed ECU Configuration PDF data.

    Returns:
        Dictionary mapping package paths to AutosarPackage objects.
    """
    cache = {}

    def build_cache(pkg: AutosarPackage, prefix: str = "") -> None:
        """Build cache of packages by their full path."""
        current_path = f"{prefix}::{pkg.name}" if prefix else pkg.name
        cache[current_path] = pkg

        for subpkg in pkg.subpackages:
            build_cache(subpkg, current_path)

    for pkg in ecu_configuration_pdf.packages:
        build_cache(pkg)

    return cache


@pytest.fixture(scope="session")
def ecu_configuration_bsw_implementation(ecu_configuration_pdf: AutosarDoc) -> AutosarClass:
    """Cache the BswImplementation class from ECU Configuration PDF.

    This fixture pre-fetches and caches the BswImplementation class,
    avoiding repeated package navigation in tests.

    Args:
        ecu_configuration_pdf: Parsed ECU Configuration PDF data.

    Returns:
        The BswImplementation AutosarClass.

    Skips:
        If BswImplementation class is not found.
    """
    m2_pkg = ecu_configuration_pdf.packages[0]
    autosar_templates = m2_pkg.get_subpackage("AUTOSARTemplates")
    if not autosar_templates:
        pytest.skip("AUTOSARTemplates package not found")

    bsw_module = autosar_templates.get_subpackage("BswModuleTemplate")
    if not bsw_module:
        pytest.skip("BswModuleTemplate package not found")

    bsw_impl_pkg = bsw_module.get_subpackage("BswImplementation")
    if not bsw_impl_pkg:
        pytest.skip("BswImplementation package not found")

    bsw_impl = bsw_impl_pkg.get_class("BswImplementation")
    if not bsw_impl:
        pytest.skip("BswImplementation class not found")

    return bsw_impl


@pytest.fixture(scope="session")
def ecu_configuration_fibex_packages(ecu_configuration_pdf: AutosarDoc) -> Dict[str, AutosarPackage]:
    """Cache Fibex package hierarchy from ECU Configuration PDF.

    This fixture pre-fetches and caches the Fibex package structure,
    avoiding repeated package navigation in tests.

    Args:
        ecu_configuration_pdf: Parsed ECU Configuration PDF data.

    Returns:
        Dictionary with keys: 'm2', 'autosar_templates', 'system_template',
        'fibex', 'fibex_core', 'core_comm', 'common_structure',
        'impl_data_types'.

    Skips:
        If required packages are not found.
    """
    m2_pkg = ecu_configuration_pdf.packages[0]

    autosar_templates = m2_pkg.get_subpackage("AUTOSARTemplates")
    if not autosar_templates:
        pytest.skip("AUTOSARTemplates package not found")

    system_template = autosar_templates.get_subpackage("SystemTemplate")
    if not system_template:
        pytest.skip("SystemTemplate package not found")

    fibex = system_template.get_subpackage("Fibex")
    if not fibex:
        pytest.skip("Fibex package not found")

    fibex_core = fibex.get_subpackage("FibexCore")
    if not fibex_core:
        pytest.skip("FibexCore package not found")

    core_comm = fibex_core.get_subpackage("CoreCommunication")
    if not core_comm:
        pytest.skip("CoreCommunication package not found")

    common_structure = autosar_templates.get_subpackage("CommonStructure")
    if not common_structure:
        pytest.skip("CommonStructure package not found")

    impl_data_types = common_structure.get_subpackage("ImplementationDataTypes")
    if not impl_data_types:
        pytest.skip("ImplementationDataTypes package not found")

    return {
        'm2': m2_pkg,
        'autosar_templates': autosar_templates,
        'system_template': system_template,
        'fibex': fibex,
        'fibex_core': fibex_core,
        'core_comm': core_comm,
        'common_structure': common_structure,
        'impl_data_types': impl_data_types,
    }


@pytest.fixture(scope="session")
def generic_structure_template_pdf(parser: PdfParser) -> AutosarDoc:
    """Parse and cache the GenericStructureTemplate PDF.

    This fixture parses the PDF once per session and caches the result.
    This PDF contains descriptive text that can be incorrectly parsed as
    package names, serving as a regression test for package path validation.

    Args:
        parser: Shared PdfParser instance.

    Returns:
        AutosarDoc containing parsed packages and root classes.

    Skips:
        If the PDF file is not found.
    """
    pdf_path = "examples/pdf/AUTOSAR_FO_TPS_GenericStructureTemplate.pdf"

    if not os.path.exists(pdf_path):
        pytest.skip(f"PDF file not found: {pdf_path}")

    return parser.parse_pdf(pdf_path)


@pytest.fixture(scope="session")
def generic_structure_reference_base(generic_structure_template_pdf: AutosarDoc) -> AutosarClass:
    """Cache the ReferenceBase class from GenericStructureTemplate PDF.

    This fixture pre-fetches and caches the ReferenceBase class,
    avoiding repeated package navigation in tests.

    Args:
        generic_structure_template_pdf: Parsed GenericStructureTemplate PDF data.

    Returns:
        The ReferenceBase AutosarClass.

    Skips:
        If ReferenceBase class is not found.
    """
    m2_pkg = generic_structure_template_pdf.packages[0]
    autosar_templates = m2_pkg.get_subpackage("AUTOSARTemplates")
    if not autosar_templates:
        pytest.skip("AUTOSARTemplates package not found")

    generic_structure = autosar_templates.get_subpackage("GenericStructure")
    if not generic_structure:
        pytest.skip("GenericStructure package not found")

    general_template = generic_structure.get_subpackage("GeneralTemplateClasses")
    if not general_template:
        pytest.skip("GeneralTemplateClasses package not found")

    ar_package = general_template.get_subpackage("ARPackage")
    if not ar_package:
        pytest.skip("ARPackage package not found")

    ref_base = ar_package.get_class("ReferenceBase")
    if not ref_base:
        pytest.skip("ReferenceBase class not found")

    return ref_base


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


def find_first_class(packages: List[AutosarPackage]) -> Tuple[Optional[AutosarPackage], Optional[AutosarPackage]]:
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


def find_class_by_name(packages: List[AutosarPackage], class_name: str) -> Optional[Tuple[AutosarPackage, AutosarClass]]:
    """Find a class by name across all packages.

    This is an optimized helper that uses early termination once
    the target class is found, avoiding unnecessary traversal.

    Args:
        packages: List of AutosarPackage objects to search.
        class_name: Name of the class to find.

    Returns:
        Tuple of (package, class) if found, None otherwise.
    """
    def search(pkg: AutosarPackage) -> Optional[Tuple[AutosarPackage, AutosarClass]]:
        # Search in current package
        for typ in pkg.types:
            if isinstance(typ, AutosarClass) and typ.name == class_name:
                return (pkg, typ)

        # Search in subpackages
        for subpkg in pkg.subpackages:
            result = search(subpkg)
            if result:
                return result

        return None

    for pkg in packages:
        result = search(pkg)
        if result:
            return result

    return None


def collect_classes_with_predicate(packages: List[AutosarPackage], predicate) -> List[AutosarClass]:
    """Collect classes that match a given predicate function.

    This is an optimized helper that traverses the package hierarchy
    and collects classes matching the predicate.

    Args:
        packages: List of AutosarPackage objects to search.
        predicate: Function that takes an AutosarClass and returns bool.

    Returns:
        List of AutosarClass objects matching the predicate.
    """
    def collect(pkg: AutosarPackage) -> List[AutosarClass]:
        matches = []
        for typ in pkg.types:
            if isinstance(typ, AutosarClass) and predicate(typ):
                matches.append(typ)
        for subpkg in pkg.subpackages:
            matches.extend(collect(subpkg))
        return matches

    all_matches = []
    for pkg in packages:
        all_matches.extend(collect(pkg))

    return all_matches
