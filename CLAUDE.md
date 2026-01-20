# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`autosar-pdf2txt` is a Python package for extracting AUTOSAR model hierarchies from PDF files and converting them to markdown format. The project uses a dataclass-based model for representing AUTOSAR packages and classes with ATP (AUTOSAR Tool Platform) marker support, a PDF parser for extraction using pdfplumber, and a markdown writer for output with support for both consolidated and per-class file generation.

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
# Install in editable mode for development
pip install -e .

# Install with all development dependencies
pip install -e ".[dev]"  # If dev extras are defined
# Or manually:
pip install pytest pytest-cov ruff mypy pdfplumber
```

### Running Tests
```bash
# Run all tests (generates coverage report automatically to scripts/report/coverage.md)
python scripts/run_tests.py --all

# Run only unit tests
python scripts/run_tests.py --unit

# Run only integration tests
python scripts/run_tests.py --integration

# Run specific test file
pytest tests/models/test_autosar_models.py -v

# Run specific test with verbose output
pytest tests/models/test_autosar_models.py::TestAutosarClass::test_init_concrete_class -v

# Run with coverage manually (if needed)
pytest tests/ -v --cov=autosar_pdf2txt --cov-report=term
```

**Note**: The test runner automatically generates coverage reports at `scripts/report/coverage.md` after tests complete.

### Linting and Type Checking
```bash
# Lint with ruff
ruff check src/ tests/

# Auto-fix linting issues where possible
ruff check --fix src/ tests/

# Type check with mypy
mypy src/autosar_pdf2txt/

# Run both linting and type checking
ruff check src/ tests/ && mypy src/autosar_pdf2txt/
```

### Running Full CI Pipeline
```bash
# Quick check - run unit tests only
python scripts/run_tests.py --unit

