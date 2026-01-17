"""Tests for AutosarAttribute, AutosarClass and AutosarPackage models.

Test coverage for autosar_models.py targeting 100%.
"""

import pytest

from autosar_pdf2txt.models import AutosarAttribute, AutosarClass, AutosarPackage


class TestAutosarAttribute:
    """Tests for AutosarAttribute class.

    Requirements:
        SWR_MODEL_00010: AUTOSAR Attribute Representation
        SWR_MODEL_00011: AUTOSAR Attribute Name Validation
        SWR_MODEL_00012: AUTOSAR Attribute Type Validation
        SWR_MODEL_00013: AUTOSAR Attribute String Representation
    """

    def test_init_reference_attribute(self) -> None:
        """Test creating a reference type attribute.

        Requirements:
            SWR_MODEL_00010: AUTOSAR Attribute Representation
        """
        attr = AutosarAttribute(name="dataReadPort", type="PPortPrototype", is_ref=True)
        assert attr.name == "dataReadPort"
        assert attr.type == "PPortPrototype"
        assert attr.is_ref is True

    def test_init_non_reference_attribute(self) -> None:
        """Test creating a non-reference type attribute.

        Requirements:
            SWR_MODEL_00010: AUTOSAR Attribute Representation
        """
        attr = AutosarAttribute(name="id", type="uint32", is_ref=False)
        assert attr.name == "id"
        assert attr.type == "uint32"
        assert attr.is_ref is False

    def test_post_init_valid_name(self) -> None:
        """Test valid name validation.

        Requirements:
            SWR_MODEL_00011: AUTOSAR Attribute Name Validation
        """
        attr = AutosarAttribute(name="validAttribute", type="string", is_ref=False)
        assert attr.name == "validAttribute"

    def test_post_init_empty_name(self) -> None:
        """Test empty name raises ValueError.

        Requirements:
            SWR_MODEL_00011: AUTOSAR Attribute Name Validation
        """
        with pytest.raises(ValueError, match="Attribute name cannot be empty"):
            AutosarAttribute(name="", type="string", is_ref=False)

    def test_post_init_whitespace_name(self) -> None:
        """Test whitespace-only name raises ValueError.

        Requirements:
            SWR_MODEL_00011: AUTOSAR Attribute Name Validation
        """
        with pytest.raises(ValueError, match="Attribute name cannot be empty"):
            AutosarAttribute(name="   ", type="string", is_ref=False)

    def test_post_init_valid_type(self) -> None:
        """Test valid type validation.

        Requirements:
            SWR_MODEL_00012: AUTOSAR Attribute Type Validation
        """
        attr = AutosarAttribute(name="attr", type="ValidType", is_ref=False)
        assert attr.type == "ValidType"

    def test_post_init_empty_type(self) -> None:
        """Test empty type raises ValueError.

        Requirements:
            SWR_MODEL_00012: AUTOSAR Attribute Type Validation
        """
        with pytest.raises(ValueError, match="Attribute type cannot be empty"):
            AutosarAttribute(name="attr", type="", is_ref=False)

    def test_post_init_whitespace_type(self) -> None:
        """Test whitespace-only type raises ValueError.

        Requirements:
            SWR_MODEL_00012: AUTOSAR Attribute Type Validation
        """
        with pytest.raises(ValueError, match="Attribute type cannot be empty"):
            AutosarAttribute(name="attr", type="   ", is_ref=False)

    def test_str_reference_attribute(self) -> None:
        """Test string representation of reference attribute.

        Requirements:
            SWR_MODEL_00013: AUTOSAR Attribute String Representation
        """
        attr = AutosarAttribute(name="port", type="PPortPrototype", is_ref=True)
        assert str(attr) == "port: PPortPrototype (ref)"

    def test_str_non_reference_attribute(self) -> None:
        """Test string representation of non-reference attribute.

        Requirements:
            SWR_MODEL_00013: AUTOSAR Attribute String Representation
        """
        attr = AutosarAttribute(name="value", type="uint32", is_ref=False)
        assert str(attr) == "value: uint32"

    def test_repr(self) -> None:
        """Test __repr__ method.

        Requirements:
            SWR_MODEL_00013: AUTOSAR Attribute String Representation
        """
        attr = AutosarAttribute(name="testAttr", type="TestType", is_ref=True)
        result = repr(attr)
        assert "AutosarAttribute" in result
        assert "name='testAttr'" in result
        assert "type='TestType'" in result
        assert "is_ref=True" in result


