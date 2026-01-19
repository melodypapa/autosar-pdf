"""Integration tests for AUTOSAR PDF parsing.

These tests use real AUTOSAR PDF files to verify end-to-end functionality.
"""

import os
import pytest

from autosar_pdf2txt.models import ATPType
from autosar_pdf2txt.parser import PdfParser


class TestPdfIntegration:
    """Integration tests using real AUTOSAR PDF files.

    These tests require actual PDF files to be present in the examples/pdf directory.
    Tests are skipped if files are not available (for CI/CD environments).
    """

    def test_parse_bsw_module_template_pdf_first_class(self) -> None:
        """Test parsing real AUTOSAR BSW Module Template PDF and verify first class.

        SWIT_00001: Test Parsing Real AUTOSAR PDF and Verifying First Class

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00006: Package Hierarchy Building
            SWR_PARSER_00009: Proper Word Spacing in PDF Text Extraction
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
            # Check M2 top-level package (may not have classes directly)
            if pkg.types:
                first_package = pkg
                first_class = pkg.types[0]
                break

            # Check subpackages (AUTOSARTemplates, MSR, etc.)
            for subpkg in pkg.subpackages:
                if subpkg.types:
                    first_package = subpkg
                    first_class = subpkg.types[0]
                    break

                # Check nested subpackages (e.g., AutosarTopLevelStructure)
                for subsubpkg in subpkg.subpackages:
                    if subsubpkg.types:
                        first_package = subsubpkg
                        first_class = subsubpkg.types[0]
                        break
                    if first_class:
                        break
                if first_class:
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

        SWIT_00002: Test Parsing Real AUTOSAR PDF Extracts Multiple Classes

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00006: Package Hierarchy Building
            SWR_PARSER_00009: Proper Word Spacing in PDF Text Extraction
        """
        parser = PdfParser()
        pdf_path = "examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf"

        # Skip test if PDF doesn't exist
        if not os.path.exists(pdf_path):
            pytest.skip(f"PDF file not found: {pdf_path}")

        # Parse the PDF
        packages = parser.parse_pdf(pdf_path)

        # Count total classes recursively
        def count_classes(pkg):
            count = len(pkg.types)
            for subpkg in pkg.subpackages:
                count += count_classes(subpkg)
            return count

        total_classes = 0
        for pkg in packages:
            total_classes += count_classes(pkg)

        # Should have extracted many classes from the AUTOSAR template
        assert total_classes > 10, f"Expected to extract many classes, got {total_classes}"

        print(f"\nTotal classes extracted: {total_classes}")
        print(f"Total packages: {len(packages)}")

    def test_parse_bsw_module_template_pdf_has_bases_and_notes(self) -> None:
        """Test parsing real AUTOSAR PDF has bases and notes.

        SWIT_00003: Test Parsing Real AUTOSAR PDF Has Bases and Notes

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00009: Proper Word Spacing in PDF Text Extraction
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        parser = PdfParser()
        pdf_path = "examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf"

        # Skip test if PDF doesn't exist
        if not os.path.exists(pdf_path):
            pytest.skip(f"PDF file not found: {pdf_path}")

        # Parse the PDF
        packages = parser.parse_pdf(pdf_path)

        # Find classes with bases and notes recursively
        classes_with_bases = []
        classes_with_notes = []

        def collect_classes(pkg):
            for cls in pkg.types:
                if cls.bases:
                    classes_with_bases.append(cls)
                if cls.note:
                    classes_with_notes.append(cls)
            for subpkg in pkg.subpackages:
                collect_classes(subpkg)

        for pkg in packages:
            collect_classes(pkg)

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

    def test_parse_pdf_with_atp_patterns(self, monkeypatch) -> None:
        """Test end-to-end parsing and writing with ATP patterns.

        SWIT_00005: Test End-to-End Parsing and Writing with ATP Patterns

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_MODEL_00001: AUTOSAR Class Representation
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        parser = PdfParser()

        # Mock pdfplumber to return class with ATP patterns
        class MockPage:
            def extract_words(self, x_tolerance=1):
                # Return word data structure with 'text' and 'top' keys
                return [
                    {'text': 'Class', 'top': 0},
                    {'text': 'MyData', 'top': 0},
                    {'text': '<<atpVariation>>', 'top': 0},
                    {'text': 'Package', 'top': 10},
                    {'text': 'M2::AUTOSAR::Data', 'top': 10},
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

        # Parse PDF
        packages = parser.parse_pdf("dummy.pdf")

        # Verify parsing
        assert len(packages) == 1
        m2_pkg = packages[0]
        assert m2_pkg.name == "M2"
        autosar_pkg = m2_pkg.get_subpackage("AUTOSAR")
        assert autosar_pkg is not None
        data_pkg = autosar_pkg.get_subpackage("Data")
        assert data_pkg is not None
        my_data = data_pkg.get_class("MyData")
        assert my_data is not None
        assert my_data.atp_type == ATPType.ATP_VARIATION

        # Verify writer output
        from autosar_pdf2txt.writer import MarkdownWriter
        import tempfile

        writer = MarkdownWriter()
        with tempfile.TemporaryDirectory() as tmp_dir:
            from pathlib import Path
            writer.write_packages_to_files(packages, base_dir=Path(tmp_dir))

            # Check individual file has ATP section
            class_file = Path(tmp_dir) / "M2" / "AUTOSAR" / "Data" / "MyData.md"
            content = class_file.read_text(encoding="utf-8")
            assert "## ATP Type\n\n" in content
            assert "* atpVariation\n" in content

    def test_parse_ecu_configuration_pdf_fibex_package_structure(self) -> None:
        """Test parsing ECU Configuration PDF and verify Fibex package structure and ImplementationDataType attributes.

        SWIT_00004: Test Parsing ECU Configuration PDF and Verifying Fibex Package Structure and ImplementationDataType Attributes

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00006: Package Hierarchy Building
            SWR_PARSER_00007: Top-Level Package Selection
            SWR_PARSER_00009: Proper Word Spacing in PDF Text Extraction
            SWR_PARSER_00010: Attribute Extraction from PDF
            SWR_PARSER_00011: Metadata Filtering in Attribute Extraction
            SWR_PARSER_00012: Multi-Line Attribute Handling
            SWR_MODEL_00004: AUTOSAR Package Representation
        """
        parser = PdfParser()
        pdf_path = "examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf"

        # Skip test if PDF doesn't exist
        if not os.path.exists(pdf_path):
            pytest.skip(f"PDF file not found: {pdf_path}")

        # Parse the PDF
        packages = parser.parse_pdf(pdf_path)

        # Verify we have exactly 1 top-level package (M2)
        assert len(packages) == 1, f"Expected 1 top-level package (M2), got {len(packages)}"

        # Find M2 package
        m2_pkg = packages[0]
        assert m2_pkg.name == "M2", f"Expected top-level package 'M2', got '{m2_pkg.name}'"

        # Find AUTOSARTemplates subpackage under M2
        autosar_templates_pkg = m2_pkg.get_subpackage("AUTOSARTemplates")
        assert autosar_templates_pkg is not None, "AUTOSARTemplates should be a subpackage of M2"

        # Find SystemTemplate subpackage
        system_template_pkg = autosar_templates_pkg.get_subpackage("SystemTemplate")
        assert system_template_pkg is not None, "SystemTemplate should be a subpackage of AUTOSARTemplates"

        # Find Fibex subpackage
        fibex_pkg = system_template_pkg.get_subpackage("Fibex")
        assert fibex_pkg is not None, "Fibex should be a subpackage of SystemTemplate"

        # Find FibexCore subpackage
        fibex_core_pkg = fibex_pkg.get_subpackage("FibexCore")
        assert fibex_core_pkg is not None, "FibexCore should be a subpackage of Fibex"

        # Find CoreCommunication subpackage
        core_comm_pkg = fibex_core_pkg.get_subpackage("CoreCommunication")
        assert core_comm_pkg is not None, "CoreCommunication should be a subpackage of FibexCore"

        # Verify CoreCommunication has classes
        assert len(core_comm_pkg.types) > 0, "CoreCommunication should contain classes"

        # Verify specific Fibex classes exist
        fibex_class_names = [cls.name for cls in core_comm_pkg.types]
        expected_classes = ["Frame", "NPdu", "Pdu", "PduTriggering", "UserDefinedPdu"]
        for expected_class in expected_classes:
            assert expected_class in fibex_class_names, \
                f"Expected class '{expected_class}' not found in CoreCommunication. Found: {fibex_class_names}"

        # Verify Fibex is NOT a top-level package
        top_level_names = [pkg.name for pkg in packages]
        assert "Fibex" not in top_level_names, \
            f"Fibex should not be a top-level package. Top-level packages: {top_level_names}"
        assert "SystemTemplate" not in top_level_names, \
            f"SystemTemplate should not be a top-level package. Top-level packages: {top_level_names}"
        assert "FibexCore" not in top_level_names, \
            f"FibexCore should not be a top-level package. Top-level packages: {top_level_names}"
        assert "AUTOSARTemplates" not in top_level_names, \
            f"AUTOSARTemplates should not be a top-level package. Top-level packages: {top_level_names}"

        # Verify package hierarchy path
        print("\nFibex package hierarchy verified:")
        print("  Top-level: M2")
        print("    └─ AUTOSARTemplates")
        print("       └─ SystemTemplate")
        print("          └─ Fibex")
        print("             └─ FibexCore")
        print(f"                └─ CoreCommunication ({len(core_comm_pkg.types)} classes)")
        print(f"                   Classes: {', '.join(sorted(fibex_class_names))}")

        # Find CommonStructure subpackage under AUTOSARTemplates
        common_structure_pkg = autosar_templates_pkg.get_subpackage("CommonStructure")
        assert common_structure_pkg is not None, "CommonStructure should be a subpackage of AUTOSARTemplates"

        # Find ImplementationDataTypes subpackage under CommonStructure
        impl_data_types_pkg = common_structure_pkg.get_subpackage("ImplementationDataTypes")
        assert impl_data_types_pkg is not None, "ImplementationDataTypes should be a subpackage of CommonStructure"

        # Find ImplementationDataType class
        impl_data_type = impl_data_types_pkg.get_class("ImplementationDataType")
        assert impl_data_type is not None, "ImplementationDataType class should exist in ImplementationDataTypes"

        # Verify ImplementationDataType has exactly 5 attributes
        assert len(impl_data_type.attributes) == 5, \
            f"ImplementationDataType should have 5 attributes, got {len(impl_data_type.attributes)}"

        # Verify the expected attributes exist
        expected_attributes = {
            "dynamicArray": "String",
            "isStructWithOptionalElement": "Boolean",
            "subElement": "ImplementationData",
            "symbolProps": "SymbolProps",
            "typeEmitter": "NameToken"
        }

        for attr_name, expected_type in expected_attributes.items():
            assert attr_name in impl_data_type.attributes, \
                f"Expected attribute '{attr_name}' not found. Found: {list(impl_data_type.attributes.keys())}"
            assert impl_data_type.attributes[attr_name].type == expected_type, \
                f"Attribute '{attr_name}' should have type '{expected_type}', got '{impl_data_type.attributes[attr_name].type}'"

        print("\nImplementationDataType attributes verified:")
        print(f"  Total attributes: {len(impl_data_type.attributes)}")
        for attr_name, attr in impl_data_type.attributes.items():
            print(f"    - {attr_name}: {attr.type} (ref: {attr.is_ref})")
