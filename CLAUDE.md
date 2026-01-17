# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`autosar-pdf2txt` is a Python package for extracting AUTOSAR model hierarchies from PDF files and converting them to markdown format. The project uses a dataclass-based model for representing AUTOSAR packages and classes, a PDF parser for extraction, and a markdown writer for output.

## Stable Identifiers

**CRITICAL: All unique IDs are permanent and immutable.**

Once assigned, requirement IDs, test IDs, and coding rule IDs must never be changed, even if:
- The associated requirement, test, or rule is removed from the codebase
- The requirement is superseded by a new requirement
- The test is no longer applicable
- The coding rule is modified or replaced

### ID Formats

**Requirements:** `SWR_<MODULE>_<NUMBER>`
- Example: `SWR_MODEL_00001`, `SWR_PARSER_00003`

**Tests:** `SWUT_<MODULE>_<NUMBER>` (Software Unit Test)
- Example: `SWUT_MODEL_00001`, `SWUT_PARSER_00002`

**Coding Rules:** `CODING_RULE_<CATEGORY>_<NUMBER>`
- Example: `CODING_RULE_IMPORT_00001`, `CODING_RULE_STYLE_00003`

### Maturity Levels

Each requirement, test case, and coding rule has a maturity level that indicates its status:

**Maturity Levels:**
- **draft**: Newly created, under review, or not yet implemented
- **accept**: Accepted, implemented, and validated
- **invalid**: Deprecated, superseded, or no longer applicable

**Examples:**
```markdown
#### SWR_MODEL_00001
**Title**: AUTOSAR Class Representation

**Maturity**: accept

**Description**: The system shall provide a data model...
```

```markdown
### CODING_RULE_IMPORT_00001: Import Order

**Maturity**: accept

**Imports must be organized into three distinct sections...**
```

### Purpose of Stable IDs

Stable IDs ensure:
- **Traceability**: Links between requirements, code, and tests remain valid over time
- **Historical accuracy**: Old documentation and references remain meaningful
- **Audit trails**: Change history can be tracked accurately
- **Cross-references**: External systems can reference IDs without fear of breakage

When adding new items, always use the next available number in the sequence. Never reuse a deleted ID.

## Development Commands

### Installation
```bash
pip install -e .
```

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/models/test_autosar_models.py -v

# Run with coverage
pytest tests/ -v --cov=src/autosar_pdf2txt --cov-report=term
```

### Linting and Type Checking
```bash
# Lint with ruff
ruff check src/ tests/

# Type check with mypy
mypy src/autosar_pdf2txt/
```

### Running Full CI Pipeline
```bash
# Install dev dependencies
pip install pytest pytest-cov ruff mypy

# Run all checks
ruff check src/ tests/
mypy src/autosar_pdf2txt/
pytest tests/ -v --cov=src/autosar_pdf2txt --cov-report=term
```

## Code Architecture

### Package Structure
```
src/autosar_pdf2txt/
├── __init__.py          # Package exports
├── models/
│   ├── __init__.py
│   └── autosar_models.py   # AutosarClass, AutosarPackage dataclasses
├── parser/
│   ├── __init__.py
│   └── pdf_parser.py       # PdfParser class for extracting AUTOSAR from PDFs
├── writer/
│   ├── __init__.py
│   └── markdown_writer.py   # MarkdownWriter class
└── cli/
    ├── __init__.py
    └── autosar_cli.py       # Command-line interface
```

### Core Components

**Models (`models/autosar_models.py`)**
- `AutosarClass`: Dataclass representing an AUTOSAR class with name and abstract flag
- `AutosarPackage`: Dataclass for hierarchical package structures containing classes and subpackages
- Validation: Both classes validate non-empty names in `__post_init__`
- Duplicate prevention: `add_class()` and `add_subpackage()` check for duplicates by name
- Query methods: `get_class()`, `get_subpackage()`, `has_class()`, `has_subpackage()`

**Parser (`parser/pdf_parser.py`)**
- `PdfParser`: Extracts AUTOSAR hierarchies from PDF files using pdfplumber
- Pattern recognition: Identifies class definitions, package paths, base classes, and subclasses
- Hierarchy building: Constructs nested package structures from parsed data
- Default PDF engine: pdfplumber (no backend selection)

**Writer (`writer/markdown_writer.py`)**
- `MarkdownWriter`: Class-based API for writing package hierarchies to markdown
- Output format: Asterisk-based hierarchy with indentation (2 spaces per level)
- Classes indented 1 level deeper than their parent package
- No writer-level deduplication (relies on model-level duplicate prevention)

## CLI Usage

### Basic Usage
```bash
# Parse a single PDF and output to stdout
autosar-extract input.pdf

# Parse multiple PDFs and save to file
autosar-extract file1.pdf file2.pdf -o output.md

# Parse all PDFs in a directory
autosar-extract /path/to/pdfs/

