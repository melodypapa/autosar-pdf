"""Tests for JsonWriter class."""

import json

from autosar_pdf2txt.writer import JsonWriter
from autosar_pdf2txt.models import AutosarPackage, AutosarClass


class TestJsonWriter:
    """Test cases for JsonWriter class.

    Requirements:
        SWR_WRITER_00010: JSON Writer Initialization
    """

    def test_init(self):
        """Test JsonWriter initialization.

        Requirements:
            SWR_WRITER_00010: JSON Writer Initialization
        """
        writer = JsonWriter()
        assert writer is not None

    def test_write_packages_to_files_creates_directories(self, tmp_path):
        """Test write_packages_to_files creates package directories.

        Requirements:
            SWR_WRITER_00011: JSON Directory Structure Creation
        """
        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass("TestClass", "TestPackage", False))

        # Write to temporary directory
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify packages directory was created
        packages_dir = tmp_path / "packages"
        assert packages_dir.exists()
        assert packages_dir.is_dir()

    def test_write_packages_to_files_creates_index(self, tmp_path):
        """Test write_packages_to_files creates index.json.

        Requirements:
            SWR_WRITER_00013: JSON Index File Output
        """

        writer = JsonWriter()
        pkg = AutosarPackage(name="M2")
        pkg.add_class(AutosarClass("TestClass", "M2::AUTOSAR", False))

        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify index.json was created
        index_file = tmp_path / "index.json"
        assert index_file.exists()

        # Verify index structure
        with open(index_file) as f:
            index = json.load(f)

        assert "version" in index
        assert index["version"] == "1.0"
        assert "metadata" in index
        assert "packages" in index

    def test_write_package_metadata_file(self, tmp_path):
        """Test package metadata JSON file has correct structure.

        Requirements:
            SWR_WRITER_00014: JSON Package Metadata File Output
        """

        writer = JsonWriter()
        pkg = AutosarPackage(name="M2::AUTOSAR::DataTypes")
        pkg.add_class(AutosarClass("TestClass", "M2::AUTOSAR::DataTypes", False))

        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify package file was created
        package_file = tmp_path / "packages" / "M2_AUTOSAR_DataTypes.json"
        assert package_file.exists()

        # Verify package structure
        with open(package_file) as f:
            data = json.load(f)

        assert data["name"] == "M2::AUTOSAR::DataTypes"
        assert data["path"] == "M2::AUTOSAR::DataTypes"
        assert "files" in data
        assert "summary" in data

    def test_write_classes_file(self, tmp_path):
        """Test classes JSON file with complete class data.

        Requirements:
            SWR_WRITER_00015: JSON Class Serialization
        """
        from autosar_pdf2txt.models import AutosarAttribute, AutosarDocumentSource, AttributeKind

        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(
            "TestClass",
            "TestPackage",
            is_abstract=False,
            note="Test class note"
        )
        cls.attributes = {
            "test_attr": AutosarAttribute(
                "test_attr",
                "String",
                False,
                "1",
                AttributeKind.ATTR,
                "Test attribute"
            )
        }
        cls.sources = [
            AutosarDocumentSource("test.pdf", 42, "AUTOSAR", "R22-11")
        ]
        pkg.add_class(cls)

        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify classes file was created
        classes_file = tmp_path / "packages" / "TestPackage.classes.json"
        assert classes_file.exists()

        # Verify class structure
        with open(classes_file) as f:
            data = json.load(f)

        assert data["package"] == "TestPackage"
        assert len(data["classes"]) == 1

        cls_data = data["classes"][0]
        assert cls_data["name"] == "TestClass"
        assert cls_data["is_abstract"] is False
        assert cls_data["note"] == "Test class note"
        assert "sources" in cls_data
        assert len(cls_data["sources"]) == 1
        assert cls_data["sources"][0]["pdf_file"] == "test.pdf"
        assert cls_data["sources"][0]["page_number"] == 42

    def test_write_enums_file(self, tmp_path):
        """Test enumerations JSON file with literal values.

        Requirements:
            SWR_WRITER_00020: JSON Enumeration Serialization
        """
        from autosar_pdf2txt.models import AutosarEnumeration, AutosarEnumLiteral, AutosarDocumentSource

        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        enum = AutosarEnumeration(
            "TestEnum",
            "TestPackage",
            enumeration_literals=[
                AutosarEnumLiteral("VALUE1", index=0, description="First value"),
                AutosarEnumLiteral("VALUE2", index=1, description="Second value<br>Tags: key=val")
            ]
        )
        enum.sources = [
            AutosarDocumentSource("test.pdf", 50, "AUTOSAR", "R22-11")
        ]
        pkg.add_type(enum)

        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify enums file was created
        enums_file = tmp_path / "packages" / "TestPackage.enums.json"
        assert enums_file.exists()

        # Verify enumeration structure
        with open(enums_file) as f:
            data = json.load(f)

        assert data["package"] == "TestPackage"
        assert len(data["enumerations"]) == 1

        enum_data = data["enumerations"][0]
        assert enum_data["name"] == "TestEnum"
        assert len(enum_data["literals"]) == 2

        # Check first literal
        lit1 = enum_data["literals"][0]
        assert lit1["name"] == "VALUE1"
        assert lit1["index"] == 0
        assert lit1["description"] == "First value"

        # Check second literal with merged tags
        lit2 = enum_data["literals"][1]
        assert lit2["name"] == "VALUE2"
        assert lit2["index"] == 1
        assert "Tags: key=val" in lit2["description"]

    def test_write_primitives_file(self, tmp_path):
        """Test primitives JSON file with attributes.

        Requirements:
            SWR_WRITER_00021: JSON Primitive Serialization
        """
        from autosar_pdf2txt.models import AutosarPrimitive, AutosarAttribute, AttributeKind

        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        prim = AutosarPrimitive("Limit", "TestPackage")
        prim.attributes = {
            "interval_type": AutosarAttribute(
                "interval_type",
                "String",
                False,
                "1",
                AttributeKind.ATTR,
                "Open or closed interval"
            )
        }
        pkg.add_type(prim)

        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify primitives file was created
        primitives_file = tmp_path / "packages" / "TestPackage.primitives.json"
        assert primitives_file.exists()

        # Verify primitive structure
        with open(primitives_file) as f:
            data = json.load(f)

        assert data["package"] == "TestPackage"
        assert len(data["primitives"]) == 1

        prim_data = data["primitives"][0]
        assert prim_data["name"] == "Limit"
        assert "attributes" in prim_data
        assert "interval_type" in prim_data["attributes"]
