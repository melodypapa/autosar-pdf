"""Tests for PdfParser class.

Test coverage for pdf_parser.py targeting PDF parsing functionality.
"""

import pytest
from unittest.mock import patch
from typing import List, Union

from autosar_pdf2txt.models import ATPType, AttributeKind, AutosarClass, AutosarEnumeration, AutosarPrimitive
from autosar_pdf2txt.parser import PdfParser
from autosar_pdf2txt.parser.class_parser import AutosarClassParser
from autosar_pdf2txt.parser.enumeration_parser import AutosarEnumerationParser
from autosar_pdf2txt.parser.primitive_parser import AutosarPrimitiveParser
# ClassDefinition removed - using model objects directly


def _parse_class_text(text: str) -> List[AutosarClass]:
    """Helper function to parse class definitions from text using new specialized parsers.

    This function simulates the old _parse_class_text behavior by using the new
    AutosarClassParser directly.

    Args:
        text: The text to parse.

    Returns:
        List of parsed AutosarClass objects.
    """
    parser = AutosarClassParser()
    lines = text.strip().split("\n")
    classes = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Try to parse a class definition
        class_def = parser.parse_definition(lines, i)
        if class_def:
            # Continue parsing to get base classes, attributes, etc.
            new_i, is_complete = parser.continue_parsing(class_def, lines, i + 1)
            classes.append(class_def)
            i = new_i
        else:
            i += 1

    return classes


def _parse_enumeration_text(text: str) -> List[AutosarEnumeration]:
    """Helper function to parse enumeration definitions from text using new specialized parsers.

    Args:
        text: The text to parse.

    Returns:
        List of parsed AutosarEnumeration objects.
    """
    parser = AutosarEnumerationParser()
    lines = text.strip().split("\n")
    enumerations = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Try to parse an enumeration definition
        enum_def = parser.parse_definition(lines, i)
        if enum_def:
            # Continue parsing to get literals
            new_i, is_complete = parser.continue_parsing(enum_def, lines, i + 1)
            enumerations.append(enum_def)
            i = new_i
        else:
            i += 1

    return enumerations


def _parse_primitive_text(text: str) -> List[AutosarPrimitive]:
    """Helper function to parse primitive definitions from text using new specialized parsers.

    Args:
        text: The text to parse.

    Returns:
        List of parsed AutosarPrimitive objects.
    """
    parser = AutosarPrimitiveParser()
    lines = text.strip().split("\n")
    primitives = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Try to parse a primitive definition
        primitive_def = parser.parse_definition(lines, i)
        if primitive_def:
            # Continue parsing to get attributes
            new_i, is_complete = parser.continue_parsing(primitive_def, lines, i + 1)
            primitives.append(primitive_def)
            i = new_i
        else:
            i += 1

    return primitives


