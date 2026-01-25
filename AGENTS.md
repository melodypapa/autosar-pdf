# AGENTS.md

This document provides context information for iFlow CLI agents working on the autosar-pdf2txt project, helping agents understand the project structure, development standards, and workflows.

## Project Overview

**autosar-pdf2txt** is a Python package for extracting AUTOSAR model hierarchies from PDF specification documents and converting them to Markdown format.

### Core Features
- **PDF Extraction**: Extract AUTOSAR packages, classes, enumerations, and primitive types from PDF specification documents
- **Two-Phase Parsing**: Read phase extracts all text from PDF, parse phase processes complete buffer for multi-page definitions
- **Specialized Parsers**: Dedicated parsers for classes, enumerations, and primitive types with shared base functionality
- **Hierarchical Parsing**: Parse complex hierarchical class structures with inheritance relationships
- **Source Location Tracking**: Track PDF file and page number for each type definition and base class reference, with optional AUTOSAR standard and release information
- **Markdown Output**: Generate well-formatted Markdown output with proper indentation
- **Class Details**: Support for abstract classes, attributes, ATP markers, and source information
- **Class Hierarchy**: Generate separate class inheritance hierarchy files showing root classes and their subclasses
- **Individual Class Files**: Create separate markdown files for each class with detailed information
- **Model Validation**: Built-in duplicate handling with warnings for multiple PDFs that may define the same class name
- **Subclasses Validation**: Validate subclass relationships against actual inheritance hierarchy (SWR_PARSER_00029)
- **Log File Support**: CLI supports persistent logging with timestamps via --log-file option
- **Comprehensive Coverage**: 97%+ test coverage with robust error handling

### Technology Stack
- **Language**: Python 3.7+
- **Core Dependency**: pdfplumber (PDF parsing)
- **Development Tools**:
  - pytest (testing framework)
  - pytest-cov (coverage)
  - ruff (code linting)
  - mypy (type checking)

### Project Architecture

The project follows a **pipeline architecture** with clear separation of concerns:

```
PDF Files → PdfParser (Two-Phase) → Specialized Parsers → AutosarDoc → MarkdownWriter → Markdown Output
```

#### Layered Structure

1. **Input Layer (CLI)**: `cli/autosar_cli.py`
   - Accepts file/directory paths
   - Validates inputs
   - Orchestrates the pipeline

2. **Parsing Layer**: `parser/` directory with two-phase architecture
   - **Two-Phase Approach** (SWR_PARSER_00003):
     - **Read Phase**: Extract all text from all pages using pdfplumber's `extract_words()` with `x_tolerance=1`
     - **Parse Phase**: Process complete text buffer with state management for multi-page definitions
   - **Base Parser** (`base_parser.py`): `AbstractTypeParser` - shared functionality for all specialized parsers
     - Common regex patterns
     - Attribute validation and filtering
     - Package path validation
     - ATP marker validation
     - Source location tracking
   - **Specialized Parsers**:
     - `class_parser.py`: `AutosarClassParser` - parses class definitions, attributes, base classes, subclasses
     - `enumeration_parser.py`: `AutosarEnumerationParser` - parses enumeration types and literals
     - `primitive_parser.py`: `AutosarPrimitiveParser` - parses primitive type definitions
   - **Orchestrator** (`pdf_parser.py`): `PdfParser` - coordinates specialized parsers, manages two-phase process
   - **Parent Resolution**: Ancestry-based parent resolution with subclass validation (SWR_PARSER_00018, SWR_PARSER_00029)

3. **Model Layer**: `models/` directory, modular design
   - `base.py`: `AbstractAutosarBase` - shared base class for all AUTOSAR types, `AutosarDocumentSource` for location tracking
   - `enums.py`: `ATPType`, `AttributeKind` enumerations
   - `attributes.py`: `AutosarAttribute`, `AutosarEnumLiteral`
   - `types.py`: `AutosarClass`, `AutosarEnumeration`, `AutosarPrimitive` (inherit from `AbstractAutosarBase`)
   - `containers.py`: `AutosarPackage`, `AutosarDoc`
   - Unified type system: Packages contain `types` list (classes, enumerations, primitives)
   - Inheritance tracking: `AutosarClass` has `bases`, `parent`, `children`, `subclasses`, `aggregated_by` attributes
   - Source location: Each type can track its definition location (PDF file and page number)
   - Duplicate prevention at model level

