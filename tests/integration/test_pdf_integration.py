"""Integration tests for AUTOSAR PDF parsing.

These tests use real AUTOSAR PDF files to verify end-to-end functionality.
"""

import os
import pytest

from autosar_pdf2txt.parser import PdfParser


class TestPdfIntegration:
    """Integration tests using real AUTOSAR PDF files.

    These tests require actual PDF files to be present in the examples/pdf directory.
    Tests are skipped if files are not available (for CI/CD environments).
    """

    def test_parse_bsw_module_template_pdf_first_class(self) -> None:
        """Test parsing real AUTOSAR BSW Module Template PDF and verify first class.

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00006: Package Hierarchy Building
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        parser = PdfParser()
        pdf_path = "examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf"

        # Skip test if PDF doesn't exist (for CI/CD environments)
        if not os.path.exists(pdf_path):
            pytest.skip(f"PDF file not found: {pdf_path}")

        # Parse the PDF
        packages = parser.parse_pdf(pdf_path)

        # Verify we got some packages
        assert len(packages) > 0, "Should extract at least one package from PDF"

        # Find the first class with actual data
        first_class = None
        first_package = None

        for pkg in packages:
            if pkg.classes:
                first_package = pkg
                first_class = pkg.classes[0]
                break

            # Check subpackages
            for subpkg in pkg.subpackages:
                if subpkg.classes:
                    first_package = subpkg
                    first_class = subpkg.classes[0]
                    break
            if first_class:
                break

        assert first_class is not None, "Should find at least one class in the PDF"
        assert first_package is not None, "Should find the package containing the class"

        # Verify the first class details
        assert first_class.name == "AUTOSAR", f"Expected class name 'AUTOSAR', got '{first_class.name}'"
        assert first_class.is_abstract is False, "AUTOSAR class should not be abstract"
        assert first_package.name == "AutosarTopLevelStructure", f"Expected package 'AutosarTopLevelStructure', got '{first_package.name}'"

        # Verify bases - should have one base class
        assert len(first_class.bases) == 1, f"Expected 1 base class, got {len(first_class.bases)}"
        assert "ARObject" in first_class.bases, f"Expected 'ARObject' in bases, got {first_class.bases}"

        # Verify note - should have a note
        assert first_class.note is not None, "AUTOSAR class should have a note"
        assert len(first_class.note) > 0, "Note should not be empty"
        assert "AUTOSAR" in first_class.note or "Rootelement" in first_class.note, \
            f"Note should contain AUTOSAR or Rootelement, got: '{first_class.note}'"

        # Print class information for verification
        print("\nFirst class found:")
        print(f"  Name: {first_class.name}")
        print(f"  Abstract: {first_class.is_abstract}")
        print(f"  Bases: {first_class.bases}")
        print(f"  Note: {first_class.note}")
        print(f"  Package: {first_package.name}")

    def test_parse_bsw_module_template_pdf_multiple_classes(self) -> None:
        """Test that multiple classes are parsed from real AUTOSAR PDF.

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00006: Package Hierarchy Building
        """
        parser = PdfParser()
        pdf_path = "examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf"

        # Skip test if PDF doesn't exist
        if not os.path.exists(pdf_path):
            pytest.skip(f"PDF file not found: {pdf_path}")

        # Parse the PDF
        packages = parser.parse_pdf(pdf_path)

        # Count total classes
        total_classes = 0
        for pkg in packages:
            total_classes += len(pkg.classes)
            for subpkg in pkg.subpackages:
                total_classes += len(subpkg.classes)

        # Should have extracted many classes from the AUTOSAR template
        assert total_classes > 10, f"Expected to extract many classes, got {total_classes}"

        print(f"\nTotal classes extracted: {total_classes}")
        print(f"Total packages: {len(packages)}")

    def test_parse_bsw_module_template_pdf_has_bases_and_notes(self) -> None:
        """Test that classes with bases and notes are parsed correctly.

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        parser = PdfParser()
        pdf_path = "examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf"

        # Skip test if PDF doesn't exist
        if not os.path.exists(pdf_path):
            pytest.skip(f"PDF file not found: {pdf_path}")

        # Parse the PDF
        packages = parser.parse_pdf(pdf_path)

        # Find classes with bases and notes
        classes_with_bases = []
        classes_with_notes = []

        for pkg in packages:
            for cls in pkg.classes:
                if cls.bases:
                    classes_with_bases.append(cls)
                if cls.note:
                    classes_with_notes.append(cls)

            for subpkg in pkg.subpackages:
                for cls in subpkg.classes:
                    if cls.bases:
                        classes_with_bases.append(cls)
                    if cls.note:
                        classes_with_notes.append(cls)

        # Verify we have classes with bases
        assert len(classes_with_bases) > 0, "Should find classes with base classes"

        # Verify we have classes with notes
        assert len(classes_with_notes) > 0, "Should find classes with notes"

        print(f"\nClasses with bases: {len(classes_with_bases)}")
        print(f"Classes with notes: {len(classes_with_notes)}")

        # Show examples
        if classes_with_bases:
            example = classes_with_bases[0]
            print("\nExample class with bases:")
            print(f"  Name: {example.name}")
            print(f"  Bases: {example.bases}")

        if classes_with_notes:
            example = classes_with_notes[0]
            print("\nExample class with note:")
            print(f"  Name: {example.name}")
            print(f"  Note: {example.note}")
