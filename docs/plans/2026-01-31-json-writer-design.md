# JSON Writer Design Document

**Date**: 2026-01-31
**Status**: Draft
**Author**: Collaborative design session

## Overview

This document describes the design for a JSON output format for AUTOSAR class extraction. The JSON format provides complete data model representation with all metadata (sources, inheritance, attributes, package paths) in a machine-parsable format suitable for downstream Python scripts.

## Design Goals

1. **Complete data model representation**: All metadata from the AUTOSAR extraction
2. **Manageable file sizes**: Split files by package and entity type
3. **Easy parsing**: Separated entity types (classes, enumerations, primitives)
4. **CLI compatibility**: Parallel to existing MarkdownWriter

## File Structure

```
output_dir/
├── index.json                                              # Root index with overview
└── packages/
    ├── M2.json                                              # Top-level package metadata
    ├── M2 AUTOSAR.json                                      # Package metadata
    ├── M2 AUTOSAR.classes.json                              # All classes in M2::AUTOSAR
    ├── M2 AUTOSAR.enums.json                                # All enumerations in M2::AUTOSAR
    ├── M2 AUTOSAR.primitives.json                           # All primitives in M2::AUTOSAR
    ├── M2 AUTOSAR DataTypes.json                            # Subpackage metadata
    ├── M2 AUTOSAR DataTypes.classes.json                    # Classes in subpackage
    ├── M2 AUTOSAR DataTypes.enums.json                      # Enumerations in subpackage
    └── ...
```

**Key principles:**
- **Split by entity type**: Each package has separate files for classes, enumerations, primitives
- **Metadata files**: Lightweight package JSON files with summary counts and file references
- **Hierarchical**: Mirrors the package structure with nested directories

## JSON Schemas

### 1. Root Index (index.json)

```json
{
  "version": "1.0",
  "metadata": {
    "generated_at": "2025-01-31T10:30:00Z",
    "source_files": ["AUTOSAR_CP_Schema.pdf"],
    "autosar_standard": "AUTOSAR CP",
    "standard_release": "R22-11",
    "total_packages": 15,
    "total_classes": 342,
    "total_enumerations": 89,
    "total_primitives": 12
  },
  "packages": [
    {
      "name": "M2",
      "file": "packages/M2.json",
      "class_count": 0,
      "subpackages": ["M2::AUTOSAR", "M2::ECUC"]
    },
    {
      "name": "M2::AUTOSAR",
      "file": "packages/M2 AUTOSAR.json",
      "class_count": 45,
      "subpackages": ["M2::AUTOSAR::DataTypes"]
    }
  ]
}
```

**Fields:**
- `version`: Schema version for forward compatibility
- `metadata`: Global extraction context
- `packages`: Array of top-level package references

### 2. Package Metadata File (packages/{name}.json)

```json
{
  "name": "M2::AUTOSAR::DataTypes",
  "path": "M2::AUTOSAR::DataTypes",
  "files": {
    "classes": "packages/M2 AUTOSAR DataTypes.classes.json",
    "enumerations": "packages/M2 AUTOSAR DataTypes.enums.json",
    "primitives": "packages/M2 AUTOSAR DataTypes.primitives.json"
  },
  "subpackages": [
    {
      "name": "ImplementationDataTypes",
      "full_path": "M2::AUTOSAR::DataTypes::ImplementationDataTypes",
      "file": "packages/M2 AUTOSAR DataTypes ImplementationDataTypes.json"
    }
  ],
  "summary": {
    "class_count": 25,
    "enumeration_count": 8,
    "primitive_count": 3
  }
}
```

**Fields:**
- `name`: Package short name
- `path`: Full package path with `::` separator
- `files`: References to entity files
- `subpackages`: Child package metadata
- `summary`: Quick counts without loading entity files

### 3. Classes File (packages/{name}.classes.json)

