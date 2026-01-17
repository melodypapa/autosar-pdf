# Software Requirements Specification

## autosar-pdf2txt Requirements

This document contains all software requirements extracted from the current implementation of the autosar-pdf2txt package.

## Maturity Levels

Each requirement has a maturity level that indicates its status:

- **draft**: Newly created requirement, under review, or not yet implemented
- **accept**: Accepted requirement, implemented in the codebase
- **invalid**: Deprecated requirement, superseded, or no longer applicable

All existing requirements in this document are currently at maturity level **accept**.

### 1. Model

#### SWR_MODEL_00001
**Title**: AUTOSAR Class Representation

**Maturity**: accept

**Description**: The system shall provide a data model to represent an AUTOSAR class with the following attributes:
- `name`: The name of the class (non-empty string)
- `is_abstract`: Boolean flag indicating whether the class is abstract
- `attributes`: Dictionary of AUTOSAR attributes where key is the attribute name and value is the AUTOSAR attribute object
- `bases`: List of base class names for inheritance tracking (List[str], defaults to empty list)
- `note`: Optional free-form text for documentation or comments (str | None, defaults to None)

---

#### SWR_MODEL_00002
**Title**: AUTOSAR Class Name Validation

**Maturity**: accept

**Description**: The system shall validate that AUTOSAR class names are non-empty and do not contain only whitespace upon initialization.

---

#### SWR_MODEL_00003
**Title**: AUTOSAR Class String Representation

**Maturity**: accept

**Description**: The system shall provide string representations of AUTOSAR classes, including:
- A user-friendly string with "(abstract)" suffix for abstract classes
- A debug representation showing all attributes

---

#### SWR_MODEL_00004
**Title**: AUTOSAR Package Representation

**Maturity**: accept

**Description**: The system shall provide a data model to represent an AUTOSAR package with the following attributes:
- `name`: The name of the package (non-empty string)
- `classes`: List of AutosarClass objects contained in the package
- `subpackages`: List of AutosarPackage objects (nested packages)

---

#### SWR_MODEL_00005
**Title**: AUTOSAR Package Name Validation

**Maturity**: accept

**Description**: The system shall validate that AUTOSAR package names are non-empty and do not contain only whitespace upon initialization.

---

#### SWR_MODEL_00006
**Title**: Add Class to Package

**Maturity**: accept

**Description**: The system shall provide functionality to add an AutosarClass to an AutosarPackage. The system shall check for duplicate classes by class name. If a class with the same name already exists in the package, the class shall not be added again.

---

#### SWR_MODEL_00007
**Title**: Add Subpackage to Package

**Maturity**: accept

**Description**: The system shall provide functionality to add an AutosarPackage as a subpackage to another AutosarPackage. The system shall check for duplicate subpackages by subpackage name. If a subpackage with the same name already exists in the parent package, the subpackage shall not be added again.

---

#### SWR_MODEL_00008
**Title**: Query Package Contents

**Maturity**: accept

**Description**: The system shall provide query methods to:
- Get a class by name from a package
- Get a subpackage by name from a package
- Check if a class exists in a package
- Check if a subpackage exists in a package

---

#### SWR_MODEL_00009
**Title**: Package String Representation

**Maturity**: accept

**Description**: The system shall provide string representations of AUTOSAR packages, including summary information about the number of classes and subpackages.

---

#### SWR_MODEL_00010
**Title**: AUTOSAR Attribute Representation

**Maturity**: accept

**Description**: The system shall provide a data model to represent an AUTOSAR class attribute with the following attributes:
- `name`: The name of the attribute (non-empty string)
- `type`: The data type of the attribute (non-empty string)
- `is_ref`: Boolean flag indicating whether the attribute is a reference type

---

#### SWR_MODEL_00011
**Title**: AUTOSAR Attribute Name Validation

**Maturity**: accept

**Description**: The system shall validate that AUTOSAR attribute names are non-empty and do not contain only whitespace upon initialization.

---

#### SWR_MODEL_00012
**Title**: AUTOSAR Attribute Type Validation

**Maturity**: accept

**Description**: The system shall validate that AUTOSAR attribute types are non-empty and do not contain only whitespace upon initialization.

---

#### SWR_MODEL_00013
**Title**: AUTOSAR Attribute String Representation

**Maturity**: accept

**Description**: The system shall provide string representations of AUTOSAR attributes, including:
- A user-friendly string showing attribute name and type, with "(ref)" suffix for reference types
- A debug representation showing all attributes (name, type, is_ref)

---

### 2. Parser

#### SWR_PARSER_00001
**Title**: PDF Parser Initialization

**Maturity**: accept

**Description**: The system shall provide a PDF parser class that uses pdfplumber as the default PDF engine.

---

#### SWR_PARSER_00002
**Title**: Backend Validation

**Maturity**: accept

**Description**: The system shall validate that the requested PDF parsing backend is available and properly installed before attempting to parse PDFs.

---

#### SWR_PARSER_00003
**Title**: PDF File Parsing

**Maturity**: accept

**Description**: The system shall provide functionality to parse a PDF file and extract AUTOSAR package and class hierarchies from it.

