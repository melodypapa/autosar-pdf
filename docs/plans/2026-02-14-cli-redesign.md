# CLI Redesign Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Redesign CLI output arguments to allow --mapping, --hierarchy, and --class-details flags to work independently or combined.

**Architecture:** Replace single -o output flag with three independent output flags (--mapping, --hierarchy, --class-details). Parse all flags, validate at least one is specified, parse PDFs once, then route to appropriate writer(s). Format auto-detected from file extensions.

**Tech Stack:** argparse (CLI), pdfplumber (PDF parsing), existing writer modules (MappingWriter, HierarchyWriter, MarkdownWriter)

---

### Task 1: Add requirements documentation

**Files:**
- Modify: `docs/requirements/requirements_cli.md`

**Step 1: Add new requirements**

Add to `docs/requirements/requirements_cli.md`:

```markdown
### SWR_CLI_00015: --mapping FILE argument

The CLI SHALL provide a `--mapping FILE` argument to generate type-to-package mapping output to the specified file.

**Maturity Level:** Draft

### SWR_CLI_00016: --hierarchy FILE argument

The CLI SHALL provide a `--hierarchy FILE` argument to generate class inheritance hierarchy output to the specified file.

**Maturity Level:** Draft

### SWR_CLI_00017: --class-details DIR argument

The CLI SHALL provide a `--class-details DIR` argument to generate individual class files in the specified directory.

**Maturity Level:** Draft

### SWR_CLI_00018: At least one output flag required

The CLI SHALL require at least one output flag (--mapping, --hierarchy, or --class-details) to be specified. If none are provided, the CLI SHALL exit with an error message.

**Maturity Level:** Draft

### SWR_CLI_00019: Format auto-detection from file extension

The CLI SHALL auto-detect output format from file extension: .md/.markdown for markdown, .json for JSON. Default to markdown if extension not recognized.

**Maturity Level:** Draft

### SWR_CLI_00020: Output flags can be combined

The CLI SHALL allow --mapping, --hierarchy, and --class-details flags to be combined in any combination without conflicts.

**Maturity Level:** Draft
```

Mark old requirements as deprecated:

```markdown
**DEPRECATED:** SWR_CLI_00008 - Replaced by SWR_CLI_00015, SWR_CLI_00016, SWR_CLI_00017
**DEPRECATED:** SWR_CLI_00011 - Replaced by SWR_CLI_00017
**DEPRECATED:** SWR_CLI_00012 - Replaced by SWR_CLI_00016
**DEPRECATED:** SWR_CLI_00014 - Replaced by SWR_CLI_00015
```

**Step 2: Commit**

```bash
git add docs/requirements/requirements_cli.md
git commit -m "docs: Add CLI redesign requirements (SWR_CLI_00015-00020)

- Add --mapping, --hierarchy, --class-details flag requirements
- Add validation and format auto-detection requirements
- Deprecate old output argument requirements

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### Task 2: Document test cases

**Files:**
- Modify: `docs/test_cases/unit_tests.md`

**Step 1: Add test case documentation**

Add to `docs/test_cases/unit_tests.md`:

```markdown
### SWUT_CLI_00038: --mapping flag generates mapping output

**Test:** When `--mapping FILE` is specified, the CLI SHALL generate type-to-package mapping to FILE.

**Scenarios:**
- Mapping only, markdown format
- Mapping only, JSON format
- Mapping + hierarchy (both files created)
- Mapping + class details (both created)
- Mapping + hierarchy + class details (all three created)

**Maturity Level:** Draft

### SWUT_CLI_00039: --hierarchy flag generates hierarchy output

**Test:** When `--hierarchy FILE` is specified, the CLI SHALL generate class inheritance hierarchy to FILE.

**Scenarios:**
- Hierarchy only, markdown format
- Hierarchy + mapping (both files created)
- Hierarchy + class details (both created)
- Hierarchy + mapping + class details (all three created)

**Maturity Level:** Draft

### SWUT_CLI_00040: --class-details flag generates class details

**Test:** When `--class-details DIR` is specified, the CLI SHALL generate individual class files in DIR/.

**Scenarios:**
- Class details only
- Class details + mapping (both created)
- Class details + hierarchy (both created)
- Class details + mapping + hierarchy (all three created)

**Maturity Level:** Draft

### SWUT_CLI_00041: Multiple output flags can be combined

**Test:** When multiple output flags are specified together, all outputs SHALL be generated.

