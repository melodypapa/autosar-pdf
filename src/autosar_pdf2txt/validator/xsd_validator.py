"""XSD validator for AUTOSAR class definitions.

This module validates and auto-corrects parsed AUTOSAR classes
against the XSD schema definition.

Requirements:
    SWR_PARSER_00031: XSD-based validation of parsed types
"""

import logging
from typing import Dict, List, Optional, Set

from autosar_pdf2txt.models import AutosarClass
from autosar_pdf2txt.validator.xsd_parser import XsdClass, XsdAttribute


logger = logging.getLogger(__name__)


class XsdValidator:
    """Validator for AUTOSAR classes against XSD schema.

    Validates class definitions and auto-corrects common parsing errors
    in attribute names and types.

    Requirements:
        SWR_PARSER_00031: XSD-based validation of parsed types
    """

    # Common type corrections (invalid type -> correct type)
    TYPE_CORRECTIONS: Dict[str, str] = {
        "SwComponent": "SwComponentType",
        "SwcService": "ServiceSwComponentType",
        "MultiLanguageOverview": "MultiLanguageOverview",
        "Communication": "PortInterface",
        "CompositionSw": "CompositionSwComponentType",
        "ApplicationComposite": "ApplicationCompositeDataType",
        "DiagnosticRequest": "DiagnosticRequest",
        "RootSwComposition": "CompositionSwComponentType",
        "EOCExecutableEntity": "ExecutableEntity",
        "EthernetPhysical": "EthernetPhysicalChannel",
        "AbstractRequiredPort": "RequiredPortPrototype",
        "AbstractProvidedPort": "ProvidedPortPrototype",
        "AtomicSwComponent": "AtomicSwComponentType",
        "MultilanguageLong": "MultilanguageLongName",
        "IntegerBit": "Integer",
        "ImplementationData": "ImplementationDataType",
        "PostBuildVariant": "VariationPoint",
        "DiagnosticFunction": "DiagnosticService",
        "CryptoService": "CryptoServicePrimitive",
        "AbstractImplementation": "ImplementationDataType",
    }

    def __init__(self, xsd_classes: Dict[str, XsdClass]) -> None:
        """Initialize XSD validator.

        Args:
            xsd_classes: Dictionary of XSD class definitions from XsdParser.
        """
        self.xsd_classes = xsd_classes
        self._attribute_cache: Dict[str, Set[str]] = {}

    def validate_and_correct_class(
        self, cls: AutosarClass
    ) -> List[str]:
        """Validate and correct a class against XSD.

        Validates the class definition and auto-corrects common parsing errors
        in attribute names and types. Returns a list of corrections made.

        Args:
            cls: AutosarClass to validate and correct.

        Returns:
            List of correction messages describing what was fixed.
        """
        corrections: List[str] = []

        # Skip validation if class not in XSD
        if cls.name not in self.xsd_classes:
            return corrections

        xsd_class = self.xsd_classes[cls.name]

        # Get all XSD attributes (including inherited)
        xsd_attrs = self._get_all_xsd_attributes(xsd_class)

        # Validate and correct each attribute
        for attr_name, attr in list(cls.attributes.items()):
            # Auto-correct attribute name
            corrected_name = self._correct_attribute_name(
                attr_name, xsd_attrs, cls.name
            )
            if corrected_name != attr_name:
                corrections.append(
                    f"Renamed attribute '{cls.name}.{attr_name}' → '{corrected_name}'"
                )
                # Update attribute in class
                cls.attributes[corrected_name] = cls.attributes.pop(attr_name)

            # Auto-correct attribute type
            corrected_type = self._correct_attribute_type(attr.type, cls.name, corrected_name)
            if corrected_type != attr.type:
                corrections.append(
                    f"Fixed type for '{cls.name}.{corrected_name}': '{attr.type}' → '{corrected_type}'"
                )
                attr.type = corrected_type

        return corrections

    def _get_all_xsd_attributes(
        self, xsd_class: XsdClass, visited: Optional[Set[str]] = None
    ) -> Dict[str, XsdAttribute]:
        """Get all XSD attributes including inherited ones.

        Traverses the inheritance chain to collect attributes from
        base classes. Handles diamond inheritance.

        Args:
            xsd_class: XSD class to get attributes from.
            visited: Set of already visited classes (for diamond inheritance).

        Returns:
            Dictionary of all attributes keyed by name.
        """
        if visited is None:
            visited = set()

        # Check for circular inheritance
        if xsd_class.name in visited:
            return {}
        visited.add(xsd_class.name)

        # Start with own attributes
        attrs = dict(xsd_class.attributes)

        # Add attributes from base classes
        for base_name in xsd_class.base_classes:
            if base_name in self.xsd_classes:
                base_class = self.xsd_classes[base_name]
                base_attrs = self._get_all_xsd_attributes(base_class, visited)
                attrs.update(base_attrs)

        return attrs

    def _correct_attribute_name(
        self, attr_name: str, xsd_attrs: Dict[str, XsdAttribute], class_name: str
    ) -> str:
        """Correct attribute name based on XSD definition.

        Checks if the attribute name exists in XSD attributes.
        If not, tries to find a similar name using fuzzy matching.

        Args:
            attr_name: Current attribute name.
            xsd_attrs: Dictionary of XSD attributes.
            class_name: Name of the class (for logging).

        Returns:
            Corrected attribute name (or original if no correction needed).
        """
        # Direct match - no correction needed
        if attr_name in xsd_attrs:
            return attr_name

        # Try case-insensitive match
        attr_lower = attr_name.lower()
        for xsd_attr_name in xsd_attrs:
            if xsd_attr_name.lower() == attr_lower:
                return xsd_attr_name

        # Try to find similar name by checking XSD names
        # Convert attr_name to XSD format and check
        for xsd_attr in xsd_attrs.values():
            if xsd_attr.xsd_name.lower().replace("-", "") == attr_lower.replace(
                "_", ""
            ).replace("-", ""):
                return xsd_attr.name

        # No correction found, return original
        return attr_name

    def _correct_attribute_type(
        self, attr_type: str, class_name: str, attr_name: str
    ) -> str:
        """Correct attribute type based on common patterns.

        Applies known type corrections and validates against XSD.

        Args:
            attr_type: Current attribute type.
            class_name: Name of the class.
            attr_name: Name of the attribute.

        Returns:
            Corrected type name.
        """
        # Check for known corrections
        if attr_type in self.TYPE_CORRECTIONS:
            return self.TYPE_CORRECTIONS[attr_type]

        # Try to find type in XSD classes
        if attr_type in self.xsd_classes:
            return attr_type

        # Try case-insensitive match
        attr_type_lower = attr_type.lower()
        for xsd_class_name in self.xsd_classes:
            if xsd_class_name.lower() == attr_type_lower:
                return xsd_class_name

        # Try to find similar type by checking XSD names
        for xsd_class in self.xsd_classes.values():
            if (
                xsd_class.xsd_name.lower().replace("-", "")
                == attr_type_lower.replace("_", "").replace("-", "")
            ):
                return xsd_class.name

        # No correction found, return original
        return attr_type