# AUTOSAR Models Usage Guide

This guide shows how to use the Package and Class models in the pdf2txt library.

## Overview

The library provides two main data models:

- **Class**: Represents an AUTOSAR class with a name and abstract flag
- **Package**: Represents an AUTOSAR package with a name and list of classes

## Class Model

```python
from pdf2txt.extractor.models import Class

# Create a concrete class
concrete_class = Class(name="ConcreteClass", abstract=False)

# Create an abstract class
abstract_class = Class(name="AbstractClass", abstract=True)

# Create a class with default abstract value (False)
default_class = Class(name="DefaultClass")

print(f"Class: {default_class.name}, Abstract: {default_class.abstract}")
```

## Package Model

```python
from pdf2txt.extractor.models import Package, Class

# Create classes
classes = [
    Class(name="ClassA", abstract=False),
    Class(name="ClassB", abstract=True),
    Class(name="ClassC", abstract=False),
]

# Create package
pkg = Package(name="MyPackage", classes=classes)

# Access package properties
print(f"Package: {pkg.name}")
print(f"Total classes: {pkg.total_classes}")
print(f"Abstract classes: {pkg.total_abstract_classes}")

# Access individual classes
for cls in pkg.classes:
    abstract_mark = " [abstract]" if cls.abstract else ""
    print(f"  - {cls.name}{abstract_mark}")
```

## Extracting from PDF with Models

```python
from pdf2txt.extractor import extract_package_and_class_info
from pdf2txt.core.converter import convert_pdf_to_text

# Extract text from PDF
text = convert_pdf_to_text("autosar.pdf", method="pdfplumber")

# Parse and get Package objects
packages = extract_package_and_class_info(text)

# Work with Package objects
for pkg in packages:
    print(f"\nPackage: {pkg.name}")
    print(f"  Total classes: {pkg.total_classes}")
    print(f"  Abstract classes: {pkg.total_abstract_classes}")
    
    for cls in pkg.classes:
        abstract_mark = " (abstract)" if cls.abstract else ""
        print(f"    - {cls.name}{abstract_mark}")
```

## Filtering Packages and Classes

```python
from pdf2txt.extractor import extract_package_and_class_info
from pdf2txt.core.converter import convert_pdf_to_text

# Extract packages
text = convert_pdf_to_text("autosar.pdf", method="pdfplumber")
all_packages = extract_package_and_class_info(text)

# Filter by package name prefix
filtered_packages = [
    pkg for pkg in all_packages
    if pkg.name.startswith("AUTOSARTemplates::")
]

# Filter abstract classes
all_abstract_classes = []
for pkg in all_packages:
    for cls in pkg.classes:
        if cls.abstract:
            all_abstract_classes.append((pkg.name, cls.name))

print(f"Found {len(all_abstract_classes)} abstract classes")
```

## Converting to Hierarchy

```python
from pdf2txt.extractor import (
    extract_package_and_class_info,
    build_package_hierarchy,
)
from pdf2txt.core.converter import convert_pdf_to_text

# Extract packages
text = convert_pdf_to_text("autosar.pdf", method="pdfplumber")
packages = extract_package_and_class_info(text)

# Build hierarchical tree
tree = build_package_hierarchy(packages)

# The tree is a nested dictionary structure
# Access: tree['AUTOSARTemplates']['BswModuleTemplate']['__classes__']
# Returns: List[Class] objects
```

## Working with Multiple PDFs

```python
from pdf2txt.extractor import extract_from_multiple_pdfs

# Extract from multiple PDFs
pdf_files = ["autosar_part1.pdf", "autosar_part2.pdf"]

results = extract_from_multiple_pdfs(
    pdf_paths=pdf_files,
    output_path="merged_autosar.md",
    format="markdown",
    method="pdfplumber",
    merge_output=True,
)

print(f"Total packages: {results['total_packages']}")
print(f"Total classes: {results['total_classes']}")
```

## Writing Output

```python
from pdf2txt.extractor import (
    extract_package_and_class_info,
    build_package_hierarchy,
    write_markdown_hierarchy,
    write_text_summary,
)
from pdf2txt.core.converter import convert_pdf_to_text

# Extract packages
text = convert_pdf_to_text("autosar.pdf", method="pdfplumber")
packages = extract_package_and_class_info(text)

# Write markdown output
tree = build_package_hierarchy(packages)
write_markdown_hierarchy(
    tree,
    "output.md",
    title="AUTOSAR Package and Class Reference"
)

# Write text output
write_text_summary(packages, "output.txt")
```

## Notes

- The `abstract` flag is extracted from the class definition line in the PDF
- The search for "abstract" keyword is case-insensitive
- All class names in a package are unique (deduplicated during extraction)
- Package paths use "::" as separator (AUTOSAR convention)