**Scenarios:**
- --mapping + --hierarchy
- --mapping + --class-details
- --hierarchy + --class-details
- All three flags together

**Maturity Level:** Draft

### SWUT_CLI_00042: Error when no output flags specified

**Test:** When no output flags are specified, CLI SHALL exit with error message "At least one output flag must be specified: --mapping, --hierarchy, --class-details".

**Maturity Level:** Draft

### SWUT_CLI_00043: Format auto-detection from file extension

**Test:** Output format SHALL be auto-detected from file extension.

**Scenarios:**
- .md extension → markdown
- .markdown extension → markdown
- .json extension → json
- Unknown extension → error

**Maturity Level:** Draft

### SWUT_CLI_00044: Path validation for output files/directories

**Test:** CLI SHALL validate output paths before writing.

**Scenarios:**
- Parent directory doesn't exist for --mapping → error
- Parent directory doesn't exist for --hierarchy → error
- Directory doesn't exist for --class-details → create automatically
- Same file used for multiple outputs → error
- Directory path used for --mapping → error
- File path used for --class-details → error

**Maturity Level:** Draft
```

**Step 2: Commit**

```bash
git add docs/test_cases/unit_tests.md
git commit -m "docs: Add test cases for CLI redesign (SWUT_CLI_00038-00044)

- Document mapping, hierarchy, class-details output tests
- Document combination and validation tests
- Document format detection and path validation tests

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### Task 3: Create format detection utility

**Files:**
- Create: `src/autosar_pdf2txt/utils.py`
- Test: `tests/utils/test_utils.py`

**Step 1: Write failing test**

Create `tests/utils/test_utils.py`:

```python
"""Tests for utility functions."""

import pytest
from autosar_pdf2txt.utils import detect_format


class TestDetectFormat:
    """Test format detection from file extensions."""

    def test_markdown_extension(self):
        """Test .md extension detects markdown format."""
        assert detect_format("output.md") == "markdown"

    def test_markdown_long_extension(self):
        """Test .markdown extension detects markdown format."""
        assert detect_format("output.markdown") == "markdown"

    def test_json_extension(self):
        """Test .json extension detects json format."""
        assert detect_format("output.json") == "json"

    def test_unknown_extension_raises_error(self):
        """Test unknown extension raises ValueError."""
        with pytest.raises(ValueError, match="Unknown format .xyz"):
            detect_format("output.xyz")

    def test_no_extension_defaults_to_markdown(self):
        """Test no extension defaults to markdown."""
        assert detect_format("output") == "markdown"
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/utils/test_utils.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'autosar_pdf2txt.utils'"

**Step 3: Write minimal implementation**

Create `src/autosar_pdf2txt/utils.py`:

```python
"""Utility functions for autosar-pdf2txt."""

from pathlib import Path


def detect_format(filepath: str) -> str:
    """
    Detect output format from file extension.

    Args:
        filepath: Path to output file

    Returns:
        "markdown" or "json"

    Raises:
        ValueError: If file extension is not supported

    Requirements:
        SWR_CLI_00019: Format auto-detection from file extension
    """
    path = Path(filepath)
    extension = path.suffix.lower()

    format_map = {
        ".md": "markdown",
        ".markdown": "markdown",
        ".json": "json",
    }

    if extension in format_map:
        return format_map[extension]

    if not extension:
        # No extension, default to markdown
        return "markdown"

    raise ValueError(f"Unknown format {extension} (supported: .md, .markdown, .json)")
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/utils/test_utils.py -v
```

Expected: PASS (6/6 tests pass)

**Step 5: Commit**

```bash
git add src/autosar_pdf2txt/utils.py tests/utils/test_utils.py
git commit -m "feat: Add format detection utility (SWR_CLI_00019)

- Add detect_format() function for auto-detecting output format
- Support .md, .markdown, .json extensions
- Default to markdown if no extension
- Raise ValueError for unknown extensions

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### Task 4: Test CLI argument validation - no output flags

**Files:**
- Create: `tests/cli/test_cli_validation.py`
- Modify: `src/autosar_pdf2txt/cli.py` (later task)

**Step 1: Write failing test**

Create `tests/cli/test_cli_validation.py`:

