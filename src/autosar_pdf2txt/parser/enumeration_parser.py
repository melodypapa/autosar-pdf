"""AutosarEnumeration parser for extracting AUTOSAR enumeration definitions from PDF files.

This module provides the specialized parser for AutosarEnumeration definitions,
including literal parsing and index extraction.

Requirements:
    SWR_PARSER_00004: Class Definition Pattern Recognition
    SWR_PARSER_00013: Recognition of Primitive and Enumeration Class Definition Patterns
    SWR_PARSER_00014: Enumeration Literal Header Recognition
    SWR_PARSER_00015: Enumeration Literal Extraction from PDF
    SWR_PARSER_00016: Enumeration Literal Section Termination
    SWR_PARSER_00025: AutosarEnumeration Specialized Parser
    SWR_PARSER_00028: Direct Model Creation by Specialized Parsers
"""

import re
from typing import List, Optional, Tuple

from autosar_pdf2txt.models import (
    AutosarEnumeration,
    AutosarEnumLiteral,
    AutosarDocumentSource,
)
from autosar_pdf2txt.parser.base_parser import AbstractTypeParser, AutosarType


class AutosarEnumerationParser(AbstractTypeParser):
    """Specialized parser for AutosarEnumeration definitions.

    This parser handles the parsing of AUTOSAR enumeration definitions from PDF files,
    including:
    - Enumeration definition pattern recognition
    - Enumeration literal header recognition
    - Enumeration literal extraction with indices
    - State management across multiple pages

    Requirements:
        SWR_PARSER_00025: AutosarEnumeration Specialized Parser
        SWR_PARSER_00028: Direct Model Creation by Specialized Parsers
    """

    def __init__(self) -> None:
        """Initialize the AutosarEnumeration parser.

        Requirements:
            SWR_PARSER_00025: AutosarEnumeration Specialized Parser
        """
        super().__init__()
        # Parsing state
        self._in_enumeration_literal_section: bool = False

    def _reset_state(self) -> None:
        """Reset parser state for a new enumeration definition.

        This method clears all state variables to ensure clean parsing
        of each new enumeration definition without interference from previous enumerations.

        Requirements:
            SWR_PARSER_00025: AutosarEnumeration Specialized Parser
        """
        self._in_enumeration_literal_section = False

    def parse_definition(
        self,
        lines: List[str],
        line_index: int,
        pdf_filename: Optional[str] = None,
        page_number: Optional[int] = None,
        autosar_standard: Optional[str] = None,
        standard_release: Optional[str] = None,
    ) -> Optional[AutosarEnumeration]:
        """Parse an enumeration definition from PDF lines.

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00013: Recognition of Primitive and Enumeration Class Definition Patterns
            SWR_MODEL_00027: AUTOSAR Source Location Representation
            SWR_PARSER_00022: PDF Source Location Extraction

        Args:
            lines: List of text lines from the PDF.
            line_index: Current line index in the lines list.
            pdf_filename: Optional PDF filename for source tracking.
            page_number: Optional page number for source tracking.
            autosar_standard: Optional AUTOSAR standard identifier for source tracking.
            standard_release: Optional AUTOSAR standard release for source tracking.

        Returns:
            The parsed AutosarEnumeration object, or None if parsing failed.
        """
        if line_index >= len(lines):
            return None

        line = lines[line_index].strip()
        enum_match = self.ENUMERATION_PATTERN.match(line)

        if not enum_match:
            return None

        # Extract enumeration name
        raw_enum_name = enum_match.group(1).strip()

        # Validate ATP markers and get clean name
        atp_type, enum_name = self._validate_atp_markers(raw_enum_name)

        # Check if this is a valid enumeration definition (followed by package path)
        if not self._is_valid_enumeration_definition(lines, line_index):
            return None

        # Extract package path
        package_path = self._extract_package_path(lines, line_index)
        if not package_path:
            return None

        # Create source location
        source = None
        if pdf_filename:
            # SWR_PARSER_00030: Use page_number directly (no default fallback)
            # Page boundary markers now ensure accurate page tracking in two-phase parsing
            # page_number should always be provided by the main loop, but check for None for safety
            if page_number is None:
                page_number = 1
            source = AutosarDocumentSource(
                pdf_file=pdf_filename,
                page_number=page_number,
                autosar_standard=autosar_standard,
                standard_release=standard_release,
            )

        # Create AutosarEnumeration directly (no intermediate ClassDefinition)
        return AutosarEnumeration(
            name=enum_name,
            package=package_path,
            source=source,
        )

    def _is_valid_enumeration_definition(self, lines: List[str], start_index: int) -> bool:
        """Check if this is a valid enumeration definition.

        A valid enumeration definition must be followed by a Package line within 3 lines.

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition

        Args:
            lines: List of text lines from the PDF.
            start_index: Starting line index.

        Returns:
            True if valid, False otherwise.
        """
        for i in range(start_index + 1, min(start_index + 4, len(lines))):
            line = lines[i].strip()
            if line.startswith("Package "):
                return True
            if line and not line.startswith("Note "):
                # Found a non-package, non-note line - invalid
                return False
        return False

    def _extract_package_path(self, lines: List[str], start_index: int) -> Optional[str]:
        """Extract package path from lines following enumeration definition.

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building

        Args:
            lines: List of text lines from the PDF.
            start_index: Starting line index.

        Returns:
            The package path, or None if not found.
        """
        for i in range(start_index + 1, min(start_index + 4, len(lines))):
            line = lines[i].strip()
            package_match = self.PACKAGE_PATTERN.match(line)
            if package_match:
                # Remove M2:: prefix if present
                package_path = package_match.group(2)
                if package_match.group(1):  # M2:: was present
                    package_path = "M2::" + package_path
                return package_path
        return None

    def continue_parsing(
        self,
        current_model: AutosarType,
        lines: List[str],
        line_index: int,
    ) -> Tuple[int, bool]:
        """Continue parsing an enumeration definition from subsequent lines.

        Requirements:
            SWR_PARSER_00014: Enumeration Literal Header Recognition
            SWR_PARSER_00015: Enumeration Literal Extraction from PDF
            SWR_PARSER_00016: Enumeration Literal Section Termination

        Args:
            current_model: The current AutosarEnumeration being parsed.
            lines: List of text lines from the PDF.
            line_index: Current line index in the lines list.

        Returns:
            Tuple of (new_line_index, is_complete) where:
            - new_line_index: The line index to continue from
            - is_complete: True if parsing is complete, False if more lines needed
        """
        # Type narrowing: current_model is always AutosarEnumeration for this parser
        assert isinstance(current_model, AutosarEnumeration)
        i = line_index
        while i < len(lines):
            line = lines[i].strip()

            if not line:
                i += 1
                continue

            # Check for enumeration literal header
            enum_literal_header_match = self.ENUMERATION_LITERAL_HEADER_PATTERN.match(line)
            if enum_literal_header_match:
                self._in_enumeration_literal_section = True
                i += 1
                continue

            # Check for new class/primitive/enumeration definition
            if (self.CLASS_PATTERN.match(line) or
                self.PRIMITIVE_PATTERN.match(line) or
                self.ENUMERATION_PATTERN.match(line)):
                # New type definition - return
                return i, True

            # Check for table (end of enumeration)
            if line.startswith("Table "):
                return i, True

            # Process enumeration literal section
            if self._in_enumeration_literal_section:
                enum_section_ended = self._process_enumeration_literal_line(line, current_model)
                if enum_section_ended:
                    self._in_enumeration_literal_section = False
                    return i, True
                i += 1
                continue

            # Check for note
            note_match = self.NOTE_PATTERN.match(line)
            if note_match:
                self._process_note_line(note_match, lines, i, current_model)
                i += 1
                continue

            i += 1

        # End of lines - return
        return i, True

    def _process_enumeration_literal_line(self, line: str, current_model: AutosarEnumeration) -> bool:
        """Process an enumeration literal line.

        Requirements:
            SWR_PARSER_00015: Enumeration Literal Extraction from PDF
            SWR_PARSER_00016: Enumeration Literal Section Termination

        Args:
            line: The literal line.
            current_model: The current AutosarEnumeration being parsed.

        Returns:
            True if the enumeration literal section ended, False otherwise.
        """
        # Check if this line ends the enumeration literal section
        if line.startswith("Table ") or line.startswith("Class ") or line.startswith("Primitive ") or line.startswith("Enumeration "):
            return True

        # Try to match enumeration literal pattern
        literal_match = self.ENUMERATION_LITERAL_PATTERN.match(line)
        if literal_match:
            literal_name = literal_match.group(1)
            literal_description = literal_match.group(2).strip()

            # Extract index from description if present
            index = self._extract_literal_index(literal_description)

            # Clean description by removing ATP marker
            if index is not None:
                import re
                literal_description = re.sub(r"\s*atp\.EnumerationLiteralIndex=\d+", "", literal_description).strip()

            # Create and add the literal
            literal = AutosarEnumLiteral(
                name=literal_name,
                description=literal_description,
                index=index,
            )
            current_model.enumeration_literals.append(literal)

        return False

    def _extract_literal_index(self, description: str) -> Optional[int]:
        """Extract literal index from description.

        Requirements:
            SWR_PARSER_00015: Enumeration Literal Extraction from PDF

        Args:
            description: The literal description.

        Returns:
            The index if found, None otherwise.
        """
        # Look for pattern like "atp.EnumerationLiteralIndex=0"
        import re
        index_pattern = re.compile(r"atp\.EnumerationLiteralIndex=(\d+)")
        match = index_pattern.search(description)
        if match:
            return int(match.group(1))
        return None

    def _process_note_line(
        self, note_match, lines: List[str], line_index: int, current_model: AutosarEnumeration
    ) -> None:
        """Process a note line and extract multi-line note text.

        Requirements:
            SWR_PARSER_00021: Multi-Line Attribute Parsing for AutosarClass

        Args:
            note_match: The regex match object.
            lines: List of text lines from the PDF.
            line_index: Current line index.
            current_model: The current AutosarEnumeration being parsed.
        """
        note_text = note_match.group(1).strip()

        # Check if note continues on next lines
        i = line_index + 1
        while i < len(lines):
            next_line = lines[i].strip()
            # Note continues if next line doesn't start with a known pattern
            if (next_line and
                not self.CLASS_PATTERN.match(next_line) and
                not self.PRIMITIVE_PATTERN.match(next_line) and
                not self.ENUMERATION_PATTERN.match(next_line) and
                not self.PACKAGE_PATTERN.match(next_line) and
                not self.NOTE_PATTERN.match(next_line) and
                not self.ENUMERATION_LITERAL_HEADER_PATTERN.match(next_line)):
                note_text += " " + next_line
                i += 1
            else:
                break

        current_model.note = note_text.strip()