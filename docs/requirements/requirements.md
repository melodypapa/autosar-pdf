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
- `atp_type`: ATP marker type enum indicating the AUTOSAR Tool Platform marker (defaults to NONE)
- `attributes`: Dictionary of AUTOSAR attributes where key is the attribute name and value is the AUTOSAR attribute object
- `bases`: List of base class names for inheritance tracking (List[str], defaults to empty list)
- `note`: Optional free-form text for documentation or comments (str | None, defaults to None)

The ATP type enum shall support the following values:
- `NONE`: No ATP marker present
- `ATP_MIXED_STRING`: The class has the <<atpMixedString>> marker
- `ATP_VARIATION`: The class has the <<atpVariation>> marker
- `ATP_MIXED`: The class has the <<atpMixed>> marker

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
- Class definitions with ATP markers: `Class <name> <<atpMixedString>>`, `Class <name> <<atpVariation>>`, and `Class <name> <<atpMixed>>`
- Package definitions: `Package <M2::?><path>`
- Base classes: `Base <class_list>` (extracted from the Base column in class tables)
- Subclasses: `Subclasses <class_list>`
- Notes: Extracted from the Note column in class tables as free-form documentation text

The system shall preserve the "M2::" prefix in package paths when present, treating "M2" as the root metamodel package. This ensures that the complete package hierarchy is maintained, with "M2" as the top-level package containing all AUTOSAR packages (e.g., M2 → AUTOSARTemplates → BswModuleTemplate).

The system shall strip ATP marker patterns from the class name and determine the appropriate ATP type enum value based on the detected markers:
- No markers: `ATPType.NONE`
- Only <<atpMixedString>>: `ATPType.ATP_MIXED_STRING`
- Only <<atpVariation>>: `ATPType.ATP_VARIATION`
- Only <<atpMixed>>: `ATPType.ATP_MIXED`

When multiple ATP markers are detected on the same class, the system shall report a validation error indicating that a class cannot have multiple ATP markers simultaneously.

The system shall filter out class definitions that do not have an associated package path, as these are typically false positives caused by page headers, footers, or other text in the PDF that matches the class pattern but does not represent a valid class definition.

---

#### SWR_PARSER_00005
**Title**: Class Definition Data Model

**Maturity**: accept

**Description**: The system shall provide an internal data model (`ClassDefinition`) to represent parsed class information including:
- Class name (extracted from PDF text following the pattern `Class <name>`)
- Full package path
- Abstract flag (set to `true` when the class name starts with "Abstract" or the class is marked as abstract in the PDF)
- List of base classes
- List of subclasses

---

#### SWR_PARSER_00006
**Title**: Package Hierarchy Building

**Maturity**: accept

**Description**: The system shall build a hierarchical AUTOSAR package structure from parsed class definitions, creating nested packages based on the package path delimiter ("::").

The system shall:
1. Parse the package path into individual components using "::" as the delimiter
2. Create or retrieve package objects for each component in the path
3. Establish parent-child relationships between packages by adding subpackages to their parent packages
4. Add classes to the appropriate package based on the full package path

---

#### SWR_PARSER_00007
**Title**: Top-Level Package Selection

**Maturity**: accept

**Description**: The system shall correctly identify and return only top-level packages from the package hierarchy.

The system shall:
1. Return only packages that have no "::" in their full path (indicating they are root-level packages)
2. Ensure that packages contain either classes or subpackages (or both)
3. Use proper operator precedence in the selection logic: `if "::" not in path and (pkg.classes or pkg.subpackages)`
4. Ensure that intermediate packages in the hierarchy (e.g., `AUTOSARTemplates::SystemTemplate::Fibex`) are not returned as top-level packages

This requirement prevents packages that are nested within other packages from being incorrectly returned as root-level packages.

---

#### SWR_PARSER_00008
**Title**: PDF Backend Support - pdfplumber

**Maturity**: accept

**Description**: The system shall support pdfplumber as a PDF parsing backend for extracting text content from PDF files.

---

