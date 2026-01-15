# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`autosar-pdf2txt` is a Python package for extracting text and structured metadata from PDF files, specifically designed for AUTOSAR template specification documents.

**autosar-extract** - AUTOSAR-specific package and class hierarchy extraction

## Development Commands

### Installation
```bash
pip install -e .
```

### Linting
```bash
ruff check src/autosar_pdf2txt/ tests/
```

### Type Checking
```bash
mypy src/autosar_pdf2txt/
```

### Running Tests
```bash
pytest tests/
```

## Architecture

### Package Structure

```
src/autosar_pdf2txt/
├── cli/                    # Command-line interfaces
│   └── autosar_cli.py      # AUTOSAR extraction tool (entry point: autosar-extract)
├── models/                 # Data models for AUTOSAR packages/classes
│   └── autosar_models.py   # AutosarClass and AutosarPackage dataclasses
├── parser/                 # PDF parsing and extraction logic
│   ├── pdf_reader.py       # PDF text extraction with backend abstraction
│   ├── hierarchy_parser.py # Parse asterisk-based hierarchy to nested packages
│   └── autosar_parser.py   # Integration of PDF reader and hierarchy parser
└── writer/                 # Markdown output writer with duplicate removal
```

### Project Purpose

This package extracts AUTOSAR (AUTomotive Open System ARchitecture) package and class hierarchies from PDF specification documents and converts them to markdown format.

Reference documentation:
- `docs/models/autosar_models.md` - Full AUTOSAR package/class reference
- `examples/pdf/Screenshot 2026-01-13 064408.png` - Visual reference of the hierarchy structure

### Data Models

**AutosarClass** (`models/autosar_models.py`):
- `name: str` - Class name
- `is_abstract: bool` - Whether the class is abstract
- Methods: `__str__()`, `__repr__()`, validation in `__post_init__()`

**AutosarPackage** (`models/autosar_models.py`):
- `name: str` - Package name
- `classes: List[AutosarClass]` - List of classes in this package
- `subpackages: List[AutosarPackage]` - List of subpackages (nested packages)
- Methods:
  - `add_class(cls: AutosarClass)` - Add a class (prevents duplicates)
  - `add_subpackage(pkg: AutosarPackage)` - Add a subpackage (prevents duplicates)
  - `get_class(name: str) -> AutosarClass | None` - Find a class by name
  - `get_subpackage(name: str) -> AutosarPackage | None` - Find a subpackage by name
  - `has_class(name: str) -> bool` - Check if class exists
  - `has_subpackage(name: str) -> bool` - Check if subpackage exists

### Parser Modules

**PDFReader** (`parser/pdf_reader.py`):
- Multi-backend PDF text extraction (pdfplumber, fitz, pypdf)
- Automatic backend selection or manual specification
- Handles page separation with form feeds

**HierarchyParser** (`parser/hierarchy_parser.py`):
- Parses asterisk-based hierarchy format to nested package structures
- Detects indentation levels for package nesting
- Identifies classes vs packages (has children = package)
- Extracts "(abstract)" suffix from class names

**AutosarParser** (`parser/autosar_parser.py`):
- Integration of PDFReader and HierarchyParser
- `parse_pdf(path)` - Parse AUTOSAR PDF to nested packages
- `parse_autosar_pdf(path)` - Functional interface

The hierarchy format uses asterisks (`*`) for indentation:
```
* ParentPackage
  * ChildPackage
      * Class
```

**Important**: Duplicate packages/classes within the same parent should be written to markdown only once (keep first occurrence, remove subsequent duplicates).

## Code Conventions

### Style Guidelines
- **Type hints** required on all function/method parameters and returns
- **Google-style docstrings** with Args/Returns/Raises sections
- **Import order**: standard library → third-party → local
- **Naming**: snake_case (functions), PascalCase (classes), UPPER_CASE (constants)
- **Error handling**: `ValueError` for invalid arguments, try-except for I/O operations
- **Comments**: English in code, Chinese in test docstrings
- **Two-tier API**: Always provide both functional and class-based implementations

### Parsing and Writing Requirements

**Duplicate Handling**:
- When extracting hierarchies from PDFs, track seen items within each parent context
- When writing to markdown, only write the first occurrence of any package/class
- Duplicate detection is case-sensitive and applies within the same parent level

**Hierarchy Parsing**:
- Detect indentation level by counting leading spaces/asterisks
- Maintain parent-child relationships during parsing
- Preserve the original hierarchy structure in output

### Error Handling Patterns

**File Operations**:
```python
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    raise ValueError(f"File not found: {file_path}")
except IOError as e:
    raise ValueError(f"Error reading file {file_path}: {e}")
```

### CLI Function Organization

CLI functions should be broken into smaller methods:
- `parse_arguments()` - Argument parsing logic
- `process_files()` - File processing orchestration
- `write_output()` - Markdown output handling
- Each method ≤ 50 lines where possible

### Example Files

Example PDFs are available in `examples/pdf/` for testing:
- `AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf`
- `AUTOSAR_CP_TPS_SoftwareComponentTemplate.pdf`

