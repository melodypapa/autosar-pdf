# Scripts

This directory contains utility scripts for the autosar-pdf2txt project.

## run_tests.py

Convenient test runner script for running tests and generating coverage reports.

### Features

- Run all tests with coverage
- Run only integration tests with coverage
- Run only unit tests with coverage
- Automatically generates markdown coverage report after each test run

### Usage

```bash
# Run all tests (generates coverage report automatically)
python scripts/run_tests.py --all

# Run only integration tests
python scripts/run_tests.py --integration

# Run only unit tests
python scripts/run_tests.py --unit
```

**Note**: Coverage reports are automatically generated after tests complete and saved to `scripts/report/coverage.md`.

### Output Examples

#### All Tests (Coverage Report Generated Automatically)

```bash
$ python scripts/run_tests.py --all

======================================================================
Running: python -m pytest tests/ -v --cov=autosar_pdf2txt --cov-report=term --cov-report=json:cov_report.json
======================================================================

============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.0.2, pluggy-1.6.0
...

======================= 100 passed in 398.49s (0:06:38) ========================

======================================================================
Generating coverage report...
======================================================================

Coverage report saved to: scripts/report/coverage.md
```

#### Coverage Report

Coverage reports are automatically saved to `scripts/report/coverage.md` after each test run.

Example report content:
======================================================================
COVERAGE REPORT - MARKDOWN FORMAT
======================================================================

## Overall Coverage: 93.8%

**Total Statements**: 290

**Statements Covered**: 272

**Statements Missing**: 18

## All Source Files Coverage

| Source File                    | Statements | Covered | Missing | Coverage |
| ------------------------------ | ---------- | ------- | ------- | -------- |
| OK `__init__.py`               | 5          | 5       | 0       | 100.0%   |
| OK `cli/__init__.py`           | 2          | 2       | 0       | 100.0%   |
| TODO `cli/autosar_cli.py`      | 64         | 54      | 10      | 84.4%    |
| OK `models/__init__.py`        | 2          | 2       | 0       | 100.0%   |
| OK `models/autosar_models.py`  | 76         | 76      | 0       | 100.0%   |
| OK `parser/__init__.py`        | 2          | 2       | 0       | 100.0%   |
| TODO `parser/pdf_parser.py`    | 116        | 108     | 8       | 93.1%    |
| OK `writer/__init__.py`        | 2          | 2       | 0       | 100.0%   |
| OK `writer/markdown_writer.py` | 21         | 21      | 0       | 100.0%   |

## Files with Less Than 100% Coverage

| Source File            | Coverage        | Missing Statements |
| ---------------------- | --------------- | ------------------ |
| `cli/autosar_cli.py`   | 84.4% (54/64)   | 10 stmts (15.6%)   |
| `parser/pdf_parser.py` | 93.1% (108/116) | 8 stmts (6.9%)     |

======================================================================
```

The report is automatically saved in Markdown format with UTF-8 encoding, perfect for:
- Including in project documentation
- Attaching to pull requests
- Generating historical coverage reports
- Integration with CI/CD pipelines

### Coverage Report Location

**Default behavior**: Coverage reports are automatically saved to:
- **Location**: `scripts/report/coverage.md`
- The `report` directory is created automatically if it doesn't exist
- Report is generated after successful test completion

### Requirements

- pytest
- pytest-cov

### Exit Codes

- 0: Success
- 1: Error (test failures, coverage issues, or invalid arguments)
