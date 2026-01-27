# Multi-line Parsing Support Summary

This document summarizes which fields in the AUTOSAR PDF parser support multi-line parsing and how they handle it.

## Overview

The AUTOSAR PDF parser supports multi-line parsing for various fields to handle cases where PDF table formatting causes content to span multiple lines. This is essential for accurate extraction of complex AUTOSAR model definitions.

## Fields with Multi-line Support

### 1. Class Attributes (SWR_PARSER_00012)
**Files**: `src/autosar_pdf2txt/parser/class_parser.py`, `src/autosar_pdf2txt/parser/primitive_parser.py`

**Support**: ✅ Full multi-line support

**Handling**:
- Detects when attribute names or types span multiple lines
- Reconstructs complete attribute names (e.g., "isStructWithOptionalElement" split across lines)
- Reconstructs complete attribute types (e.g., "dynamicArraySizeProfile" split across lines)
- Filters out continuation fragments: "data", "If", "has", "to", "Element", "SizeProfile"
- Uses pending attribute state to accumulate multi-line attributes
- Method: `_handle_attribute_continuation()` in `base_parser.py`

**Example**:
```
PDF Line 1: isStructWith OptionalElement 1..1 REF
PDF Line 2: Some description text

Result: Single attribute with complete name "isStructWithOptionalElement" and combined description
```

### 2. Enumeration Literal Descriptions (SWR_PARSER_00015)
**Files**: `src/autosar_pdf2txt/parser/enumeration_parser.py`

**Support**: ✅ Full multi-line support

**Handling**:
- Detects continuation lines by:
  - Duplicate literal names
  - Common continuation words: "enable", "qualification", "the", "condition", "conditions", "of", "or", "and", "with", "will", "after", "related", "all"
  - Lowercase first letter in description
- Appends continuation text to previous literal's description
- Supports multiple literals on separate lines sharing same description (enum3.png scenario)
- Uses regex pattern `^([a-zA-Z_][a-zA-Z0-9_]*)(?:\s+(.*))?$` to match literals with or without description

**Example**:
```
PDF Line 1: VALUE1 First part of description
PDF Line 2: enable the feature
PDF Line 3: VALUE2 Second value

Result: Two literals, first with combined description
```

### 3. Class Notes (SWR_PARSER_00021)
**Files**: `src/autosar_pdf2txt/parser/class_parser.py`, `src/autosar_pdf2txt/parser/primitive_parser.py`, `src/autosar_pdf2txt/parser/enumeration_parser.py`

**Support**: ✅ Full multi-line support

**Handling**:
- Detects note continuation lines by checking if line doesn't match known patterns
- Extracts multi-line note text from "Note:" marker until next known pattern
- Method: `_extract_note_text()` and `_is_note_continuation()` in `base_parser.py`
- Works for Class, Primitive, and Enumeration parsers

**Example**:
```
PDF Line 1: Note: This is a multi-line note
PDF Line 2: that continues across several lines
PDF Line 3: and provides detailed information.

Result: Single note with all three lines combined
```

### 4. Class Lists (Base, Subclasses, Aggregated by)
**Files**: `src/autosar_pdf2txt/parser/class_parser.py`

**Support**: ✅ Full multi-line support

**Handling**:
- Detects continuation lines by checking for commas or continuation fragments
- Handles class names split across lines (e.g., "Packageable" on one line, "Element" on next)
- Filters out continuation fragments: "Element", "Referrable", "Packageable", "Type", "Profile"
- Method: `_handle_class_list_continuation()` in `class_parser.py`
- Applies to Base classes, Subclasses, and Aggregated by lists

**Example**:
```
PDF Line 1: Base ARObject, Packageable
PDF Line 2: Element, Referrable

Result: Single list: ["ARObject", "PackageableElement", "Referrable"]
```

### 5. Multi-page Definitions (SWR_PARSER_00003, SWR_PARSER_00032)
**Files**: `src/autosar_pdf2txt/parser/pdf_parser.py`, `src/autosar_pdf2txt/parser/class_parser.py`, `src/autosar_pdf2txt/parser/enumeration_parser.py`, `src/autosar_pdf2txt/parser/primitive_parser.py`