#### SWR_PARSER_00009
**Title**: Proper Word Spacing in PDF Text Extraction

**Maturity**: accept

**Description**: The system shall extract text from PDF files with proper spacing between words to ensure readable and accurate documentation.

The system shall:
1. Use word-level extraction (pdfplumber's `extract_words()` method) instead of raw text extraction to properly identify word boundaries
2. Apply appropriate x-tolerance parameters (x_tolerance=1) to detect word separation based on character positions
3. Reconstruct text from extracted words while preserving line breaks based on vertical position changes
4. Ensure that extracted notes, descriptions, and other text fields contain spaces between words as they appear in the original PDF document

This requirement addresses common PDF text extraction issues where words are concatenated without spaces due to tight kerning or custom font spacing in the source PDF files.

---

#### SWR_PARSER_00010
**Title**: Attribute Extraction from PDF

**Maturity**: accept

**Description**: The system shall extract class attributes from PDF files and convert them to AutosarAttribute objects.

The system shall:
1. Recognize the attribute section in PDF class tables (identified by "Attribute Type Mult. Kind Note" header)
2. Parse each attribute line with the format: `<name> <type> <multiplicity> <kind> <description>`
3. Create AutosarAttribute objects with the extracted name and type
4. Determine if an attribute is a reference type based on the attribute type (e.g., types ending with "Prototype", "Ref", or other reference indicators)
5. Store attributes in a dictionary keyed by attribute name in the ClassDefinition
6. Transfer attributes to the AutosarClass object during package hierarchy building

This requirement ensures that class attributes are properly extracted and stored, enabling complete documentation of AUTOSAR class structures including their properties.

---

#### SWR_PARSER_00011
**Title**: Metadata Filtering in Attribute Extraction

**Maturity**: accept

**Description**: The system shall filter out metadata and formatting information from PDF class tables during attribute extraction to ensure only valid AUTOSAR class attributes are extracted.

The system shall:
1. Track when parsing is within the attribute section (after the "Attribute Type Mult. Kind Note" header)
2. Validate attribute names to exclude lines containing special characters like `:` or `;`
3. Validate attribute names to exclude lines that start with a number
4. Validate attribute types to exclude metadata indicators such as `:`, `of`, `CP`, or `atpSplitable`
5. Only parse attribute lines when within the attribute section to prevent false positives from other sections of the PDF

This requirement prevents metadata lines (e.g., "Stereotypes: : atpSplitable;", "287 : of", "Specification : of", "AUTOSAR : CP") from being incorrectly parsed as class attributes, ensuring the extracted attributes match the official AUTOSAR metamodel specification.

---

#### SWR_PARSER_00012
**Title**: Multi-Line Attribute Handling

**Maturity**: accept

**Description**: The system shall handle multi-line attribute definitions in PDF class tables to prevent broken or split attributes from being incorrectly parsed as separate attributes.

The system shall:
1. Detect when attribute names or types span multiple lines in the PDF due to table formatting
2. Properly reconstruct complete attribute names that may be split across lines (e.g., "isStructWithOptionalElement" split as "isStructWith" on one line and "OptionalElement" on another)
3. Properly reconstruct complete attribute types that may be split across lines (e.g., "dynamicArraySizeProfile" split as "dynamicArray" on one line and "SizeProfile" on another)
4. Prevent partial attribute fragments from being treated as complete attributes
5. Ensure that only complete, valid attribute definitions are extracted
6. Filter out common continuation words and fragment names that appear in broken attribute lines, including:
   - Continuation types: "data", "If", "has", "to"
   - Fragment names: "Element", "SizeProfile", "intention", "ImplementationDataType"
   - Partial attribute names: "dynamicArray" (should be "dynamicArraySizeProfile"), "isStructWith" (should be "isStructWithOptionalElement")

This requirement addresses PDF table formatting issues where attribute names or types may wrap across multiple lines, preventing incorrect extraction of partial attributes like "SizeProfile", "Element", "ImplementationDataType", and "intention" as separate attributes when they are actually part of a larger attribute definition or continuation of previous content. The system filters out these broken fragments to ensure only valid, complete attributes are extracted.

---

#### SWR_PARSER_00013
**Title**: Recognition of Primitive and Enumeration Class Definition Patterns

**Maturity**: accept

**Description**: The system shall recognize and correctly parse AUTOSAR class definitions that use "Primitive" and "Enumeration" prefixes in addition to the standard "Class" prefix.

The system shall:
1. Recognize the pattern `Primitive <classname>` as a valid class definition for primitive type classes (e.g., "Primitive Limit")
2. Recognize the pattern `Enumeration <classname>` as a valid class definition for enumeration type classes (e.g., "Enumeration IntervalTypeEnum")
3. Recognize the pattern `Class <classname>` as a valid class definition for regular classes (e.g., "Class ImplementationDataType")
4. Apply the same validation rules to all three patterns (require package path within 5 lines to avoid page header false positives)
5. Treat all three patterns as class definition markers that end the attribute section of the previous class
6. Properly assign attributes to the correct class based on which definition they follow

This requirement ensures that the parser correctly handles the three types of class definitions used in AUTOSAR PDF specification documents:
- Regular classes: `Class ImplementationDataType`
- Primitive types: `Primitive Limit`
- Enumeration types: `Enumeration IntervalTypeEnum`

Without this requirement, the parser would fail to recognize when a new class starts after "Primitive" or "Enumeration" definitions, causing attributes from subsequent classes to be incorrectly added to the previous class. For example, without recognizing "Primitive Limit" as a new class, the `intervalType` attribute from the Limit class would be incorrectly added to the ImplementationDataType class.

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
- No abstract marker in the class name (abstract status is shown only in individual class files)

---

#### SWR_WRITER_00004
**Title**: Bulk Package Writing

**Maturity**: accept

**Description**: The system shall provide functionality to write multiple top-level packages to markdown format in a single operation.

---

#### SWR_WRITER_00005
**Title**: Directory-Based Class File Output

**Maturity**: accept

**Description**: The system shall provide functionality to write AUTOSAR classes to separate markdown files organized in a directory structure that mirrors the package hierarchy. The root directory for the file structure shall be the same as the output markdown file location. For each package:
- Create a directory corresponding to the package name
- Create a single markdown file for each class in the package, named with the class name
- Maintain nested directory structure for subpackages

---

#### SWR_WRITER_00006
**Title**: Individual Class Markdown File Content

**Maturity**: accept

**Description**: The markdown file for each AUTOSAR class shall contain the following information in a structured format:
- Title: Class name with "(abstract)" suffix for abstract classes
- Package name: The full package path containing the class
- Type section: Explicit indicator showing whether the class is "Abstract" or "Concrete"
- ATP Type section: List of ATP markers based on the ATP type enum value, included only when the ATP type is not NONE
- Base classes: List of base class names that this class inherits from
- Note: Class documentation/description extracted from the note field
- Attributes list: Complete list of class attributes showing name, type, and reference indicator for each attribute

The ATP Type section shall:
- Be included only when ATP type is ATP_MIXED_STRING or ATP_VARIATION
- List the applicable marker: atpVariation for ATP_VARIATION, or atpMixedString for ATP_MIXED_STRING
- Appear immediately after the Type section and before the Base Classes section when present

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

#### SWR_CLI_00010
**Title**: CLI Class File Output

**Maturity**: accept

**Description**: When the `--write-class-files` flag is specified along with the `-o` / `--output` option, the CLI shall create separate markdown files for each AUTOSAR class in a directory structure that mirrors the package hierarchy. The root directory for the class files shall be the same as the output markdown file location.

---

#### SWR_CLI_00011
**Title**: CLI Class Files Flag

**Maturity**: accept

**Description**: The CLI shall support a `--write-class-files` flag to enable creation of separate markdown files for each class. This flag only has effect when used with the `-o` / `--output` option. When not specified, only the main hierarchy output file is created.

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
