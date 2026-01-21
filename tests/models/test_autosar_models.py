"""Tests for AutosarAttribute, AutosarClass, AutosarEnumeration, AutosarEnumLiteral, AutosarPackage, AutosarPrimitive and AbstractAutosarBase models.

Test coverage for autosar_models.py targeting 100%.
"""

import pytest

from autosar_pdf2txt.models import (
    ATPType,
    AttributeKind,
    AutosarAttribute,
    AutosarClass,
    AutosarEnumLiteral,
    AutosarEnumeration,
    AutosarPackage,
    AutosarPrimitive,
)


class TestAutosarEnumLiteral:
    """Tests for AutosarEnumLiteral class.

    Requirements:
        SWR_MODEL_00014: AUTOSAR Enumeration Literal Representation
        SWR_MODEL_00015: AUTOSAR Enumeration Literal Name Validation
        SWR_MODEL_00016: AUTOSAR Enumeration Literal String Representation
    """

    def test_init_with_all_fields(self) -> None:
        """Test initialization with all fields.

        Requirements:
            SWR_MODEL_00014: AUTOSAR Enumeration Literal Representation
        """
        literal = AutosarEnumLiteral(
            name="leafOfTargetContainer", index=0, description="Elements directly owned"
        )
        assert literal.name == "leafOfTargetContainer"
        assert literal.index == 0
        assert literal.description == "Elements directly owned"

    def test_init_with_name_only(self) -> None:
        """Test initialization with only name field.

        Requirements:
            SWR_MODEL_00014: AUTOSAR Enumeration Literal Representation
        """
        literal = AutosarEnumLiteral(name="targetContainer")
        assert literal.name == "targetContainer"
        assert literal.index is None
        assert literal.description is None

    def test_init_with_name_and_description(self) -> None:
        """Test initialization with name and description.

        Requirements:
            SWR_MODEL_00014: AUTOSAR Enumeration Literal Representation
        """
        literal = AutosarEnumLiteral(name="vertexOfTargetContainer", description="Nested elements")
        assert literal.name == "vertexOfTargetContainer"
        assert literal.description == "Nested elements"
        assert literal.index is None

    def test_init_with_name_and_index(self) -> None:
        """Test initialization with name and index.

        Requirements:
            SWR_MODEL_00014: AUTOSAR Enumeration Literal Representation
        """
        literal = AutosarEnumLiteral(name="VALUE1", index=1)
        assert literal.name == "VALUE1"
        assert literal.index == 1
        assert literal.description is None

    def test_post_init_valid_name(self) -> None:
        """Test valid name is accepted.

        Requirements:
            SWR_MODEL_00015: AUTOSAR Enumeration Literal Name Validation
        """
        literal = AutosarEnumLiteral(name="validLiteral")
        assert literal.name == "validLiteral"

    def test_post_init_empty_name(self) -> None:
        """Test empty name raises ValueError.

        Requirements:
            SWR_MODEL_00015: AUTOSAR Enumeration Literal Name Validation
        """
        with pytest.raises(ValueError, match="Enumeration literal name cannot be empty"):
            AutosarEnumLiteral(name="")

    def test_post_init_whitespace_name(self) -> None:
        """Test whitespace-only name raises ValueError.

        Requirements:
            SWR_MODEL_00015: AUTOSAR Enumeration Literal Name Validation
        """
        with pytest.raises(ValueError, match="Enumeration literal name cannot be empty"):
            AutosarEnumLiteral(name="   ")

    def test_str_without_index(self) -> None:
        """Test string representation without index.

        Requirements:
            SWR_MODEL_00016: AUTOSAR Enumeration Literal String Representation
        """
        literal = AutosarEnumLiteral(name="MyLiteral")
        assert str(literal) == "MyLiteral"

    def test_str_with_index(self) -> None:
        """Test string representation with index.

        Requirements:
            SWR_MODEL_00016: AUTOSAR Enumeration Literal String Representation
        """
        literal = AutosarEnumLiteral(name="MyLiteral", index=0)
        assert str(literal) == "MyLiteral (index=0)"
        literal2 = AutosarEnumLiteral(name="AnotherLiteral", index=5)
        assert str(literal2) == "AnotherLiteral (index=5)"

    def test_repr(self) -> None:
        """Test debug representation.

        Requirements:
            SWR_MODEL_00016: AUTOSAR Enumeration Literal String Representation
        """
        literal = AutosarEnumLiteral(name="TestLiteral", index=1, description="Test description")
        result = repr(literal)
        assert "AutosarEnumLiteral" in result
        assert "name='TestLiteral'" in result
        assert "index=1" in result
        assert "description=True" in result

    def test_repr_without_description(self) -> None:
        """Test debug representation without description.

        Requirements:
            SWR_MODEL_00016: AUTOSAR Enumeration Literal String Representation
        """
        literal = AutosarEnumLiteral(name="TestLiteral")
        result = repr(literal)
        assert "AutosarEnumLiteral" in result
        assert "name='TestLiteral'" in result
        assert "description=False" in result

    def test_index_zero(self) -> None:
        """Test that index can be zero.

        Requirements:
            SWR_MODEL_00014: AUTOSAR Enumeration Literal Representation
        """
        literal = AutosarEnumLiteral(name="FirstValue", index=0)
        assert literal.index == 0
        assert str(literal) == "FirstValue (index=0)"


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
        attr = AutosarAttribute(
            name="dataReadPort",
            type="PPortPrototype",
            is_ref=True,
            multiplicity="0..1",
            kind=AttributeKind.ATTR,
            note="Data read port"
        )
        assert attr.name == "dataReadPort"
        assert attr.type == "PPortPrototype"
        assert attr.is_ref is True
        assert attr.multiplicity == "0..1"
        assert attr.kind == AttributeKind.ATTR
        assert attr.note == "Data read port"

    def test_init_non_reference_attribute(self) -> None:
        """Test creating a non-reference type attribute.

        Requirements:
            SWR_MODEL_00010: AUTOSAR Attribute Representation
        """
        attr = AutosarAttribute(
            name="id",
            type="uint32",
            is_ref=False,
            multiplicity="1",
            kind=AttributeKind.ATTR,
            note="Unique identifier"
        )
        assert attr.name == "id"
        assert attr.type == "uint32"
        assert attr.is_ref is False
        assert attr.multiplicity == "1"
        assert attr.kind == AttributeKind.ATTR
        assert attr.note == "Unique identifier"

    def test_post_init_valid_name(self) -> None:
        """Test valid name validation.

        Requirements:
            SWR_MODEL_00011: AUTOSAR Attribute Name Validation
        """
        attr = AutosarAttribute(
            name="validAttribute",
            type="string",
            is_ref=False,
            multiplicity="1",
            kind=AttributeKind.ATTR,
            note=""
        )
        assert attr.name == "validAttribute"

    def test_post_init_empty_name(self) -> None:
        """Test empty name raises ValueError.

        Requirements:
            SWR_MODEL_00011: AUTOSAR Attribute Name Validation
        """
        with pytest.raises(ValueError, match="Attribute name cannot be empty"):
            AutosarAttribute(
                name="",
                type="string",
                is_ref=False,
                multiplicity="1",
                kind=AttributeKind.ATTR,
                note=""
            )

    def test_post_init_whitespace_name(self) -> None:
        """Test whitespace-only name raises ValueError.

        Requirements:
            SWR_MODEL_00011: AUTOSAR Attribute Name Validation
        """
        with pytest.raises(ValueError, match="Attribute name cannot be empty"):
            AutosarAttribute(
                name="   ",
                type="string",
                is_ref=False,
                multiplicity="1",
                kind=AttributeKind.ATTR,
                note=""
            )

    def test_post_init_valid_type(self) -> None:
        """Test valid type validation.

        Requirements:
            SWR_MODEL_00012: AUTOSAR Attribute Type Validation
        """
        attr = AutosarAttribute(
            name="attr",
            type="ValidType",
            is_ref=False,
            multiplicity="1",
            kind=AttributeKind.ATTR,
            note=""
        )
        assert attr.type == "ValidType"

    def test_post_init_empty_type(self) -> None:
        """Test empty type raises ValueError.

        Requirements:
            SWR_MODEL_00012: AUTOSAR Attribute Type Validation
        """
        with pytest.raises(ValueError, match="Attribute type cannot be empty"):
            AutosarAttribute(
                name="attr",
                type="",
                is_ref=False,
                multiplicity="1",
                kind=AttributeKind.ATTR,
                note=""
            )

    def test_post_init_whitespace_type(self) -> None:
        """Test whitespace-only type raises ValueError.

        Requirements:
            SWR_MODEL_00012: AUTOSAR Attribute Type Validation
        """
        with pytest.raises(ValueError, match="Attribute type cannot be empty"):
            AutosarAttribute(
                name="attr",
                type="   ",
                is_ref=False,
                multiplicity="1",
                kind=AttributeKind.ATTR,
                note=""
            )

    def test_str_reference_attribute(self) -> None:
        """Test string representation of reference attribute.

        Requirements:
            SWR_MODEL_00013: AUTOSAR Attribute String Representation
        """
        attr = AutosarAttribute(
            name="port",
            type="PPortPrototype",
            is_ref=True,
            multiplicity="0..1",
            kind=AttributeKind.ATTR,
            note="Port"
        )
        assert str(attr) == "port: PPortPrototype (ref) [0..1] (attr) - Port"

    def test_str_non_reference_attribute(self) -> None:
        """Test string representation of non-reference attribute.

        Requirements:
            SWR_MODEL_00013: AUTOSAR Attribute String Representation
        """
        attr = AutosarAttribute(
            name="value",
            type="uint32",
            is_ref=False,
            multiplicity="1",
            kind=AttributeKind.ATTR,
            note="Value"
        )
        assert str(attr) == "value: uint32 [1] (attr) - Value"

    def test_repr(self) -> None:
        """Test __repr__ method.

        Requirements:
            SWR_MODEL_00013: AUTOSAR Attribute String Representation
        """
        attr = AutosarAttribute(
            name="testAttr",
            type="TestType",
            is_ref=True,
            multiplicity="*",
            kind=AttributeKind.AGGR,
            note="Test"
        )
        result = repr(attr)
        assert "AutosarAttribute" in result
        assert "name='testAttr'" in result
        assert "type='TestType'" in result
        assert "is_ref=True" in result
        assert "multiplicity='*'" in result
        assert "kind=AttributeKind.AGGR" in result
        assert "note='Test'" in result


