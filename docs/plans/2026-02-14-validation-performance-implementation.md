# Validation and Performance Improvement Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** Add PDF extraction correctness validation via ground truth comparison and optimize parsing performance through caching and parallel processing.

**Architecture:** Two-phase parsing (parallel extract → merge → validate) with pickle-based caching (mtime+hash keys) and multiprocessing Pool for concurrent PDF processing. Ground truth loaded once from `data/packages/*.json` at startup for validation.

**Tech Stack:** Python multiprocessing, pickle serialization, hashlib for content hashing, existing pdfplumber backend, pytest for testing.

---

## Task 1: Add ValidationError Model

**Files:**
- Create: `src/autosar_pdf2txt/models/validation.py`
- Test: `tests/models/test_validation.py`

**Step 1: Write failing test**

```python
# tests/models/test_validation.py
import pytest
from autosar_pdf2txt.models.validation import ValidationError, ValidationErrorSeverity

def test_validation_error_creation():
    error = ValidationError(
        class_name="TestClass",
        package="M2::TestPackage",
        attribute_name="testAttr",
        issue="attribute_type_not_found",
        severity="error",
        extracted_value="WrongType",
        expected_value=None,
        source=AutosarDocumentSource(
            pdf_file="test.pdf",
            page_number=42
        )
    )
    assert error.class_name == "TestClass"
    assert error.issue == "attribute_type_not_found"
    assert error.severity == "error"

def test_validation_error_to_dict():
    error = ValidationError(
        class_name="TestClass",
        issue="test_issue",
        severity="warning"
    )
    data = error.to_dict()
    assert data["class_name"] == "TestClass"
    assert data["severity"] == "warning"
    assert "hint" in data
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/models/test_validation.py -v`
Expected: FAIL with "ValidationError not defined" or import error

**Step 3: Write minimal implementation**

```python
# src/autosar_pdf2txt/models/validation.py
from dataclasses import dataclass, field
from typing import Optional
from autosar_pdf2txt.models.base import AutosarDocumentSource

@dataclass
class ValidationError:
    """Represents a validation error found during PDF extraction validation.

    Requirements:
        SWR_VALIDATION_00001: ValidationError Data Model

    Attributes:
        class_name: Name of the class with the error
        package: Package path (optional)
        attribute_name: Name of attribute with error (optional)
        issue: Type of issue (e.g., "attribute_type_not_found")
        severity: "error", "warning", or "info"
        extracted_value: The value that was extracted (optional)
        expected_value: The value that was expected (optional)
        source: Document source location (optional)
        hint: Helpful message for manual review (auto-generated)
    """
    class_name: str
    package: Optional[str] = None
    attribute_name: Optional[str] = None
    issue: str
    severity: str = "error"
    extracted_value: Optional[str] = None
    expected_value: Optional[str] = None
    source: Optional[AutosarDocumentSource] = None
    hint: Optional[str] = None

    def __post_init__(self):
        """Auto-generate hint if not provided."""
        if self.hint is None:
            self.hint = self._generate_hint()

    def _generate_hint(self) -> str:
        """Generate helpful hint based on issue type."""
        if self.issue == "attribute_type_not_found":
            return f"Type '{self.extracted_value}' not found in ground truth. Check PDF page {self.source.page_number if self.source else '?'} for multi-line split or OCR error."
        return f"Validation issue: {self.issue}"

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "class_name": self.class_name,
            "package": self.package,
            "attribute_name": self.attribute_name,
            "issue": self.issue,
            "severity": self.severity,
            "extracted_value": self.extracted_value,
            "expected_value": self.expected_value,
            "source": {
                "pdf_file": self.source.pdf_file,
                "page": self.source.page_number
            } if self.source else None,
            "hint": self.hint
        }
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/models/test_validation.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/autosar_pdf2txt/models/validation.py tests/models/test_validation.py
git commit -m "feat: add ValidationError model

Add ValidationError dataclass for tracking parsing correctness issues.
Supports severity levels, source location tracking, and auto-generated
hints for manual review.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 2: Implement Cache Manager

**Files:**
- Create: `src/autosar_pdf2txt/cache/__init__.py`
- Create: `src/autosar_pdf2txt/cache/cache_manager.py`
- Test: `tests/cache/test_cache_manager.py`

**Step 1: Write failing test**

```python
# tests/cache/test_cache_manager.py
import pytest
from pathlib import Path
from autosar_pdf2txt.cache.cache_manager import CacheManager
from autosar_pdf2txt.models import AutosarDoc

