# Test-Driven Development (TDD) Rules

## Core TDD Cycle

Follow the Red-Green-Refactor cycle for all development:

1. **Red**: Write a failing test that captures the desired behavior
2. **Green**: Write the minimum code to make the test pass
3. **Refactor**: Improve the code while keeping tests passing

## Test Type Selection Strategy

### Unit Tests as First Priority

**Rule**: TDD rules should use unit tests as the first priority solution to perform the TDD cycle.

**Rationale**:
- Unit tests are faster to write and execute
- Unit tests provide fine-grained feedback on specific functionality
- Unit tests are easier to debug when they fail
- Unit tests can be written without external dependencies (PDF files)

**When to Use Unit Tests**:
- Implementing new parser logic (pattern recognition, validation, state management)
- Testing model class behavior (validation, string representation, relationships)
- Testing writer functionality (markdown generation, formatting)
- Testing CLI argument parsing and validation
- Testing edge cases and error conditions

**When to Use Integration Tests**:
- Verifying end-to-end functionality with real PDF files
- Testing complete workflow from PDF parsing to markdown output
- Validating complex interactions between multiple components
- Ensuring the system works with actual AUTOSAR specification documents

### Integration Test Requirement

**Rule**: Integration tests are always based on the actual PDF file.

**Requirements**:
- Integration tests MUST use real PDF files from `examples/pdf/**` directory
- Integration tests MUST NOT mock or simulate PDF parsing
- Tests that do not use real PDF files from `examples/pdf/**` MUST NOT be classified as integration tests
- Integration tests verify the complete system works with actual AUTOSAR specification documents
- Integration tests are used for final validation and regression testing

**Purpose**:
- Ensure the system works correctly with real-world AUTOSAR PDFs
- Validate that parsing patterns match actual PDF formatting
- Catch issues that only appear with real PDF files (spacing, formatting, encoding)
- Provide confidence that the system works with official AUTOSAR specifications

**Classification Rule**:
- If a test case uses a real PDF file from `examples/pdf/**`, it is an **integration test**
- If a test case does NOT use a real PDF file from `examples/pdf/**`, it is a **unit test**
- No exceptions to this rule

## Application to AUTOSAR PDF Project

### For New Features

#### Step 1: Write Unit Test First (Primary Approach)
1. Write a failing unit test in the appropriate test file:
   - Parser logic: `tests/parser/test_pdf_parser.py`
   - Model classes: `tests/models/test_autosar_models.py`
   - Writer functionality: `tests/writer/test_markdown_writer.py`
   - CLI functionality: `tests/cli/test_autosar_cli.py`
2. Verify the unit test fails (RED)

#### Step 2: Implement Feature
1. Write minimum code in `src/autosar_pdf2txt/` to make the unit test pass
2. Run the unit test to verify it passes (GREEN)

#### Step 3: Write Integration Test (If Applicable)
1. Create or update integration test in `docs/test_cases/integration_tests.md`
2. Implement the integration test in `tests/integration/test_pdf_integration.py`
3. Verify the integration test uses actual PDF files from `examples/pdf/`
4. Verify the integration test passes

#### Step 4: Refactor
1. Improve code quality, structure, and naming
2. Ensure both unit and integration tests still pass

### For Bug Fixes

#### Step 1: Write Failing Unit Test
1. Write a unit test that reproduces the bug
2. Verify test fails (RED)

#### Step 2: Fix Bug
1. Write minimum code to fix the issue
2. Verify unit test passes (GREEN)

#### Step 3: Verify with Integration Test (If Applicable)
1. Run relevant integration tests with actual PDF files
2. Ensure the fix works correctly with real AUTOSAR documents
3. Verify no regressions in existing functionality

#### Step 4: Refactor
1. Improve the fix if needed
2. Ensure no regressions in all tests

## Test Case Documentation Requirement

**Rule**: Test cases documentation must be written before test case implementation.