4. **Output Layer**: `writer/markdown_writer.py`
   - Traverses package hierarchy
   - Generates markdown with proper indentation
   - Supports both consolidated output and per-class file generation
   - Writes source information (PDF file and page number)

#### Directory Structure

```
src/autosar_pdf2txt/
├── __init__.py          # Package exports and version
├── models/
│   ├── __init__.py
│   ├── base.py            # AbstractAutosarBase, AutosarDocumentSource
│   ├── enums.py           # ATPType, AttributeKind enumerations
│   ├── attributes.py      # AutosarAttribute, AutosarEnumLiteral
│   ├── types.py           # AutosarClass, AutosarEnumeration, AutosarPrimitive
│   └── containers.py      # AutosarPackage, AutosarDoc
├── parser/
│   ├── __init__.py
│   ├── base_parser.py     # AbstractTypeParser base class with shared functionality
│   ├── class_parser.py    # AutosarClassParser for class definitions
│   ├── enumeration_parser.py  # AutosarEnumerationParser for enumerations
│   ├── primitive_parser.py    # AutosarPrimitiveParser for primitives
│   └── pdf_parser.py      # PdfParser orchestrator with two-phase parsing
├── writer/
│   ├── __init__.py
│   └── markdown_writer.py # MarkdownWriter class
└── cli/
    ├── __init__.py
    ├── autosar_cli.py     # Main command-line interface
    └── extract_tables_cli.py # Table extraction CLI
```

## Building and Running

### Installation

```bash
# Install in editable mode (recommended for development)
pip install -e .

# Or install from source
git clone https://github.com/melodypapa/autosar-pdf.git
cd autosar-pdf
pip install -e .
```

### Running Tests

```bash
# Run all tests (automatically generates coverage report to scripts/report/coverage.md)
python scripts/run_tests.py --all

# Run only unit tests
python scripts/run_tests.py --unit

# Run only integration tests
python scripts/run_tests.py --integration

# Run specific test file
pytest tests/models/test_autosar_models.py -v

# Run specific test with verbose output
pytest tests/models/test_autosar_models.py::TestAutosarClass::test_init_concrete_class -v
```

### Code Quality Checks

```bash
# Lint with ruff
ruff check src/ tests/

# Auto-fix issues where possible
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

### Command Line Interface Usage

**autosar-extract** - Extract AUTOSAR models from PDF files:

```bash
# Parse a single PDF and output to stdout
autosar-extract input.pdf

# Parse multiple PDFs and save to file
autosar-extract file1.pdf file2.pdf -o output.md

# Parse all PDFs in a directory
autosar-extract /path/to/pdfs/

# Verbose debug mode
autosar-extract input.pdf -v

# Create separate markdown files for each class
autosar-extract input.pdf -o output.md --include-class-details

# Generate class inheritance hierarchy in separate file
autosar-extract input.pdf -o output.md --include-class-hierarchy

# Write log messages to a file with timestamps
autosar-extract input.pdf -o output.md --log-file extraction.log

# Combine multiple options
autosar-extract input.pdf -o output.md --include-class-details --include-class-hierarchy --log-file extraction.log -v
```

**autosar-extract-table** - Extract AUTOSAR-related tables from PDF files as images (SWR_CLI_00013):

```bash
# Extract tables from a single PDF
autosar-extract-table input.pdf -o output_dir/

# Extract tables from multiple PDFs
autosar-extract-table file1.pdf file2.pdf -o output_dir/

# Extract tables from all PDFs in a directory
autosar-extract-table /path/to/pdfs/ -o output_dir/

