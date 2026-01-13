# AUTOSAR Multiple PDF Extraction

This example demonstrates how to extract package and class information from multiple AUTOSAR PDF files.

## Usage Examples

### Python API

#### Extract from multiple PDF files (merged output)

```python
from pdf2txt.extractor import extract_from_multiple_pdfs

# List of PDF files
pdf_files = [
    "path/to/autosar_part1.pdf",
    "path/to/autosar_part2.pdf",
    "path/to/autosar_part3.pdf",
]

# Extract and merge all packages into a single output
results = extract_from_multiple_pdfs(
    pdf_paths=pdf_files,
    output_path="merged_autosar.md",
    format="markdown",
    method="pdfplumber",
    merge_output=True,
)

print(f"Total Packages: {results['total_packages']}")
print(f"Total Classes: {results['total_classes']}")
```

#### Extract from multiple PDF files (separate outputs)

```python
from pdf2txt.extractor import extract_from_multiple_pdfs

pdf_files = [
    "path/to/autosar_part1.pdf",
    "path/to/autosar_part2.pdf",
]

# Extract each PDF to its own output file
results = extract_from_multiple_pdfs(
    pdf_paths=pdf_files,
    output_path=None,  # Will auto-generate filenames
    format="text",
    method="pdfplumber",
    merge_output=False,
)

# Results is a dict mapping each PDF file to its statistics
for pdf_file, stats in results.items():
    print(f"{pdf_file}: {stats['total_packages']} packages, {stats['total_classes']} classes")
```

#### Extract from a directory containing PDFs

```python
from pdf2txt.extractor import extract_from_multiple_pdfs

# Extract all PDF files from a directory
results = extract_from_multiple_pdfs(
    pdf_paths="path/to/autosar_directory",
    output_path="all_autosar_packages.md",
    format="markdown",
    method="pdfplumber",
    merge_output=True,
)

print(f"Merged {results['total_packages']} packages from all PDFs")
```

### Command Line Interface

#### Extract from multiple PDF files

```bash
# Extract multiple files with merged output
autosar-extract autosar_part1.pdf autosar_part2.pdf autosar_part3.pdf --merge -o merged_autosar.md

# Extract multiple files with separate outputs
autosar-extract autosar_part1.pdf autosar_part2.pdf

# Extract all PDFs from a directory
autosar-extract ./autosar_specs/ --merge -o all_specs.md

# Extract with specific options
autosar-extract *.pdf --merge -o merged.md --format markdown -v
```

## Options

- `pdf_paths`: Directory path or list of PDF file paths
- `output_path`: Output file path (for merged mode) or None for auto-generated names
- `format`: "markdown" or "text"
- `method`: "pdfplumber" (recommended) or "pypdf2"
- `merge_output`: True to merge all packages, False for separate outputs

## Notes

- When `merge_output=True`, packages with the same name from different PDFs are merged together
- When `merge_output=False`, each PDF produces its own output file with auto-generated names
- The `--merge` flag in CLI enables merged output for multiple inputs
- Without `--merge`, each input PDF generates its own output file
