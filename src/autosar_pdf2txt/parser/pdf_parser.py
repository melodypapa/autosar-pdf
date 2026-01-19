"""PDF parser for extracting AUTOSAR class hierarchies from PDF files."""

import logging
import re
from dataclasses import dataclass, field
from io import StringIO
from typing import Dict, List, Optional, Set, Tuple

from autosar_pdf2txt.models import ATPType, AutosarAttribute, AutosarClass, AutosarPackage

logger = logging.getLogger(__name__)


@dataclass
class ClassDefinition:
    """Represents a parsed class definition from PDF.

    Requirements:
        SWR_PARSER_00005: Class Definition Data Model
        SWR_PARSER_00010: Attribute Extraction from PDF

    Attributes:
        name: The name of the class.
        package_path: Full package path (e.g., "M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior").
        is_abstract: Whether the class is abstract.
        atp_type: ATP marker type enum indicating the AUTOSAR Tool Platform marker.
        base_classes: List of base class names.
        subclasses: List of subclass names.
        note: Documentation note extracted from the Note column.
        attributes: Dictionary of class attributes (key: attribute name, value: AutosarAttribute).
    """

    name: str
    package_path: str
    is_abstract: bool
    atp_type: ATPType = ATPType.NONE
    base_classes: List[str] = field(default_factory=list)
    subclasses: List[str] = field(default_factory=list)
    note: str | None = None
    attributes: Dict[str, AutosarAttribute] = field(default_factory=dict)


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
    CLASS_PATTERN = re.compile(r"^Class\s+(.+?)(?:\s*\((abstract)\))?\s*$")
    PRIMITIVE_PATTERN = re.compile(r"^Primitive\s+(.+)$")
    ENUMERATION_PATTERN = re.compile(r"^Enumeration\s+(.+)$")
    PACKAGE_PATTERN = re.compile(r"^Package\s+(M2::)?(.+)$")
    BASE_PATTERN = re.compile(r"^Base\s+(.+)$")
    SUBCLASS_PATTERN = re.compile(r"^Subclasses\s+(.+)$")
    NOTE_PATTERN = re.compile(r"^Note\s+(.+)$")
    ATTRIBUTE_HEADER_PATTERN = re.compile(r"^Attribute\s+Type\s+Mult\.\s+Kind\s+Note$")
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

    def parse_pdf(self, pdf_path: str) -> List[AutosarPackage]:
        """Parse a PDF file and extract the package hierarchy.

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00010: Attribute Extraction from PDF

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            List of top-level AutosarPackage objects.

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

        Args:
            text: The extracted text from PDF.

        Returns:
            List of ClassDefinition objects.
        """
        class_defs: List[ClassDefinition] = []
        lines = text.split("\n")

        current_class: Optional[ClassDefinition] = None
        in_attribute_section = False
        class_definition_complete = False
        pending_attr_name: Optional[str] = None
        pending_attr_type: Optional[str] = None

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
                # Determine which pattern matched and extract class name
                if class_match:
                    raw_class_name = class_match.group(1).strip()
                    is_abstract = class_match.group(2) is not None
                elif primitive_match:
                    raw_class_name = primitive_match.group(1).strip()
                    is_abstract = False
                else:  # enumeration_match
                    # Since one of the three patterns matched, this must be not None
                    assert enumeration_match is not None  # Help mypy type checker
                    raw_class_name = enumeration_match.group(1).strip()
                    is_abstract = False

                # Finalize any pending attribute from the previous class
                # This must be done BEFORE checking if this is a valid class,
                # because the attribute header for the new class might appear
                # before we determine if the class is valid (has package path)
                if current_class is not None and pending_attr_name is not None and pending_attr_type is not None:
                    if (":" not in pending_attr_name and ";" not in pending_attr_name and
                        not pending_attr_name.isdigit() and
                        pending_attr_type not in [":", "of", "CP", "atpSplitable"]):
                        is_ref = self._is_reference_type(pending_attr_type)
                        attr = AutosarAttribute(
                            name=pending_attr_name,
                            type=pending_attr_type,
                            is_ref=is_ref
                        )
                        current_class.attributes[pending_attr_name] = attr
                    pending_attr_name = None
                    pending_attr_type = None

                # Look ahead to see if this is followed by a package path within the next 5 lines
                # This helps avoid treating page headers as new class definitions
                is_valid_class = False
                for j in range(i + 1, min(len(lines), i + 6)):
                    if self.PACKAGE_PATTERN.match(lines[j].strip()):
                        is_valid_class = True
                        break

                # Only create a new class if it's followed by a package path
                if is_valid_class:
                    # Save previous class if exists
                    if current_class is not None:
                        class_defs.append(current_class)

                    # Detect ATP patterns (only for regular Class pattern)
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

                    # Determine if abstract: explicitly marked OR clean name starts with "Abstract"
                    if class_match and class_match.group(2) is not None:
                        is_abstract = True
                    elif clean_class_name.startswith("Abstract"):
                        is_abstract = True
                    else:
                        is_abstract = False

                    current_class = ClassDefinition(
                        name=clean_class_name,
                        package_path="",
                        is_abstract=is_abstract,
                        atp_type=atp_type
                    )
                    # Reset attribute section flag and pending attributes when starting a new class
                    in_attribute_section = False
                    class_definition_complete = False
                    pending_attr_name = None
                    pending_attr_type = None
                continue

            # Check for package definition
            package_match = self.PACKAGE_PATTERN.match(line)
            if package_match and current_class is not None and not class_definition_complete:
                # Include M2 prefix if present to preserve the full package hierarchy
                m2_prefix = package_match.group(1) or ""
                package_path = package_match.group(2).strip()
                current_class.package_path = m2_prefix + package_path
                continue

            # Check for base classes
            base_match = self.BASE_PATTERN.match(line)
            if base_match and current_class is not None and not class_definition_complete:
                base_classes_str = base_match.group(1)
                current_class.base_classes = [
                    bc.strip() for bc in base_classes_str.split(",") if bc.strip()
                ]
                continue

            # Check for subclasses
            subclass_match = self.SUBCLASS_PATTERN.match(line)
            if subclass_match and current_class is not None and not class_definition_complete:
                subclasses_str = subclass_match.group(1)
                current_class.subclasses = [
                    sc.strip() for sc in subclasses_str.split(",") if sc.strip()
                ]
                continue

            # Check for note
            note_match = self.NOTE_PATTERN.match(line)
            if note_match and current_class is not None and not class_definition_complete:
                current_class.note = note_match.group(1).strip()
                continue

            # Check for attribute header
            attr_header_match = self.ATTRIBUTE_HEADER_PATTERN.match(line)
            if attr_header_match and current_class is not None:
                # Attribute section starts, parse subsequent lines as attributes
                in_attribute_section = True
                pending_attr_name = None
                pending_attr_type = None
                continue

            # Check for attribute (only if we're in the attribute section)
            if in_attribute_section and current_class is not None and line and " " in line:

                # Check if this line ends the attribute section
                # End attribute section if we encounter:
                # 1. Table header (e.g., "Table F.18: ImplementationDataType")
                # 2. Enumeration definition (e.g., "Enumeration IntervalTypeEnum")
                # 3. New class definition (handled by CLASS_PATTERN check above)
                if line.startswith("Table ") or line.startswith("Enumeration "):
                    # Finalize pending attribute before ending section
                    if pending_attr_name is not None and pending_attr_type is not None:
                        if (":" not in pending_attr_name and ";" not in pending_attr_name and
                            not pending_attr_name.isdigit() and
                            pending_attr_type not in [":", "of", "CP", "atpSplitable"]):
                            is_ref = self._is_reference_type(pending_attr_type)
                            attr = AutosarAttribute(
                                name=pending_attr_name,
                                type=pending_attr_type,
                                is_ref=is_ref
                            )
                            current_class.attributes[pending_attr_name] = attr
                        else:
                            pass  # Not adding attribute
                    in_attribute_section = False
                    class_definition_complete = True
                    pending_attr_name = None
                    pending_attr_type = None
                    continue
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
                        # This is a new attribute line
                        # Finalize any pending attribute first
                        if pending_attr_name is not None and pending_attr_type is not None:
                            # Validate and add the pending attribute
                            if (":" not in pending_attr_name and ";" not in pending_attr_name and
                                not pending_attr_name.isdigit() and
                                pending_attr_type not in [":", "of", "CP", "atpSplitable"]):
                                is_ref = self._is_reference_type(pending_attr_type)
                                attr = AutosarAttribute(
                                    name=pending_attr_name,
                                    type=pending_attr_type,
                                    is_ref=is_ref
                                )
                                current_class.attributes[pending_attr_name] = attr
                            else:
                                pass  # Not adding attribute

                        # Save as pending (might be a multi-line attribute)
                        pending_attr_name = attr_name
                        pending_attr_type = attr_type
                    elif pending_attr_name is not None and pending_attr_type is not None:
                        # This is a continuation line for the pending attribute
                        if len(words) > 0:
                            first_word = words[0]

                            # Check if this is a continuation of the attribute name
                            # Only append specific continuation words in specific contexts
                            # (e.g., "Optional" continuing "isStructWith" to make "isStructWithOptionalElement")
                            if first_word == "Optional" and pending_attr_name == "isStructWith":
                                # This is a continuation of the attribute name
                                pending_attr_name += first_word
                            elif first_word == "Element" and pending_attr_name == "isStructWithOptional":
                                # This is a continuation of the attribute name
                                pending_attr_name += first_word
                            # Otherwise it's just description continuation, ignore
                elif pending_attr_name is not None and pending_attr_type is not None:
                    # No match but we have a pending attribute, check if it's a continuation
                    words = line.split()
                    if len(words) > 0:
                        first_word = words[0]
                        # Check if this is a continuation of the attribute name
                        if first_word == "Optional" and pending_attr_name == "isStructWith":
                            # This is a continuation of the attribute name
                            pending_attr_name += first_word
                        elif first_word == "Element" and pending_attr_name == "isStructWithOptional":
                            # This is a continuation of the attribute name
                            pending_attr_name += first_word
                else:
                    # No pending attribute and no new attribute match, skip
                    continue

        # Don't forget the last class
        if current_class is not None:
            # Finalize any pending attribute
            if pending_attr_name is not None and pending_attr_type is not None:
                # Validate that this is a real attribute, not metadata
                if (":" not in pending_attr_name and ";" not in pending_attr_name and
                    not pending_attr_name.isdigit() and
                    pending_attr_type not in [":", "of", "CP", "atpSplitable"]):
                    is_ref = self._is_reference_type(pending_attr_type)
                    attr = AutosarAttribute(
                        name=pending_attr_name,
                        type=pending_attr_type,
                        is_ref=is_ref
                    )
                    current_class.attributes[pending_attr_name] = attr
                else:
                    pass  # Not adding attribute
            class_defs.append(current_class)

        return class_defs

    def _build_package_hierarchy(
        self, class_defs: List[ClassDefinition]
    ) -> List[AutosarPackage]:
        """Build AutosarPackage hierarchy from class definitions.

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building
            SWR_PARSER_00007: Top-Level Package Selection

        Args:
            class_defs: List of ClassDefinition objects.

        Returns:
            List of top-level AutosarPackage objects.
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
            parent_package: AutosarPackage | None = None

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

            # Add class to the last package
            if parent_package is not None:
                class_key = (parent_package.name, class_def.name)
                if class_key not in processed_classes:
                    autosar_class = AutosarClass(
                        name=class_def.name,
                        is_abstract=class_def.is_abstract,
                        atp_type=class_def.atp_type,
                        bases=class_def.base_classes.copy(),
                        note=class_def.note,
                        attributes=class_def.attributes.copy()
                    )
                    parent_package.add_class(autosar_class)
                    processed_classes.add(class_key)

        # Return top-level packages (those with no "::" in path)
        top_level_packages = [
            pkg
            for path, pkg in package_map.items()
            if "::" not in path and (pkg.classes or pkg.subpackages)
        ]

        return top_level_packages
