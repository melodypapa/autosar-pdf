# AGENTS.md

This document provides context information for iFlow CLI agents working on the autosar-pdf2txt project, helping agents understand the project structure, development standards, and workflows.

## Project Overview

**autosar-pdf2txt** is a Python package for extracting AUTOSAR model hierarchies from PDF specification documents and converting them to Markdown format.

### Core Features
- **PDF Extraction**: Extract AUTOSAR packages, classes, and enumerations from PDF specification documents
- **Hierarchical Parsing**: Parse complex hierarchical class structures with inheritance relationships
- **Markdown Output**: Generate well-formatted Markdown output with proper indentation
- **Class Details**: Support for abstract classes, attributes, and ATP markers
- **Class Hierarchy**: Generate separate class inheritance hierarchy files showing root classes and their subclasses
- **Individual Class Files**: Create separate markdown files for each class with detailed information
- **Model Validation**: Built-in duplicate prevention and validation at the model level
- **Comprehensive Coverage**: 96%+ test coverage with robust error handling

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
PDF Files → PdfParser → AutosarPackage/AutosarClass → MarkdownWriter → Markdown Output
```

#### Layered Structure

1. **Input Layer (CLI)**: `cli/autosar_cli.py`
   - Accepts file/directory paths
   - Validates inputs
   - Orchestrates the pipeline

2. **Parsing Layer**: `parser/pdf_parser.py`
   - Reads PDF files using pdfplumber
   - Extracts text line-by-line
   - Recognizes AUTOSAR patterns (Class, Package, Attributes, etc.)
   - Builds `ClassDefinition` intermediate objects
   - Constructs nested `AutosarPackage` hierarchy

3. **Model Layer**: `models/` directory, modular design
   - `base.py`: `AbstractAutosarBase` - shared base class for all AUTOSAR types
   - `enums.py`: `ATPType`, `AttributeKind` enumerations
   - `attributes.py`: `AutosarAttribute`, `AutosarEnumLiteral`
   - `types.py`: `AutosarClass`, `AutosarEnumeration`, `AutosarPrimitive` (inherit from `AbstractAutosarBase`)
   - `containers.py`: `AutosarPackage`, `AutosarDoc`
   - Unified type system: Packages contain `types` list (classes, enumerations, primitives)
   - Inheritance tracking: `AutosarClass` has `parent` and `children` attributes
   - Duplicate prevention at model level

4. **Output Layer**: `writer/markdown_writer.py`
   - Traverses package hierarchy
   - Generates markdown with proper indentation
   - Supports both consolidated output and per-class file generation

#### Directory Structure

```
src/autosar_pdf2txt/
├── __init__.py          # Package exports
├── models/
│   ├── __init__.py
│   ├── base.py            # AbstractAutosarBase abstract base class
│   ├── enums.py           # ATPType, AttributeKind enumerations
│   ├── attributes.py      # AutosarAttribute, AutosarEnumLiteral
│   ├── types.py           # AutosarClass, AutosarEnumeration, AutosarPrimitive
│   └── containers.py      # AutosarPackage, AutosarDoc
├── parser/
│   ├── __init__.py
│   └── pdf_parser.py      # PdfParser class for extracting AUTOSAR from PDFs
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
- Coverage reports automatically generated at `scripts/report/coverage.md`

### Test Patterns

**Exception Testing**:
```python
def test_add_class_duplicate(self) -> None:
    """Test adding duplicate class raises ValueError."""
    pkg = AutosarPackage(name="TestPackage")
    cls1 = AutosarClass(name="DuplicateClass", is_abstract=False)
    cls2 = AutosarClass(name="DuplicateClass", is_abstract=True)
    pkg.add_class(cls1)
    with pytest.raises(ValueError, match="already exists"):
        pkg.add_class(cls2)
```

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
- **Model**: SWR_MODEL_00001 - SWR_MODEL_00026
- **Parser**: SWR_PARSER_00001 - SWR_PARSER_00017
- **Writer**: SWR_WRITER_00001 - SWR_WRITER_00007
- **CLI**: SWR_CLI_00001 - SWR_CLI_00011
- **Package**: SWR_PACKAGE_00001 - SWR_PACKAGE_00003

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

