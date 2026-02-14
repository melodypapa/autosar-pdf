# CLI Redesign for Flexible Output

**Date:** 2026-02-14
**Status:** Approved
**Version:** 2.0.0 (Breaking Change)

## Overview

Redesign CLI output arguments to remove conflicts between `--generate-mapping` and other output flags (`--include-class-hierarchy`, `--include-class-details`). The new design allows all output types to work together seamlessly with explicit filename control.

## Motivation

Current CLI has these limitations:
- `--generate-mapping` conflicts with `--include-class-details` and `--include-class-hierarchy`
- Cannot combine mapping output with hierarchy or class details
- Filename for non-mapping outputs tied to `-o` flag with auto-generated suffixes

## Design

### 1. CLI Interface

**New CLI Arguments:**
```
autosar-extract [OPTIONS] PDF_FILES

Options:
  --mapping FILE        Generate type-to-package mapping to FILE
  --hierarchy FILE      Generate class inheritance hierarchy to FILE
  --class-details DIR   Generate individual class files to DIR/
  --format {markdown,json}
                       Output format for mapping/hierarchy (auto-detected from extension)
  -v, --verbose         Enable verbose output
  --log-file LOG_FILE   Write log messages to file with timestamps
  -h, --help            Show help message
```

**Removed Arguments:**
- `-o OUTPUT, --output OUTPUT` (replaced by specific flags)
- `--include-class-details` (replaced by `--class-details DIR`)
- `--include-class-hierarchy` (replaced by `--hierarchy FILE`)
- `--generate-mapping` (replaced by `--mapping FILE`)

**Behavior:**
- All three output flags (`--mapping`, `--hierarchy`, `--class-details`) are optional
- Can be used independently or in any combination
- At least one output flag must be specified (error if none provided)
- Format auto-detected from file extension (.md, .markdown → markdown, .json → json)
- `--class-details DIR` creates individual class files under DIR/ in subdirectories by package

### 2. Architecture

**High-Level Flow:**
```
CLI Argument Parsing → PDF Parsing → Output Generation (parallel)
                                  ├── MappingWriter
                                  ├── HierarchyWriter
                                  └── ClassDetailsWriter
```

**Component Changes:**

**A. CLI Module (`src/autosar_pdf2txt/cli.py`)**
- Remove old argument definitions (`output`, `include_class_details`, `include_class_hierarchy`, `generate_mapping`)
- Add new argument definitions (`mapping`, `hierarchy`, `class_details`)
- Add validation: at least one output flag must be specified
- Pass output specifications to main function as dictionary

**B. Main Processing (`src/autosar_pdf2txt/__init__.py`)**
- Update `main()` function signature to accept output config dict instead of single output path
- Parse PDFs once (unchanged)
- Route to appropriate writer(s) based on output config

**C. Writer Module (`src/autosar_pdf2txt/writer/`)**
- `MarkdownWriter`: Keep as-is (used by `--class-details`)
- `MappingWriter`: Keep as-is (used by `--mapping`)
- `HierarchyWriter`: Keep as-is (used by `--hierarchy`)
- New coordination logic in main to invoke multiple writers

**D. Error Handling**
- Validate file paths before writing (directory exists, writable)
- Validate format compatibility (mapping supports both md/json, hierarchy supports md)
- Clear error messages for invalid combinations

### 3. Data Flow & Implementation

**Step-by-Step Flow:**

```python
# CLI Parsing
args = parse_args(argv)
output_config = {
    'mapping': args.mapping,      # None or filepath
    'hierarchy': args.hierarchy,  # None or filepath
    'class_details': args.class_details  # None or directory
}

# Validation
if not any(output_config.values()):
    raise ValueError("At least one output flag must be specified: --mapping, --hierarchy, --class-details")

# PDF Parsing (unchanged)
parser = PdfParser(verbose=args.verbose, log_file=args.log_file)
doc = parser.parse_pdfs(args.pdf_files)

# Output Generation (parallel, not concurrent)
outputs = []

if output_config['mapping']:
    mapping_writer = MappingWriter()
    format = detect_format(output_config['mapping'])
    content = mapping_writer.write_mapping(doc.packages, format=format)
    write_file(output_config['mapping'], content)
    outputs.append(output_config['mapping'])

if output_config['hierarchy']:
    hierarchy_writer = HierarchyWriter()
    format = detect_format(output_config['hierarchy'])
    root_classes = collect_root_classes(doc)
    content = hierarchy_writer.write_hierarchy(root_classes, doc, format=format)
    write_file(output_config['hierarchy'], content)
    outputs.append(output_config['hierarchy'])

if output_config['class_details']:
    details_writer = ClassDetailsWriter()
    details_writer.write_classes(doc, output_config['class_details'])
    outputs.append(output_config['class_details'])

log.info(f"Generated {len(outputs)} output(s): {', '.join(outputs)}")
```