```python
"""Tests for CLI argument validation."""

import pytest
from autosar_pdf2txt.cli import parse_args


class TestOutputValidation:
    """Test output flag validation."""

    def test_no_output_flags_raises_error(self):
        """Test error when no output flags specified."""
        with pytest.raises(SystemExit):
            parse_args(["input.pdf"])

    def test_only_mapping_flag_ok(self):
        """Test --mapping flag alone is accepted."""
        args = parse_args(["input.pdf", "--mapping", "output.md"])
        assert args.mapping == "output.md"
        assert args.hierarchy is None
        assert args.class_details is None

    def test_only_hierarchy_flag_ok(self):
        """Test --hierarchy flag alone is accepted."""
        args = parse_args(["input.pdf", "--hierarchy", "output.md"])
        assert args.mapping is None
        assert args.hierarchy == "output.md"
        assert args.class_details is None

    def test_only_class_details_flag_ok(self):
        """Test --class-details flag alone is accepted."""
        args = parse_args(["input.pdf", "--class-details", "classes/"])
        assert args.mapping is None
        assert args.hierarchy is None
        assert args.class_details == "classes/"
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/cli/test_cli_validation.py -v
```

Expected: FAIL with "AttributeError: module 'autosar_pdf2txt.cli' has no attribute 'parse_args'" or existing parser doesn't have new flags

**Step 3: Run existing CLI to understand current structure**

```bash
python -m autosar_pdf2txt.cli --help
```

**Step 4: Commit test file**

```bash
git add tests/cli/test_cli_validation.py
git commit -m "test: Add CLI validation tests (SWUT_CLI_00042, SWUT_CLI_00038-00040)

- Add test for error when no output flags specified
- Add tests for individual output flags
- Tests will fail until CLI is updated

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### Task 5: Update CLI parser with new arguments

**Files:**
- Modify: `src/autosar_pdf2txt/cli.py`

**Step 1: Read current CLI implementation**

```bash
cat src/autosar_pdf2txt/cli.py
```

**Step 2: Remove old argument definitions**

Remove these lines from `parse_args()` function:
- `parser.add_argument("-o", "--output", ...)`
- `parser.add_argument("--include-class-details", ...)`
- `parser.add_argument("--include-class-hierarchy", ...)`
- `parser.add_argument("--generate-mapping", ...)`

**Step 3: Add new argument definitions**

Add to `parse_args()` function:

```python
# Output arguments (at least one required)
output_group = parser.add_argument_group("output arguments")
output_group.add_argument(
    "--mapping",
    metavar="FILE",
    help="Generate type-to-package mapping to FILE",
)
output_group.add_argument(
    "--hierarchy",
    metavar="FILE",
    help="Generate class inheritance hierarchy to FILE",
)
output_group.add_argument(
    "--class-details",
    metavar="DIR",
    help="Generate individual class files to DIR/",
)
```

**Step 4: Add validation logic**

After `args = parser.parse_args()` add:

```python
# Validate at least one output flag is specified
if not any([args.mapping, args.hierarchy, args.class_details]):
    parser.error("At least one output flag must be specified: --mapping, --hierarchy, --class-details")
```

**Step 5: Run test to verify it passes**

```bash
pytest tests/cli/test_cli_validation.py -v
```

Expected: PASS (4/4 tests pass)

**Step 6: Test CLI help**

```bash
python -m autosar_pdf2txt.cli --help
```

Expected: Help shows new --mapping, --hierarchy, --class-details flags

**Step 7: Commit**

```bash
git add src/autosar_pdf2txt/cli.py
git commit -m "feat: Add new output CLI arguments (SWR_CLI_00015-00018)

- Add --mapping FILE argument for type-to-package mapping
- Add --hierarchy FILE argument for class hierarchy
- Add --class-details DIR argument for individual class files
- Remove old -o, --include-class-details, --include-class-hierarchy, --generate-mapping flags
- Validate at least one output flag is specified

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### Task 6: Test format auto-detection in CLI

**Files:**
- Test: `tests/cli/test_cli_validation.py`

**Step 1: Write failing test**

Add to `tests/cli/test_cli_validation.py`:

```python
def test_format_auto_detection_not_in_cli(self):
    """Note: Format detection happens in main(), not CLI parser."""
    # CLI just passes file paths, format detection happens later
    args = parse_args(["input.pdf", "--mapping", "output.json"])
    assert args.mapping == "output.json"
```

**Step 2: Run test**

```bash
pytest tests/cli/test_cli_validation.py::TestOutputValidation::test_format_auto_detection_not_in_cli -v
```

