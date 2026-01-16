# AUTOSAR PDF to Text

A Python package to extract AUTOSAR model hierarchies from PDF files and convert them to markdown format.

## Features

- Extract AUTOSAR packages and classes from PDF specification documents
- Parse hierarchical class structures
- Generate markdown output with proper indentation
- Support for abstract classes

## Installation

```bash
pip install autosar-pdf2txt
```

## Usage

### Command Line

```bash
# Extract from single PDF and print to stdout
autosar-extract path/to/file.pdf

# Extract from multiple PDFs
autosar-extract path/to/file1.pdf path/to/file2.pdf path/to/file3.pdf

# Extract from directory (processes all PDFs in directory)
autosar-extract path/to/directory

# Extract from multiple directories and files
autosar-extract path/to/dir1 path/to/file.pdf path/to/dir2

# Extract and save to file
autosar-extract path/to/file.pdf -o output.md

# Extract from multiple PDFs with deduplication disabled
autosar-extract *.pdf --no-deduplicate -o output.md
```

### Python API

```python
from autosar_pdf2txt import PdfParser, MarkdownWriter

# Parse single PDF file
parser = PdfParser()
packages = parser.parse_pdf("path/to/file.pdf")

# Parse multiple PDF files
parser = PdfParser()
all_packages = []
for pdf_path in ["path/to/file1.pdf", "path/to/file2.pdf"]:
    packages = parser.parse_pdf(pdf_path)
    all_packages.extend(packages)

# Write to markdown
writer = MarkdownWriter()
markdown = writer.write_packages(all_packages)
print(markdown)
```

## Requirements

- Python 3.10+
- pdfplumber

## License

MIT