# Verbose mode for detailed debug information
autosar-extract-table input.pdf -o output_dir/ -v
```

## Development Standards

### Type Hints
- All functions and methods must have type hints for parameters and return values
- Use `|` for union types (e.g., `str | None`) - Python 3.10+ syntax
- Use `List[T]` from typing for lists (not built-in `list[T]`)

### Docstrings
- Use Google-style docstrings with Args/Returns/Raises sections
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
- Perform dataclass validation in `__post_init__`
- Raise errors immediately on validation failure
- Use logging module for CLI error messages (not print to stderr)

### Comments and Docstrings
- All comments and docstrings must be in **English**

### Detailed Coding Standards

Complete coding standards are documented in `docs/development/coding_rules.md`, combining project-specific rules with PEP 8 standards.

Key coding rules summary:

1. **Indentation**: Use 4 spaces per indentation level (never tabs)
2. **Maximum line length**: 79 characters (72 for docstrings and comments)
3. **String quotes**: Use double quotes (except when string contains double quotes)
4. **Import order**: Standard library → Third-party → Local, separated by blank lines
5. **Type hints**: All function parameters and return values must have type hints
6. **Docstrings**: Google style, include Requirements section
7. **Avoid duplication**: Extract repeated logic into reusable components (DRY principle)

## Testing

### Test Structure
- Test files mirror source structure in `tests/` directory
- Test classes named `Test<ClassName>` for models, `Test<ModuleName>` for modules
- Test methods: `test_<method_name>_<scenario>` or `test_<scenario>`
- All test docstrings must be in English

### Coverage Goals
- Target 100% coverage for all modules (currently at 97%+)
- Tests cover success paths, error paths, and edge cases
- Coverage reports automatically generated at `scripts/report/coverage.md` after each test run

### Test Patterns

**Exception Testing**:
```python
def test_add_class_duplicate(self) -> None:
    """Test adding duplicate class logs warning and skips."""
    pkg = AutosarPackage(name="TestPackage")
    cls1 = AutosarClass(name="DuplicateClass", is_abstract=False)
    cls2 = AutosarClass(name="DuplicateClass", is_abstract=True)
    pkg.add_class(cls1)
    with pytest.warns(UserWarning, match="already exists"):
        pkg.add_class(cls2)
    # Verify only one class was added
    assert len(pkg.types) == 1
    assert pkg.types[0].name == "DuplicateClass"