class TestPdfParser:
    """Tests for PdfParser class.

    Requirements:
        SWR_PARSER_00001: PDF Parser Initialization
        SWR_PARSER_00003: PDF File Parsing
        SWR_PARSER_00004: Class Definition Pattern Recognition
        SWR_PARSER_00005: Class Definition Data Model
        SWR_PARSER_00006: Package Hierarchy Building
        SWR_PARSER_00017: AUTOSAR Class Parent Resolution
    """

    def test_init(self) -> None:
        """Test parser initialization.

        SWUT_PARSER_00001: Test Parser Initialization

        Requirements:
            SWR_PARSER_00001: PDF Parser Initialization
        """
        parser = PdfParser()
        assert parser is not None

    def test_extract_class_with_base_classes(self) -> None:
        """Test extracting class with base classes.

        SWUT_PARSER_00002: Test Extracting Class with Base Classes

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class RunnableEntity
        Package M2::AUTOSAR::BswModule
        Base InternalBehavior
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "RunnableEntity"
        assert class_defs[0].bases == ["InternalBehavior"]

    def test_extract_class_with_multiple_base_classes(self) -> None:
        """Test extracting class with multiple base classes.

        SWUT_PARSER_00003: Test Extracting Class with Multiple Base Classes

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class DerivedClass
        Package M2::AUTOSAR
        Base BaseClass1, BaseClass2, BaseClass3
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].bases == ["BaseClass1", "BaseClass2", "BaseClass3"]

    def test_extract_class_with_multiline_base_classes(self) -> None:
        """Test extracting class with multi-line base classes.

        SWUT_PARSER_00021: Test Extracting Class with Multi-Line Base Classes

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00021: Multi-Line Base Class Parsing
        """
        PdfParser()
        text = """
        Class CanTpConfig
        Package M2::AUTOSARTemplates::SystemTemplate::TransportProtocols
        Base ARObject,CollectableElement,FibexElement,Identifiable,MultilanguageReferrable,Packageable
        Element,Referrable,TpConfig
        Note This is a test class.
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        can_tp = class_defs[0]

        # Should include all base classes from both lines
        assert "ARObject" in can_tp.bases
        assert "CollectableElement" in can_tp.bases
        assert "FibexElement" in can_tp.bases
        assert "Identifiable" in can_tp.bases
        assert "MultilanguageReferrable" in can_tp.bases
        assert "PackageableElement" in can_tp.bases  # Combined from Packageable + Element
        assert "Referrable" in can_tp.bases
        assert "TpConfig" in can_tp.bases  # Critical: TpConfig should be in the list

    def test_extract_class_with_note(self) -> None:
        """Test extracting class with note.

        SWUT_PARSER_00004: Test Extracting Class with Note

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class BswInternalBehavior
        Package M2::AUTOSAR::BswModule
        Note Implementation for basic software internal behavior
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "BswInternalBehavior"
        assert class_defs[0].note == "Implementation for basic software internal behavior"

    def test_extract_class_with_base_and_note(self) -> None:
        """Test extracting class with both base classes and note.

        SWUT_PARSER_00005: Test Extracting Class with Base and Note

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class BswInternalBehavior
        Package M2::AUTOSAR::BswModule
        Base InternalBehavior
        Note Implementation for basic software entities
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "BswInternalBehavior"
        assert class_defs[0].bases == ["InternalBehavior"]
        assert class_defs[0].note == "Implementation for basic software entities"

    def test_extract_class_with_multi_line_note(self) -> None:
        """Test extracting class with multi-line note.

        SWUT_PARSER_00050: Test Extracting Class with Multi-Line Note

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class BswImplementation
        Package M2::AUTOSARTemplates::BswModuleTemplate::BswImplementation
        Note Contains the implementation specific information in addition to the generic specification (BswModule
        Description and BswBehavior). It is possible to have several different BswImplementations referring to
        the same BswBehavior.
        Base ARElement
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "BswImplementation"
        # Verify the multi-line note is captured completely
        expected_note = (
            "Contains the implementation specific information in addition to the generic specification "
            "(BswModule Description and BswBehavior). It is possible to have several different "
            "BswImplementations referring to the same BswBehavior."
        )
        assert class_defs[0].note == expected_note, f"Expected '{expected_note}', got '{class_defs[0].note}'"
        # Verify note word count is at least 20 words (ensures multi-line capture)
        assert len(class_defs[0].note.split()) >= 20

    def test_extract_class_without_base_or_note(self) -> None:
        """Test extracting class without base classes or note.

        SWUT_PARSER_00006: Test Extracting Class without Base or Note

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class SimpleClass
        Package M2::AUTOSAR
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "SimpleClass"
        assert class_defs[0].bases == []
        assert class_defs[0].note is None

    def test_extract_class_with_abstract(self) -> None:
        """Test extracting abstract class.

        SWUT_PARSER_00007: Test Extracting Abstract Class

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00005: Class Definition Data Model
        """
        PdfParser()
        text = """
        Class InternalBehavior (abstract)
        Package M2::AUTOSAR
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "InternalBehavior"
        assert class_defs[0].is_abstract is True

    def test_extract_class_with_abstract_prefix(self) -> None:
        """Test extracting class with Abstract prefix as abstract.

        SWUT_PARSER_00008: Test Extracting Class with Abstract Prefix

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00005: Class Definition Data Model
        """
        PdfParser()
        text = """
        Class AbstractRequiredPortPrototype
        Package M2::AUTOSAR::PortPrototype
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "AbstractRequiredPortPrototype"
        assert class_defs[0].is_abstract is True

    def test_extract_class_with_abstract_prefix_explicit_abstract(self) -> None:
        """Test extracting class with Abstract prefix and explicit abstract marker.

        SWUT_PARSER_00009: Test Extracting Class with Abstract Prefix and Explicit Abstract

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00005: Class Definition Data Model
        """
        PdfParser()
        text = """
        Class AbstractProvidedPortPrototype (abstract)
        Package M2::AUTOSAR::PortPrototype
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "AbstractProvidedPortPrototype"
        assert class_defs[0].is_abstract is True

    def test_extract_multiple_abstract_classes(self) -> None:
        """Test extracting multiple abstract classes with different patterns.

        SWUT_PARSER_00010: Test Extracting Multiple Abstract Classes

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00005: Class Definition Data Model
        """
        PdfParser()
        text = """
        Class InternalBehavior (abstract)
        Package M2::AUTOSAR

        Class AbstractRequiredPortPrototype
        Package M2::AUTOSAR::PortPrototype

        Class AbstractProvidedPortPrototype (abstract)
        Package M2::AUTOSAR::PortPrototype

        Class ConcreteClass
        Package M2::AUTOSAR
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 4

        # First class: explicitly marked as abstract
        assert class_defs[0].name == "InternalBehavior"
        assert class_defs[0].is_abstract is True

        # Second class: name ends with "Abstract"
        assert class_defs[1].name == "AbstractRequiredPortPrototype"
        assert class_defs[1].is_abstract is True

        # Third class: both name ends with "Abstract" and explicitly marked
        assert class_defs[2].name == "AbstractProvidedPortPrototype"
        assert class_defs[2].is_abstract is True

        # Fourth class: concrete class
        assert class_defs[3].name == "ConcreteClass"
        assert class_defs[3].is_abstract is False

    def test_extract_class_with_subclasses(self) -> None:
        """Test extracting class with subclasses.

        SWUT_PARSER_00011: Test Extracting Class with Subclasses

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class BaseClass
        Package M2::AUTOSAR
        Subclasses DerivedClass1, DerivedClass2
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "BaseClass"
        assert class_defs[0].subclasses == ["DerivedClass1", "DerivedClass2"]

    def test_extract_multiple_classes(self) -> None:
        """Test extracting multiple classes.

        SWUT_PARSER_00012: Test Extracting Multiple Classes

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
        """
        PdfParser()
        text = """
        Class InternalBehavior (abstract)
        Package M2::AUTOSAR
        Note Base class for all internal behaviors

        Class BswInternalBehavior
        Package M2::AUTOSAR::BswModule
        Base InternalBehavior
        Note Basic software internal behavior implementation
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 2
        assert class_defs[0].name == "InternalBehavior"
        assert class_defs[0].is_abstract is True
        assert class_defs[0].note == "Base class for all internal behaviors"
        assert class_defs[1].name == "BswInternalBehavior"
        assert class_defs[1].bases == ["InternalBehavior"]
        assert class_defs[1].note == "Basic software internal behavior implementation"

    def test_build_packages_with_bases_and_notes(self) -> None:
        """Test building package hierarchy with bases and notes.

        SWUT_PARSER_00013: Test Building Packages with Bases and Notes

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building
        """
        parser = PdfParser()

        class_defs = [
            AutosarClass(
                name="InternalBehavior",
                package="AUTOSAR",
                is_abstract=True,
                note="Base behavior class"
            ),
            AutosarClass(
                name="BswInternalBehavior",
                package="AUTOSAR::BswModule",
                is_abstract=False,
                bases=["InternalBehavior"],
                note="BSW specific behavior"
            )
        ]

        doc = parser._build_package_hierarchy(class_defs)
        packages = doc.packages
        assert len(packages) == 1
        assert packages[0].name == "AUTOSAR"

        # Check InternalBehavior
        internal_behavior = packages[0].get_class("InternalBehavior")
        assert internal_behavior is not None
        assert internal_behavior.is_abstract is True
        assert internal_behavior.bases == []
        assert internal_behavior.note == "Base behavior class"

        # Check BswInternalBehavior
        bsw_subpkg = packages[0].get_subpackage("BswModule")
        assert bsw_subpkg is not None
        bsw_internal = bsw_subpkg.get_class("BswInternalBehavior")
        assert bsw_internal is not None
        assert bsw_internal.bases == ["InternalBehavior"]
        assert bsw_internal.note == "BSW specific behavior"

        # Check root classes
        assert len(doc.root_classes) == 1
        assert doc.root_classes[0].name == "InternalBehavior"

    def test_extract_with_pdfplumber_exception_handling(self, monkeypatch) -> None:
        """Test exception handling in _extract_with_pdfplumber.

        SWUT_PARSER_00014: Test Exception Handling in PDF Extraction

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
        """
        parser = PdfParser()

        # Mock pdfplumber.open to raise an exception
        def mock_open(path, **kwargs):
            raise Exception("Mock PDF read error")

        monkeypatch.setattr("pdfplumber.open", mock_open)

        # Should raise wrapped exception
        with pytest.raises(Exception) as exc_info:
            parser._extract_with_pdfplumber("dummy.pdf")

        assert "Failed to parse PDF with pdfplumber" in str(exc_info.value)
        assert "Mock PDF read error" in str(exc_info.value)

    def test_build_package_handles_duplicate_subpackages(self) -> None:
        """Test that _build_package_hierarchy handles duplicate subpackages gracefully.

        SWUT_PARSER_00015: Test Building Package Handles Duplicate Subpackages

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building
        """
        parser = PdfParser()

        # Create package and subpackage
        doc = parser._build_package_hierarchy([
            AutosarClass(
                name="Class1",
                package="AUTOSAR::Module1",
                is_abstract=False
            )
        ])
        parent_pkg = doc.packages

        # Manually add Module1 subpackage to trigger duplicate
        module1 = parent_pkg[0].get_subpackage("Module1")
        assert module1 is not None

        # Try to add the same subpackage again (should trigger ValueError and pass)
        from autosar_pdf2txt.models import AutosarPackage
        duplicate_module = AutosarPackage(name="Module1")

        # This should trigger ValueError: "Subpackage 'Module1' already exists"
        # and the code should catch it and pass
        try:
            parent_pkg[0].add_subpackage(duplicate_module)
        except ValueError:
            pass  # Expected, but should be caught in _build_package_hierarchy

        # Now test with _build_package_hierarchy creating duplicate structure
        # by having conflicting package paths
        class_defs = [
            AutosarClass(
                name="Class1",
                package="AUTOSAR::Module1",
                is_abstract=False
            ),
            AutosarClass(
                name="Class2",
                package="AUTOSAR::Module1",  # Same path, should trigger duplicate
                is_abstract=False
            ),
            AutosarClass(
                name="Class3",
                package="AUTOSAR::Module2",
                is_abstract=False
            ),
        ]

        # Should not raise ValueError for duplicate subpackages
        doc = parser._build_package_hierarchy(class_defs)
        packages = doc.packages

        # Should successfully create packages
        assert len(packages) == 1
        assert packages[0].name == "AUTOSAR"

        # Should have Module1 and Module2 as subpackages
        module1 = packages[0].get_subpackage("Module1")
        assert module1 is not None
        assert len(module1.types) == 2  # Class1 and Class2

        module2 = packages[0].get_subpackage("Module2")
        assert module2 is not None
        assert len(module2.types) == 1  # Class3

    def test_build_package_handles_duplicate_classes(self) -> None:
        """Test that _build_package_hierarchy handles duplicate classes gracefully.

        SWUT_PARSER_00016: Test Building Package Handles Duplicate Classes

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building
        """
        parser = PdfParser()
        from autosar_pdf2txt.models import AutosarClass

        # Create package with a class
        doc = parser._build_package_hierarchy([
            AutosarClass(
                name="ExistingClass",
                package="AUTOSAR",
                is_abstract=False,
                bases=["Base1"]
            )
        ])
        packages = doc.packages

        # Try to manually add duplicate class (should trigger ValueError)
        duplicate_class = AutosarClass(name="ExistingClass", package="M2::Test",
    is_abstract=False,
            bases=["Base2"]
        )

        try:
            packages[0].add_class(duplicate_class)
        except ValueError:
            pass  # Expected

        # Now test with duplicate class definitions
        class_defs = [
            AutosarClass(
                name="DuplicateClass",
                package="AUTOSAR",
                is_abstract=False,
                bases=["Base1"]
            ),
            AutosarClass(
                name="DuplicateClass",
                package="AUTOSAR",
                is_abstract=False,
                bases=["Base2"]
            ),
        ]

        # Should raise ValueError for duplicate classes
        with pytest.raises(ValueError, match="already exists"):
            parser._build_package_hierarchy(class_defs)

    def test_parse_pdf_with_nonexistent_file(self) -> None:
        """Test parsing a non-existent PDF file.

        SWUT_PARSER_00017: Test Parsing Non-Existent PDF File

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
        """
        parser = PdfParser()

        # Should raise Exception when file doesn't exist
        with pytest.raises(Exception) as exc_info:
            parser.parse_pdf("nonexistent_file.pdf")

        # The error should mention the file or pdfplumber
        error_msg = str(exc_info.value).lower()
        assert "pdf" in error_msg or "failed" in error_msg or "file" in error_msg

    def test_parse_pdf_successful_with_mock(self, monkeypatch) -> None:
        """Test successful PDF parsing with mocked pdfplumber.

        SWUT_PARSER_00018: Test Successful PDF Parsing with Mock

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00006: Package Hierarchy Building
        """
        parser = PdfParser()

        # Mock pdfplumber.open to return test data
        class MockPage:
            def extract_words(self, x_tolerance=1):
                # Return words that simulate proper extraction with spaces
                return [
                    {'text': 'Class', 'top': 0, 'x0': 0, 'x1': 40},
                    {'text': 'TestClass', 'top': 0, 'x0': 45, 'x1': 105},
                    {'text': 'Package', 'top': 20, 'x0': 0, 'x1': 55},
                    {'text': 'AUTOSAR::Module', 'top': 20, 'x0': 60, 'x1': 160},
                ]

        class MockPdf:
            pages = [MockPage()]

        def mock_open(path, **kwargs):
            class MockPdfManager:
                def __enter__(self):
                    return MockPdf()
                def __exit__(self, *args):
                    pass
            return MockPdfManager()

        monkeypatch.setattr("pdfplumber.open", mock_open)

        # Parse the PDF
        doc = parser.parse_pdf("dummy.pdf")
        packages = doc.packages

        # Verify results
        assert len(packages) == 1
        assert packages[0].name == "AUTOSAR"

    def test_build_package_with_empty_parts(self) -> None:
        """Test that empty package parts are skipped.

        SWUT_PARSER_00019: Test Building Package with Empty Parts

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building
        """
        parser = PdfParser()

        # Create class definition with empty parts in package path
        class_defs = [
            AutosarClass(
                name="TestClass",
                package="AUTOSAR::::Module",  # Multiple consecutive colons
                is_abstract=False
            ),
        ]

        # Should raise ValueError for empty package parts
        with pytest.raises(ValueError, match="cannot be empty"):
            parser._build_package_hierarchy(class_defs)

    def test_extract_class_with_atp_variation(self) -> None:
        """Test extracting class with <<atpVariation>> pattern.

        SWUT_PARSER_00020: Test Extracting Class with ATP Variation

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class MyClass <<atpVariation>>
        Package M2::AUTOSAR
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "MyClass"
        assert class_defs[0].atp_type == ATPType.ATP_VARIATION

    def test_extract_class_with_atp_mixed_string(self) -> None:
        """Test extracting class with <<atpMixedString>> pattern.

        SWUT_PARSER_00021: Test Extracting Class with ATP Mixed String

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class MyClass <<atpMixedString>>
        Package M2::AUTOSAR
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "MyClass"
        assert class_defs[0].atp_type == ATPType.ATP_MIXED_STRING

    def test_extract_class_with_atp_mixed(self) -> None:
        """Test extracting class with <<atpMixed>> pattern.

        SWUT_PARSER_00022: Test Extracting Class with ATP Mixed

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class MyClass <<atpMixed>>
        Package M2::AUTOSAR
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "MyClass"
        assert class_defs[0].atp_type == ATPType.ATP_MIXED

    def test_extract_class_with_both_atp_patterns_raises_error(self) -> None:
        """Test extracting class with both ATP patterns raises validation error.

        SWUT_PARSER_00023: Test Extracting Class with Both ATP Patterns Raises Error

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class MyClass <<atpVariation>> <<atpMixedString>>
        Package M2::AUTOSAR
        """
        with pytest.raises(ValueError, match="Multiple ATP markers detected"):
            _parse_class_text(text)

    def test_extract_class_with_atp_patterns_reversed_order_raises_error(self) -> None:
        """Test extracting class with ATP patterns in reverse order raises validation error.

        SWUT_PARSER_00024: Test Extracting Class with ATP Patterns in Reverse Order Raises Error

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class MyClass <<atpMixedString>> <<atpVariation>>
        Package M2::AUTOSAR
        """
        with pytest.raises(ValueError, match="Multiple ATP markers detected"):
            _parse_class_text(text)

    def test_extract_class_with_atp_mixed_and_variation_raises_error(self) -> None:
        """Test extracting class with <<atpMixed>> and <<atpVariation>> raises validation error.

        SWUT_PARSER_00025: Test Extracting Class with ATP Mixed and Variation Raises Error

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class MyClass <<atpMixed>> <<atpVariation>>
        Package M2::AUTOSAR
        """
        with pytest.raises(ValueError, match="Multiple ATP markers detected"):
            _parse_class_text(text)

    def test_extract_class_with_atp_mixed_string_and_mixed_raises_error(self) -> None:
        """Test extracting class with <<atpMixedString>> and <<atpMixed>> raises validation error.

        SWUT_PARSER_00026: Test Extracting Class with ATP Mixed String and Mixed Raises Error

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class MyClass <<atpMixedString>> <<atpMixed>>
        Package M2::AUTOSAR
        """
        with pytest.raises(ValueError, match="Multiple ATP markers detected"):
            _parse_class_text(text)

    def test_extract_class_with_all_three_atp_patterns_raises_error(self) -> None:
        """Test extracting class with all three ATP patterns raises validation error.

        SWUT_PARSER_00027: Test Extracting Class with All Three ATP Patterns Raises Error

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class MyClass <<atpMixed>> <<atpVariation>> <<atpMixedString>>
        Package M2::AUTOSAR
        """
        with pytest.raises(ValueError, match="Multiple ATP markers detected"):
            _parse_class_text(text)

    def test_extract_class_with_atp_and_abstract(self) -> None:
        """Test extracting class with ATP pattern and abstract marker.

        SWUT_PARSER_00028: Test Extracting Class with ATP and Abstract

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class MyClass <<atpVariation>> (abstract)
        Package M2::AUTOSAR
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "MyClass"
        assert class_defs[0].atp_type == ATPType.ATP_VARIATION
        assert class_defs[0].is_abstract is True

    def test_extract_class_without_atp_patterns(self) -> None:
        """Test extracting class without ATP patterns defaults to NONE.

        SWUT_PARSER_00029: Test Extracting Class without ATP Patterns

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class MyClass
        Package M2::AUTOSAR
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "MyClass"
        assert class_defs[0].atp_type == ATPType.NONE

    def test_extract_class_malformed_atp_pattern_ignored(self) -> None:
        """Test that malformed ATP patterns are treated as part of class name.

        SWUT_PARSER_00030: Test Extracting Class with Malformed ATP Pattern

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class MyClass <atpVariation>
        Package M2::AUTOSAR
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        # Malformed pattern (missing >) is kept in name
        assert "<atpVariation>" in class_defs[0].name
        assert class_defs[0].atp_type == ATPType.NONE

    def test_build_packages_with_atp_flags(self) -> None:
        """Test building package hierarchy with ATP flags.

        SWUT_PARSER_00031: Test Building Packages with ATP Flags

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building
        """
        parser = PdfParser()

        class_defs = [
            AutosarClass(
                name="MyClass",
                package="AUTOSAR",
                is_abstract=False,
                atp_type=ATPType.ATP_VARIATION
            )
        ]

        doc = parser._build_package_hierarchy(class_defs)
        packages = doc.packages

        assert len(packages) == 1

        my_class = packages[0].get_class("MyClass")
        assert my_class is not None
        assert my_class.atp_type == ATPType.ATP_VARIATION

    def test_extract_class_with_attributes(self) -> None:
        """Test extracting class with attributes.

        SWUT_PARSER_00032: Test Extracting Class with Attributes

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00010: Attribute Extraction from PDF
            SWR_PARSER_00012: Multi-Line Attribute Handling
            SWR_MODEL_00010: AUTOSAR Attribute Representation
        """
        from autosar_pdf2txt.models import AttributeKind

        PdfParser()
        text = """
        Class BswModuleDescription
        Package M2::AUTOSARTemplates::BswModuleTemplate
        Note Root element for BSW module description
        Attribute Type Mult. Kind Note
        bswModule BswModuleDependency * aggr Describes dependency to another BSW module
        bswDocumentation SwComponent 0..1 aggr Adds documentation to BSW module
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "BswModuleDescription"
        assert len(class_defs[0].attributes) == 2

        # Check first attribute (reference type)
        attr1 = class_defs[0].attributes.get("bswModule")
        assert attr1 is not None
        assert attr1.name == "bswModule"
        assert attr1.type == "BswModuleDependency"
        assert attr1.is_ref is True  # Contains "Ref"
        assert attr1.kind == AttributeKind.AGGR
        assert attr1.multiplicity == "*"

        # Check second attribute (non-reference type)
        attr2 = class_defs[0].attributes.get("bswDocumentation")
        assert attr2 is not None
        assert attr2.name == "bswDocumentation"
        assert attr2.type == "SwComponent"
        assert attr2.is_ref is False  # "SwComponent" is not a reference type
        assert attr2.kind == AttributeKind.AGGR
        assert attr2.multiplicity == "0..1"
        
    def test_extract_class_with_reference_attribute(self) -> None:
        """Test extracting class with reference attribute.

        SWUT_PARSER_00033: Test Extracting Class with Reference Attribute

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00010: Attribute Extraction from PDF
            SWR_PARSER_00012: Multi-Line Attribute Handling
        """
        PdfParser()
        text = """
        Class RunnableEntity
        Package M2::AUTOSAR::BswModule
        Note Runnable entity in BSW
        Attribute Type Mult. Kind Note
        dataReadPort PPortPrototype * aggr Data read port prototype
        invocationTriggerMode ModeDeclarationGroup 0..1 aggr Invocation trigger mode
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "RunnableEntity"
        assert len(class_defs[0].attributes) == 2
        
        # Check reference attribute (contains "Prototype")
        attr1 = class_defs[0].attributes.get("dataReadPort")
        assert attr1 is not None
        assert attr1.name == "dataReadPort"
        assert attr1.type == "PPortPrototype"
        assert attr1.is_ref is True
        
        # Check reference attribute (contains "Group")
        attr2 = class_defs[0].attributes.get("invocationTriggerMode")
        assert attr2 is not None
        assert attr2.name == "invocationTriggerMode"
        assert attr2.type == "ModeDeclarationGroup"
        assert attr2.is_ref is True

    def test_extract_class_with_ref_kind_attribute(self) -> None:
        """Test extracting class with REF kind attributes.

        SWUT_PARSER_00051: Test Extracting Class with REF Kind Attributes

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00010: Attribute Extraction from PDF
            SWR_MODEL_00010: AUTOSAR Attribute Representation
        """
        from autosar_pdf2txt.models import AttributeKind

        PdfParser()
        text = """
        Class BswImplementation
        Package M2::AUTOSARTemplates::BswModuleTemplate::BswImplementation
        Note Contains the implementation specific information
        Attribute Type Mult. Kind Note
        behavior BswInternalBehavior 0..1 ref The behavior of this implementation
        arRelease RevisionLabelString 0..1 attr Version of the AUTOSAR Release
        preconfigured EcucModule * ref Preconfigured modules
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "BswImplementation"
        assert len(class_defs[0].attributes) == 3

        # Check REF kind attribute (behavior)
        attr1 = class_defs[0].attributes.get("behavior")
        assert attr1 is not None
        assert attr1.name == "behavior"
        assert attr1.type == "BswInternalBehavior"
        assert attr1.kind == AttributeKind.REF
        assert attr1.multiplicity == "0..1"

        # Check ATTR kind attribute (arRelease)
        attr2 = class_defs[0].attributes.get("arRelease")
        assert attr2 is not None
        assert attr2.name == "arRelease"
        assert attr2.type == "RevisionLabelString"
        assert attr2.kind == AttributeKind.ATTR
        assert attr2.multiplicity == "0..1"

        # Check REF kind attribute (preconfigured)
        attr3 = class_defs[0].attributes.get("preconfigured")
        assert attr3 is not None
        assert attr3.name == "preconfigured"
        assert attr3.type == "EcucModule"
        assert attr3.kind == AttributeKind.REF
        assert attr3.multiplicity == "*"

    def test_extract_class_with_tags_in_note(self) -> None:
        """Test extracting class with Tags field included in note.

        SWUT_PARSER_00052: Test Extracting Class with Tags in Note

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        PdfParser()
        text = """
        Class BswImplementation
        Package M2::AUTOSARTemplates::BswModuleTemplate::BswImplementation
        Note Contains the implementation specific information
        Tags: atp.recommendedPackage=BswImplementations
        Base ARElement
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "BswImplementation"

        # Verify that Tags field is included in the note
        assert "Tags:" in class_defs[0].note
        assert "atp.recommendedPackage=BswImplementations" in class_defs[0].note
        assert "Contains the implementation specific information" in class_defs[0].note

    def test_extract_class_with_multi_line_attribute_notes(self) -> None:
        """Test extracting class with multi-line attribute notes.

        SWUT_PARSER_00053: Test Extracting Class with Multi-Line Attribute Notes

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00010: Attribute Extraction from PDF
            SWR_MODEL_00010: AUTOSAR Attribute Representation
        """
        PdfParser()
        text = """
        Class BswImplementation
        Package M2::AUTOSARTemplates::BswModuleTemplate::BswImplementation
        Note Contains the implementation specific information
        Attribute Type Mult. Kind Note
        arRelease RevisionLabelString 0..1 attr Version of the AUTOSAR Release on which this
        Version implementation is based. The numbering contains three
        levels (major, minor, revision) which are defined by
        AUTOSAR.
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "BswImplementation"

        # Verify arRelease attribute has multi-line note
        attr = class_defs[0].attributes.get("arRelease")
        assert attr is not None
        assert attr.name == "arRelease"
        assert attr.type == "RevisionLabelString"
        assert attr.multiplicity == "0..1"
        assert attr.kind.value == "attr"
        # Verify the note contains text from multiple lines
        assert "Version of the AUTOSAR Release" in attr.note
        assert "The numbering contains three" in attr.note
        assert "AUTOSAR" in attr.note
        # Verify note length (should be longer than single-line note)
        assert len(attr.note) > 100, f"Expected note longer than 100 chars, got {len(attr.note)}"
        assert len(attr.note.split()) > 15, f"Expected more than 15 words, got {len(attr.note.split())}"

    def test_build_packages_with_attributes(self) -> None:
        """Test that attributes are transferred to AutosarClass objects.

        SWUT_PARSER_00034: Test Building Packages with Attributes

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building
            SWR_PARSER_00010: Attribute Extraction from PDF
            SWR_PARSER_00012: Multi-Line Attribute Handling
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        parser = PdfParser()
        from autosar_pdf2txt.models import AutosarAttribute

        class_defs = [
            AutosarClass(
                name="MyClass",
                package="AUTOSAR",
                is_abstract=False,
                attributes={
                    "attr1": AutosarAttribute("attr1", "String", False, multiplicity="1", kind=AttributeKind.ATTR, note=""),
                    "attr2": AutosarAttribute("attr2", "PPortPrototype", True, multiplicity="1", kind=AttributeKind.ATTR, note="")
                }
            )
        ]

        doc = parser._build_package_hierarchy(class_defs)
        packages = doc.packages
        assert len(packages) == 1

        my_class = packages[0].get_class("MyClass")
        assert my_class is not None
        assert len(my_class.attributes) == 2
        assert "attr1" in my_class.attributes
        assert "attr2" in my_class.attributes
        assert my_class.attributes["attr1"].is_ref is False
        assert my_class.attributes["attr2"].is_ref is True

    def test_extract_class_ignores_metadata_as_attributes(self) -> None:
        """Test that metadata lines are not incorrectly parsed as attributes.

        SWUT_PARSER_00035: Test Metadata Filtering in Attribute Extraction

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00010: Attribute Extraction from PDF
            SWR_PARSER_00011: Metadata Filtering in Attribute Extraction

        This test verifies that lines like "Stereotypes: : atpSplitable;",
        "287 : of", "Specification : of", "AUTOSAR : CP" are NOT
        parsed as attributes, as they are metadata or formatting information.
        """
        PdfParser()
        text = """
        Class AUTOSAR
        Package M2::AUTOSARTemplates::AutosarTopLevelStructure
        Base ARObject
        Note Root element of an AUTOSAR description
        Attribute Type Mult. Kind Note
        adminData AdminData * aggr Administrative data
        arPackage ARPackage * aggr AR package
        fileInfo FileInfoComment 0..1 aggr File information
        Comment Comment 0..1 aggr Comment
        Stereotypes: : atpSplitable;
        287 : of
        Specification : of
        AUTOSAR : CP
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "AUTOSAR"

        # Should only have 4 valid attributes, not 8
        assert len(class_defs[0].attributes) == 4, \
            f"Expected 4 attributes, got {len(class_defs[0].attributes)}: {list(class_defs[0].attributes.keys())}"

        # Verify only valid attributes are present
        assert "adminData" in class_defs[0].attributes
        assert "arPackage" in class_defs[0].attributes
        assert "fileInfo" in class_defs[0].attributes
        assert "Comment" in class_defs[0].attributes

        # Verify metadata lines are NOT parsed as attributes
        assert "Stereotypes" not in class_defs[0].attributes
        assert "287" not in class_defs[0].attributes
        assert "Specification" not in class_defs[0].attributes
        assert "AUTOSAR" not in class_defs[0].attributes

    def test_extract_class_filters_broken_attribute_fragments(self) -> None:
        """Test that broken attribute fragments from multi-line PDF tables are filtered out.

        SWUT_PARSER_00036: Test Multi-Line Attribute Handling

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00010: Attribute Extraction from PDF
            SWR_PARSER_00012: Multi-Line Attribute Handling

        This test verifies that broken attribute fragments like "SizeProfile", "Element",
        "ImplementationDataType", "intention", "isStructWith" are filtered out
        as they are continuation words or partial attribute names from multi-line PDF table formatting.
        However, attributes with proper type information (like "dynamicArray String") are kept.
        """
        PdfParser()
        text = """
        Class ImplementationDataType
        Package M2::AUTOSARTemplates::CommonStructure::ImplementationDataTypes
        Note Describes a reusable data type on the implementation level
        Attribute Type Mult. Kind Note
        dynamicArray String * aggr
        SizeProfile data 0..1 aggr
        isStructWith Boolean 0..1 aggr
        Element If * aggr
        ImplementationDataType has * aggr
        intention to * aggr
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "ImplementationDataType"

        # Verify that dynamicArray is kept (has proper type "String")
        assert "dynamicArray" in class_defs[0].attributes
        assert class_defs[0].attributes["dynamicArray"].type == "String"

        # Verify that broken fragments are filtered out
        assert "SizeProfile" not in class_defs[0].attributes
        assert "isStructWith" not in class_defs[0].attributes
        assert "Element" not in class_defs[0].attributes
        assert "ImplementationDataType" not in class_defs[0].attributes
        assert "intention" not in class_defs[0].attributes

        # Verify that only 1 attribute remains (dynamicArray)
        assert len(class_defs[0].attributes) == 1

    def test_extract_primitive_class_definition(self) -> None:
        """Test that the parser correctly recognizes class definitions with 'Primitive' prefix.

        SWUT_PARSER_00037: Test Recognition of Primitive Class Definition Pattern

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00013: Recognition of Primitive and Enumeration Class Definition Patterns

        This test verifies that 'Primitive <classname>' definitions are recognized
        as valid class definitions and that attributes are correctly assigned.
        """
        PdfParser()
        text = """
        Primitive Limit
        Package M2::AUTOSARTTemplates::GenericStructure::GeneralTemplateClasses::PrimitiveTypes
        Note This class represents the ability to express a numerical limit
        Attribute Type Mult. Kind Note
        intervalType IntervalTypeEnum 0..1 attr Specifies the type of the interval
        """
        class_defs = _parse_primitive_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].package == "M2::AUTOSARTTemplates::GenericStructure::GeneralTemplateClasses::PrimitiveTypes"
        assert class_defs[0].attributes["intervalType"].type == "IntervalTypeEnum"

    def test_extract_enumeration_class_definition(self) -> None:
        """Test that the parser correctly recognizes class definitions with 'Enumeration' prefix.

        SWUT_PARSER_00038: Test Recognition of Enumeration Class Definition Pattern

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00013: Recognition of Primitive and Enumeration Class Definition Patterns

        This test verifies that 'Enumeration <classname>' definitions are recognized
        as valid class definitions.
        """
        PdfParser()
        text = """
        Enumeration IntervalTypeEnum
        Package M2::AUTOSARTTemplates::GenericStructure::GeneralTemplateClasses::PrimitiveTypes
        Note This enumerator specifies the type of an interval
        Attribute Type Mult. Kind Note
        """
        class_defs = _parse_enumeration_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "IntervalTypeEnum"

    def test_prevent_attribute_bleed_between_class_types(self) -> None:
        """Test that attributes don't bleed between classes with different definition patterns.

        SWUT_PARSER_00039: Test Prevention of Attribute Bleed Between Class Definitions

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00010: Attribute Extraction from PDF
            SWR_PARSER_00013: Recognition of Primitive and Enumeration Class Definition Patterns

        This test verifies that when Class, Primitive, and Enumeration definitions appear
        sequentially, each class receives only its own attributes.
        """
        PdfParser()
        text = """
        Class ImplementationDataType
        Package M2::AUTOSARTTemplates::CommonStructure::ImplementationDataTypes
        Attribute Type Mult. Kind Note
        dynamicArray String 0..1 attr Specifies the profile
        typeEmitter NameToken 0..1 attr Controls the toolchain

        Primitive Limit
        Package M2::AUTOSARTTemplates::GenericStructure::GeneralTemplateClasses::PrimitiveTypes
        Attribute Type Mult. Kind Note
        intervalType IntervalTypeEnum 0..1 attr Specifies the interval type

        Enumeration IntervalTypeEnum
        Package M2::AUTOSARTemplates::GenericStructure::GeneralTemplateClasses::PrimitiveTypes
        """
        class_defs = _parse_all_types(text)
        assert len(class_defs) == 3

        # Find each class
        impl_data_type = next((c for c in class_defs if c.name == "ImplementationDataType"), None)
        limit = next((c for c in class_defs if c.name == "Limit"), None)
        interval_enum = next((c for c in class_defs if c.name == "IntervalTypeEnum"), None)

        # Verify ImplementationDataType has only its attributes
        assert impl_data_type is not None
        assert "dynamicArray" in impl_data_type.attributes
        assert "typeEmitter" in impl_data_type.attributes
        assert "intervalType" not in impl_data_type.attributes  # NOT from Limit class

        # Verify Limit has only its attributes
        assert limit is not None
        assert "intervalType" in limit.attributes
        assert "dynamicArray" not in limit.attributes  # NOT from ImplementationDataType

        # Verify IntervalTypeEnum exists
        assert interval_enum is not None

    def test_extract_enumeration_with_literals(self) -> None:
        """Test extracting enumeration with enumeration literals.

        SWUT_PARSER_00040: Test Extracting Enumeration with Enumeration Literals

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00013: Recognition of Primitive and Enumeration Class Definition Patterns
            SWR_PARSER_00014: Enumeration Literal Header Recognition
            SWR_PARSER_00015: Enumeration Literal Extraction from PDF
            SWR_PARSER_00016: Enumeration Literal Section Termination
            SWR_MODEL_00019: AUTOSAR Enumeration Type Representation
        """
        PdfParser()
        text = """
        Enumeration EcucDestinationUriNestingContractEnum
        Package M2::AUTOSAR::DataTypes
        Note This enumerator specifies the type of an interval
        Literal Description
        leafOfTargetContainer EcucDestinationUriPolicy describes elements directly owned by the target container
        targetContainer EcucDestinationUriPolicy describes the target container of EcucUriReferenceDef
        vertexOfTargetContainer EcucDestinationUriPolicy describes elements of the target container
        """
        class_defs = _parse_enumeration_text(text)
        assert len(class_defs) == 1

        enum_def = class_defs[0]
        assert enum_def.name == "EcucDestinationUriNestingContractEnum"
        assert len(enum_def.enumeration_literals) == 3

        # Check first literal
        literal1 = enum_def.enumeration_literals[0]
        assert literal1.name == "leafOfTargetContainer"
        assert "EcucDestinationUriPolicy describes elements directly owned" in literal1.description

        # Check second literal
        literal2 = enum_def.enumeration_literals[1]
        assert literal2.name == "targetContainer"
        assert "EcucDestinationUriPolicy describes the target container" in literal2.description

        # Check third literal
        literal3 = enum_def.enumeration_literals[2]
        assert literal3.name == "vertexOfTargetContainer"
        assert "EcucDestinationUriPolicy describes elements of the target container" in literal3.description

    def test_extract_enumeration_literal_with_index(self) -> None:
        """Test extracting enumeration literal with index.

        SWUT_PARSER_00041: Test Extracting Enumeration Literal with Index

        Requirements:
            SWR_PARSER_00014: Enumeration Literal Header Recognition
            SWR_PARSER_00015: Enumeration Literal Extraction from PDF
        """
        PdfParser()
        text = """
        Enumeration TestEnum
        Package M2::AUTOSAR::DataTypes
        Literal Description
        VALUE1 First value atp.EnumerationLiteralIndex=0
        VALUE2 Second value atp.EnumerationLiteralIndex=1
        VALUE3 Third value atp.EnumerationLiteralIndex=2
        """
        class_defs = _parse_enumeration_text(text)
        assert len(class_defs) == 1

        enum_def = class_defs[0]
        assert len(enum_def.enumeration_literals) == 3

        # Check indices are extracted correctly
        assert enum_def.enumeration_literals[0].index == 0
        assert enum_def.enumeration_literals[0].description == "First value"

        assert enum_def.enumeration_literals[1].index == 1
        assert enum_def.enumeration_literals[1].name == "VALUE2"
        assert enum_def.enumeration_literals[1].description == "Second value"

        assert enum_def.enumeration_literals[2].index == 2
        assert enum_def.enumeration_literals[2].name == "VALUE3"
        assert enum_def.enumeration_literals[2].description == "Third value"

    def test_enumeration_literal_section_termination(self) -> None:
        """Test that enumeration literal section terminates on new class definition.

        SWUT_PARSER_00042: Test Enumeration Literal Section Termination

        Requirements:
            SWR_PARSER_00014: Enumeration Literal Header Recognition
            SWR_PARSER_00015: Enumeration Literal Extraction from PDF
            SWR_PARSER_00016: Enumeration Literal Section Termination
        """
        PdfParser()
        text = """
        Enumeration FirstEnum
        Package M2::AUTOSAR::DataTypes
        Literal Description
        VALUE1 First value
        VALUE2 Second value

        Class SecondClass
        Package M2::AUTOSAR::Other
        """
        # Parse both enumerations and classes
        enum_defs = _parse_enumeration_text(text)
        class_defs = _parse_class_text(text)
        assert len(enum_defs) == 1
        assert len(class_defs) == 1

        # First definition should be enumeration with 2 literals
        enum_def = enum_defs[0]
        assert enum_def.name == "FirstEnum"
        assert len(enum_def.enumeration_literals) == 2

        # Second definition should be class
        class_def = class_defs[0]
        assert class_def.name == "SecondClass"

    def test_enumeration_literal_section_termination_on_table(self) -> None:
        """Test that enumeration literal section terminates on table header.

        SWUT_PARSER_00043: Test Enumeration Literal Section Termination on Table Header

        Requirements:
            SWR_PARSER_00014: Enumeration Literal Header Recognition
            SWR_PARSER_00015: Enumeration Literal Extraction from PDF
            SWR_PARSER_00016: Enumeration Literal Section Termination
        """
        PdfParser()
        text = """
        Enumeration TestEnum
        Package M2::AUTOSAR::DataTypes
        Literal Description
        VALUE1 First value
        VALUE2 Second value
        Table F.18: Test Table
        """
        class_defs = _parse_enumeration_text(text)
        assert len(class_defs) == 1

        enum_def = class_defs[0]
        assert len(enum_def.enumeration_literals) == 2

        # Should only have 2 literals (the table header should stop the enumeration literal section)
        assert enum_def.enumeration_literals[0].name == "VALUE1"
        assert enum_def.enumeration_literals[1].name == "VALUE2"

    def test_build_package_creates_enumeration_object(self) -> None:
        """Test that _build_package_hierarchy creates AutosarEnumeration for enumeration types.

        SWUT_PARSER_00044: Test Building Package Creates Enumeration Object

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building
            SWR_PARSER_00013: Recognition of Primitive and Enumeration Class Definition Patterns
            SWR_MODEL_00019: AUTOSAR Enumeration Type Representation
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        parser = PdfParser()
        from autosar_pdf2txt.models import AutosarEnumLiteral, AutosarEnumeration

        class_defs = [
            AutosarEnumeration(
                name="MyEnum",
                package="AUTOSAR::DataTypes",
                enumeration_literals=[
                    AutosarEnumLiteral("VALUE1", 0, "First value"),
                    AutosarEnumLiteral("VALUE2", 1, "Second value")
                ]
            )
        ]

        doc = parser._build_package_hierarchy(class_defs)
        packages = doc.packages
        assert len(packages) == 1

        # Check that the package contains an AutosarEnumeration, not an AutosarClass
        pkg = packages[0]
        assert pkg.name == "AUTOSAR"

        data_types_pkg = pkg.get_subpackage("DataTypes")
        assert data_types_pkg is not None

        # Verify it's an enumeration
        enum = data_types_pkg.get_enumeration("MyEnum")
        assert enum is not None
        assert isinstance(enum, AutosarEnumeration)
        assert enum.name == "MyEnum"
        assert len(enum.enumeration_literals) == 2
        assert enum.enumeration_literals[0].name == "VALUE1"
        assert enum.enumeration_literals[0].index == 0
        assert enum.enumeration_literals[1].name == "VALUE2"
        assert enum.enumeration_literals[1].index == 1

    def test_build_package_mixed_classes_and_enumerations(self) -> None:
        """Test that _build_package_hierarchy handles both classes and enumerations.

        SWUT_PARSER_00045: Test Building Package with Mixed Classes and Enumerations

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building
            SWR_MODEL_00019: AUTOSAR Enumeration Type Representation
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        parser = PdfParser()
        from autosar_pdf2txt.models import AutosarClass, AutosarEnumeration

        class_defs = [
            AutosarClass(
                name="MyClass",
                package="AUTOSAR::DataTypes",
                is_abstract=False
            ),
            AutosarEnumeration(
                name="MyEnum",
                package="AUTOSAR::DataTypes",
                enumeration_literals=[]
            )
        ]

        doc = parser._build_package_hierarchy(class_defs)
        packages = doc.packages
        assert len(packages) == 1

        pkg = packages[0]
        data_types_pkg = pkg.get_subpackage("DataTypes")
        assert data_types_pkg is not None

        # Check that both class and enumeration are in the types list
        assert len(data_types_pkg.types) == 2

        # Verify first is a class
        assert isinstance(data_types_pkg.types[0], AutosarClass)
        assert data_types_pkg.types[0].name == "MyClass"

        # Verify second is an enumeration
        assert isinstance(data_types_pkg.types[1], AutosarEnumeration)
        assert data_types_pkg.types[1].name == "MyEnum"

    def test_parent_resolution_sets_parent_reference(self) -> None:
        """Test that parent references are correctly resolved after building packages.

        SWUT_PARSER_00046: Test Parent Resolution Sets Parent Reference

        Requirements:
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution
        """
        parser = PdfParser()

        class_defs = [
            AutosarClass(
                name="BaseClass",
                package="AUTOSAR::Base",
                is_abstract=False,
                bases=[]
            ),
            AutosarClass(
                name="DerivedClass",
                package="AUTOSAR::Derived",
                is_abstract=False,
                bases=["BaseClass"]
            ),
        ]

        doc = parser._build_package_hierarchy(class_defs)
        packages = doc.packages
        assert len(packages) == 1

        pkg = packages[0]

        # Get both classes
        base_pkg = pkg.get_subpackage("Base")
        derived_pkg = pkg.get_subpackage("Derived")
        assert base_pkg is not None
        assert derived_pkg is not None

        base_class = base_pkg.get_class("BaseClass")
        derived_class = derived_pkg.get_class("DerivedClass")
        assert base_class is not None
        assert derived_class is not None

        # Verify parent reference is set correctly
        assert derived_class.parent == "BaseClass"

        # Verify base class has no parent
        assert base_class.parent is None

    def test_parent_resolution_with_multiple_bases_uses_most_specific(self) -> None:
        """Test that parent reference uses the most specific base class when there are multiple.

        SWUT_PARSER_00047: Test Parent Resolution with Multiple Bases Uses Most Specific

        Requirements:
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution
        """
        parser = PdfParser()

        class_defs = [
            AutosarClass(
                name="Base1",
                package="AUTOSAR::Base",
                is_abstract=False,
                bases=[]
            ),
            AutosarClass(
                name="Base2",
                package="AUTOSAR::Base",
                is_abstract=False,
                bases=[]
            ),
            AutosarClass(
                name="DerivedClass",
                package="AUTOSAR::Derived",
                is_abstract=False,
                bases=["Base1", "Base2"]
            ),
        ]

        doc = parser._build_package_hierarchy(class_defs)
        packages = doc.packages
        assert len(packages) == 1

        pkg = packages[0]
        derived_pkg = pkg.get_subpackage("Derived")

        derived = derived_pkg.get_class("DerivedClass")

        # Verify parent is set to the last (most specific) base class
        assert derived.parent == "Base2"

    def test_parent_resolution_missing_base_leaves_parent_none(self) -> None:
        """Test that parent reference remains None when base class is not found.

        SWUT_PARSER_00048: Test Parent Resolution Missing Base Leaves Parent None

        Requirements:
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution

        Note:
            When base classes cannot be located in the model, warnings are logged:
            - "Class 'X' in package 'Y' has base classes that could not be located..."
            - "Class 'Z' referenced in base classes could not be located during ancestry traversal..."
        """
        parser = PdfParser()

        class_defs = [
            AutosarClass(
                name="DerivedClass",
                package="AUTOSAR::Derived",
                is_abstract=False,
                bases=["NonExistentBase"]
            ),
        ]

        doc = parser._build_package_hierarchy(class_defs)
        packages = doc.packages
        assert len(packages) == 1

        pkg = packages[0]
        derived_pkg = pkg.get_subpackage("Derived")
        derived = derived_pkg.get_class("DerivedClass")

        # Parent should remain None when base is not found
        assert derived.parent is None
        assert derived.bases == ["NonExistentBase"]

    def test_parent_resolution_filters_out_arobject(self) -> None:
        """Test that ARObject is filtered out when selecting parent reference.

        SWUT_PARSER_00050: Test Parent Resolution Filters Out ARObject

        Requirements:
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution
        """
        parser = PdfParser()

        class_defs = [
            AutosarClass(
                name="ARObject",
                package="AUTOSAR::Base",
                is_abstract=True,
                bases=[]
            ),
            AutosarClass(
                name="ARElement",
                package="AUTOSAR::Base",
                is_abstract=True,
                bases=["ARObject"]
            ),
            AutosarClass(
                name="FibexElement",
                package="AUTOSAR::Fibex",
                is_abstract=True,
                bases=["ARObject"]
            ),
            AutosarClass(
                name="CommunicationCluster",
                package="AUTOSAR::Fibex::Core",
                is_abstract=True,
                bases=["ARElement", "ARObject", "FibexElement"]
            ),
        ]

        doc = parser._build_package_hierarchy(class_defs)
        packages = doc.packages
        assert len(packages) == 1

        pkg = packages[0]
        fibex_pkg = pkg.get_subpackage("Fibex")
        core_pkg = fibex_pkg.get_subpackage("Core")

        comm_cluster = core_pkg.get_class("CommunicationCluster")

        # Verify parent is FibexElement (most specific domain-relevant), not ARElement or ARObject
        assert comm_cluster.parent == "FibexElement"
        # Verify all bases are preserved
        assert comm_cluster.bases == ["ARElement", "ARObject", "FibexElement"]

        # Verify root classes - only ARObject should be a root class
        base_pkg = pkg.get_subpackage("Base")
        ar_object = base_pkg.get_class("ARObject")
        ar_element = base_pkg.get_class("ARElement")
        fibex_element = fibex_pkg.get_class("FibexElement")

        # ARObject has no bases and no parent (it's the true root)
        assert ar_object.parent is None
        assert ar_object.bases == []

        # Classes with only ARObject as base have ARObject as parent
        assert ar_element.parent == "ARObject"
        assert fibex_element.parent == "ARObject"

        # Verify only ARObject is in root_classes
        assert len(doc.root_classes) == 1
        assert doc.root_classes[0].name == "ARObject"

        # Verify ARObject's children list includes these classes
        assert ar_element.name in ar_object.children
        assert fibex_element.name in ar_object.children

    def test_parent_resolution_enumerations_not_affected(self) -> None:
        """Test that enumerations are not used as parent references.

        SWUT_PARSER_00049: Test Parent Resolution Enumerations Not Affected

        Requirements:
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution
        """
        parser = PdfParser()

        class_defs = [
            AutosarEnumeration(
                name="MyEnum",
                package="AUTOSAR::Enums",
                enumeration_literals=[]
            ),
            AutosarClass(
                name="MyClass",
                package="AUTOSAR::Classes",
                is_abstract=False,
                bases=["MyEnum"]
            ),
        ]

        doc = parser._build_package_hierarchy(class_defs)
        packages = doc.packages
        assert len(packages) == 1

        pkg = packages[0]
        classes_pkg = pkg.get_subpackage("Classes")
        my_class = classes_pkg.get_class("MyClass")

        # Parent should remain None because MyEnum is an enumeration, not a class
        assert my_class.parent is None

    def test_parse_multiple_pdfs_resolves_parents_across_pdfs(self) -> None:
        """Test that parse_pdfs() resolves parent/children relationships across multiple PDFs.

        SWUT_PARSER_00051: Test Parse Multiple PDFs Resolves Parents Across PDFs

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution

        This test verifies that when parsing multiple PDFs:
        1. All class definitions from all PDFs are extracted first
        2. Parent/children resolution happens once on the complete model
        3. Parent classes are found even if defined in later PDFs
        """
        parser = PdfParser()

        # Simulate first PDF with a child class
        pdf1_classes = [
            AutosarClass(
                name="ParentClass",
                package="AUTOSAR::Base",
                is_abstract=True,
                bases=[]
            ),
            AutosarClass(
                name="ChildClass",
                package="AUTOSAR::Derived",
                is_abstract=False,
                bases=["ParentClass"]
            ),
        ]

        # Simulate second PDF with another child class
        pdf2_classes = [
            AutosarClass(
                name="AnotherChildClass",
                package="AUTOSAR::Derived",
                is_abstract=False,
                bases=["ParentClass"]
            ),
        ]

        # Mock the _extract_models method to return different classes for each PDF
        with patch.object(parser, '_extract_models') as mock_extract:
            # First call returns pdf1_classes, second call returns pdf2_classes
            mock_extract.side_effect = [pdf1_classes, pdf2_classes]

            # Call parse_pdfs with two PDF paths
            doc = parser.parse_pdfs(["pdf1.pdf", "pdf2.pdf"])

            # Verify parent/children were resolved correctly
            assert len(doc.packages) == 1
            pkg = doc.packages[0]

            # Check ParentClass
            base_pkg = pkg.get_subpackage("Base")
            parent_class = base_pkg.get_class("ParentClass")
            assert parent_class is not None
            assert parent_class.parent is None  # Root class

            # Check that both children reference the parent correctly
            assert set(parent_class.children) == {"ChildClass", "AnotherChildClass"}

            # Check ChildClass
            derived_pkg = pkg.get_subpackage("Derived")
            child_class = derived_pkg.get_class("ChildClass")
            assert child_class is not None
            assert child_class.parent == "ParentClass"

            # Check AnotherChildClass
            another_child_class = derived_pkg.get_class("AnotherChildClass")
            assert another_child_class is not None
            assert another_child_class.parent == "ParentClass"

            # Verify _extract_models was called twice (once per PDF)
            assert mock_extract.call_count == 2

    def test_parent_resolution_ancestry_based_filters_ancestors_from_bases(self) -> None:
        """Test that ancestry-based parent selection correctly identifies direct parent vs ancestors.

        SWUT_PARSER_00052: Test Parent Resolution Ancestry Based Filters Ancestors From Bases

        Requirements:
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution

        This test verifies the ancestry-based parent selection algorithm from SWR_PARSER_00017:
        - Given a hierarchy where ClassB inherits from ClassA, and ClassC is a sibling of ClassA
        - When ClassD has bases [ClassA, ClassB, ClassC]
        - Then ClassD.parent should be "ClassC" (the direct parent, not an ancestor)
        - Because ClassB is an ancestor (child of ClassA) and ClassA is an ancestor (parent of ClassB)
        """
        parser = PdfParser()

        class_defs = [
            AutosarClass(
                name="ARObject",
                package="AUTOSAR::Base",
                is_abstract=True,
                bases=[]
            ),
            AutosarClass(
                name="ClassA",
                package="AUTOSAR::Base",
                is_abstract=False,
                bases=["ARObject"]
            ),
            AutosarClass(
                name="ClassB",
                package="AUTOSAR::Base",
                is_abstract=False,
                bases=["ClassA"]
            ),
            AutosarClass(
                name="ClassC",
                package="AUTOSAR::Base",
                is_abstract=False,
                bases=["ARObject"]
            ),
            AutosarClass(
                name="ClassD",
                package="AUTOSAR::Derived",
                is_abstract=False,
                bases=["ClassA", "ClassB", "ClassC"]
            ),
        ]

        doc = parser._build_package_hierarchy(class_defs)
        packages = doc.packages
        assert len(packages) == 1

        pkg = packages[0]
        derived_pkg = pkg.get_subpackage("Derived")

        class_d = derived_pkg.get_class("ClassD")

        # Verify parent is ClassC (direct parent), not ClassA or ClassB (ancestors)
        assert class_d.parent == "ClassC"
        # Verify all bases are preserved
        assert class_d.bases == ["ClassA", "ClassB", "ClassC"]

    def test_parent_resolution_ancestry_based_deep_hierarchy(self) -> None:
        """Test that ancestry-based parent selection works with deep inheritance hierarchies.

        SWUT_PARSER_00053: Test Parent Resolution Ancestry Based Deep Hierarchy

        Requirements:
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution

        This test verifies the ancestry-based parent selection algorithm with deep hierarchies:
        - Given a 4-level hierarchy: ARObject → Level1 → Level2 → Level3 → Level4
        - When DerivedWithMultipleBases has bases [Level1, Level2, Level3, Level4]
        - Then parent should be "Level4" (the most recent/direct parent)
        - Because Level1, Level2, Level3 are all ancestors of Level4
        """
        parser = PdfParser()

        class_defs = [
            AutosarClass(
                name="ARObject",
                package="AUTOSAR::Base",
                is_abstract=True,
                bases=[]
            ),
            AutosarClass(
                name="Level1",
                package="AUTOSAR::Base",
                is_abstract=False,
                bases=["ARObject"]
            ),
            AutosarClass(
                name="Level2",
                package="AUTOSAR::Base",
                is_abstract=False,
                bases=["Level1"]
            ),
            AutosarClass(
                name="Level3",
                package="AUTOSAR::Base",
                is_abstract=False,
                bases=["Level2"]
            ),
            AutosarClass(
                name="Level4",
                package="AUTOSAR::Base",
                is_abstract=False,
                bases=["Level3"]
            ),
            AutosarClass(
                name="DerivedWithMultipleBases",
                package="AUTOSAR::Derived",
                is_abstract=False,
                bases=["Level1", "Level2", "Level3", "Level4"]
            ),
        ]

        doc = parser._build_package_hierarchy(class_defs)
        packages = doc.packages
        assert len(packages) == 1

        pkg = packages[0]
        derived_pkg = pkg.get_subpackage("Derived")

        derived = derived_pkg.get_class("DerivedWithMultipleBases")

        # Verify parent is Level4 (most recent/direct parent)
        assert derived.parent == "Level4"
        # Verify all bases are preserved
        assert derived.bases == ["Level1", "Level2", "Level3", "Level4"]

    def test_parent_resolution_ancestry_based_missing_base_filtered(self) -> None:
        """Test that ancestry-based parent selection filters out missing base classes.

        SWUT_PARSER_00054: Test Parent Resolution Ancestry Based Missing Base Filtered

        Requirements:
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution

        This test verifies strict validation in ancestry-based parent selection:
        - Given a class with bases [ExistingClass, NonExistentBase]
        - When NonExistentBase doesn't exist in the model
        - Then parent should be "ExistingClass" (the only valid base)

        Note:
            A warning is logged for the missing base class:
            "Class 'DerivedClass' in package 'Derived' has base classes that could
            not be located in the model: ['NonExistentBase']. Parent resolution may
            be incomplete."
        """
        parser = PdfParser()

        class_defs = [
            AutosarClass(
                name="ExistingClass",
                package="AUTOSAR::Base",
                is_abstract=False,
                bases=["ARObject"]
            ),
            AutosarClass(
                name="ARObject",
                package="AUTOSAR::Base",
                is_abstract=True,
                bases=[]
            ),
            AutosarClass(
                name="DerivedClass",
                package="AUTOSAR::Derived",
                is_abstract=False,
                bases=["ExistingClass", "NonExistentBase"]
            ),
        ]

        doc = parser._build_package_hierarchy(class_defs)
        packages = doc.packages
        assert len(packages) == 1

        pkg = packages[0]
        derived_pkg = pkg.get_subpackage("Derived")
        derived = derived_pkg.get_class("DerivedClass")

        # Parent should be ExistingClass (only valid base after filtering)
        assert derived.parent == "ExistingClass"
        # Verify all bases are preserved (including non-existent one)
        assert derived.bases == ["ExistingClass", "NonExistentBase"]

    def test_parent_resolution_ancestry_based_multiple_independent_bases(self) -> None:
        """Test that ancestry-based parent selection handles multiple independent bases.

        SWUT_PARSER_00055: Test Parent Resolution Ancestry Based Multiple Independent Bases

        Requirements:
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution

        This test verifies backward compatibility with multiple independent bases:
        - Given three independent base classes with no ancestry relationships
        - When a class has bases [Base1, Base2, Base3]
        - Then parent should be "Base3" (last one, for backward compatibility)
        """
        parser = PdfParser()

        class_defs = [
            AutosarClass(
                name="ARObject",
                package="AUTOSAR::Base",
                is_abstract=True,
                bases=[]
            ),
            AutosarClass(
                name="Base1",
                package="AUTOSAR::Base",
                is_abstract=False,
                bases=["ARObject"]
            ),
            AutosarClass(
                name="Base2",
                package="AUTOSAR::Base",
                is_abstract=False,
                bases=["ARObject"]
            ),
            AutosarClass(
                name="Base3",
                package="AUTOSAR::Base",
                is_abstract=False,
                bases=["ARObject"]
            ),
            AutosarClass(
                name="DerivedClass",
                package="AUTOSAR::Derived",
                is_abstract=False,
                bases=["Base1", "Base2", "Base3"]
            ),
        ]

        doc = parser._build_package_hierarchy(class_defs)
        packages = doc.packages
        assert len(packages) == 1

        pkg = packages[0]
        derived_pkg = pkg.get_subpackage("Derived")
        derived = derived_pkg.get_class("DerivedClass")

        # Parent should be Base3 (last one, backward compatibility)
        assert derived.parent == "Base3"
        # Verify all bases are preserved
        assert derived.bases == ["Base1", "Base2", "Base3"]

    def test_is_valid_package_path(self) -> None:
        """Test package path validation.

        SWUT_PARSER_00047: Test Package Path Validation

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building
        """
        from autosar_pdf2txt.parser.class_parser import AutosarClassParser
        parser = AutosarClassParser()

        # Valid package paths
        assert parser._is_valid_package_path("M2::AUTOSAR::DataTypes") is True
        assert parser._is_valid_package_path("AUTOSAR::Templates") is True
        assert parser._is_valid_package_path("M2::MSR") is True
        assert parser._is_valid_package_path("Some_Package") is True
        assert parser._is_valid_package_path("_PrivatePackage") is True

        # Invalid package paths - spaces
        assert parser._is_valid_package_path("live in various packages which do not have a common") is False
        assert parser._is_valid_package_path("Package With Spaces") is False

        # Invalid package paths - special characters
        assert parser._is_valid_package_path("can coexist in the context of a ReferenceBase.(cid:99)()") is False
        assert parser._is_valid_package_path("Package.With.Dots") is False
        assert parser._is_valid_package_path("Package(With)Parens") is False

        # Invalid package paths - lowercase start
        assert parser._is_valid_package_path("lowercase::Package") is False
        assert parser._is_valid_package_path("anotherPackage") is False

        # Invalid package paths - empty parts
        assert parser._is_valid_package_path("AUTOSAR::") is False
        assert parser._is_valid_package_path("::AUTOSAR") is False


    def test_extract_class_with_multiline_aggregated_by(self) -> None:
        """Test extracting class with multi-line aggregated by list.

        SWUT_PARSER_00055: Test Extracting Class with Multi-Line Aggregated By

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00021: Multi-Line Attribute Parsing for AutosarClass

        This test verifies that multi-line "Aggregated by" lists are correctly parsed,
        including word splitting across lines (e.g., "SwComponent" + "Type" = "SwComponentType").
        """
        PdfParser()
        text = """
        Class SwDataDefProps
        Package M2::AUTOSAR::DataTypes
        Aggregated by ApplicationSwComponentPrototype,InternalBehavior,Prototype,SwComponent
        Type,Trigger,SwDataDefPropsConditional
        Note This element defines the data definition properties.
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        sw_data = class_defs[0]

        # Should include all aggregated by classes from both lines
        assert "ApplicationSwComponentPrototype" in sw_data.aggregated_by
        assert "InternalBehavior" in sw_data.aggregated_by
        assert "Prototype" in sw_data.aggregated_by
        assert "SwComponentType" in sw_data.aggregated_by  # Combined from SwComponent + Type
        assert "Trigger" in sw_data.aggregated_by
        assert "SwDataDefPropsConditional" in sw_data.aggregated_by

        # Verify exact count (6 items total)
        assert len(sw_data.aggregated_by) == 6

    def test_extract_class_with_multiline_subclasses(self) -> None:
        """Test extracting class with multi-line subclasses list.

        SWUT_PARSER_00056: Test Extracting Class with Multi-Line Subclasses

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00021: Multi-Line Attribute Parsing for AutosarClass

        This test verifies that multi-line "Subclasses" lists are correctly parsed.
        """
        PdfParser()
        text = """
        Class BaseType
        Package M2::AUTOSAR::DataTypes
        Subclasses DerivedType1,DerivedType2,DerivedType3
        ,DerivedType4,DerivedType5
        Note This is the base type.
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        base_type = class_defs[0]

        # Should include all subclasses from both lines
        assert "DerivedType1" in base_type.subclasses
        assert "DerivedType2" in base_type.subclasses
        assert "DerivedType3" in base_type.subclasses
        assert "DerivedType4" in base_type.subclasses
        assert "DerivedType5" in base_type.subclasses

        # Verify exact count (5 items total)
        assert len(base_type.subclasses) == 5

    def test_extract_class_with_aggregated_by_and_base_classes_multiline(self) -> None:
        """Test extracting class with both aggregated by and base classes, both multi-line.

        SWUT_PARSER_00057: Test Extracting Class with Aggregated By and Base Classes Multi-Line

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00021: Multi-Line Attribute Parsing for AutosarClass

        This test verifies that both "Aggregated by" and "Base" can be parsed
        correctly when they both span multiple lines.
        """
        PdfParser()
        text = """
        Class MyDataType
        Package M2::AUTOSAR::DataTypes
        Base ARObject,Identifiable,Packageable
        Element,Referrable
        Aggregated by SwComponentPrototype,InternalBehavior,Prototype
        ,Trigger
        Note This is a custom data type.
        """
        class_defs = _parse_class_text(text)
        assert len(class_defs) == 1
        my_type = class_defs[0]

        # Verify base classes (multi-line with word splitting)
        assert "ARObject" in my_type.bases
        assert "Identifiable" in my_type.bases
        assert "PackageableElement" in my_type.bases  # Combined from Packageable + Element
        assert "Referrable" in my_type.bases
        assert len(my_type.bases) == 4

        # Verify aggregated by (multi-line)
        assert "SwComponentPrototype" in my_type.aggregated_by
        assert "InternalBehavior" in my_type.aggregated_by
        assert "Prototype" in my_type.aggregated_by
        assert "Trigger" in my_type.aggregated_by
        assert len(my_type.aggregated_by) == 4

    def test_parent_resolution_missing_base_deduplicated_warnings(self) -> None:
        """Test that missing base class warnings are deduplicated.

        SWUT_PARSER_00058: Test Parent Resolution Missing Base Deduplicated Warnings

        Requirements:
            SWR_PARSER_00020: Missing Base Class Logging with Deduplication

        This test verifies that when multiple classes reference the same missing
        base class, warnings are logged only once per unique missing class,
        preventing log spam.
        """
        from unittest.mock import patch

        parser = PdfParser()

        # Create multiple classes that all reference the same missing base classes
        class_defs = [
            AutosarClass(
                name="DerivedClass1",
                package="AUTOSAR::Derived1",
                is_abstract=False,
                bases=["MissingBaseA", "ARObject"]
            ),
            AutosarClass(
                name="DerivedClass2",
                package="AUTOSAR::Derived2",
                is_abstract=False,
                bases=["MissingBaseA", "MissingBaseB", "ARObject"]
            ),
            AutosarClass(
                name="DerivedClass3",
                package="AUTOSAR::Derived3",
                is_abstract=False,
                bases=["MissingBaseB", "MissingBaseC", "ARObject"]
            ),
        ]

        # Capture warnings
        with patch('autosar_pdf2txt.parser.pdf_parser.logger') as mock_logger:
            doc = parser._build_package_hierarchy(class_defs)
            packages = doc.packages

            # Verify packages were created
            assert len(packages) == 1
            pkg = packages[0]

            # Verify all classes were created
            derived1_pkg = pkg.get_subpackage("Derived1")
            derived2_pkg = pkg.get_subpackage("Derived2")
            derived3_pkg = pkg.get_subpackage("Derived3")
            assert derived1_pkg is not None
            assert derived2_pkg is not None
            assert derived3_pkg is not None

            # Verify warning calls
            warning_calls = [call for call in mock_logger.warning.call_args_list]

            # Extract and format warning messages
            warning_messages = []
            for call in warning_calls:
                # call[0] contains positional args (format_string, arg1, arg2, ...)
                if call[0]:
                    format_string = call[0][0]
                    args = call[0][1:] if len(call[0]) > 1 else []
                    try:
                        formatted_msg = format_string % tuple(args) if args else format_string
                    except (TypeError, ValueError):
                        formatted_msg = format_string
                    warning_messages.append(formatted_msg)

            # Count unique missing base class warnings
            missing_base_warnings = [msg for msg in warning_messages
                                    if "could not be located in the model" in msg
                                    and "during ancestry traversal" not in msg]

            # Should have exactly 3 warnings (one for each unique missing base)
            assert len(missing_base_warnings) == 3, \
                f"Expected 3 unique missing base warnings, got {len(missing_base_warnings)}: {missing_base_warnings}"

            # Verify each missing base is warned about exactly once
            assert any("MissingBaseA" in msg for msg in missing_base_warnings), \
                "MissingBaseA should be in warnings"
            assert any("MissingBaseB" in msg for msg in missing_base_warnings), \
                "MissingBaseB should be in warnings"
            assert any("MissingBaseC" in msg for msg in missing_base_warnings), \
                "MissingBaseC should be in warnings"

            # Verify no duplicates
            base_names = []
            for msg in missing_base_warnings:
                # Extract class name from message
                if "Class '" in msg:
                    start = msg.find("Class '") + 7
                    end = msg.find("'", start)
                    base_names.append(msg[start:end])

            assert len(base_names) == len(set(base_names)), \
                f"Each base class should appear only once, got duplicates: {base_names}"

    @pytest.mark.skip(reason="Ancestry traversal warning functionality not implemented")
    def test_parent_resolution_missing_ancestry_deduplicated_warnings(self) -> None:
        """Test that missing ancestry class warnings are deduplicated.

        SWUT_PARSER_00059: Test Parent Resolution Missing Ancestry Deduplicated Warnings

        Requirements:
            SWR_PARSER_00020: Missing Base Class Logging with Deduplication

        This test verifies that when ancestry traversal encounters missing classes
        referenced from multiple classes, warnings are logged only once per unique
        missing class, preventing log spam from repeated references.
        """
        from unittest.mock import patch

        parser = PdfParser()

        # Create a hierarchy where multiple classes reference the same missing base
        # Base -> MissingMiddle -> Derived
        class_defs = [
            AutosarClass(
                name="BaseClass",
                package="AUTOSAR::Base",
                is_abstract=False,
                bases=["ARObject"]
            ),
            AutosarClass(
                name="DerivedClass1",
                package="AUTOSAR::Derived1",
                is_abstract=False,
                bases=["MissingMiddleClass", "ARObject"]
            ),
            AutosarClass(
                name="DerivedClass2",
                package="AUTOSAR::Derived2",
                is_abstract=False,
                bases=["MissingMiddleClass", "ARObject"]
            ),
            AutosarClass(
                name="DerivedClass3",
                package="AUTOSAR::Derived3",
                is_abstract=False,
                bases=["MissingMiddleClass", "ARObject"]
            ),
        ]

        # Capture warnings
        with patch('autosar_pdf2txt.parser.pdf_parser.logger') as mock_logger:
            doc = parser._build_package_hierarchy(class_defs)
            packages = doc.packages

            # Verify packages were created
            assert len(packages) == 1

            # Verify warning calls
            warning_calls = [call for call in mock_logger.warning.call_args_list]

            # Extract and format warning messages
            warning_messages = []
            for call in warning_calls:
                # call[0] contains positional args (format_string, arg1, arg2, ...)
                if call[0]:
                    format_string = call[0][0]
                    args = call[0][1:] if len(call[0]) > 1 else []
                    try:
                        formatted_msg = format_string % tuple(args) if args else format_string
                    except (TypeError, ValueError):
                        formatted_msg = format_string
                    warning_messages.append(formatted_msg)

            # Count ancestry traversal warnings
            ancestry_warnings = [msg for msg in warning_messages
                               if "during ancestry traversal" in msg]

            # Should have exactly 1 ancestry warning for MissingMiddleClass
            assert len(ancestry_warnings) == 1, \
                f"Expected 1 unique ancestry warning, got {len(ancestry_warnings)}: {ancestry_warnings}"

            # Verify the warning mentions the missing class
            assert "MissingMiddleClass" in ancestry_warnings[0], \
                "Ancestry warning should mention MissingMiddleClass"

    def test_parent_resolution_builds_data_structures_once(self) -> None:
        """Test that class registry and ancestry cache are built only once.

        SWUT_PARSER_00060: Test Parent Resolution Builds Data Structures Once

        Requirements:
            SWR_PARSER_00020: Missing Base Class Logging with Deduplication

        This test verifies that the class registry and ancestry cache are built
        only on the initial call to _set_parent_references and are reused in
        recursive calls, avoiding redundant computation.
        """
        from unittest.mock import patch

        parser = PdfParser()

        # Create nested packages to trigger recursive calls
        class_defs = [
            AutosarClass(
                name="Class1",
                package="AUTOSAR::Package1::SubPackage1",
                is_abstract=False,
                bases=["ARObject"]
            ),
            AutosarClass(
                name="Class2",
                package="AUTOSAR::Package1::SubPackage2",
                is_abstract=False,
                bases=["ARObject"]
            ),
            AutosarClass(
                name="Class3",
                package="AUTOSAR::Package2",
                is_abstract=False,
                bases=["ARObject"]
            ),
        ]

        # Patch _build_ancestry_cache to track call count
        original_build_cache = parser._build_ancestry_cache
        call_count = [0]

        def mock_build_cache(packages):
            call_count[0] += 1
            return original_build_cache(packages)

        with patch.object(parser, '_build_ancestry_cache', side_effect=mock_build_cache):
            parser._build_package_hierarchy(class_defs)

            # _build_ancestry_cache should be called exactly once (not once per package)
            assert call_count[0] == 1, \
                f"_build_ancestry_cache should be called once, was called {call_count[0]} times"