---

#### SWR_PARSER_00004
**Title**: Class Definition Pattern Recognition

**Maturity**: accept

**Description**: The system shall recognize and parse AUTOSAR class definitions from PDF text using the following patterns:
- Class definitions: `Class <name> (abstract)`
- Package definitions: `Package <M2::?><path>`
- Base classes: `Base <class_list>` (extracted from the Base column in class tables)
- Subclasses: `Subclasses <class_list>`
- Notes: Extracted from the Note column in class tables as free-form documentation text

---

#### SWR_PARSER_00005
**Title**: Class Definition Data Model

**Maturity**: accept

**Description**: The system shall provide an internal data model (`ClassDefinition`) to represent parsed class information including:
- Class name
- Full package path
- Abstract flag
- List of base classes
- List of subclasses

---

#### SWR_PARSER_00006
**Title**: Package Hierarchy Building

**Maturity**: accept

**Description**: The system shall build a hierarchical AUTOSAR package structure from parsed class definitions, creating nested packages based on the package path delimiter ("::").

---

#### SWR_PARSER_00007
**Title**: PDF Backend Support - pdfplumber

**Maturity**: accept

**Description**: The system shall support pdfplumber as a PDF parsing backend for extracting text content from PDF files.

---

### 3. Writer

#### SWR_WRITER_00001
**Title**: Markdown Writer Initialization

**Maturity**: accept

**Description**: The system shall provide a markdown writer class for writing AUTOSAR packages and classes to markdown format.

---

#### SWR_WRITER_00002
**Title**: Markdown Package Hierarchy Output

**Maturity**: accept

**Description**: The system shall write AUTOSAR package hierarchies to markdown format using asterisk (*) bullet points with 2-space indentation per nesting level.

---

#### SWR_WRITER_00003
**Title**: Markdown Class Output Format

**Maturity**: accept

**Description**: The system shall write AUTOSAR classes in markdown format with:
- Indentation 1 level deeper than their parent package
- "(abstract)" suffix appended to abstract class names

---

#### SWR_WRITER_00004
**Title**: Bulk Package Writing

**Maturity**: accept

**Description**: The system shall provide functionality to write multiple top-level packages to markdown format in a single operation.

---

### 4. CLI

#### SWR_CLI_00001
**Title**: CLI Entry Point

**Maturity**: accept

**Description**: The system shall provide a command-line interface tool named `autosar-extract` for extracting AUTOSAR models from PDF files.

---

#### SWR_CLI_00002
**Title**: CLI File Input Support

**Maturity**: accept

**Description**: The CLI shall accept one or more PDF file paths as input arguments.

---

#### SWR_CLI_00003
**Title**: CLI Directory Input Support

**Maturity**: accept

**Description**: The CLI shall accept directory paths as input and automatically discover all PDF files within them (sorted alphabetically).

---

#### SWR_CLI_00004
**Title**: CLI Output File Option

**Maturity**: accept

**Description**: The CLI shall support an `-o` / `--output` option to write the extracted markdown to a specified file instead of stdout.

---

#### SWR_CLI_00005
**Title**: CLI Verbose Mode

**Maturity**: accept

**Description**: The CLI shall support a `-v` / `--verbose` option to enable verbose output mode, which prints detailed debug information during processing.

---

#### SWR_CLI_00006
**Title**: CLI Input Validation

**Maturity**: accept

**Description**: The CLI shall validate input paths and provide appropriate error messages for:
- Non-existent paths
- Non-PDF files (with warning)
- Empty directories (with warning)
- No valid PDF files to process (with error)

---

#### SWR_CLI_00007
**Title**: CLI Progress Feedback

**Maturity**: accept

**Description**: The CLI shall provide progress feedback via stderr messages indicating:
- PDF files being parsed
- Number of top-level packages found per PDF
- Total number of packages processed
- Output file location when applicable

---

#### SWR_CLI_00008
**Title**: CLI Logging

**Maturity**: accept

**Description**: The CLI shall provide logging information to show the current processing progress, including detailed status messages for each operation step.

---

#### SWR_CLI_00009
**Title**: CLI Error Handling

**Maturity**: accept

**Description**: The CLI shall catch and report exceptions with user-friendly error messages via stderr and return appropriate exit codes (0 for success, 1 for error).

---

### 5. Package

#### SWR_PACKAGE_00001
**Title**: Package API Export

**Maturity**: accept

**Description**: The system shall export the following public API from the root package:
- `AutosarAttribute`
- `AutosarClass`
- `AutosarPackage`
- `PdfParser`
- `MarkdownWriter`
- `__version__`

---

#### SWR_PACKAGE_00002
**Title**: Python Version Support

**Maturity**: accept

**Description**: The system shall support Python versions 3.7 through 3.11.

---

#### SWR_PACKAGE_00003
**Title**: Package Metadata

**Maturity**: accept

**Description**: The system shall include appropriate package metadata including:
- Package name: autosar-pdf2txt
- Version information
- Author and contact information
- Description and long description
- Project URL
- License classification (MIT)