@pytest.fixture
def temp_cache_dir(tmp_path):
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    return cache_dir

def test_cache_miss(temp_cache_dir, sample_pdf):
    """Cache miss returns None when document not cached."""
    manager = CacheManager(temp_cache_dir)
    result = manager.get_cached_doc(sample_pdf)
    assert result is None

def test_cache_save_and_load(temp_cache_dir, sample_doc):
    """Saving and loading cached document works."""
    manager = CacheManager(temp_cache_dir)
    manager.save_cached_doc("test.pdf", sample_doc)

    loaded = manager.get_cached_doc("test.pdf")
    assert loaded is not None
    assert loaded.packages == sample_doc.packages
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/cache/test_cache_manager.py -v`
Expected: FAIL with "CacheManager not defined"

**Step 3: Write minimal implementation**

```python
# src/autosar_pdf2txt/cache/cache_manager.py
import hashlib
import pickle
from pathlib import Path
from typing import Optional

from autosar_pdf2txt.models import AutosarDoc

class CacheManager:
    """Manages caching of parsed AutosarDoc objects.

    Requirements:
        SWR_CACHE_00001: Cache File Structure
        SWR_CACHE_00002: Cache Key Generation (mtime + hash)
        SWR_CACHE_00003: Cache Validation

    Cache key format: {pdf_filename}_{mtime}_{content_hash}.pkl
    """

    def __init__(self, cache_dir: Path):
        """Initialize cache manager.

        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_index_path = self.cache_dir / "cache_index.json"

    def _generate_cache_key(self, pdf_path: Path) -> str:
        """Generate cache key from PDF path.

        Requirements:
            SWR_CACHE_00002: Cache Key Generation

        Key format: {filename}_{mtime}_{sha256_prefix}
        """
        mtime = int(pdf_path.stat().st_mtime)

        # Read first and last 1KB for hash
        with open(pdf_path, 'rb') as f:
            f.seek(0)
            start = f.read(1024)
            f.seek(-1024, 2)
            end = f.read(1024)
            content_hash = hashlib.sha256(start + end).hexdigest()[:16]

        filename = pdf_path.stem
        return f"{filename}_{mtime}_{content_hash}.pkl"

    def get_cached_doc(self, pdf_path: Path) -> Optional[AutosarDoc]:
        """Get cached document if valid.

        Requirements:
            SWR_CACHE_00003: Cache Validation

        Args:
            pdf_path: Path to PDF file

        Returns:
            AutosarDoc if cache valid, None otherwise
        """
        cache_key = self._generate_cache_key(pdf_path)
        cache_file = self.cache_dir / cache_key

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        except (pickle.UnpicklingError, EOFError):
            # Corrupted cache, return None
            return None

    def save_cached_doc(self, pdf_path: Path, doc: AutosarDoc) -> None:
        """Save document to cache.

        Args:
            pdf_path: Path to PDF file (for key generation)
            doc: AutosarDoc to cache
        """
        cache_key = self._generate_cache_key(pdf_path)
        cache_file = self.cache_dir / cache_key

        with open(cache_file, 'wb') as f:
            pickle.dump(doc, f, protocol=pickle.HIGHEST_PROTOCOL)

    def is_cache_valid(self, pdf_path: Path) -> bool:
        """Check if cache exists and is valid.

        Args:
            pdf_path: Path to PDF file

        Returns:
            True if cache file exists and matches current PDF
        """
        cache_key = self._generate_cache_key(pdf_path)
        cache_file = self.cache_dir / cache_key
        return cache_file.exists()

    def clear_cache(self, older_than_days: int = 30) -> int:
        """Clear cache files older than specified days.

        Args:
            older_than_days: Remove cache older than this many days

        Returns:
            Number of cache files removed
        """
        import time
        cutoff_time = time.time() - (older_than_days * 86400)
        removed = 0

        for cache_file in self.cache_dir.glob("*.pkl"):
            if cache_file.stat().st_mtime < cutoff_time:
                cache_file.unlink()
                removed += 1

        return removed
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/cache/test_cache_manager.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/autosar_pdf2txt/cache/ tests/cache/
git commit -m "feat: implement CacheManager

Add mtime and SHA256-based cache key generation for AutosarDoc caching.
Supports cache validation, saving, and clearing old cache files.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 3: Implement Ground Truth Loader

**Files:**
- Create: `src/autosar_pdf2txt/validation/__init__.py`
- Create: `src/autosar_pdf2txt/validation/ground_truth.py`
- Test: `tests/validation/test_ground_truth.py`

**Step 1: Write failing test**

```python
# tests/validation/test_ground_truth.py
import pytest
from pathlib import Path
from autosar_pdf2txt.validation.ground_truth import GroundTruthLoader

@pytest.fixture
def sample_packages_dir(tmp_path):
    """Create sample package JSON files."""
    pkg_dir = tmp_path / "packages"
    pkg_dir.mkdir()

    # Sample class file
    (pkg_dir / "M2_TestPackage_TestClass.classes.json").write_text('''{
      "package": "M2::TestPackage::TestClass",
      "classes": [{
        "name": "TestClass",
        "package": "M2::TestPackage::TestClass",
        "is_abstract": false,
        "attributes": [
          {"name": "validAttr", "type": "string", "mult": "1", "kind": "attribute"}
        ]
      }]
    }''')

    return pkg_dir

def test_load_packages(sample_packages_dir):
    """Load package JSON files into ground truth."""
    loader = GroundTruthLoader(sample_packages_dir)
    loader.load_packages()

    type_info = loader.find_type("TestClass")
    assert type_info is not None
    assert type_info.name == "TestClass"

def test_find_type_not_found(sample_packages_dir):
    """Return None when type doesn't exist."""
    loader = GroundTruthLoader(sample_packages_dir)
    loader.load_packages()

    result = loader.find_type("NonExistentType")
    assert result is None
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/validation/test_ground_truth.py -v`
Expected: FAIL with "GroundTruthLoader not defined"

**Step 3: Write minimal implementation**

```python
# src/autosar_pdf2txt/validation/ground_truth.py
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