**Requirements**:
- Before implementing any test case (unit or integration), the test case documentation MUST be written first
- Unit test cases MUST be documented in `docs/test_cases/unit_tests.md`
- Integration test cases MUST be documented in `docs/test_cases/integration_tests.md`
- Test case documentation MUST include:
  - Test case ID (e.g., SWUT_PARSER_00001 for unit tests)
  - Test case title
  - Requirement traceability (which requirement(s) this test validates)
  - Test description
  - Test steps
  - Expected results
  - Test data (if applicable, including PDF file names for integration tests)

**Purpose**:
- Ensure test cases are well-designed before implementation
- Provide clear documentation for test case maintenance
- Enable traceability between requirements and test cases
- Facilitate test case review and approval
- Serve as executable documentation for the system

**Process**:
1. **Document Test Case**: Write the test case documentation in the appropriate test cases document
2. **Review Test Case**: Ensure the test case documentation is complete and accurate
3. **Implement Test Case**: Write the actual test code based on the documented specification
4. **Verify Test Case**: Run the test and ensure it passes

**Example Test Case Documentation Format**:

```markdown
### SWUT_PARSER_00001: Class Definition Pattern Recognition

**Requirements**: SWR_PARSER_00004

**Description**: Verify that the parser correctly recognizes and extracts class definitions from PDF text, including abstract classes and classes with ATP markers.

**Test Steps**:
1. Create a test input with various class definition patterns
2. Parse the input using the PdfParser
3. Verify that all classes are extracted correctly
4. Verify that abstract flag is set correctly
5. Verify that ATP markers are detected correctly

**Expected Results**:
- All class definitions are extracted
- Abstract classes have is_abstract=True
- ATP markers are correctly identified and converted to ATPType enum values
- Multiple ATP markers on same class raise ValueError

**Test Data**:
- Class definition: "Class MyAbstractClass (abstract)"
- Class with ATP: "Class MyMixedClass <<atpMixedString>>"
- Class with multiple ATPs: "Class MyInvalidClass <<atpMixedString>> <<atpVariation>>"
```

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

---

## TDD Enforcement and Common Mistakes

### Common TDD Violations

#### Violation 1: Implementing Before Testing

**Wrong Approach**:
1. Implement the feature
2. Write tests
3. Update documentation

**Correct TDD Approach**:
1. Document test case in `docs/test_cases/unit_tests.md`
2. Write failing test (Red)
3. Implement minimum code to pass (Green)
4. Refactor if needed

**Why This Matters**:
- Writing tests first ensures you understand the requirements
- Prevents writing code that doesn't match requirements
- Tests serve as executable documentation
- Forces better design decisions

#### Violation 2: Skipping Test Documentation

**Wrong Approach**:
1. Write test code directly
2. Implement feature
3. Forget to document test case

**Correct TDD Approach**:
1. Document test case in `docs/test_cases/unit_tests.md` FIRST
2. Write test code based on documentation
3. Implement feature
4. Verify test passes

**Why This Matters**:
- Test documentation provides clear specification
- Enables traceability between requirements and tests
- Facilitates test case review and approval
- Serves as reference for future maintenance

#### Violation 3: Writing Too Much Code at Once

**Wrong Approach**:
1. Write complete feature implementation
2. Write all tests at once
3. Debug multiple issues simultaneously

**Correct TDD Approach**:
1. Write one failing test
2. Write minimum code to pass that test
3. Run tests to verify
4. Repeat for next test

**Why This Matters**:
- Smaller changes are easier to debug
- Tests guide implementation step by step
- Prevents over-engineering
- Faster feedback loop

#### Violation 4: Not Running Tests Frequently

**Wrong Approach**:
1. Write multiple tests
2. Implement multiple features
3. Run tests at the end

**Correct TDD Approach**:
1. Write one test
2. Run test (should fail)
3. Implement code
4. Run test (should pass)
5. Repeat

**Why This Matters**:
- Catch issues early
- Faster debugging
- Prevents cascading failures
- Maintains test suite health

### TDD Checklist

