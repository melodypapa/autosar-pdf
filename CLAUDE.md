# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`autosar-pdf2txt` is a Python package for extracting text and structured metadata from PDF files, specifically designed for AUTOSAR template specification documents.

**Version**: 0.1.0 (2026-01-16)

**Key Features**:
- Extract AUTOSAR package and class hierarchies from PDF specification documents
- Multi-backend PDF reading (pdfplumber, fitz, pypdf)
- Parse asterisk-based hierarchy format to nested structures
- Write hierarchies to markdown with duplicate prevention
- 99% test coverage (107 tests)

**Entry Point**:
- `autosar-extract` - AUTOSAR-specific package and class hierarchy extraction CLI tool

## Documentation

- **Requirements**: `docs/req/autosar_extract.md` - Complete functional and non-functional requirements
- **Test Cases**: `docs/req/test_cases.md` - All 107 test cases with detailed steps
- **Models Reference**: `docs/models/autosar_models.md` - AUTOSAR package/class reference
- **Visual Reference**: `examples/pdf/Screenshot 2026-01-13 064408.png` - Hierarchy structure example

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
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src/autosar_pdf2txt --cov-report=term-missing

# Run specific module
pytest tests/models/ -v
pytest tests/parser/ -v
pytest tests/writer/ -v
```

### Test Coverage
- **Models**: 100% (32 tests)
- **Parser**: 100% (53 tests)
- **Writer**: 97% (22 tests)
- **Overall**: 99% (107 tests)

## Architecture

### Package Structure

```
src/autosar_pdf2txt/
├── __init__.py             # Version 0.1.0, exports AutosarClass, AutosarPackage
├── cli/                    # Command-line interfaces
│   └── autosar_cli.py      # AUTOSAR extraction tool (entry point: autosar-extract)
├── models/                 # Data models for AUTOSAR packages/classes
│   ├── __init__.py         # Exports AutosarClass, AutosarPackage
│   └── autosar_models.py   # AutosarClass and AutosarPackage dataclasses (167 lines)
├── parser/                 # PDF parsing and extraction logic
│   ├── __init__.py         # Exports PDFReader, HierarchyParser, AutosarParser
│   ├── pdf_reader.py       # PDF text extraction with backend abstraction (202 lines)
│   ├── hierarchy_parser.py # Parse asterisk-based hierarchy to nested packages (178 lines)
│   └── autosar_parser.py   # Integration of PDF reader and hierarchy parser (110 lines)
└── writer/                 # Markdown output writer with duplicate removal
    ├── __init__.py         # Exports MarkdownWriter, write_markdown
    └── markdown_writer.py  # Write packages to markdown format (134 lines)

tests/                      # Matching src/ structure
├── models/
│   └── test_autosar_models.py  # 32 tests
├── parser/
│   ├── test_pdf_reader.py      # 20 tests
│   ├── test_hierarchy_parser.py # 23 tests
│   └── test_autosar_parser.py   # 10 tests
└── writer/
    └── test_markdown_writer.py  # 22 tests
```

## Data Models

### AutosarClass (`models/autosar_models.py`)

**Fields**:
- `name: str` - Class name (validated: non-empty, non-whitespace)
- `is_abstract: bool` - Whether the class is abstract

**Methods**:
- `__str__()` - Returns "ClassName" or "ClassName (abstract)"
- `__repr__()` - Returns detailed representation
- `__post_init__()` - Validates name is not empty/whitespace

**Example**:
```python
from autosar_pdf2txt import AutosarClass

cls = AutosarClass(name="RunnableEntity", is_abstract=False)
print(cls)  # "RunnableEntity"

abstract_cls = AutosarClass(name="AbstractBehavior", is_abstract=True)
print(abstract_cls)  # "AbstractBehavior (abstract)"
```

### AutosarPackage (`models/autosar_models.py`)

**Fields**:
- `name: str` - Package name (validated: non-empty, non-whitespace)
- `classes: List[AutosarClass]` - List of classes in this package
- `subpackages: List[AutosarPackage]` - List of subpackages (nested packages)

**Methods**:
- `add_class(cls: AutosarClass)` - Add a class (raises ValueError if duplicate name)
- `add_subpackage(pkg: AutosarPackage)` - Add a subpackage (raises ValueError if duplicate name)
- `get_class(name: str) -> AutosarClass | None` - Find a class by name
- `get_subpackage(name: str) -> AutosarPackage | None` - Find a subpackage by name
- `has_class(name: str) -> bool` - Check if class exists
- `has_subpackage(name: str) -> bool` - Check if subpackage exists
- `__str__()` - Returns summary with class/subpackage counts
- `__repr__()` - Returns detailed representation

**Example**:
```python
from autosar_pdf2txt import AutosarPackage, AutosarClass

