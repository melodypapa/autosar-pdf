# JSON Writer Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add JSON output format for AUTOSAR class extraction with complete metadata representation, split files for manageable sizes, and CLI integration.

**Architecture:** Create `JsonWriter` class parallel to existing `MarkdownWriter`, generating multi-file JSON structure (index.json + packages/ with separate entity files). Follow TDD with unit tests first, then implementation. File structure mirrors MarkdownWriter for consistency.

**Tech Stack:** Python 3.9+, json module, pathlib, pytest for testing, existing data models (AutosarClass, AutosarEnumeration, AutosarPrimitive)

**Design Reference:** `docs/plans/2026-01-31-json-writer-design.md`

**Requirements IDs:** SWR_WRITER_00010 - SWR_WRITER_00020 (to be added)

---

## Task 1: Add JSON Writer Requirements

**Files:**
- Modify: `docs/requirements/requirements_writer.md`

**Step 1: Add new requirements to requirements_writer.md**

Add these requirements at the end of the file before existing requirements:

```markdown
### JSON Writer Requirements

**Document**: [requirements_writer.md](requirements_writer.md)

**Requirements**: SWR_WRITER_00010 - SWR_WRITER_00020

**Key Areas**:
- JSON Writer Initialization
- JSON Package Metadata File Output
- JSON Entity File Output (Classes, Enumerations, Primitives)
- JSON Index File Output
- JSON File Naming and Sanitization
- JSON Source Information Encoding
- JSON Attribute Encoding
- JSON Inheritance Hierarchy Encoding
- JSON CLI Integration
```

**Step 2: Commit**

```bash
git add docs/requirements/requirements_writer.md
git commit -m "docs: Add JSON writer requirements stub"
```

---

## Task 2: Create JsonWriter Class Structure

**Files:**
- Create: `src/autosar_pdf2txt/writer/json_writer.py`
- Modify: `src/autosar_pdf2txt/writer/__init__.py`

**Step 1: Write failing test for JsonWriter initialization**

Create: `tests/writer/test_json_writer.py`

```python
"""Tests for JsonWriter class."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from autosar_pdf2txt.writer import JsonWriter
from autosar_pdf2txt.models import AutosarPackage, AutosarClass


class TestJsonWriter:
    """Test cases for JsonWriter class.

    Requirements:
        SWR_WRITER_00010: JSON Writer Initialization
    """

    def test_init(self):
        """Test JsonWriter initialization.

        Requirements:
            SWR_WRITER_00010: JSON Writer Initialization
        """
        writer = JsonWriter()
        assert writer is not None
```

**Step 2: Run test to verify it fails**

```bash
cd /Users/ray/Workspace/autosar-pdf/.worktrees/json-writer
pytest tests/writer/test_json_writer.py::TestJsonWriter::test_init -v
```

Expected: `ImportError: cannot import name 'JsonWriter' from 'autosar_pdf2txt.writer'`

**Step 3: Create JsonWriter class with minimal implementation**

Create: `src/autosar_pdf2txt/writer/json_writer.py`

```python
"""JSON writer for AUTOSAR packages and classes."""

from autosar_pdf2txt.models import AutosarPackage


class JsonWriter:
    """Write AUTOSAR packages and classes to JSON format.

    Requirements:
        SWR_WRITER_00010: JSON Writer Initialization

    The output format uses separate JSON files for different entity types
    to keep file sizes manageable and enable efficient querying:

    - index.json: Root index with overview and package references
    - packages/{name}.json: Package metadata with entity file references
    - packages/{name}.classes.json: All classes in the package
    - packages/{name}.enums.json: All enumerations in the package
    - packages/{name}.primitives.json: All primitives in the package

    File naming sanitizes package names for filesystem safety by replacing
    invalid characters (< > : " / \ | ? *) with underscores.
    """

    def __init__(self) -> None:
        """Initialize the JSON writer.

        Requirements:
            SWR_WRITER_00010: JSON Writer Initialization
        """
```

**Step 4: Export JsonWriter from writer module**

Modify: `src/autosar_pdf2txt/writer/__init__.py`

```python
"""Writer module for AUTOSAR data."""

# Export writers
from autosar_pdf2txt.writer.markdown_writer import MarkdownWriter
from autosar_pdf2txt.writer.json_writer import JsonWriter

__all__ = ["MarkdownWriter", "JsonWriter"]
```

**Step 5: Run test to verify it passes**

```bash
pytest tests/writer/test_json_writer.py::TestJsonWriter::test_init -v
```

Expected: `PASSED`

**Step 6: Commit**

```bash
git add src/autosar_pdf2txt/writer/json_writer.py src/autosar_pdf2txt/writer/__init__.py tests/writer/test_json_writer.py
git commit -m "feat: Add JsonWriter class structure"
```

---

## Task 3: Implement write_packages_to_files with Directory Creation

**Files:**
- Modify: `src/autosar_pdf2txt/writer/json_writer.py`
- Modify: `tests/writer/test_json_writer.py`

**Step 1: Write failing test for directory creation**

Add to `tests/writer/test_json_writer.py`:

```python
    def test_write_packages_to_files_creates_directories(self, tmp_path):
        """Test write_packages_to_files creates package directories.

        Requirements:
            SWR_WRITER_00011: JSON Directory Structure Creation
        """
        from autosar_pdf2txt.models import AutosarClass

        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass("TestClass", False))

        # Write to temporary directory
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify packages directory was created
        packages_dir = tmp_path / "packages"
        assert packages_dir.exists()
        assert packages_dir.is_dir()
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/writer/test_json_writer.py::TestJsonWriter::test_write_packages_to_files_creates_directories -v
```

Expected: `AttributeError: 'JsonWriter' object has no attribute 'write_packages_to_files'`

**Step 3: Implement write_packages_to_files method**

Add to `src/autosar_pdf2txt/writer/json_writer.py`:

