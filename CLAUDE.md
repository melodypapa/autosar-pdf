# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`autosar-pdf2txt` is a Python package for extracting AUTOSAR model hierarchies from PDF specification documents and converting them to markdown format. The project uses a **two-phase parsing architecture** with specialized parsers for classes, enumerations, and primitives, a dataclass-based model with inheritance tracking, and a markdown writer supporting multiple output formats.

## Essential Commands

```bash
# Installation
pip install -e .

# Run tests (coverage auto-generated to scripts/report/coverage.md)
python scripts/run_tests.py --unit          # Unit tests only
python scripts/run_tests.py --integration   # Integration tests only
python scripts/run_tests.py --all           # All tests
pytest tests/models/test_autosar_models.py -v  # Specific test file

# Quality checks
ruff check src/ tests/                      # Linting
ruff check --fix src/ tests/                # Auto-fix
mypy src/autosar_pdf2txt/                   # Type checking

# Full CI pipeline
python scripts/run_tests.py --unit && ruff check src/ tests/ && mypy src/autosar_pdf2txt/

# Parse PDFs
autosar-extract examples/pdf/input.pdf -o output.md
autosar-extract examples/pdf/ -o output.md --include-class-details --include-class-hierarchy
```

## Test PDFs

The `examples/pdf/` directory contains AUTOSAR specification PDFs for testing (both CP and FO templates). Use these to verify parser changes.

## Architecture Overview

### Data Pipeline
```
PDF → PdfParser (Two-Phase) → Specialized Parsers → AutosarDoc → MarkdownWriter → Output
```

### Two-Phase Parsing (SWR_PARSER_00003)
1. **Read Phase**: Extract all text using `extract_words(x_tolerance=1)`, insert `<<<PAGE:N>>>` markers for tracking (SWR_PARSER_00030)
2. **Parse Phase**: Process complete buffer with state management for multi-page definitions, track page numbers

### Specialized Parsers
All inherit from `AbstractTypeParser` (SWR_PARSER_00023):
- `AutosarClassParser`: Class definitions, attributes, bases, subclasses, notes, aggregated_by
- `AutosarEnumerationParser`: Enumeration types and literals
- `AutosarPrimitiveParser`: Primitive types and attributes

### Model Layer
```
AbstractAutosarBase (name, package, note, source)
├── AutosarClass (is_abstract, atp_type, attributes, bases, parent, children, subclasses, aggregated_by)
├── AutosarEnumeration (enumeration_literals)
└── AutosarPrimitive (attributes)
```

**Key Design Principles**:
- **M2 Package Preservation**: `M2::` prefix preserved as root metamodel package
- **Unified Type System**: Packages contain unified `types` collection
- **Source Location Tracking**: `AutosarDocumentSource` tracks PDF file, page number, optional AUTOSAR standard/release (SWR_MODEL_00027)
- **Ancestry-based Parent Resolution**: Determine immediate parent from bases list (SWR_PARSER_00018)
- **Subclasses Validation**: Detect inheritance contradictions (SWR_PARSER_00029)
- **Model-Level Validation**: All validation in `__post_init__`, duplicate types log warnings

## Coding Standards

**Complete standards in `docs/development/coding_rules.md`**

- **Type hints**: Required for all functions/methods, use `|` for unions (Python 3.10+), use `List[T]` from typing
- **Docstrings**: Google-style with Args/Returns/Raises, include "Requirements:" section with relevant IDs
- **Imports**: Standard library → Third-party → Local (separated by blank lines)
- **Naming**: `snake_case` for functions, `PascalCase` for classes, `UPPER_CASE` for constants
- **Error handling**: Use `ValueError` in `__post_init__` for validation, logging module for CLI errors
- **Language**: All comments and docstrings in English

## TDD Workflow (MANDATORY)

**Critical**: All features and bug fixes MUST follow TDD. See `docs/development/tdd_rules.md` for complete details.

### Process
1. **Document test case FIRST** in `docs/test_cases/unit_tests.md` with test ID (e.g., SWUT_CLI_00037)
2. **Write failing test** (Red phase) - Unit tests prioritized over integration tests
3. **Implement minimum code** (Green phase)
4. **Refactor** if needed
5. **Update requirements** with maturity level

### Test Type Selection
- **Unit tests**: First priority for TDD cycle (faster, easier to debug)
- **Integration tests**: For validation with real PDFs from `examples/pdf/`

## Key Implementation Details