# Create package with classes
pkg = AutosarPackage(name="BswBehavior")
pkg.add_class(AutosarClass(name="BswInternalBehavior", is_abstract=False))
pkg.add_class(AutosarClass(name="ExecutableEntity", is_abstract=True))

# Create nested structure
root = AutosarPackage(name="AUTOSARTemplates")
root.add_subpackage(pkg)
```

## Parser Modules

### PDFReader (`parser/pdf_reader.py`)

Multi-backend PDF text extraction with automatic backend selection.

**Backends** (priority order):
1. `pdfplumber` - Preferred, highest quality
2. `fitz` (PyMuPDF) - Alternative
3. `pypdf` - Fallback option

**Class API**:
```python
from autosar_pdf2txt.parser import PDFReader

reader = PDFReader(backend="auto")  # or "pdfplumber", "fitz", "pypdf"
text = reader.read_text("path/to/file.pdf")
```

**Functional API**:
```python
from autosar_pdf2txt.parser import read_pdf

text = read_pdf("path/to/file.pdf", backend="auto")
```

**Features**:
- Automatic backend selection when `backend="auto"`
- Graceful fallback to next available backend
- Proper error handling with informative messages
- Page separation with form feeds

### HierarchyParser (`parser/hierarchy_parser.py`)

Parses asterisk-based hierarchy format to nested package structures.

**Input Format**:
```
* PackageName
  * SubPackageName
      * ClassName
      * AbstractClass (abstract)
```

**Rules**:
- Lines start with `*` followed by content
- Indentation (leading spaces) determines nesting level: 2 spaces = 1 level
- Items with children (next line has greater indentation) are packages
- Items without children are classes
- `(abstract)` suffix indicates abstract class

**Class API**:
```python
from autosar_pdf2xt.parser import HierarchyParser

parser = HierarchyParser(text)
packages = parser.parse()
```

**Functional API**:
```python
from autosar_pdf2txt.parser import parse_hierarchy

packages = parse_hierarchy(text)
```

**Features**:
- Handles arbitrarily deep nesting
- Detects package vs class by looking at next line indentation
- Extracts and removes `(abstract)` marker
- Ignores blank lines and invalid lines
- Prevents duplicate classes within same package

### AutosarParser (`parser/autosar_parser.py`)

Integration layer combining PDFReader and HierarchyParser.

**Class API**:
```python
from autosar_pdf2txt.parser import AutosarParser

parser = AutosarParser(pdf_backend="auto")
packages = parser.parse_pdf("path/to/file.pdf")
```

**Functional APIs**:
```python
from autosar_pdf2txt.parser import parse_autosar_pdf, extract_pdf_text

# Parse to packages
packages = parse_autosar_pdf("path/to/file.pdf", pdf_backend="auto")

# Extract raw text only
text = extract_pdf_text("path/to/file.pdf", pdf_backend="auto")
```

**Workflow**:
1. Read PDF file using PDFReader
2. Extract text content
3. Parse text using HierarchyParser to extract package/class hierarchy
4. Return list of AutosarPackage objects

## Writer Module

### MarkdownWriter (`writer/markdown_writer.py`)

Write AUTOSAR packages and classes to markdown format with asterisk-based indentation.

**Output Format**:
```
* PackageName
  * SubPackageName
      * ClassName
      * AbstractClass (abstract)
```

**Indentation Rules**:
- Level 0 (top-level package): 0 spaces before `*`
- Level N (subpackage): N * 2 spaces before `*`
- Level N+1 (class): (N + 2) * 2 spaces before `*`

**Class API**:
```python
from autosar_pdf2txt.writer import MarkdownWriter

writer = MarkdownWriter(deduplicate=True)
markdown = writer.write_packages(packages)

# Multiple calls maintain deduplication state
markdown2 = writer.write_packages(more_packages)
```

**Functional API**:
```python
from autosar_pdf2txt.writer import write_markdown

