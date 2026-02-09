"""Tests for mapping writer.

Test coverage for mapping_writer.py.
"""

import json

from autosar_pdf2txt.models import (
    AutosarClass,
    AutosarEnumeration,
    AutosarPackage,
    AutosarPrimitive,
)
from autosar_pdf2txt.writer.mapping_writer import MappingWriter


class TestMappingWriter:
    """Tests for MappingWriter class.

    Requirements:
        SWR_WRITER_00024: Mapping Writer Initialization
        SWR_WRITER_00025: JSON Mapping Output Format
        SWR_WRITER_00026: Markdown Mapping Table Output
    """

    def test_init_default(self) -> None:
        """SWUT_WRITER_00058: Test initialization with default settings.

        Requirements:
            SWR_WRITER_00024: Mapping Writer Initialization
        """
        writer = MappingWriter()
        assert writer is not None

    def test_write_mapping_json_basic(self) -> None:
        """SWUT_WRITER_00059: Test writing mapping in JSON format with all type categories.

        Requirements:
            SWR_WRITER_00024: Mapping Writer Initialization
            SWR_WRITER_00025: JSON Mapping Output Format
        """
        # Create a package with all three types
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_type(AutosarClass(name="TestClass", package="M2::TestPackage", is_abstract=False))
        pkg.add_type(AutosarEnumeration(name="TestEnum", package="M2::TestPackage"))
        pkg.add_type(AutosarPrimitive(name="TestPrimitive", package="M2::TestPackage"))

        # Generate JSON mapping
        writer = MappingWriter()
        result = writer.write_mapping([pkg], format="json")

        # Parse JSON
        data = json.loads(result)

        # Verify structure
        assert "types" in data
        assert isinstance(data["types"], list)
        assert len(data["types"]) == 3

        # Verify each type entry has required fields
        for entry in data["types"]:
            assert "name" in entry
            assert "type" in entry
            assert "package_path" in entry

        # Verify type values
        type_names = {entry["name"]: entry["type"] for entry in data["types"]}
        assert type_names["TestClass"] == "Class"
        assert type_names["TestEnum"] == "Enumeration"
        assert type_names["TestPrimitive"] == "Primitive"

        # Verify package paths
        for entry in data["types"]:
            assert entry["package_path"] == "M2::TestPackage"

    def test_write_mapping_markdown_basic(self) -> None:
        """SWUT_WRITER_00060: Test writing mapping in Markdown table format.

        Requirements:
            SWR_WRITER_00024: Mapping Writer Initialization
            SWR_WRITER_00026: Markdown Mapping Table Output
        """
        # Create a package with all three types
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_type(AutosarClass(name="TestClass", package="M2::TestPackage", is_abstract=False))
        pkg.add_type(AutosarEnumeration(name="TestEnum", package="M2::TestPackage"))
        pkg.add_type(AutosarPrimitive(name="TestPrimitive", package="M2::TestPackage"))

        # Generate Markdown mapping
        writer = MappingWriter()
        result = writer.write_mapping([pkg], format="markdown")

        # Verify header
        assert "# Type to Package Mapping" in result

        # Verify table header
        assert "| Name | Type | Package Path |" in result

        # Verify table separator
        assert "|------|------|" in result

        # Verify all types are in the table
        assert "TestClass" in result
        assert "TestEnum" in result
        assert "TestPrimitive" in result

        # Verify type categories are in the table
        assert "Class" in result
        assert "Enumeration" in result
        assert "Primitive" in result

    def test_collect_mapping_empty_packages(self) -> None:
        """SWUT_WRITER_00062: Test collecting mapping from empty packages.

        Requirements:
            SWR_WRITER_00024: Mapping Writer Initialization
            SWR_WRITER_00025: JSON Mapping Output Format
            SWR_WRITER_00026: Markdown Mapping Table Output
        """
        # Create empty package
        pkg = AutosarPackage(name="EmptyPackage")

        # Test JSON format
        writer = MappingWriter()
        json_result = writer.write_mapping([pkg], format="json")
        data = json.loads(json_result)

        assert "types" in data
        assert len(data["types"]) == 0

        # Test Markdown format
        md_result = writer.write_mapping([pkg], format="markdown")

        # Verify header exists but no data rows
        assert "# Type to Package Mapping" in md_result
        assert "| Name | Type | Package Path |" in md_result
        # Should not have any data rows (lines starting with | that are not header/separator)
        lines = [line for line in md_result.split("\n") if line.startswith("|") and line.strip()]
        # Header + separator = 2 lines max
        assert len(lines) <= 2

    def test_collect_mapping_nested_packages(self) -> None:
        """SWUT_WRITER_00061: Test collecting mapping from nested packages.

        Requirements:
            SWR_WRITER_00024: Mapping Writer Initialization
            SWR_WRITER_00025: JSON Mapping Output Format
        """
        # Create parent package
        parent_pkg = AutosarPackage(name="ParentPackage")

        # Create child package
        child_pkg = AutosarPackage(name="ChildPackage")

        # Add class to parent package
        parent_pkg.add_type(AutosarClass(name="ParentClass", package="M2::ParentPackage", is_abstract=False))

        # Add class to child package
        child_pkg.add_type(AutosarClass(name="ChildClass", package="M2::ParentPackage::ChildPackage", is_abstract=False))

        # Add child package to parent
        parent_pkg.add_subpackage(child_pkg)

        # Generate JSON mapping
        writer = MappingWriter()
        result = writer.write_mapping([parent_pkg], format="json")
        data = json.loads(result)

        # Verify both classes are present
        assert len(data["types"]) == 2

        # Verify package paths
        type_paths = {entry["name"]: entry["package_path"] for entry in data["types"]}
        assert type_paths["ParentClass"] == "M2::ParentPackage"
        assert type_paths["ChildClass"] == "M2::ParentPackage::ChildPackage"