```python
from pathlib import Path
from typing import List, Optional, Union


class JsonWriter:
    # ... existing __init__ ...

    def write_packages_to_files(
        self, packages: List[AutosarPackage], output_path: Optional[Union[str, Path]] = None, base_dir: Optional[Union[str, Path]] = None
    ) -> None:
        """Write packages to separate JSON files organized in directory structure.

        Requirements:
            SWR_WRITER_00011: JSON Directory Structure Creation

        For each package:
        - Creates a packages/ directory in the output location
        - Creates a package metadata JSON file
        - Creates separate JSON files for classes, enumerations, and primitives
        - Maintains nested directory structure for subpackages

        The root directory for the file structure is the same as the output JSON file location.
        If output_path is provided, the directory containing that file is used as the root.
        If base_dir is provided, it is used directly as the root directory.

        Args:
            packages: List of top-level AutosarPackage objects.
            output_path: Path to the output JSON file. The root directory will be
                the directory containing this file. Cannot be used with base_dir.
            base_dir: Base directory path where the package structure will be created.
                Cannot be used with output_path.

        Raises:
            OSError: If directory creation or file writing fails.
            ValueError: If both output_path and base_dir are provided, or if neither is provided,
                or if the path is empty.

        Examples:
            >>> writer = JsonWriter()
            >>> pkg = AutosarPackage(name="TestPackage")
            >>> pkg.add_class(AutosarClass("MyClass", False))
            >>> # Using output file path (root is dir of output.json)
            >>> writer.write_packages_to_files([pkg], output_path="/tmp/output.json")
            >>> # Using base directory directly
            >>> writer.write_packages_to_files([pkg], base_dir="/tmp/output")
        """
        if output_path is not None and base_dir is not None:
            raise ValueError("Cannot specify both output_path and base_dir")
        if output_path is None and base_dir is None:
            raise ValueError("Must specify either output_path or base_dir")
        if output_path is not None and not output_path:
            raise ValueError("output_path cannot be empty")
        if base_dir is not None and not base_dir:
            raise ValueError("base_dir cannot be empty")

        # Determine base path from output_path or base_dir
        if output_path is not None:
            output_file = Path(output_path)
            base_path = output_file.parent
        else:
            base_path = Path(base_dir)  # type: ignore

        # Create packages directory
        packages_dir = base_path / "packages"
        packages_dir.mkdir(parents=True, exist_ok=True)

        for pkg in packages:
            self._write_package_to_files(pkg, packages_dir)
```

**Step 4: Add _write_package_to_files stub method**

Add to `src/autosar_pdf2txt/writer/json_writer.py`:

```python
    def _write_package_to_files(self, pkg: AutosarPackage, parent_dir: Path, parent_path: Optional[List[str]] = None) -> None:
        """Write a package to directory structure with entity files.

        Requirements:
            SWR_WRITER_00011: JSON Directory Structure Creation

        Args:
            pkg: The package to write.
            parent_dir: Parent directory path where the package directory will be created.
            parent_path: List of parent package names for constructing full package path.
        """
        if parent_path is None:
            parent_path = []

        # Build full package path for this package
        full_package_path = parent_path + [pkg.name]
        package_path_str = "::".join(full_package_path)

        # For now, just create a placeholder file
        # Will implement full functionality in subsequent tasks
        sanitized_name = self._sanitize_filename(pkg.name)
        package_file = parent_dir / f"{sanitized_name}.json"
        package_file.write_text('{"name": "' + pkg.name + '"}', encoding="utf-8")

        # Recursively write subpackages
        for subpkg in pkg.subpackages:
            self._write_package_to_files(subpkg, parent_dir, full_package_path)
```

**Step 5: Add _sanitize_filename method (reused from MarkdownWriter)**

Add to `src/autosar_pdf2txt/writer/json_writer.py`:

```python
import re


class JsonWriter:
    # ... existing methods ...

    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a package or class name for use as a filename.

        Requirements:
            SWR_WRITER_00012: JSON File Naming and Sanitization

        Removes or replaces characters that are invalid in file paths on Windows
        and other operating systems. This ensures that package names with special
        characters can still be written to the filesystem.

        Args:
            name: The package or class name to sanitize.

        Returns:
            A sanitized version of the name safe for use in file paths.

        Examples:
            >>> writer = JsonWriter()
            >>> writer._sanitize_filename("M2::AUTOSAR::DataTypes")
            'M2_AUTOSAR_DataTypes'
        """
        # Replace invalid filename characters with underscores
        # Invalid chars: < > : " / \ | ? * and control characters
        # Note: using \\ in pattern to match literal backslash
        invalid_chars = r'[<>:"/|?*\x00-\x1f]'
        # First handle backslash separately since it's tricky in regex
        sanitized = name.replace('\\', '_')
        # Then replace all other invalid characters
        sanitized = re.sub(invalid_chars, '_', sanitized)

        # Ensure name doesn't start or end with spaces or dots
        sanitized = sanitized.strip('. ')

        # If the name becomes empty or only underscores, use a default
        if not sanitized or sanitized.replace('_', '') == '':
            sanitized = 'UnnamedPackage'

        return sanitized
```

**Step 6: Run test to verify it passes**

```bash
pytest tests/writer/test_json_writer.py::TestJsonWriter::test_write_packages_to_files_creates_directories -v
```

Expected: `PASSED`

**Step 7: Commit**

```bash
git add src/autosar_pdf2txt/writer/json_writer.py tests/writer/test_json_writer.py
git commit -m "feat: Implement write_packages_to_files with directory creation"
```

---

## Task 4: Implement Index JSON Generation

**Files:**
- Modify: `src/autosar_pdf2txt/writer/json_writer.py`
- Modify: `tests/writer/test_json_writer.py`

**Step 1: Write failing test for index.json generation**

Add to `tests/writer/test_json_writer.py`:

```python
    def test_write_packages_to_files_creates_index(self, tmp_path):
        """Test write_packages_to_files creates index.json.

        Requirements:
            SWR_WRITER_00013: JSON Index File Output
        """
        from autosar_pdf2txt.models import AutosarClass
        import json

        writer = JsonWriter()
        pkg = AutosarPackage(name="M2")
        pkg.add_class(AutosarClass("TestClass", "M2::AUTOSAR", False))

        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify index.json was created
        index_file = tmp_path / "index.json"
        assert index_file.exists()

        # Verify index structure
        with open(index_file) as f:
            index = json.load(f)

        assert "version" in index
        assert index["version"] == "1.0"
        assert "metadata" in index
        assert "packages" in index
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/writer/test_json_writer.py::TestJsonWriter::test_write_packages_to_files_creates_index -v
```