```json
{
  "package": "M2::AUTOSAR::DataTypes",
  "classes": [
    {
      "name": "ImplementationDataType",
      "package": "M2::AUTOSAR::DataTypes",
      "is_abstract": false,
      "atp_type": "atpVariation",
      "parent": null,
      "bases": [],
      "children": ["SwDataDefProps", "ApplicationDataType"],
      "subclasses": [],
      "aggregated_by": [],
      "implements": [],
      "implemented_by": [],
      "note": "Data type for implementation specific data definitions",
      "sources": [
        {
          "pdf_file": "AUTOSAR_CP_Schema.pdf",
          "page_number": 245,
          "autosar_standard": "AUTOSAR CP",
          "standard_release": "R22-11"
        }
      ],
      "attributes": {
        "category": {
          "type": "DataRepresentationCategoryEnum",
          "multiplicity": "1",
          "kind": "attribute",
          "is_ref": false,
          "note": "Category of this data type"
        },
        "sw_data_def_props": {
          "type": "SwDataDefProps",
          "multiplicity": "0..1",
          "kind": "reference",
          "is_ref": true,
          "note": "Implementation data type specific properties"
        }
      }
    }
  ]
}
```

**Class fields:**
- `name`: Class name
- `package`: Full package path
- `is_abstract`: Boolean for abstract classes
- `atp_type`: ATP marker type (one of: `"atpVariation"`, `"atpMixedString"`, `"atpMixed"`, `"atpPrototype"`, or `null`)
- `parent`: Immediate parent class name (or `null`)
- `bases`: Array of all base class names
- `children`: Array of child class names
- `subclasses`: Array of subclass names from PDF
- `aggregated_by`: Array of aggregating class names
- `implements`: Array of interface names this class implements
- `implemented_by`: Array of class names implementing this ATP interface
- `note`: Documentation note
- `sources`: Array of source locations
- `attributes`: Object with attribute names as keys

**Attribute structure:**
- `type`: Attribute type name
- `multiplicity`: Multiplicity string (e.g., `"1"`, `"0..1"`, `"0.."`)
- `kind`: One of `"attribute"`, `"reference"`
- `is_ref`: Boolean indicating if it's a reference
- `note`: Attribute description

**Source structure:**
- `pdf_file`: PDF filename
- `page_number`: Page number
- `autosar_standard`: AUTOSAR standard name (or `null`)
- `standard_release`: Release version (or `null`)

### 4. Enumerations File (packages/{name}.enums.json)

```json
{
  "package": "M2::AUTOSAR::DataTypes",
  "enumerations": [
    {
      "name": "DataRepresentationCategoryEnum",
      "package": "M2::AUTOSAR::DataTypes",
      "note": "Categories for data representation",
      "sources": [
        {
          "pdf_file": "AUTOSAR_CP_Schema.pdf",
          "page_number": 247,
          "autosar_standard": "AUTOSAR CP",
          "standard_release": "R22-11"
        }
      ],
      "literals": [
        {
          "name": "DATA_TYPE",
          "value": 0,
          "description": "Standard data type"
        },
        {
          "name": "DATA_DEFINITION",
          "value": 1,
          "description": "Data definition reference<br>Tags: deprecated=false, since=4.2.0"
        }
      ]
    }
  ]
}
```

**Enumeration fields:**
- `name`: Enumeration name
- `package`: Full package path
- `note`: Documentation note
- `sources`: Array of source locations
- `literals`: Array of literal values

**Literal structure:**
- `name`: Literal name
- `value`: Numeric value (or `null` if not specified)
- `description`: Description text (tags already merged into description with `<br>Tags:` format)

### 5. Primitives File (packages/{name}.primitives.json)

```json
{
  "package": "M2::AUTOSAR::DataTypes",
  "primitives": [
    {
      "name": "Limit",
      "package": "M2::AUTOSAR::DataTypes",
      "note": "Interval limit definition",
      "sources": [
        {
          "pdf_file": "AUTOSAR_CP_Schema.pdf",
          "page_number": 250,
          "autosar_standard": "AUTOSAR CP",
          "standard_release": "R22-11"
        }
      ],
      "attributes": {
        "interval_type": {
          "type": "String",
          "multiplicity": "1",
          "kind": "attribute",
          "is_ref": false,
          "note": "Open or closed interval"
        }
      }
    }
  ]
}
```

