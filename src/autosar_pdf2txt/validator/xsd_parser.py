"""XSD parser for extracting AUTOSAR class definitions.

This module parses AUTOSAR XSD files to extract class definitions,
their attributes, and inheritance relationships for validation purposes.

Requirements:
    SWR_PARSER_00031: XSD-based validation of parsed types
"""

import logging
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


logger = logging.getLogger(__name__)


@dataclass
class XsdAttribute:
    """Represents an attribute definition from XSD.

    Attributes:
        name: Attribute name in CamelCase format.
        type: Attribute type name.
        xsd_name: Original XSD element name (UPPER-CASE-HYPENATED).
        qualified_name: Fully qualified name from mmt.qualifiedName.
    """

    name: str
    type: str
    xsd_name: str
    qualified_name: Optional[str] = None


@dataclass
class XsdClass:
    """Represents a class definition from XSD.

    Attributes:
        name: Class name in CamelCase format.
        xsd_name: Original XSD group/complexType name (UPPER-CASE-HYPENATED).
        qualified_name: Fully qualified name from mmt.qualifiedName.
        attributes: Dictionary of attribute definitions keyed by name.
        base_classes: List of base class names (from group references).
        is_abstract: Whether the class is abstract.
    """

    name: str
    xsd_name: str
    qualified_name: Optional[str]
    attributes: Dict[str, XsdAttribute] = field(default_factory=dict)
    base_classes: List[str] = field(default_factory=list)
    is_abstract: bool = False