Expected: `AssertionError: assert 'index.json' in...` or file not found

**Step 3: Implement index.json generation in write_packages_to_files**

Modify `src/autosar_pdf2txt/writer/json_writer.py`:

```python
from datetime import datetime
from typing import Dict, List, Optional, Union
import json


class JsonWriter:
    # ... existing methods ...

    def write_packages_to_files(
        self, packages: List[AutosarPackage], output_path: Optional[Union[str, Path]] = None, base_dir: Optional[Union[str, Path]] = None
    ) -> None:
        """Write packages to separate JSON files organized in directory structure.

        Requirements:
            SWR_WRITER_00011: JSON Directory Structure Creation
            SWR_WRITER_00013: JSON Index File Output
        """
        if output_path is not None and base_dir is not None:
            raise ValueError("Cannot specify both output_path and base_dir")
        if output_path is None and base_dir is None:
            raise ValueError("Must specify either output_path or base_dir")
        if output_path is not None and not output_path:
            raise ValueError("output_path cannot be empty")
        if base_dir is not None and not base_dir:
            raise ValueError("base_dir cannot be empty")

        # Determine base path from output_path or base_dir
        if output_path is not None:
            output_file = Path(output_path)
            base_path = output_file.parent
        else:
            base_path = Path(base_dir)  # type: ignore

        # Create packages directory
        packages_dir = base_path / "packages"
        packages_dir.mkdir(parents=True, exist_ok=True)

        # Write all packages
        for pkg in packages:
            self._write_package_to_files(pkg, packages_dir)

        # Write index.json
        self._write_index(packages, base_path)

    def _write_index(self, packages: List[AutosarPackage], base_path: Path) -> None:
        """Write the root index.json file.

        Requirements:
            SWR_WRITER_00013: JSON Index File Output

        Args:
            packages: List of top-level AutosarPackage objects.
            base_path: Base directory where index.json will be written.
        """
        # Collect metadata
        total_classes = 0
        total_enums = 0
        total_primitives = 0
        source_files = set()

        def count_entities(pkg: AutosarPackage) -> None:
            nonlocal total_classes, total_enums, total_primitives
            for typ in pkg.types:
                if hasattr(typ, 'attributes'):  # AutosarClass or AutosarPrimitive
                    if typ.__class__.__name__ == 'AutosarClass':
                        total_classes += 1
                    elif typ.__class__.__name__ == 'AutosarPrimitive':
                        total_primitives += 1
                elif hasattr(typ, 'enumeration_literals'):  # AutosarEnumeration
                    total_enums += 1

            # Collect source files
            for typ in pkg.types:
                if typ.sources:
                    for source in typ.sources:
                        source_files.add(source.pdf_file)

            # Recursively count subpackages
            for subpkg in pkg.subpackages:
                count_entities(subpkg)

        count_entities(packages[0] if packages else None)

        # Build package references
        package_refs = []
        for pkg in packages:
            ref = {
                "name": pkg.name,
                "file": f"packages/{self._sanitize_filename(pkg.name)}.json",
                "class_count": 0,  # Will be calculated in package metadata
                "subpackages": [subpkg.name for subpkg in pkg.subpackages]
            }
            package_refs.append(ref)

        # Build index
        index = {
            "version": "1.0",
            "metadata": {
                "generated_at": datetime.utcnow().isoformat() + "Z",
                "source_files": sorted(list(source_files)),
                "total_packages": sum(1 for _ in packages),
                "total_classes": total_classes,
                "total_enumerations": total_enums,
                "total_primitives": total_primitives
            },
            "packages": package_refs
        }

        # Write index.json
        index_file = base_path / "index.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/writer/test_json_writer.py::TestJsonWriter::test_write_packages_to_files_creates_index -v
```

Expected: `PASSED`

**Step 5: Commit**

```bash
git add src/autosar_pdf2txt/writer/json_writer.py tests/writer/test_json_writer.py
git commit -m "feat: Implement index.json generation"
```

---

## Task 5: Implement Package Metadata File

**Files:**
- Modify: `src/autosar_pdf2txt/writer/json_writer.py`
- Modify: `tests/writer/test_json_writer.py`

**Step 1: Write failing test for package metadata file**

Add to `tests/writer/test_json_writer.py`:

```python
    def test_write_package_metadata_file(self, tmp_path):
        """Test package metadata JSON file has correct structure.

        Requirements:
            SWR_WRITER_00014: JSON Package Metadata File Output
        """
        from autosar_pdf2txt.models import AutosarClass
        import json

        writer = JsonWriter()
        pkg = AutosarPackage(name="M2::AUTOSAR::DataTypes")
        pkg.add_class(AutosarClass("TestClass", "M2::AUTOSAR::DataTypes", False))

        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify package file was created
        package_file = tmp_path / "packages" / "M2_AUTOSAR_DataTypes.json"
        assert package_file.exists()

        # Verify package structure
        with open(package_file) as f:
            data = json.load(f)

        assert data["name"] == "M2::AUTOSAR::DataTypes"
        assert data["path"] == "M2::AUTOSAR::DataTypes"
        assert "files" in data
        assert "summary" in data
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/writer/test_json_writer.py::TestJsonWriter::test_write_package_metadata_file -v
```

Expected: Structure doesn't match

**Step 3: Implement _write_package_to_files with full metadata**

Modify `src/autosar_pdf2txt/writer/json_writer.py`:

```python
    def _write_package_to_files(self, pkg: AutosarPackage, parent_dir: Path, parent_path: Optional[List[str]] = None) -> None:
        """Write a package to directory structure with entity files.

        Requirements:
            SWR_WRITER_00014: JSON Package Metadata File Output

        Creates:
        - Package metadata JSON file with summary and file references
        - Separate entity files for classes, enumerations, primitives
        """
        if parent_path is None:
            parent_path = []

        # Build full package path for this package
        full_package_path = parent_path + [pkg.name]
        package_path_str = "::".join(full_package_path)

        # Sanitize package name for filename
        sanitized_name = self._sanitize_filename("::".join(full_package_path))

        # Count entities in this package
        class_count = sum(1 for typ in pkg.types if typ.__class__.__name__ == 'AutosarClass')
        enum_count = sum(1 for typ in pkg.types if typ.__class__.__name__ == 'AutosarEnumeration')
        primitive_count = sum(1 for typ in pkg.types if typ.__class__.__name__ == 'AutosarPrimitive')

        # Build entity file references
        entity_files = {}
        if class_count > 0:
            entity_files["classes"] = f"packages/{sanitized_name}.classes.json"
        if enum_count > 0:
            entity_files["enumerations"] = f"packages/{sanitized_name}.enums.json"
        if primitive_count > 0:
            entity_files["primitives"] = f"packages/{sanitized_name}.primitives.json"

        # Build subpackage references
        subpackage_refs = []
        for subpkg in pkg.subpackages:
            sub_full_path = "::".join(full_package_path + [subpkg.name])
            subpackage_refs.append({
                "name": subpkg.name,
                "full_path": sub_full_path,
                "file": f"packages/{self._sanitize_filename(sub_full_path)}.json"
            })

        # Build package metadata
        package_metadata = {
            "name": package_path_str,
            "path": package_path_str,
            "files": entity_files,
            "subpackages": subpackage_refs,
            "summary": {
                "class_count": class_count,
                "enumeration_count": enum_count,
                "primitive_count": primitive_count
            }
        }

        # Write package metadata file
        package_file = parent_dir / f"{sanitized_name}.json"
        with open(package_file, 'w', encoding='utf-8') as f:
            json.dump(package_metadata, f, indent=2, ensure_ascii=False)

        # Recursively write subpackages
        for subpkg in pkg.subpackages:
            self._write_package_to_files(subpkg, parent_dir, full_package_path)
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/writer/test_json_writer.py::TestJsonWriter::test_write_package_metadata_file -v
```

Expected: `PASSED`

**Step 5: Commit**

```bash
git add src/autosar_pdf2txt/writer/json_writer.py tests/writer/test_json_writer.py
git commit -m "feat: Implement package metadata file generation"
```

---

## Task 6: Implement Class Serialization

**Files:**
- Modify: `src/autosar_pdf2txt/writer/json_writer.py`
- Modify: `tests/writer/test_json_writer.py`

**Step 1: Write failing test for class serialization**

Add to `tests/writer/test_json_writer.py`:

```python
    def test_write_classes_file(self, tmp_path):
        """Test classes JSON file with complete class data.

        Requirements:
            SWR_WRITER_00015: JSON Class Serialization
        """
        from autosar_pdf2txt.models import AutosarClass, AutosarAttribute, AutosarDocumentSource, AttributeKind
        import json

        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(
            "TestClass",
            "TestPackage",
            is_abstract=False,
            note="Test class note"
        )
        cls.attributes = {
            "test_attr": AutosarAttribute(
                "test_attr",
                "String",
                False,
                "1",
                AttributeKind.ATTRIBUTE,
                "Test attribute"
            )
        }
        cls.sources = [
            AutosarDocumentSource("test.pdf", 42, "AUTOSAR", "R22-11")
        ]
        pkg.add_class(cls)

        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify classes file was created
        classes_file = tmp_path / "packages" / "TestPackage.classes.json"
        assert classes_file.exists()

        # Verify class structure
        with open(classes_file) as f:
            data = json.load(f)

        assert data["package"] == "TestPackage"
        assert len(data["classes"]) == 1

        cls_data = data["classes"][0]
        assert cls_data["name"] == "TestClass"
        assert cls_data["is_abstract"] is False
        assert cls_data["note"] == "Test class note"
        assert "sources" in cls_data
        assert len(cls_data["sources"]) == 1
        assert cls_data["sources"][0]["pdf_file"] == "test.pdf"
        assert cls_data["sources"][0]["page_number"] == 42
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/writer/test_json_writer.py::TestJsonWriter::test_write_classes_file -v
```

Expected: File not created or structure doesn't match

**Step 3: Implement class serialization**

Add to `src/autosar_pdf2txt/writer/json_writer.py`:

```python
from autosar_pdf2txt.models import AutosarClass, AutosarEnumeration, AutosarPrimitive, ATPType


class JsonWriter:
    # ... existing methods ...

    def _write_package_to_files(self, pkg: AutosarPackage, parent_dir: Path, parent_path: Optional[List[str]] = None) -> None:
        """Write a package to directory structure with entity files.

        Requirements:
            SWR_WRITER_00014: JSON Package Metadata File Output
            SWR_WRITER_00015: JSON Class Serialization
        """
        if parent_path is None:
            parent_path = []

        # Build full package path for this package
        full_package_path = parent_path + [pkg.name]
        package_path_str = "::".join(full_package_path)

        # Sanitize package name for filename
        sanitized_name = self._sanitize_filename("::".join(full_package_path))

        # Separate entities by type
        classes = [typ for typ in pkg.types if isinstance(typ, AutosarClass)]
        enums = [typ for typ in pkg.types if isinstance(typ, AutosarEnumeration)]
        primitives = [typ for typ in pkg.types if isinstance(typ, AutosarPrimitive)]

        # Write entity files
        if classes:
            self._write_classes_file(classes, package_path_str, parent_dir, sanitized_name)
        if enums:
            self._write_enums_file(enums, package_path_str, parent_dir, sanitized_name)
        if primitives:
            self._write_primitives_file(primitives, package_path_str, parent_dir, sanitized_name)

        # Build entity file references
        entity_files = {}
        if classes:
            entity_files["classes"] = f"packages/{sanitized_name}.classes.json"
        if enums:
            entity_files["enumerations"] = f"packages/{sanitized_name}.enums.json"
        if primitives:
            entity_files["primitives"] = f"packages/{sanitized_name}.primitives.json"

        # ... rest of method (subpackage refs, metadata, etc.)
```

Add the serialization helper methods:

