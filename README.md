# AUTOSAR PDF to Markdown

A Python package for extracting AUTOSAR model hierarchies from PDF specification documents and converting them to markdown format.

## Features

- **Two-Phase Parsing Architecture**: Extracts all text using `pdfplumber` with precise word extraction, then processes the complete buffer with state management for multi-page definitions
- **Specialized Parsers**: Dedicated parsers for classes, enumerations, and primitives
- **Dataclass-Based Model**: Strongly-typed models with inheritance tracking
- **Multiple Output Formats**: Generate type-to-package mappings, class inheritance hierarchies, and detailed class documentation
- **Directory Support**: Process individual PDF files or entire directories
- **Source Tracking**: Tracks PDF file, page number, and optional AUTOSAR standard/release information

## Installation

```bash
pip install autosar-pdf2txt
```

For development:

```bash
git clone https://github.com/melodypapa/autosar-pdf.git
cd autosar-pdf
pip install -e .
```

## Quick Start

The `autosar-extract` command extracts AUTOSAR models from PDF files and generates various output formats.

### Basic Usage

```bash
# Generate type-to-package mapping
autosar-extract examples/pdf/ --mapping mapping.md

# Generate class inheritance hierarchy
autosar-extract examples/pdf/ --hierarchy hierarchy.md

# Generate individual class files (default Markdown format)
autosar-extract examples/pdf/ --class-details classes/

# Generate individual class files in JSON format
autosar-extract examples/pdf/ --class-details classes/ --json

# Generate individual class files with explicit Markdown format
autosar-extract examples/pdf/ --class-details classes/ --markdown

# Combine multiple outputs
autosar-extract examples/pdf/ --mapping data/mapping.md --hierarchy data/hierarchy.md --class-details data/packages/

autosar-extract examples/pdf/ --mapping data/mapping.json --hierarchy data/hierarchy.json --class-details data/packages/ --json
```

### Command-Line Options

- `pdf_files` - Path(s) to PDF file(s) or director(y/ies) containing PDFs
- `--mapping FILE` - Generate type-to-package mapping to FILE
- `--hierarchy FILE` - Generate class inheritance hierarchy to FILE
- `--class-details DIR` - Generate individual class files to DIR/
- `--json` - Generate class details in JSON format (requires --class-details)
- `--markdown` - Generate class details in Markdown format (requires --class-details)
- `-v, --verbose` - Enable verbose output mode for detailed debug information
- `--log-file FILE` - Write log messages to specified file

**Note**: At least one output flag (`--mapping`, `--hierarchy`, or `--class-details`) must be specified.

**Class Details Format**:
- Default: Markdown format (backward compatible)
- Use `--json` flag for JSON output with structured files
- Use `--markdown` flag for explicit Markdown output
- Cannot specify both `--json` and `--markdown`

### Output Format Auto-Detection

Output format is automatically detected from file extensions:
- `.md` - Markdown format
- `.yaml`, `.yml` - YAML format
- `.json` - JSON format

## Library Usage

You can also use the package programmatically:

```python
from autosar_pdf2txt import PdfParser, MarkdownWriter, MappingWriter

# Parse PDFs
parser = PdfParser()
doc = parser.parse_pdfs(["examples/pdf/AUTOSAR_CP_TPS_SystemTemplate.pdf"])

# Generate markdown
writer = MarkdownWriter()
writer.write_packages_to_files(doc.packages, output_path="output/")

# Generate mapping
mapping_writer = MappingWriter()
mapping = mapping_writer.write_mapping(doc.packages, format="markdown")
```

## Project Structure

```
src/autosar_pdf2txt/
├── __init__.py           # Package exports
├── cli/                  # Command-line interfaces
│   ├── autosar_cli.py     # Main CLI entry point
│   └── extract_tables_cli.py
├── models/               # Data models
│   ├── base.py           # Abstract base classes
│   ├── containers.py     # Package and document containers
│   ├── types.py          # Class, enumeration, primitive types
│   ├── attributes.py     # Attribute models
│   └── enums.py          # Enumerations
├── parser/               # PDF parsers
│   ├── pdf_parser.py     # Main PDF parser (two-phase architecture)
│   ├── base_parser.py    # Base parser utilities
│   ├── class_parser.py   # Class definition parser
│   ├── enumeration_parser.py
│   └── primitive_parser.py
└── writer/               # Output writers
    ├── markdown_writer.py
    ├── mapping_writer.py
    └── json_writer.py
```

## Testing

```bash
# Run all tests
python scripts/run_tests.py --all

# Run unit tests only
python scripts/run_tests.py --unit

# Run integration tests only
python scripts/run_tests.py --integration

# Run specific test file
pytest tests/models/test_autosar_models.py -v
```

Test coverage reports are automatically generated to `scripts/report/coverage.md`.

## Development

### Code Quality

```bash
# Linting
ruff check src/ tests/
ruff check --fix src/ tests/

# Type checking
mypy src/autosar_pdf2txt/

# Full CI pipeline
python scripts/run_tests.py --unit && ruff check src/ tests/ && mypy src/autosar_pdf2txt/
```

### Coding Standards

- **Type hints**: Required for all functions/methods
- **Docstrings**: Google-style with Args/Returns/Raises, including requirement IDs
- **Language**: All comments and docstrings in English
- **Style**: Ruff for linting, mypy for type checking

Complete standards: See `docs/development/coding_rules.md`

### TDD Workflow

All features and bug fixes must follow Test-Driven Development:

1. Document test case FIRST in `docs/test_cases/unit_tests.md` with test ID
2. Write failing test (Red phase) - Unit tests prioritized
3. Implement minimum code (Green phase)
4. Refactor if needed
5. Update requirements with maturity level

Complete TDD rules: See `docs/development/tdd_rules.md`

## Architecture

### Data Pipeline

```
PDF → PdfParser (Two-Phase) → Specialized Parsers → AutosarDoc → MarkdownWriter → Output
```

### Two-Phase Parsing

1. **Read Phase**: Extract all text using `extract_words(x_tolerance=1)`, insert `<<<PAGE:N>>>` markers
2. **Parse Phase**: Process complete buffer with state management for multi-page definitions

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
- **Source Location Tracking**: `AutosarDocumentSource` tracks PDF file and page number
- **Ancestry-based Parent Resolution**: Determine immediate parent from bases list
- **Subclasses Validation**: Detect inheritance contradictions
- **Model-Level Validation**: All validation in `__post_init__`, duplicate types log warnings

## Requirements Traceability

All code includes requirement IDs in docstrings. Requirements by module:
- **Model**: SWR_MODEL_00001 - SWR_MODEL_00027
- **Parser**: SWR_PARSER_00001 - SWR_PARSER_00030
- **Writer**: SWR_WRITER_00001 - SWR_WRITER_00008
- **CLI**: SWR_CLI_00001 - SWR_CLI_00014
- **Package**: SWR_PACKAGE_00001 - SWR_PACKAGE_00003

Full requirements: See `docs/requirements/requirements.md`

## License

MIT License - see LICENSE file for details

## Links

- [Homepage](https://github.com/melodypapa/autosar-pdf)
- [Issue Tracker](https://github.com/melodypapa/autosar-pdf/issues)
- [Documentation](docs/)