Expected: PASS (CLI just stores filepath, format detection happens in main)

**Step 3: Commit**

```bash
git add tests/cli/test_cli_validation.py
git commit -m "test: Verify CLI accepts any file extension for format detection

- CLI parser accepts any filepath
- Format detection happens in main() using detect_format()

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### Task 7: Update main() function signature and logic

**Files:**
- Modify: `src/autosar_pdf2txt/__init__.py`

**Step 1: Read current main() implementation**

```bash
cat src/autosar_pdf2txt/__init__.py
```

**Step 2: Write failing test for output config dictionary**

Create `tests/integration/test_output_combinations.py`:

```python
"""Tests for output combinations."""

import pytest
import tempfile
from pathlib import Path
from autosar_pdf2txt import main


class TestOutputCombinations:
    """Test multiple output flags work together."""

    def test_mapping_only(self, tmp_path):
        """Test --mapping flag alone."""
        mapping_file = tmp_path / "mapping.md"
        main(
            pdf_files=["examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf"],
            mapping=str(mapping_file),
            hierarchy=None,
            class_details=None,
            verbose=False,
            log_file=None,
        )
        assert mapping_file.exists()

    def test_hierarchy_only(self, tmp_path):
        """Test --hierarchy flag alone."""
        hierarchy_file = tmp_path / "hierarchy.md"
        main(
            pdf_files=["examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf"],
            mapping=None,
            hierarchy=str(hierarchy_file),
            class_details=None,
            verbose=False,
            log_file=None,
        )
        assert hierarchy_file.exists()

    def test_class_details_only(self, tmp_path):
        """Test --class-details flag alone."""
        details_dir = tmp_path / "classes"
        main(
            pdf_files=["examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf"],
            mapping=None,
            hierarchy=None,
            class_details=str(details_dir),
            verbose=False,
            log_file=None,
        )
        assert details_dir.exists()
        assert (details_dir / "AUTOSAR").exists()

    def test_mapping_and_hierarchy(self, tmp_path):
        """Test --mapping and --hierarchy together."""
        mapping_file = tmp_path / "mapping.md"
        hierarchy_file = tmp_path / "hierarchy.md"
        main(
            pdf_files=["examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf"],
            mapping=str(mapping_file),
            hierarchy=str(hierarchy_file),
            class_details=None,
            verbose=False,
            log_file=None,
        )
        assert mapping_file.exists()
        assert hierarchy_file.exists()

    def test_all_outputs(self, tmp_path):
        """Test all three output flags together."""
        mapping_file = tmp_path / "mapping.md"
        hierarchy_file = tmp_path / "hierarchy.md"
        details_dir = tmp_path / "classes"
        main(
            pdf_files=["examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf"],
            mapping=str(mapping_file),
            hierarchy=str(hierarchy_file),
            class_details=str(details_dir),
            verbose=False,
            log_file=None,
        )
        assert mapping_file.exists()
        assert hierarchy_file.exists()
        assert details_dir.exists()
```

**Step 3: Run test to verify it fails**

```bash
pytest tests/integration/test_output_combinations.py -v
```

Expected: FAIL with "main() got unexpected keyword argument" or wrong signature

**Step 4: Update main() signature**

Change `src/autosar_pdf2txt/__init__.py` main() signature from:

```python
def main(
    pdf_files: List[str],
    output: Optional[str] = None,
    include_class_details: bool = False,
    include_class_hierarchy: bool = False,
    generate_mapping: bool = False,
    verbose: bool = False,
    log_file: Optional[str] = None,
) -> None:
```

To:

```python
def main(
    pdf_files: List[str],
    mapping: Optional[str] = None,
    hierarchy: Optional[str] = None,
    class_details: Optional[str] = None,
    verbose: bool = False,
    log_file: Optional[str] = None,
) -> None:
```

**Step 5: Update main() implementation body**

Replace old output logic with:

```python
# Route to appropriate writers
outputs = []

if mapping:
    from autosar_pdf2txt.writer import MappingWriter
    from autosar_pdf2txt.utils import detect_format

    mapping_writer = MappingWriter()
    format = detect_format(mapping)
    content = mapping_writer.write_mapping(doc.packages, format=format)

    # Ensure parent directory exists
    Path(mapping).parent.mkdir(parents=True, exist_ok=True)

    with open(mapping, "w") as f:
        f.write(content)
    outputs.append(mapping)

