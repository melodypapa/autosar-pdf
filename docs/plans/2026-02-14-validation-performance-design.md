# PDF Extraction Validation and Performance Improvement Design

**Date:** 2026-02-14
**Status:** Approved
**Version:** 1.0

## Overview

Design to improve PDF extraction correctness through ground truth validation and optimize parsing performance through caching and parallel processing. The system will validate extracted attributes against existing JSON definitions and generate error reports for manual review, enabling fast iteration cycles for improving YAML configuration.

## Motivation

Current limitations:
- PDF reading and parsing is very slow
- Difficult to identify parsing errors without manual review
- No automated validation against ground truth
- Slow iteration cycle for improving extraction accuracy

## Design

### 1. Architecture

**High-Level Flow:**
```
CLI → PDF Parser (parallel + cache) → Models (self-validate in __post_init__) → Error Report Writer
                                                          ↓
                                                    Markdown/JSON/Class Details
```

**Components:**

1. **Cache Layer** (new)
   - Stores parsed `AutosarDoc` as pickle file
   - Key: PDF file path + mtime + content hash
   - Location: `.cache/parsed_pdfs/`
   - Valid cache hit → skip parsing, load directly

2. **Parallel PDF Processing** (enhanced)
   - Use `multiprocessing.Pool` for parsing multiple PDFs
   - Each worker has own parser instance
   - Results combined after all workers complete

3. **Model Validation** (enhanced)
   - Add `ValidationError` collection to `AutosarDoc`
   - In `__post_init__`, validate attribute types exist
   - Track: missing classes, missing enums, missing primitives
   - Also track: attribute name mismatches, type mismatches

4. **Error Report Writer** (new)
   - Reads `AutosarDoc.validation_errors`
   - Generates structured error report (JSON)
   - Groups by severity/type for manual review

### 2. Caching Strategy

**Cache File Structure:**
```
.cache/
├── parsed_pdfs/
│   ├── {pdf_filename}_{mtime}_{hash}.pkl
│   └── cache_index.json  # Maps PDF path → cache file
└── validation_errors/
     └── errors_{timestamp}.json  # Historical error reports
```

**Cache Key Components:**
1. PDF file path
2. File modification time (mtime)
3. Content hash (SHA-256 of first/last 1KB)

**Cache Logic:**
```python
def get_cached_doc(pdf_path: Path) -> Optional[AutosarDoc]:
    # Check cache_index.json for valid entry
    # Verify mtime matches
    # Verify content hash matches
    # Load pickle and return
```

**Invalidation:**
- PDF file modified
- Cache older than 30 days
- Manual `--force-refresh` flag

**Performance Impact:**
- Cache hit: ~100ms (vs ~5-10s parsing)
- Development workflow: only parse changed PDFs

### 3. Parallel Processing Strategy

**Parallelization Approach:**

```python
# Process PDFs in parallel using multiprocessing
from multiprocessing import Pool, cpu_count

def parse_single_pdf(pdf_path: str) -> AutosarDoc:
    # Each worker has independent parser instance
    # Uses cache automatically
    parser = PdfParser()
    return parser.parse_pdf(pdf_path)

# Main parsing function
def parse_pdfs_parallel(pdf_paths: List[str]) -> AutosarDoc:
    # Split PDFs into batches
    num_workers = min(cpu_count(), len(pdf_paths))

    with Pool(processes=num_workers) as pool:
        results = pool.map(parse_single_pdf, pdf_paths)

    # Merge all AutosarDocs into one
    return merge_docs(results)
```

**Configuration:**
- Default: `min(cpu_count(), number_of_pdfs)`
- Override with `--jobs N` flag
- Disable with `--jobs 1` for sequential processing

**Considerations:**
1. **Cache-safe**: Each worker reads/writes cache independently (no race conditions)
2. **Memory**: Pickle cache is memory-efficient
3. **Progress**: Show progress bar with `[worker_id] PDF_name`

**Performance Estimate:**
- 10 PDFs, 10s each = 100s sequential
- 4 workers = ~25s parallel (4x speedup)

### 4. Model Validation

**Two-Phase Approach:**

**Phase 1: Parse (no validation)**
```python
def parse_pdfs_parallel(pdf_paths: List[str]) -> AutosarDoc:
    # Parse all PDFs, collect all models
    # NO validation during parsing
    # All classes/enums/primitives added to doc
    return doc
```

**Phase 2: Validate (after all parsing)**
```python
# In AutosarDoc.__post_init__ or separate validation method
def validate_document(self) -> List[ValidationError]:
    errors = []

    # Now we have ALL classes, enums, primitives
    for cls in self.all_classes():
        for attr in cls.attributes:
            type_name = attr.type
            # Search complete document
            if not self.find_type(type_name):
                errors.append(ValidationError(
                    class_name=cls.name,
                    attribute_name=attr.name,
                    issue="attribute_type_not_found",
                    expected=type_name,
                    source=attr.source
                ))

    return errors
```

**Validation Trigger Points:**
1. **After all PDFs parsed** in `parse_pdfs_parallel()`
2. **CLI command** `autosar-validate` on existing cache/JSON
3. **Manual flag** `--validate-after` to force validation

### 5. Error Report Format

**validation_errors.json**
```json
{
  "report_generated": "2026-02-14T10:30:00",
  "pdf_files_parsed": [
    "AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf"
  ],
  "validation_errors": [
    {
      "class_name": "BswModuleDescription",
      "package": "M2::AUTOSARTemplates::BswModuleTemplate::BswOverview",
      "attribute_name": "swComponent",
      "issue": "attribute_type_not_found",
      "severity": "error",
      "extracted_value": "SwComponent",
      "expected_value": null,
      "source": {
        "pdf_file": "AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf",
        "page": 42,
        "line": 15
      },
      "hint": "Type 'SwComponent' not found in ground truth. Check PDF page 42 for multi-line split or OCR error."
    }
  ],
  "summary": {
    "total_errors": 1,
    "by_severity": {
      "error": 1,
      "warning": 0
    },
    "by_issue_type": {
      "attribute_type_not_found": 1
    }
  }
}
```