class TestAutosarClass:
    """Tests for AutosarClass class.

    Requirements:
        SWR_MODEL_00001: AUTOSAR Class Representation
        SWR_MODEL_00002: AUTOSAR Class Name Validation
        SWR_MODEL_00003: AUTOSAR Class String Representation
        SWR_MODEL_00022: AUTOSAR Class Parent Attribute
        SWR_MODEL_00026: AUTOSAR Class Children Attribute
    """

    def test_init_concrete_class(self) -> None:
        """Test creating a concrete class.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(name="RunnableEntity", package="M2::Test", is_abstract=False)
        assert cls.name == "RunnableEntity"
        assert cls.is_abstract is False

    def test_init_abstract_class(self) -> None:
        """Test creating an abstract class.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(name="InternalBehavior", package="M2::Test", is_abstract=True)
        assert cls.name == "InternalBehavior"
        assert cls.is_abstract is True

    def test_post_init_valid_name(self) -> None:
        """Test valid name validation.

        Requirements:
            SWR_MODEL_00002: AUTOSAR Class Name Validation
        """
        cls = AutosarClass(name="ValidClass", package="M2::Test", is_abstract=False)
        assert cls.name == "ValidClass"

    def test_post_init_empty_name(self) -> None:
        """Test empty name raises ValueError.

        Requirements:
            SWR_MODEL_00002: AUTOSAR Class Name Validation
        """
        with pytest.raises(ValueError, match="Type name cannot be empty"):
            AutosarClass(name="", package="M2::Test", is_abstract=False)

    def test_post_init_whitespace_name(self) -> None:
        """Test whitespace-only name raises ValueError.

        Requirements:
            SWR_MODEL_00002: AUTOSAR Class Name Validation
        """
        with pytest.raises(ValueError, match="Type name cannot be empty"):
            AutosarClass(name="   ", package="M2::Test", is_abstract=False)

    def test_str_concrete_class(self) -> None:
        """Test string representation of concrete class.

        Requirements:
            SWR_MODEL_00003: AUTOSAR Class String Representation
        """
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        assert str(cls) == "MyClass"

    def test_str_abstract_class(self) -> None:
        """Test string representation of abstract class.

        Requirements:
            SWR_MODEL_00003: AUTOSAR Class String Representation
        """
        cls = AutosarClass(name="AbstractClass", package="M2::Test", is_abstract=True)
        assert str(cls) == "AbstractClass (abstract)"

    def test_repr(self) -> None:
        """Test __repr__ method.

        Requirements:
            SWR_MODEL_00003: AUTOSAR Class String Representation
        """
        cls = AutosarClass(name="TestClass", package="M2::Test", is_abstract=True)
        result = repr(cls)
        assert "AutosarClass" in result
        assert "name='TestClass'" in result
        assert "is_abstract=True" in result

    def test_init_with_empty_attributes(self) -> None:
        """Test creating a class with empty attributes dictionary.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(name="Component", package="M2::Test", is_abstract=False)
        assert cls.attributes == {}
        assert len(cls.attributes) == 0

    def test_init_with_attributes(self) -> None:
        """Test creating a class with attributes.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        attr1 = AutosarAttribute(
            name="dataReadPort",
            type="PPortPrototype",
            is_ref=True,
            multiplicity="0..1",
            kind=AttributeKind.ATTR,
            note="Data read port"
        )
        attr2 = AutosarAttribute(
            name="id",
            type="uint32",
            is_ref=False,
            multiplicity="1",
            kind=AttributeKind.ATTR,
            note="Unique identifier"
        )
        cls = AutosarClass(
    name="Component",
    package="M2::Test",
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
        attr1 = AutosarAttribute(name="port", type="PPortPrototype", is_ref=True, multiplicity="1", kind=AttributeKind.ATTR, note="")
        attr2 = AutosarAttribute(name="value", type="uint32", is_ref=False, multiplicity="1", kind=AttributeKind.ATTR, note="")
        cls = AutosarClass(
    name="Component",
    package="M2::Test",
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
        cls = AutosarClass(name="Component", package="M2::Test", is_abstract=False)
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
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        assert cls.bases == []
        assert len(cls.bases) == 0

    def test_init_with_bases(self) -> None:
        """Test creating a class with base classes.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(
    name="DerivedClass",
    package="M2::Test",
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
    package="M2::Test",
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
    package="M2::Test",
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
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        assert cls.note is None

    def test_init_with_note(self) -> None:
        """Test creating a class with a note.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(
    name="MyClass",
    package="M2::Test",
    is_abstract=False,
            note="This is a documentation note"
        )
        assert cls.note == "This is a documentation note"

    def test_init_with_empty_note(self) -> None:
        """Test creating a class with empty string note.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False, note="")
        assert cls.note == ""

    def test_repr_with_note(self) -> None:
        """Test __repr__ includes note presence.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(
    name="MyClass",
    package="M2::Test",
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
        attr = AutosarAttribute(name="port", type="PPortPrototype", is_ref=True, multiplicity="1", kind=AttributeKind.ATTR, note="")
        cls = AutosarClass(
    name="CompleteClass",
    package="M2::Test",
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
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        cls.bases.append("BaseClass")
        assert len(cls.bases) == 1
        assert "BaseClass" in cls.bases

    def test_note_reassignment(self) -> None:
        """Test that note can be reassigned.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        cls.note = "Updated note"
        assert cls.note == "Updated note"

    def test_init_default_atp_type_is_none(self) -> None:
        """Test that ATP type defaults to NONE.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        assert cls.atp_type == ATPType.NONE

    def test_init_with_atp_mixed_string(self) -> None:
        """Test creating class with atpMixedString type.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False, atp_type=ATPType.ATP_MIXED_STRING)
        assert cls.atp_type == ATPType.ATP_MIXED_STRING

    def test_init_with_atp_variation(self) -> None:
        """Test creating class with atpVariation type.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Representation
        """
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False, atp_type=ATPType.ATP_VARIATION)
        assert cls.atp_type == ATPType.ATP_VARIATION

    def test_repr_includes_atp_type(self) -> None:
        """Test __repr__ includes ATP type.

        Requirements:
            SWR_MODEL_00003: AUTOSAR Class String Representation
        """
        cls = AutosarClass(
    name="MyClass",
    package="M2::Test",
    is_abstract=False,
            atp_type=ATPType.ATP_VARIATION
        )
        result = repr(cls)
        assert "atp_type=ATP_VARIATION" in result

    def test_repr_with_atp_mixed_string(self) -> None:
        """Test __repr__ with atpMixedString type.

        Requirements:
            SWR_MODEL_00003: AUTOSAR Class String Representation
        """
        cls = AutosarClass(
    name="MyClass",
    package="M2::Test",
    is_abstract=False,
            atp_type=ATPType.ATP_MIXED_STRING
        )
        result = repr(cls)
        assert "atp_type=ATP_MIXED_STRING" in result

    def test_init_default_parent_is_none(self) -> None:
        """Test that parent defaults to None.

        Requirements:
            SWR_MODEL_00022: AUTOSAR Class Parent Attribute
        """
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        assert cls.parent is None

    def test_init_with_parent(self) -> None:
        """Test creating a class with a parent.

        Requirements:
            SWR_MODEL_00022: AUTOSAR Class Parent Attribute
        """
        parent_cls = AutosarClass(name="ParentClass", package="M2::Test", is_abstract=False)
        child_cls = AutosarClass(name="ChildClass", package="M2::Test", is_abstract=False, parent=parent_cls)
        assert child_cls.parent is parent_cls
        assert child_cls.parent.name == "ParentClass"

    def test_parent_reference_maintains_object(self) -> None:
        """Test that parent maintains the actual object reference.

        Requirements:
            SWR_MODEL_00022: AUTOSAR Class Parent Attribute
        """
        parent = AutosarClass(name="ParentClass", package="M2::Test", is_abstract=False)
        child = AutosarClass(name="ChildClass", package="M2::Test", is_abstract=False, parent=parent)
        # Verify it's the same object
        assert child.parent is parent
        # Verify we can access parent attributes
        assert child.parent.name == "ParentClass"
        assert child.parent.is_abstract is False

    def test_repr_shows_parent_name(self) -> None:
        """Test that __repr__ includes parent name when parent is set.

        Requirements:
            SWR_MODEL_00022: AUTOSAR Class Parent Attribute
        """
        parent = AutosarClass(name="ParentClass", package="M2::Test", is_abstract=False)
        child = AutosarClass(name="ChildClass", package="M2::Test", is_abstract=False, parent=parent)
        result = repr(child)
        assert "parent=ParentClass" in result

    def test_repr_shows_parent_none_when_no_parent(self) -> None:
        """Test that __repr__ shows parent=None when no parent.

        Requirements:
            SWR_MODEL_00022: AUTOSAR Class Parent Attribute
        """
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        result = repr(cls)
        assert "parent=None" in result

    def test_parent_can_be_reassigned(self) -> None:
        """Test that parent can be reassigned.

        Requirements:
            SWR_MODEL_00022: AUTOSAR Class Parent Attribute
        """
        parent1 = AutosarClass(name="Parent1", package="M2::Test", is_abstract=False)
        parent2 = AutosarClass(name="Parent2", package="M2::Test", is_abstract=False)
        child = AutosarClass(name="ChildClass", package="M2::Test", is_abstract=False, parent=parent1)
        assert child.parent is parent1
        child.parent = parent2
        assert child.parent is parent2
        assert child.parent.name == "Parent2"

    def test_init_default_children_is_empty_list(self) -> None:
        """Test that children defaults to empty list.

        Requirements:
            SWR_MODEL_00026: AUTOSAR Class Children Attribute
        """
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        assert cls.children == []

    def test_init_with_children(self) -> None:
        """Test creating a class with children.

        Requirements:
            SWR_MODEL_00026: AUTOSAR Class Children Attribute
        """
        cls = AutosarClass(
            name="ParentClass",
            package="M2::Test",
            is_abstract=False,
            children=["Child1", "Child2"]
        )
        assert len(cls.children) == 2
        assert "Child1" in cls.children
        assert "Child2" in cls.children

    def test_children_mutation(self) -> None:
        """Test that children list can be mutated.

        Requirements:
            SWR_MODEL_00026: AUTOSAR Class Children Attribute
        """
        cls = AutosarClass(name="ParentClass", package="M2::Test", is_abstract=False)
        assert cls.children == []
        cls.children.append("Child1")
        cls.children.append("Child2")
        assert len(cls.children) == 2
        cls.children.remove("Child1")
        assert len(cls.children) == 1
        assert "Child2" in cls.children

    def test_repr_shows_children_count(self) -> None:
        """Test that __repr__ includes children count.

        Requirements:
            SWR_MODEL_00026: AUTOSAR Class Children Attribute
        """
        cls = AutosarClass(
            name="ParentClass",
            package="M2::Test",
            is_abstract=False,
            children=["Child1", "Child2", "Child3"]
        )
        result = repr(cls)
        assert "children=3" in result

    def test_repr_shows_children_zero_when_no_children(self) -> None:
        """Test that __repr__ shows children=0 when no children.

        Requirements:
            SWR_MODEL_00026: AUTOSAR Class Children Attribute
        """
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        result = repr(cls)
        assert "children=0" in result

    def test_children_can_be_reassigned(self) -> None:
        """Test that children can be reassigned.

        Requirements:
            SWR_MODEL_00026: AUTOSAR Class Children Attribute
        """
        cls = AutosarClass(
            name="ParentClass",
            package="M2::Test",
            is_abstract=False,
            children=["Child1", "Child2"]
        )
        assert len(cls.children) == 2
        cls.children = ["Child3", "Child4", "Child5"]
        assert len(cls.children) == 3
        assert "Child3" in cls.children
        assert "Child1" not in cls.children


class TestAutosarEnumeration:
    """Tests for AutosarEnumeration class.

    Requirements:
        SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
        SWR_MODEL_00019: AUTOSAR Enumeration Type Representation
    """

    def test_init_concrete_enumeration(self) -> None:
        """Test creating a concrete enumeration.

        Requirements:
            SWR_MODEL_00019: AUTOSAR Enumeration Type Representation
        """
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")
        assert enum.name == "MyEnum"
        assert enum.enumeration_literals == []

    def test_init_abstract_enumeration(self) -> None:
        """Test creating an abstract enumeration.

        Requirements:
            SWR_MODEL_00019: AUTOSAR Enumeration Type Representation
        """
        enum = AutosarEnumeration(name="AbstractEnum", package="M2::Test")
        assert enum.name == "AbstractEnum"

    def test_init_with_literals(self) -> None:
        """Test creating enumeration with literals.

        Requirements:
            SWR_MODEL_00019: AUTOSAR Enumeration Type Representation
        """
        literals = [
            AutosarEnumLiteral("VALUE1", 0, "First value"),
            AutosarEnumLiteral("VALUE2", 1, "Second value"),
        ]
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test", enumeration_literals=literals)
        assert enum.name == "MyEnum"
        assert len(enum.enumeration_literals) == 2
        assert enum.enumeration_literals[0].name == "VALUE1"
        assert enum.enumeration_literals[1].name == "VALUE2"

    def test_init_with_note(self) -> None:
        """Test creating enumeration with note.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
        """
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test", note="Documentation note")
        assert enum.note == "Documentation note"

    def test_init_with_atp_variation(self) -> None:
        """Test creating enumeration with note.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
        """
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test", note="Test note")
        assert enum.note == "Test note"

    def test_init_with_all_fields(self) -> None:
        """Test creating enumeration with all fields.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
            SWR_MODEL_00019: AUTOSAR Enumeration Type Representation
        """
        literals = [
            AutosarEnumLiteral("VALUE1", 0),
            AutosarEnumLiteral("VALUE2", 1),
        ]
        enum = AutosarEnumeration(
            name="CompleteEnum",
            package="M2::Test",
            note="Complete enumeration",
            enumeration_literals=literals
        )
        assert enum.name == "CompleteEnum"
        assert enum.note == "Complete enumeration"
        assert len(enum.enumeration_literals) == 2

    def test_str_concrete_enumeration(self) -> None:
        """Test string representation of concrete enumeration.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
        """
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")
        assert str(enum) == "MyEnum"

    def test_repr_without_literals(self) -> None:
        """Test debug representation without literals.

        Requirements:
            SWR_MODEL_00019: AUTOSAR Enumeration Type Representation
        """
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")
        result = repr(enum)
        assert "AutosarEnumeration" in result
        assert "name='MyEnum'" in result
        assert "enumeration_literals=0" in result

    def test_repr_with_literals(self) -> None:
        """Test debug representation with literals.

        Requirements:
            SWR_MODEL_00019: AUTOSAR Enumeration Type Representation
        """
        literals = [
            AutosarEnumLiteral("VALUE1", 0),
            AutosarEnumLiteral("VALUE2", 1),
        ]
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test", enumeration_literals=literals)
        result = repr(enum)
        assert "enumeration_literals=2" in result

    def test_repr_with_all_fields(self) -> None:
        """Test debug representation with all fields.

        Requirements:
            SWR_MODEL_00019: AUTOSAR Enumeration Type Representation
        """
        literals = [AutosarEnumLiteral("VALUE1", 0)]
        enum = AutosarEnumeration(
            name="CompleteEnum",
            package="M2::Test",
            note="Note",
            enumeration_literals=literals
        )
        result = repr(enum)
        assert "name='CompleteEnum'" in result
        assert "enumeration_literals=1" in result
        assert "note=True" in result

    def test_literals_mutation(self) -> None:
        """Test that enumeration_literals list can be mutated.

        Requirements:
            SWR_MODEL_00019: AUTOSAR Enumeration Type Representation
        """
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")
        enum.enumeration_literals.append(AutosarEnumLiteral("VALUE1", 0))
        assert len(enum.enumeration_literals) == 1
        enum.enumeration_literals.append(AutosarEnumLiteral("VALUE2", 1))
        assert len(enum.enumeration_literals) == 2

    def test_inheritance_from_abstract_autosar_base(self) -> None:
        """Test that AutosarEnumeration inherits from AbstractAutosarBase.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
            SWR_MODEL_00019: AUTOSAR Enumeration Type Representation
        """
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")
        # Check inherited attributes
        assert hasattr(enum, 'name')
        assert hasattr(enum, 'package')
        assert hasattr(enum, 'note')
        # Check enumeration-specific attribute
        assert hasattr(enum, 'enumeration_literals')


class TestAutosarPrimitive:
    """Tests for AutosarPrimitive class.

    Requirements:
        SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
        SWR_MODEL_00024: AUTOSAR Primitive Type Representation
    """

    def test_init_concrete_primitive(self) -> None:
        """Test creating a concrete primitive type.

        Requirements:
            SWR_MODEL_00024: AUTOSAR Primitive Type Representation
        """
        primitive = AutosarPrimitive(name="Limit", package="M2::DataTypes")
        assert primitive.name == "Limit"
        assert primitive.package == "M2::DataTypes"
        assert primitive.note is None

    def test_init_with_note(self) -> None:
        """Test creating a primitive type with note.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
        """
        primitive = AutosarPrimitive(name="Interval", package="M2::DataTypes", note="Interval type")
        assert primitive.name == "Interval"
        assert primitive.note == "Interval type"

    def test_init_with_all_fields(self) -> None:
        """Test creating a primitive type with all fields.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
            SWR_MODEL_00024: AUTOSAR Primitive Type Representation
        """
        attr = AutosarAttribute(name="intervalType", type="String", is_ref=False, multiplicity="1", kind=AttributeKind.ATTR, note="")
        primitive = AutosarPrimitive(
            name="CompletePrimitive",
            package="M2::DataTypes",
            note="Complete primitive type",
            attributes={"intervalType": attr}
        )
        assert primitive.name == "CompletePrimitive"
        assert primitive.package == "M2::DataTypes"
        assert primitive.note == "Complete primitive type"
        assert len(primitive.attributes) == 1
        assert "intervalType" in primitive.attributes

    def test_init_with_empty_attributes(self) -> None:
        """Test creating a primitive type with empty attributes dictionary.

        Requirements:
            SWR_MODEL_00024: AUTOSAR Primitive Type Representation
        """
        primitive = AutosarPrimitive(name="Limit", package="M2::DataTypes")
        assert primitive.attributes == {}
        assert len(primitive.attributes) == 0

    def test_init_with_attributes(self) -> None:
        """Test creating a primitive type with attributes.

        Requirements:
            SWR_MODEL_00024: AUTOSAR Primitive Type Representation
        """
        attr1 = AutosarAttribute(name="intervalType", type="String", is_ref=False, multiplicity="1", kind=AttributeKind.ATTR, note="")
        attr2 = AutosarAttribute(name="limitType", type="Integer", is_ref=False, multiplicity="1", kind=AttributeKind.ATTR, note="")
        primitive = AutosarPrimitive(
            name="Limit",
            package="M2::DataTypes",
            attributes={"intervalType": attr1, "limitType": attr2}
        )
        assert len(primitive.attributes) == 2
        assert "intervalType" in primitive.attributes
        assert "limitType" in primitive.attributes
        assert primitive.attributes["intervalType"] == attr1
        assert primitive.attributes["limitType"] == attr2

    def test_repr_with_attributes(self) -> None:
        """Test __repr__ method shows attributes count.

        Requirements:
            SWR_MODEL_00024: AUTOSAR Primitive Type Representation
        """
        attr = AutosarAttribute(name="intervalType", type="String", is_ref=False, multiplicity="1", kind=AttributeKind.ATTR, note="")
        primitive = AutosarPrimitive(
            name="Limit",
            package="M2::DataTypes",
            attributes={"intervalType": attr}
        )
        result = repr(primitive)
        assert "AutosarPrimitive" in result
        assert "name='Limit'" in result
        assert "attributes=1" in result

    def test_repr_without_attributes(self) -> None:
        """Test __repr__ method with no attributes.

        Requirements:
            SWR_MODEL_00024: AUTOSAR Primitive Type Representation
        """
        primitive = AutosarPrimitive(name="Limit", package="M2::DataTypes")
        result = repr(primitive)
        assert "AutosarPrimitive" in result
        assert "name='Limit'" in result
        assert "attributes=0" in result

    def test_str_primitive(self) -> None:
        """Test string representation of primitive type.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
            SWR_MODEL_00024: AUTOSAR Primitive Type Representation
        """
        primitive = AutosarPrimitive(name="Limit", package="M2::DataTypes")
        assert str(primitive) == "Limit"

    def test_repr_without_note(self) -> None:
        """Test debug representation without note.

        Requirements:
            SWR_MODEL_00024: AUTOSAR Primitive Type Representation
        """
        primitive = AutosarPrimitive(name="Limit", package="M2::DataTypes")
        result = repr(primitive)
        assert "AutosarPrimitive" in result
        assert "name='Limit'" in result
        assert "package='M2::DataTypes'" in result
        assert "attributes=0" in result
        assert "note=False" in result

    def test_repr_with_note(self) -> None:
        """Test debug representation with note.

        Requirements:
            SWR_MODEL_00024: AUTOSAR Primitive Type Representation
        """
        primitive = AutosarPrimitive(name="Limit", package="M2::DataTypes", note="Test note")
        result = repr(primitive)
        assert "AutosarPrimitive" in result
        assert "name='Limit'" in result
        assert "attributes=0" in result
        assert "note=True" in result

    def test_post_init_valid_name(self) -> None:
        """Test valid name validation.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
        """
        primitive = AutosarPrimitive(name="ValidPrimitive", package="M2::DataTypes")
        assert primitive.name == "ValidPrimitive"

    def test_post_init_empty_name(self) -> None:
        """Test empty name raises ValueError.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
        """
        with pytest.raises(ValueError, match="Type name cannot be empty"):
            AutosarPrimitive(name="", package="M2::DataTypes")

    def test_post_init_whitespace_name(self) -> None:
        """Test whitespace-only name raises ValueError.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
        """
        with pytest.raises(ValueError, match="Type name cannot be empty"):
            AutosarPrimitive(name="   ", package="M2::DataTypes")


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
        assert len(pkg.types) == 0
        assert len(pkg.subpackages) == 0

    def test_init_with_classes(self) -> None:
        """Test creating a package with classes.

        Requirements:
            SWR_MODEL_00004: AUTOSAR Package Representation
        """
        cls1 = AutosarClass(name="Class1", package="M2::Test", is_abstract=False)
        cls2 = AutosarClass(name="Class2", package="M2::Test", is_abstract=True)
        pkg = AutosarPackage(name="TestPackage", types=[cls1, cls2])
        assert len(pkg.types) == 2
        assert pkg.types[0].name == "Class1"
        assert pkg.types[1].name == "Class2"

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
        cls = AutosarClass(name="NewClass", package="M2::Test", is_abstract=False)
        pkg.add_class(cls)
        assert len(pkg.types) == 1
        assert pkg.types[0] == cls

    def test_add_class_duplicate(self) -> None:
        """Test adding duplicate class raises ValueError.

        Requirements:
            SWR_MODEL_00006: Add Class to Package
        """
        pkg = AutosarPackage(name="TestPackage")
        cls1 = AutosarClass(name="DuplicateClass", package="M2::Test", is_abstract=False)
        cls2 = AutosarClass(name="DuplicateClass", package="M2::Test", is_abstract=True)
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
        cls = AutosarClass(name="TargetClass", package="M2::Test", is_abstract=False)
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
        cls = AutosarClass(name="ExistingClass", package="M2::Test", is_abstract=False)
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
        pkg.add_class(AutosarClass(name="Class1", package="M2::Test", is_abstract=False))
        pkg.add_class(AutosarClass(name="Class2", package="M2::Test", is_abstract=True))
        result = str(pkg)
        assert "TestPackage" in result
        assert "2 types" in result

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
        pkg.add_class(AutosarClass(name="Class1", package="M2::Test", is_abstract=False))
        pkg.add_subpackage(AutosarPackage(name="Sub1"))
        result = str(pkg)
        assert "TestPackage" in result
        assert "1 types" in result
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
        pkg.add_class(AutosarClass(name="Class1", package="M2::Test", is_abstract=False))
        pkg.add_subpackage(AutosarPackage(name="Sub1"))
        result = repr(pkg)
        assert "AutosarPackage" in result
        assert "name='TestPackage'" in result
        assert "types=1" in result
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

    def test_add_type_with_class(self) -> None:
        """Test add_type method with a class.

        Requirements:
            SWR_MODEL_00006: Add Class to Package
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        pkg.add_type(cls)
        assert len(pkg.types) == 1
        assert pkg.types[0].name == "MyClass"

    def test_add_type_with_enumeration(self) -> None:
        """Test add_type method with an enumeration.

        Requirements:
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")
        pkg.add_type(enum)
        assert len(pkg.types) == 1
        assert pkg.types[0].name == "MyEnum"

    def test_add_type_duplicate(self) -> None:
        """Test add_type method rejects duplicate type names.

        Requirements:
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyType", package="M2::Test", is_abstract=False)
        enum = AutosarEnumeration(name="MyType", package="M2::Test")

        pkg.add_type(cls)
        with pytest.raises(ValueError, match="Type 'MyType' already exists"):
            pkg.add_type(enum)

    def test_add_enumeration(self) -> None:
        """Test add_enumeration method.

        Requirements:
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")
        pkg.add_enumeration(enum)
        assert len(pkg.types) == 1
        assert isinstance(pkg.types[0], AutosarEnumeration)

    def test_get_type_found(self) -> None:
        """Test get_type method when type exists.

        Requirements:
            SWR_MODEL_00008: Query Package Contents
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        pkg.add_type(cls)
        result = pkg.get_type("MyClass")
        assert result is not None
        assert result.name == "MyClass"

    def test_get_type_not_found(self) -> None:
        """Test get_type method when type doesn't exist.

        Requirements:
            SWR_MODEL_00008: Query Package Contents
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        result = pkg.get_type("NonExistent")
        assert result is None

    def test_get_type_from_mixed_types(self) -> None:
        """Test get_type can retrieve classes, enumerations, and primitives.

        Requirements:
            SWR_MODEL_00020: AUTOSAR Package Type Support
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")
        primitive = AutosarPrimitive(name="Limit", package="M2::DataTypes")
        pkg.add_type(cls)
        pkg.add_type(enum)
        pkg.add_type(primitive)

        cls_result = pkg.get_type("MyClass")
        enum_result = pkg.get_type("MyEnum")
        primitive_result = pkg.get_type("Limit")

        assert isinstance(cls_result, AutosarClass)
        assert isinstance(enum_result, AutosarEnumeration)
        assert isinstance(primitive_result, AutosarPrimitive)

    def test_get_enumeration_found(self) -> None:
        """Test get_enumeration method when enumeration exists.

        Requirements:
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")
        pkg.add_enumeration(enum)
        result = pkg.get_enumeration("MyEnum")
        assert result is not None
        assert result.name == "MyEnum"
        assert isinstance(result, AutosarEnumeration)

    def test_get_enumeration_not_found(self) -> None:
        """Test get_enumeration method when enumeration doesn't exist.

        Requirements:
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        result = pkg.get_enumeration("NonExistent")
        assert result is None

    def test_get_enumeration_returns_none_for_class(self) -> None:
        """Test get_enumeration returns None for classes.

        Requirements:
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        pkg.add_class(cls)
        result = pkg.get_enumeration("MyClass")
        assert result is None

    def test_has_type_true(self) -> None:
        """Test has_type returns True when type exists.

        Requirements:
            SWR_MODEL_00008: Query Package Contents
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        pkg.add_type(cls)
        assert pkg.has_type("MyClass") is True

    def test_has_type_false(self) -> None:
        """Test has_type returns False when type doesn't exist.

        Requirements:
            SWR_MODEL_00008: Query Package Contents
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        assert pkg.has_type("NonExistent") is False

    def test_has_enumeration_true(self) -> None:
        """Test has_enumeration returns True when enumeration exists.

        Requirements:
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")
        pkg.add_enumeration(enum)
        assert pkg.has_enumeration("MyEnum") is True

    def test_has_enumeration_false_for_class(self) -> None:
        """Test has_enumeration returns False for classes.

        Requirements:
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        pkg.add_class(cls)
        assert pkg.has_enumeration("MyClass") is False

    def test_has_enumeration_false_not_found(self) -> None:
        """Test has_enumeration returns False when not found.

        Requirements:
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        assert pkg.has_enumeration("NonExistent") is False

    def test_add_primitive(self) -> None:
        """Test add_primitive method.

        Requirements:
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        primitive = AutosarPrimitive(name="Limit", package="M2::DataTypes")
        pkg.add_primitive(primitive)
        assert len(pkg.types) == 1
        assert isinstance(pkg.types[0], AutosarPrimitive)

    def test_get_primitive_found(self) -> None:
        """Test get_primitive method when primitive exists.

        Requirements:
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        primitive = AutosarPrimitive(name="Limit", package="M2::DataTypes")
        pkg.add_primitive(primitive)
        result = pkg.get_primitive("Limit")
        assert result is not None
        assert result.name == "Limit"
        assert isinstance(result, AutosarPrimitive)

    def test_get_primitive_not_found(self) -> None:
        """Test get_primitive method when primitive doesn't exist.

        Requirements:
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        result = pkg.get_primitive("NonExistent")
        assert result is None

    def test_get_primitive_returns_none_for_class(self) -> None:
        """Test get_primitive returns None for classes.

        Requirements:
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        pkg.add_class(cls)
        result = pkg.get_primitive("MyClass")
        assert result is None

    def test_get_primitive_returns_none_for_enumeration(self) -> None:
        """Test get_primitive returns None for enumerations.

        Requirements:
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")
        pkg.add_enumeration(enum)
        result = pkg.get_primitive("MyEnum")
        assert result is None

    def test_has_primitive_true(self) -> None:
        """Test has_primitive returns True when primitive exists.

        Requirements:
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        primitive = AutosarPrimitive(name="Limit", package="M2::DataTypes")
        pkg.add_primitive(primitive)
        assert pkg.has_primitive("Limit") is True

    def test_has_primitive_false_for_class(self) -> None:
        """Test has_primitive returns False for classes.

        Requirements:
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        pkg.add_class(cls)
        assert pkg.has_primitive("MyClass") is False

    def test_has_primitive_false_for_enumeration(self) -> None:
        """Test has_primitive returns False for enumerations.

        Requirements:
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")
        pkg.add_enumeration(enum)
        assert pkg.has_primitive("MyEnum") is False

    def test_has_primitive_false_not_found(self) -> None:
        """Test has_primitive returns False when not found.

        Requirements:
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        assert pkg.has_primitive("NonExistent") is False

    def test_unified_type_management(self) -> None:
        """Test that types collection unifies classes, enumerations, and primitives.

        Requirements:
            SWR_MODEL_00020: AUTOSAR Package Type Support
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")
        primitive = AutosarPrimitive(name="Limit", package="M2::DataTypes")

        pkg.add_type(cls)
        pkg.add_type(enum)
        pkg.add_type(primitive)

        assert len(pkg.types) == 3
        assert pkg.has_type("MyClass") is True
        assert pkg.has_type("MyEnum") is True
        assert pkg.has_type("Limit") is True

    def test_duplicate_prevention_across_type_kinds(self) -> None:
        """Test duplicate names prevented across classes, enumerations, and primitives.

        Requirements:
            SWR_MODEL_00020: AUTOSAR Package Type Support
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyType", package="M2::Test", is_abstract=False)
        enum = AutosarEnumeration(name="MyType", package="M2::Test")

        pkg.add_type(cls)
        with pytest.raises(ValueError, match="Type 'MyType' already exists"):
            pkg.add_type(enum)

        assert len(pkg.types) == 1
        assert isinstance(pkg.types[0], AutosarClass)

    def test_add_class_backward_compatibility(self) -> None:
        """Test add_class method still works.

        Requirements:
            SWR_MODEL_00006: Add Class to Package
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        pkg.add_class(cls)
        assert len(pkg.types) == 1
        assert pkg.has_class("MyClass") is True

    def test_get_class_returns_only_classes(self) -> None:
        """Test get_class returns only classes, not enumerations.

        Requirements:
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")

        pkg.add_type(cls)
        pkg.add_type(enum)

        cls_result = pkg.get_class("MyClass")
        enum_result = pkg.get_class("MyEnum")

        assert isinstance(cls_result, AutosarClass)
        assert enum_result is None

    def test_has_class_returns_true_only_for_classes(self) -> None:
        """Test has_class returns True only for classes.

        Requirements:
            SWR_MODEL_00020: AUTOSAR Package Type Support
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")

        pkg.add_type(cls)
        pkg.add_type(enum)

        assert pkg.has_class("MyClass") is True
        assert pkg.has_class("MyEnum") is False
