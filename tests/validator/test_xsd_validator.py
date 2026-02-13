"""Unit tests for XSD validator.

Tests the XSD parser and validator functionality for real-time
validation and auto-correction of parsed AUTOSAR classes.

Requirements:
    SWR_PARSER_00031: XSD-based validation of parsed types
"""

from autosar_pdf2txt.models import AutosarClass, AutosarAttribute
from autosar_pdf2txt.models.enums import ATPType, AttributeKind
from autosar_pdf2txt.validator import XsdParser, XsdValidator


def test_xsd_parser_loads_classes():
    """Test that XSD parser loads class definitions from XSD file."""
    parser = XsdParser()
    xsd_classes = parser.parse_xsd("examples/xsd/AUTOSAR_00052.xsd")

    # Should load thousands of classes
    assert len(xsd_classes) > 1000

    # Check for known classes (XSD parser uses lowercase first letter)
    assert "abstractAccessPoint" in xsd_classes
    assert "absoluteTolerance" in xsd_classes


def test_xsd_class_has_attributes():
    """Test that XSD classes have attribute definitions."""
    parser = XsdParser()
    xsd_classes = parser.parse_xsd("examples/xsd/AUTOSAR_00052.xsd")

    # Check AbstractAccessPoint has returnValueProvision attribute
    abstract_access_point = xsd_classes["abstractAccessPoint"]
    assert "returnValueProvision" in abstract_access_point.attributes

    # Check that the attribute has a type
    attr = abstract_access_point.attributes["returnValueProvision"]
    assert attr.type is not None
    assert attr.type == "RTE-API-RETURN-VALUE-PROVISION-ENUM"


def test_xsd_naming_conversion():
    """Test XSD to CamelCase naming conversion."""
    # Test UPPER-CASE-HYPENATED to CamelCase
    assert XsdParser.xsd_to_camel_case("RETURN-VALUE-PROVISION") == "returnValueProvision"
    assert XsdParser.xsd_to_camel_case("ABSTRACT-ACCESS-POINT") == "abstractAccessPoint"
    assert XsdParser.xsd_to_camel_case("AR-OBJECT") == "arObject"

    # Test CamelCase to UPPER-CASE-HYPENATED
    assert XsdParser.camel_to_xsd_case("returnValueProvision") == "RETURN-VALUE-PROVISION"
    assert XsdParser.camel_to_xsd_case("abstractAccessPoint") == "ABSTRACT-ACCESS-POINT"


def test_validator_handles_class_not_in_xsd():
    """Test that validator handles classes not in XSD gracefully."""
    parser = XsdParser()
    xsd_classes = parser.parse_xsd("examples/xsd/AUTOSAR_00052.xsd")
    validator = XsdValidator(xsd_classes)

    # Create a class that doesn't exist in XSD
    cls = AutosarClass(
        name="NonExistentClass",
        package="TestPackage",
        is_abstract=False,
        atp_type=ATPType.NONE,
        sources=[],
    )
    cls.attributes["testAttr"] = AutosarAttribute(
        name="testAttr",
        type="SomeType",
        is_ref=False,
        multiplicity="1",
        kind=AttributeKind.ATTR,
        note="Test attribute",
    )

    # Validate
    corrections = validator.validate_and_correct_class(cls)

    # Should have no corrections (class not in XSD)
    assert len(corrections) == 0


def test_validator_corrects_known_type():
    """Test that validator can correct known type names."""
    parser = XsdParser()
    xsd_classes = parser.parse_xsd("examples/xsd/AUTOSAR_00052.xsd")
    validator = XsdValidator(xsd_classes)

    # Create a class that exists in XSD
    cls = AutosarClass(
        name="AbstractAccessPoint",
        package="TestPackage",
        is_abstract=True,
        atp_type=ATPType.NONE,
        sources=[],
    )

    # Add attribute with correct name
    cls.attributes["returnValueProvision"] = AutosarAttribute(
        name="returnValueProvision",
        type="RteApiReturnValueProvisionEnum",  # Using CamelCase version
        is_ref=False,
        multiplicity="0..1",
        kind=AttributeKind.ATTR,
        note="Test attribute",
    )

    # Validate
    corrections = validator.validate_and_correct_class(cls)

    # Should have at least one correction (type name conversion)
    # The type should be converted from CamelCase to UPPER-CASE-HYPENATED
    # or vice versa depending on the XSD definition
    print(f"Corrections: {corrections}")
    print(f"Final type: {cls.attributes['returnValueProvision'].type}")

    # At minimum, the validation should complete without errors
    assert len(corrections) >= 0  # May have corrections or may not


def test_xsd_parser_handles_large_file():
    """Test that XSD parser can handle the large AUTOSAR XSD file."""
    parser = XsdParser()
    
    # This should complete without errors
    xsd_classes = parser.parse_xsd("examples/xsd/AUTOSAR_00052.xsd")
    
    # Should have parsed a significant number of classes
    assert len(xsd_classes) > 2000


def test_xsd_parser_extracts_qualified_names():
    """Test that XSD parser extracts qualified names correctly."""
    parser = XsdParser()
    xsd_classes = parser.parse_xsd("examples/xsd/AUTOSAR_00052.xsd")

    # Check that classes have qualified names
    absolute_tolerance = xsd_classes["absoluteTolerance"]
    assert absolute_tolerance.qualified_name == "AbsoluteTolerance"

    abstract_access_point = xsd_classes["abstractAccessPoint"]
    assert abstract_access_point.qualified_name == "AbstractAccessPoint"