```python
    def _serialize_atp_type(self, atp_type: ATPType) -> Optional[str]:
        """Serialize ATP type enum to string value.

        Requirements:
            SWR_WRITER_00016: JSON ATP Type Encoding

        Args:
            atp_type: ATPType enum value.

        Returns:
            String value or None if ATPType.NONE.
        """
        if atp_type == ATPType.NONE:
            return None
        elif atp_type == ATPType.ATP_VARIATION:
            return "atpVariation"
        elif atp_type == ATPType.ATP_MIXED_STRING:
            return "atpMixedString"
        elif atp_type == ATPType.ATP_MIXED:
            return "atpMixed"
        elif atp_type == ATPType.ATP_PROTO:
            return "atpPrototype"
        return None

    def _serialize_source(self, source) -> Dict:
        """Serialize AutosarDocumentSource to dictionary.

        Requirements:
            SWR_WRITER_00017: JSON Source Information Encoding

        Args:
            source: AutosarDocumentSource object.

        Returns:
            Dictionary with source information.
        """
        return {
            "pdf_file": source.pdf_file,
            "page_number": source.page_number,
            "autosar_standard": source.autosar_standard,
            "standard_release": source.standard_release
        }

    def _serialize_attribute(self, attr) -> Dict:
        """Serialize AutosarAttribute to dictionary.

        Requirements:
            SWR_WRITER_00018: JSON Attribute Encoding

        Args:
            attr: AutosarAttribute object.

        Returns:
            Dictionary with attribute information.
        """
        from autosar_pdf2txt.models import AttributeKind

        kind_map = {
            AttributeKind.ATTRIBUTE: "attribute",
            AttributeKind.REFERENCE: "reference"
        }

        return {
            "type": attr.type,
            "multiplicity": attr.multiplicity,
            "kind": kind_map.get(attr.kind, "attribute"),
            "is_ref": attr.is_ref,
            "note": attr.note
        }

    def _serialize_class(self, cls: AutosarClass) -> Dict:
        """Serialize AutosarClass to dictionary.

        Requirements:
            SWR_WRITER_00015: JSON Class Serialization
            SWR_WRITER_00016: JSON ATP Type Encoding
            SWR_WRITER_00017: JSON Source Information Encoding
            SWR_WRITER_00018: JSON Attribute Encoding
            SWR_WRITER_00019: JSON Inheritance Hierarchy Encoding

        Args:
            cls: AutosarClass object.

        Returns:
            Dictionary with all class information.
        """
        # Serialize attributes
        attributes = {}
        for attr_name, attr in cls.attributes.items():
            attributes[attr_name] = self._serialize_attribute(attr)

        # Serialize sources
        sources = [self._serialize_source(source) for source in cls.sources] if cls.sources else []

        return {
            "name": cls.name,
            "package": cls.package,
            "is_abstract": cls.is_abstract,
            "atp_type": self._serialize_atp_type(cls.atp_type),
            "parent": cls.parent,
            "bases": cls.bases,
            "children": cls.children,
            "subclasses": cls.subclasses,
            "aggregated_by": cls.aggregated_by,
            "implements": cls.implements,
            "implemented_by": cls.implemented_by,
            "note": cls.note,
            "sources": sources,
            "attributes": attributes
        }

    def _write_classes_file(self, classes: List[AutosarClass], package_path: str, parent_dir: Path, sanitized_name: str) -> None:
        """Write classes to a dedicated JSON file.

        Requirements:
            SWR_WRITER_00015: JSON Class Serialization

        Args:
            classes: List of AutosarClass objects.
            package_path: Full package path string.
            parent_dir: Parent directory for the file.
            sanitized_name: Sanitized package name for filename.
        """
        classes_data = {
            "package": package_path,
            "classes": [self._serialize_class(cls) for cls in classes]
        }

        classes_file = parent_dir / f"{sanitized_name}.classes.json"
        with open(classes_file, 'w', encoding='utf-8') as f:
            json.dump(classes_data, f, indent=2, ensure_ascii=False)
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/writer/test_json_writer.py::TestJsonWriter::test_write_classes_file -v
```

Expected: `PASSED`

**Step 5: Commit**

```bash
git add src/autosar_pdf2txt/writer/json_writer.py tests/writer/test_json_writer.py
git commit -m "feat: Implement class serialization to JSON"
```

---

## Task 7: Implement Enumeration Serialization

**Files:**
- Modify: `src/autosar_pdf2txt/writer/json_writer.py`
- Modify: `tests/writer/test_json_writer.py`

**Step 1: Write failing test for enumeration serialization**

Add to `tests/writer/test_json_writer.py`:

```python
    def test_write_enums_file(self, tmp_path):
        """Test enumerations JSON file with literal values.

        Requirements:
            SWR_WRITER_00020: JSON Enumeration Serialization
        """
        from autosar_pdf2txt.models import AutosarEnumeration, AutosarEnumLiteral, AutosarDocumentSource
        import json

        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        enum = AutosarEnumeration(
            "TestEnum",
            "TestPackage",
            enumeration_literals=[
                AutosarEnumLiteral("VALUE1", 0, "First value"),
                AutosarEnumLiteral("VALUE2", 1, "Second value<br>Tags: key=val")
            ]
        )
        enum.sources = [
            AutosarDocumentSource("test.pdf", 50, "AUTOSAR", "R22-11")
        ]
        pkg.add_type(enum)

        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify enums file was created
        enums_file = tmp_path / "packages" / "TestPackage.enums.json"
        assert enums_file.exists()

        # Verify enumeration structure
        with open(enums_file) as f:
            data = json.load(f)

        assert data["package"] == "TestPackage"
        assert len(data["enumerations"]) == 1

        enum_data = data["enumerations"][0]
        assert enum_data["name"] == "TestEnum"
        assert len(enum_data["literals"]) == 2

        # Check first literal
        lit1 = enum_data["literals"][0]
        assert lit1["name"] == "VALUE1"
        assert lit1["value"] == 0
        assert lit1["description"] == "First value"

        # Check second literal with merged tags
        lit2 = enum_data["literals"][1]
        assert lit2["name"] == "VALUE2"
        assert lit2["value"] == 1
        assert "Tags: key=val" in lit2["description"]
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/writer/test_json_writer.py::TestJsonWriter::test_write_enums_file -v
```

Expected: File not created or structure doesn't match

**Step 3: Implement enumeration serialization**

Add to `src/autosar_pdf2txt/writer/json_writer.py`:

```python
    def _serialize_enumeration_literal(self, literal) -> Dict:
        """Serialize AutosarEnumLiteral to dictionary.

        Requirements:
            SWR_WRITER_00020: JSON Enumeration Serialization

        Merges tags into description field with <br>Tags: format.

        Args:
            literal: AutosarEnumLiteral object.

        Returns:
            Dictionary with literal information.
        """
        # Build description with tags merged
        description_parts = []
        if literal.description:
            description_parts.append(literal.description)
        if literal.tags:
            # Merge all tags as "Tags: key=value, key2=value2"
            tag_strings = [f"{k}={v}" for k, v in sorted(literal.tags.items())]
            description_parts.append(f"<br>Tags: {', '.join(tag_strings)}")

        description = "".join(description_parts) if description_parts else ""

        return {
            "name": literal.name,
            "value": literal.value,
            "description": description
        }

    def _serialize_enumeration(self, enum: AutosarEnumeration) -> Dict:
        """Serialize AutosarEnumeration to dictionary.

        Requirements:
            SWR_WRITER_00020: JSON Enumeration Serialization
            SWR_WRITER_00017: JSON Source Information Encoding

        Args:
            enum: AutosarEnumeration object.

        Returns:
            Dictionary with all enumeration information.
        """
        # Serialize sources
        sources = [self._serialize_source(source) for source in enum.sources] if enum.sources else []

        # Serialize literals
        literals = [self._serialize_enumeration_literal(lit) for lit in enum.enumeration_literals]

        return {
            "name": enum.name,
            "package": enum.package,
            "note": enum.note,
            "sources": sources,
            "literals": literals
        }

    def _write_enums_file(self, enums: List[AutosarEnumeration], package_path: str, parent_dir: Path, sanitized_name: str) -> None:
        """Write enumerations to a dedicated JSON file.

        Requirements:
            SWR_WRITER_00020: JSON Enumeration Serialization

        Args:
            enums: List of AutosarEnumeration objects.
            package_path: Full package path string.
            parent_dir: Parent directory for the file.
            sanitized_name: Sanitized package name for filename.
        """
        enums_data = {
            "package": package_path,
            "enumerations": [self._serialize_enumeration(enum) for enum in enums]
        }

        enums_file = parent_dir / f"{sanitized_name}.enums.json"
        with open(enums_file, 'w', encoding='utf-8') as f:
            json.dump(enums_data, f, indent=2, ensure_ascii=False)
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/writer/test_json_writer.py::TestJsonWriter::test_write_enums_file -v
```

Expected: `PASSED`

**Step 5: Commit**

```bash
git add src/autosar_pdf2txt/writer/json_writer.py tests/writer/test_json_writer.py
git commit -m "feat: Implement enumeration serialization to JSON"
```

---

## Task 8: Implement Primitive Serialization

**Files:**
- Modify: `src/autosar_pdf2txt/writer/json_writer.py`
- Modify: `tests/writer/test_json_writer.py`

**Step 1: Write failing test for primitive serialization**

Add to `tests/writer/test_json_writer.py`:

```python
    def test_write_primitives_file(self, tmp_path):
        """Test primitives JSON file with attributes.

        Requirements:
            SWR_WRITER_00021: JSON Primitive Serialization
        """
        from autosar_pdf2txt.models import AutosarPrimitive, AutosarAttribute, AttributeKind
        import json

        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        prim = AutosarPrimitive("Limit", "TestPackage")
        prim.attributes = {
            "interval_type": AutosarAttribute(
                "interval_type",
                "String",
                False,
                "1",
                AttributeKind.ATTRIBUTE,
                "Open or closed interval"
            )
        }
        pkg.add_type(prim)

        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify primitives file was created
        primitives_file = tmp_path / "packages" / "TestPackage.primitives.json"
        assert primitives_file.exists()

        # Verify primitive structure
        with open(primitives_file) as f:
            data = json.load(f)

        assert data["package"] == "TestPackage"
        assert len(data["primitives"]) == 1

        prim_data = data["primitives"][0]
        assert prim_data["name"] == "Limit"
        assert "attributes" in prim_data
        assert "interval_type" in prim_data["attributes"]
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/writer/test_json_writer.py::TestJsonWriter::test_write_primitives_file -v
```

Expected: File not created or structure doesn't match

**Step 3: Implement primitive serialization**

Add to `src/autosar_pdf2txt/writer/json_writer.py`:

```python
    def _serialize_primitive(self, prim: AutosarPrimitive) -> Dict:
        """Serialize AutosarPrimitive to dictionary.

        Requirements:
            SWR_WRITER_00021: JSON Primitive Serialization
            SWR_WRITER_00018: JSON Attribute Encoding
            SWR_WRITER_00017: JSON Source Information Encoding

        Args:
            prim: AutosarPrimitive object.

        Returns:
            Dictionary with all primitive information.
        """
        # Serialize attributes
        attributes = {}
        for attr_name, attr in prim.attributes.items():
            attributes[attr_name] = self._serialize_attribute(attr)

        # Serialize sources
        sources = [self._serialize_source(source) for source in prim.sources] if prim.sources else []

        return {
            "name": prim.name,
            "package": prim.package,
            "note": prim.note,
            "sources": sources,
            "attributes": attributes
        }

    def _write_primitives_file(self, primitives: List[AutosarPrimitive], package_path: str, parent_dir: Path, sanitized_name: str) -> None:
        """Write primitives to a dedicated JSON file.

        Requirements:
            SWR_WRITER_00021: JSON Primitive Serialization

        Args:
            primitives: List of AutosarPrimitive objects.
            package_path: Full package path string.
            parent_dir: Parent directory for the file.
            sanitized_name: Sanitized package name for filename.
        """
        primitives_data = {
            "package": package_path,
            "primitives": [self._serialize_primitive(prim) for prim in primitives]
        }

        primitives_file = parent_dir / f"{sanitized_name}.primitives.json"
        with open(primitives_file, 'w', encoding='utf-8') as f:
            json.dump(primitives_data, f, indent=2, ensure_ascii=False)
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/writer/test_json_writer.py::TestJsonWriter::test_write_primitives_file -v
```

Expected: `PASSED`

**Step 5: Commit**