# Full validation - all tests + quality checks
python scripts/run_tests.py --all && ruff check src/ tests/ && mypy src/autosar_pdf2txt/
```

## Project Examples

The `examples/pdf/` directory contains sample AUTOSAR specification PDFs for testing:

- `AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf`
- `AUTOSAR_CP_TPS_DiagnosticExtractTemplate.pdf`
- `AUTOSAR_CP_TPS_ECUConfiguration.pdf`
- `AUTOSAR_CP_TPS_ECUResourceTemplate.pdf`
- `AUTOSAR_CP_TPS_SoftwareComponentTemplate.pdf`
- `AUTOSAR_CP_TPS_SystemTemplate.pdf`
- `AUTOSAR_CP_TPS_TimingExtensions.pdf`

Use these files to test parser changes or verify extraction behavior.

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

### Data Flow Architecture

The project follows a **pipeline architecture** with clear separation of concerns:

```
PDF Files → PdfParser → AutosarPackage/AutosarClass → MarkdownWriter → Markdown Output
```

1. **Input Layer (CLI)**: `autosar_cli.py`
   - Accepts file/directory paths
   - Validates inputs
   - Orchestrates the pipeline

2. **Parsing Layer**: `pdf_parser.py`
   - Reads PDF files using pdfplumber
   - Extracts text line-by-line
   - Recognizes AUTOSAR patterns (Class, Package, Attributes, etc.)
   - Builds `ClassDefinition` intermediate objects
   - Constructs `AutosarPackage` hierarchy with nested `AutosarClass` objects

3. **Model Layer**: `autosar_models.py`
   - Immutable dataclasses with validation
   - `AutosarPackage`: Hierarchical package structure
   - `AutosarClass`: Class representation with attributes, inheritance, ATP markers
   - `AutosarAttribute`: Attribute details with reference type tracking
   - Duplicate prevention at model level

4. **Output Layer**: `markdown_writer.py`
   - Traverses package hierarchy
   - Generates markdown with proper indentation
   - Supports both consolidated output and per-class file generation

**Key Design Principles:**
- **Separation of Concerns**: Each layer has a single responsibility
- **Dataclass-Based Models**: Immutable, validated data structures
- **Model-Level Validation**: All validation happens in `__post_init__`, not in the parser
- **No Writer-Level Deduplication**: Parser ensures uniqueness through model validation

### Core Components

**Models (`models/autosar_models.py`)**
- `ATPType`: Enum representing AUTOSAR Tool Platform marker types (NONE, ATP_MIXED_STRING, ATP_VARIATION, ATP_MIXED)
- `AutosarClass`: Dataclass representing an AUTOSAR class with name, abstract flag, atp_type, attributes, bases (inheritance), and note (documentation)
- `AutosarAttribute`: Dataclass representing an AUTOSAR attribute with name, type, and reference flag
- `AutosarPackage`: Dataclass for hierarchical package structures containing classes and subpackages
- Validation: All classes validate non-empty names in `__post_init__`
- Duplicate prevention: `add_class()` and `add_subpackage()` check for duplicates by name
- Query methods: `get_class()`, `get_subpackage()`, `has_class()`, `has_subpackage()`

**Parser (`parser/pdf_parser.py`)**
- `PdfParser`: Extracts AUTOSAR hierarchies from PDF files using pdfplumber
- Pattern recognition: Identifies class definitions, package paths, base classes, and subclasses using regex patterns
- Hierarchy building: Constructs nested package structures from parsed data
- Default PDF engine: pdfplumber (no backend selection - this is fixed)
- Key intermediate class: `ClassDefinition` (internal to parser) for building parsed data before creating model objects

**Writer (`writer/markdown_writer.py`)**
- `MarkdownWriter`: Class-based API for writing package hierarchies to markdown
- Output format: Asterisk-based hierarchy with indentation (2 spaces per level)
- Classes indented 1 level deeper than their parent package
- No writer-level deduplication (relies on model-level duplicate prevention)
- Supports two output modes:
  - Consolidated: All packages and classes in single markdown file
  - Per-class: Individual markdown files for each class (with `--include-class-details`)

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

# Create separate markdown files for each class
autosar-extract input.pdf -o output.md --include-class-details
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
- Target 100% coverage for all modules (currently at 97%+)
- Tests cover success paths, error paths, and edge cases
- Coverage reports automatically generated at `scripts/report/coverage.md`
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
- Primitive class definitions: `Primitive <name>` (SWR_PARSER_00013)
- Enumeration class definitions: `Enumeration <name>` (SWR_PARSER_00013)
- Class definitions with ATP markers: `Class <name> <<atpMixedString>>`, `Class <name> <<atpVariation>>`, and `Class <name> <<atpMixed>>`
- Package definitions: `Package <M2::?><path>`
- Base classes: `Base <class_list>`
- Subclasses: `Subclasses <class_list>`
- Notes: `Note <text>` (documentation/comments)
- Attribute header: `Attribute Type Mult. Kind Note` (SWR_PARSER_00010)
- Attributes: `<name> <type> <mult> <kind> <description>` (SWR_PARSER_00010, SWR_PARSER_00011, SWR_PARSER_00012)

### PDF Text Extraction Strategy
The parser uses word-level extraction (pdfplumber's `extract_words()` with `x_tolerance=1`) instead of raw text extraction to properly handle word spacing and avoid concatenated words due to tight kerning in PDF files (SWR_PARSER_00009).

### Attribute Extraction Details
- Recognizes attribute section by the "Attribute Type Mult. Kind Note" header (SWR_PARSER_00010)
- Filters out metadata lines containing special characters (`:`, `;`) or starting with numbers (SWR_PARSER_00011)
- Handles multi-line attribute definitions by detecting and filtering broken attribute fragments (SWR_PARSER_00012)
- Common filtered fragments: "Element", "SizeProfile", "data", "If", "has", "to", "ImplementationDataType", "intention"

## Requirement Traceability

All code includes requirement IDs in docstrings for traceability to `docs/requirement/requirements.md`. Coding standards are defined in `docs/development/coding_rules.md` with stable identifiers.

**Requirements by Module:**
- **Model**: SWR_MODEL_00001 - SWR_MODEL_00013
  - SWR_MODEL_00001: AUTOSAR Class Representation
  - SWR_MODEL_00002: AUTOSAR Class Name Validation
  - SWR_MODEL_00003: AUTOSAR Class String Representation
  - SWR_MODEL_00004: AUTOSAR Package Representation
  - SWR_MODEL_00005: AUTOSAR Package Name Validation
  - SWR_MODEL_00006: Add Class to Package
  - SWR_MODEL_00007: Add Subpackage to Package
  - SWR_MODEL_00008: Query Package Contents
  - SWR_MODEL_00009: Package String Representation
  - SWR_MODEL_00010: AUTOSAR Attribute Representation
  - SWR_MODEL_00011: AUTOSAR Attribute Name Validation
  - SWR_MODEL_00012: AUTOSAR Attribute Type Validation
  - SWR_MODEL_00013: AUTOSAR Attribute String Representation

- **Parser**: SWR_PARSER_00001 - SWR_PARSER_00013
  - SWR_PARSER_00001: PDF Parser Initialization
  - SWR_PARSER_00002: Backend Validation
  - SWR_PARSER_00003: PDF File Parsing
  - SWR_PARSER_00004: Class Definition Pattern Recognition
  - SWR_PARSER_00005: Class Definition Data Model
  - SWR_PARSER_00006: Package Hierarchy Building
  - SWR_PARSER_00007: PDF Backend Support - pdfplumber
  - SWR_PARSER_00008: PDF Backend Support - pdfplumber (duplicate of SWR_PARSER_00007)
  - SWR_PARSER_00009: Proper Word Spacing in PDF Text Extraction
  - SWR_PARSER_00010: Attribute Extraction from PDF
  - SWR_PARSER_00011: Metadata Filtering in Attribute Extraction
  - SWR_PARSER_00012: Multi-Line Attribute Handling
  - SWR_PARSER_00013: Recognition of Primitive and Enumeration Class Definition Patterns

- **Writer**: SWR_WRITER_00001 - SWR_WRITER_00006
  - SWR_WRITER_00001: Markdown Writer Initialization
  - SWR_WRITER_00002: Markdown Package Hierarchy Output
  - SWR_WRITER_00003: Markdown Class Output Format
  - SWR_WRITER_00004: Bulk Package Writing
  - SWR_WRITER_00005: Directory-Based Class File Output
  - SWR_WRITER_00006: Individual Class Markdown File Content

- **CLI**: SWR_CLI_00001 - SWR_CLI_00011
  - SWR_CLI_00001: CLI Entry Point
  - SWR_CLI_00002: CLI File Input Support
  - SWR_CLI_00003: CLI Directory Input Support
  - SWR_CLI_00004: CLI Output File Option
  - SWR_CLI_00005: CLI Verbose Mode
  - SWR_CLI_00006: CLI Input Validation
  - SWR_CLI_00007: CLI Progress Feedback
  - SWR_CLI_00008: CLI Logging
  - SWR_CLI_00009: CLI Error Handling
  - SWR_CLI_00010: CLI Class File Output
  - SWR_CLI_00011: CLI Class Files Flag

- **Package**: SWR_PACKAGE_00001 - SWR_PACKAGE_00003
  - SWR_PACKAGE_00001: Package API Export
  - SWR_PACKAGE_00002: Python Version Support
  - SWR_PACKAGE_00003: Package Metadata

## Quality Checks

Before committing changes, run the following quality checks to ensure code quality:

### Quality Gate Workflow
```bash
# Run all quality checks in sequence
python scripts/run_tests.py --unit && ruff check src/ tests/ && mypy src/autosar_pdf2txt/
```

### Individual Quality Checks

**Linting:**
```bash
# Run ruff linter
ruff check src/ tests/