```

### Test-Driven Development (TDD) - MANDATORY

**Critical Rule**: All new features and bug fixes MUST follow TDD methodology.

**TDD Process** (see `docs/development/tdd_rules.md` for complete details):

1. **Document Test Case FIRST** in `docs/test_cases/unit_tests.md`
   - Test case ID (e.g., SWUT_CLI_00037)
   - Test case title
   - Requirement traceability
   - Test description, steps, expected results

2. **Write Failing Test** (Red phase)
   - Write test based on documentation
   - Verify test fails

3. **Implement Minimum Code** (Green phase)
   - Write only enough code to make test pass
   - Verify test passes

4. **Refactor** (if needed)
   - Improve code quality
   - Verify all tests pass

5. **Update Requirements**
   - Add/update requirement with maturity level
   - Update requirement index

**Common TDD Violations to Avoid**:
- ❌ Implementing feature before writing tests
- ❌ Skipping test case documentation
- ❌ Writing too much code at once
- ❌ Not running tests frequently

**TDD Checklist** (see `docs/development/tdd_rules.md` for complete checklist):
- [ ] Document test case in `docs/test_cases/unit_tests.md`
- [ ] Write failing unit test
- [ ] Implement minimum code to pass
- [ ] Refactor if needed
- [ ] Update requirements
- [ ] Run quality checks

**Why TDD is Mandatory**:
- Ensures code matches requirements
- Provides executable documentation
- Prevents over-engineering
- Catches bugs early
- Facilitates refactoring
- Improves code quality

## Quality Gates

Before committing changes, run the following quality checks to ensure code quality:

### Quality Gate Workflow
```bash
# Run all quality checks in sequence
python scripts/run_tests.py --unit && ruff check src/ tests/ && mypy src/autosar_pdf2txt/
```

### Quality Standards
All of the following must pass before committing:
1. ✅ Ruff linting: No errors
2. ✅ Mypy type checking: No issues
3. ✅ Pytest: All tests pass
4. ✅ Coverage: ≥95%

## Requirement Traceability

All code includes requirement IDs in docstrings for traceability to `docs/requirements/requirements.md`. Coding standards are defined in `docs/development/coding_rules.md` with stable identifiers.

**Requirements by Module**:
- **Model**: SWR_MODEL_00001 - SWR_MODEL_00027
- **Parser**: SWR_PARSER_00001 - SWR_PARSER_00029
- **Writer**: SWR_WRITER_00001 - SWR_WRITER_00008
- **CLI**: SWR_CLI_00001 - SWR_CLI_00014
- **Package**: SWR_PACKAGE_00001 - SWR_PACKAGE_00003

**Key New Requirements**:
- SWR_PARSER_00003: Two-phase PDF parsing approach (read phase + parse phase)
- SWR_PARSER_00018: Ancestry-based parent resolution
- SWR_PARSER_00023: Abstract base parser for common functionality
- SWR_PARSER_00027: Parser backward compatibility
- SWR_PARSER_00028: Direct model creation by specialized parsers
- SWR_PARSER_00029: Subclasses contradiction validation
- SWR_MODEL_00018: AUTOSAR type abstract base class
- SWR_MODEL_00027: AUTOSAR source location representation with optional AUTOSAR standard and release
- SWR_WRITER_00008: Markdown source information output
- SWR_CLI_00014: CLI logger file specification for persistent logging with timestamps

## Custom Slash Commands

The project includes custom slash commands in `.claude/commands/` directory for automating common workflows:

### `/gh-workflow` - GitHub Workflow Automation
Automates the complete GitHub workflow:
1. Create GitHub issue based on changes
2. Create feature branch
3. Stage and commit changes
4. Push to GitHub only (not gitee)
5. Create pull request

### `/merge-pr` - Merge Pull Request
Check pull request status, merge it, and return to master branch.

### `/test` - Test Runner
Run the project test suite with comprehensive reporting.

### `/quality` - Quality Check
Run all quality checks (linting, type checking, testing) to ensure code meets project standards.

### `/parse` - PDF Parser
Parse AUTOSAR PDF files and extract model hierarchies.

### `/req` - Requirement Management
Manage AUTOSAR project requirements with traceability.

### `/sync-docs` - Synchronize Documentation
Synchronize requirements, test cases, and source code to ensure consistency across the codebase.

## Common Development Tasks

### Adding a New Requirement

When implementing new features, follow this workflow:

1. **Add the requirement to** `docs/requirements/requirements.md`:
   - Use the next available ID in the sequence (e.g., `SWR_MODEL_00027`)
   - Set maturity to `draft`
   - Include description and acceptance criteria

2. **Implement the feature in** the appropriate module:
   - Add requirement ID to all relevant docstrings
   - Follow coding standards in `docs/development/coding_rules.md`
   - Include type hints and Google-style docstrings
   - For new types, inherit from `AbstractAutosarBase` if applicable

3. **Add tests to** the appropriate test file:
   - Use the next available test ID (e.g., `SWUT_MODEL_00027`)
   - Test success paths, error paths, and edge cases
   - Include requirement ID in test docstrings
   - Target 100% coverage for new code

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

3. **Verify regex patterns** in specialized parsers match the PDF format:
   - **Class Parser** (`class_parser.py`): `CLASS_PATTERN`, `ATTRIBUTE_HEADER_PATTERN`, `ATTRIBUTE_PATTERN`
   - **Enumeration Parser** (`enumeration_parser.py`): `ENUMERATION_PATTERN`, `ENUMERATION_LITERAL_HEADER_PATTERN`, `ENUMERATION_LITERAL_PATTERN`
   - **Primitive Parser** (`primitive_parser.py`): `PRIMITIVE_PATTERN`
   - **Base Parser** (`base_parser.py`): `PACKAGE_PATTERN`, `ATP_MIXED_STRING_PATTERN`, `ATP_VARIATION_PATTERN`, `ATP_MIXED_PATTERN`

4. **Check two-phase parsing issues**:
   - Verify read phase is extracting all text correctly
   - Check parse phase state management for multi-page definitions
   - Look for issues with current_models and model_parsers dictionaries

5. **Check for attribute extraction issues**:
   - Verify attribute header recognition: "Attribute Type Mult. Kind Note"
   - Check for metadata lines being incorrectly parsed (SWR_PARSER_00011)
   - Look for multi-line attribute fragments (SWR_PARSER_00012)
   - Common problematic fragments: "Element", "SizeProfile", "data", "If", "has"

6. **Check for enumeration literal extraction**:
   - Verify literal header recognition: "Literal Description"
   - Ensure literals are being extracted with correct indices

7. **Check for parent resolution issues**:
   - Verify ancestry-based parent resolution is working correctly
   - Check for circular inheritance detection
   - Validate subclass relationships (SWR_PARSER_00029)

8. **Check for M2 package prefixes** which affect hierarchy building (prefix is now preserved)

9. **Check source location tracking**:
   - Verify AutosarDocumentSource is being attached to types correctly
   - Check PDF file names and page numbers are accurate

### Understanding Package Hierarchy

The parser builds package hierarchies from path strings like `"M2::AUTOSAR::DataTypes"`:

- `M2::` prefix is **preserved** (M2 is treated as the root metamodel package)
- `::` separator indicates nesting levels
- Each level becomes a nested `AutosarPackage`
- Types (classes, enumerations, primitives) are added to the deepest package level via `add_type()`
- Packages maintain a unified `types` collection containing all type variants

Example:
```
Package: M2::AUTOSAR::DataTypes