**Primitive fields:**
- Similar to classes but no inheritance fields (no `parent`, `bases`, `children`, etc.)
- `attributes`: Same structure as class attributes

## CLI Integration

### New CLI Arguments

```bash
# Explicit format selection
autosar-extract input.pdf -o output --format json
autosar-extract input.pdf -o output --format markdown

# File extension inference (default behavior)
autosar-extract input.pdf -o output.json    # Creates index.json + packages/
autosar-extract input.pdf -o output.md      # Creates markdown files
autosar-extract input.pdf -o output         # Default: markdown
```

### Implementation Components

1. **`--format` argument**: Add to `autosar_cli.py`
   - Choices: `"markdown"`, `"json"`
   - Default: infer from file extension
   - Fallback: `"markdown"`

2. **`JsonWriter` class**: New writer in `src/autosar_pdf2txt/writer/json_writer.py`
   - Parallel structure to `MarkdownWriter`
   - Methods:
     - `write_packages_to_files(packages, output_path, base_dir)`: Main entry point
     - `write_packages(packages)`: Return JSON string
   - Creates the file structure defined above

3. **Writer selection in CLI**:
   ```python
   if format == "json" or output_path.suffix == ".json":
       writer = JsonWriter()
   else:
       writer = MarkdownWriter()
   ```

### File Naming Convention

- Sanitize package names for filesystem safety (same as MarkdownWriter)
- Replace invalid chars: `< > : " / \ | ? *` → `_`
- Pattern: `{sanitized_package_name}.classes.json`
  - `"M2::AUTOSAR::DataTypes"` → `"M2 AUTOSAR DataTypes.classes.json"`

## Implementation Plan

### Phase 1: Core Writer Implementation
1. Create `JsonWriter` class with basic structure
2. Implement `write_packages_to_files()` with directory creation
3. Implement index.json generation
4. Implement package metadata file generation

### Phase 2: Entity Serialization
1. Implement class serialization to JSON
2. Implement enumeration serialization to JSON
3. Implement primitive serialization to JSON
4. Handle attribute encoding for all entity types

### Phase 3: CLI Integration
1. Add `--format` argument to CLI
2. Implement file extension inference
3. Wire up writer selection logic
4. Update help documentation

### Phase 4: Testing
1. Unit tests for `JsonWriter` methods
2. Integration tests with sample PDFs
3. Validate JSON schema correctness
4. Compare JSON output vs Markdown output completeness

### Phase 5: Documentation
1. Update README with JSON output examples
2. Add requirements to `requirements_writer.md`
3. Update CLAUDE.md with JSON usage patterns

## Benefits

1. **Machine-readable**: Easy to parse with Python `json` module
2. **Complete metadata**: All sources, inheritance, attributes preserved
3. **File size control**: Split files prevent massive single files
4. **Type separation**: Query only what you need (classes, enums, primitives)
5. **Future-proof**: Version field allows schema evolution
6. **Consistent**: Mirrors MarkdownWriter structure and behavior

## Example Usage

```python
import json

# Load all classes from a package
with open("output/packages/M2 AUTOSAR.classes.json") as f:
    data = json.load(f)
    classes = data["classes"]

# Find classes with specific base
for cls in classes:
    if "AutosarClass" in cls["bases"]:
        print(f"{cls['name']} extends AutosarClass")

# Load all enumerations
with open("output/packages/M2 AUTOSAR.enums.json") as f:
    data = json.load(f)
    enums = data["enumerations"]

# Get enumeration literal values
for enum in enums:
    print(f"{enum['name']}:")
    for literal in enum["literals"]:
        print(f"  {literal['name']} = {literal['value']}")
```

## Notes

- **Enum literal tags**: Merged into `description` field (not separate)
- **ATP types**: String values in JSON (not enum constants)
- **Attribute kinds**: String values (`"attribute"`, `"reference"`)
- **Source fields**: `null` when not available (vs missing fields)
- **File encoding**: UTF-8 for all JSON files