markdown = write_markdown(packages, deduplicate=True)
```

**Features**:
- Proper indentation for nested structures (2 spaces per level)
- Marks abstract classes with `(abstract)` suffix
- Duplicate prevention based on full path tuple:
  - Example: `("Root", "Sub", "Class")` vs `("Root", "Other", "Class")`
- Deduplication persists across multiple `write_packages()` calls when `deduplicate=True`
- Can disable deduplication with `deduplicate=False`

**Duplicate Detection**:
- Tracks seen packages by full path: `tuple(parent_path + [package_name])`
- Tracks seen classes by full path: `tuple(parent_path + [class_name])`
- Same class name in different packages: both written (different paths)
- Same package path on second call: skipped entirely

## Code Conventions

### Style Guidelines
- **Type hints** required on all function/method parameters and returns
- **Google-style docstrings** with Args/Returns/Raises sections
- **Import order**: standard library → third-party → local
- **Naming**:
  - Functions: snake_case
  - Classes: PascalCase
  - Constants: UPPER_CASE
- **Error handling**:
  - `ValueError` for invalid arguments
  - `FileNotFoundError` for missing files
  - try-except for I/O operations
- **Comments**: English in all code (including tests)
- **Two-tier API**: Always provide both functional and class-based implementations

### Dataclass Guidelines
- Use `@dataclass` decorator for models
- Use `field(default_factory=list)` for mutable defaults
- Implement validation in `__post_init__` method
- Provide both `__str__` and `__repr__` methods

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

**Validation**:
```python
if not name or name.strip() == "":
    raise ValueError("Name cannot be empty")
```

**Backend Selection**:
```python
if self.backend == "pdfplumber":
    return self._read_with_pdfplumber(path)
elif self.backend == "fitz":
    return self._read_with_fitz(path)
elif self.backend == "pypdf":
    return self._read_with_pypdf(path)
else:
    raise ValueError(f"Unknown backend: {self.backend}")
```

### Testing Guidelines

**Test Structure**:
- One test file per source file (matching src/ structure)
- Test classes grouped by functionality
- Test methods named `test_<functionality>_<scenario>`
- English docstrings for all tests

**Test Coverage**:
- Target 100% coverage for models and parser
- Target ≥95% coverage for writer
- Cover normal operations, edge cases, and error conditions

**Test Categories**:
1. **Initialization tests** - Constructor with various parameters
2. **Success path tests** - Normal operations
3. **Error condition tests** - Invalid inputs, missing files
4. **Edge case tests** - Empty inputs, boundary conditions
5. **Integration tests** - End-to-end workflows

**Example Test**:
```python
def test_parse_package_with_class(self) -> None:
    """Test parsing package with class."""
    text = """* Package
    * Class"""
    parser = HierarchyParser(text)
    packages = parser._parse_hierarchy()
    assert len(packages) == 1
    assert packages[0].name == "Package"
    assert len(packages[0].classes) == 1
    assert packages[0].classes[0].name == "Class"
```

### CLI Function Organization

CLI functions should be broken into smaller methods (≤ 50 lines each):
- `parse_arguments()` - Argument parsing logic
- `process_files()` - File processing orchestration
- `write_output()` - Output handling

## Output Format Specification

### Markdown Hierarchy Format

```
* AUTOSARTemplates
  * BswModuleTemplate
    * BswBehavior
        * BswInternalBehavior
        * ExecutableEntity (abstract)
        * BswModuleEntity (abstract)
```

### Indentation Calculation

| Item Type | Level | Spaces | Example |
|-----------|-------|--------|---------|
| Top-level package | 0 | 0 | `* Package` |
| Subpackage (level 1) | 1 | 2 | `  * SubPackage` |
| Subpackage (level 2) | 2 | 4 | `    * NestedPackage` |
| Class (in level 0) | 2 | 4 | `    * Class` |
| Class (in level 1) | 3 | 6 | `      * Class` |
| Class (in level 2) | 4 | 8 | `        * Class` |

Formula: `indent_spaces = (level + (1 if package else 2)) * 2`

## Example Files

Example PDFs are available in `examples/pdf/` for testing:
- `AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf`
- `AUTOSAR_CP_TPS_SoftwareComponentTemplate.pdf`

## Version History

| Version | Date       | Description                                                                     |
| ------- | ---------- | ------------------------------------------------------------------------------- |
| v0.1.0  | 2026-01-16 | Initial implementation with PDF reading, hierarchy parsing, and markdown output |
