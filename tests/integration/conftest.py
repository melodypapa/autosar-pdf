"""Pytest configuration and fixtures for integration tests.

This module provides session-scoped fixtures for caching parsed PDF data,
significantly improving integration test performance by avoiding redundant
PDF parsing across multiple tests.

Performance optimizations:
- Session-scoped fixtures prevent redundant PDF parsing
- Pre-computed lookup tables for frequently accessed packages/classes
"""

import os
from typing import List, Optional, Tuple

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
def generic_structure_sw_component_type(generic_structure_template_pdf: AutosarDoc) -> AutosarClass:
    """Cache the SwComponentType class from GenericStructureTemplate PDF.

    This fixture pre-fetches and caches the SwComponentType class,
    avoiding repeated package navigation in tests.

    Args:
        generic_structure_template_pdf: Parsed GenericStructureTemplate PDF data.

    Returns:
        The SwComponentType AutosarClass.

    Skips:
        If SwComponentType class is not found.
    """
    # Find M2 package (root metamodel package)
    m2 = generic_structure_template_pdf.get_package("M2")
    if not m2:
        pytest.skip("M2 package not found")

    # Navigate to AUTOSARTemplates -> SWComponentTemplate -> Components
    autosar_templates = m2.get_subpackage("AUTOSARTemplates")
    if not autosar_templates:
        pytest.skip("AUTOSARTemplates package not found")

    sw_component_template = autosar_templates.get_subpackage("SWComponentTemplate")
    if not sw_component_template:
        pytest.skip("SWComponentTemplate package not found")

    components = sw_component_template.get_subpackage("Components")
    if not components:
        pytest.skip("Components package not found")

    sw_component_type = components.get_class("SwComponentType")
    if not sw_component_type:
        pytest.skip("SwComponentType class not found")

    return sw_component_type


@pytest.fixture(scope="session")
def generic_structure_arelement(generic_structure_template_pdf: AutosarDoc) -> AutosarClass:
    """Cache the ARElement class from GenericStructureTemplate PDF.

    This fixture pre-fetches and caches the ARElement class,
    avoiding repeated package navigation in tests.

    Args:
        generic_structure_template_pdf: Parsed GenericStructureTemplate PDF data.

    Returns:
        The ARElement AutosarClass.

    Skips:
        If ARElement class is not found.
    """
    # Find M2 package (root metamodel package)
    m2 = generic_structure_template_pdf.get_package("M2")
    if not m2:
        pytest.skip("M2 package not found")

    # Navigate to AUTOSARTemplates -> GenericStructure -> GeneralTemplateClasses -> ARPackage
    autosar_templates = m2.get_subpackage("AUTOSARTemplates")
    if not autosar_templates:
        pytest.skip("AUTOSARTemplates package not found")

    generic_structure = autosar_templates.get_subpackage("GenericStructure")
    if not generic_structure:
        pytest.skip("GenericStructure package not found")

    general_template_classes = generic_structure.get_subpackage("GeneralTemplateClasses")
    if not general_template_classes:
        pytest.skip("GeneralTemplateClasses package not found")

    ar_package = general_template_classes.get_subpackage("ARPackage")
    if not ar_package:
        pytest.skip("ARPackage package not found")

    arelement = ar_package.get_class("ARElement")
    if not arelement:
        pytest.skip("ARElement class not found")

    return arelement


@pytest.fixture(scope="session")
def timing_extensions_pdf(parser: PdfParser) -> AutosarDoc:
    """Parse and cache the TimingExtensions PDF.

    This fixture parses the PDF once per session and caches the result.

    Args:
        parser: Shared PdfParser instance.

    Returns:
        AutosarDoc containing parsed packages and root classes.

    Skips:
        If the PDF file is not found.
    """
    pdf_path = "examples/pdf/AUTOSAR_CP_TPS_TimingExtensions.pdf"

    if not os.path.exists(pdf_path):
        pytest.skip(f"PDF file not found: {pdf_path}")

    return parser.parse_pdf(pdf_path)


@pytest.fixture(scope="session")
def bsw_module_description_pdf(parser: PdfParser) -> AutosarDoc:
    """Parse and cache the BSWModuleDescriptionTemplate PDF.

    This fixture parses the PDF once per session and caches the result.

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
def bsw_module_description_atomic_sw_component_type(bsw_module_description_pdf: AutosarDoc) -> AutosarClass:
    """Cache the AtomicSwComponentType class from BSWModuleDescriptionTemplate PDF.

    This fixture pre-fetches and caches the AtomicSwComponentType class,
    avoiding repeated package navigation in tests.

    Args:
        bsw_module_description_pdf: Parsed BSWModuleDescriptionTemplate PDF data.

    Returns:
        The AtomicSwComponentType AutosarClass.

    Skips:
        If AtomicSwComponentType class is not found.
    """
    # Find M2 package (root metamodel package)
    m2 = bsw_module_description_pdf.get_package("M2")
    if not m2:
        pytest.skip("M2 package not found")

    # Navigate to AUTOSARTemplates -> SWComponentTemplate -> Components
    autosar_templates = m2.get_subpackage("AUTOSARTemplates")
    if not autosar_templates:
        pytest.skip("AUTOSARTemplates package not found")

    sw_component_template = autosar_templates.get_subpackage("SWComponentTemplate")
    if not sw_component_template:
        pytest.skip("SWComponentTemplate package not found")

    components = sw_component_template.get_subpackage("Components")
    if not components:
        pytest.skip("Components package not found")

    atomic_sw_component_type = components.get_class("AtomicSwComponentType")
    if not atomic_sw_component_type:
        pytest.skip("AtomicSwComponentType class not found")

    return atomic_sw_component_type


@pytest.fixture(scope="session")
def timing_extensions_atomic_sw_component_type(timing_extensions_pdf: AutosarDoc) -> AutosarClass:
    """Cache the AtomicSwComponentType class from TimingExtensions PDF.

    This fixture pre-fetches and caches the AtomicSwComponentType class,
    avoiding repeated package navigation in tests.

    Args:
        timing_extensions_pdf: Parsed TimingExtensions PDF data.

    Returns:
        The AtomicSwComponentType AutosarClass.

    Skips:
        If AtomicSwComponentType class is not found.
    """
    # Find M2 package (root metamodel package)
    m2 = timing_extensions_pdf.get_package("M2")
    if not m2:
        pytest.skip("M2 package not found")

    # Navigate to AUTOSARTemplates -> SWComponentTemplate -> Components
    autosar_templates = m2.get_subpackage("AUTOSARTemplates")
    if not autosar_templates:
        pytest.skip("AUTOSARTemplates package not found")

    sw_component_template = autosar_templates.get_subpackage("SWComponentTemplate")
    if not sw_component_template:
        pytest.skip("SWComponentTemplate package not found")

    components = sw_component_template.get_subpackage("Components")
    if not components:
        pytest.skip("Components package not found")

    atomic_sw_component_type = components.get_class("AtomicSwComponentType")
    if not atomic_sw_component_type:
        pytest.skip("AtomicSwComponentType class not found")

    return atomic_sw_component_type


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