### PDF Parsing Patterns
- Class: `Class <name> (abstract)` with optional ATP markers (`<<atpMixedString>>`, etc.)
- Primitive: `Primitive <name>` (SWR_PARSER_00013)
- Enumeration: `Enumeration <name>` (SWR_PARSER_00013)
- Package: `Package <M2::?><path>` (M2 prefix preserved)
- Base classes: `Base <class_list>`
- Subclasses: `Subclasses <class_list>`
- Aggregated by: `Aggregated by <class_list>`
- Attribute header: `Attribute Type Mult. Kind Note` (SWR_PARSER_00010)
- Enumeration header: `Literal Description` (SWR_PARSER_00014)
- Attributes: `<name> <type> <mult> <kind> <description>` (SWR_PARSER_00011, SWR_PARSER_00012)
- Page markers: `<<<PAGE:N>>>` (inserted during read phase, SWR_PARSER_00030)

### Duplicate Handling
- Model-level duplicate prevention in `AutosarPackage.add_type()`, `add_class()`, `add_subpackage()`
- Duplicate types log warnings and are skipped (allows parsing multiple PDFs with same class names)
- No writer-level deduplication needed

### Markdown Output
- **Package hierarchy**: `* <name>` with `level * 2` spaces indent
- **Classes**: `* <name> (abstract)` with `(level + 1) * 2` spaces indent
- **Class hierarchy**: Separate file showing inheritance tree from root classes
- **Source table**: Markdown table with PDF File, Page, AUTOSAR Standard, Release columns (SWR_WRITER_00008)

## Testing

- Test files mirror source structure in `tests/`
- Test classes: `Test<ClassName>` for models, `Test<ModuleName>` for modules
- Test methods: `test_<method_name>_<scenario>` or `test_<scenario>`
- **Coverage goal**: ≥95% (currently 97%+)
- Reports auto-generated to `scripts/report/coverage.md`

## Critical Concepts

### Package Hierarchy
- Path `"M2::AUTOSAR::DataTypes"` creates nested packages: M2 → AUTOSAR → DataTypes
- `M2::` prefix is **preserved** (M2 is root metamodel package)
- Types added to deepest level via `add_type()`
- Query with: `pkg.get_type()`, `pkg.get_class()`, `pkg.get_enumeration()`, `pkg.get_primitive()`

### Multi-Page Definitions
- State managed via `current_models` and `model_parsers` dictionaries
- `current_page` variable tracks page number (SWR_PARSER_00030)
- Enables parsing across page boundaries

### Attribute Extraction
- Recognizes "Attribute Type Mult. Kind Note" header (SWR_PARSER_00010)
- Filters metadata lines with `:`, `;`, or leading numbers (SWR_PARSER_00011)
- Handles multi-line attributes by detecting broken fragments (SWR_PARSER_00012)
- Common filtered fragments: "Element", "SizeProfile", "data", "If", "has"

## Requirements Traceability

All code includes requirement IDs in docstrings. Requirements by module:
- **Model**: SWR_MODEL_00001 - SWR_MODEL_00027
- **Parser**: SWR_PARSER_00001 - SWR_PARSER_00030
- **Writer**: SWR_WRITER_00001 - SWR_WRITER_00008
- **CLI**: SWR_CLI_00001 - SWR_CLI_00014
- **Package**: SWR_PACKAGE_00001 - SWR_PACKAGE_00003

Full requirements in `docs/requirements/requirements.md`.

## Quality Gates

Before committing:
```bash
python scripts/run_tests.py --unit && ruff check src/ tests/ && mypy src/autosar_pdf2txt/
```

All must pass:
1. ✅ Ruff: No errors
2. ✅ Mypy: No issues
3. ✅ Pytest: All tests pass
4. ✅ Coverage: ≥95%

## Documentation

- `docs/requirements/` - Software requirements with stable IDs
- `docs/development/coding_rules.md` - Complete coding standards
- `docs/development/tdd_rules.md` - TDD methodology
- `scripts/report/coverage.md` - Auto-generated coverage reports

## Common Tasks

### Debugging PDF Parsing
```bash
# Enable verbose mode
autosar-extract input.pdf -v

# Check text extraction
python -c "import pdfplumber; pdf = pdfplumber.open('input.pdf'); print([p.extract_text() for p in pdf.pages])"
```

Check regex patterns in:
- `class_parser.py`: CLASS_PATTERN, ATTRIBUTE_HEADER_PATTERN, ATTRIBUTE_PATTERN
- `enumeration_parser.py`: ENUMERATION_PATTERN, ENUMERATION_LITERAL_HEADER_PATTERN
- `base_parser.py`: PACKAGE_PATTERN, ATP markers

### Adding Features
1. Add requirement to `docs/requirements/requirements.md` with next ID
2. Implement with requirement IDs in docstrings
3. Add tests to appropriate test file
4. Update maturity levels
5. Run quality checks

