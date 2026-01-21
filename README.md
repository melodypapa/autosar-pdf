# AUTOSAR PDF to Text

A Python package to extract AUTOSAR model hierarchies from PDF files and convert them to markdown format.

## Features

- Extract AUTOSAR packages and classes from PDF specification documents
- Parse hierarchical class structures
- Generate markdown output with proper indentation
- Support for abstract classes
- Model-level duplicate prevention

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

# Enable verbose mode for detailed debug information
autosar-extract path/to/file.pdf -v

# Extract from multiple PDFs with verbose output
autosar-extract *.pdf -o output.md -v
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

## Examples

### Example: Extracting AUTOSAR Templates

The repository includes sample AUTOSAR specification PDFs in the `examples/pdf/` directory that you can use to test the tool:

```bash
# Extract a single AUTOSAR template
autosar-extract examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf

# Extract all AUTOSAR templates from the examples directory
autosar-extract examples/pdf/

# Save output to a markdown file
autosar-extract examples/pdf/ -o autosar_templates.md

# Extract specific templates
autosar-extract \
  examples/pdf/AUTOSAR_CP_TPS_SystemTemplate.pdf \
  examples/pdf/AUTOSAR_CP_TPS_SoftwareComponentTemplate.pdf \
  -o system_and_component.md

# Extract with verbose output to see processing details
autosar-extract examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf -v
```

### Example: Generate Class Files

Generate separate markdown files for each AUTOSAR class:

```bash
# Extract Software Component Template and create individual class files
autosar-extract examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf --include-class-details -o data/autosar_models.md

autosar-extract examples/pdf/AUTOSAR_FO_TPS_GenericStructureTemplate.pdf --include-class-details -o data/autosar_models.md
```

Include the `--include-class-details` flag to generate individual class files in the `output/classes/` directory.

### Example Output

When you run the command above, you'll see output like:

```
Parsing: examples/pdf/AUTOSAR_CP_TPS_SoftwareComponentTemplate.pdf
Found 15 packages
Writing to: software_components.md
Writing class files to: output/classes/
```

## Requirements

- Python 3.7+
- pdfplumber

## License

MIT
