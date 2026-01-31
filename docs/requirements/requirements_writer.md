# Writer Requirements

This document contains all software requirements for the autosar-pdf2txt markdown writer.

## Maturity Levels

Each requirement has a maturity level that indicates its status:

- **draft**: Newly created requirement, under review, or not yet implemented
- **accept**: Accepted requirement, implemented in the codebase
- **invalid**: Deprecated requirement, superseded, or no longer applicable

---

### SWR_WRITER_00001
**Title**: Markdown Writer Initialization

**Maturity**: accept

**Description**: The system shall provide a markdown writer class for writing AUTOSAR packages and classes to markdown format.

---

### SWR_WRITER_00002
**Title**: Markdown Package Hierarchy Output

**Maturity**: accept

**Description**: The system shall write AUTOSAR package hierarchies to markdown format using asterisk (*) bullet points with 2-space indentation per nesting level.

---

### SWR_WRITER_00003
**Title**: Markdown Class Output Format

**Maturity**: accept

**Description**: The system shall write AUTOSAR classes in markdown format with:
- Indentation 1 level deeper than their parent package
- No abstract marker in the class name (abstract status is shown only in individual class files)
- Attributes displayed in a table format with columns: Attribute | Type | Mult. | Kind | Note

---

### SWR_WRITER_00004
**Title**: Bulk Package Writing

**Maturity**: accept

**Description**: The system shall provide functionality to write multiple top-level packages to markdown format in a single operation.

---

### SWR_WRITER_00005
**Title**: Directory-Based Class File Output

**Maturity**: accept

**Description**: The system shall provide functionality to write AUTOSAR classes to separate markdown files organized in a directory structure that mirrors the package hierarchy. The root directory for the file structure shall be the same as the output markdown file location. For each package:
- Create a directory corresponding to the package name (if it does not exist)
- Create a single markdown file for each class in the package, named with the class name
- Maintain nested directory structure for subpackages

If the destination directory or any intermediate directories in the path do not exist, they shall be created automatically.

---

### SWR_WRITER_00006
**Title**: Individual Class Markdown File Content

**Maturity**: accept

**Description**: The markdown file for each AUTOSAR class shall contain the following information in a structured format:
- Title: Class name with "(abstract)" suffix for abstract classes
- Package name: The full package path containing the class
- Type section: Explicit indicator showing whether the class is "Abstract" or "Concrete"
- Parent: The immediate parent class name from the parent attribute (included only when parent is not None)
- ATP Type section: List of ATP markers based on the ATP type enum value, included only when the ATP type is not NONE
- Base classes: List of base class names that this class inherits from
- Subclasses: List of subclass names explicitly listed in the PDF source document (included only when the subclasses list is not empty)
- Children: List of child class names that inherit from this class (included only when the children list is not empty)
- Note: Class documentation/description extracted from the note field
- Attributes list: Complete list of class attributes showing name, type, and reference indicator for each attribute

The Parent section shall:
- Be included only when the parent attribute is not None
- Display the parent class name as a string
- Appear immediately after the Type section and before the ATP Type section when present

The ATP Type section shall:
- Be included only when ATP type is ATP_MIXED_STRING or ATP_VARIATION
- List the applicable marker: atpVariation for ATP_VARIATION, or atpMixedString for ATP_MIXED_STRING
- Appear immediately after the Parent section (or Type section if no parent) and before the Base Classes section when present

The Subclasses section shall:
- Be included only when the subclasses list is not empty
- Display the list of subclass names as a comma-separated list
- Sort subclass names alphabetically in ascending order
- Appear immediately after the Base Classes section and before the Note section when present

The Children section shall:
- Be included only when the children list is not empty
- Display the list of child class names as bullet points
- Sort child class names alphabetically in ascending order
- Appear immediately after the Document Source section (if present) or Subclasses section (if no source) and before the Note section when present

---

### SWR_WRITER_00007
**Title**: Class Hierarchy Output

**Maturity**: accept

**Description**: The system shall provide functionality to write AUTOSAR class inheritance hierarchies to markdown format. The class hierarchy output shall:
- Start with a "## Class Hierarchy" heading
- Display root classes (classes with no parent) at the top level with asterisk (*) bullet points
- Indent child classes 2 spaces per level relative to their parent class
- Mark abstract classes with "(abstract)" suffix after the class name
- Support both root-only output (when all_classes parameter is None) and full hierarchy output (when all_classes parameter is provided)
- Return empty string when no root classes are provided