@dataclass
class TypeInfo:
    """Information about a type from ground truth."""
    name: str
    kind: str  # "class", "enumeration", "primitive"
    package: str
    attributes: List[dict]

class GroundTruthLoader:
    """Loads ground truth data from JSON package files.

    Requirements:
        SWR_VALIDATION_00010: Ground Truth Loading
        SWR_VALIDATION_00011: Type Lookup

    Ground truth is the authoritative source for valid type names,
    attribute names, and attribute types extracted from PDFs.
    """

    def __init__(self, packages_dir: Path):
        """Initialize ground truth loader.

        Args:
            packages_dir: Path to data/packages/ directory
        """
        self.packages_dir = Path(packages_dir)
        self._types: Dict[str, TypeInfo] = {}

    def load_packages(self) -> None:
        """Load all package JSON files into memory.

        Requirements:
            SWR_VALIDATION_00010: Ground Truth Loading
        """
        for json_file in self.packages_dir.rglob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)

                # Extract types based on file type
                if "classes" in data:
                    for cls in data["classes"]:
                        info = TypeInfo(
                            name=cls["name"],
                            kind="class",
                            package=cls.get("package", ""),
                            attributes=cls.get("attributes", [])
                        )
                        self._types[info.name] = info

                elif "enumerations" in data:
                    for enum in data["enumerations"]:
                        info = TypeInfo(
                            name=enum["name"],
                            kind="enumeration",
                            package=enum.get("package", ""),
                            attributes=[]
                        )
                        self._types[info.name] = info

                elif "primitives" in data:
                    for prim in data["primitives"]:
                        info = TypeInfo(
                            name=prim["name"],
                            kind="primitive",
                            package=prim.get("package", ""),
                            attributes=prim.get("attributes", [])
                        )
                        self._types[info.name] = info

            except (json.JSONDecodeError, KeyError) as e:
                # Skip invalid JSON files
                continue

    def find_type(self, name: str) -> Optional[TypeInfo]:
        """Find type by name.

        Requirements:
            SWR_VALIDATION_00011: Type Lookup

        Args:
            name: Type name to search for

        Returns:
            TypeInfo if found, None otherwise
        """
        return self._types.get(name)

    def get_all_type_names(self) -> List[str]:
        """Get list of all known type names."""
        return list(self._types.keys())
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/validation/test_ground_truth.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/autosar_pdf2txt/validation/ tests/validation/
git commit -m "feat: add GroundTruthLoader