if hierarchy:
    from autosar_pdf2txt.writer import HierarchyWriter
    from autosar_pdf2txt.utils import detect_format
    from autosar_pdf2txt.writer import collect_classes_from_package

    hierarchy_writer = HierarchyWriter()
    format = detect_format(hierarchy)

    # Collect root classes
    all_classes = []
    for pkg in doc.packages:
        classes = collect_classes_from_package(pkg)
        all_classes.extend(classes)
    root_classes = [cls for cls in all_classes if not cls.bases]

    content = hierarchy_writer.write_class_hierarchy(root_classes, all_classes)

    # Ensure parent directory exists
    Path(hierarchy).parent.mkdir(parents=True, exist_ok=True)

    with open(hierarchy, "w") as f:
        f.write(content)
    outputs.append(hierarchy)

if class_details:
    from autosar_pdf2txt.writer import MarkdownWriter

    details_writer = MarkdownWriter()

    # Ensure directory exists
    Path(class_details).mkdir(parents=True, exist_ok=True)

    # Generate individual class files
    for pkg in doc.packages:
        for cls in pkg.classes:
            class_path = Path(class_details) / f"{pkg.name}_{cls.name}.md"
            with open(class_path, "w") as f:
                f.write(details_writer.write_class(cls))
    outputs.append(class_details)

# Log success
if outputs:
    log.info(f"Generated {len(outputs)} output(s): {', '.join(outputs)}")
```

**Step 6: Run test to verify it passes**

```bash
pytest tests/integration/test_output_combinations.py -v
```

Expected: PASS (5/5 tests pass)

**Step 7: Commit**

```bash
git add src/autosar_pdf2txt/__init__.py tests/integration/test_output_combinations.py
git commit -m "feat: Implement output routing for new CLI arguments (SWR_CLI_00020)

- Update main() signature to accept mapping, hierarchy, class_details
- Route to MappingWriter when --mapping specified
- Route to HierarchyWriter when --hierarchy specified
- Route to MarkdownWriter for individual classes when --class-details specified
- All three outputs can be combined
- Use detect_format() for auto-detecting output format

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### Task 8: Update CLI entry point to use new arguments

**Files:**
- Modify: `src/autosar_pdf2txt/cli.py`

**Step 1: Find cli_main() function**

```bash
grep -n "def cli_main" src/autosar_pdf2txt/cli.py
```

**Step 2: Update cli_main() to pass new arguments**

Change from old arguments to new:

```python
def cli_main() -> None:
    """Entry point for autosar-extract command."""
    args = parse_args(sys.argv[1:])

    try:
        main(
            pdf_files=args.pdf_files,
            mapping=args.mapping,
            hierarchy=args.hierarchy,
            class_details=args.class_details,
            verbose=args.verbose,
            log_file=args.log_file,
        )
    except Exception as e:
        log.error(f"Error: {e}")
        sys.exit(1)
```

**Step 3: Test with real PDF**

```bash
python -m autosar_pdf2txt.cli examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf --mapping /tmp/test.md
```

Expected: /tmp/test.md created

**Step 4: Commit**

```bash
git add src/autosar_pdf2txt/cli.py
git commit -m "feat: Update CLI entry point to use new output arguments

- Update cli_main() to pass mapping, hierarchy, class_details to main()
- Remove old output, include_class_details, include_class_hierarchy, generate_mapping parameters

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### Task 9: Add path validation tests

**Files:**
- Test: `tests/integration/test_output_validation.py`

**Step 1: Write path validation tests**

Create `tests/integration/test_output_validation.py`:

```python
"""Tests for output path validation."""

import pytest
from pathlib import Path
from autosar_pdf2txt import main