---

### SWR_WRITER_00008
**Title**: Markdown Source Information Output

**Maturity**: accept

**Description**: The markdown writer shall output source information in individual class files when using the `--include-class-details` flag. The output shall include:
- A "Document Source" section listing all source locations where the type is defined (if sources are available)
- A markdown table format with columns for PDF file, page number, AUTOSAR standard, and standard release
- Display **all source locations** where the type is defined (supports types appearing in multiple PDFs)
- One row per source location in the table

The Document Source section shall:
- Only be included when source information is available from the parsing process
- Use markdown table format with column headers: PDF File, Page, AUTOSAR Standard, Standard Release
- Include all four columns regardless of whether some values are empty (use "-" for missing values)
- Sort rows alphabetically by PDF filename

**Example Output (single source)**:
```markdown
## Document Source

| PDF File | Page | AUTOSAR Standard | Standard Release |
|----------|------|------------------|------------------|
| AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf | 42 | Classic Platform | R23-11 |
```

**Example Output (multiple sources)**:
```markdown
## Document Source

| PDF File | Page | AUTOSAR Standard | Standard Release |
|----------|------|------------------|------------------|
| AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf | 42 | Classic Platform | R23-11 |
| AUTOSAR_CP_TPS_SoftwareComponentTemplate.pdf | 15 | Classic Platform | R23-11 |
```

**Example Output (minimal - no standard info)**:
```markdown
## Document Source

| PDF File | Page | AUTOSAR Standard | Standard Release |
|----------|------|------------------|------------------|
| AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf | 42 | - | - |
```

This requirement enables complete traceability of AUTOSAR type definitions to their source documents using a structured table format for easy reading and parsing, including specification document identification, version tracking, and support for types defined across multiple PDF specifications.

---

### SWR_WRITER_00009
**Title**: Enumeration Literal Table Output Format

**Maturity**: accept

**Description**: The markdown writer shall output enumeration literals in a table format with three columns: Name, Value, and Description. The output shall:
- Use markdown table format with column headers: Name, Value, Description
- Display the literal name in the Name column
- Display the literal value (extracted from xml.name tag) in the Value column, or "-" if no value is present
- Display the literal description in the Description column
- Append all tags to the description on a new line using `<br>` tag followed by "Tags: key=value, key2=value2" format
- Sort tags alphabetically by key in the merged tags string
- Display "-" in the Description column if no description or tags are present
- Preserve the order of enumeration literals as they appear in the PDF source document

**Example Output (with value and tags)**:
```markdown
## Enumeration Literals

| Name | Value | Description |
|------|-------|-------------|
| PRE_R4_2 | PRE–R-4–2 | Check has the legacy behavior, before AUTOSAR Release 4.2.<br>Tags: atp.EnumerationLiteralIndex=0, xml.name=PRE–R-4–2 |
| R4_2 | R-4–2 | Check behaves like new P4/P5/P6 profiles introduced in AUTOSAR Release 4.2.<br>Tags: atp.EnumerationLiteralIndex=1, xml.name=R-4–2 |
```

**Example Output (without value)**:
```markdown
## Enumeration Literals

| Name | Value | Description |
|------|-------|-------------|
| eventCombination | - | Event combination on retrieval is used to combine events. Tags: xml.name=SOME-VALUE |
```

**Example Output (minimal)**:
```markdown
## Enumeration Literals

| Name | Value | Description |
|------|-------|-------------|
| SimpleLiteral | - | - |
```

This requirement provides a clean, tabular format for enumeration literals that separates the literal name from its value and description, making it easier to read and parse programmatically while maintaining all metadata information in a structured manner.

---

### JSON Writer Requirements

The following requirements define JSON output format for AUTOSAR class extraction.

**Document**: [requirements_writer.md](requirements_writer.md)

**Requirements**: SWR_WRITER_00010 - SWR_WRITER_00023

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

---

### SWR_WRITER_00010
**Title**: JSON Writer Initialization

**Maturity**: draft

**Description**: The system shall provide a JSON writer class (JsonWriter) for writing AUTOSAR packages and classes to JSON format. The JsonWriter class shall:
- Be parallel in structure to the existing MarkdownWriter class
- Require no parameters for initialization
- Support multi-file JSON output organized by entity type and package

---