# Auto-fix issues where possible
ruff check --fix src/ tests/
```

**Expected Result**: All checks pass with no errors or warnings.

**Type Checking:**
```bash
# Run mypy type checker
mypy src/autosar_pdf2txt/
```

**Expected Result**: Success: no issues found in source files.

**Testing:**
```bash
# Run all unit tests with coverage
python scripts/run_tests.py --unit

# Or run pytest directly
pytest tests/ -v
```

**Expected Result**: All tests pass with 97%+ coverage.

### Quality Gates
All of the following must pass before committing:
1. ✅ Ruff linting: No errors
2. ✅ Mypy type checking: No issues
3. ✅ Pytest: All tests pass
4. ✅ Coverage: ≥95%

**Example with Requirements Traceability:**
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

## Documentation Structure

The project maintains comprehensive documentation in the `docs/` directory:

- `docs/requirements/requirements.md` - Complete software requirements specification with stable IDs
- `docs/development/coding_rules.md` - Detailed coding standards combining PEP 8 with project-specific rules
- `docs/models/` - Model-specific documentation
- `docs/test_cases/` - Test case documentation with traceability to requirements
- `scripts/report/coverage.md` - Auto-generated coverage reports (updated after each test run)

## Common Development Tasks

### Adding a New Requirement

When implementing new features, follow this workflow:

1. **Add the requirement** to `docs/requirements/requirements.md`:
   - Use the next available ID in the sequence (e.g., `SWR_MODEL_00014`)
   - Set maturity to `draft`
   - Include description and acceptance criteria

2. **Implement the feature** in the appropriate module:
   - Add requirement ID to all relevant docstrings
   - Follow coding standards in `docs/development/coding_rules.md`
   - Include type hints and Google-style docstrings

3. **Add tests** to the appropriate test file:
   - Use the next available test ID (e.g., `SWUT_MODEL_00014`)
   - Test success paths, error paths, and edge cases
   - Include requirement ID in test docstrings

4. **Update maturity levels**:
   - Change requirement maturity from `draft` to `accept`
   - Change test maturity from `draft` to `accept`

5. **Run quality checks**:
   ```bash
   python scripts/run_tests.py --unit && ruff check src/ tests/ && mypy src/autosar_pdf2txt/
   ```

### Debugging PDF Parsing Issues

If the parser is not extracting classes correctly from a PDF:

1. **Enable verbose mode** to see detailed parsing information:
   ```bash
   autosar-extract input.pdf -v
   ```

2. **Check the PDF text extraction** by inspecting what pdfplumber extracts:
   ```python
   import pdfplumber

   with pdfplumber.open("input.pdf") as pdf:
       for page in pdf.pages:
           print(page.extract_text())
   ```

3. **Verify regex patterns** in `pdf_parser.py` match the PDF format:
   - Class definitions: `CLASS_PATTERN`, `PRIMITIVE_PATTERN`, `ENUMERATION_PATTERN`
   - Package paths: `PACKAGE_PATTERN`
   - Attributes: `ATTRIBUTE_PATTERN` (checks for "Attribute Type Mult. Kind Note" header)
   - ATP markers: `ATP_MIXED_STRING_PATTERN`, `ATP_VARIATION_PATTERN`, `ATP_MIXED_PATTERN`

4. **Check for attribute extraction issues**:
   - Verify attribute header recognition: "Attribute Type Mult. Kind Note"
   - Check for metadata lines being incorrectly parsed (SWR_PARSER_00011)
   - Look for multi-line attribute fragments (SWR_PARSER_00012)
   - Common problematic fragments: "Element", "SizeProfile", "data", "If", "has"

5. **Check for M2 package prefixes** which affect hierarchy building

### Understanding Package Hierarchy

The parser builds package hierarchies from path strings like `"M2::AUTOSAR::DataTypes"`:

- `M2::` prefix is stripped during parsing
- `::` separator indicates nesting levels
- Each level becomes a nested `AutosarPackage`
- Classes are added to the deepest package level

Example:
```
Package: M2::AUTOSAR::DataTypes