**Support**: ✅ Full multi-page support

**Handling**:
- Two-phase parsing: Read phase (all text) → Parse phase (complete buffer)
- State management via `current_models` and `model_parsers` dictionaries
- `continue_parsing()` method returns `(new_line_index, is_complete)` tuple
- Returns `False` for `is_complete` when more content expected on next page
- Maintains parsing state across page boundaries
- Supports both repeated and non-repeated headers on subsequent pages

**Example**:
```
Page 1: Class SwDataDefProps
Page 1: Attribute Type Mult. Kind Note
Page 1: swDataDefProps SwDataDefProps 1 REF
Page 2: initialValue AbstractString 0..1 REF

Result: Class with both attributes extracted from different pages
```

## Fields WITHOUT Multi-line Support

### 1. Package Paths
**Status**: ❌ No multi-line support (not needed)
- Package paths are always on a single line in AUTOSAR PDFs
- Format: `Package M2::AUTOSAR::DataTypes`

### 2. ATP Markers
**Status**: ❌ No multi-line support (not needed)
- ATP markers are always inline with the class name
- Format: `Class ClassName <<atpMixedString>>`

### 3. Enumeration Literal Tags
**Status**: ✅ Implicit multi-line support via description extraction
- Tags are extracted from the description field
- If description spans multiple lines, tags are still extracted correctly
- Tags are removed from the cleaned description

## Detection Mechanisms

The parser uses several mechanisms to detect multi-line content:

### 1. Duplicate Names
- When the same literal name appears on consecutive lines
- Indicates continuation of previous literal's description

### 2. Continuation Words
- Predefined set of common continuation words
- `{"enable", "qualification", "the", "condition", "conditions", "of", "or", "and", "with", "will", "after", "related", "all"}`

### 3. Lowercase First Letter
- If the description starts with lowercase, it's likely a continuation
- Formal descriptions typically start with uppercase

### 4. Fragment Detection
- Known fragment patterns that indicate incomplete content
- `{"Element", "SizeProfile", "Referrable", "Packageable", "Type", "Profile"}`

### 5. Comma Detection
- Presence of comma indicates continuation of a list
- Used for Base, Subclasses, Aggregated by lists

### 6. Empty Description with Previous Tags
- Literal with no description but previous literal has complete description with tags
- Indicates second literal sharing same description (enum3.png scenario)

## Implementation Details

### State Management
- **Pending attributes**: `self._pending_attr_name`, `self._pending_attr_type`, etc.
- **Pending literals**: `self._pending_literals` list
- **Pending class lists**: `self._pending_class_lists` dictionary
- **Section flags**: `self._in_attribute_section`, `self._in_enumeration_literal_section`, etc.

### Regex Patterns
- **Enumeration literal**: `^([a-zA-Z_][a-zA-Z0-9_]*)(?:\s+(.*))?$` (name optional description)
- **Attribute**: `^(\S+)\s+(\S+)\s+.*$` (name type ...)

### Methods
- `_handle_attribute_continuation()` - Attribute multi-line handling
- `_handle_class_list_continuation()` - Class list multi-line handling
- `_is_note_continuation()` - Note continuation detection
- `_extract_note_text()` - Multi-line note extraction
- `continue_parsing()` - Multi-page continuation handling

## Test Coverage

All multi-line parsing features have comprehensive test coverage:
- Unit tests in `tests/parser/test_pdf_parser.py`
- Integration tests in `tests/integration/test_pdf_integration.py`
- Coverage: ≥95% for all parser modules

## References

- **SWR_PARSER_00003**: PDF File Parsing (Two-Phase Approach)
- **SWR_PARSER_00012**: Multi-Line Attribute Handling
- **SWR_PARSER_00015**: Enumeration Literal Extraction from PDF (with multi-line support)
- **SWR_PARSER_00021**: Multi-Line Attribute Parsing for AutosarClass
- **SWR_PARSER_00030**: Page Number Tracking in Two-Phase Parsing
- **SWR_PARSER_00031**: Enumeration Literal Tags Extraction
- **SWR_PARSER_00032**: Multi-page Enumeration Literal List Support