class TestPathValidation:
    """Test output path validation."""

    def test_same_file_multiple_outputs_error(self, tmp_path):
        """Test error when same file used for multiple outputs."""
        output_file = tmp_path / "output.md"
        with pytest.raises(ValueError, match="Cannot use same output file"):
            main(
                pdf_files=["examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf"],
                mapping=str(output_file),
                hierarchy=str(output_file),
                class_details=None,
                verbose=False,
                log_file=None,
            )

    def test_directory_for_mapping_flag_error(self, tmp_path):
        """Test error when directory path used for --mapping."""
        dir_path = tmp_path / "output"
        dir_path.mkdir()
        with pytest.raises(ValueError, match="Expected file for --mapping"):
            main(
                pdf_files=["examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf"],
                mapping=str(dir_path),
                hierarchy=None,
                class_details=None,
                verbose=False,
                log_file=None,
            )

    def test_file_for_class_details_flag_error(self, tmp_path):
        """Test error when file path used for --class-details."""
        file_path = tmp_path / "not_a_dir.md"
        file_path.touch()
        with pytest.raises(ValueError, match="Expected directory for --class-details"):
            main(
                pdf_files=["examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf"],
                mapping=None,
                hierarchy=None,
                class_details=str(file_path),
                verbose=False,
                log_file=None,
            )

    def test_unknown_format_extension_error(self, tmp_path):
        """Test error when unknown format extension used."""
        mapping_file = tmp_path / "output.xyz"
        with pytest.raises(ValueError, match="Unknown format .xyz"):
            main(
                pdf_files=["examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf"],
                mapping=str(mapping_file),
                hierarchy=None,
                class_details=None,
                verbose=False,
                log_file=None,
            )
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/integration/test_output_validation.py -v
```

Expected: FAIL (validation not implemented yet)

**Step 3: Commit test file**

```bash
git add tests/integration/test_output_validation.py
git commit -m "test: Add path validation tests (SWUT_CLI_00044)

- Add tests for same file multiple outputs
- Add tests for directory vs file path validation
- Add test for unknown format extension
- Tests will fail until validation is implemented

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### Task 10: Implement path validation in main()

**Files:**
- Modify: `src/autosar_pdf2txt/__init__.py`

**Step 1: Add validation function to main()**

Add before output routing:

```python
# Validate output paths
output_files = []
if mapping:
    mapping_path = Path(mapping)
    if mapping_path.is_dir():
        raise ValueError(f"Expected file for --mapping but '{mapping}' is a directory")
    output_files.append(mapping_path)

if hierarchy:
    hierarchy_path = Path(hierarchy)
    if hierarchy_path.is_dir():
        raise ValueError(f"Expected file for --hierarchy but '{hierarchy}' is a directory")
    if hierarchy_path in output_files:
        raise ValueError(f"Cannot use same output file '{hierarchy}' for multiple outputs")
    output_files.append(hierarchy_path)

if mapping and hierarchy and Path(mapping) == Path(hierarchy):
    raise ValueError(f"Cannot use same output file '{mapping}' for multiple outputs")

if class_details:
    details_path = Path(class_details)
    if details_path.exists() and details_path.is_file():
        raise ValueError(f"Expected directory for --class-details but '{class_details}' is a file")
```

**Step 2: Run test to verify it passes**

```bash
pytest tests/integration/test_output_validation.py -v
```

Expected: PASS (4/4 tests pass)

**Step 3: Commit**

```bash
git add src/autosar_pdf2txt/__init__.py
git commit -m "feat: Add path validation for output arguments (SWUT_CLI_00044)

- Validate --mapping and --hierarchy are files, not directories
- Validate --class-details is directory, not file
- Detect and error on same file used for multiple outputs
- Format validation already handled by detect_format()

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### Task 11: Test JSON format output for mapping

**Files:**
- Test: `tests/integration/test_format_detection.py`

**Step 1: Write JSON format test**

Create `tests/integration/test_format_detection.py`:

```python
"""Tests for format auto-detection."""

import json
from pathlib import Path
from autosar_pdf2txt import main


class TestFormatDetection:
    """Test format auto-detection from file extension."""

    def test_mapping_markdown_format(self, tmp_path):
        """Test .md extension generates markdown."""
        mapping_file = tmp_path / "mapping.md"
        main(
            pdf_files=["examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf"],
            mapping=str(mapping_file),
            hierarchy=None,
            class_details=None,
            verbose=False,
            log_file=None,
        )
        content = mapping_file.read_text()
        assert "# Type to Package Mapping" in content
        assert "| Name | Type |" in content

    def test_mapping_json_format(self, tmp_path):
        """Test .json extension generates JSON."""
        mapping_file = tmp_path / "mapping.json"
        main(
            pdf_files=["examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf"],
            mapping=str(mapping_file),
            hierarchy=None,
            class_details=None,
            verbose=False,
            log_file=None,
        )
        content = mapping_file.read_text()
        data = json.loads(content)
        assert "types" in data
        assert isinstance(data["types"], list)
