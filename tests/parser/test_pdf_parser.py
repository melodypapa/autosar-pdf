"""Tests for PdfParser class.

Test coverage for pdf_parser.py targeting PDF parsing functionality.
"""

import pytest

from autosar_pdf2txt.models import AutosarPackage
from autosar_pdf2txt.parser import PdfParser


class TestPdfParser:
    """Tests for PdfParser class.

    Requirements:
        SWR_PARSER_00001: PDF Parser Initialization
        SWR_PARSER_00003: PDF File Parsing
        SWR_PARSER_00004: Class Definition Pattern Recognition
        SWR_PARSER_00005: Class Definition Data Model
        SWR_PARSER_00006: Package Hierarchy Building
    """

    def test_init(self) -> None:
        """Test parser initialization.

        Requirements:
            SWR_PARSER_00001: PDF Parser Initialization
        """
        parser = PdfParser()
        assert parser is not None

    def test_extract_class_with_base_classes(self) -> None:
        """Test extracting class with base classes.

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        parser = PdfParser()
        text = """
        Class RunnableEntity
        Package M2::AUTOSAR::BswModule
        Base InternalBehavior
        """
        class_defs = parser._parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "RunnableEntity"
        assert class_defs[0].base_classes == ["InternalBehavior"]

    def test_extract_class_with_multiple_base_classes(self) -> None:
        """Test extracting class with multiple base classes.

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        parser = PdfParser()
        text = """
        Class DerivedClass
        Package M2::AUTOSAR
        Base BaseClass1, BaseClass2, BaseClass3
        """
        class_defs = parser._parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].base_classes == ["BaseClass1", "BaseClass2", "BaseClass3"]

    def test_extract_class_with_note(self) -> None:
        """Test extracting class with note.

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        parser = PdfParser()
        text = """
        Class BswInternalBehavior
        Package M2::AUTOSAR::BswModule
        Note Implementation for basic software internal behavior
        """
        class_defs = parser._parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "BswInternalBehavior"
        assert class_defs[0].note == "Implementation for basic software internal behavior"

    def test_extract_class_with_base_and_note(self) -> None:
        """Test extracting class with both base classes and note.

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        parser = PdfParser()
        text = """
        Class BswInternalBehavior
        Package M2::AUTOSAR::BswModule
        Base InternalBehavior
        Note Implementation for basic software entities
        """
        class_defs = parser._parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "BswInternalBehavior"
        assert class_defs[0].base_classes == ["InternalBehavior"]
        assert class_defs[0].note == "Implementation for basic software entities"

    def test_extract_class_without_base_or_note(self) -> None:
        """Test extracting class without base classes or note.

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        parser = PdfParser()
        text = """
        Class SimpleClass
        Package M2::AUTOSAR
        """
        class_defs = parser._parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "SimpleClass"
        assert class_defs[0].base_classes == []
        assert class_defs[0].note is None

    def test_extract_class_with_abstract(self) -> None:
        """Test extracting abstract class.

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        parser = PdfParser()
        text = """
        Class InternalBehavior (abstract)
        Package M2::AUTOSAR
        """
        class_defs = parser._parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "InternalBehavior"
        assert class_defs[0].is_abstract is True

    def test_extract_class_with_subclasses(self) -> None:
        """Test extracting class with subclasses.

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
        """
        parser = PdfParser()
        text = """
        Class BaseClass
        Package M2::AUTOSAR
        Subclasses DerivedClass1, DerivedClass2
        """
        class_defs = parser._parse_class_text(text)
        assert len(class_defs) == 1
        assert class_defs[0].name == "BaseClass"
        assert class_defs[0].subclasses == ["DerivedClass1", "DerivedClass2"]

    def test_extract_multiple_classes(self) -> None:
        """Test extracting multiple classes.

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
        """
        parser = PdfParser()
        text = """
        Class InternalBehavior (abstract)
        Package M2::AUTOSAR
        Note Base class for all internal behaviors

        Class BswInternalBehavior
        Package M2::AUTOSAR::BswModule
        Base InternalBehavior
        Note Basic software internal behavior implementation
        """
        class_defs = parser._parse_class_text(text)
        assert len(class_defs) == 2
        assert class_defs[0].name == "InternalBehavior"
        assert class_defs[0].is_abstract is True
        assert class_defs[0].note == "Base class for all internal behaviors"
        assert class_defs[1].name == "BswInternalBehavior"
        assert class_defs[1].base_classes == ["InternalBehavior"]
        assert class_defs[1].note == "Basic software internal behavior implementation"

    def test_build_packages_with_bases_and_notes(self) -> None:
        """Test building package hierarchy with bases and notes.

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building
        """
        parser = PdfParser()
        from autosar_pdf2txt.parser.pdf_parser import ClassDefinition

        class_defs = [
            ClassDefinition(
                name="InternalBehavior",
                package_path="AUTOSAR",
                is_abstract=True,
                note="Base behavior class"
            ),
            ClassDefinition(
                name="BswInternalBehavior",
                package_path="AUTOSAR::BswModule",
                is_abstract=False,
                base_classes=["InternalBehavior"],
                note="BSW specific behavior"
            )
        ]

        packages = parser._build_package_hierarchy(class_defs)
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

    def test_extract_with_pdfplumber_exception_handling(self, monkeypatch) -> None:
        """Test exception handling in _extract_with_pdfplumber.

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

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building
        """
        parser = PdfParser()
        from autosar_pdf2txt.parser.pdf_parser import ClassDefinition

        # Create package and subpackage
        parent_pkg = parser._build_package_hierarchy([
            ClassDefinition(
                name="Class1",
                package_path="AUTOSAR::Module1",
                is_abstract=False
            )
        ])

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
            ClassDefinition(
                name="Class1",
                package_path="AUTOSAR::Module1",
                is_abstract=False
            ),
            ClassDefinition(
                name="Class2",
                package_path="AUTOSAR::Module1",  # Same path, should trigger duplicate
                is_abstract=False
            ),
            ClassDefinition(
                name="Class3",
                package_path="AUTOSAR::Module2",
                is_abstract=False
            ),
        ]

        # Should not raise ValueError for duplicate subpackages
        packages = parser._build_package_hierarchy(class_defs)

        # Should successfully create packages
        assert len(packages) == 1
        assert packages[0].name == "AUTOSAR"

        # Should have Module1 and Module2 as subpackages
        module1 = packages[0].get_subpackage("Module1")
        assert module1 is not None
        assert len(module1.classes) == 2  # Class1 and Class2

        module2 = packages[0].get_subpackage("Module2")
        assert module2 is not None
        assert len(module2.classes) == 1  # Class3

    def test_build_package_handles_duplicate_classes(self) -> None:
        """Test that _build_package_hierarchy handles duplicate classes gracefully.

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building
        """
        parser = PdfParser()
        from autosar_pdf2txt.parser.pdf_parser import ClassDefinition
        from autosar_pdf2txt.models import AutosarClass

        # Create package with a class
        packages = parser._build_package_hierarchy([
            ClassDefinition(
                name="ExistingClass",
                package_path="AUTOSAR",
                is_abstract=False,
                base_classes=["Base1"]
            )
        ])

        # Try to manually add duplicate class (should trigger ValueError)
        duplicate_class = AutosarClass(
            name="ExistingClass",
            is_abstract=False,
            bases=["Base2"]
        )

        try:
            packages[0].add_class(duplicate_class)
        except ValueError:
            pass  # Expected

        # Now test with duplicate class definitions
        class_defs = [
            ClassDefinition(
                name="DuplicateClass",
                package_path="AUTOSAR",
                is_abstract=False,
                base_classes=["Base1"]
            ),
            ClassDefinition(
                name="DuplicateClass",
                package_path="AUTOSAR",
                is_abstract=False,
                base_classes=["Base2"]
            ),
        ]

        # Should not raise ValueError for duplicate classes
        packages = parser._build_package_hierarchy(class_defs)

        # Should successfully create package with one class
        assert len(packages) == 1
        assert packages[0].name == "AUTOSAR"

        # Should have only one instance of DuplicateClass
        duplicate_class = packages[0].get_class("DuplicateClass")
        assert duplicate_class is not None
        # First definition wins
        assert duplicate_class.bases == ["Base1"]

    def test_parse_pdf_with_nonexistent_file(self) -> None:
        """Test parsing a non-existent PDF file.

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

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00006: Package Hierarchy Building
        """
        parser = PdfParser()

        # Mock pdfplumber.open to return test data
        class MockPage:
            def extract_text(self):
                return "Class TestClass\nPackage AUTOSAR::Module\n"

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
        packages = parser.parse_pdf("dummy.pdf")

        # Verify results
        assert len(packages) == 1
        assert packages[0].name == "AUTOSAR"

    def test_build_package_with_empty_parts(self) -> None:
        """Test that empty package parts are skipped.

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building
        """
        parser = PdfParser()
        from autosar_pdf2txt.parser.pdf_parser import ClassDefinition

        # Create class definition with empty parts in package path
        class_defs = [
            ClassDefinition(
                name="TestClass",
                package_path="AUTOSAR::::Module",  # Multiple consecutive colons
                is_abstract=False
            ),
        ]

        # Should handle empty parts gracefully
        packages = parser._build_package_hierarchy(class_defs)

        assert len(packages) == 1
        assert packages[0].name == "AUTOSAR"

        # Module should be created as subpackage
        module = packages[0].get_subpackage("Module")
        assert module is not None
        assert len(module.classes) == 1
        assert module.classes[0].name == "TestClass"


