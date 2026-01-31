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