```

**Step 2: Run test to verify it passes**

```bash
pytest tests/integration/test_format_detection.py -v
```

Expected: PASS (2/2 tests pass)

**Step 3: Commit**

```bash
git add tests/integration/test_format_detection.py
git commit -m "test: Add format auto-detection tests (SWR_CLI_00019)

- Test .md extension generates markdown output
- Test .json extension generates JSON output
- Verify detect_format() integrates correctly with main()

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### Task 12: Remove old CLI tests for deprecated arguments

**Files:**
- Modify: `tests/cli/test_cli_args.py` (or similar)

**Step 1: Find old CLI tests**

```bash
grep -r "include-class-details\|include-class-hierarchy\|generate-mapping" tests/
```

**Step 2: Remove tests for old arguments**

Remove test functions that test:
- `--output` or `-o`
- `--include-class-details`
- `--include-class-hierarchy`
- `--generate-mapping`
- Conflicts between `--generate-mapping` and other flags

**Step 3: Commit**

```bash
git add tests/
git commit -m "test: Remove tests for deprecated CLI arguments

- Remove tests for --output, --include-class-details, --include-class-hierarchy, --generate-mapping
- Keep tests for --verbose, --log-file, and positional arguments

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### Task 13: Run full test suite and fix any issues

**Files:**
- All files

**Step 1: Run unit tests**

```bash
python scripts/run_tests.py --unit
```

Expected: All unit tests pass

**Step 2: Run integration tests**

```bash
python scripts/run_tests.py --integration
```

Expected: All integration tests pass

**Step 3: Run all tests**

```bash
python scripts/run_tests.py --all
```

Expected: All tests pass with ≥95% coverage

**Step 4: Fix any failing tests**

If any tests fail, debug and fix:
- Read test output
- Identify failure reason
- Fix implementation or test
- Re-run until all pass

**Step 5: Commit**

```bash
git add .
git commit -m "test: Fix failing tests after CLI redesign

- Update any tests that broke due to signature changes
- Ensure all tests pass with ≥95% coverage

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### Task 14: Update README with new CLI usage

**Files:**
- Modify: `README.md`

**Step 1: Update CLI Options section**

Replace old CLI options table with new:

````markdown
#### CLI Options

- `pdf_files`: Path(s) to PDF file(s) or director(y/ies) containing PDFs to parse
- `--mapping FILE`: Generate type-to-package mapping to FILE
- `--hierarchy FILE`: Generate class inheritance hierarchy to FILE
- `--class-details DIR`: Generate individual class files to DIR/
- `--format {markdown,json}`: Output format (default: inferred from file extension)
- `-v, --verbose`: Enable verbose output mode for detailed debug information
- `--log-file LOG_FILE`: Write log messages to a file with timestamps (default: console only)
- `-h, --help`: Show help message

**Note:** At least one output flag (`--mapping`, `--hierarchy`, `--class-details`) must be specified.
````

**Step 2: Update usage examples**

Replace old examples with new:

````markdown
### Command Line Interface

```bash
# Generate type-to-package mapping
autosar-extract examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf --mapping mapping.md

# Generate class hierarchy
autosar-extract examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf --hierarchy hierarchy.md

# Generate individual class files
autosar-extract examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf --class-details classes/

# Combine multiple outputs
autosar-extract examples/pdf/ --mapping mapping.md --hierarchy hierarchy.md --class-details classes/

# Generate mapping in JSON format
autosar-extract examples/pdf/ --mapping mapping.json
```
````

**Step 3: Add migration guide**

Add new section after usage examples:

````markdown
### Migration from v1.x to v2.0

Version 2.0.0 includes breaking changes to CLI arguments. Here's how to migrate:

**Old: Generate mapping**
```bash
autosar-extract input.pdf -o output.md --generate-mapping
```

**New:**
```bash
autosar-extract input.pdf --mapping output.md
```

**Old: Generate hierarchy**
```bash
autosar-extract input.pdf -o output.md --include-class-hierarchy
```

**New:**
```bash
autosar-extract input.pdf --hierarchy output.md
```

**Old: Generate class details**
```bash
autosar-extract input.pdf -o output.md --include-class-details
```

**New:**
```bash
autosar-extract input.pdf --class-details output/
```

**Old: Combine mapping + hierarchy**
```bash
autosar-extract input.pdf -o output.md --generate-mapping --include-class-hierarchy
```

**New:**
```bash
autosar-extract input.pdf --mapping mapping.md --hierarchy hierarchy.md
```
````