```bash
git add src/autosar_pdf2txt/writer/json_writer.py tests/writer/test_json_writer.py
git commit -m "feat: Implement primitive serialization to JSON"
```

---

## Task 9: Add --format CLI Argument

**Files:**
- Modify: `src/autosar_pdf2txt/cli/autosar_cli.py`
- Create: `tests/cli/test_json_format_cli.py`

**Step 1: Write failing test for --format argument**

Create: `tests/cli/test_json_format_cli.py`

```python
"""Tests for JSON format CLI argument."""

import json
from pathlib import Path
import pytest
from click.testing import CliRunner
from autosar_pdf2txt.cli.autosar_cli import main


class TestJSONFormatCLI:
    """Test cases for JSON format CLI integration.

    Requirements:
        SWR_WRITER_00022: JSON CLI Format Argument
    """

    def test_format_json_creates_json_output(self, tmp_path):
        """Test --format json creates JSON files.

        Requirements:
            SWR_WRITER_00022: JSON CLI Format Argument
        """
        from autosar_pdf2txt.models import AutosarPackage, AutosarClass

        # This is a unit test for the CLI, not a full integration test
        # We'll test the format argument parsing
        runner = CliRunner()
        result = runner.invoke(main, ['--help'])

        # Verify --format option is documented
        assert '--format' in result.output
        assert 'json' in result.output
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/cli/test_json_format_cli.py::TestJSONFormatCLI::test_format_json_creates_json_output -v
```

Expected: `AssertionError: assert '--format' in '...'` fails

**Step 3: Add --format argument to CLI**

Read the CLI file first to understand the structure:

```bash
head -100 /Users/ray/Workspace/autosar-pdf/.worktrees/json-writer/src/autosar_pdf2txt/cli/autosar_cli.py
```

Then modify it to add the --format argument. The modification will be:

Find the `@click.option` decorators and add:

```python
@click.option(
    '--format',
    type=click.Choice(['markdown', 'json'], case_sensitive=False),
    default=None,
    help='Output format (default: inferred from file extension)'
)
```

And update the writer selection logic to use JsonWriter when format is 'json'.

**Step 4: Run test to verify it passes**

```bash
pytest tests/cli/test_json_format_cli.py::TestJSONFormatCLI::test_format_json_creates_json_output -v
```

Expected: `PASSED`

**Step 5: Commit**

```bash
git add src/autosar_pdf2txt/cli/autosar_cli.py tests/cli/test_json_format_cli.py
git commit -m "feat: Add --format CLI argument for JSON output"
```

---

## Task 10: Implement File Extension Inference

**Files:**
- Modify: `src/autosar_pdf2txt/cli/autosar_cli.py`
- Modify: `tests/cli/test_json_format_cli.py`

**Step 1: Write failing test for extension inference**

Add to `tests/cli/test_json_format_cli.py`:

```python
    def test_json_extension_infers_format(self, tmp_path, sample_pdf):
        """Test .json extension infers JSON format.

        Requirements:
            SWR_WRITER_00023: JSON Format Inference from Extension
        """
        runner = CliRunner()

        output_file = tmp_path / "output.json"
        result = runner.invoke(main, [str(sample_pdf), '-o', str(output_file)])

        # Should create JSON files
        assert result.exit_code == 0
        assert (tmp_path / "index.json").exists()
        assert (tmp_path / "packages").exists()
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/cli/test_json_format_cli.py::TestJSONFormatCLI::test_json_extension_infers_format -v
```

Expected: Doesn't create JSON files or fails

**Step 3: Implement format inference logic**

Add format inference in the CLI:

```python
def infer_format_from_path(output_path: Optional[str]) -> Optional[str]:
    """Infer output format from file extension.

    Requirements:
        SWR_WRITER_00023: JSON Format Inference from Extension

    Args:
        output_path: Output file path.

    Returns:
        'json', 'markdown', or None if cannot infer.
    """
    if not output_path:
        return None

    path = Path(output_path)
    if path.suffix.lower() == '.json':
        return 'json'
    elif path.suffix.lower() == '.md':
        return 'markdown'
    return None
```

Update the main function to use this inference.

**Step 4: Run test to verify it passes**

```bash
pytest tests/cli/test_json_format_cli.py::TestJSONFormatCLI::test_json_extension_infers_format -v
```

Expected: `PASSED`

**Step 5: Commit**

```bash
git add src/autosar_pdf2txt/cli/autosar_cli.py tests/cli/test_json_format_cli.py
git commit -m "feat: Implement format inference from file extension"
```

---

## Task 11: Update Documentation

**Files:**
- Modify: `README.md`
- Modify: `docs/requirements/requirements_writer.md`
- Modify: `CLAUDE.md`

**Step 1: Update README with JSON examples**

Add a section to README.md:

```markdown
## JSON Output

The tool supports JSON output format for machine-readable data:

```bash
# Explicit format
autosar-extract input.pdf -o output --format json