3. **Verify regex patterns** in `pdf_parser.py` match the PDF format:
   - Class definitions: `CLASS_PATTERN`, `PRIMITIVE_PATTERN`, `ENUMERATION_PATTERN`
   - Package paths: `PACKAGE_PATTERN`
   - Attributes: `ATTRIBUTE_PATTERN` (checks for "Attribute Type Mult. Kind Note" header)
   - Enumeration literals: `ENUMERATION_LITERAL_HEADER_PATTERN`, `ENUMERATION_LITERAL_PATTERN`
   - ATP markers: `ATP_MIXED_STRING_PATTERN`, `ATP_VARIATION_PATTERN`, `ATP_MIXED_PATTERN`

4. **Check for attribute extraction issues**:
   - Verify attribute header recognition: "Attribute Type Mult. Kind Note"
   - Check for metadata lines being incorrectly parsed (SWR_PARSER_00011)
   - Look for multi-line attribute fragments (SWR_PARSER_00012)
   - Common problematic fragments: "Element", "SizeProfile", "data", "If", "has"

5. **Check for enumeration literal extraction**:
   - Verify literal header recognition: "Literal Description"
   - Ensure literals are being extracted with correct indices

6. **Check for M2 package prefixes** which affect hierarchy building

### Understanding Package Hierarchy

The parser builds package hierarchies from path strings like `"M2::AUTOSAR::DataTypes"`:

- `M2::` prefix is stripped during parsing
- `::` separator indicates nesting levels
- Each level becomes a nested `AutosarPackage`
- Types (classes, enumerations, primitives) are added to the deepest package level via `add_type()`
- Packages maintain a unified `types` collection containing all type variants

Example:
```
Package: M2::AUTOSAR::DataTypes

Creates hierarchy:
AutosarPackage("AUTOSAR")
  └── AutosarPackage("DataTypes")
        ├── AutosarClass("SwDataDefProps")
        ├── AutosarEnumeration("CategoryEnum")
        └── AutosarPrimitive("Limit")
```

### Understanding Model Inheritance

The model layer uses an abstract base class pattern:

```
AbstractAutosarBase (name, package, note)
    ├── AutosarClass (is_abstract, atp_type, attributes, bases, parent, children)
    ├── AutosarEnumeration (enumeration_literals)
    └── AutosarPrimitive (attributes)
```

- **AutosarClass**: Tracks inheritance with `bases` (all parents), `parent` (immediate parent), and `children` (derived classes)
- **AutosarEnumeration**: Contains `AutosarEnumLiteral` objects
- **AutosarPrimitive**: Represents primitive data types like `Limit`, `Interval`
- **AutosarPackage**: Contains unified `types` list (can hold any of the above types)

Access types in packages:
```python
# Unified access
typ = pkg.get_type("MyClass")  # Returns AutosarClass | AutosarEnumeration | AutosarPrimitive | None

# Specific access
cls = pkg.get_class("MyClass")  # Returns only AutosarClass | None
enum = pkg.get_enumeration("MyEnum")  # Returns only AutosarEnumeration | None
prim = pkg.get_primitive("Limit")  # Returns only AutosarPrimitive | None
```

### Test-Driven Development Workflow

When fixing bugs or adding features:

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

## Documentation Structure

The project maintains comprehensive documentation in the `docs/` directory:

- `docs/requirements/requirements.md` - Complete software requirements specification with stable IDs
- `docs/development/coding_rules.md` - Detailed coding standards combining PEP 8 with project-specific rules
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

Use these files to test parser changes or verify extraction behavior.

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
- Primitive type definitions: `Primitive <name>` (SWR_PARSER_00013)
- Enumeration type definitions: `Enumeration <name>` (SWR_PARSER_00013)
- Class definitions with ATP markers: `Class <name> <<atpMixedString>>`, `Class <name> <<atpVariation>>`, and `Class <name> <<atpMixed>>`
- Package definitions: `Package <M2::?><path>`
- Base classes: `Base <class_list>`
- Subclasses: `Subclasses <class_list>`
- Notes: `Note <text>` (documentation/comments)
- Attribute header: `Attribute Type Mult. Kind Note` (SWR_PARSER_00010)
- Enumeration literal header: `Literal Description` (SWR_PARSER_00014)
- Attributes: `<name> <type> <mult> <kind> <description>` (SWR_PARSER_00011, SWR_PARSER_00012)
- Enumeration literals: `<name> <description>` (SWR_PARSER_00015)

### PDF Text Extraction Strategy

The parser uses word-level extraction (pdfplumber's `extract_words()` with `x_tolerance=1`) instead of raw text extraction to properly handle word spacing and avoid concatenated words due to tight kerning in PDF files (SWR_PARSER_00009).

## Version Information

- **Current Version**: 0.15.0
- **Python Requirement**: >= 3.7
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