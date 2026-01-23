"""Integration tests for AUTOSAR PDF parsing.

These tests use real AUTOSAR PDF files to verify end-to-end functionality.

Performance optimization: Tests use session-scoped fixtures defined in conftest.py
to cache parsed PDF data. Each PDF is parsed only once per test session, with
results shared across all tests that need them.
"""

import os

import pytest

from autosar_pdf2txt.models import AutosarClass, AutosarDoc


# Import helper functions from conftest
from tests.integration.conftest import (
    find_first_class,
)


class TestPdfIntegration:
    """Integration tests using real AUTOSAR PDF files.

    These tests require actual PDF files to be present in the examples/pdf directory.
    Tests are skipped if files are not available (for CI/CD environments).
    """

    def test_parse_real_autosar_pdf_and_verify_autosar_and_sw_component_type(
        self, bsw_template_pdf: AutosarDoc, generic_structure_sw_component_type: AutosarClass
    ) -> None:
        """Test parsing real AUTOSAR PDF files and verify AUTOSAR and SwComponentType classes.

        SWIT_00001: Test Parsing Real AUTOSAR PDF and Verifying AUTOSAR and SwComponentType Classes

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00006: Package Hierarchy Building
            SWR_PARSER_00009: Proper Word Spacing in PDF Text Extraction
            SWR_PARSER_00010: Attribute Extraction from PDF
            SWR_MODEL_00001: AUTOSAR Class Representation
            SWR_MODEL_00010: AUTOSAR Attribute Representation
            SWR_MODEL_00023: AUTOSAR Document Model

        Args:
            bsw_template_pdf: Cached parsed BSW Module Template PDF data (AutosarDoc).
            generic_structure_sw_component_type: Cached SwComponentType class from GenericStructureTemplate PDF.
        """
        # ========== Verify AUTOSAR class from BSW Module Template PDF ==========
        packages = bsw_template_pdf.packages

        # Verify we got some packages
        assert len(packages) > 0, "Should extract at least one package from PDF"

        # Find the first class with actual data (using cached helper)
        first_package, autosar_class = find_first_class(packages)

        assert autosar_class is not None, "Should find at least one class in the PDF"
        assert first_package is not None, "Should find the package containing the class"

        # Verify the AUTOSAR class details
        assert autosar_class.name == "AUTOSAR", f"Expected class name 'AUTOSAR', got '{autosar_class.name}'"
        assert autosar_class.is_abstract is False, "AUTOSAR class should not be abstract"
        assert first_package.name == "AutosarTopLevelStructure", f"Expected package 'AutosarTopLevelStructure', got '{first_package.name}'"

        # Verify bases - should have one base class
        assert len(autosar_class.bases) == 1, f"Expected 1 base class, got {len(autosar_class.bases)}"
        assert "ARObject" in autosar_class.bases, f"Expected 'ARObject' in bases, got {autosar_class.bases}"

        # Verify note - should have a note
        assert autosar_class.note is not None, "AUTOSAR class should have a note"
        assert len(autosar_class.note) > 0, "Note should not be empty"
        assert "AUTOSAR" in autosar_class.note or "Rootelement" in autosar_class.note, \
            f"Note should contain AUTOSAR or Rootelement, got: '{autosar_class.note}'"

        # Print AUTOSAR class information for verification
        print("\n=== AUTOSAR class verified ===")
        print(f"  Name: {autosar_class.name}")
        print(f"  Abstract: {autosar_class.is_abstract}")
        print(f"  Bases: {autosar_class.bases}")
        print(f"  Note: {autosar_class.note}")
        print(f"  Package: {first_package.name}")

        # ========== Verify SwComponentType class from GenericStructureTemplate PDF ==========
        sw_component_type = generic_structure_sw_component_type

        # Verify class name
        assert sw_component_type.name == "SwComponentType", \
            f"Expected class name 'SwComponentType', got '{sw_component_type.name}'"

        # Verify package name is M2::AUTOSARTemplates::SWComponentTemplate::Components
        expected_package = "M2::AUTOSARTemplates::SWComponentTemplate::Components"
        assert sw_component_type.package == expected_package, \
            f"Expected package '{expected_package}', got '{sw_component_type.package}'"

        # Verify note
        assert sw_component_type.note is not None, "SwComponentType should have a note"
        assert len(sw_component_type.note) > 0, "Note should not be empty"
        assert sw_component_type.note == "Base class for AUTOSAR software components.", \
            f"Expected note 'Base class for AUTOSAR software components.', got '{sw_component_type.note}'"

        # Verify base list
        expected_bases = [
            "ARElement", "ARObject", "AtpBlueprint", "AtpBlueprintable", "AtpClassifier",
            "AtpType", "CollectableElement", "Identifiable", "MultilanguageReferrable",
            "PackageableElement", "Referrable"
        ]
        assert len(sw_component_type.bases) == len(expected_bases), \
            f"Expected {len(expected_bases)} base classes, got {len(sw_component_type.bases)}"
        for base in expected_bases:
            assert base in sw_component_type.bases, \
                f"Expected '{base}' in bases, got {sw_component_type.bases}"

        # Verify attribute list
        # Note: Multi-line attributes have truncated names due to SWR_PARSER_00012 filtering
        expected_attributes = [
            "consistency", "port", "portGroup", "swcMapping", "swComponent", "unitGroup"
        ]
        assert len(sw_component_type.attributes) == len(expected_attributes), \
            f"Expected {len(expected_attributes)} attributes, got {len(sw_component_type.attributes)}"
        for attr_name in expected_attributes:
            assert attr_name in sw_component_type.attributes, \
                f"Expected attribute '{attr_name}' not found. Got: {list(sw_component_type.attributes.keys())}"

        # Verify swcMapping attribute kind is "ref" and is_ref is true
        swc_mapping = sw_component_type.attributes.get("swcMapping")
        assert swc_mapping is not None, "swcMapping attribute should exist"
        assert swc_mapping.kind.value == "ref", \
            f"Expected swcMapping kind to be 'ref', got '{swc_mapping.kind.value}'"
        assert swc_mapping.is_ref is True, \
            f"Expected swcMapping is_ref to be True, got {swc_mapping.is_ref}"

        # Verify attribute types match expected values
        expected_types = {
            "consistency": "ConsistencyNeeds",
            "port": "PortPrototype",
            "portGroup": "PortGroup",
            "swcMapping": "SwComponentMapping",
            "swComponent": "SwComponent",
            "unitGroup": "UnitGroup"
        }
        for attr_name, expected_type in expected_types.items():
            attr = sw_component_type.attributes.get(attr_name)
            assert attr is not None, f"Attribute '{attr_name}' should exist"
            assert attr.type == expected_type, \
                f"Expected attribute '{attr_name}' to have type '{expected_type}', got '{attr.type}'"

        # Verify attribute notes exist
        attrs_with_notes = [name for name, attr in sw_component_type.attributes.items() if attr.note]
        assert len(attrs_with_notes) > 0, "At least one attribute should have a note"

        # Print SwComponentType class information for verification
        print("\n=== SwComponentType class verified ===")
        print(f"  Name: {sw_component_type.name}")
        print(f"  Package: {sw_component_type.package}")
        print(f"  Abstract: {sw_component_type.is_abstract}")
        print(f"  Bases ({len(sw_component_type.bases)}): {', '.join(sw_component_type.bases)}")
        print(f"  Note: {sw_component_type.note}")
        print(f"  Attributes ({len(sw_component_type.attributes)}):")
        for attr_name, attr in sw_component_type.attributes.items():
            print(f"    - {attr_name}: {attr.type} (ref: {attr.is_ref}, kind: {attr.kind.value})")

    def test_parse_timing_extensions_pdf_and_verify_class_list(
        self, timing_extensions_pdf: AutosarDoc
    ) -> None:
        """Test parsing TimingExtensions PDF and verify complete class list.

        SWIT_00002: Test Parsing TimingExtensions PDF and Verifying Class List

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00006: Package Hierarchy Building
            SWR_MODEL_00001: AUTOSAR Class Representation
            SWR_MODEL_00023: AUTOSAR Document Model

        Args:
            timing_extensions_pdf: Cached parsed TimingExtensions PDF data (AutosarDoc).
        """
        # Read expected class list from file
        class_list_file = "tests/integration/timing_extensions_class_list.txt"

        if not os.path.exists(class_list_file):
            pytest.skip(f"Class list file not found: {class_list_file}")

        expected_classes = set()
        with open(class_list_file, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    expected_classes.add(line)

        # Verify expected count from file header
        expected_count = 148
        assert len(expected_classes) == expected_count, \
            f"Expected {expected_count} classes in file, found {len(expected_classes)}"

        # Extract all class names from parsed PDF
        extracted_classes = set()
        packages = timing_extensions_pdf.packages

        # Collect all classes, enumerations, and primitives recursively
        def collect_types(pkg) -> set:
            """Recursively collect all type names from a package."""
            types = set()
            for typ in pkg.types:
                types.add(typ.name)
            for subpkg in pkg.subpackages:
                types.update(collect_types(subpkg))
            return types

        for pkg in packages:
            extracted_classes.update(collect_types(pkg))

        # Verify total number of classes
        actual_count = len(extracted_classes)
        assert actual_count == expected_count, \
            f"Expected {expected_count} classes, but found {actual_count}"

        # Verify all expected classes are present
        missing_classes = expected_classes - extracted_classes
        assert not missing_classes, \
            f"Missing {len(missing_classes)} classes: {sorted(missing_classes)}"

        # Verify no extra classes were extracted
        extra_classes = extracted_classes - expected_classes
        assert not extra_classes, \
            f"Found {len(extra_classes)} unexpected classes: {sorted(extra_classes)}"

        # Print summary for verification
        print(f"\n=== TimingExtensions PDF verification ===")
        print(f"  Expected classes: {expected_count}")
        print(f"  Extracted classes: {actual_count}")
        print(f"  All expected classes found: YES")
        print(f"  Sample classes: {sorted(list(extracted_classes))[:10]}...")