Creates hierarchy:
AutosarPackage("M2")
  └── AutosarPackage("AUTOSAR")
        └── AutosarPackage("DataTypes")
              ├── AutosarClass("SwDataDefProps")
              ├── AutosarEnumeration("CategoryEnum")
              └── AutosarPrimitive("Limit")
```

### Understanding Model Inheritance

The model layer uses an abstract base class pattern:

```
AbstractAutosarBase (name, package, note, source)
    ├── AutosarClass (is_abstract, atp_type, attributes, bases, parent, children, subclasses, aggregated_by)
    ├── AutosarEnumeration (enumeration_literals)
    └── AutosarPrimitive (attributes)
```

- **AutosarClass**: Tracks inheritance with `bases` (all parents), `parent` (immediate parent), `children` (derived classes), `subclasses` (explicitly documented subclasses), and `aggregated_by` (classes that aggregate this class)
- **AutosarClass**: Includes `source` attribute tracking PDF file and page number where the class was defined
- **AutosarEnumeration**: Contains `AutosarEnumLiteral` objects
- **AutosarPrimitive**: Represents primitive data types like `Limit`, `Interval`
- **AutosarPackage**: Contains unified `types` list (can hold any of the above types)
- **AutosarDoc**: Document-level container for packages and root classes, provides query methods

Access types in packages:
```python
# Unified access
typ = pkg.get_type("MyClass")  # Returns AutosarClass | AutosarEnumeration | AutosarPrimitive | None

# Specific access
cls = pkg.get_class("MyClass")  # Returns only AutosarClass | None
enum = pkg.get_enumeration("MyEnum")  # Returns only AutosarEnumeration | None
prim = pkg.get_primitive("Limit")  # Returns only AutosarPrimitive | None
```

Document-level operations:
```python
# Parse PDF and get AutosarDoc
parser = PdfParser()
doc = parser.parse_pdf("file.pdf")

