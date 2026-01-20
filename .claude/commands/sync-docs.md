# Sync Documentation

Synchronize requirements, test cases, and source code to ensure consistency across the codebase.

## Usage

```
/sync-docs
```

## What This Command Does

This command analyzes the source code implementation and updates the requirements and test case documentation to match, ensuring traceability and accuracy.

## Steps

### 1. Analyze Source Code
- Scan source files to identify:
  - Class attributes and their types
  - Method signatures
  - Constructor parameters
  - Inheritance relationships
- Extract actual implementation details

### 2. Compare with Documentation
- Read current requirements (`docs/requirements/requirements.md`)
- Read current unit test cases (`docs/test_cases/unit_tests.md`)
- Read current integration test cases (`docs/test_cases/integration_tests.md`)
- Identify discrepancies:
  - Missing or incorrect attributes in requirements
  - Outdated parameter lists
  - Incorrect inheritance hierarchies
  - Missing or stale unit test case descriptions
  - Missing or stale integration test case descriptions

### 3. Update Requirements
- Update requirement descriptions to match implementation
- Add missing attributes to requirement specifications
- Remove deprecated features from requirements
- Update attribute types and default values
- Ensure maturity levels match implementation status

### 4. Update Unit Test Cases
- Update test case descriptions to match current implementation
- Add missing test steps for new attributes
- Remove test steps for deprecated features
- Update expected results to match actual behavior
- Ensure test cases reference correct requirement IDs

### 5. Update Integration Test Cases
- Update integration test scenarios to match current implementation
- Add missing integration test steps for new features
- Remove test steps for deprecated features
- Update expected results to match actual behavior
- Ensure integration test cases reference correct requirement IDs
- Verify end-to-end workflows are documented correctly

### 6. Verify Synchronization
- Run all tests to ensure documentation is accurate
- Run type checking to verify signatures match
- Check for orphaned requirements or tests
- Generate synchronization report

## Common Synchronization Tasks

### Attribute Changes
When attributes are moved/added/removed:
1. Update affected requirement specifications
2. Update unit test case steps that verify attributes
3. Update integration test scenarios that test attributes
4. Update examples in documentation
5. Update `__init__` signatures if needed

### Inheritance Changes
When inheritance hierarchies change:
1. Update base class requirements
2. Update derived class requirements
3. Update unit test inheritance verification steps
4. Update integration test scenarios that test inheritance
5. Update docstrings that reference inheritance

### Type Changes
When attribute types change:
1. Update requirement type specifications
2. Update unit test type checks
3. Update integration test type checks
4. Update examples with correct types
5. Update type hints in source if missing

### Integration Workflow Changes
When end-to-end workflows change:
1. Update integration test scenarios
2. Update test data and fixtures
3. Update expected results
4. Verify workflow documentation accuracy

## Files Modified

- `docs/requirements/requirements.md` - Requirements specifications
- `docs/test_cases/unit_tests.md` - Unit test case documentation
- `docs/test_cases/integration_tests.md` - Integration test case documentation

## Files Analyzed (Read-Only)

- `src/autosar_pdf2txt/models/*.py` - Model implementations
- `src/autosar_pdf2txt/parser/*.py` - Parser implementations
- `src/autosar_pdf2txt/writer/*.py` - Writer implementations
- `src/autosar_pdf2txt/cli/*.py` - CLI implementations
- `tests/**/*.py` - Test implementations

## Verification

After synchronization, run:
```bash
pytest tests/ --cache-clear
ruff check src/ tests/
mypy src/autosar_pdf2txt/
```

All checks must pass for synchronization to be complete.

## Examples

### After Refactoring
```
User: /sync-docs
System: Analyzing source code...
       Found 3 discrepancies in requirements
       Found 5 discrepancies in unit test cases
       Found 2 discrepancies in integration test cases
       Updating SWR_MODEL_00018...
       Updating SWUT_MODEL_00034...
       Updating SWIT_PARSER_00012...
       Verification: All tests pass ✅
       Synchronization complete
```

### After Adding New Attribute
```
User: /sync-docs
System: Detected new attribute 'package' in AbstractAutosarBase
       Updating requirements...
       Updating unit test cases...
       Updating integration test cases...
       Complete: 2 requirements updated, 3 unit tests updated, 1 integration test updated
```

### After Workflow Changes
```
User: /sync-docs
System: Detected changes in PDF parsing workflow
       Updating integration test scenarios...
       Updating end-to-end test steps...
       Complete: 2 integration test scenarios updated
```

## Notes

- Always run quality checks after synchronization
- Document what changed and why
- If in doubt, ask user before making changes
- Never change stable requirement IDs
- Keep maturity levels accurate

## Related Commands

- `/req` - Manage individual requirements
- `/test` - Run tests and coverage
- `/quality` - Run quality checks