class TestAutosarClass:
    """Tests for AutosarClass class.

    Requirements:
        SWR_MODEL_00001: AUTOSAR Class Representation
        SWR_MODEL_00002: AUTOSAR Class Name Validation
        SWR_MODEL_00003: AUTOSAR Class String Representation
    """

    def test_init_concrete_class(self) -> None:
        """Test creating a concrete class.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(name="RunnableEntity", is_abstract=False)
        assert cls.name == "RunnableEntity"
        assert cls.is_abstract is False

    def test_init_abstract_class(self) -> None:
        """Test creating an abstract class.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(name="InternalBehavior", is_abstract=True)
        assert cls.name == "InternalBehavior"
        assert cls.is_abstract is True

    def test_post_init_valid_name(self) -> None:
        """Test valid name validation.

        Requirements:
            SWR_MODEL_00002: AUTOSAR Class Name Validation
        """
        cls = AutosarClass(name="ValidClass", is_abstract=False)
        assert cls.name == "ValidClass"

    def test_post_init_empty_name(self) -> None:
        """Test empty name raises ValueError.

        Requirements:
            SWR_MODEL_00002: AUTOSAR Class Name Validation
        """
        with pytest.raises(ValueError, match="Class name cannot be empty"):
            AutosarClass(name="", is_abstract=False)

    def test_post_init_whitespace_name(self) -> None:
        """Test whitespace-only name raises ValueError.

        Requirements:
            SWR_MODEL_00002: AUTOSAR Class Name Validation
        """
        with pytest.raises(ValueError, match="Class name cannot be empty"):
            AutosarClass(name="   ", is_abstract=False)

    def test_str_concrete_class(self) -> None:
        """Test string representation of concrete class.

        Requirements:
            SWR_MODEL_00003: AUTOSAR Class String Representation
        """
        cls = AutosarClass(name="MyClass", is_abstract=False)
        assert str(cls) == "MyClass"

    def test_str_abstract_class(self) -> None:
        """Test string representation of abstract class.

        Requirements:
            SWR_MODEL_00003: AUTOSAR Class String Representation
        """
        cls = AutosarClass(name="AbstractClass", is_abstract=True)
        assert str(cls) == "AbstractClass (abstract)"

    def test_repr(self) -> None:
        """Test __repr__ method.

        Requirements:
            SWR_MODEL_00003: AUTOSAR Class String Representation
        """
        cls = AutosarClass(name="TestClass", is_abstract=True)
        result = repr(cls)
        assert "AutosarClass" in result
        assert "name='TestClass'" in result
        assert "is_abstract=True" in result

    def test_init_with_empty_attributes(self) -> None:
        """Test creating a class with empty attributes dictionary.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(name="Component", is_abstract=False)
        assert cls.attributes == {}
        assert len(cls.attributes) == 0

    def test_init_with_attributes(self) -> None:
        """Test creating a class with attributes.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        attr1 = AutosarAttribute(name="dataReadPort", type="PPortPrototype", is_ref=True)
        attr2 = AutosarAttribute(name="id", type="uint32", is_ref=False)
        cls = AutosarClass(
            name="Component",
            is_abstract=False,
            attributes={"dataReadPort": attr1, "id": attr2}
        )
        assert len(cls.attributes) == 2
        assert "dataReadPort" in cls.attributes
        assert "id" in cls.attributes
        assert cls.attributes["dataReadPort"] == attr1
        assert cls.attributes["id"] == attr2

    def test_repr_with_attributes(self) -> None:
        """Test __repr__ method shows attributes count.

        Requirements:
            SWR_MODEL_00003: AUTOSAR Class String Representation
        """
        attr1 = AutosarAttribute(name="port", type="PPortPrototype", is_ref=True)
        attr2 = AutosarAttribute(name="value", type="uint32", is_ref=False)
        cls = AutosarClass(
            name="Component",
            is_abstract=False,
            attributes={"port": attr1, "value": attr2}
        )
        result = repr(cls)
        assert "AutosarClass" in result
        assert "name='Component'" in result
        assert "is_abstract=False" in result
        assert "attributes=2" in result

    def test_repr_without_attributes(self) -> None:
        """Test __repr__ method with no attributes.

        Requirements:
            SWR_MODEL_00003: AUTOSAR Class String Representation
        """
        cls = AutosarClass(name="Component", is_abstract=False)
        result = repr(cls)
        assert "AutosarClass" in result
        assert "name='Component'" in result
        assert "is_abstract=False" in result
        assert "attributes=0" in result
        assert "bases=0" in result
        assert "note=False" in result

    def test_init_with_empty_bases(self) -> None:
        """Test creating a class with empty bases list (default).

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(name="MyClass", is_abstract=False)
        assert cls.bases == []
        assert len(cls.bases) == 0

    def test_init_with_bases(self) -> None:
        """Test creating a class with base classes.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(
            name="DerivedClass",
            is_abstract=False,
            bases=["BaseClass1", "BaseClass2"]
        )
        assert len(cls.bases) == 2
        assert "BaseClass1" in cls.bases
        assert "BaseClass2" in cls.bases

    def test_init_with_single_base(self) -> None:
        """Test creating a class with single base class.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(
            name="DerivedClass",
            is_abstract=False,
            bases=["BaseClass"]
        )
        assert len(cls.bases) == 1
        assert cls.bases[0] == "BaseClass"

    def test_repr_with_bases(self) -> None:
        """Test __repr__ includes bases count.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(
            name="DerivedClass",
            is_abstract=False,
            bases=["Base1", "Base2"]
        )
        result = repr(cls)
        assert "bases=2" in result

    def test_init_with_none_note(self) -> None:
        """Test creating a class with None note (default).

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(name="MyClass", is_abstract=False)
        assert cls.note is None

    def test_init_with_note(self) -> None:
        """Test creating a class with a note.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(
            name="MyClass",
            is_abstract=False,
            note="This is a documentation note"
        )
        assert cls.note == "This is a documentation note"

    def test_init_with_empty_note(self) -> None:
        """Test creating a class with empty string note.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(name="MyClass", is_abstract=False, note="")
        assert cls.note == ""

    def test_repr_with_note(self) -> None:
        """Test __repr__ includes note presence.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(
            name="MyClass",
            is_abstract=False,
            note="Documentation"
        )
        result = repr(cls)
        assert "note=True" in result

    def test_init_with_all_fields(self) -> None:
        """Test creating a class with all fields populated.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        attr = AutosarAttribute(name="port", type="PPortPrototype", is_ref=True)
        cls = AutosarClass(
            name="CompleteClass",
            is_abstract=False,
            attributes={"port": attr},
            bases=["Base1", "Base2"],
            note="Complete example"
        )
        assert cls.name == "CompleteClass"
        assert cls.is_abstract is False
        assert len(cls.attributes) == 1
        assert len(cls.bases) == 2
        assert cls.note == "Complete example"

    def test_bases_mutation(self) -> None:
        """Test that bases list can be mutated.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(name="MyClass", is_abstract=False)
        cls.bases.append("BaseClass")
        assert len(cls.bases) == 1
        assert "BaseClass" in cls.bases

    def test_note_reassignment(self) -> None:
        """Test that note can be reassigned.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(name="MyClass", is_abstract=False)
        cls.note = "Updated note"
        assert cls.note == "Updated note"


class TestAutosarPackage:
    """Tests for AutosarPackage class.

    Requirements:
        SWR_MODEL_00004: AUTOSAR Package Representation
        SWR_MODEL_00005: AUTOSAR Package Name Validation
        SWR_MODEL_00006: Add Class to Package
        SWR_MODEL_00007: Add Subpackage to Package
        SWR_MODEL_00008: Query Package Contents
        SWR_MODEL_00009: Package String Representation
    """

    def test_init_empty_package(self) -> None:
        """Test creating an empty package.

        Requirements:
            SWR_MODEL_00004: AUTOSAR Package Representation
        """
        pkg = AutosarPackage(name="TestPackage")
        assert pkg.name == "TestPackage"
        assert len(pkg.classes) == 0
        assert len(pkg.subpackages) == 0

    def test_init_with_classes(self) -> None:
        """Test creating a package with classes.

        Requirements:
            SWR_MODEL_00004: AUTOSAR Package Representation
        """
        cls1 = AutosarClass(name="Class1", is_abstract=False)
        cls2 = AutosarClass(name="Class2", is_abstract=True)
        pkg = AutosarPackage(name="TestPackage", classes=[cls1, cls2])
        assert len(pkg.classes) == 2
        assert pkg.classes[0].name == "Class1"
        assert pkg.classes[1].name == "Class2"

    def test_init_with_subpackages(self) -> None:
        """Test creating a package with subpackages.

        Requirements:
            SWR_MODEL_00004: AUTOSAR Package Representation
        """
        subpkg = AutosarPackage(name="SubPackage")
        pkg = AutosarPackage(name="TestPackage", subpackages=[subpkg])
        assert len(pkg.subpackages) == 1
        assert pkg.subpackages[0].name == "SubPackage"

    def test_post_init_valid_name(self) -> None:
        """Test valid name validation.

        Requirements:
            SWR_MODEL_00005: AUTOSAR Package Name Validation
        """
        pkg = AutosarPackage(name="ValidPackage")
        assert pkg.name == "ValidPackage"

    def test_post_init_empty_name(self) -> None:
        """Test empty name raises ValueError.

        Requirements:
            SWR_MODEL_00005: AUTOSAR Package Name Validation
        """
        with pytest.raises(ValueError, match="Package name cannot be empty"):
            AutosarPackage(name="")

    def test_post_init_whitespace_name(self) -> None:
        """Test whitespace-only name raises ValueError.

        Requirements:
            SWR_MODEL_00005: AUTOSAR Package Name Validation
        """
        with pytest.raises(ValueError, match="Package name cannot be empty"):
            AutosarPackage(name="   ")

    def test_add_class_success(self) -> None:
        """Test successfully adding a class.

        Requirements:
            SWR_MODEL_00006: Add Class to Package
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="NewClass", is_abstract=False)
        pkg.add_class(cls)
        assert len(pkg.classes) == 1
        assert pkg.classes[0] == cls

    def test_add_class_duplicate(self) -> None:
        """Test adding duplicate class raises ValueError.

        Requirements:
            SWR_MODEL_00006: Add Class to Package
        """
        pkg = AutosarPackage(name="TestPackage")
        cls1 = AutosarClass(name="DuplicateClass", is_abstract=False)
        cls2 = AutosarClass(name="DuplicateClass", is_abstract=True)
        pkg.add_class(cls1)
        with pytest.raises(ValueError, match="already exists"):
            pkg.add_class(cls2)

    def test_add_subpackage_success(self) -> None:
        """Test successfully adding a subpackage.

        Requirements:
            SWR_MODEL_00007: Add Subpackage to Package
        """
        pkg = AutosarPackage(name="ParentPackage")
        subpkg = AutosarPackage(name="ChildPackage")
        pkg.add_subpackage(subpkg)
        assert len(pkg.subpackages) == 1
        assert pkg.subpackages[0] == subpkg

    def test_add_subpackage_duplicate(self) -> None:
        """Test adding duplicate subpackage raises ValueError.

        Requirements:
            SWR_MODEL_00007: Add Subpackage to Package
        """
        pkg = AutosarPackage(name="ParentPackage")
        subpkg1 = AutosarPackage(name="DuplicateSub")
        subpkg2 = AutosarPackage(name="DuplicateSub")
        pkg.add_subpackage(subpkg1)
        with pytest.raises(ValueError, match="already exists"):
            pkg.add_subpackage(subpkg2)

    def test_get_class_found(self) -> None:
        """Test finding an existing class.

        Requirements:
            SWR_MODEL_00008: Query Package Contents
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="TargetClass", is_abstract=False)
        pkg.add_class(cls)
        result = pkg.get_class("TargetClass")
        assert result is not None
        assert result.name == "TargetClass"

    def test_get_class_not_found(self) -> None:
        """Test finding a non-existent class.

        Requirements:
            SWR_MODEL_00008: Query Package Contents
        """
        pkg = AutosarPackage(name="TestPackage")
        result = pkg.get_class("NonExistent")
        assert result is None

    def test_get_subpackage_found(self) -> None:
        """Test finding an existing subpackage.

        Requirements:
            SWR_MODEL_00008: Query Package Contents
        """
        pkg = AutosarPackage(name="ParentPackage")
        subpkg = AutosarPackage(name="TargetSub")
        pkg.add_subpackage(subpkg)
        result = pkg.get_subpackage("TargetSub")
        assert result is not None
        assert result.name == "TargetSub"

    def test_get_subpackage_not_found(self) -> None:
        """Test finding a non-existent subpackage.

        Requirements:
            SWR_MODEL_00008: Query Package Contents
        """
        pkg = AutosarPackage(name="ParentPackage")
        result = pkg.get_subpackage("NonExistent")
        assert result is None

    def test_has_class_true(self) -> None:
        """Test has_class returns True when class exists.

        Requirements:
            SWR_MODEL_00008: Query Package Contents
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="ExistingClass", is_abstract=False)
        pkg.add_class(cls)
        assert pkg.has_class("ExistingClass") is True

    def test_has_class_false(self) -> None:
        """Test has_class returns False when class doesn't exist.

        Requirements:
            SWR_MODEL_00008: Query Package Contents
        """
        pkg = AutosarPackage(name="TestPackage")
        assert pkg.has_class("NonExistent") is False

    def test_has_subpackage_true(self) -> None:
        """Test has_subpackage returns True when subpackage exists.

        Requirements:
            SWR_MODEL_00008: Query Package Contents
        """
        pkg = AutosarPackage(name="ParentPackage")
        subpkg = AutosarPackage(name="ExistingSub")
        pkg.add_subpackage(subpkg)
        assert pkg.has_subpackage("ExistingSub") is True

    def test_has_subpackage_false(self) -> None:
        """Test has_subpackage returns False when subpackage doesn't exist.

        Requirements:
            SWR_MODEL_00008: Query Package Contents
        """
        pkg = AutosarPackage(name="ParentPackage")
        assert pkg.has_subpackage("NonExistent") is False

    def test_str_package_with_classes_only(self) -> None:
        """Test string representation of package with only classes.

        Requirements:
            SWR_MODEL_00009: Package String Representation
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="Class1", is_abstract=False))
        pkg.add_class(AutosarClass(name="Class2", is_abstract=True))
        result = str(pkg)
        assert "TestPackage" in result
        assert "2 classes" in result

    def test_str_package_with_subpackages_only(self) -> None:
        """Test string representation of package with only subpackages.

        Requirements:
            SWR_MODEL_00009: Package String Representation
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_subpackage(AutosarPackage(name="Sub1"))
        pkg.add_subpackage(AutosarPackage(name="Sub2"))
        result = str(pkg)
        assert "TestPackage" in result
        assert "2 subpackages" in result

    def test_str_package_with_both(self) -> None:
        """Test string representation of package with both classes and subpackages.

        Requirements:
            SWR_MODEL_00009: Package String Representation
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="Class1", is_abstract=False))
        pkg.add_subpackage(AutosarPackage(name="Sub1"))
        result = str(pkg)
        assert "TestPackage" in result
        assert "1 classes" in result
        assert "1 subpackages" in result

    def test_str_empty_package(self) -> None:
        """Test string representation of empty package.

        Requirements:
            SWR_MODEL_00009: Package String Representation
        """
        pkg = AutosarPackage(name="EmptyPackage")
        result = str(pkg)
        assert "EmptyPackage" in result

    def test_repr(self) -> None:
        """Test __repr__ method.

        Requirements:
            SWR_MODEL_00009: Package String Representation
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="Class1", is_abstract=False))
        pkg.add_subpackage(AutosarPackage(name="Sub1"))
        result = repr(pkg)
        assert "AutosarPackage" in result
        assert "name='TestPackage'" in result
        assert "classes=1" in result
        assert "subpackages=1" in result

    def test_nested_packages(self) -> None:
        """Test nested package structure.

        Requirements:
            SWR_MODEL_00007: Add Subpackage to Package
            SWR_MODEL_00008: Query Package Contents
        """
        root = AutosarPackage(name="Root")
        child = AutosarPackage(name="Child")
        grandchild = AutosarPackage(name="Grandchild")

        root.add_subpackage(child)
        child.add_subpackage(grandchild)

        assert len(root.subpackages) == 1
        assert root.get_subpackage("Child") == child
        assert child.get_subpackage("Grandchild") == grandchild
