# autosar-pdf2txt

A Python package to extract AUTOSAR package and class hierarchies from PDF specification documents and convert them to markdown format.

## Features

- **Multi-backend PDF Reading**: Supports pdfplumber, PyMuPDF (fitz), and pypdf with automatic backend selection
- **Hierarchy Parsing**: Parses asterisk-based hierarchy format to nested package structures
- **Duplicate Prevention**: Automatically removes duplicate packages and classes in output
- **CLI Tool**: Simple command-line interface for easy usage
- **High Test Coverage**: 99% test coverage with 107 tests

## Installation

### From source

```bash
git clone https://github.com/yourusername/autosar-pdf.git
cd autosar-pdf
pip install -e .
```

### Requirements

- Python 3.7 or higher
- pdfplumber (preferred) or pymupdf or pypdf

## Usage

### Command Line Interface

Extract AUTOSAR hierarchy from a PDF file:

```bash
autosar-extract input.pdf -o output.md
```

Extract with specific PDF backend:

```bash
autosar-extract input.pdf -o output.md --backend pdfplumber
```

### Python API

```python
from autosar_pdf2txt import parse_autosar_pdf, write_markdown

# Parse PDF to packages
packages = parse_autosar_pdf("path/to/file.pdf")

# Write to markdown
markdown = write_markdown(packages, deduplicate=True)

# Or use the classes directly
from autosar_pdf2txt.parser import AutosarParser
from autosar_pdf2txt.writer import MarkdownWriter

parser = AutosarParser(pdf_backend="auto")
packages = parser.parse_pdf("path/to/file.pdf")

writer = MarkdownWriter(deduplicate=True)
markdown = writer.write_packages(packages)
```

## Input Format

The tool expects AUTOSAR PDF documents with hierarchy formatted as:

```
* AUTOSARTemplates
  * BswModuleTemplate
    * BswBehavior
        * BswInternalBehavior
        * ExecutableEntity (abstract)
```

Where:
- Lines start with `*` followed by content
- Indentation (2 spaces per level) determines nesting
- Items with children are packages
- Items without children are classes
- `(abstract)` suffix indicates abstract classes

## Output Format

The tool generates markdown with the same asterisk-based hierarchy format:

```markdown
* AUTOSARTemplates
  * BswModuleTemplate
    * BswBehavior
        * BswInternalBehavior
        * ExecutableEntity (abstract)
```

## Development

### Setup Development Environment

```bash
# Install in editable mode
pip install -e .

# Install development dependencies
pip install pytest pytest-cov ruff mypy
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src/autosar_pdf2txt --cov-report=term-missing
```

### Linting and Type Checking

```bash
# Lint with ruff
ruff check src/autosar_pdf2txt/ tests/

# Type check with mypy
mypy src/autosar_pdf2txt/
```

## Project Structure

```
src/autosar_pdf2txt/
├── __init__.py
├── cli/
│   └── autosar_cli.py      # Command-line interface
├── models/
│   └── autosar_models.py   # AutosarClass and AutosarPackage dataclasses
├── parser/
│   ├── pdf_reader.py       # PDF text extraction
│   ├── hierarchy_parser.py # Hierarchy parsing
│   └── autosar_parser.py   # Integration layer
└── writer/
    └── markdown_writer.py  # Markdown output writer
```

## License

MIT License - see LICENSE file for details

## Author

Melodypapa <melodypapa@outlook.com>

## Version

0.1.0