**Purpose**: Human opens PDF page 42, sees the issue, manually updates `parser_config.yaml`, re-runs.

### 6. Data Flow

**Complete Flow with Caching + Parallel + Validation:**

```
User runs: autosar-extract examples/pdf/*.pdf --output output.md

[Phase 1: Cache Check & Parse]
  For each PDF (in parallel):
    1. Check cache: {pdf}_{mtime}_{hash}.pkl
    2. Cache hit? → Load AutosarDoc, skip to Phase 3
    3. Cache miss? → Parse PDF → Extract models → Save to cache

[Phase 2: Merge & Validate]
  1. Merge all AutosarDocs → Single AutosarDoc
  2. Validate all classes/attributes against JSON ground truth
  3. Collect validation_errors

[Phase 3: Output Generation]
  1. Write markdown/JSON/class-details to output
  2. Write validation_errors.json
  3. Display summary: "15 errors found in validation_errors.json"
```

**Key Points:**
- **Validation happens after all parsing** (complete document)
- **Ground truth loaded once** at startup
- **Error report always generated** (even if empty)
- **Human reviews error report** → Updates YAML manually → Re-runs

### 7. CLI Enhancements

**New CLI Arguments:**
```bash
autosar-extract [OPTIONS] PDF_FILES

Options:
  --jobs N            Number of parallel workers (default: min(cpu_count, #pdfs))
  --no-validate       Disable validation (for faster parsing only)
  --error-report FILE  Write validation errors to FILE (default: validation_errors.json)
  --force-refresh     Ignore cache and re-parse all PDFs
  --clear-cache       Clear all cached data
  -v, --verbose       Enable verbose output
```

### 8. Implementation Structure

**New Files to Add:**

```
src/autosar_pdf2txt/
├── cache/
│   ├── __init__.py
│   ├── cache_manager.py      # Cache read/write/mtime validation
│   └── parallel_parser.py      # Multiprocessing coordination
├── validation/
│   ├── __init__.py
│   ├── ground_truth.py         # Load data/packages/*.json
│   └── validator.py             # Document validation logic
└── models/
    └── validation.py             # ValidationError dataclass

tests/
├── test_cache/
├── test_validation/
└── test_parallel_parser/
```

**Key Implementation Sections:**

**A. Cache Manager**
```python
# src/autosar_pdf2txt/cache/cache_manager.py
class CacheManager:
    def get_cached_doc(pdf_path: Path) -> Optional[AutosarDoc]
    def save_cached_doc(pdf_path: Path, doc: AutosarDoc)
    def is_cache_valid(pdf_path: Path) -> bool
    def clear_cache(older_than_days: int = 30)
```

**B. Ground Truth Loader**
```python
# src/autosar_pdf2txt/validation/ground_truth.py
class GroundTruthLoader:
    def load_packages(data_dir: Path) -> Dict[str, TypeInfo]
    def find_type(name: str) -> Optional[TypeInfo]
    # Uses: {type_name: {kind, package, attributes}}
```

**C. Document Validator**
```python
# src/autosar_pdf2txt/validation/validator.py
class DocumentValidator:
    def validate_document(doc: AutosarDoc, ground_truth: GroundTruthLoader) -> List[ValidationError]
    def validate_attribute_types()
    def validate_class_names_in_mapping()
    def write_error_report(errors: List[ValidationError], output_path: Path)
```

**D. Parallel Parser Wrapper**
```python
# src/autosar_pdf2txt/cache/parallel_parser.py
def parse_pdfs_parallel(pdf_paths: List[str], num_workers: int = None) -> AutosarDoc:
    # Splits PDFs, creates Pool, merges results
```

### 9. Testing Strategy

**Unit Tests:**

```python
# tests/test_cache/test_cache_manager.py
def test_cache_hit_miss():
def test_cache_invalid_on_mtime_change():
def test_cache_hash_verification():

# tests/test_validation/test_ground_truth.py
def test_load_ground_truth():
def test_find_type_exists():
def test_find_type_not_found():

# tests/test_validation/test_validator.py
def test_validate_attribute_types():
def test_validate_missing_class():
def test_error_report_generation():
```

**Integration Tests:**

```python
# tests/integration/test_parallel_validation.py
def test_parse_multiple_pdfs_parallel():
def test_cache_across_runs():
def test_validation_error_report():
```

**Performance Benchmarks:**

```python
# tests/performance/test_caching_performance.py
def test_cache_hit_speed():
    # Expect: <100ms for cached doc vs ~5s for parse

def test_parallel_speedup():
    # Compare sequential vs parallel parsing
```

**Coverage Goal**: ≥95% (existing standard)

## Summary

**Features to Implement:**

1. ✅ **Parallel PDF Processing** - multiprocessing for faster parsing
2. ✅ **Intelligent Caching** - mtime/hash-based, skip re-parsing
3. ✅ **Ground Truth Validation** - load JSON once, validate after parsing
4. ✅ **Error Reporting** - structured JSON for manual review
5. ✅ **CLI Enhancements** - `--jobs`, `--no-validate`, `--error-report`

**Benefits:**
- **4-10x faster** for repeated runs (caching)
- **2-4x faster** for initial runs (parallel processing)
- **Automatic correctness checking** via ground truth validation
- **Fast iteration cycle** for improving YAML configuration

**No Breaking Changes** - All existing functionality preserved.
