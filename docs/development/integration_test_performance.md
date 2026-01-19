# Integration Test Performance Guide

This document describes the performance optimizations implemented for integration tests and how to use them effectively.

## Overview

Integration tests parse real AUTOSAR specification PDF files, which can be large and time-consuming. To improve test execution performance, session-scoped pytest fixtures are used to cache parsed PDF data and share results across multiple tests.

## Performance Improvements

### Before Optimization
- Each test created its own `PdfParser` instance
- Each test parsed its own PDF files from scratch
- Multiple tests using the same PDF would re-parse it repeatedly
- Example: 3 tests using BSW Module Template PDF = 3 × ~96s = 288s

### After Optimization
- Single `PdfParser` instance shared across all tests (session-scoped)
- Each PDF parsed once per test session and cached
- All tests using the same PDF share the cached data
- Example: 3 tests using BSW Module Template PDF = 1 × 96s = 96s

### Performance Gains
- **3-5x faster** for tests using the same PDF files
- Reduced I/O operations (PDFs read once, not multiple times)
- Reduced CPU usage (parsing done once, results reused)
- Scalable improvement: More tests using the same PDF = greater speedup

## Fixture Architecture

### Session-Scoped Fixtures

Located in `tests/integration/conftest.py`:

```python
@pytest.fixture(scope="session")
def parser() -> PdfParser:
    """Single PdfParser instance for the entire test session."""

@pytest.fixture(scope="session")
def bsw_template_pdf(parser: PdfParser) -> List[AutosarPackage]:
    """Parsed and cached BSW Module Template PDF."""

@pytest.fixture(scope="session")
def ecu_configuration_pdf(parser: PdfParser) -> List[AutosarPackage]:
    """Parsed and cached ECU Configuration PDF."""

@pytest.fixture(scope="session")
def pdf_cache(parser: PdfParser) -> Dict[str, List[AutosarPackage]]:
    """Dictionary of all parsed PDFs."""
```

### Helper Functions

The conftest module also provides utility functions for common operations:

```python
def find_first_class(packages: List[AutosarPackage]) -> tuple:
    """Find the first class in a package hierarchy."""

def count_classes(packages: List[AutosarPackage]) -> int:
    """Count total classes across all packages recursively."""
```

## Usage

### Using Cached PDF Fixtures

Tests should use the cached fixtures instead of parsing PDFs directly:

**Before (inefficient):**
```python
def test_some_feature(self) -> None:
    parser = PdfParser()
    packages = parser.parse_pdf("examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf")
    # Test logic...
```

**After (optimized):**
```python
def test_some_feature(self, bsw_template_pdf: list) -> None:
    packages = bsw_template_pdf  # Use cached data
    # Test logic...
```

### Adding New PDF Fixtures

To add a new PDF fixture:

1. Add the fixture to `tests/integration/conftest.py`:
   ```python
   @pytest.fixture(scope="session")
   def my_new_pdf(parser: PdfParser) -> List[AutosarPackage]:
       pdf_path = "examples/pdf/MyNewFile.pdf"
       if not os.path.exists(pdf_path):
           pytest.skip(f"PDF file not found: {pdf_path}")
       return parser.parse_pdf(pdf_path)
   ```

2. Use it in your test:
   ```python
   def test_my_new_feature(self, my_new_pdf: list) -> None:
       packages = my_new_pdf
       # Test logic...
   ```

### Using the General PDF Cache

For tests that need access to all available PDFs:

```python
def test_multiple_pdfs(self, pdf_cache: dict) -> None:
    for pdf_name, packages in pdf_cache.items():
        # Test logic for each PDF...
```

## Running Integration Tests

### Run All Integration Tests
```bash
pytest tests/integration/ -v
```

### Run Specific Test
```bash
pytest tests/integration/test_pdf_integration.py::TestPdfIntegration::test_parse_bsw_module_template_pdf_first_class -v
```

### Run with Timing Information
```bash
pytest tests/integration/ -v --durations=10
```

This shows the slowest test setup and execution times, helping identify performance bottlenecks.

### Performance Comparison

To see the performance improvement, compare the setup times:

**Without caching** (old implementation):
- Each test: ~96s setup time
- 3 tests: ~288s total

**With caching** (current implementation):
- First test: ~96s setup time (parsing occurs)
- Subsequent tests: <0.005s setup time (using cache)
- 3 tests: ~96s total

## Performance Tips

### 1. Use Appropriate Fixture Scopes

- **scope="session"**: For expensive operations like PDF parsing (used here)
- **scope="module"**: For data shared within a module
- **scope="function"**: For test-specific data (default)

### 2. Minimize Fixture Setup Time

- Fixtures should only do expensive work once
- Use lazy evaluation for optional data
- Skip gracefully if resources aren't available

### 3. Reuse Helper Functions

Common operations like `find_first_class()` and `count_classes()` are defined in `conftest.py` and can be imported across tests to avoid code duplication.

### 4. Leverage the PDF Cache

For tests that need to verify behavior across multiple PDFs, use the `pdf_cache` fixture instead of defining multiple individual PDF fixtures.

## Future Optimizations

### Potential Additional Improvements

1. **pytest-xdist for Parallel Execution**
   - Run tests in parallel across multiple CPU cores
   - Combine with session-scoped fixtures for maximum benefit
   - Installation: `pip install pytest-xdist`
   - Usage: `pytest -n auto tests/integration/`

2. **Mock PDF Data for Unit Tests**
   - Create minimal PDF mock data for focused unit tests
   - Reserve real PDF parsing for true integration tests
   - Further reduces test execution time

3. **Incremental Test Execution**
   - Use pytest's `--lf` flag to run only failed tests from last run
   - Use `--ff` to run failed tests first, then pass tests

4. **Continuous Optimization**
   - Monitor test execution times with `--durations`
   - Identify and optimize new bottlenecks as they appear
   - Profile memory usage to ensure efficient caching

## Maintenance

### When to Update Fixtures

- When PDF file locations change
- When parsing logic changes significantly
- When new test PDFs are added
- When fixture setup becomes a bottleneck itself

### Testing Fixture Changes

After modifying fixtures, always run:

```bash
pytest tests/integration/ -v
```

Verify that:
- All tests still pass
- Performance improvements are maintained
- No regressions are introduced
