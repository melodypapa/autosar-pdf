# Test Update Rules

## Rule: Always Update Requirements and Test Cases Before Implementation

When updating tests (both integration and unit tests), follow this order:

### For Integration Tests

1. **Update Requirements Document First**
   - Modify the test case specification in `docs/test_cases/integration_tests.md`
   - Include all expected behaviors, verification steps, and expected results
   - Document any new requirements or changes to existing requirements

2. **Update Test Implementation Second**
   - Implement the test in `tests/integration/test_pdf_integration.py`
   - Ensure the test matches the specification in the requirements document
   - Verify all assertions match the expected results

3. **Verification**
   - Run the test to ensure it passes
   - Run all tests to ensure no regressions
   - Update coverage reports if needed

### For Unit Tests

1. **Update Requirements Document First**
   - Identify the requirement ID in `docs/requirements/requirements.md`
   - Document the test case in `docs/test_cases/unit_tests.md` with requirement ID
   - Include expected behaviors, verification steps, and expected results

2. **Update Test Implementation Second**
   - Implement the test in the appropriate test file (e.g., `tests/models/test_autosar_models.py`)
   - Ensure the test matches the specification in the test case document
   - Add requirement ID to test docstring for traceability

3. **Verification**
   - Run the test to ensure it passes
   - Run all tests to ensure no regressions
   - Update coverage reports if needed

## Example Flow

**Integration Test:**
1. User requests: "Update test to verify ARElement subclasses"
2. First: Update `docs/test_cases/integration_tests.md` with the test specification
3. Second: Update `tests/integration/test_pdf_integration.py` with the test implementation
4. Third: Run tests to verify

**Unit Test:**
1. User requests: "Add test for AutosarClass duplicate prevention"
2. First: Update `docs/test_cases/unit_tests.md` with test specification and requirement ID (e.g., SWUT_MODEL_00001)
3. Second: Update `tests/models/test_autosar_models.py` with the test implementation
4. Third: Run tests to verify

## Why This Order Matters

- **Clarity**: The requirements document serves as the single source of truth
- **Traceability**: Test cases are explicitly linked to requirements via requirement IDs
- **Maintainability**: Future developers can understand what the test should do without reading code
- **Documentation**: The test case documents are part of the project documentation
- **Coverage**: Ensures all requirements have corresponding test cases