**Key Implementation Points:**

1. **Format Detection:** Auto-detect from file extension
   - `.md`, `.markdown` → markdown
   - `.json` → json
   - Default: markdown

2. **Path Validation:** Check before writing
   - Directory exists for `--class-details` (create if not exists)
   - Parent directory exists for `--mapping`, `--hierarchy` (error if not)
   - File is writable

3. **Error Messages:** Clear and actionable
   - "Error: At least one output flag must be specified"
   - "Error: Cannot write to /path/to/file: Permission denied"
   - "Error: Unknown format .xyz (supported: .md, .json)"

4. **Logging:** Update success messages
   - Old: `Writing to: output.md`
   - New: `Generated 3 output(s): mapping.md, hierarchy.md, classes/`

### 4. Testing Strategy

**Test Categories:**

**A. CLI Argument Tests (`tests/cli/test_cli_args.py`)**
- Test new argument parsing (`--mapping`, `--hierarchy`, `--class-details`)
- Test format detection from file extensions
- Test validation: error when no output flags specified
- Test that old arguments are removed
- Test multiple output flags together

**B. Integration Tests (`tests/integration/test_output_combinations.py`)**
- Test `--mapping` only (markdown and json)
- Test `--hierarchy` only
- Test `--class-details` only
- Test all three combinations:
  - `--mapping` + `--hierarchy`
  - `--mapping` + `--class-details`
  - `--hierarchy` + `--class-details`
  - All three together
- Test path validation (non-existent directory, permission denied)

**C. Writer Tests (Existing, minimal updates)**
- `MappingWriter`: No changes needed (100% coverage)
- `HierarchyWriter`: No changes needed (100% coverage)
- `ClassDetailsWriter`: No changes needed (100% coverage)

**D. Error Handling Tests**
- Test error when no output flags specified
- Test error when directory doesn't exist for `--class-details`
- Test error when parent directory doesn't exist for `--mapping`, `--hierarchy`

**Test Cases to Document:**
- SWUT_CLI_00038: New `--mapping` flag generates mapping output
- SWUT_CLI_00039: New `--hierarchy` flag generates hierarchy output
- SWUT_CLI_00040: New `--class-details` flag generates class details
- SWUT_CLI_00041: Multiple output flags can be combined
- SWUT_CLI_00042: Error when no output flags specified
- SWUT_CLI_00043: Format auto-detection from file extension
- SWUT_CLI_00044: Path validation for output files/directories

### 5. Breaking Changes & Migration

**Breaking Changes:**

1. **Removed Arguments:**
   - `-o OUTPUT, --output OUTPUT`
   - `--include-class-details`
   - `--include-class-hierarchy`
   - `--generate-mapping`

2. **Required Change:** Users must specify at least one output flag

**Migration Examples:**

```bash
# OLD: Generate mapping
autosar-extract input.pdf -o output.md --generate-mapping

# NEW:
autosar-extract input.pdf --mapping output.md

---

# OLD: Generate hierarchy
autosar-extract input.pdf -o output.md --include-class-hierarchy

# NEW:
autosar-extract input.pdf --hierarchy output.md

---

# OLD: Generate class details
autosar-extract input.pdf -o output.md --include-class-details

# NEW:
autosar-extract input.pdf --class-details output/

---

# OLD: Generate mapping + hierarchy
autosar-extract input.pdf -o output.md --generate-mapping --include-class-hierarchy

# NEW:
autosar-extract input.pdf --mapping output.md --hierarchy output-hierarchy.md

---

# OLD: Generate all outputs
autosar-extract input.pdf -o output.md --include-class-hierarchy --include-class-details

# NEW:
autosar-extract input.pdf --mapping output.md --hierarchy output-hierarchy.md --class-details output/classes/
```

