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
# Extract from PDF and print to stdout
autosar-extract path/to/file.pdf

# Extract and save to file
autosar-extract path/to/file.pdf -o output.md
```

### Python API

```python
from autosar_pdf2txt import PdfParser, MarkdownWriter

# Parse PDF file
parser = PdfParser()
packages = parser.parse_pdf("path/to/file.pdf")

# Write to markdown
writer = MarkdownWriter()
markdown = writer.write_packages(packages)
print(markdown)
```

## Requirements

- Python 3.10+
- pdfplumber

## License

MIT