# Query packages and root classes
pkg = doc.get_package("AUTOSAR")
root_cls = doc.get_root_class("SwComponentPrototype")
```

### Test-Driven Development Workflow

When fixing bugs or adding features, follow the Red-Green-Refactor cycle:

1. **Write a failing test first** that reproduces the issue
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

**TDD Guidelines** (see `docs/development/tdd_rules.md`):
- **Unit tests as first priority**: Use unit tests for TDD cycle (faster, easier to debug, no external dependencies)
- **Integration tests for validation**: Integration tests MUST use real PDF files from `examples/pdf/` directory
- Integration tests verify end-to-end functionality with actual AUTOSAR specification documents
- Integration tests are used for final validation and regression testing

## Documentation Structure

The project maintains comprehensive documentation in the `docs/` directory:

- `docs/requirements/requirements.md` - Complete software requirements specification index with stable IDs
- `docs/requirements/requirements_model.md` - Model requirements (SWR_MODEL_00001 - SWR_MODEL_00027)
- `docs/requirements/requirements_parser.md` - Parser requirements (SWR_PARSER_00001 - SWR_PARSER_00029)
- `docs/requirements/requirements_writer.md` - Writer requirements (SWR_WRITER_00001 - SWR_WRITER_00008)
- `docs/requirements/requirements_cli.md` - CLI requirements (SWR_CLI_00001 - SWR_CLI_00013)
- `docs/requirements/requirements_package.md` - Package requirements (SWR_PACKAGE_00001 - SWR_PACKAGE_00003)
- `docs/development/coding_rules.md` - Detailed coding standards combining PEP 8 with project-specific rules
- `docs/development/tdd_rules.md` - Test-driven development rules and guidelines
- `docs/development/test_update_rules.md` - Test update procedures
- `docs/development/integration_test_performance.md` - Integration test performance guidelines
- `docs/development/version_control.md` - Version control practices
- `docs/models/` - Model-specific documentation
- `docs/test_cases/` - Test case documentation with traceability to requirements
- `scripts/report/coverage.md` - Auto-generated coverage reports (updated after each test run)

## Example PDF Files

The `examples/pdf/` directory contains sample AUTOSAR specification PDFs for testing:

- `AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf`
- `AUTOSAR_CP_TPS_DiagnosticExtractTemplate.pdf`
- `AUTOSAR_CP_TPS_ECUConfiguration.pdf`
- `AUTOSAR_CP_TPS_ECUResourceTemplate.pdf`
- `AUTOSAR_CP_TPS_SoftwareComponentTemplate.pdf`
- `AUTOSAR_CP_TPS_SystemTemplate.pdf`
- `AUTOSAR_CP_TPS_TimingExtensions.pdf`
- `AUTOSAR_FO_TPS_GenericStructureTemplate.pdf`

Use these files to test parser changes or verify extraction behavior.

## Key Implementation Details

### Two-Phase PDF Parsing (SWR_PARSER_00003)

The parser uses a two-phase approach to handle multi-page definitions:

1. **Read Phase**:
   - Extract all text from all pages using pdfplumber's `extract_words()` with `x_tolerance=1`
   - Reconstruct text from words while preserving line breaks based on vertical position
   - Accumulate all pages' text into a single StringIO buffer

2. **Parse Phase**:
   - Process all lines sequentially from the complete text buffer
   - Maintain state management for multi-page definitions via `current_models` and `model_parsers` dictionaries
   - Delegate to appropriate specialized parsers (class, enumeration, primitive) for each type definition
   - Continue parsing for existing models across page boundaries

**Benefits**:
- Complete text available for analysis before parsing begins
- Simpler debugging with all text in a single buffer
- Consistent handling of multi-page definitions through state management
- Better separation of concerns between reading and parsing phases

### Specialized Parser Architecture

The parser uses specialized parsers for each AUTOSAR type, all inheriting from `AbstractTypeParser`:

- **`AutosarClassParser`**: Handles class definitions, attributes, base classes, subclasses, notes
- **`AutosarEnumerationParser`**: Handles enumeration type definitions and literals
- **`AutosarPrimitiveParser`**: Handles primitive type definitions and attributes

**Shared Functionality** (in `AbstractTypeParser`):
- Common regex patterns for type definitions
- Attribute validation and filtering logic
- Package path validation
- ATP marker detection and validation
- Source location tracking

### Source Location Tracking (SWR_MODEL_00027)

Each AUTOSAR type can track its definition location using `AutosarDocumentSource`:

```python
@dataclass(frozen=True)
class AutosarDocumentSource:
    pdf_file: str                      # Path to the PDF file
    page_number: int                   # Page number (1-indexed)
    autosar_standard: Optional[str]    # AUTOSAR standard identifier (e.g., "TPS_BSWModuleDescriptionTemplate")
    standard_release: Optional[str]    # AUTOSAR standard release (e.g., "R21-11")
