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
    SWR_PARSER_00036: Table-Based Enumeration Literal Extraction
"""

import logging
import re
from typing import TYPE_CHECKING, Any, Dict, List, Match, Optional, Tuple

from autosar_pdf2txt.models import (
    AutosarEnumeration,
    AutosarEnumLiteral,
)
from autosar_pdf2txt.parser.base_parser import AbstractTypeParser, AutosarType

if TYPE_CHECKING:
    import pdfplumber
else:
    pdfplumber: Any = None  # type: ignore

logger = logging.getLogger(__name__)


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
        # Collecting tags mode (when we see "Tags:" header)
        self._collecting_tags: bool = False
        # Buffer to collect tag lines
        self._tag_lines: List[str] = []
        # Temporary list to collect literals during parsing (converted to tuple at end)
        self._pending_literals: List[AutosarEnumLiteral] = []

    def _reset_state(self) -> None:
        """Reset parser state for a new enumeration definition.

        This method clears all state variables to ensure clean parsing
        of each new enumeration definition without interference from previous enumerations.

        Requirements:
            SWR_PARSER_00025: AutosarEnumeration Specialized Parser
        """
        self._in_enumeration_literal_section = False
        self._collecting_tags = False
        self._tag_lines = []
        self._pending_literals = []

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
        # Reset state for new enumeration
        self._pending_literals = []

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

        # Extract package path (standard approach)
        package_path = self._extract_package_path(lines, line_index)

        # Check if this is a valid enumeration definition (followed by package path)
        is_valid = self._is_valid_type_definition(lines, line_index)

        # Return None if enumeration definition is not valid (missing package path)
        if not is_valid or not package_path:
            return None

        # Create source location
        source = self._create_source_location(
            pdf_filename, page_number, autosar_standard, standard_release
        )

        # Create AutosarEnumeration directly (no intermediate ClassDefinition)
        return AutosarEnumeration(
            name=enum_name,
            package=package_path,
            sources=[source] if source else [],
        )

    def continue_parsing(
        self,
        current_model: AutosarType,
        lines: List[str],
        line_index: int,
        page_objects: Optional[Dict[int, Any]] = None,
        current_page: int = 1,
    ) -> Tuple[int, bool]:
        """Continue parsing an enumeration definition from subsequent lines.

        Requirements:
            SWR_PARSER_00014: Enumeration Literal Header Recognition
            SWR_PARSER_00015: Enumeration Literal Extraction from PDF
            SWR_PARSER_00016: Enumeration Literal Section Termination
            SWR_PARSER_00036: Table-Based Enumeration Literal Extraction

        Args:
            current_model: The current AutosarEnumeration being parsed.
            lines: List of text lines from the PDF.
            line_index: Current line index in the lines list.
            page_objects: Optional dictionary of page objects for table extraction.
            current_page: Current page number being parsed.

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

                # Try table-based extraction if page objects are available
                if page_objects and current_page in page_objects:
                    # Extract and process table from current page
                    table_extracted = self._extract_and_process_enumeration_table(
                        page_objects[current_page], current_model
                    )
                    if table_extracted:
                        # Table was successfully extracted and processed
                        # Skip to end of page to avoid reprocessing table content as text lines
                        # Move to next page marker or end of lines
                        while i < len(lines) and not lines[i].strip().startswith("<<<PAGE:"):
                            i += 1
                        self._in_enumeration_literal_section = False
                        self._finalize_enumeration(current_model)
                        return i, True

                    # Table extraction failed - fall through to line-based parsing below
                    logger.info(f"Table extraction failed on page {current_page}, falling back to line-based parsing")

                # Fall back to line-based parsing if table extraction not available/failed
                i += 1
                continue

            # Check for new class/primitive/enumeration definition
            if self._is_new_type_definition(line):
                # Special case: Multi-page enumeration continuation
                # If we're in the literal section and see "Enumeration <same_name>", it's a continuation
                if self._in_enumeration_literal_section:
                    enum_match = self.ENUMERATION_PATTERN.match(line)
                    if enum_match:
                        enum_name = enum_match.group(1).strip()
                        # Check if this is the same enumeration we're currently parsing
                        if isinstance(current_model, AutosarEnumeration) and current_model.name == enum_name:
                            # Same enumeration - this is a multi-page continuation
                            # Skip the "Enumeration <name>" line and continue processing
                            i += 1
                            continue

                # Not a multi-page continuation - finalize and return
                self._finalize_enumeration(current_model)
                return i, True

            # Check for table (end of enumeration)
            if self._is_table_marker(line):
                self._finalize_enumeration(current_model)
                return i, True

            # Process enumeration literal section (line-based fallback)
            if self._in_enumeration_literal_section:
                enum_section_ended = self._process_enumeration_literal_line(line, current_model)
                if enum_section_ended:
                    self._in_enumeration_literal_section = False
                    self._finalize_enumeration(current_model)
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

        # End of lines - finalize and return
        self._finalize_enumeration(current_model)

        # If in enumeration literal section, return False to allow multi-page continuation
        # Requirements: SWR_PARSER_00032: Multi-page Enumeration Literal List Support
        if self._in_enumeration_literal_section:
            return i, False  # More literals expected on next page
        else:
            return i, True   # Complete

    def _finalize_enumeration(self, current_model: AutosarEnumeration) -> None:
        """Finalize the enumeration by converting pending literals to tuple.

        This method is called when enumeration parsing is complete to convert
        the temporarily collected literals into an immutable tuple.

        Requirements:
            SWR_PARSER_00015: Enumeration Literal Extraction from PDF
            SWR_MODEL_00019: AUTOSAR Enumeration Type Representation

        Args:
            current_model: The current AutosarEnumeration being parsed.
        """
        # Apply any pending tags before finalizing
        if self._collecting_tags and self._pending_literals and self._tag_lines:
            self._apply_collected_tags()

        # Convert pending literals to immutable tuple
        current_model.enumeration_literals = tuple(self._pending_literals)
        self._pending_literals = []

    def _extract_and_process_enumeration_table(
        self, page: Any, current_model: AutosarEnumeration
    ) -> bool:
        """Extract and process enumeration table from PDF page.

        This method uses pdfplumber's extract_tables() to directly extract
        the enumeration literal table, preserving column structure.
        This is more robust than line-based parsing.

        Supports two table formats:
        1. Tables with "Literal Description" headers (possibly after Package/Note rows)
        2. Direct format tables starting with "Enumeration <name>" followed by literal rows

        Requirements:
            SWR_PARSER_00036: Table-Based Enumeration Literal Extraction

        Args:
            page: The pdfplumber Page object containing the enumeration table.
            current_model: The current AutosarEnumeration being parsed.

        Returns:
            True if table was successfully extracted and processed, False otherwise.
        """
        try:
            # Extract all tables from the page
            tables = page.extract_tables()
            if not tables:
                logger.info("No tables found on page")
                return False

            logger.info(f"Found {len(tables)} table(s) on page")

            # Find the enumeration literal table
            # Look for a table with "Literal" and "Description" columns
            # OR a table that starts with "Enumeration <current_name>"
            for table_idx, table in enumerate(tables):
                if not table or len(table) < 2:  # Need at least header + 1 row
                    continue

                logger.info(f"Table {table_idx}: {len(table)} rows")

                # Find the header row with "Literal" and "Description"
                # The header may not be row 0 - it could be after other rows like "Package", "Note", etc.
                header_row_idx = None
                header = None
                literal_col_idx = None
                description_col_idx = None

                for row_idx, row in enumerate(table):
                    if not row or len(row) < 2:
                        continue

                    # Normalize row values
                    normalized_row = [str(cell).strip().lower() if cell else "" for cell in row]

                    # Check if this row contains "Literal" and "Description"
                    has_literal = any("literal" in col for col in normalized_row)
                    has_description = any("description" in col or "desc" in col for col in normalized_row)

                    if has_literal and has_description:
                        header_row_idx = row_idx
                        header = normalized_row
                        logger.info(f"Table {table_idx}: Found header at row {row_idx}: {row}")

                        # Find column indices
                        for col_idx, col in enumerate(header):
                            if "literal" in col:
                                literal_col_idx = col_idx
                            elif "description" in col or "desc" in col:
                                description_col_idx = col_idx
                        break

                if header_row_idx is None:
                    logger.info(f"Table {table_idx} skipped: no literal/description header found")
                    continue

                if literal_col_idx is None or description_col_idx is None:
                    logger.info(f"Table {table_idx} skipped: missing required columns")
                    continue

                # Check if this table is for the current enumeration
                # Look for the enumeration name in the rows before the header
                is_correct_table = False
                for row in table[:header_row_idx]:
                    if row and len(row) >= 2:
                        row_str = [str(cell).strip() if cell else "" for cell in row]
                        # Check if any row contains "Enumeration" and the current enumeration name
                        if any("Enumeration" in col for col in row_str):
                            # Check if the enumeration name matches
                            if any(current_model.name in col for col in row_str):
                                is_correct_table = True
                                logger.info(f"Table {table_idx} confirmed for enumeration '{current_model.name}'")
                                break

                if not is_correct_table:
                    logger.info(f"Table {table_idx} skipped: not for enumeration '{current_model.name}'")
                    continue

                logger.info(f"Table {table_idx} looks like enumeration literal table")
                logger.info(f"Processing table {table_idx}: literal_col={literal_col_idx}, desc_col={description_col_idx}, header_row={header_row_idx}")

                # Check for tags column (optional)
                tags_col_idx: Optional[int] = None
                if header:
                    for col_idx, col in enumerate(header):
                        if col and ("tag" in col or "note" in col):
                            tags_col_idx = col_idx
                            break

                # If we couldn't find tags column and there are 3+ columns, assume third column
                if tags_col_idx is None and header is not None and len(header) >= 3:
                    tags_col_idx = 2

                logger.info(f"Tags column: {tags_col_idx}")

                # Process data rows (start from row after header)
                processed_count = 0
                for row_idx, row in enumerate(table[header_row_idx + 1:], start=header_row_idx + 1):
                    if not row or len(row) <= max(literal_col_idx, description_col_idx):
                        continue

                    # Extract literal name
                    literal_name = row[literal_col_idx]
                    if literal_name:
                        # Convert to string and handle multi-line cells
                        # Table cells may contain literal names split across lines
                        # e.g., "reportingIn\nChronlogicalOrder\nOldestFirst"
                        # We need to combine these by removing the newlines
                        literal_name = str(literal_name).strip()
                        # Remove newlines to combine multi-line literal names
                        literal_name = literal_name.replace('\n', '')
                    else:
                        continue

                    # Skip empty rows or header-like rows
                    if not literal_name or literal_name.lower() in ["literal", "description", ""]:
                        continue

                    # Extract description
                    description = None
                    if description_col_idx < len(row) and row[description_col_idx]:
                        description = str(row[description_col_idx]).strip()
                        # Replace newlines with spaces in descriptions
                        description = description.replace('\n', ' ')

                    # Extract tags (from tags column if present, or from description)
                    tags_text = ""
                    if tags_col_idx is not None and tags_col_idx < len(row) and row[tags_col_idx]:
                        tags_text = str(row[tags_col_idx]).strip()
                        logger.debug(f"Row {row_idx}: tags from column {tags_col_idx}: {tags_text[:100]}")
                    elif description:
                        # Tags might be embedded in description
                        tags_text = description
                        logger.debug(f"Row {row_idx}: tags from description: {tags_text[:100]}")

                    # Parse tags
                    tags = self._extract_literal_tags(tags_text)
                    if tags:
                        logger.debug(f"Row {row_idx}: extracted tags: {tags}")
                    else:
                        logger.debug(f"Row {row_idx}: no tags found")

                    # Extract value from atp.EnumerationLiteralIndex
                    value = None
                    if "atp.EnumerationLiteralIndex" in tags:
                        try:
                            value = int(tags["atp.EnumerationLiteralIndex"])
                        except (ValueError, TypeError):
                            pass

                    # Clean description by removing all tag patterns
                    clean_description = description if description else ""
                    if description:
                        if "atp.EnumerationLiteralIndex" in tags:
                            clean_description = re.sub(r"\s*atp\.EnumerationLiteralIndex=\d+", "", clean_description)
                        if "xml.name" in tags:
                            clean_description = re.sub(r"\s*xml\.name=[^\s,]+", "", clean_description)
                        clean_description = clean_description.strip()

                    # Create literal
                    literal = AutosarEnumLiteral(
                        name=literal_name,
                        description=clean_description if clean_description else None,
                        value=value,
                        index=value,
                        tags=tags,
                    )
                    logger.info(f"Created literal: name='{literal_name}', index={value}, tags={list(tags.keys())}")
                    self._pending_literals.append(literal)
                    processed_count += 1

                logger.debug(f"Table {table_idx}: processed {processed_count} literals")

                # Successfully processed table
                if processed_count > 0:
                    logger.info(f"Successfully extracted {processed_count} enumeration literals from table")
                    return True
                else:
                    logger.debug(f"Table {table_idx} found but no literals extracted")
                    return False

            # Fallback: Check if any table matches "Enumeration <current_name>" direct format
            # This handles tables without "Literal Description" headers
            first_row = table[0] if table else []
            if (first_row and len(first_row) >= 2 and
                str(first_row[0]).strip() == "Enumeration" and
                current_model.name in str(first_row[1])):
                # This table contains literals for the current enumeration in direct format
                # Format: Row 0 is "Enumeration <name>", subsequent rows are [literal, description]
                logger.info(f"Table {table_idx} matches enumeration '{current_model.name}' (direct format)")

                # Process rows starting from row 1
                processed_count = 0
                for row_idx, row in enumerate(table[1:], start=1):
                    if not row or len(row) < 2:
                        continue

                    # Extract literal name (column 0)
                    literal_name = row[0]
                    if literal_name:
                        literal_name = str(literal_name).strip().replace('\n', '')
                    else:
                        continue

                    # Skip empty rows or non-literal rows (Package, Note, Aggregatedby)
                    if not literal_name or literal_name in ["Package", "Note", "Aggregatedby", "Literal"]:
                        continue

                    # Extract description (column 1)
                    description = None
                    if len(row) > 1 and row[1]:
                        description = str(row[1]).strip().replace('\n', ' ')

                    # Extract tags from description
                    tags = self._extract_literal_tags(description) if description else {}

                    # Extract value from atp.EnumerationLiteralIndex
                    literal_value: Optional[int] = None
                    if "atp.EnumerationLiteralIndex" in tags:
                        try:
                            literal_value = int(tags["atp.EnumerationLiteralIndex"])
                        except (ValueError, TypeError):
                            pass

                    # Clean description by removing tag patterns
                    clean_literal_description: Optional[str] = None
                    if description:
                        clean_literal_description = description
                        if "atp.EnumerationLiteralIndex" in tags:
                            clean_literal_description = re.sub(r"\s*atp\.EnumerationLiteralIndex=\d+", "", clean_literal_description)
                        if "xml.name" in tags:
                            clean_literal_description = re.sub(r"\s*xml\.name=[^\s,]+", "", clean_literal_description)
                        clean_literal_description = clean_literal_description.strip()

                    # Create literal
                    literal = AutosarEnumLiteral(
                        name=literal_name,
                        description=clean_literal_description if clean_literal_description else None,
                        value=literal_value,
                        index=literal_value,
                        tags=tags,
                    )
                    logger.info(f"Created literal: name='{literal_name}', index={literal_value}")
                    self._pending_literals.append(literal)
                    processed_count += 1

                if processed_count > 0:
                    logger.info(f"Successfully extracted {processed_count} literals from direct-format table")
                    return True

        except Exception as e:
            # Table extraction failed - fall back to line-based parsing
            logger.warning(f"Table extraction failed: {e}, falling back to line-based parsing")
            return False

        # If we get here, no suitable table was found
        logger.info(f"No suitable enumeration literal table found for '{current_model.name}'")
        return False

    def _process_enumeration_literal_line(self, line: str, current_model: AutosarEnumeration) -> bool:
        """Process a line in the enumeration literal section.

        This method handles the parsing of enumeration literal lines, including
        multi-line names, descriptions, and tags. It supports 5 different patterns
        of enumeration literal formatting found in AUTOSAR PDF specifications.

        This is the fallback when table-based extraction fails.

        Args:
            line: The line to process.
            current_model: The current enumeration model being built.

        Returns:
            True if the enumeration literal section ended, False otherwise.
        """
        # Check if this line ends the enumeration literal section
        if line.startswith("Table ") or line.startswith("Class ") or line.startswith("Primitive ") or line.startswith("Enumeration "):
            return True

        # If we're collecting tags, check if this line is a tag line
        if self._collecting_tags:
            # Check if this line is a new literal (ends tag collection)
            literal_match_check = self.ENUMERATION_LITERAL_PATTERN.match(line)
            if literal_match_check:
                literal_name_check = literal_match_check.group(1)
                literal_desc_check = literal_match_check.group(2)
                literal_desc_check = literal_desc_check.strip() if literal_desc_check else None

                # Special case: If previous literal doesn't have index yet OR we're still collecting tag lines,
                # this literal name might be a continuation of the multi-line name (e.g., "reportingIn ChronlogicalOrder OldestFirst")
                if (self._pending_literals and
                    (self._pending_literals[-1].index is None or self._tag_lines) and
                    not literal_desc_check):
                    # This is a continuation of the previous literal's name
                    self._pending_literals[-1].name += literal_name_check
                    # Continue collecting - this line is part of the name, not a new literal
                    return False

                # This is a new literal - apply collected tags to previous literal
                if self._pending_literals and self._tag_lines:
                    self._apply_collected_tags()
                # Exit tag collection mode
                self._collecting_tags = False
                self._tag_lines = []
                # Continue processing this line as a new literal below
            else:
                # Not a literal line - add to tag collection if not empty
                if line.strip():
                    self._tag_lines.append(line.strip())
                return False

        # Special handling for "Tags:" lines
        # These lines indicate that tag information follows on subsequent lines
        # The actual tags are on the lines following "Tags:" (or on the same line)
        # They don't match the ENUMERATION_LITERAL_PATTERN because they have a colon
        if line.strip().startswith("Tags:"):
            # Enter tag collection mode
            self._collecting_tags = True
            self._tag_lines = []

            # Extract tag content from the same line (after "Tags:")
            tag_content = line.strip()[5:].strip()  # Remove "Tags:" prefix
            if tag_content:
                # Tags are on the same line as "Tags:"
                self._tag_lines.append(tag_content)
            return False

        # Try to match enumeration literal pattern
        literal_match = self.ENUMERATION_LITERAL_PATTERN.match(line)
        if literal_match:
            literal_name = literal_match.group(1)
            literal_description = literal_match.group(2).strip() if literal_match.group(2) else ""

            # Type annotation for previous_literal (used in multiple branches below)
            previous_literal: Optional[AutosarEnumLiteral]

            # Common continuation words that indicate multi-line descriptions
            # These are fragments that should be appended to the previous literal
            continuation_words = {
                "enable", "qualification", "the", "condition", "conditions",
                "of", "or", "and", "with", "will", "after", "related", "all",
                "first", "last", "on", "in", "out", "up", "down"  # Common suffix words for Pattern 2/5
            }

            # Check if this is a continuation line (multi-line description or multi-line literal name)
            is_continuation = False
            append_to_name = False  # Flag to indicate if we should append to name instead of description
            if self._pending_literals:
                # Check if this is the same literal name (duplicate indicates continuation)
                if literal_name == self._pending_literals[-1].name:
                    # Check if previous literal already has tags (index is not None)
                    # If it does, this is a NEW literal with same base name (Pattern 2/5)
                    if self._pending_literals[-1].index is not None:
                        is_continuation = False  # Don't treat as continuation, will create new literal below
                    else:
                        is_continuation = True
                # Check if the "name" is a common continuation word or starts with one
                elif (literal_name.lower() in continuation_words or
                      any(literal_name.lower().startswith(word) for word in ["first", "last", "on", "in", "out", "up", "down"])):
                    # If it's a suffix word (First, Last, On, In, etc.), append to name
                    if (literal_name.lower() in {"first", "last", "on", "in", "out", "up", "down"} or
                        any(literal_name.lower().startswith(word) for word in ["first", "last", "on", "in", "out", "up", "down"])):
                        is_continuation = True
                        append_to_name = True
                    else:
                        is_continuation = True
                # Check if description starts with lowercase (indicates continuation)
                # EXCEPT if it contains tag patterns (like "atp.EnumerationLiteralIndex")
                elif (literal_description and
                      literal_description[0].islower() and
                      "atp.EnumerationLiteralIndex" not in literal_description and
                      "xml.name" not in literal_description):
                    is_continuation = True
            
            if is_continuation and self._pending_literals:
                if append_to_name:
                    # Append to previous literal's name (for Pattern 2/5)
                    self._pending_literals[-1].name += literal_name
                else:
                    # Append to previous literal's description
                    previous_literal = self._pending_literals[-1]  # Safe: guarded by self._pending_literals check above
                    # Initialize description if None
                    if previous_literal.description is None:
                        previous_literal.description = ''
                    # Add a space before appending if needed
                    if not previous_literal.description.endswith(' '):
                        previous_literal.description += ' '
                    # Append the continuation text (include the "name" as it's part of the description)
                    continuation_text = f"{literal_name} {literal_description}" if literal_description else literal_name
                    previous_literal.description += continuation_text
                return False  # Important: return False to prevent further processing
            else:
                # Distinguish between Pattern 3 (combined names) and Pattern 2/5 (separate literals)
                previous_literal = self._pending_literals[-1] if self._pending_literals else None

                # Check for multi-line literal name scenario (enum3.png from master):
                # When consecutive lines have the same description and the literal name
                # continues the previous name (e.g., "reportingIn", "ChronologicalOrder", "OldestFirst")
                # Also handle case where first line has description and subsequent lines don't
                is_multiline_name = False
                if (literal_description and previous_literal and previous_literal.description and
                      literal_description == previous_literal.description):
                    # Pattern: Same description on multiple lines
                    is_multiline_name = True
                elif (not literal_description and previous_literal and previous_literal.description and
                      previous_literal.index is None):
                    # Pattern: First line has description, subsequent lines don't
                    # AND previous literal doesn't have index yet (still being built)
                    # This is a continuation of the previous literal's name
                    is_multiline_name = True

                if is_multiline_name:
                    # Append to previous literal's name (stacked names with same description)
                    self._pending_literals[-1].name += literal_name
                    # Don't create a new literal, continue processing
                    return False

                # Check if this is Pattern 2/5 (separate literal):
                # - Previous literal has tags and index (complete)
                # - Current description is a real description (not just "Tags:")
                # - Previous literal has index tag
                # - Current name is NOT a small suffix word (which would be Pattern 3)
                # - Names are different (or same base name for Pattern 2)
                # - NOT a continuation line (append_to_name=False)
                # OR:
                # - Previous literal exists (with or without tags)
                # - Current description starts with uppercase (indicates new literal)
                # - Names are different
                # - NOT a continuation line (append_to_name=False)
                # - NOT a continuation word (in continuation_words set)
                is_new_literal_by_tags = (
                    previous_literal and
                    previous_literal.tags and
                    previous_literal.index is not None and
                    literal_description and
                    literal_description != "Tags:" and
                    "atp.EnumerationLiteralIndex" in previous_literal.tags and
                    not append_to_name and  # Not a continuation line (append_to_name=False)
                    # Only treat as Pattern 2/5 if name is NOT a small suffix word (First, Last, etc.)
                    (len(literal_name) > 5 or literal_name not in {"first", "last", "on", "in", "out", "up", "down"})
                )
                is_new_literal_by_uppercase = (
                    previous_literal and
                    not is_continuation and  # NOT a continuation line (important!)
                    not append_to_name and  # Not a continuation line (append_to_name=False)
                    literal_description and
                    not literal_description.startswith("Tags:") and  # Not starting with "Tags:" (Pattern 3)
                    literal_description[0].isupper() and  # Starts with uppercase
                    literal_name != previous_literal.name and
                    len(literal_name) > 2  # Not a small word like "of", "in"
                )

                if is_new_literal_by_tags or is_new_literal_by_uppercase:
                    # This is Pattern 2/5 (separate literal) - current line is a NEW literal
                    # For Pattern 2, names are the same (base name) but create separate literals
                    # For Pattern 5, names are different but create separate literals
                    # Create a new literal with current name and description
                    tags = self._extract_literal_tags(literal_description)
                    index = None
                    if "atp.EnumerationLiteralIndex" in tags:
                        index = int(tags["atp.EnumerationLiteralIndex"])

                    # Clean description by removing all tag patterns
                    clean_description = literal_description
                    if "atp.EnumerationLiteralIndex" in tags:
                        clean_description = re.sub(r"\s*atp\.EnumerationLiteralIndex=\d+", "", clean_description)
                    if "xml.name" in tags:
                        clean_description = re.sub(r"\s*xml\.name=[^\s,]+", "", clean_description)
                    clean_description = clean_description.strip()

                    # Create new literal with current name and description
                    literal = AutosarEnumLiteral(
                        name=literal_name,
                        description=clean_description if clean_description else None,
                        index=index,
                        value=index,
                        tags=tags,
                    )
                    self._pending_literals.append(literal)
                    return False  # Pattern 2/5 handled, don't continue
                else:
                    # Previous literal doesn't have complete tags yet OR description is only "Tags:" OR names match
                    # This is Pattern 3 (combined names) or continuation
                    # Append to previous literal's name (not description)
                    # This handles literal names split across multiple lines in one cell
                    if self._pending_literals:
                        self._pending_literals[-1].name += literal_name
                        # If this line has "Tags:", process them
                        if literal_description.startswith("Tags:"):
                            tags = self._extract_literal_tags(literal_description)
                            index = None
                            if "atp.EnumerationLiteralIndex" in tags:
                                index = int(tags["atp.EnumerationLiteralIndex"])
                            self._pending_literals[-1].index = index
                            self._pending_literals[-1].tags = tags
                        return False  # Pattern 3 handled, don't continue
                    # If no previous literals, fall through to create new literal below

            if is_continuation and self._pending_literals:
                # Append to previous literal's description
                previous_literal = self._pending_literals[-1]
                # Initialize description if None
                if previous_literal.description is None:
                    previous_literal.description = ''
                # Add a space before appending if needed
                if not previous_literal.description.endswith(' '):
                    previous_literal.description += ' '
                # Append the continuation text (include the "name" as it's part of the description)
                continuation_text = f"{literal_name} {literal_description}" if literal_description else literal_name
                previous_literal.description += continuation_text
            else:
                # This is a new literal - create it
                # Filter out common header words and phrases that are not valid enumeration literals
                # These often appear in PDF headers around enumeration tables
                header_exclusion_patterns = {
                    "extract template", "cp r23-11", "r23-11", "template",
                    "autosar ", "diagnostic "
                }
                # Check if literal name or description matches header exclusion patterns
                skip_literal = False
                literal_lower = literal_name.lower()
                desc_lower = literal_description.lower() if literal_description else ""

                # Check if description contains header patterns (e.g., "Extract Template")
                for pattern in header_exclusion_patterns:
                    if pattern in desc_lower or pattern in literal_lower:
                        skip_literal = True
                        break

                # Also check if name is a single common header word with generic description
                # e.g., "Diagnostic" with description "Extract Template"
                if (literal_name in ["Diagnostic", "AUTOSAR", "Generic", "Structure", "Timing"] and
                    any(p in desc_lower for p in ["extract", "template", "r23-11", "structure", "timing"])):
                    skip_literal = True

                if skip_literal:
                    # Skip this literal - it's likely header text
                    return False
                # Extract tags from description
                tags = self._extract_literal_tags(literal_description)

                # Extract index from tags (backward compatible)
                index = None
                if "atp.EnumerationLiteralIndex" in tags:
                    index = int(tags["atp.EnumerationLiteralIndex"])

                # Clean description by removing all tag patterns
                clean_description = literal_description
                if "atp.EnumerationLiteralIndex" in tags:
                    clean_description = re.sub(r"\s*atp\.EnumerationLiteralIndex=\d+", "", clean_description)
                if "xml.name" in tags:
                    clean_description = re.sub(r"\s*xml\.name=[^\s,]+", "", clean_description)
                clean_description = clean_description.strip()

                # Create and add the literal to pending list
                literal = AutosarEnumLiteral(
                    name=literal_name,
                    description=clean_description if clean_description else None,
                    index=index,
                    value=index,
                    tags=tags,
                )
                self._pending_literals.append(literal)

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
        index_pattern = re.compile(r"atp\.EnumerationLiteralIndex=(\d+)")
        match = index_pattern.search(description)
        if match:
            return int(match.group(1))
        return None

    def _extract_literal_tags(self, description: str) -> Dict[str, str]:
        """Extract all metadata tags from description.

        Extracts patterns like:
        - atp.EnumerationLiteralIndex=0
        - xml.name=ISO-11992-4
        - Tags: atp.EnumerationLiteralIndex=0

        Requirements:
            SWR_PARSER_00031: Enumeration Literal Tags Extraction

        Args:
            description: The literal description.

        Returns:
            Dictionary of tag keys to tag values.
        """
        tags: Dict[str, str] = {}

        if not description:
            return tags

        # Handle multi-line tag descriptions
        # Normalize by replacing newlines with spaces
        normalized = description.replace("\n", " ").strip()

        # Extract atp.EnumerationLiteralIndex
        index_pattern = re.compile(r"atp\.EnumerationLiteralIndex=(\d+)")
        index_match = index_pattern.search(normalized)
        if index_match:
            tags["atp.EnumerationLiteralIndex"] = index_match.group(1)

        # Extract xml.name
        xml_pattern = re.compile(r"xml\.name=([^\s,]+)")
        xml_match = xml_pattern.search(normalized)
        if xml_match:
            tags["xml.name"] = xml_match.group(1)

        return tags

    def _apply_collected_tags(self) -> None:
        """Apply collected tag lines to the most recent literal.

        This method is called when we've finished collecting multi-line tags
        (after seeing "Tags:" followed by tag lines, then a new literal).

        Requirements:
            SWR_PARSER_00031: Enumeration Literal Tags Extraction
        """
        if not self._pending_literals or not self._tag_lines:
            return

        # Combine all tag lines and extract tags
        tags_text = " ".join(self._tag_lines)
        tags = self._extract_literal_tags(tags_text)

        if tags:
            # Extract index from tags
            index = None
            if "atp.EnumerationLiteralIndex" in tags:
                try:
                    index = int(tags["atp.EnumerationLiteralIndex"])
                except (ValueError, TypeError):
                    pass

            # Update the most recent literal with tags and index
            self._pending_literals[-1].tags = tags
            if index is not None:
                self._pending_literals[-1].index = index
                self._pending_literals[-1].value = index

    def _process_note_line(
        self, note_match: Match, lines: List[str], line_index: int, current_model: AutosarEnumeration
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
        note_text = self._extract_note_text(note_match, lines, line_index, parser_type="enumeration")
        current_model.note = note_text