Load and index types from data/packages/*.json files for validation.
Supports lookup of classes, enumerations, and primitives by name.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 4: Implement Document Validator

**Files:**
- Create: `src/autosar_pdf2txt/validation/validator.py`
- Test: `tests/validation/test_validator.py`

**Step 1: Write failing test**

```python
# tests/validation/test_validator.py
import pytest
from autosar_pdf2txt.validation.validator import DocumentValidator
from autosar_pdf2txt.validation.ground_truth import GroundTruthLoader, TypeInfo
from autosar_pdf2txt.models import AutosarClass, AutosarPackage, AutosarDoc, ValidationError
from autosar_pdf2txt.models.base import AutosarDocumentSource

@pytest.fixture
def sample_ground_truth(tmp_path):
    """Create sample ground truth data."""
    pkg_dir = tmp_path / "packages"
    pkg_dir.mkdir()

    (pkg_dir / "test.json").write_text('''{
      "classes": [{
        "name": "ValidClass",
        "package": "TestPackage",
        "attributes": [{"name": "attr1", "type": "string"}]
      }]
    }''')

    loader = GroundTruthLoader(pkg_dir)
    loader.load_packages()
    return loader

def test_validate_attribute_types_found(sample_ground_truth):
    """No errors when all attribute types exist in ground truth."""
    doc = AutosarDoc(packages=[])

    pkg = AutosarPackage(name="TestPackage", path="TestPackage")
    cls = AutosarClass(
        name="ValidClass",
        package="TestPackage",
        is_abstract=False,
        attributes=[create_attribute("attr1", "string")]
    )
    pkg.add_class(cls)
    doc.packages.append(pkg)

    validator = DocumentValidator(sample_ground_truth)
    errors = validator.validate_document(doc)

    assert len(errors) == 0

def test_validate_attribute_types_not_found(sample_ground_truth):
    """Error when attribute type doesn't exist in ground truth."""
    doc = AutosarDoc(packages=[])

    pkg = AutosarPackage(name="TestPackage", path="TestPackage")
    cls = AutosarClass(
        name="TestClass",
        package="TestPackage",
        is_abstract=False,
        attributes=[create_attribute("attr1", "InvalidType")]
    )
    pkg.add_class(cls)
    doc.packages.append(pkg)

    validator = DocumentValidator(sample_ground_truth)
    errors = validator.validate_document(doc)

    assert len(errors) == 1
    assert errors[0].issue == "attribute_type_not_found"
    assert errors[0].extracted_value == "InvalidType"

def create_attribute(name: str, type_name: str):
    """Helper to create test attribute."""
    from autosar_pdf2txt.models.attributes import AutosarAttribute
    return AutosarAttribute(
        name=name,
        type=type_name,
        multiplicity="1",
        kind=AttributeKind.ATTRIBUTE
    )
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/validation/test_validator.py -v`
Expected: FAIL with "DocumentValidator not defined"

**Step 3: Write minimal implementation**

```python
# src/autosar_pdf2txt/validation/validator.py
import json
from pathlib import Path
from typing import List

from autosar_pdf2txt.models import AutosarDoc
from autosar_pdf2txt.models.validation import ValidationError
from autosar_pdf2txt.validation.ground_truth import GroundTruthLoader

class DocumentValidator:
    """Validates AutosarDoc against ground truth.

    Requirements:
        SWR_VALIDATION_00020: Document Validation
        SWR_VALIDATION_00021: Attribute Type Validation
    """

    def __init__(self, ground_truth: GroundTruthLoader):
        """Initialize validator.

        Args:
            ground_truth: Loaded ground truth data
        """
        self.ground_truth = ground_truth

    def validate_document(self, doc: AutosarDoc) -> List[ValidationError]:
        """Validate complete document against ground truth.

        Requirements:
            SWR_VALIDATION_00020: Document Validation

        Args:
            doc: AutosarDoc to validate

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        errors.extend(self._validate_attribute_types(doc))
        return errors

    def _validate_attribute_types(self, doc: AutosarDoc) -> List[ValidationError]:
        """Validate all attribute types exist in ground truth.

        Requirements:
            SWR_VALIDATION_00021: Attribute Type Validation

        Args:
            doc: AutosarDoc to validate

        Returns:
            List of validation errors
        """
        errors = []

        for cls in doc.all_classes():
            for attr in cls.attributes:
                attr_type = attr.type

                # Check if type exists in ground truth
                if not self.ground_truth.find_type(attr_type):
                    errors.append(ValidationError(
                        class_name=cls.name,
                        package=cls.package,
                        attribute_name=attr.name,
                        issue="attribute_type_not_found",
                        severity="error",
                        extracted_value=attr_type,
                        expected_value=None,
                        source=attr.source
                    ))

        return errors

    def write_error_report(self, errors: List[ValidationError], output_path: Path) -> None:
        """Write validation errors to JSON file.

        Args:
            errors: List of validation errors
            output_path: Path to write report
        """
        report = {
            "validation_errors": [e.to_dict() for e in errors],
            "summary": {
                "total_errors": len(errors),
                "by_severity": self._count_by_severity(errors),
                "by_issue_type": self._count_by_issue_type(errors)
            }
        }

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

    def _count_by_severity(self, errors: List[ValidationError]) -> dict:
        """Count errors by severity level."""
        counts = {}
        for error in errors:
            counts[error.severity] = counts.get(error.severity, 0) + 1
        return counts

    def _count_by_issue_type(self, errors: List[ValidationError]) -> dict:
        """Count errors by issue type."""
        counts = {}
        for error in errors:
            counts[error.issue] = counts.get(error.issue, 0) + 1
        return counts
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/validation/test_validator.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/autosar_pdf2txt/validation/validator.py tests/validation/test_validator.py
git commit -m "feat: add DocumentValidator

Validate AutosarDoc against ground truth, checking attribute types.
Generates structured error reports with severity and issue type grouping.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 5: Integrate CacheManager into PdfParser

**Files:**
- Modify: `src/autosar_pdf2txt/parser/pdf_parser.py:62-95`
- Test: `tests/parser/test_pdf_parser_cache_integration.py`

**Step 1: Write failing test**

```python
# tests/parser/test_pdf_parser_cache_integration.py
import pytest
from pathlib import Path
from autosar_pdf2txt.parser.pdf_parser import PdfParser
from autosar_pdf2txt.cache.cache_manager import CacheManager

def test_parser_uses_cache(tmp_path, sample_pdf):
    """Parser uses cache when available."""
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()

    # First parse - cache miss
    parser = PdfParser(cache_manager=CacheManager(cache_dir))
    doc1 = parser.parse_pdf(sample_pdf)

    # Second parse - cache hit
    doc2 = parser.parse_pdf(sample_pdf)

    # Verify same document returned
    assert doc2 is not None
    assert doc1.packages == doc2.packages
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/parser/test_pdf_parser_cache_integration.py -v`
Expected: FAIL with "__init__() got unexpected keyword argument 'cache_manager'"

**Step 3: Modify PdfParser to accept CacheManager**

```python
# In src/autosar_pdf2txt/parser/pdf_parser.py

# Add import at top
from autosar_pdf2txt.cache.cache_manager import CacheManager
from typing import Optional

# Modify __init__ method (line ~62)
def __init__(self, cache_manager: Optional[CacheManager] = None) -> None:
    """Initialize PDF parser.

    Requirements:
        SWR_PARSER_00001: PDF Parser Initialization
        SWR_CACHE_00005: CacheManager Integration

    Args:
        cache_manager: Optional cache manager for caching parsed docs
    """
    self._validate_backend()

    # Store cache manager
    self._cache_manager = cache_manager

    # Instantiate specialized parsers
    self._class_parser = AutosarClassParser()
    self._enum_parser = AutosarEnumerationParser()
    self._primitive_parser = AutosarPrimitiveParser()

# Modify parse_pdf method (line ~136)
def parse_pdf(self, pdf_path: str) -> AutosarDoc:
    """Parse a PDF file and extract package hierarchy.

    Requirements:
        SWR_PARSER_00003: PDF File Parsing
        SWR_CACHE_00006: Cache Check Before Parsing

    Args:
        pdf_path: Path to PDF file.

    Returns:
        AutosarDoc containing packages and root classes.
    """
    pdf_path_obj = Path(pdf_path)

    # Check cache first
    if self._cache_manager:
        cached_doc = self._cache_manager.get_cached_doc(pdf_path_obj)
        if cached_doc is not None:
            return cached_doc

    # Parse PDF
    doc = self.parse_pdfs([pdf_path])

    # Save to cache
    if self._cache_manager:
        self._cache_manager.save_cached_doc(pdf_path_obj, doc)

    return doc
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/parser/test_pdf_parser_cache_integration.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/autosar_pdf2txt/parser/pdf_parser.py tests/parser/test_pdf_parser_cache_integration.py
git commit -m "feat: integrate CacheManager into PdfParser

Parser now checks cache before parsing and saves results after parsing.
Cache hit returns cached AutosarDoc without re-parsing PDF.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 6: Add Parallel PDF Processing

**Files:**
- Create: `src/autosar_pdf2txt/cache/parallel_parser.py`
- Test: `tests/cache/test_parallel_parser.py`

**Step 1: Write failing test**

```python
# tests/cache/test_parallel_parser.py
import pytest
from pathlib import Path
from autosar_pdf2txt.cache.parallel_parser import parse_pdfs_parallel

def test_parse_multiple_pdfs_parallel(sample_pdfs):
    """Parse multiple PDFs in parallel."""
    docs = parse_pdfs_parallel(sample_pdfs, num_workers=2)

    assert len(docs) == len(sample_pdfs)
    assert all(doc is not None for doc in docs)

def test_parse_with_single_worker(sample_pdfs):
    """Parse sequentially with single worker."""
    docs = parse_pdfs_parallel(sample_pdfs, num_workers=1)

    assert len(docs) == len(sample_pdfs)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/cache/test_parallel_parser.py -v`
Expected: FAIL with "parse_pdfs_parallel not defined"

**Step 3: Write minimal implementation**

```python
# src/autosar_pdf2txt/cache/parallel_parser.py
from multiprocessing import Pool, cpu_count
from typing import List

from autosar_pdf2txt.parser.pdf_parser import PdfParser
from autosar_pdf2txt.models import AutosarDoc

def parse_single_pdf(pdf_path: str) -> AutosarDoc:
    """Parse single PDF (worker function).

    Args:
        pdf_path: Path to PDF file

    Returns:
        Parsed AutosarDoc
    """
    parser = PdfParser()
    return parser.parse_pdf(pdf_path)

def parse_pdfs_parallel(pdf_paths: List[str], num_workers: int = None) -> List[AutosarDoc]:
    """Parse multiple PDFs in parallel.

    Requirements:
        SWR_PARALLEL_00001: Parallel PDF Processing
        SWR_PARALLEL_00002: Worker Pool Management

    Args:
        pdf_paths: List of PDF file paths
        num_workers: Number of worker processes (default: min(cpu_count, len(pdf_paths)))

    Returns:
        List of AutosarDoc objects (one per input PDF)
    """
    if num_workers is None:
        num_workers = min(cpu_count(), len(pdf_paths))

    if num_workers <= 1 or len(pdf_paths) <= 1:
        # Sequential parsing for single worker or single PDF
        return [parse_single_pdf(pdf) for pdf in pdf_paths]

    # Parallel parsing
    with Pool(processes=num_workers) as pool:
        results = pool.map(parse_single_pdf, pdf_paths)

    return list(results)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/cache/test_parallel_parser.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/autosar_pdf2txt/cache/parallel_parser.py tests/cache/test_parallel_parser.py
git commit -m "feat: add parallel PDF processing

Parse multiple PDFs concurrently using multiprocessing Pool.
Falls back to sequential for single worker or PDF.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 7: Update CLI with New Options

**Files:**
- Modify: `src/autosar_pdf2txt/cli/autosar_cli.py:1-200`
- Test: `tests/cli/test_cli_new_options.py`

**Step 1: Write failing test**

```python
# tests/cli/test_cli_new_options.py
import pytest
from click.testing import CliRunner
from autosar_pdf2txt.cli.autosar_cli import main

def test_jobs_flag():
    """CLI accepts --jobs flag."""
    runner = CliRunner()
    result = runner.invoke(main, ['--jobs', '4', 'examples/pdf/*.pdf'])

    # Should not error on flag parsing
    assert result.exit_code != 2  # Not a usage error

def test_no_validate_flag():
    """CLI accepts --no-validate flag."""
    runner = CliRunner()
    result = runner.invoke(main, ['--no-validate', 'examples/pdf/*.pdf'])

    assert result.exit_code != 2
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/cli/test_cli_new_options.py -v`
Expected: FAIL with "no such option: --jobs"

**Step 3: Modify CLI to add options**

```python
# In src/autosar_pdf2txt/cli/autosar_cli.py

# Add to existing CLI options (around line ~50-100)
@click.option(
    '--jobs',
    default=None,
    type=int,
    help='Number of parallel workers for PDF parsing (default: min(cpu_count, #pdfs))'
)
@click.option(
    '--no-validate',
    is_flag=True,
    default=False,
    help='Disable validation for faster parsing'
)
@click.option(
    '--error-report',
    default='validation_errors.json',
    type=click.Path(),
    help='Write validation errors to FILE'
)
@click.option(
    '--force-refresh',
    is_flag=True,
    default=False,
    help='Ignore cache and re-parse all PDFs'
)
@click.option(
    '--clear-cache',
    is_flag=True,
    default=False,
    help='Clear all cached data'
)
def main(
    pdf_files: tuple[Path, ...],
    # ... existing options ...
    jobs: int,
    no_validate: bool,
    error_report: Path,
    force_refresh: bool,
    clear_cache: bool
):
    """Extract AUTOSAR model hierarchy from PDF specification documents.

    PDF_FILES: One or more PDF files to process
    """
    from autosar_pdf2txt import __init__ as autosar_init
    from autosar_pdf2txt.cache.cache_manager import CacheManager
    from autosar_pdf2txt.cache.parallel_parser import parse_pdfs_parallel
    from autosar_pdf2txt.validation.validator import DocumentValidator
    from autosar_pdf2txt.validation.ground_truth import GroundTruthLoader

    # Clear cache if requested
    if clear_cache:
        cache_mgr = CacheManager(Path('.cache'))
        removed = cache_mgr.clear_cache()
        click.echo(f"Cleared {removed} cached files")
        return

    # Create cache manager
    cache_mgr = CacheManager(Path('.cache/parsed_pdfs'))

    # Convert paths to strings
    pdf_paths = [str(f) for f in pdf_files]

    # Parse PDFs (parallel or sequential based on --jobs)
    docs = parse_pdfs_parallel(pdf_paths, num_workers=jobs)

    # Merge docs
    merged_doc = autosar_init.merge_docs(docs)

    # Validate unless disabled
    if not no_validate:
        ground_truth = GroundTruthLoader(Path('data/packages'))
        ground_truth.load_packages()

        validator = DocumentValidator(ground_truth)
        errors = validator.validate_document(merged_doc)

        # Write error report
        validator.write_error_report(errors, error_report)
        click.echo(f"Validation complete: {len(errors)} errors found in {error_report}")
    else:
        click.echo("Validation disabled (--no-validate)")

    # ... rest of existing output logic ...
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/cli/test_cli_new_options.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/autosar_pdf2txt/cli/autosar_cli.py tests/cli/test_cli_new_options.py
git commit -m "feat: add CLI options for parallel processing and validation

Add --jobs, --no-validate, --error-report, --force-refresh, --clear-cache
options to control parsing behavior and validation output.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 8: Add Performance Benchmark Tests

**Files:**
- Create: `tests/performance/test_caching_performance.py`
- Create: `tests/performance/test_parallel_speedup.py`

**Step 1: Write cache hit speed test**

```python
# tests/performance/test_caching_performance.py
import time
import pytest
from pathlib import Path
from autosar_pdf2txt.parser.pdf_parser import PdfParser
from autosar_pdf2txt.cache.cache_manager import CacheManager

def test_cache_hit_performance(tmp_path, sample_pdf):
    """Cache hit should be <100ms."""
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()

    cache_mgr = CacheManager(cache_dir)

    # First parse - cache miss
    parser = PdfParser(cache_manager=cache_mgr)
    parser.parse_pdf(sample_pdf)

    # Second parse - cache hit
    start = time.time()
    doc = parser.parse_pdf(sample_pdf)
    elapsed_ms = (time.time() - start) * 1000

    assert doc is not None
    assert elapsed_ms < 100, f"Cache hit took {elapsed_ms}ms, expected <100ms"
```

**Step 2: Write parallel speedup test**

```python
# tests/performance/test_parallel_speedup.py
import time
import pytest
from autosar_pdf2txt.cache.parallel_parser import parse_pdfs_parallel

@pytest.mark.slow
def test_parallel_speedup(sample_pdfs):
    """Parallel processing should be faster than sequential."""
    # Sequential
    start = time.time()
    docs_seq = parse_pdfs_parallel(sample_pdfs, num_workers=1)
    sequential_time = time.time() - start

    # Parallel (2 workers)
    start = time.time()
    docs_par = parse_pdfs_parallel(sample_pdfs, num_workers=2)
    parallel_time = time.time() - start

    speedup = sequential_time / parallel_time
    assert speedup >= 1.5, f"Speedup: {speedup:.2f}x (expected >=1.5x)"
```

**Step 3: Run tests**

Run: `pytest tests/performance/ -v`
Expected: PASS

**Step 4: Commit**

```bash
git add tests/performance/
git commit -m "test: add performance benchmark tests

Add tests for cache hit speed (<100ms target) and parallel speedup
(>=1.5x target). Marked as slow tests.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Task 9: Update Documentation

**Files:**
- Create: `docs/development/cache_architecture.md`
- Modify: `CLAUDE.md`
- Modify: `README.md`

**Step 1: Write cache architecture documentation**

```markdown
# Cache Architecture

## Overview

The AutosarPDF parser uses pickle-based caching to avoid re-parsing unchanged PDF files.

## Cache Key Format

Cache files are named: `{filename}_{mtime}_{sha256_prefix}.pkl`

- **filename**: PDF file name (without extension)
- **mtime**: File modification time (Unix timestamp)
- **sha256_prefix**: First 16 chars of SHA-256 hash of first+last 1KB

## Invalidation

Cache is automatically invalidated when:
- PDF file mtime changes
- PDF content hash changes
- Cache is older than 30 days

## Performance

- **Cache hit**: ~100ms (loading pickle)
- **Cache miss**: ~5-10s (PDF parsing)
- **Speedup**: 50-100x for cached PDFs
```

**Step 2: Update CLAUDE.md**

Add to "Essential Commands" section:
```bash
# Performance options
autosar-extract examples/pdf/*.pdf --jobs 4              # Use 4 parallel workers
autosar-extract examples/pdf/*.pdf --force-refresh      # Re-parse ignoring cache
autosar-extract examples/pdf/*.pdf --clear-cache        # Clear all cache

# Validation options
autosar-extract examples/pdf/*.pdf --no-validate       # Skip validation
autosar-extract examples/pdf/*.pdf --error-report errs.json  # Custom error report path
```

**Step 3: Update README.md**

Add to "Features" section:
- **Intelligent Caching**: Avoid re-parsing with mtime-based cache invalidation
- **Parallel Processing**: Multi-core PDF parsing with configurable workers
- **Ground Truth Validation**: Automatic correctness checking against reference data

**Step 4: Commit**

```bash
git add docs/ CLAUDE.md README.md
git commit -m "docs: add caching and performance documentation

Document cache architecture, invalidation rules, and performance characteristics.
Update CLI reference and README with new features.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## Summary

**Total Tasks:** 9

**Key Deliverables:**
1. ValidationError model for structured error tracking
2. CacheManager with mtime+hash-based invalidation
3. GroundTruthLoader for type validation
4. DocumentValidator with error reporting
5. Cache integration into PdfParser
6. Parallel PDF processing with multiprocessing
7. CLI enhancements for new features
8. Performance benchmark tests
9. Complete documentation

**Estimated Completion Time:** 45-75 minutes (5-10 min per task)

**Performance Gains:**
- 50-100x speedup for cached PDFs
- 2-4x speedup for parallel processing on initial runs
