"""PDF parser for extracting AUTOSAR class hierarchies from PDF files."""

import logging
import re
from dataclasses import dataclass, field
from io import StringIO
from typing import Dict, List, Optional, Set, Tuple, Union, cast

from autosar_pdf2txt.models import (
    ATPType,
    AttributeKind,
    AutosarAttribute,
    AutosarClass,
    AutosarDoc,
    AutosarEnumLiteral,
    AutosarEnumeration,
    AutosarPackage,
    AutosarPrimitive,
)

logger = logging.getLogger(__name__)


@dataclass
class ClassDefinition:
    """Represents a parsed class definition from PDF.

    Requirements:
        SWR_PARSER_00005: Class Definition Data Model
        SWR_PARSER_00010: Attribute Extraction from PDF
        SWR_PARSER_00014: Enumeration Literal Header Recognition
        SWR_PARSER_00015: Enumeration Literal Extraction from PDF
        SWR_MODEL_00019: AUTOSAR Enumeration Type Representation
        SWR_MODEL_00024: AUTOSAR Primitive Type Representation
        SWR_PARSER_00013: Recognition of Primitive and Enumeration Class Definition Patterns

    Attributes:
        name: The name of the class, enumeration, or primitive type.
        package_path: Full package path (e.g., "M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior").
        is_abstract: Whether the type is abstract.
        atp_type: ATP marker type enum indicating the AUTOSAR Tool Platform marker.
        base_classes: List of base class names.
        subclasses: List of subclass names.
        note: Documentation note extracted from the Note column.
        attributes: Dictionary of class attributes (key: attribute name, value: AutosarAttribute).
        is_enumeration: Whether this is an enumeration type (True) or a class type (False).
        is_primitive: Whether this is a primitive type (True) or a class/enumeration type (False).
        enumeration_literals: List of enumeration literals (for enumeration types only).
    """

    name: str
    package_path: str
    is_abstract: bool
    atp_type: ATPType = ATPType.NONE
    base_classes: List[str] = field(default_factory=list)
    subclasses: List[str] = field(default_factory=list)
    note: Optional[str] = None
    attributes: Dict[str, AutosarAttribute] = field(default_factory=dict)
    is_enumeration: bool = False
    is_primitive: bool = False
    enumeration_literals: List[AutosarEnumLiteral] = field(default_factory=list)