### SWR_WRITER_00011
**Title**: JSON Directory Structure Creation

**Maturity**: draft

**Description**: The JSON writer shall create a packages/ directory in the output location and maintain a nested directory structure for subpackages. The root directory for the file structure shall be the same as the output JSON file location.

---

### SWR_WRITER_00012
**Title**: JSON File Naming and Sanitization

**Maturity**: draft

**Description**: The JSON writer shall sanitize package names for filesystem safety by replacing invalid characters (< > : " / \ | ? *) with underscores. The file naming pattern shall be {sanitized_package_name}.classes.json for class files.

---

### SWR_WRITER_00013
**Title**: JSON Index File Output

**Maturity**: draft

**Description**: The JSON writer shall create an index.json file in the root output directory containing:
- version: Schema version string ("1.0")
- metadata: Object with generated_at timestamp, source_files array, total entity counts
- packages: Array of package references with name, file path, class_count, and subpackages

---

### SWR_WRITER_00014
**Title**: JSON Package Metadata File Output

**Maturity**: draft

**Description**: The JSON writer shall create a package metadata JSON file (packages/{name}.json) containing:
- name: Package short name
- path: Full package path with :: separator
- files: Object with references to classes, enumerations, primitives files
- subpackages: Array of child package metadata objects
- summary: Object with class_count, enumeration_count, primitive_count

---

### SWR_WRITER_00015
**Title**: JSON Class Serialization

**Maturity**: draft

**Description**: The JSON writer shall serialize AUTOSAR classes to JSON format with all class fields:
- name, package, is_abstract, atp_type
- parent, bases, children, subclasses, aggregated_by
- implements, implemented_by, note, sources
- attributes: Object with attribute names as keys

---

### SWR_WRITER_00016
**Title**: JSON ATP Type Encoding

**Maturity**: draft

**Description**: The JSON writer shall encode ATP type enum values as strings or null:
- "atpVariation" for ATP_VARIATION
- "atpMixedString" for ATP_MIXED_STRING
- "atpMixed" for ATP_MIXED
- "atpPrototype" for ATP_PROTO
- null for ATP_NONE

---

### SWR_WRITER_00017
**Title**: JSON Source Information Encoding

**Maturity**: draft

**Description**: The JSON writer shall encode AutosarDocumentSource objects as dictionaries with:
- pdf_file: PDF filename string
- page_number: Integer page number
- autosar_standard: AUTOSAR standard name string or null
- standard_release: Release version string or null

---

### SWR_WRITER_00018
**Title**: JSON Attribute Encoding

**Maturity**: draft

**Description**: The JSON writer shall encode AutosarAttribute objects as dictionaries with:
- type: Attribute type name string
- multiplicity: Multiplicity string (e.g., "1", "0..1", "0..")
- kind: String "attribute" or "reference"
- is_ref: Boolean indicating if it's a reference
- note: Attribute description string

---

### SWR_WRITER_00019
**Title**: JSON Inheritance Hierarchy Encoding

**Maturity**: draft

**Description**: The JSON writer shall encode inheritance-related class fields:
- parent: Immediate parent class name or null
- bases: Array of all base class names
- children: Array of child class names
- subclasses: Array of subclass names from PDF
- implements: Array of interface names this class implements
- implemented_by: Array of class names implementing this ATP interface

---

### SWR_WRITER_00020
**Title**: JSON Enumeration Serialization

**Maturity**: draft

**Description**: The JSON writer shall serialize AUTOSAR enumerations to JSON format with:
- name, package, note, sources
- literals: Array of literal objects with name, value, description
- Enumeration literal tags merged into description field with <br>Tags: format

---

### SWR_WRITER_00021
**Title**: JSON Primitive Serialization

**Maturity**: draft

**Description**: The JSON writer shall serialize AUTOSAR primitives to JSON format with:
- name, package, note, sources
- attributes: Object with attribute names as keys (no inheritance fields)

---

### SWR_WRITER_00022
**Title**: JSON CLI Format Argument

**Maturity**: draft

**Description**: The CLI shall provide a --format option with choices: "markdown", "json". Default format shall be inferred from file extension.

---

### SWR_WRITER_00023
**Title**: JSON Format Inference from Extension

**Maturity**: draft

**Description**: The CLI shall infer output format from file extension:
- .json extension → JSON format
- .md extension → Markdown format
- No extension or unknown → Markdown (default)