```

Types include source location in their `source` attribute, enabling traceability back to the original PDF documentation with optional AUTOSAR standard and release information.

### Parent Resolution and Validation (SWR_PARSER_00018, SWR_PARSER_00029)

The parser uses ancestry-based parent resolution:

1. **Parent Resolution**: After all classes are parsed, analyze each class's `bases` list to determine the immediate parent
2. **Subclasses Validation**: Validate that the `subclasses` attribute does not contain contradictions:
   - Subclass must actually exist in the model
   - Subclass must have this class in its `bases` list
   - Subclass cannot be in this class's `bases` list (circular inheritance)
   - Subclass cannot be in this class's parent's `bases` list (would be an ancestor)
   - Subclass cannot be the parent class itself

### Markdown Indentation Rules
- Packages: indent = `level * 2` spaces
- Classes: indent = `(level + 1) * 2` spaces (1 level deeper than parent package)
- Format: `* <name>` or `* <name> (abstract)`

### Duplicate Handling
- Model-level duplicate handling in `AutosarPackage.add_type()`, `add_class()`, and `add_subpackage()`
- Checks for duplicates by name before adding
- Logs warnings and skips duplicate type definitions (allows parsing multiple PDFs that may define the same class name, which is common in AUTOSAR specifications)
- Raises `ValueError` when attempting to add duplicate subpackages
- No writer-level deduplication needed (model guarantees uniqueness)

### Model Validation
- Empty/whitespace names raise `ValueError`
- Duplicate types in package log warnings and are skipped (allows parsing multiple PDFs with same class names)
- Duplicate subpackages in package raise `ValueError`
- Multiple ATP markers on same class raise `ValueError`
- Subclasses contradictions raise `ValueError` with descriptive messages (SWR_PARSER_00029)

### PDF Parsing Patterns
- Class definitions: `Class <name> (abstract)`
- Primitive type definitions: `Primitive <name>` (SWR_PARSER_00013)
- Enumeration type definitions: `Enumeration <name>` (SWR_PARSER_00013)
- Class definitions with ATP markers: `Class <name> <<atpMixedString>>`, `Class <name> <<atpVariation>>`, and `Class <name> <<atpMixed>>`
- Package definitions: `Package <M2::?><path>` (M2 prefix is preserved)
- Base classes: `Base <class_list>` (extracted from Base column in class tables)
- Subclasses: `Subclasses <class_list>` (descendants that inherit from this class)
- Notes: Extracted from Note column, may span multiple lines until next known pattern
- Attribute header: `Attribute Type Mult. Kind Note` (SWR_PARSER_00010)
- Enumeration literal header: `Literal Description` (SWR_PARSER_00014)
- Attributes: `<name> <type> <mult> <kind> <description>` (SWR_PARSER_00011, SWR_PARSER_00012)
- Enumeration literals: `<name> <description>` (SWR_PARSER_00015)

### PDF Text Extraction Strategy

The parser uses word-level extraction (pdfplumber's `extract_words()` with `x_tolerance=1`) instead of raw text extraction to properly handle word spacing and avoid concatenated words due to tight kerning in PDF files (SWR_PARSER_00009).

### M2 Package Prefix Handling

The parser preserves the "M2::" prefix in package paths when present, treating "M2" as the root metamodel package. This ensures complete package hierarchy is maintained (e.g., M2 → AUTOSARTemplates → BswModuleTemplate).

## Changelog

### Version 0.16.0
- Added CLI log file support (`--log-file`) for persistent logging with timestamps (SWR_CLI_00014)
- Implemented subclasses validation (SWR_PARSER_00029) to detect inheritance contradictions
- Refactored duplicate type handling to log warnings instead of raising errors, allowing parsing of multiple PDFs that may define the same class name
- Enhanced AutosarDocumentSource with optional AUTOSAR standard and release fields
- Enhanced test documentation with 15 new test cases for log file feature
- Enhanced test documentation with 10 new test cases for subclasses validation
- Improved test coverage from 96% to 97%
- Updated AGENTS.md with mandatory TDD section
- Updated development guidelines with TDD enforcement and common mistakes

### Version 0.15.0
- Implemented two-phase PDF parsing approach (read phase + parse phase)
- Added specialized parsers for classes, enumerations, and primitives
- Added ancestry-based parent resolution for complex inheritance hierarchies
- Added source location tracking for PDF file and page number
- Added subclasses attribute to track explicitly documented subclass relationships
- Refactored requirements documentation into separate module files
- Enhanced TDD rules with test type selection strategy
- Fixed multi-line class list parsing and multi-page class definition handling

## Version Information

- **Current Version**: 0.16.0
- **Python Requirement**: >= 3.7 (supports 3.7, 3.8, 3.9, 3.10, 3.11)
- **Main Dependency**: pdfplumber >= 0.10.0

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please ensure:

1. All tests pass: `pytest tests/`
2. Code coverage remains ≥95%
3. Linting passes: `ruff check src/ tests/`
4. Type checking passes: `mypy src/autosar_pdf2txt/`

## Project Links

- **GitHub Repository**: https://github.com/melodypapa/autosar-pdf
- **Issue Tracker**: https://github.com/melodypapa/autosar-pdf/issues
- **Documentation**: See `docs/` directory for detailed requirements and development guidelines