class PdfParser:
    """Parse AUTOSAR PDF files to extract package and class hierarchies.

    Requirements:
        SWR_PARSER_00001: PDF Parser Initialization

    The parser extracts class definitions from PDF files and builds
    AutosarPackage and AutosarClass objects using pdfplumber as the
    default PDF engine.

    Usage:
        >>> parser = PdfParser()
        >>> packages = parser.parse_pdf("path/to/file.pdf")
        >>> print(len(packages))
    """

    # Regex patterns for parsing class definitions
    # SWR_PARSER_00004: Class Definition Pattern Recognition
    # SWR_PARSER_00013: Recognition of Primitive and Enumeration Class Definition Patterns
    # SWR_PARSER_00010: Attribute Extraction from PDF
    # SWR_PARSER_00012: Multi-Line Attribute Handling
    # SWR_PARSER_00014: Enumeration Literal Header Recognition
    CLASS_PATTERN = re.compile(r"^Class\s+(.+?)(?:\s*\((abstract)\))?\s*$")
    PRIMITIVE_PATTERN = re.compile(r"^Primitive\s+(.+)$")
    ENUMERATION_PATTERN = re.compile(r"^Enumeration\s+(.+)$")
    PACKAGE_PATTERN = re.compile(r"^Package\s+(M2::)?(.+)$")
    BASE_PATTERN = re.compile(r"^Base\s+(.+)$")
    SUBCLASS_PATTERN = re.compile(r"^Subclasses\s+(.+)$")
    NOTE_PATTERN = re.compile(r"^Note\s+(.+)$")
    ATTRIBUTE_HEADER_PATTERN = re.compile(r"^Attribute\s+Type\s+Mult\.\s+Kind\s+Note$")
    ENUMERATION_LITERAL_HEADER_PATTERN = re.compile(r"^Literal\s+Description$")
    ENUMERATION_LITERAL_PATTERN = re.compile(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s+(.*)$")
    ATTRIBUTE_PATTERN = re.compile(r"^(\S+)\s+(\S+)\s+.*$")
    ATP_MIXED_STRING_PATTERN = re.compile(r"<<atpMixedString>>")
    ATP_VARIATION_PATTERN = re.compile(r"<<atpVariation>>")
    ATP_MIXED_PATTERN = re.compile(r"<<atpMixed>>")

    def __init__(self) -> None:
        """Initialize the PDF parser.

        Requirements:
            SWR_PARSER_00001: PDF Parser Initialization
            SWR_PARSER_00007: PDF Backend Support - pdfplumber

        Raises:
            ImportError: If pdfplumber is not installed.
        """
        self._validate_backend()

    def _validate_backend(self) -> None:
        """Validate that pdfplumber backend is available.

        Requirements:
            SWR_PARSER_00002: Backend Validation
            SWR_PARSER_00007: PDF Backend Support - pdfplumber

        Raises:
            ImportError: If pdfplumber is not installed.
        """
        try:
            import pdfplumber as _  # noqa: F401
        except ImportError:  # pragma: no cover
            raise ImportError(
                "pdfplumber is not installed. Install it with: pip install pdfplumber"
            )

    def _is_reference_type(self, attr_type: str) -> bool:
        """Determine if an attribute type is a reference type.

        Requirements:
            SWR_PARSER_00010: Attribute Extraction from PDF

        Args:
            attr_type: The attribute type string.

        Returns:
            True if the attribute type appears to be a reference type, False otherwise.

        Reference types typically end with common AUTOSAR reference patterns:
        - Prototype (e.g., PPortPrototype, RPortPrototype)
        - Ref (e.g., InstanceRef)
        - Dependency (e.g., BswModuleDependency)
        - Trigger (e.g., Trigger)
        - Mapping (e.g., Mapping)
        - Group (e.g., ModeDeclarationGroup)
        - Set (e.g., ModeDeclarationGroupSet)
        - List (e.g., List)
        - Collection (e.g., Collection)
        """
        reference_indicators = [
            "Prototype",
            "Ref",
            "Dependency",
            "Trigger",
            "Mapping",
            "Group",
            "Set",
            "List",
            "Collection",
        ]
        return any(indicator in attr_type for indicator in reference_indicators)

    def _is_broken_attribute_fragment(
        self, attr_name: str, attr_type: str
    ) -> bool:
        """Check if an attribute is a broken fragment from multi-line PDF table formatting.

        Requirements:
            SWR_PARSER_00012: Multi-Line Attribute Handling

        Args:
            attr_name: The attribute name.
            attr_type: The attribute type.

        Returns:
            True if this is a broken fragment that should be filtered out, False otherwise.
        """
        # Continuation types that appear as attribute types in broken fragments
        continuation_types = ["data", "If", "has", "to"]

        # Fragment names that appear as attribute names in broken fragments
        fragment_names = [
            "Element",
            "SizeProfile",
            "intention",
            "ImplementationDataType",
        ]

        # Partial attribute names that are incomplete
        # Note: These are only filtered if they don't have proper type information
        partial_names = ["isStructWith"]  # Removed "dynamicArray" - it's a valid attribute

        return (
            attr_type in continuation_types
            or attr_name in fragment_names
            or attr_name in partial_names
        )

    def _is_valid_package_path(self, package_path: str) -> bool:
        """Check if a package path is valid and should be accepted.

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building

        Args:
            package_path: The package path to validate (e.g., "M2::AUTOSAR::DataTypes").

        Returns:
            True if the package path is valid, False if it should be filtered out.

        Valid package paths:
        - Contain only alphanumeric characters, underscores, and :: separators
        - Each part starts with an uppercase letter or underscore
        - No spaces or special characters (parentheses, PDF artifacts like (cid:99))
        - Parts follow PascalCase naming convention

        Invalid examples:
        - "live in various packages which do not have a common" (spaces, lowercase)
        - "can coexist in the context of a ReferenceBase.(cid:99)()" (special characters)
        """
        # Filter out paths with obvious invalid characters
        if "(" in package_path or ")" in package_path:
            return False
        if "(cid:" in package_path:
            return False
        if "." in package_path:
            return False

        # Split into parts and validate each
        parts = package_path.split("::")

        for part in parts:
            part = part.strip()

            # Empty part is invalid
            if not part:
                return False

            # Check for spaces
            if " " in part:
                return False

            # Valid package names are PascalCase or contain underscores
            # Must start with uppercase letter or underscore
            if not (part[0].isupper() or part[0] == "_"):
                return False

            # Must contain only alphanumeric characters and underscores
            if not all(c.isalnum() or c == "_" for c in part):
                return False

        return True

    def parse_pdf(self, pdf_path: str) -> AutosarDoc:
        """Parse a PDF file and extract the package hierarchy.

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00010: Attribute Extraction from PDF

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            AutosarDoc containing packages and root classes.

        Raises:
            FileNotFoundError: If the PDF file doesn't exist.
            Exception: If PDF parsing fails.
        """
        # Extract class definitions from PDF
        class_defs = self._extract_class_definitions(pdf_path)

        # Build package hierarchy from class definitions
        return self._build_package_hierarchy(class_defs)

    def _extract_class_definitions(self, pdf_path: str) -> List[ClassDefinition]:
        """Extract all class definitions from the PDF.

        Requirements:
            SWR_PARSER_00003: PDF File Parsing

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            List of ClassDefinition objects.
        """
        return self._extract_with_pdfplumber(pdf_path)

    def _extract_with_pdfplumber(self, pdf_path: str) -> List[ClassDefinition]:
        """Extract class definitions using pdfplumber.

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00007: PDF Backend Support - pdfplumber
            SWR_PARSER_00009: Proper Word Spacing in PDF Text Extraction

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            List of ClassDefinition objects.
        """
        import pdfplumber

        class_defs: List[ClassDefinition] = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                text_buffer = StringIO()

                for page in pdf.pages:
                    # Use extract_words() with x_tolerance=1 to properly extract words with spaces
                    # This fixes the issue where words are concatenated without spaces
                    words = page.extract_words(x_tolerance=1)

                    if words:
                        # Reconstruct text from words, preserving line breaks
                        # Group words by their vertical position (top coordinate)
                        current_y = None
                        for word in words:
                            text = word['text']
                            top = word['top']

                            # Check if we've moved to a new line
                            if current_y is not None and abs(top - current_y) > 5:
                                text_buffer.write("\n")

                            text_buffer.write(text + " ")
                            current_y = top

                        # Add newline after each page
                        text_buffer.write("\n")

                full_text = text_buffer.getvalue()
                class_defs = self._parse_class_text(full_text)

        except Exception as e:
            raise Exception(f"Failed to parse PDF with pdfplumber: {e}") from e

        return class_defs

    def _parse_class_text(self, text: str) -> List[ClassDefinition]:
        """Parse class definitions from extracted text.

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00012: Multi-Line Attribute Handling
            SWR_PARSER_00014: Enumeration Literal Header Recognition
            SWR_PARSER_00015: Enumeration Literal Extraction from PDF
            SWR_PARSER_00016: Enumeration Literal Section Termination
            SWR_PARSER_00013: Recognition of Primitive and Enumeration Class Definition Patterns

        Args:
            text: The extracted text from PDF.

        Returns:
            List of ClassDefinition objects.
        """
        class_defs: List[ClassDefinition] = []
        lines = text.split("\n")

        current_class: Optional[ClassDefinition] = None
        in_attribute_section = False
        in_enumeration_literal_section = False
        class_definition_complete = False
        pending_attr_name: Optional[str] = None
        pending_attr_type: Optional[str] = None
        pending_attr_multiplicity: Optional[str] = None
        pending_attr_kind: Optional[AttributeKind] = None
        pending_attr_note: Optional[str] = None

        for i, line in enumerate(lines):
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Check for class definition (multiple patterns)
            class_match = self.CLASS_PATTERN.match(line)
            primitive_match = self.PRIMITIVE_PATTERN.match(line)
            enumeration_match = self.ENUMERATION_PATTERN.match(line)

            if class_match or primitive_match or enumeration_match:
                # Finalize pending attribute before processing new class
                if current_class is not None:
                    (pending_attr_name, pending_attr_type, pending_attr_multiplicity,
                     pending_attr_kind, pending_attr_note) = self._finalize_pending_attribute(
                        current_class, pending_attr_name, pending_attr_type,
                        pending_attr_multiplicity, pending_attr_kind, pending_attr_note
                    )

                # Process class definition patterns
                result = self._process_class_definition_pattern(
                    class_match, primitive_match, enumeration_match, lines, i
                )
                if result:
                    # Save previous class if exists
                    if current_class is not None:
                        class_defs.append(current_class)

                    current_class = result
                    # Reset attribute section flag and pending attributes when starting a new class
                    in_attribute_section = False
                    in_enumeration_literal_section = False
                    class_definition_complete = False
                    pending_attr_name = None
                    pending_attr_type = None
                continue

            # Check for package definition
            package_match = self.PACKAGE_PATTERN.match(line)
            if package_match and current_class is not None and not class_definition_complete:
                self._process_package_line(package_match, current_class)
                continue

            # Check for base classes
            base_match = self.BASE_PATTERN.match(line)
            if base_match and current_class is not None and not class_definition_complete:
                self._process_base_classes_line(base_match, current_class)
                continue

            # Check for subclasses
            subclass_match = self.SUBCLASS_PATTERN.match(line)
            if subclass_match and current_class is not None and not class_definition_complete:
                self._process_subclasses_line(subclass_match, current_class)
                continue

            # Check for note
            note_match = self.NOTE_PATTERN.match(line)
            if note_match and current_class is not None and not class_definition_complete:
                self._process_note_line(note_match, lines, i, current_class)
                continue

            # Check for attribute header
            attr_header_match = self.ATTRIBUTE_HEADER_PATTERN.match(line)
            if attr_header_match and current_class is not None:
                (in_attribute_section, pending_attr_name, pending_attr_type,
                 pending_attr_multiplicity, pending_attr_kind, pending_attr_note) = self._process_attribute_header(
                    pending_attr_name, pending_attr_type, pending_attr_multiplicity,
                    pending_attr_kind, pending_attr_note
                )
                continue

            # Check for enumeration literal header
            enum_literal_header_match = self.ENUMERATION_LITERAL_HEADER_PATTERN.match(line)
            if enum_literal_header_match and current_class is not None and current_class.is_enumeration:
                in_enumeration_literal_section = True
                continue

            # Check for enumeration literal line
            if in_enumeration_literal_section and current_class is not None and current_class.is_enumeration:
                enum_section_ended = self._process_enumeration_literal_line(line, current_class)
                if enum_section_ended:
                    in_enumeration_literal_section = False
                    class_definition_complete = True
                continue

            # Check for attribute (only if we're in the attribute section)
            if in_attribute_section and current_class is not None and line and " " in line:
                attr_result: Dict[str, Union[bool, Optional[str], Optional[AttributeKind]]] = self._process_attribute_line(
                    line, current_class, pending_attr_name, pending_attr_type,
                    pending_attr_multiplicity, pending_attr_kind, pending_attr_note
                )
                if attr_result["section_ended"]:
                    in_attribute_section = False
                    class_definition_complete = True

                pending_attr_name = cast(Optional[str], attr_result["pending_attr_name"])
                pending_attr_type = cast(Optional[str], attr_result["pending_attr_type"])
                pending_attr_multiplicity = cast(Optional[str], attr_result["pending_attr_multiplicity"])
                pending_attr_kind = cast(Optional[AttributeKind], attr_result["pending_attr_kind"])
                pending_attr_note = cast(Optional[str], attr_result["pending_attr_note"])

        # Don't forget the last class
        if current_class is not None:
            # Finalize any pending attribute
            self._finalize_pending_attribute(
                current_class, pending_attr_name, pending_attr_type,
                pending_attr_multiplicity, pending_attr_kind, pending_attr_note
            )
            class_defs.append(current_class)

        return class_defs

    def _finalize_pending_attribute(
        self,
        current_class: ClassDefinition,
        pending_attr_name: Optional[str],
        pending_attr_type: Optional[str],
        pending_attr_multiplicity: Optional[str],
        pending_attr_kind: Optional[AttributeKind],
        pending_attr_note: Optional[str],
    ) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[AttributeKind], Optional[str]]:
        """Finalize a pending attribute and add it to the current class if valid.

        Requirements:
            SWR_PARSER_00012: Multi-Line Attribute Handling

        Args:
            current_class: The current class definition being processed.
            pending_attr_name: Name of the pending attribute.
            pending_attr_type: Type of the pending attribute.
            pending_attr_multiplicity: Multiplicity of the pending attribute.
            pending_attr_kind: Kind of the pending attribute.
            pending_attr_note: Note of the pending attribute.

        Returns:
            Tuple of reset pending attribute values (all None).
        """
        if pending_attr_name is not None and pending_attr_type is not None:
            if (":" not in pending_attr_name and ";" not in pending_attr_name and
                not pending_attr_name.isdigit() and
                pending_attr_type not in [":", "of", "CP", "atpSplitable"] and
                not self._is_broken_attribute_fragment(pending_attr_name, pending_attr_type)):
                is_ref = self._is_reference_type(pending_attr_type)
                kind = pending_attr_kind or (AttributeKind.REF if is_ref else AttributeKind.ATTR)
                attr = AutosarAttribute(
                    name=pending_attr_name,
                    type=pending_attr_type,
                    is_ref=is_ref,
                    multiplicity=pending_attr_multiplicity or "1",
                    kind=kind,
                    note=pending_attr_note or ""
                )
                current_class.attributes[pending_attr_name] = attr

        return (None, None, None, None, None)

    def _validate_atp_markers(self, raw_class_name: str) -> Tuple[ATPType, str]:
        """Validate ATP markers and extract ATP type and clean class name.

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition

        Args:
            raw_class_name: The raw class name that may contain ATP markers.

        Returns:
            Tuple of (atp_type, clean_class_name).

        Raises:
            ValueError: If multiple ATP markers are detected on the same class.
        """
        # Detect ATP patterns
        has_atp_mixed_string = bool(self.ATP_MIXED_STRING_PATTERN.search(raw_class_name))
        has_atp_variation = bool(self.ATP_VARIATION_PATTERN.search(raw_class_name))
        has_atp_mixed = bool(self.ATP_MIXED_PATTERN.search(raw_class_name))

        # Validate: multiple ATP markers on same class is an error
        atp_markers = []
        if has_atp_mixed_string:
            atp_markers.append("<<atpMixedString>>")
        if has_atp_variation:
            atp_markers.append("<<atpVariation>>")
        if has_atp_mixed:
            atp_markers.append("<<atpMixed>>")

        if len(atp_markers) > 1:
            logger.error(
                f"Class '{raw_class_name}' has multiple ATP markers: "
                f"{', '.join(atp_markers)}. A class cannot have multiple ATP markers."
            )
            raise ValueError(
                f"Class '{raw_class_name}' has multiple ATP markers: "
                f"{', '.join(atp_markers)}. A class cannot have multiple ATP markers."
            )

        # Determine ATP type
        if has_atp_mixed_string:
            atp_type = ATPType.ATP_MIXED_STRING
        elif has_atp_variation:
            atp_type = ATPType.ATP_VARIATION
        elif has_atp_mixed:
            atp_type = ATPType.ATP_MIXED
        else:
            atp_type = ATPType.NONE

        # Strip ATP patterns from class name
        clean_class_name = self.ATP_MIXED_STRING_PATTERN.sub("", raw_class_name)
        clean_class_name = self.ATP_VARIATION_PATTERN.sub("", clean_class_name)
        clean_class_name = self.ATP_MIXED_PATTERN.sub("", clean_class_name)
        clean_class_name = clean_class_name.strip()

        return (atp_type, clean_class_name)

    def _is_valid_class_definition(self, lines: List[str], start_index: int) -> bool:
        """Check if a class definition is valid by looking ahead for a package path.

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition

        Args:
            lines: List of text lines.
            start_index: The index to start looking from.

        Returns:
            True if a valid package path is found within the next 5 lines, False otherwise.
        """
        # Look ahead to see if this is followed by a valid package path within the next 5 lines
        # This helps avoid treating page headers as new class definitions
        for j in range(start_index + 1, min(len(lines), start_index + 6)):
            package_match = self.PACKAGE_PATTERN.match(lines[j].strip())
            if package_match:
                m2_prefix = package_match.group(1) or ""
                package_path = package_match.group(2).strip()
                full_package_path = m2_prefix + package_path
                # Only accept if the package path is valid
                if self._is_valid_package_path(full_package_path):
                    return True
        return False

    def _process_class_definition_pattern(
        self,
        class_match: Optional[re.Match],
        primitive_match: Optional[re.Match],
        enumeration_match: Optional[re.Match],
        lines: List[str],
        line_index: int,
    ) -> Optional[ClassDefinition]:
        """Process class/primitive/enumeration definition patterns and create ClassDefinition.

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00013: Recognition of Primitive and Enumeration Class Definition Patterns

        Args:
            class_match: Match object for class pattern, or None.
            primitive_match: Match object for primitive pattern, or None.
            enumeration_match: Match object for enumeration pattern, or None.
            lines: List of text lines.
            line_index: Current line index.

        Returns:
            ClassDefinition if valid, None otherwise.
        """
        # Determine which pattern matched and extract class name
        is_enumeration = False
        is_primitive = False
        if class_match:
            raw_class_name = class_match.group(1).strip()
            is_abstract = class_match.group(2) is not None
        elif primitive_match:
            raw_class_name = primitive_match.group(1).strip()
            is_abstract = False
            is_primitive = True
        else:  # enumeration_match
            # Since one of the three patterns matched, this must be not None
            assert enumeration_match is not None  # Help mypy type checker
            raw_class_name = enumeration_match.group(1).strip()
            is_abstract = False
            is_enumeration = True

        # Check if this is a valid class definition (followed by package path)
        if not self._is_valid_class_definition(lines, line_index):
            return None

        # Validate ATP markers and get clean class name
        atp_type, clean_class_name = self._validate_atp_markers(raw_class_name)

        # Determine if abstract: explicitly marked OR clean name starts with "Abstract"
        if class_match and class_match.group(2) is not None:
            is_abstract = True
        elif clean_class_name.startswith("Abstract"):
            is_abstract = True
        else:
            is_abstract = False

        return ClassDefinition(
            name=clean_class_name,
            package_path="",
            is_abstract=is_abstract,
            atp_type=atp_type,
            is_enumeration=is_enumeration,
            is_primitive=is_primitive
        )

    def _process_package_line(
        self,
        package_match: re.Match,
        current_class: ClassDefinition,
    ) -> None:
        """Process a package definition line.

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building

        Args:
            package_match: Match object for package pattern.
            current_class: The current class definition being processed.
        """
        # Include M2 prefix if present to preserve the full package hierarchy
        m2_prefix = package_match.group(1) or ""
        package_path = package_match.group(2).strip()
        full_package_path = m2_prefix + package_path

        # Validate package path before accepting it
        # This filters out descriptive text that looks like a package path
        # but contains spaces, special characters, or invalid naming
        if self._is_valid_package_path(full_package_path):
            current_class.package_path = full_package_path

    def _process_base_classes_line(
        self,
        base_match: re.Match,
        current_class: ClassDefinition,
    ) -> None:
        """Process a base classes line.

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition

        Args:
            base_match: Match object for base pattern.
            current_class: The current class definition being processed.
        """
        base_classes_str = base_match.group(1)
        current_class.base_classes = [
            bc.strip() for bc in base_classes_str.split(",") if bc.strip()
        ]

    def _process_subclasses_line(
        self,
        subclass_match: re.Match,
        current_class: ClassDefinition,
    ) -> None:
        """Process a subclasses line.

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition

        Args:
            subclass_match: Match object for subclass pattern.
            current_class: The current class definition being processed.
        """
        subclasses_str = subclass_match.group(1)
        current_class.subclasses = [
            sc.strip() for sc in subclasses_str.split(",") if sc.strip()
        ]

    def _process_note_line(
        self,
        note_match: re.Match,
        lines: List[str],
        line_index: int,
        current_class: ClassDefinition,
    ) -> None:
        """Process a note line with multi-line support.

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition

        Args:
            note_match: Match object for note pattern.
            lines: List of text lines.
            line_index: Current line index.
            current_class: The current class definition being processed.
        """
        # Notes can span multiple lines, capture all lines until we hit another pattern
        note_text = note_match.group(1).strip()

        # Look ahead to capture continuation lines (including Tags: line)
        for j in range(line_index + 1, len(lines)):
            next_line = lines[j].strip()

            # Stop if we hit another known pattern (but include Tags: line)
            # Note: Tags: should be included in the note, so we don't stop at it
            # We stop AFTER Tags: at Base, Attribute, Class, etc.
            if (next_line.startswith("Base ") or
                next_line.startswith("Subclasses ") or
                next_line.startswith("Attribute ") or
                next_line.startswith("Class ") or
                next_line.startswith("Primitive ") or
                next_line.startswith("Enumeration ") or
                next_line.startswith("Table ") or
                next_line.startswith("Package ") or
                next_line.startswith("Aggregated ")):
                break

            # Append the continuation line (including Tags: line)
            if next_line:
                note_text += " " + next_line

        current_class.note = note_text.strip()

    def _process_attribute_header(
        self,
        pending_attr_name: Optional[str],
        pending_attr_type: Optional[str],
        pending_attr_multiplicity: Optional[str],
        pending_attr_kind: Optional[AttributeKind],
        pending_attr_note: Optional[str],
    ) -> Tuple[bool, Optional[str], Optional[str], Optional[str], Optional[AttributeKind], Optional[str]]:
        """Process an attribute header line.

        Requirements:
            SWR_PARSER_00010: Attribute Extraction from PDF

        Args:
            pending_attr_name: Current pending attribute name.
            pending_attr_type: Current pending attribute type.
            pending_attr_multiplicity: Current pending attribute multiplicity.
            pending_attr_kind: Current pending attribute kind.
            pending_attr_note: Current pending attribute note.

        Returns:
            Tuple of (in_attribute_section, pending_attr_name, pending_attr_type,
                     pending_attr_multiplicity, pending_attr_kind, pending_attr_note).
        """
        # Attribute section starts, reset pending attributes
        return (True, None, None, None, None, None)

    def _process_enumeration_literal_line(
        self,
        line: str,
        current_class: ClassDefinition,
    ) -> bool:
        """Process an enumeration literal line.

        Requirements:
            SWR_PARSER_00015: Enumeration Literal Extraction from PDF
            SWR_PARSER_00016: Enumeration Literal Section Termination

        Args:
            line: The current line being processed.
            current_class: The current class definition being processed.

        Returns:
            True if the enumeration literal section ended, False otherwise.
        """
        # Check if this line ends the enumeration literal section
        if line.startswith("Table ") or line.startswith("Class ") or line.startswith("Primitive ") or line.startswith("Enumeration "):
            return True

        # Try to match enumeration literal pattern
        enum_literal_match = self.ENUMERATION_LITERAL_PATTERN.match(line)
        if enum_literal_match:
            literal_name = enum_literal_match.group(1)
            description = enum_literal_match.group(2).strip()

            # Extract index from description if present (e.g., "atp.EnumerationLiteralIndex=0")
            index = None
            index_match = re.search(r"atp\.EnumerationLiteralIndex=(\d+)", description)
            if index_match:
                index = int(index_match.group(1))
                # Remove the index tag from description
                description = re.sub(r"\s*atp\.EnumerationLiteralIndex=\d+\s*", "", description).strip()

            # Create enumeration literal
            literal = AutosarEnumLiteral(
                name=literal_name,
                index=index,
                description=description if description else None
            )
            current_class.enumeration_literals.append(literal)

        return False

    def _should_filter_attribute(
        self,
        attr_name: str,
        attr_type: str,
    ) -> bool:
        """Check if an attribute should be filtered out.

        Requirements:
            SWR_PARSER_00011: Attribute Metadata Filtering
            SWR_PARSER_00012: Multi-Line Attribute Handling

        Args:
            attr_name: The attribute name.
            attr_type: The attribute type.

        Returns:
            True if the attribute should be filtered, False otherwise.
        """
        continuation_types = ["data", "If", "has", "to", "of", "CP", "atpSplitable"]
        fragment_names = ["Element", "SizeProfile", "intention", "ImplementationDataType"]
        partial_names = ["isStructWith"]  # Always filtered - never a complete attribute

        return (
            ":" in attr_name or
            ";" in attr_name or
            attr_name.isdigit() or
            attr_type in continuation_types or
            attr_name in fragment_names or
            attr_name in partial_names
        )

    def _create_attribute_from_pending(
        self,
        attr_name: str,
        attr_type: str,
        multiplicity: str,
        kind: AttributeKind,
        note: str,
    ) -> AutosarAttribute:
        """Create an AutosarAttribute from pending attribute data.

        Requirements:
            SWR_PARSER_00010: Attribute Extraction from PDF

        Args:
            attr_name: The attribute name.
            attr_type: The attribute type.
            multiplicity: The attribute multiplicity.
            kind: The attribute kind.
            note: The attribute note.

        Returns:
            AutosarAttribute object.
        """
        is_ref = self._is_reference_type(attr_type)
        final_kind = kind or (AttributeKind.REF if is_ref else AttributeKind.ATTR)
        return AutosarAttribute(
            name=attr_name,
            type=attr_type,
            is_ref=is_ref,
            multiplicity=multiplicity or "1",
            kind=final_kind,
            note=note or ""
        )

    def _process_attribute_line(
        self,
        line: str,
        current_class: ClassDefinition,
        pending_attr_name: Optional[str],
        pending_attr_type: Optional[str],
        pending_attr_multiplicity: Optional[str],
        pending_attr_kind: Optional[AttributeKind],
        pending_attr_note: Optional[str],
    ) -> Dict[str, Union[bool, Optional[str], Optional[AttributeKind]]]:
        """Process an attribute line in the attribute section.

        Requirements:
            SWR_PARSER_00010: Attribute Extraction from PDF
            SWR_PARSER_00011: Attribute Metadata Filtering
            SWR_PARSER_00012: Multi-Line Attribute Handling

        Args:
            line: The current line being processed.
            current_class: The current class definition being processed.
            pending_attr_name: Current pending attribute name.
            pending_attr_type: Current pending attribute type.
            pending_attr_multiplicity: Current pending attribute multiplicity.
            pending_attr_kind: Current pending attribute kind.
            pending_attr_note: Current pending attribute note.

        Returns:
            Dict with keys: section_ended, pending_attr_name, pending_attr_type,
            pending_attr_multiplicity, pending_attr_kind, pending_attr_note.
        """
        result = {
            "section_ended": False,
            "pending_attr_name": pending_attr_name,
            "pending_attr_type": pending_attr_type,
            "pending_attr_multiplicity": pending_attr_multiplicity,
            "pending_attr_kind": pending_attr_kind,
            "pending_attr_note": pending_attr_note,
        }

        # Check if this line ends the attribute section
        # End attribute section if we encounter:
        # 1. Table header (e.g., "Table F.18: ImplementationDataType")
        # 2. Enumeration definition (e.g., "Enumeration IntervalTypeEnum")
        if line.startswith("Table ") or line.startswith("Enumeration "):
            # Finalize pending attribute before ending section
            if pending_attr_name is not None and pending_attr_type is not None:
                if not self._should_filter_attribute(pending_attr_name, pending_attr_type):
                    attr = self._create_attribute_from_pending(
                        pending_attr_name,
                        pending_attr_type,
                        pending_attr_multiplicity or "1",
                        pending_attr_kind or AttributeKind.ATTR,
                        pending_attr_note or ""
                    )
                    current_class.attributes[pending_attr_name] = attr

            result["section_ended"] = True
            result["pending_attr_name"] = None
            result["pending_attr_type"] = None
            result["pending_attr_multiplicity"] = None
            result["pending_attr_kind"] = None
            result["pending_attr_note"] = None
            return result

        # This might be an attribute line or continuation
        attr_match = self.ATTRIBUTE_PATTERN.match(line)
        if attr_match:
            # This is a potential attribute line
            attr_name = attr_match.group(1)
            attr_type = attr_match.group(2)
            words = line.split()

            # A real attribute line should have:
            # - Third word as multiplicity (0..1, *, 0..*) or kind (attr, aggr)
            # - Type should start with uppercase or be a valid type
            third_word = words[2] if len(words) > 2 else ""
            fourth_word = words[3] if len(words) > 3 else ""

            is_new_attribute = (
                # Third word is multiplicity or kind
                third_word in ["0..1", "0..*", "*", "attr", "aggr"] or
                # Fourth word is kind (for lines like "dynamicArray String 0..1 attr")
                fourth_word in ["attr", "aggr"]
            )

            if is_new_attribute:
                # This is a new attribute line with proper structure
                # Finalize any pending attribute first
                if pending_attr_name is not None and pending_attr_type is not None:
                    if not self._should_filter_attribute(pending_attr_name, pending_attr_type):
                        attr = self._create_attribute_from_pending(
                            pending_attr_name,
                            pending_attr_type,
                            pending_attr_multiplicity or "1",
                            pending_attr_kind or AttributeKind.ATTR,
                            pending_attr_note or ""
                        )
                        current_class.attributes[pending_attr_name] = attr

                # Save as pending (might be a multi-line attribute)
                result["pending_attr_name"] = attr_name
                result["pending_attr_type"] = attr_type

                # Extract multiplicity, kind, and note from the attribute line
                # Format: name type mult kind note
                multiplicity = "1"
                kind = AttributeKind.ATTR
                note = ""

                if len(words) > 2:
                    # Check if third word is multiplicity or kind
                    if words[2] in ["0..1", "0..*", "*"]:
                        multiplicity = words[2]
                        # Fourth word is kind
                        if len(words) > 3 and words[3] in ["attr", "aggr", "ref"]:
                            if words[3] == "attr":
                                kind = AttributeKind.ATTR
                            elif words[3] == "aggr":
                                kind = AttributeKind.AGGR
                            else:  # words[3] == "ref"
                                kind = AttributeKind.REF
                            # Fifth word onwards is note
                            if len(words) > 4:
                                note = " ".join(words[4:])
                    elif words[2] in ["attr", "aggr", "ref"]:
                        if words[2] == "attr":
                            kind = AttributeKind.ATTR
                        elif words[2] == "aggr":
                            kind = AttributeKind.AGGR
                        else:  # words[2] == "ref"
                            kind = AttributeKind.REF
                        # Third word onwards is note
                        if len(words) > 3:
                            note = " ".join(words[3:])

                result["pending_attr_multiplicity"] = multiplicity
                result["pending_attr_kind"] = kind
                result["pending_attr_note"] = note
            elif pending_attr_name is not None and pending_attr_type is not None:
                # This is a continuation line for the pending attribute
                continuation_result = self._handle_attribute_continuation(
                    words, pending_attr_name, pending_attr_note
                )
                # Update result with continuation data
                result.update(continuation_result)
        elif pending_attr_name is not None and pending_attr_type is not None:
            # No match but we have a pending attribute, check if it's a continuation
            words = line.split()
            continuation_result = self._handle_attribute_continuation(
                words, pending_attr_name, pending_attr_note
            )
            # Update result with continuation data
            result.update(continuation_result)

        return result

    def _handle_attribute_continuation(
        self,
        words: List[str],
        pending_attr_name: str,
        pending_attr_note: Optional[str],
    ) -> Dict[str, Union[Optional[str], Optional[AttributeKind], bool]]:
        """Handle continuation lines for multi-line attributes.

        Requirements:
            SWR_PARSER_00012: Multi-Line Attribute Handling

        Args:
            words: List of words in the continuation line.
            pending_attr_name: Current pending attribute name.
            pending_attr_note: Current pending attribute note.

        Returns:
            Dict with keys that should be updated (pending_attr_name, pending_attr_note).
            Note: This dict only contains keys that should be updated; other keys are preserved.
        """
        result: Dict[str, Union[Optional[str], Optional[AttributeKind], bool]] = {}

        if len(words) > 0:
            first_word = words[0]

            # Check if this is a continuation of the attribute name
            # Only append specific continuation words in specific contexts
            # (e.g., "Optional" continuing "isStructWith" to make "isStructWithOptionalElement")
            if first_word == "Optional" and pending_attr_name == "isStructWith":
                # This is a continuation of the attribute name
                result["pending_attr_name"] = pending_attr_name + first_word
            elif first_word == "Element" and pending_attr_name == "isStructWithOptional":
                # This is a continuation of the attribute name
                result["pending_attr_name"] = pending_attr_name + first_word
            else:
                # This is a continuation of the attribute note/description
                # Append the entire line to the pending note
                continuation_text = " ".join(words)
                if pending_attr_note:
                    result["pending_attr_note"] = pending_attr_note + " " + continuation_text
                else:
                    result["pending_attr_note"] = continuation_text

        return result

    def _build_package_hierarchy(
        self, class_defs: List[ClassDefinition]
    ) -> AutosarDoc:
        """Build AutosarPackage hierarchy from class definitions.

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building
            SWR_PARSER_00007: Top-Level Package Selection
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution

        Args:
            class_defs: List of ClassDefinition objects.

        Returns:
            AutosarDoc containing packages and root classes.
        """
        # Filter out class definitions without package paths
        # These are typically false positives from page headers/footers
        valid_class_defs = [cd for cd in class_defs if cd.package_path]

        # Track all packages by their full path
        package_map: Dict[str, AutosarPackage] = {}

        # Track which classes have been added to packages
        processed_classes: Set[Tuple[str, str]] = set()

        for class_def in valid_class_defs:
            # Parse package path
            package_parts = [p.strip() for p in class_def.package_path.split("::") if p.strip()]

            # Create/get packages in hierarchy
            current_path = ""
            parent_package: Optional[AutosarPackage] = None

            for part in package_parts:
                if current_path:
                    current_path += "::" + part
                else:
                    current_path = part

                # Get or create package
                if current_path not in package_map:
                    pkg = AutosarPackage(name=part)
                    package_map[current_path] = pkg

                    # Add to parent package if exists
                    if parent_package is not None:
                        parent_package.add_subpackage(pkg)

                parent_package = package_map[current_path]

            # Add class, enumeration, or primitive to the last package
            if parent_package is not None:
                class_key = (parent_package.name, class_def.name)
                if class_key not in processed_classes:
                    # SWR_MODEL_00019: AUTOSAR Enumeration Type Representation
                    # SWR_MODEL_00024: AUTOSAR Primitive Type Representation
                    # SWR_PARSER_00013: Recognition of Primitive and Enumeration Class Definition Patterns
                    # Create AutosarEnumeration for enumeration types, AutosarPrimitive for primitive types, AutosarClass for class types
                    autosar_type: Union[AutosarClass, AutosarEnumeration, AutosarPrimitive]
                    if class_def.is_enumeration:
                        autosar_type = AutosarEnumeration(
                            name=class_def.name,
                            package=class_def.package_path,
                            note=class_def.note,
                            enumeration_literals=class_def.enumeration_literals.copy()
                        )
                    elif class_def.is_primitive:
                        autosar_type = AutosarPrimitive(
                            name=class_def.name,
                            package=class_def.package_path,
                            note=class_def.note,
                            attributes=class_def.attributes.copy()
                        )
                    else:
                        autosar_type = AutosarClass(
                            name=class_def.name,
                            package=class_def.package_path,
                            is_abstract=class_def.is_abstract,
                            atp_type=class_def.atp_type,
                            bases=class_def.base_classes.copy(),
                            note=class_def.note,
                            attributes=class_def.attributes.copy()
                        )
                    parent_package.add_type(autosar_type)
                    processed_classes.add(class_key)

        # Return top-level packages (those with no "::" in path)
        top_level_packages = [
            pkg
            for path, pkg in package_map.items()
            if "::" not in path and (pkg.types or pkg.subpackages)
        ]

        # SWR_PARSER_00017: AUTOSAR Class Parent Resolution
        # After building all packages and classes, resolve parent references and collect root classes
        root_classes = self._resolve_parent_references(top_level_packages)

        return AutosarDoc(packages=top_level_packages, root_classes=root_classes)

    def _resolve_parent_references(self, packages: List[AutosarPackage]) -> List[AutosarClass]:
        """Resolve parent references for all classes in the package hierarchy.

        Requirements:
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution

        This method sets the `parent` attribute for each AutosarClass to the name
        of its immediate parent class based on the class's `bases` list.
        It also collects root classes (classes with empty bases).

        Args:
            packages: List of top-level AutosarPackage objects.

        Returns:
            List of root AutosarClass objects (classes with empty bases).
        """
        root_classes: List[AutosarClass] = []

        # Process each package and set parent references
        for pkg in packages:
            self._set_parent_references(pkg, root_classes, packages)

        return root_classes

    def _set_parent_references(self, pkg: AutosarPackage, root_classes: List[AutosarClass], all_packages: List[AutosarPackage]) -> None:
        """Recursively set parent references for all AutosarClass objects in a package.

        Requirements:
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution

        This method sets the `parent` attribute to the name of the first base class
        if it exists and is a class (not an enumeration), and collects root classes
        (classes with empty bases).

        Args:
            pkg: The package to process.
            root_classes: List to populate with root AutosarClass objects.
            all_packages: List of all top-level packages for searching base classes.
        """
        for typ in pkg.types:
            if isinstance(typ, AutosarClass):
                if typ.bases:
                    # Only set parent if the base class exists and is a class (not enumeration)
                    base_name = typ.bases[0]
                    base_class = self._find_class_in_all_packages(all_packages, base_name)
                    if base_class is not None:
                        typ.parent = base_name
                else:
                    # No bases means this is a root class
                    root_classes.append(typ)

        # Recursively process subpackages
        for subpkg in pkg.subpackages:
            self._set_parent_references(subpkg, root_classes, all_packages)

    def _find_class_in_all_packages(self, packages: List[AutosarPackage], class_name: str) -> Optional[AutosarClass]:
        """Recursively search for a class by name across all packages.

        Args:
            packages: List of top-level packages to search in.
            class_name: The name of the class to find.

        Returns:
            The AutosarClass if found, None otherwise.
        """
        for pkg in packages:
            # Check current package
            for typ in pkg.types:
                if isinstance(typ, AutosarClass) and typ.name == class_name:
                    return typ

            # Recursively search subpackages
            result = self._find_class_in_package(pkg, class_name)
            if result is not None:
                return result

        return None

    def _find_class_in_package(self, pkg: AutosarPackage, class_name: str) -> Optional[AutosarClass]:
        """Recursively search for a class by name in a package and its subpackages.

        Args:
            pkg: The package to search in.
            class_name: The name of the class to find.

        Returns:
            The AutosarClass if found, None otherwise.
        """
        # Check current package
        for typ in pkg.types:
            if isinstance(typ, AutosarClass) and typ.name == class_name:
                return typ

        # Recursively search subpackages
        for subpkg in pkg.subpackages:
            result = self._find_class_in_package(subpkg, class_name)
            if result is not None:
                return result

        return None