**Version Bump:**
- Update version from 1.0.0 → 2.0.0 (major version for breaking changes)

**Changelog Entry:**
```
## Version 2.0.0 (Breaking Change)
- Redesigned CLI output arguments for better flexibility
- Removed: -o, --generate-mapping, --include-class-hierarchy, --include-class-details
- Added: --mapping FILE, --hierarchy FILE, --class-details DIR
- Output flags can now be combined in any combination
- Format auto-detected from file extension
```

### 6. Edge Cases & Special Scenarios

**A. Output Path Conflicts**
- **Scenario:** Same output file specified multiple times
  ```bash
  autosar-extract input.pdf --mapping output.md --hierarchy output.md
  ```
  - **Resolution:** Error - "Cannot use same output file 'output.md' for multiple outputs"

**B. Directory vs File Ambiguity**
- **Scenario:** Path exists as both file and directory (unlikely but possible)
  ```bash
  autosar-extract input.pdf --mapping existing_dir/
  ```
  - **Resolution:** Error - "Expected file for --mapping but 'existing_dir/' is a directory"

**C. Empty Output**
- **Scenario:** PDF contains no classes/packages
  - **Resolution:** Generate empty output files with headers only (existing behavior)

**D. Format Mismatch**
- **Scenario:** Unsupported file extension
  ```bash
  autosar-extract input.pdf --mapping output.xyz
  ```
  - **Resolution:** Error - "Unknown format .xyz (supported: .md, .json)"

**E. Path Creation**
- **Scenario:** Parent directory doesn't exist for `--mapping` or `--hierarchy`
  ```bash
  autosar-extract input.pdf --mapping /new/path/output.md
  ```
  - **Resolution:** Error - "Parent directory does not exist: /new/path/"

- **Scenario:** Directory doesn't exist for `--class-details`
  ```bash
  autosar-extract input.pdf --class-details /new/path/classes/
  ```
  - **Resolution:** Create directory and subdirectories automatically (existing behavior)

**F. JSON Format Compatibility**
- **Scenario:** User specifies JSON for hierarchy (not currently supported)
  ```bash
  autosar-extract input.pdf --hierarchy output.json
  ```
  - **Resolution:** Error - "Hierarchy output only supports markdown format"

### 7. Documentation Updates

**Files to Update:**

**A. README.md**
- Update "Usage" section with new CLI examples
- Update "CLI Options" table with new flags
- Add migration guide section (v1.x → v2.0)
- Remove old flag documentation
- Update all examples throughout

**B. CLAUDE.md**
- Update "Essential Commands" section with new CLI syntax
- Update examples in "Common Tasks" section
- Update requirements documentation with new CLI requirement IDs

**C. Changelog (README.md)**
- Add Version 2.0.0 entry with breaking changes notice
- Include migration examples

**D. Requirements (`docs/requirements/requirements_cli.md`)**
- Add new requirements for:
  - SWR_CLI_00015: `--mapping FILE` argument
  - SWR_CLI_00016: `--hierarchy FILE` argument
  - SWR_CLI_00017: `--class-details DIR` argument
  - SWR_CLI_00018: At least one output flag required
  - SWR_CLI_00019: Format auto-detection from file extension
  - SWR_CLI_00020: Output flags can be combined
- Mark old requirements as deprecated:
  - SWR_CLI_00008 (old `--output` argument)
  - SWR_CLI_00011 (old `--include-class-details`)
  - SWR_CLI_00012 (old `--include-class-hierarchy`)
  - SWR_CLI_00014 (old `--generate-mapping`)

**E. Test Documentation (`docs/test_cases/unit_tests.md`)**
- Document test cases SWUT_CLI_00038 through SWUT_CLI_00044
- Add test scenarios for edge cases

## Requirements Traceability

- **SWR_CLI_00015**: New `--mapping FILE` argument for type-to-package mapping
- **SWR_CLI_00016**: New `--hierarchy FILE` argument for class hierarchy
- **SWR_CLI_00017**: New `--class-details DIR` argument for individual class files
- **SWR_CLI_00018**: Validation: at least one output flag required
- **SWR_CLI_00019**: Format auto-detection from file extension
- **SWR_CLI_00020**: Output flags can be combined without conflicts

## Implementation Plan

See separate implementation plan created by writing-plans skill.

## Approval

- [x] Design approved by user
- [x] Ready for implementation plan creation
