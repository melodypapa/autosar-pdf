# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`autosar-pdf2txt` is a Python package for extracting AUTOSAR model hierarchies from PDF files and converting them to markdown format. The project uses a dataclass-based model for representing AUTOSAR packages and classes, with a markdown writer for output.

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
└── writer/
    ├── __init__.py
    └── markdown_writer.py   # MarkdownWriter class
```

### Core Components

**Models (`models/autosar_models.py`)**
- `AutosarClass`: Dataclass representing an AUTOSAR class with name and abstract flag
- `AutosarPackage`: Dataclass for hierarchical package structures containing classes and subpackages
- Validation: Both classes validate non-empty names in `__post_init__`
- Methods: `add_class()`, `add_subpackage()`, `get_class()`, `get_subpackage()`, `has_class()`, `has_subpackage()`

**Writer (`writer/markdown_writer.py`)**
- `MarkdownWriter`: Class-based API for writing package hierarchies to markdown
  - Deduplication: Tracks seen packages/classes via tuple paths to skip duplicates
  - Output format: Asterisk-based hierarchy with indentation (2 spaces per level)
  - Classes indented 2 levels deeper than their parent package

## Code Style Conventions

### Type Hints
- All functions and methods must have type hints for parameters and return values
- Use `|` for union types (e.g., `str | None`) - Python 3.10+ syntax
- Use `List[T]` from typing for lists (not built-in `list[T]`)

### Docstrings
- Google-style docstrings with Args/Returns/Raises sections
- Class docstrings include Attributes section
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
  - Deduplication behavior
  - Nested hierarchies
  - Empty inputs
  - Abstract vs concrete classes

## Key Implementation Details

### Markdown Indentation Rules
- Packages: indent = `level * 2` spaces
- Classes: indent = `(level + 2) * 2` spaces (2 levels deeper than parent package)
- Format: `* <name>` or `* <name> (abstract)`

### Deduplication Logic
- Tracks full path tuples: `(parent1, parent2, ..., item_name)`
- Packages tracked in `_seen_packages: set[tuple[str, ...]]`
- Classes tracked in `_seen_classes: set[tuple[str, ...]]`
- Deduplication prevents duplicate output when same hierarchy appears multiple times
- Can be disabled via `deduplicate=False` parameter

### Model Validation
- Empty/whitespace names raise `ValueError`
- Duplicate classes in package raise `ValueError`
- Duplicate subpackages in package raise `ValueError`