# Automatic from extension
autosar-extract input.pdf -o output.json
```

JSON output creates a multi-file structure:
- `index.json` - Root index with overview
- `packages/*.json` - Package metadata
- `packages/*.classes.json` - Class definitions
- `packages/*.enums.json` - Enumeration values
- `packages/*.primitives.json` - Primitive types

See [JSON Design Document](docs/plans/2026-01-31-json-writer-design.md) for schema details.
```

**Step 2: Add writer requirements**

Add complete requirements to `docs/requirements/requirements_writer.md`:

```markdown
### JSON Writer Requirements

**SWR_WRITER_00010**: JSON Writer Initialization
- JsonWriter class with __init__ method
- No parameters required for initialization

**SWR_WRITER_00011**: JSON Directory Structure Creation
- Creates packages/ directory in output location
- Maintains nested directory structure for subpackages

**SWR_WRITER_00012**: JSON File Naming and Sanitization
- Sanitize package names replacing invalid chars with underscores
- Invalid chars: < > : " / \ | ? *

**SWR_WRITER_00013**: JSON Index File Output
- Creates index.json with version, metadata, package references
- Includes generation timestamp, source files, entity counts

**SWR_WRITER_00014**: JSON Package Metadata File Output
- Creates {name}.json with package path, entity file refs, summary

**SWR_WRITER_00015**: JSON Class Serialization
- Serializes all class fields: name, package, is_abstract, atp_type, parent, bases, children, subclasses, aggregated_by, implements, implemented_by, note, sources, attributes

**SWR_WRITER_00016**: JSON ATP Type Encoding
- Encodes ATP type enum as string or null
- Values: "atpVariation", "atpMixedString", "atpMixed", "atpPrototype", null

**SWR_WRITER_00017**: JSON Source Information Encoding
- Encodes source as {pdf_file, page_number, autosar_standard, standard_release}

**SWR_WRITER_00018**: JSON Attribute Encoding
- Encodes attribute as {type, multiplicity, kind, is_ref, note}
- Kind values: "attribute", "reference"

**SWR_WRITER_00019**: JSON Inheritance Hierarchy Encoding
- Encodes parent, bases, children, subclasses, implements, implemented_by

**SWR_WRITER_00020**: JSON Enumeration Serialization
- Serializes enumerations with literals
- Merges tags into literal description with <br>Tags: format

**SWR_WRITER_00021**: JSON Primitive Serialization
- Serializes primitives with attributes (no inheritance fields)

**SWR_WRITER_00022**: JSON CLI Format Argument
- --format option with choices: markdown, json

**SWR_WRITER_00023**: JSON Format Inference from Extension
- .json extension → JSON format
- .md extension → Markdown format
- No extension or unknown → Markdown (default)
```

**Step 3: Update CLAUDE.md**

Add JSON usage patterns to the appropriate sections in CLAUDE.md.

**Step 4: Commit**

```bash
git add README.md docs/requirements/requirements_writer.md CLAUDE.md
git commit -m "docs: Add JSON output documentation"
```

---

## Task 12: Run Full Test Suite and Coverage

**Files:**
- None (testing)

**Step 1: Run full test suite**

```bash
cd /Users/ray/Workspace/autosar-pdf/.worktrees/json-writer
python scripts/run_tests.py --all
```

Expected: All tests pass

**Step 2: Check coverage**

```bash
# Check coverage for json_writer.py
pytest src/autosar_pdf2txt/writer/json_writer.py --cov=autosar_pdf2txt.writer.json_writer --cov-report=term-missing
```

Expected: ≥95% coverage

**Step 3: Fix any coverage gaps**

If coverage < 95%, add tests for missing branches.

**Step 4: Commit final fixes**

```bash
git add src/ tests/
git commit -m "test: Improve JsonWriter test coverage"
```

---

## Task 13: Integration Test with Real PDF

**Files:**
- None (testing)

**Step 1: Run integration test with sample PDF**

```bash
cd /Users/ray/Workspace/autosar-pdf/.worktrees/json-writer
autosar-extract examples/pdf/AUTOSAR_CP_Schema.pdf -o /tmp/test_json_output.json --format json
```

**Step 2: Verify output structure**

```bash
ls -la /tmp/test_json_output/
cat /tmp/test_json_output/index.json | python -m json.tool
```

Expected: Valid JSON with proper structure

**Step 3: Compare JSON vs Markdown output**

```bash
# Generate both formats
autosar-extract examples/pdf/AUTOSAR_CP_Schema.pdf -o /tmp/test_md_output --format markdown
autosar-extract examples/pdf/AUTOSAR_CP_Schema.pdf -o /tmp/test_json_output.json --format json

# Compare entity counts (should match)
# Write a quick Python script to verify
```

**Step 4: Create integration test**

Add to `tests/integration/test_json_integration.py`:

```python
"""Integration tests for JSON writer."""

import json
from pathlib import Path
import pytest
from autosar_pdf2txt.parser import PdfParser
from autosar_pdf2txt.writer import JsonWriter


class TestJSONIntegration:
    """Integration tests for JSON output with real PDFs.

    Requirements:
        SWR_WRITER_00024: JSON Integration Testing
    """

    def test_json_output_matches_markdown_content(self, sample_pdf):
        """Test JSON output contains same data as Markdown.

        Requirements:
            SWR_WRITER_00024: JSON Integration Testing
        """
        # Parse PDF
        parser = PdfParser()
        doc = parser.parse_file(sample_pdf)

        # Write both formats
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            # JSON output
            json_writer = JsonWriter()
            json_writer.write_packages_to_files(doc.packages, base_dir=Path(tmpdir) / "json")

            # Load JSON
            with open(Path(tmpdir) / "json" / "index.json") as f:
                index = json.load(f)

            # Verify index has expected fields
            assert "version" in index
            assert "metadata" in index
            assert "packages" in index

            # Verify entity counts match
            total_classes = sum(pkg.get("class_count", 0) for pkg in index["packages"])
            assert total_classes > 0  # Should have extracted some classes
```

**Step 5: Run integration test**

```bash
pytest tests/integration/test_json_integration.py -v
```

**Step 6: Commit**

```bash
git add tests/integration/test_json_integration.py
git commit -m "test: Add JSON integration tests"
```

---

## Completion Checklist

Before marking this feature complete:

- [ ] All unit tests pass (≥95% coverage)
- [ ] Integration tests pass with sample PDFs
- [ ] Documentation updated (README, CLAUDE.md, requirements)
- [ ] Design document linked from implementation plan
- [ ] Code follows project coding standards
- [ ] Ruff linting passes
- [ ] Mypy type checking passes
- [ ] Manual testing completed with real AUTOSAR PDFs
- [ ] JSON schema validated
- [ ] Example usage documented

---

## Post-Implementation

After completing all tasks:

1. **Merge to main branch**
   ```bash
   cd /Users/ray/Workspace/autosar-pdf
   git checkout master
   git merge feature/json-writer
   git push origin master
   ```

2. **Clean up worktree**
   ```bash
   git worktree remove .worktrees/json-writer
   ```

3. **Update todo.md**
   Mark tasks as completed:
   ```markdown
   - [x] Add the cli format argument to specify the output format. currently markdown and json can be supported
   - [x] Help me design the json format for all the autosar class extract. So it could benefit other python scripts to parse the extracted data
   ```

4. **Create GitHub issue** (if applicable) to track any follow-up improvements

---

**End of Implementation Plan**