def _parse_all_types(text: str) -> List[Union[AutosarClass, AutosarEnumeration, AutosarPrimitive]]:
    """Helper function to parse all type definitions (Class, Primitive, Enumeration) from text.

    This function simulates the old _parse_class_text behavior but handles all types.

    Args:
        text: The text to parse.

    Returns:
        List of parsed model objects (AutosarClass, AutosarEnumeration, or AutosarPrimitive).
    """
    class_parser = AutosarClassParser()
    enum_parser = AutosarEnumerationParser()
    primitive_parser = AutosarPrimitiveParser()
    
    lines = text.strip().split("\n")
    models = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Try to parse a class definition
        class_def = class_parser.parse_definition(lines, i)
        if class_def:
            new_i, is_complete = class_parser.continue_parsing(class_def, lines, i + 1)
            models.append(class_def)
            i = new_i
            continue

        # Try to parse a primitive definition
        primitive_def = primitive_parser.parse_definition(lines, i)
        if primitive_def:
            new_i, is_complete = primitive_parser.continue_parsing(primitive_def, lines, i + 1)
            models.append(primitive_def)
            i = new_i
            continue

        # Try to parse an enumeration definition
        enum_def = enum_parser.parse_definition(lines, i)
        if enum_def:
            new_i, is_complete = enum_parser.continue_parsing(enum_def, lines, i + 1)
            models.append(enum_def)
            i = new_i
            continue

        i += 1

    return models


