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
- Appear immediately after the Source section (if present) or Subclasses section (if no source) and before the Note section when present

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
- A "Source" section for the class's own definition location (if available)
- Proper formatting with PDF filename and page number for the source
- Optional AUTOSAR standard identifier (if available from the parsing process)
- Optional AUTOSAR standard release (if available from the parsing process)

The source section shall:
- Only be included when source information is available from the parsing process
- Display the PDF filename and page number on the first line
- Display "AUTOSAR Standard: <identifier>" on a separate line if autosar_standard is not None
- Display "Standard Release: <release>" on a separate line if standard_release is not None
- Format each piece of information on its own line for readability

**Example Output**:
```
Source
AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf, page 42
AUTOSAR Standard: TPS_BSWModuleDescriptionTemplate
Standard Release: R21-11
```

**Example Output (without release)**:
```
Source
AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf, page 42
AUTOSAR Standard: TPS_BSWModuleDescriptionTemplate
```

**Example Output (minimal)**:
```
Source
AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf, page 42
```

This requirement enables complete traceability of AUTOSAR type definitions to their source documents, including specification document identification and version tracking.