Before starting any new feature or bug fix:

- [ ] **Step 1**: Document test case in `docs/test_cases/unit_tests.md`
  - Test case ID (e.g., SWUT_CLI_00037)
  - Test case title
  - Requirement traceability
  - Test description
  - Test steps
  - Expected results
  - Test data (if applicable)

- [ ] **Step 2**: Write failing unit test
  - Test should fail (Red phase)
  - Test should be clear and focused
  - Test should have descriptive name

- [ ] **Step 3**: Implement minimum code
  - Write only enough code to make test pass (Green phase)
  - Don't optimize or refactor yet
  - Run test to verify it passes

- [ ] **Step 4**: Refactor if needed
  - Improve code quality
  - Ensure tests still pass
  - Run all tests to verify no regressions

- [ ] **Step 5**: Update requirements if needed
  - Add new requirement with maturity `draft`
  - Update requirement maturity to `accept` after implementation
  - Update requirement index in `docs/requirements/requirements.md`

- [ ] **Step 6**: Run quality checks
  ```bash
  python3 -m pytest tests/ -v
  ruff check src/ tests/
  mypy src/autosar_pdf2txt/
  ```

### TDD Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  Step 1: Document Test Case                                 │
│  ↓ docs/test_cases/unit_tests.md                            │
│  - Write test case documentation                            │
│  - Include test case ID, title, requirements, steps        │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Step 2: Write Failing Test (RED)                           │
│  ↓ tests/<module>/test_<module>.py                          │
│  - Write test based on documentation                        │
│  - Run test: should FAIL                                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Step 3: Implement Minimum Code (GREEN)                     │
│  ↓ src/autosar_pdf2txt/<module>/...                         │
│  - Write minimum code to make test pass                     │
│  - Run test: should PASS                                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Step 4: Refactor (if needed)                               │
│  ↓ src/autosar_pdf2txt/<module>/...                         │
│  - Improve code quality                                     │
│  - Run all tests: should all PASS                           │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Step 5: Update Requirements                                │
│  ↓ docs/requirements/requirements.md                        │
│  - Add/update requirement with maturity level               │
│  - Update requirement index                                 │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Step 6: Quality Gates                                      │
│  ↓ Run all checks                                           │
│  - pytest tests/ -v                                        │
│  - ruff check src/ tests/                                  │
│  - mypy src/autosar_pdf2txt/                               │
└─────────────────────────────────────────────────────────────┘
```

### Integration with Version Control

**Rule**: Each TDD cycle should result in a single commit.

```bash
# Correct: Single commit for complete TDD cycle
git add docs/test_cases/unit_tests.md
git add tests/cli/test_autosar_cli.py
git add src/autosar_pdf2txt/cli/autosar_cli.py
git add docs/requirements/requirements_cli.md
git add docs/requirements/requirements.md
git commit -m "feat: add --log-file CLI option

- Add SWR_CLI_00014 requirement
- Add SWUT_CLI_00037-00041 test cases
- Implement file handler creation and configuration
- Support parent directory creation
- Graceful error handling for file creation failures
- Timestamp format in log files"
```

### Automated TDD Verification

To help enforce TDD rules, consider adding pre-commit hooks:

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Check if test documentation exists for new tests
NEW_TESTS=$(git diff --cached --name-only | grep "tests/.*test_.*\.py")
if [ -n "$NEW_TESTS" ]; then
    echo "Checking for test documentation..."
    # Add validation logic here
fi

# Run tests before commit
python3 -m pytest tests/ -q
if [ $? -ne 0 ]; then
    echo "Tests failed. Please fix before committing."
    exit 1
fi
```

### Learning Resources

For team members new to TDD:

1. **Read**: `docs/development/tdd_rules.md` (this document)
2. **Practice**: Start with simple features using the TDD checklist
3. **Review**: Have code reviews verify TDD compliance
4. **Pair**: Pair program with experienced TDD practitioners
5. **Reflect**: After each task, review if TDD was followed correctly