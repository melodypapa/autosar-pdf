# Test-Driven Development (TDD) Rules

## Core TDD Cycle

Follow the Red-Green-Refactor cycle for all development:

1. **Red**: Write a failing test that captures the desired behavior
2. **Green**: Write the minimum code to make the test pass
3. **Refactor**: Improve the code while keeping tests passing

## Application to AUTOSAR PDF Project

### For New Features

1. **Write Test First**
   - Create or update integration test in `docs/test_cases/integration_tests.md`
   - Implement the test in `tests/integration/test_pdf_integration.py` or appropriate test file
   - Verify the test fails (RED)

2. **Implement Feature**
   - Write minimum code in `src/autosar_pdf2txt/` to make test pass
   - Run test to verify it passes (GREEN)

3. **Refactor**
   - Improve code quality, structure, and naming
   - Ensure all tests still pass

### For Bug Fixes

1. **Write Failing Test**
   - Create a test that reproduces the bug
   - Verify test fails (RED)

2. **Fix Bug**
   - Write minimum code to fix the issue
   - Verify test passes (GREEN)

3. **Refactor**
   - Improve the fix if needed
   - Ensure no regressions

## Quality Gates

Before committing any changes, ensure:

1. **All Tests Pass**
   ```bash
   python3 -m pytest tests/ -v
   ```

2. **Code Quality Checks Pass**
   ```bash
   ruff check src/ tests/
   mypy src/autosar_pdf2txt/
   ```

3. **Coverage Remains High**
   - Maintain ≥95% coverage
   - Review coverage report in `scripts/report/coverage.md`

## Integration with Test Update Rules

The TDD cycle works together with the test update rules:

1. **Update Requirements** (Test Update Rule)
2. **Write Failing Test** (TDD - Red)
3. **Implement Feature** (TDD - Green)
4. **Refactor** (TDD - Refactor)
5. **Verify All Tests Pass** (Quality Gates)

## Benefits

- **Confidence**: Tests ensure code works as expected
- **Documentation**: Tests serve as executable documentation
- **Refactoring Safety**: Tests prevent regressions during refactoring
- **Design Focus**: Writing tests first leads to better design
- **Faster Development**: Catch bugs early, reduce debugging time