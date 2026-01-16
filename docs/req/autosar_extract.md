# Requirements: AUTOSAR PDF to Markdown Extractor

## Overview

The autosar-pdf2txt tool extracts structured AUTOSAR package and class hierarchies from PDF specification documents and outputs them in markdown format with asterisk-based indentation.

## Functional Requirements

### FR1: PDF Text Extraction
- **FR1.1**: The system shall extract text content from PDF files
- **FR1.2**: The system shall support multiple PDF parsing backends:
  - pdfplumber (preferred, highest quality)
  - fitz/PyMuPDF (alternative)
  - pypdf (fallback option)
- **FR1.3**: The system shall automatically select the best available backend when backend="auto"
- **FR1.4**: The system shall allow manual backend selection
- **FR1.5**: The system shall handle PDF read errors gracefully with appropriate error messages

### FR2: Hierarchy Parsing
- **FR2.1**: The system shall parse AUTOSAR hierarchies from asterisk-based text format
- **FR2.2**: The system shall distinguish between packages and classes based on hierarchy structure
  - Items with children (subsequent lines with greater indentation) are packages
  - Items without children are classes
- **FR2.3**: The system shall detect and mark abstract classes by identifying "(abstract)" suffix
- **FR2.4**: The system shall support arbitrarily deep nesting levels
- **FR2.5**: The system shall calculate indentation based on number of leading spaces (2 spaces per level)
- **FR2.6**: The system shall handle blank lines in input text

### FR3: Data Models
- **FR3.1**: The system shall provide an `AutosarClass` data model with:
  - `name`: string (required, non-empty)
  - `is_abstract`: boolean
- **FR3.2**: The system shall provide an `AutosarPackage` data model with:
  - `name`: string (required, non-empty)
  - `classes`: list of AutosarClass objects
  - `subpackages`: list of AutosarPackage objects (for nested structures)
- **FR3.3**: AutosarPackage shall prevent duplicate class names (raise ValueError on duplicate)
- **FR3.4**: AutosarPackage shall prevent duplicate subpackage names (raise ValueError on duplicate)
- **FR3.5**: The system shall provide methods: `add_class()`, `add_subpackage()`, `get_class()`, `get_subpackage()`, `has_class()`, `has_subpackage()`

### FR4: Markdown Output
- **FR4.1**: The system shall output AUTOSAR hierarchies in markdown format using asterisk notation
- **FR4.2**: The system shall use proper indentation to show nesting levels:
  - 2 spaces per level for packages
  - Additional 2 spaces for classes (level + 2)
- **FR4.3**: The system shall mark abstract classes with "(abstract)" suffix
- **FR4.4**: The system shall prevent duplicate packages and classes in output
- **FR4.5**: Duplicate detection shall be based on full path tuple (e.g., ("Root", "Sub", "Class"))
- **FR4.6**: The system shall provide deduplication toggle (default: enabled)
- **FR4.7**: The system shall track seen packages and classes across multiple write operations when deduplication is enabled
- **FR4.8**: The system shall support both class-based and functional interfaces

### FR5: API Design
- **FR5.1**: All modules shall provide both class-based and functional interfaces
- **FR5.2**: PDF Reader:
  - Class-based: `PDFReader(backend="auto").read_text(path)`
  - Functional: `read_pdf(path, backend="auto")`
- **FR5.3**: Hierarchy Parser:
  - Class-based: `HierarchyParser().parse(text)`
  - Functional: `parse_hierarchy(text)`
- **FR5.4**: Autosar Parser (integration):
  - Class-based: `AutosarParser().parse_pdf(path)`
  - Functional: `parse_autosar_pdf(path, backend="auto")`
- **FR5.5**: Markdown Writer:
  - Class-based: `MarkdownWriter(deduplicate=True).write_packages(packages)`
  - Functional: `write_markdown(packages, deduplicate=True)`

## Non-Functional Requirements

### NFR1: Code Quality
- **NFR1.1**: Type hints required on all function/method parameters and return values
- **NFR1.2**: Google-style docstrings with Args/Returns/Raises sections
- **NFR1.3**: Import order: standard library → third-party → local
- **NFR1.4**: Naming conventions:
  - Functions: snake_case
  - Classes: PascalCase
  - Constants: UPPER_CASE
- **NFR1.5**: All code comments shall be in English