**Step 4: Update Python API section**

Remove references to old CLI arguments in Python API examples.

**Step 5: Commit**

```bash
git add README.md
git commit -m "docs: Update README for CLI redesign v2.0

- Update CLI options table with new --mapping, --hierarchy, --class-details flags
- Update usage examples with new syntax
- Add migration guide from v1.x to v2.0
- Remove references to deprecated CLI arguments

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### Task 15: Update CLAUDE.md with new commands

**Files:**
- Modify: `CLAUDE.md`

**Step 1: Update Essential Commands section**

Replace old CLI examples:

````markdown
# Parse PDFs
autosar-extract examples/pdf/ --mapping data/autosar_mapping.md
autosar-extract examples/pdf/ --hierarchy data/autosar_hierarchy.md
autosar-extract examples/pdf/ --class-details data/autosar_classes/
````

**Step 2: Update Common Tasks section**

Update all task examples to use new CLI flags.

**Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: Update CLAUDE.md for CLI redesign v2.0

- Update Essential Commands with new CLI syntax
- Update Common Tasks examples
- Remove references to deprecated CLI arguments

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### Task 16: Update version to 2.0.0

**Files:**
- Modify: `pyproject.toml`

**Step 1: Update version**

Change in `pyproject.toml`:

```
version = "2.0.0"
```

**Step 2: Update development status**

Change in `pyproject.toml`:

```
"Development Status :: 5 - Production/Stable",
```

**Step 3: Commit**

```bash
git add pyproject.toml
git commit -m "chore: Bump version to 2.0.0 for breaking changes

- Major version bump for CLI redesign
- Update development status to 5 - Production/Stable
- Breaking changes: removed -o, --generate-mapping, --include-class-hierarchy, --include-class-details

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### Task 17: Add changelog entry

**Files:**
- Modify: `README.md` (Changelog section)

**Step 1: Add version entry**

Add to Changelog section:

````markdown
## Version 2.0.0 (Breaking Change)
- **CLI Redesign**: Redesigned CLI output arguments for better flexibility
- **Removed**: `-o`, `--generate-mapping`, `--include-class-hierarchy`, `--include-class-details`
- **Added**: `--mapping FILE`, `--hierarchy FILE`, `--class-details DIR`
- **Feature**: Output flags can now be combined in any combination
- **Feature**: Format auto-detected from file extension (.md, .json)
- **Migration**: See "Migration from v1.x to v2.0" section
````

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: Add v2.0.0 changelog entry

- Document breaking changes in CLI redesign
- List removed and added arguments
- Reference migration guide

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### Task 18: Run quality gates

**Files:**
- All files

**Step 1: Run ruff linting**

```bash
ruff check src/ tests/
```

Expected: No errors

**Step 2: Run mypy type checking**

```bash
mypy src/autosar_pdf2txt/
```

Expected: No errors

**Step 3: Run full test suite**

```bash
python scripts/run_tests.py --all
```

Expected: All tests pass with ≥95% coverage

**Step 4: Fix any issues**

If any quality checks fail, fix and re-run until all pass.

**Step 5: Commit**

```bash
git add .
git commit -m "chore: Fix quality gate issues for v2.0.0

- Fix any ruff linting issues
- Fix any mypy type checking issues
- Ensure all tests pass with ≥95% coverage

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### Task 19: Create git tag for v2.0.0

**Files:**
- None

**Step 1: Create annotated tag**

```bash
git tag -a v2.0.0 -m "Version 2.0.0: CLI Redesign

Breaking Changes:
- Removed -o, --generate-mapping, --include-class-hierarchy, --include-class-details
- Added --mapping FILE, --hierarchy FILE, --class-details DIR
- Output flags can now be combined in any combination
- Format auto-detected from file extension

Features:
- Flexible output generation with explicit filename control
- No conflicts between output types
- Better CLI ergonomics

See README.md for migration guide from v1.x"
```

**Step 2: Push tag**

```bash
git push origin v2.0.0
```

---

## Summary

This implementation plan covers:
1. Requirements documentation (SWR_CLI_00015-00020)
2. Test case documentation (SWUT_CLI_00038-00044)
3. Format detection utility
4. CLI argument updates
5. Output routing logic
6. Path validation
7. Integration testing
8. Documentation updates
9. Version bump and quality gates

**Total Tasks:** 19
**Estimated Time:** 3-5 hours (following TDD with frequent commits)