class XsdParser:
    """Parser for AUTOSAR XSD files.

    Extracts class definitions, attributes, and inheritance relationships
    from AUTOSAR XML Schema Definition files.

    Requirements:
        SWR_PARSER_00031: XSD-based validation of parsed types
    """

    # XSD namespace
    XSD_NS = "http://www.w3.org/2001/XMLSchema"
    AR_NS = "http://autosar.org/schema/r4.0"

    def __init__(self) -> None:
        """Initialize XSD parser."""
        self.classes: Dict[str, XsdClass] = {}
        self._type_lookup: Dict[str, str] = {}

    def parse_xsd(self, xsd_file: str) -> Dict[str, XsdClass]:
        """Parse XSD file and extract class definitions.

        Args:
            xsd_file: Path to XSD file.

        Returns:
            Dictionary mapping class names to XsdClass objects.

        Raises:
            FileNotFoundError: If XSD file doesn't exist.
            ValueError: If XSD file is malformed.
        """
        logger.info(f"Parsing XSD file: {xsd_file}")

        xsd_path = Path(xsd_file)
        if not xsd_path.exists():
            raise FileNotFoundError(f"XSD file not found: {xsd_file}")

        # Parse XML
        try:
            tree = ET.parse(xsd_path)
            root = tree.getroot()
        except ET.ParseError as e:
            raise ValueError(f"Failed to parse XSD file: {e}")

        # Extract class definitions from groups and complexTypes
        self._extract_classes(root)

        # Build inheritance relationships
        self._build_inheritance(root)

        # Build type lookup
        self._build_type_lookup(root)

        logger.info(f"Extracted {len(self.classes)} class definitions from XSD")

        return self.classes

    def _extract_classes(self, root: ET.Element) -> None:
        """Extract class definitions from XSD groups and complexTypes.

        Args:
            root: Root XML element.
        """
        # Extract from xsd:group elements
        for group in root.findall(f".//{{{self.XSD_NS}}}group"):
            self._parse_class_element(group, "group")

        # Extract from xsd:complexType elements
        for complex_type in root.findall(f".//{{{self.XSD_NS}}}complexType"):
            self._parse_class_element(complex_type, "complexType")

    def _parse_class_element(
        self, element: ET.Element, element_type: str
    ) -> None:
        """Parse a class element (group or complexType).

        Args:
            element: XSD element to parse.
            element_type: Type of element ("group" or "complexType").
        """
        xsd_name = element.get("name")
        if not xsd_name:
            return

        # Extract qualified name from mmt.qualifiedName
        qualified_name = self._extract_qualified_name(element)

        # Convert to CamelCase
        class_name = self.xsd_to_camel_case(xsd_name)

        # Check if abstract
        is_abstract = element.get("abstract", "false") == "true"

        # Create XsdClass
        xsd_class = XsdClass(
            name=class_name,
            xsd_name=xsd_name,
            qualified_name=qualified_name,
            is_abstract=is_abstract,
        )

        # Extract attributes from child elements
        self._extract_attributes(element, xsd_class)

        self.classes[class_name] = xsd_class

    def _extract_attributes(
        self, element: ET.Element, xsd_class: XsdClass
    ) -> None:
        """Extract attributes from class element.

        Args:
            element: Parent XSD element.
            xsd_class: XsdClass to populate with attributes.
        """
        # Find all xsd:element children
        for child_elem in element.findall(f".//{{{self.XSD_NS}}}element"):
            attr_name = child_elem.get("name")
            attr_type = child_elem.get("type", "")

            if not attr_name:
                continue

            # Extract qualified name for attribute
            qualified_name = self._extract_qualified_name(child_elem)

            # Convert type to CamelCase (remove AR: prefix)
            clean_type = attr_type.replace(f"{{{self.AR_NS}}}", "").replace("AR:", "")

            # Convert attribute name to CamelCase
            camel_name = self.xsd_to_camel_case(attr_name)

            # Create XsdAttribute
            xsd_attr = XsdAttribute(
                name=camel_name,
                type=clean_type,
                xsd_name=attr_name,
                qualified_name=qualified_name,
            )

            xsd_class.attributes[camel_name] = xsd_attr

    def _extract_qualified_name(self, element: ET.Element) -> Optional[str]:
        """Extract mmt.qualifiedName from appinfo tags.

        Args:
            element: XSD element to search.

        Returns:
            Qualified name string or None.
        """
        # Find appinfo with source="tags"
        for appinfo in element.findall(f".//{{{self.XSD_NS}}}appinfo[@source='tags']"):
            if appinfo.text:
                # Extract mmt.qualifiedName value
                match = re.search(r'mmt\.qualifiedName="([^"]+)"', appinfo.text)
                if match:
                    return match.group(1)
        return None

    def _build_inheritance(self, root: ET.Element) -> None:
        """Build inheritance relationships from group references.

        Args:
            root: Root XML element.
        """
        for group in root.findall(f".//{{{self.XSD_NS}}}group"):
            xsd_name = group.get("name")
            if not xsd_name:
                continue

            class_name = self.xsd_to_camel_case(xsd_name)
            if class_name not in self.classes:
                continue

            xsd_class = self.classes[class_name]

            # Find group references (indicate inheritance)
            for group_ref in group.findall(f".//{{{self.XSD_NS}}}group[@ref]"):
                ref = group_ref.get("ref", "")
                if ref.startswith("AR:"):
                    ref = ref[3:]  # Remove AR: prefix
                    base_class_name = self.xsd_to_camel_case(ref)
                    xsd_class.base_classes.append(base_class_name)

    def _build_type_lookup(self, root: ET.Element) -> None:
        """Build lookup table for XSD types.

        Args:
            root: Root XML element.
        """
        # Find all complexType and simpleType definitions
        for type_elem in root.findall(
            f".//{{{self.XSD_NS}}}complexType | .//{{{self.XSD_NS}}}simpleType"
        ):
            type_name = type_elem.get("name")
            if type_name:
                qualified_name = self._extract_qualified_name(type_elem)
                if qualified_name:
                    self._type_lookup[type_name] = qualified_name

    @staticmethod
    def xsd_to_camel_case(xsd_name: str) -> str:
        """Convert XSD UPPER-CASE-HYPENATED name to CamelCase.

        Examples:
            >>> XsdParser.xsd_to_camel_case("RETURN-VALUE-PROVISION")
            'returnValueProvision'
            >>> XsdParser.xsd_to_camel_case("ABSTRACT-ACCESS-POINT")
            'abstractAccessPoint'
            >>> XsdParser.xsd_to_camel_case("AR-OBJECT")
            'arObject'

        Args:
            xsd_name: XSD name in UPPER-CASE-HYPENATED format.

        Returns:
            Name in CamelCase format.

        Requirements:
            SWR_PARSER_00031: XSD-based validation of parsed types
        """
        # Split by hyphen
        parts = xsd_name.split("-")

        # First part lowercase, rest capitalized
        if not parts:
            return xsd_name

        result = parts[0].lower()
        for part in parts[1:]:
            result += part.capitalize()

        return result

    @staticmethod
    def camel_to_xsd_case(camel_name: str) -> str:
        """Convert CamelCase name to XSD UPPER-CASE-HYPENATED format.

        Examples:
            >>> XsdParser.camel_to_xsd_case("returnValueProvision")
            'RETURN-VALUE-PROVISION'
            >>> XsdParser.camel_to_xsd_case("abstractAccessPoint")
            'ABSTRACT-ACCESS-POINT'

        Args:
            camel_name: Name in CamelCase format.

        Returns:
            Name in UPPER-CASE-HYPENATED format.

        Requirements:
            SWR_PARSER_00031: XSD-based validation of parsed types
        """
        # Insert hyphens before uppercase letters
        result = ""
        for i, char in enumerate(camel_name):
            if i > 0 and char.isupper():
                result += "-"
            result += char.upper()

        return result