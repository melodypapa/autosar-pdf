# autosar-pdf2txt - Agent Guidelines

## Essential Commands

### Building & Installation
```bash
pip install -e .
pip install -r requirements.txt
```

### Testing
```bash
pytest tests/                                    # Run all tests
pytest tests/test_converter.py                 # Single test file
pytest tests/test_converter.py::test_func      # Specific test function
pytest tests/ -v                                # Verbose output
pytest tests/test_converter.py::test_func --cov=autosar_pdf2txt  # With coverage
cd tests && python report.py                   # Full coverage report
```

### Linting & Type Checking
```bash
ruff check src/autosar_pdf2txt/ tests/                # Lint
ruff check --fix src/autosar_pdf2txt/ tests/          # Auto-fix
mypy src/autosar_pdf2txt/                              # Type check
ruff format src/autosar_pdf2txt/                       # Format
ruff check src/autosar_pdf2txt/ && ruff format src/autosar_pdf2txt/    # Lint + format
```

## Code Style Guidelines

### Imports
- Standard library → third-party → local imports with blank line separators
- For local imports within package: use relative imports (`from ..core import ...`)
- For external usage: use absolute imports (`from autosar_pdf2txt.core import ...`)
- Import only what's needed; avoid `from module import *`

### Formatting
- 4 spaces indentation (no tabs)
- Max line length: 100-120 characters
- Double quotes for strings, single only when string contains double quotes
- Use comments sparingly; prefer self-documenting code
- Module docstrings describe purpose at top of file

### Type Hints
- Use type hints for all params/returns
- Import from `typing`: `List`, `Dict`, `Union`, `Optional`, `Any`, `Tuple`
- Prefer explicit types over `Any`; use `Optional[Type]` for nullable

```python
def convert_pdf_to_text(
    pdf_path: str,
    method: str = "pypdf2",
    skip_header_lines: int = 0
) -> str:
    """Convert PDF to text."""

def extract_tables(
    pdf_path: str,
    page_range: Optional[List[int]] = None
) -> List[dict]:
    """Extract tables with optional page filter."""
```

### Naming Conventions
- Functions/Variables: snake_case (`convert_pdf_to_text`)
- Classes: PascalCase (`PdfConverter`, `TableExtractor`)
- Constants: UPPER_CASE (`MAX_PAGE_COUNT`)
- Private methods: leading underscore (`_helper`)
- Booleans: prefix `is_`, `has_`, `should_`

### Error Handling
- `ValueError` for invalid arguments/unsupported methods
- `try-except` for file operations and PDF processing
- CLI modules: use `sys.exit(1)` on error with descriptive messages
- Validate inputs early; catch specific exceptions

```python
if method not in ["pypdf2", "pdfplumber"]:
    raise ValueError(f"Unsupported: {method}. Use 'pypdf2' or 'pdfplumber'.")

try:
    with open(pdf_path, 'rb') as file:
        ...
except FileNotFoundError:
    print(f"Error: File {pdf_path} not found")
    sys.exit(1)
```

### Docstrings
- Google-style with `Args:`, `Returns:`, `Raises:` sections
- Module-level docstrings describe purpose
- All exported functions must have docstrings

### File Structure
- `src/autosar_pdf2txt/__init__.py`: Package exports, `__all__` for public API
- `src/autosar_pdf2txt/cli/`: Command-line interfaces (`pdf2txt_cli.py`, `autosar_cli.py`)
- `src/autosar_pdf2txt/core/`: Core conversion (`converter.py`, `cleaner.py`, `markdown.py`, `table.py`, `integration.py`)
- `src/autosar_pdf2txt/extractor/`: AUTOSAR parsing (`parser.py`, `hierarchy.py`, `writer.py`, `integration.py`, `models.py`)
- `src/autosar_pdf2txt/utils.py`: General utilities (validation, formatting)
- `tests/`: pytest files named `test_*.py`

### Testing
- Use pytest; files: `test_*.py`, functions: `test_*`
- **Use Chinese docstrings for tests** (project convention)
- Use `assert callable(func)` when no sample files available

```python
def test_convert_pdf_to_text():
    """测试 PDF 转换功能"""
    assert callable(convert_pdf_to_text)
```

### Python Version
- Support Python 3.7+
- Use type hints; avoid Python 3.8+ features unless necessary

## Additional Notes
- Package name: `autosar_pdf2txt` (import: `import autosar_pdf2txt`)
- PDF backends: pypdf (default) and pdfplumber (better for tables)
- PyMuPDF (fitz) optional dependency for `get_pdf_info()` function
- Page ranges are 0-indexed internally
- CLI commands: `pdf2txt` and `autosar-extract`
- When adding features, implement both CLI and Python API paths
- Test both CLI and API paths
