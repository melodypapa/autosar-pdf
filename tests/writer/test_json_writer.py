"""Tests for JsonWriter class."""

import json
import pytest

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

    def test_error_when_both_output_path_and_base_dir(self, tmp_path):
        """Test error when both output_path and base_dir are specified.

        Requirements:
            SWR_WRITER_00011: JSON Directory Structure Creation
        """
        from autosar_pdf2txt.models import AutosarClass

        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass("TestClass", "TestPackage", False))

        with pytest.raises(ValueError, match="Cannot specify both output_path and base_dir"):
            writer.write_packages_to_files([pkg], output_path=str(tmp_path / "output.json"), base_dir=str(tmp_path))

    def test_error_when_neither_output_path_nor_base_dir(self):
        """Test error when neither output_path nor base_dir is specified.

        Requirements:
            SWR_WRITER_00011: JSON Directory Structure Creation
        """
        from autosar_pdf2txt.models import AutosarClass

        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass("TestClass", "TestPackage", False))

        with pytest.raises(ValueError, match="Must specify either output_path or base_dir"):
            writer.write_packages_to_files([pkg])

    def test_error_when_empty_output_path(self):
        """Test error when output_path is empty.

        Requirements:
            SWR_WRITER_00011: JSON Directory Structure Creation
        """
        from autosar_pdf2txt.models import AutosarClass

        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass("TestClass", "TestPackage", False))

        with pytest.raises(ValueError, match="output_path cannot be empty"):
            writer.write_packages_to_files([pkg], output_path="")

    def test_error_when_empty_base_dir(self):
        """Test error when base_dir is empty.

        Requirements:
            SWR_WRITER_00011: JSON Directory Structure Creation
        """
        from autosar_pdf2txt.models import AutosarClass

        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass("TestClass", "TestPackage", False))

        with pytest.raises(ValueError, match="base_dir cannot be empty"):
            writer.write_packages_to_files([pkg], base_dir="")

    def test_write_packages_with_output_path(self, tmp_path):
        """Test write_packages_to_files with output_path parameter.

        Requirements:
            SWR_WRITER_00011: JSON Directory Structure Creation
        """
        from autosar_pdf2txt.models import AutosarClass

        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass("TestClass", "TestPackage", False))

        output_file = tmp_path / "custom_index.json"
        writer.write_packages_to_files([pkg], output_path=output_file)

        # Verify custom index file was created
        assert output_file.exists()
        assert (tmp_path / "packages").exists()

    def test_sanitize_filename_with_special_chars(self):
        """Test filename sanitization with special characters.

        Requirements:
            SWR_WRITER_00012: JSON File Naming and Sanitization
        """
        writer = JsonWriter()

        # Test various special characters
        assert writer._sanitize_filename("M2::AUTOSAR::DataTypes") == "M2_AUTOSAR_DataTypes"
        assert writer._sanitize_filename("Test<>Class") == "Test_Class"
        assert writer._sanitize_filename('Test"Class') == "Test_Class"
        assert writer._sanitize_filename("Test/Class") == "Test_Class"
        assert writer._sanitize_filename("Test\\Class") == "Test_Class"
        assert writer._sanitize_filename("Test|Class") == "Test_Class"
        assert writer._sanitize_filename("Test?Class") == "Test_Class"
        assert writer._sanitize_filename("Test*Class") == "Test_Class"
        assert writer._sanitize_filename("Test:Class") == "Test_Class"

    def test_serialize_atp_type_none(self):
        """Test ATP type serialization for NONE.

        Requirements:
            SWR_WRITER_00016: JSON ATP Type Encoding
        """
        from autosar_pdf2txt.models.enums import ATPType

        writer = JsonWriter()
        assert writer._serialize_atp_type(ATPType.NONE) is None

    def test_serialize_atp_type_variation(self):
        """Test ATP type serialization for VARIATION.

        Requirements:
            SWR_WRITER_00016: JSON ATP Type Encoding
        """
        from autosar_pdf2txt.models.enums import ATPType

        writer = JsonWriter()
        assert writer._serialize_atp_type(ATPType.ATP_VARIATION) == "atpVariation"

    def test_serialize_atp_type_mixed_string(self):
        """Test ATP type serialization for MIXED_STRING.

        Requirements:
            SWR_WRITER_00016: JSON ATP Type Encoding
        """
        from autosar_pdf2txt.models.enums import ATPType

        writer = JsonWriter()
        assert writer._serialize_atp_type(ATPType.ATP_MIXED_STRING) == "atpMixedString"

    def test_serialize_atp_type_mixed(self):
        """Test ATP type serialization for MIXED.

        Requirements:
            SWR_WRITER_00016: JSON ATP Type Encoding
        """
        from autosar_pdf2txt.models.enums import ATPType

        writer = JsonWriter()
        assert writer._serialize_atp_type(ATPType.ATP_MIXED) == "atpMixed"

    def test_serialize_atp_type_proto(self):
        """Test ATP type serialization for PROTO.

        Requirements:
            SWR_WRITER_00016: JSON ATP Type Encoding
        """
        from autosar_pdf2txt.models.enums import ATPType

        writer = JsonWriter()
        assert writer._serialize_atp_type(ATPType.ATP_PROTO) == "atpPrototype"

    def test_serialize_class_with_all_fields(self, tmp_path):
        """Test class serialization with all fields including inheritance.

        Requirements:
            SWR_WRITER_00015: JSON Class Serialization
            SWR_WRITER_00019: JSON Inheritance Hierarchy Encoding
        """
        from autosar_pdf2txt.models import AutosarClass, AutosarAttribute, AttributeKind, AutosarDocumentSource, ATPType

        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(
            "TestClass",
            "TestPackage",
            is_abstract=True,
            atp_type=ATPType.ATP_VARIATION,
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
        cls.bases = ["BaseClass1", "BaseClass2"]
        cls.parent = "BaseClass1"
        cls.children = ["ChildClass1", "ChildClass2"]
        cls.subclasses = ["SubClass1", "SubClass2"]
        cls.aggregated_by = ["AggregatorClass"]
        cls.implements = ["Interface1", "Interface2"]
        cls.implemented_by = ["ImplementationClass"]
        cls.sources = [
            AutosarDocumentSource("test.pdf", 42, "AUTOSAR", "R22-11")
        ]
        pkg.add_class(cls)

        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify classes file was created
        classes_file = tmp_path / "packages" / "TestPackage.classes.json"
        assert classes_file.exists()

        # Verify class structure with all fields
        with open(classes_file) as f:
            data = json.load(f)

        cls_data = data["classes"][0]
        assert cls_data["name"] == "TestClass"
        assert cls_data["is_abstract"] is True
        assert cls_data["atp_type"] == "atpVariation"
        assert cls_data["note"] == "Test class note"
        assert cls_data["bases"] == ["BaseClass1", "BaseClass2"]
        assert cls_data["parent"] == "BaseClass1"
        assert cls_data["children"] == ["ChildClass1", "ChildClass2"]
        assert cls_data["subclasses"] == ["SubClass1", "SubClass2"]
        assert cls_data["aggregated_by"] == ["AggregatorClass"]
        assert cls_data["implements"] == ["Interface1", "Interface2"]
        assert cls_data["implemented_by"] == ["ImplementationClass"]
        assert len(cls_data["sources"]) == 1
        assert cls_data["sources"][0]["pdf_file"] == "test.pdf"
        assert cls_data["sources"][0]["page_number"] == 42
        assert cls_data["sources"][0]["autosar_standard"] == "AUTOSAR"
        assert cls_data["sources"][0]["standard_release"] == "R22-11"

    def test_pluralize_attribute_name_single(self):
        """Test attribute name pluralization for single multiplicity.

        Requirements:
            SWR_WRITER_00018: JSON Attribute Encoding
        """
        writer = JsonWriter()

        # Single multiplicity - no pluralization
        assert writer._pluralize_attribute_name("entry", "0..1") == "entry"
        assert writer._pluralize_attribute_name("entry", "1") == "entry"
        assert writer._pluralize_attribute_name("box", "0..1") == "box"

    def test_pluralize_attribute_name_multiple(self):
        """Test attribute name pluralization for multiple multiplicity.

        Requirements:
            SWR_WRITER_00018: JSON Attribute Encoding
        """
        writer = JsonWriter()

        # Multiple multiplicity - pluralize
        assert writer._pluralize_attribute_name("entry", "*") == "entries"
        assert writer._pluralize_attribute_name("entry", "2..*") == "entries"
        assert writer._pluralize_attribute_name("entry", "2") == "entries"
        assert writer._pluralize_attribute_name("entry", "2..5") == "entries"
        assert writer._pluralize_attribute_name("box", "*") == "boxes"
        assert writer._pluralize_attribute_name("test", "*") == "tests"

    def test_pluralize_attribute_name_special_rules(self):
        """Test attribute name pluralization with special rules.

        Requirements:
            SWR_WRITER_00018: JSON Attribute Encoding
        """
        writer = JsonWriter()

        # Special pluralization rules
        assert writer._pluralize_attribute_name("entry", "*") == "entries"  # y -> ies
        assert writer._pluralize_attribute_name("box", "*") == "boxes"  # x -> boxes
        assert writer._pluralize_attribute_name("test", "*") == "tests"  # default +s
        assert writer._pluralize_attribute_name("day", "*") == "days"  # ay -> days (no change)
        assert writer._pluralize_attribute_name("key", "*") == "keys"  # ey -> keys (no change)

    def test_serialize_attribute_ref_kind(self, tmp_path):
        """Test attribute serialization with REF kind.

        Requirements:
            SWR_WRITER_00018: JSON Attribute Encoding
        """
        from autosar_pdf2txt.models import AutosarClass, AutosarAttribute, AttributeKind

        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass("TestClass", "TestPackage", False)
        cls.attributes = {
            "ref_attr": AutosarAttribute(
                "ref_attr",
                "RefClass",
                is_ref=True,
                multiplicity="1",
                kind=AttributeKind.REF,
                note="Reference attribute"
            )
        }
        pkg.add_class(cls)

        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify classes file was created
        classes_file = tmp_path / "packages" / "TestPackage.classes.json"
        assert classes_file.exists()

        # Verify attribute with REF kind
        with open(classes_file) as f:
            data = json.load(f)

        attr_data = data["classes"][0]["attributes"]["ref_attr"]
        assert attr_data["kind"] == "reference"
        assert attr_data["is_ref"] is True

    def test_serialize_primitive_with_all_fields(self, tmp_path):
        """Test primitive serialization with all fields.

        Requirements:
            SWR_WRITER_00021: JSON Primitive Serialization
        """
        from autosar_pdf2txt.models import AutosarPrimitive, AutosarAttribute, AttributeKind, AutosarDocumentSource

        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        prim = AutosarPrimitive("Limit", "TestPackage", note="Test primitive note")
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
        prim.sources = [
            AutosarDocumentSource("test.pdf", 50, "AUTOSAR", "R22-11")
        ]
        pkg.add_type(prim)

        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify primitives file was created
        primitives_file = tmp_path / "packages" / "TestPackage.primitives.json"
        assert primitives_file.exists()

        # Verify primitive structure with all fields
        with open(primitives_file) as f:
            data = json.load(f)

        prim_data = data["primitives"][0]
        assert prim_data["name"] == "Limit"
        assert prim_data["note"] == "Test primitive note"
        assert len(prim_data["sources"]) == 1
        assert prim_data["sources"][0]["pdf_file"] == "test.pdf"
        assert prim_data["sources"][0]["page_number"] == 50
        assert prim_data["sources"][0]["autosar_standard"] == "AUTOSAR"
        assert prim_data["sources"][0]["standard_release"] == "R22-11"

    def test_serialize_enumeration_literal_without_tags(self, tmp_path):
        """Test enumeration literal serialization without tags.

        Requirements:
            SWR_WRITER_00020: JSON Enumeration Serialization
        """
        from autosar_pdf2txt.models import AutosarEnumeration, AutosarEnumLiteral

        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        enum = AutosarEnumeration(
            "TestEnum",
            "TestPackage",
            enumeration_literals=[
                AutosarEnumLiteral("VALUE1", index=0, description="First value"),
                AutosarEnumLiteral("VALUE2", index=1, description="Second value")
            ]
        )
        pkg.add_type(enum)

        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify enums file was created
        enums_file = tmp_path / "packages" / "TestPackage.enums.json"
        assert enums_file.exists()

        # Verify enumeration literals without tags
        with open(enums_file) as f:
            data = json.load(f)

        lit1 = data["enumerations"][0]["literals"][0]
        assert lit1["description"] == "First value"
        assert "Tags:" not in lit1["description"]

    def test_serialize_enumeration_with_all_fields(self, tmp_path):
        """Test enumeration serialization with all fields.

        Requirements:
            SWR_WRITER_00020: JSON Enumeration Serialization
        """
        from autosar_pdf2txt.models import AutosarEnumeration, AutosarEnumLiteral, AutosarDocumentSource

        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        enum = AutosarEnumeration(
            "TestEnum",
            "TestPackage",
            note="Test enumeration note",
            enumeration_literals=[
                AutosarEnumLiteral("VALUE1", index=0, description="First value")
            ]
        )
        enum.sources = [
            AutosarDocumentSource("test.pdf", 55, "AUTOSAR", "R22-11")
        ]
        pkg.add_type(enum)

        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify enums file was created
        enums_file = tmp_path / "packages" / "TestPackage.enums.json"
        assert enums_file.exists()

        # Verify enumeration with all fields
        with open(enums_file) as f:
            data = json.load(f)

        enum_data = data["enumerations"][0]
        assert enum_data["name"] == "TestEnum"
        assert enum_data["note"] == "Test enumeration note"
        assert len(enum_data["sources"]) == 1
        assert enum_data["sources"][0]["pdf_file"] == "test.pdf"
        assert enum_data["sources"][0]["page_number"] == 55
        assert enum_data["sources"][0]["autosar_standard"] == "AUTOSAR"
        assert enum_data["sources"][0]["standard_release"] == "R22-11"