Creates hierarchy:
AutosarPackage("AUTOSAR")
  └── AutosarPackage("DataTypes")
        └── AutosarClass(...)
```

### Test-Driven Development Workflow

When fixing bugs or adding features:

1. **Write a failing test** first that reproduces the issue
2. **Run the test** to confirm it fails:
   ```bash
   pytest tests/parser/test_pdf_parser.py::TestPdfParser::test_new_feature -v
   ```
3. **Implement the fix** in the source code
4. **Run the test** again to confirm it passes
5. **Run all tests** to ensure no regressions:
   ```bash
   python scripts/run_tests.py --unit
   ```
6. **Check coverage** to ensure new code is covered

## Troubleshooting

### Issue: Import Error for pdfplumber

**Error**: `ImportError: pdfplumber is not installed`

**Solution**:
```bash
pip install pdfplumber
```

### Issue: Type Checking Failures

**Error**: Mypy reports type errors

**Common causes**:
- Missing type hints on function parameters or return values
- Using `list[T]` instead of `List[T]` from typing
- Missing forward reference strings for circular dependencies

**Solution**: Add proper type hints following the coding standards in `docs/development/coding_rules.md`

### Issue: Tests Failing Due to Missing Requirements IDs

**Error**: Test or function missing requirement traceability

**Solution**: Add "Requirements:" section to docstrings with relevant requirement IDs:
```python
def parse_pdf(self, pdf_path: str) -> List[AutosarPackage]:
    """Parse a PDF file and extract the package hierarchy.

    Requirements:
        SWR_PARSER_00003: PDF File Parsing
        SWR_PARSER_00006: Package Hierarchy Building
    """
```

### Issue: Coverage Below 95%

**Solution**:
1. Check coverage report: `scripts/report/coverage.md`
2. Identify uncovered lines in specific files
3. Add tests for uncovered code paths
4. Re-run tests: `python scripts/run_tests.py --unit`