### NFR2: Error Handling
- **NFR2.1**: Use `ValueError` for invalid arguments
- **NFR2.2**: Use try-except for I/O operations
- **NFR2.3**: Provide clear, actionable error messages

### NFR3: Testing
- **NFR3.1**: Test coverage target: 100% for models and parser, ≥95% for writer
- **NFR3.2**: One test file per source file (matching src/ structure)
- **NFR3.3**: Test framework: pytest
- **NFR3.4**: All tests shall use English docstrings
- **NFR3.5**: Tests shall cover:
  - Normal operations
  - Edge cases
  - Error conditions
  - Duplicate detection
  - Nested structures

### NFR4: Code Organization
- **NFR4.1**: Project structure:
  ```
  src/autosar_pdf2txt/
  ├── models/          # Data models
  ├── parser/          # PDF parsing and hierarchy extraction
  ├── writer/          # Markdown output
  └── cli/            # Command-line interfaces
  tests/
  ├── models/         # Model tests
  ├── parser/         # Parser tests
  └── writer/         # Writer tests
  ```
- **NFR4.2**: Each package shall have __init__.py with __all__ exports
- **NFR4.3**: Use dataclasses for models with validation in __post_init__

## Output Format Specification

### Package/Class Hierarchy Format

```
* PackageName
  * SubPackageName
      * ClassName
      * AbstractClassName (abstract)
```

### Indentation Rules
- Level 0 (top-level package): 0 spaces before `*`
- Level 1 (subpackage): 2 spaces before `*`
- Level 2 (nested subpackage): 4 spaces before `*`
- Level N+1 (class): (N+2) * 2 spaces before `*`

### Examples

**Single package with class:**
```
* TestPackage
    * MyClass
```

**Nested structure:**
```
* AUTOSARTemplates
  * BswModuleTemplate
    * BswBehavior
        * BswInternalBehavior
        * ExecutableEntity (abstract)
```

## Input Format Specification

### Expected Hierarchy Format (from PDF)

The parser expects text in the following format:
- Lines start with `*` followed by content
- Indentation indicated by leading spaces
- Optional `(abstract)` suffix for abstract classes
- Blank lines allowed and ignored

**Example input:**
```
* AUTOSARTemplates
  * BswModuleTemplate
    * BswBehavior
        * BswInternalBehavior
        * ExecutableEntity (abstract)
```

## Integration Requirements

### IR1: End-to-End Workflow
1. Read PDF file using PDFReader
2. Extract text content
3. Parse text using HierarchyParser to extract package/class hierarchy
4. Write hierarchy to markdown using MarkdownWriter

### IR2: CLI Integration
- **IR2.1**: Provide CLI tool `autosar-extract` for command-line usage
- **IR2.2**: Support input PDF path argument
- **IR2.3**: Support optional output file path
- **IR2.4**: Support backend selection via CLI flag
- **IR2.5**: Handle file I/O errors gracefully

## Validation Requirements

### VR1: Data Model Validation
- **VR1.1**: AutosarClass.name must not be empty or whitespace-only
- **VR1.2**: AutosarPackage.name must not be empty or whitespace-only
- **VR1.3**: ValueError raised on validation failure

### VR2: Parser Validation
- **VR2.1**: Ignore lines not starting with `*`
- **VR2.2**: Ignore empty lines
- **VR2.3**: Handle lines with only `*` (no content)
- **VR2.4**: Detect abstract markers with or without extra spaces

## Technical Constraints

### TC1: Python Environment
- **TC1.1**: Python version: 3.9+
- **TC1.2**: Type checking with mypy
- **TC1.3**: Linting with ruff

### TC2: Dependencies
- **TC2.1**: Optional dependencies (at least one required):
  - pdfplumber (preferred)
  - fitz/PyMuPDF
  - pypdf
- **TC2.2**: No required dependencies except for PDF backends

## Quality Metrics

### QM1: Code Coverage
- Models: 100%
- Parser modules: 100%
- Writer: ≥95% (defensive code may be unreachable)

### QM2: Test Statistics
- Total tests: 107+
- All tests must pass
- No test failures allowed

## Version History

| Version | Date       | Description                                                                     |
| ------- | ---------- | ------------------------------------------------------------------------------- |
| v0.1.0  | 2026-01-16 | Initial implementation with PDF reading, hierarchy parsing, and markdown output |