# Verbose mode for detailed debug information
autosar-extract input.pdf -v
```

### Logging Levels
- **INFO level**: Standard progress messages (default)
  - PDF files being parsed
  - Number of packages found
  - Output file location
- **DEBUG level**: Detailed debug information (with `-v` flag)
  - Full file paths
  - Package names
  - Detailed operation trace
- **WARNING level**: Non-critical issues
  - Skipping non-PDF files
  - Empty directories
- **ERROR level**: Critical failures that prevent execution

## Code Style Conventions

**Complete coding standards are documented in `docs/development/coding_rules.md`, which combines project-specific rules with PEP 8 standards.**

### Type Hints
- All functions and methods must have type hints for parameters and return values
- Use `|` for union types (e.g., `str | None`) - Python 3.10+ syntax
- Use `List[T]` from typing for lists (not built-in `list[T]`)

### Docstrings
- Google-style docstrings with Args/Returns/Raises sections
- Class docstrings include Attributes section
- **Requirement traceability**: Include "Requirements:" section with relevant requirement IDs
- Examples in docstrings use `>>>` doctest format

### Import Organization
1. Standard library imports
2. Third-party imports
3. Local imports (`from autosar_pdf2txt...`)

### Naming Conventions
- Functions/methods: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Private attributes: `_leading_underscore`

### Error Handling
- Use `ValueError` for invalid arguments (empty names, duplicates)
- Use `__post_init__` for dataclass validation
- Raise errors immediately on validation failure
- Use logging module for CLI error messages (not print to stderr)

### Comments
- All comments and docstrings must be in English

## Testing

### Test Structure
- Test files mirror source structure in `tests/` directory
- Test classes named `Test<ClassName>` for models, `Test<ModuleName>` for modules
- Test methods: `test_<method_name>_<scenario>` or `test_<scenario>`
- All test docstrings must be in English

### Coverage Goals
- Target 100% coverage for all modules
- Tests cover success paths, error paths, and edge cases
- Example test scenarios in `tests/writer/test_markdown_writer.py`:
  - Nested hierarchies
  - Empty inputs
  - Abstract vs concrete classes
  - Package and class output formatting

## Key Implementation Details

### Markdown Indentation Rules
- Packages: indent = `level * 2` spaces
- Classes: indent = `(level + 1) * 2` spaces (1 level deeper than parent package)
- Format: `* <name>` or `* <name> (abstract)`

### Duplicate Handling
- Model-level duplicate prevention in `AutosarPackage.add_class()` and `AutosarPackage.add_subpackage()`
- Checks for duplicates by name before adding
- Raises `ValueError` when attempting to add duplicates
- No writer-level deduplication needed (model guarantees uniqueness)

### Model Validation
- Empty/whitespace names raise `ValueError`
- Duplicate classes in package raise `ValueError`
- Duplicate subpackages in package raise `ValueError`

### PDF Parsing Patterns
- Class definitions: `Class <name> (abstract)`
- Package definitions: `Package <M2::?><path>`
- Base classes: `Base <class_list>`
- Subclasses: `Subclasses <class_list>`

## Requirement Traceability

All code includes requirement IDs in docstrings for traceability to `docs/requirement/requirements.md`. Coding standards are defined in `docs/development/coding_rules.md` with stable identifiers.

**Requirements by Module:**
- **Model**: SWR_MODEL_00001 - SWR_MODEL_00009
  - SWR_MODEL_00001: AUTOSAR Class Representation
  - SWR_MODEL_00002: AUTOSAR Class Name Validation
  - SWR_MODEL_00003: AUTOSAR Class String Representation
  - SWR_MODEL_00004: AUTOSAR Package Representation
  - SWR_MODEL_00005: AUTOSAR Package Name Validation
  - SWR_MODEL_00006: Add Class to Package
  - SWR_MODEL_00007: Add Subpackage to Package
  - SWR_MODEL_00008: Query Package Contents
  - SWR_MODEL_00009: Package String Representation

- **Parser**: SWR_PARSER_00001 - SWR_PARSER_00007
  - SWR_PARSER_00001: PDF Parser Initialization
  - SWR_PARSER_00002: Backend Validation
  - SWR_PARSER_00003: PDF File Parsing
  - SWR_PARSER_00004: Class Definition Pattern Recognition
  - SWR_PARSER_00005: Class Definition Data Model
  - SWR_PARSER_00006: Package Hierarchy Building
  - SWR_PARSER_00007: PDF Backend Support - pdfplumber

- **Writer**: SWR_WRITER_00001 - SWR_WRITER_00004
  - SWR_WRITER_00001: Markdown Writer Initialization
  - SWR_WRITER_00002: Markdown Package Hierarchy Output
  - SWR_WRITER_00003: Markdown Class Output Format
  - SWR_WRITER_00004: Bulk Package Writing

- **CLI**: SWR_CLI_00001 - SWR_CLI_00009
  - SWR_CLI_00001: CLI Entry Point
  - SWR_CLI_00002: CLI File Input Support
  - SWR_CLI_00003: CLI Directory Input Support
  - SWR_CLI_00004: CLI Output File Option
  - SWR_CLI_00005: CLI Verbose Mode
  - SWR_CLI_00006: CLI Input Validation
  - SWR_CLI_00007: CLI Progress Feedback
  - SWR_CLI_00008: CLI Logging
  - SWR_CLI_00009: CLI Error Handling

- **Package**: SWR_PACKAGE_00001 - SWR_PACKAGE_00003
  - SWR_PACKAGE_00001: Package API Export
  - SWR_PACKAGE_00002: Python Version Support
  - SWR_PACKAGE_00003: Package Metadata

**Example:**
```python
def __init__(self) -> None:
    """Initialize the PDF parser.

    Requirements:
        SWR_PARSER_00001: PDF Parser Initialization
        SWR_PARSER_00007: PDF Backend Support - pdfplumber

    Raises:
        ImportError: If pdfplumber is not installed.
    """
```
