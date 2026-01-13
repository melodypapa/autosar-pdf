# Class-Based Architecture

This document describes the class-based architecture of the pdf2txt library.

## Overview

The pdf2txt library uses an object-oriented design with dedicated classes for different aspects of PDF processing.

## Core Classes

### PdfConverter
Location: `pdf2txt/core/converter.py`

Handles PDF to text conversion using multiple backends (pypdf, pdfplumber).

**Key Methods:**
- `convert(pdf_path, skip_header_lines, skip_footer_lines)` - Convert PDF to text
- `convert_advanced(pdf_path, page_range, include_images, skip_header_lines, skip_footer_lines)` - Advanced conversion with options
- `get_page_count(pdf_path)` - Get number of pages in PDF (static method)

**Usage:**
```python
from pdf2txt.core.converter import PdfConverter

converter = PdfConverter(method="pdfplumber")
text = converter.convert("input.pdf")
```

### TextCleaner
Location: `pdf2txt/core/cleaner.py`

Handles text cleaning and normalization.

**Key Methods:**
- `clean(text)` - Clean special characters from text
- `remove_extra_whitespace(text)` - Normalize whitespace (static method)
- `normalize_newlines(text)` - Normalize newlines (static method)

**Usage:**
```python
from pdf2txt.core.cleaner import TextCleaner

cleaner = TextCleaner()
clean_text = cleaner.clean(extracted_text)
```

### TableExtractor
Location: `pdf2txt/core/table.py`

Extracts tables from PDF files using pdfplumber.

**Key Methods:**
- `extract(pdf_path, page_range)` - Extract tables from PDF

**Usage:**
```python
from pdf2txt.core.table import TableExtractor

extractor = TableExtractor()
tables = extractor.extract("input.pdf")
```

### TableConverter
Location: `pdf2txt/core/table.py`

Converts table data to various formats.

**Key Methods:**
- `to_markdown(table_data, include_header)` - Convert table to Markdown

**Usage:**
```python
from pdf2txt.core.table import TableConverter

converter = TableConverter()
markdown_table = converter.to_markdown(table_data)
```

### MarkdownConverter
Location: `pdf2txt/core/markdown.py`

Converts plain text to Markdown format.

**Key Methods:**
- `convert(text, preserve_structure)` - Convert text to Markdown

**Usage:**
```python
from pdf2txt.core.markdown import MarkdownConverter

converter = MarkdownConverter()
markdown_text = converter.convert(text)
```

### PdfConverterWithTables
Location: `pdf2txt/core/integration.py`

Integrated converter that combines text conversion and table extraction.

**Key Methods:**
- `convert(pdf_path, output_format, page_range, skip_header_lines, skip_footer_lines, include_tables)` - Convert with table support

**Usage:**
```python
from pdf2txt.core.integration import PdfConverterWithTables

converter = PdfConverterWithTables()
result = converter.convert("input.pdf", output_format="markdown", include_tables=True)
```

## AUTOSAR Extractor Classes

### AutosarParser
Location: `pdf2txt/extractor/parser.py`

Parses AUTOSAR specification text to extract package and class information.

**Key Methods:**
- `parse(text)` - Parse text and extract packages and classes

**Usage:**
```python
from pdf2txt.extractor.parser import AutosarParser

parser = AutosarParser()
packages = parser.parse(extracted_text)
```

### PackageHierarchyBuilder
Location: `pdf2txt/extractor/hierarchy.py`

Builds hierarchical tree structures from package data.

**Key Methods:**
- `build_tree(packages)` - Build nested tree structure
- `build_dict(packages)` - Build flat dictionary mapping

**Usage:**
```python
from pdf2txt.extractor.hierarchy import PackageHierarchyBuilder

builder = PackageHierarchyBuilder()
tree = builder.build_tree(packages)
```

### OutputWriter
Location: `pdf2txt/extractor/writer.py`

Writes package and class information to files in various formats.

**Key Methods:**
- `write_markdown_hierarchy(tree, output_path, title)` - Write Markdown hierarchy
- `write_text_summary(packages, output_path)` - Write text summary

**Usage:**
```python
from pdf2txt.extractor.writer import OutputWriter

writer = OutputWriter()
writer.write_markdown_hierarchy(tree, "output.md", "My Reference")
```

### AutosarExtractor
Location: `pdf2txt/extractor/integration.py`

High-level AUTOSAR extraction that combines parsing, hierarchy building, and writing.

**Key Methods:**
- `extract_from_pdf(pdf_path, output_path, format, method)` - Extract from single PDF
- `extract_from_multiple_pdfs(pdf_paths, output_path, format, method, merge_output)` - Extract from multiple PDFs

**Usage:**
```python
from pdf2txt.extractor.integration import AutosarExtractor

extractor = AutosarExtractor()
stats = extractor.extract_from_pdf("autosar.pdf", "output.md", format="markdown")
```

## Data Models

### Class
Location: `pdf2txt/extractor/models.py`

Represents an AUTOSAR class.

**Attributes:**
- `name` (str): Class name
- `abstract` (bool): Whether the class is abstract

### Package
Location: `pdf2txt/extractor/models.py`

Represents an AUTOSAR package containing classes.

**Attributes:**
- `name` (str): Package name
- `classes` (List[Class]): List of Class objects

**Properties:**
- `total_classes` (int): Total number of classes in the package
- `total_abstract_classes` (int): Number of abstract classes

## Backward Compatibility

All old function-based APIs are maintained for backward compatibility. They create instances of the new classes internally and delegate to them.

Example:
```python
# Old function-based API (still works)
from pdf2txt.core.converter import convert_pdf_to_text
text = convert_pdf_to_text("input.pdf")

# New class-based API
from pdf2txt.core.converter import PdfConverter
converter = PdfConverter()
text = converter.convert("input.pdf")
```

## Benefits of Class-Based Architecture

1. **Encapsulation**: Related data and methods are grouped together
2. **State Management**: Classes can maintain state across method calls
3. **Extensibility**: Easy to add new functionality by extending classes
4. **Testability**: Classes can be easily mocked and tested in isolation
5. **Reusability**: Classes can be instantiated with different configurations
6. **Maintainability**: Easier to understand and modify code structure