class TestAncestryBasedParentSelection:
    """Tests for ancestry-based parent selection algorithm.

    Requirements:
        SWR_PARSER_00017: AUTOSAR Class Parent Resolution
    """

    def test_parent_selection_with_multiple_bases_ancestry(self) -> None:
        """Test ancestry-based parent selection with multiple bases.

        SWUT_PARSER_00061: Test Ancestry-Based Parent Selection with Multiple Bases

        Requirements:
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution

        This test verifies that when a class has multiple base classes with ancestry
        relationships, the system correctly identifies the direct parent by filtering
        out ancestors.
        """
        from autosar_pdf2txt.models import AutosarPackage

        # Create classes with inheritance hierarchy
        level1 = AutosarClass(name="Level1", package="M2::Test", is_abstract=False)
        level1.bases = []

        level2 = AutosarClass(name="Level2", package="M2::Test", is_abstract=False)
        level2.bases = ["Level1"]

        level3 = AutosarClass(name="Level3", package="M2::Test", is_abstract=False)
        level3.bases = ["Level2"]

        level4 = AutosarClass(name="Level4", package="M2::Test", is_abstract=False)
        level4.bases = ["Level3"]

        derived = AutosarClass(name="DerivedWithMultipleBases", package="M2::Test", is_abstract=False)
        derived.bases = ["Level1", "Level2", "Level3", "Level4"]

        # Create package and add classes
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(level1)
        pkg.add_class(level2)
        pkg.add_class(level3)
        pkg.add_class(level4)
        pkg.add_class(derived)

        # Build package hierarchy and resolve parent references
        parser = PdfParser()
        parser._build_package_hierarchy([level1, level2, level3, level4, derived])
        # Resolve parent references (this is where ancestry-based selection happens)
        all_packages = [pkg]  # In real scenario, this would be doc.packages
        parser._resolve_parent_references(all_packages)

        # Verify parent is correctly identified as Level4 (most specific, not ancestor)
        derived_class = pkg.get_class("DerivedWithMultipleBases")
        assert derived_class is not None
        assert derived_class.parent == "Level4", \
            f"Expected parent to be 'Level4' but got '{derived_class.parent}'"

    def test_parent_selection_with_independent_bases(self) -> None:
        """Test parent selection with independent base classes.

        SWUT_PARSER_00062: Test Parent Selection with Independent Bases

        Requirements:
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution

        This test verifies that when a class has multiple independent base classes
        (no ancestry relationships), the system selects the last base as the parent.
        """
        from autosar_pdf2txt.models import AutosarPackage

        # Create classes with independent bases
        base1 = AutosarClass(name="BaseClass1", package="M2::Test", is_abstract=False)
        base1.bases = []

        base2 = AutosarClass(name="BaseClass2", package="M2::Test", is_abstract=False)
        base2.bases = []

        base3 = AutosarClass(name="BaseClass3", package="M2::Test", is_abstract=False)
        base3.bases = []

        derived = AutosarClass(name="DerivedClass", package="M2::Test", is_abstract=False)
        derived.bases = ["BaseClass1", "BaseClass2", "BaseClass3"]

        # Create package and add classes
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(base1)
        pkg.add_class(base2)
        pkg.add_class(base3)
        pkg.add_class(derived)

        # Build package hierarchy
        parser = PdfParser()
        doc = parser._build_package_hierarchy([base1, base2, base3, derived])

        # Verify parent is correctly identified as BaseClass3 (last base)
        derived_class = None
        for pkg in doc.packages:
            derived_class = pkg.get_class("DerivedClass")
            if derived_class:
                break

        assert derived_class is not None
        assert derived_class.parent == "BaseClass3", \
            f"Expected parent to be 'BaseClass3' but got '{derived_class.parent}'"

    def test_parent_selection_with_missing_base_classes(self) -> None:
        """Test parent selection with missing base classes.

        SWUT_PARSER_00063: Test Parent Selection with Missing Base Classes

        Requirements:
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution

        This test verifies that when a class has base classes that don't exist
        in the model, the system filters them out and selects from the remaining bases.
        """
        from autosar_pdf2txt.models import AutosarPackage

        # Create classes
        existing = AutosarClass(name="ExistingClass", package="M2::Test", is_abstract=False)
        existing.bases = []

        derived = AutosarClass(name="DerivedClass", package="M2::Test", is_abstract=False)
        derived.bases = ["ExistingClass", "NonExistentBase"]

        # Create package and add classes
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(existing)
        pkg.add_class(derived)

        # Build package hierarchy
        parser = PdfParser()
        doc = parser._build_package_hierarchy([existing, derived])

        # Verify parent is correctly identified as ExistingClass
        derived_class = None
        for pkg in doc.packages:
            derived_class = pkg.get_class("DerivedClass")
            if derived_class:
                break

        assert derived_class is not None
        assert derived_class.parent == "ExistingClass", \
            f"Expected parent to be 'ExistingClass' but got '{derived_class.parent}'"
