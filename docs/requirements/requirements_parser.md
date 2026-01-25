# Parser Requirements

This document contains all software requirements for the autosar-pdf2txt PDF parser.

## Maturity Levels

Each requirement has a maturity level that indicates its status:

- **draft**: Newly created requirement, under review, or not yet implemented
- **accept**: Accepted requirement, implemented in the codebase
- **invalid**: Deprecated requirement, superseded, or no longer applicable

---

### SWR_PARSER_00001
**Title**: PDF Parser Initialization

**Maturity**: accept

**Description**: The system shall provide a PDF parser class that uses pdfplumber as the default PDF engine.

---

### SWR_PARSER_00002
**Title**: Backend Validation

**Maturity**: accept

**Description**: The system shall validate that the requested PDF parsing backend is available and properly installed before attempting to parse PDFs.

---

### SWR_PARSER_00003
**Title**: PDF File Parsing

**Maturity**: accept

**Description**: The system shall provide functionality to parse a PDF file and extract AUTOSAR package and class hierarchies from it.

The system shall use a two-phase parsing approach:
1. **Read Phase**: Extract all text from all pages of the PDF into a single buffer
   - Use pdfplumber's extract_words() method with x_tolerance=1 to properly handle word spacing
   - Reconstruct text from words while preserving line breaks based on vertical position
   - Accumulate all pages' text into a single StringIO buffer
2. **Parse Phase**: Parse the complete text buffer to extract AUTOSAR model objects
   - Process all lines sequentially from the complete text buffer
   - Maintain state management for multi-page definitions via current_models and model_parsers dictionaries
   - Delegate to appropriate specialized parsers (class, enumeration, primitive) for each type definition
   - Continue parsing for existing models across page boundaries

This two-phase approach ensures:
- Complete text is available for analysis before parsing begins
- Simpler debugging with all text in a single buffer
- Consistent handling of multi-page definitions through state management
- Better separation of concerns between reading and parsing phases

---

### SWR_PARSER_00004
**Title**: Class Definition Pattern Recognition

**Maturity**: accept

**Description**: The system shall recognize and parse AUTOSAR class definitions from PDF text using the following patterns:
- Class definitions: `Class <name> (abstract)`
- Class definitions with ATP markers: `Class <name> <<atpMixedString>>`, `Class <name> <<atpVariation>>`, and `Class <name> <<atpMixed>>`
- Package definitions: `Package <M2::?><path>`
- Base classes: `Base <class_list>` (extracted from the Base column in class tables)
- Subclasses: `Subclasses <class_list>` (extracted and stored in the subclasses attribute). The subclasses are the descendants of a class, meaning they inherit from this class. Therefore, a subclass cannot be the parent of this class, and it also cannot be in the bases list of this class's parent.
- Notes: Extracted from the Note column in class tables as free-form documentation text. Notes may span multiple lines in the PDF and are captured completely until encountering another known pattern (Base, Subclasses, Tags:, Attribute, Class, Primitive, Enumeration, Table, Package).

The system shall preserve the "M2::" prefix in package paths when present, treating "M2" as the root metamodel package. This ensures that the complete package hierarchy is maintained, with "M2" as the top-level package containing all AUTOSAR packages (e.g., M2 → AUTOSARTemplates → BswModuleTemplate).

The system shall strip ATP marker patterns from the class name and determine the appropriate ATP type enum value based on the detected markers:
- No markers: `ATPType.NONE`
- Only <<atpMixedString>>: `ATPType.ATP_MIXED_STRING`
- Only <<atpVariation>>: `ATPType.ATP_VARIATION`
- Only <<atpMixed>>: `ATPType.ATP_MIXED`

When multiple ATP markers are detected on the same class, the system shall report a validation error indicating that a class cannot have multiple ATP markers simultaneously.

The system shall filter out class definitions that do not have an associated package path, as these are typically false positives caused by page headers, footers, or other text in the PDF that matches the class pattern but does not represent a valid class definition.

---

### SWR_PARSER_00005
**Title**: Class Definition Data Model

**Maturity**: accept

**Description**: The system shall provide an internal data model (`ClassDefinition`) to represent parsed class information including:
- Class name (extracted from PDF text following the pattern `Class <name>`, `Primitive <name>`, or `Enumeration <name>`)
- Full package path
- Abstract flag (set to `true` when the class name starts with "Abstract" or the class is marked as abstract in the PDF)
- List of base classes
- List of subclasses
- `is_enumeration`: Boolean flag indicating whether this is an enumeration type
- `is_primitive`: Boolean flag indicating whether this is a primitive type

---

### SWR_PARSER_00006
**Title**: Package Hierarchy Building

**Maturity**: accept

**Description**: The system shall build a hierarchical AUTOSAR package structure from parsed class, enumeration, and primitive definitions, creating nested packages based on the package path delimiter ("::").

Requirements:
    SWR_MODEL_00020: AUTOSAR Package Type Support
    SWR_MODEL_00025: AUTOSAR Package Primitive Type Support

The system shall:
1. Parse the package path into individual components using "::" as the delimiter
2. Create or retrieve package objects for each component in the path
3. Establish parent-child relationships between packages by adding subpackages to their parent packages
4. Add types (classes, enumerations, and primitives) to the appropriate package based on the full package path using the unified `types` collection

---

### SWR_PARSER_00007
**Title**: Top-Level Package Selection

**Maturity**: accept

**Description**: The system shall correctly identify and return only top-level packages from the package hierarchy.

Requirements:
    SWR_MODEL_00020: AUTOSAR Package Type Support

The system shall:
1. Return only packages that have no "::" in their full path (indicating they are root-level packages)
2. Ensure that packages contain either types (classes/enumerations) or subpackages (or both)
3. Use proper operator precedence in the selection logic: `if "::" not in path and (pkg.types or pkg.subpackages)`
4. Ensure that intermediate packages in the hierarchy (e.g., `AUTOSARTemplates::SystemTemplate::Fibex`) are not returned as top-level packages

This requirement prevents packages that are nested within other packages from being incorrectly returned as root-level packages.

---

### SWR_PARSER_00008
**Title**: PDF Backend Support - pdfplumber

**Maturity**: accept

**Description**: The system shall support pdfplumber as a PDF parsing backend for extracting text content from PDF files.

---

### SWR_PARSER_00009
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

### SWR_PARSER_00010
**Title**: Attribute Extraction from PDF

**Maturity**: accept

**Description**: The system shall extract class attributes from PDF files and convert them to AutosarAttribute objects.

The system shall:
1. Recognize the attribute section in PDF class tables (identified by "Attribute Type Mult. Kind Note" header)
2. Parse each attribute line with the format: `<name> <type> <multiplicity> <kind> <description>`
3. Create AutosarAttribute objects with the extracted name, type, multiplicity, kind, and note
4. Determine if an attribute is a reference type based on the attribute type (e.g., types ending with "Prototype", "Ref", or other reference indicators)
5. Store attributes in a dictionary keyed by attribute name in the ClassDefinition
6. Transfer attributes to the AutosarClass object during package hierarchy building

This requirement ensures that class attributes are properly extracted and stored, enabling complete documentation of AUTOSAR class structures including their properties.

---

### SWR_PARSER_00011
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

### SWR_PARSER_00012
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

### SWR_PARSER_00013
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
7. Create AutosarPrimitive objects for primitive type definitions
8. Create AutosarEnumeration objects for enumeration type definitions
9. Create AutosarClass objects for regular class definitions

This requirement ensures that the parser correctly handles the three types of class definitions used in AUTOSAR PDF specification documents:
- Regular classes: `Class ImplementationDataType`
- Primitive types: `Primitive Limit`
- Enumeration types: `Enumeration IntervalTypeEnum`

Without this requirement, the parser would fail to recognize when a new class starts after "Primitive" or "Enumeration" definitions, causing attributes from subsequent classes to be incorrectly added to the previous class. For example, without recognizing "Primitive Limit" as a new class, the `intervalType` attribute from the Limit class would be incorrectly added to the ImplementationDataType class.

---

### SWR_PARSER_00014
**Title**: Enumeration Literal Header Recognition

**Maturity**: accept

**Description**: The system shall recognize enumeration literal table headers in PDF files to identify when enumeration literals should be extracted.

The system shall:
1. Recognize the "Literal Description" header pattern that indicates the start of an enumeration literal table
2. Track when parsing is within the enumeration literal section
3. Initialize enumeration literal parsing state when the header is detected

---

### SWR_PARSER_00015
**Title**: Enumeration Literal Extraction from PDF

**Maturity**: accept

**Description**: The system shall extract enumeration literals from PDF files and convert them to AutosarEnumLiteral objects.

The system shall:
1. Parse enumeration literal lines with the format: `<literal_name> <description>`
2. Extract the literal name (must start with a letter and contain alphanumeric characters or underscores)
3. Extract the literal description (free-form text after the literal name)
4. Extract enumeration literal indices from description tags (e.g., "atp.EnumerationLiteralIndex=0")
5. Create AutosarEnumLiteral objects with the extracted name, index, and description
6. Store enumeration literals in a list in the ClassDefinition
7. Transfer enumeration literals to the AutosarClass object during package hierarchy building

This requirement ensures that enumeration literals are properly extracted for enumeration classes like `EcucDestinationUriNestingContractEnum` from AUTOSAR CP TPS ECUConfiguration, which contains literals such as:
- `leafOfTargetContainer` (index=0, description="EcucDestinationUriPolicy describes elements directly owned by the target container")
- `targetContainer` (index=1, description="EcucDestinationUriPolicy describes the target container of EcucUriReferenceDef")
- `vertexOfTargetContainer` (index=2, description="EcucDestinationUriPolicy describes elements of the target container which can be defined in arbitrary nested subContainer structure")

---

### SWR_PARSER_00016
**Title**: Enumeration Literal Section Termination

**Maturity**: accept

**Description**: The system shall properly detect the end of enumeration literal sections in PDF files to prevent incorrect extraction of non-literal content.

The system shall:
1. Terminate the enumeration literal section when encountering new class definitions (Class, Primitive, or Enumeration patterns)
2. Terminate the enumeration literal section when encountering new table headers (e.g., "Table X.Y:")
3. Ensure that only valid enumeration literals are extracted and stored
4. Prevent false positives from other sections of the PDF

This requirement ensures that enumeration literal extraction is scoped correctly to the enumeration literal table, preventing extraction of unrelated text content as enumeration literals.

---

### SWR_PARSER_00017
**Title**: AUTOSAR Class Parent Resolution

**Maturity**: accept

**Description**: After parsing all classes and building the AUTOSAR class hierarchy tree, the system shall automatically set the `parent` attribute for each class to reference the actual direct parent `AutosarClass` object using ancestry-based analysis.

The system shall:
1. Build complete inheritance graph data structures:
   - **Class Registry**: `Dict[str, AutosarClass]` for O(1) class lookup by name
   - **Ancestry Cache**: `Dict[str, Set[str]]` mapping each class to all its ancestors
   - Recursively collect ancestors for each class by following its bases
   - Filter out ARObject from ancestry cache (implicit root)

2. For each class that has a non-empty `bases` list:
   - Filter out "ARObject" from the `bases` list (ARObject is the implicit root of all AUTOSAR classes)
   - Filter out bases that don't exist in the model (strict validation)
   - If no bases remain after filtering → parent = None
   - For each remaining base, check if it's an ancestor of any OTHER base:
     - If Base2 is in Base1's ancestry → Base1 is an ancestor, NOT direct parent
   - The direct parent is the base that is NOT an ancestor of any other base
   - If multiple candidates exist, pick the last one (backward compatibility)

3. For classes with only "ARObject" in their bases list:
   - Set `parent` attribute to "ARObject" (they inherit directly from the root)
   - These classes are NOT root classes (they have a parent)

4. Only classes with an empty `bases` list are considered root classes (ARObject itself)

5. Process all classes after all PDFs have been parsed to ensure complete model is available

**Ancestry-Based Parent Selection Algorithm**:

The critical insight is that in a base classes list like `[ClassA, ClassB, ClassC]`, some bases may be ancestors (not direct parents). The algorithm must build the complete inheritance hierarchy and traverse it to find the **ACTUAL direct parent**.

**Example 1: Identifying Direct Parent vs Ancestor**
```
Hierarchy:
  ARObject
    ├── ClassA
    │   └── ClassB (child of ClassA)
    └── ClassC (sibling of ClassA)

ClassD bases: [ClassA, ClassB, ClassC]

Analysis:
- ClassB is an ancestor (child of ClassA), NOT direct parent
- ClassA is an ancestor (parent of ClassB), NOT direct parent
- ClassC is a direct parent (not an ancestor of any other base)

Result: ClassD.parent = "ClassC" (actual direct parent)
```

**Example 2: Deep Hierarchy Traversal**
```
Hierarchy:
  ARObject → Level1 → Level2 → Level3 → Level4

DerivedWithMultipleBases bases: [Level1, Level2, Level3, Level4]

Analysis:
- Level4 is the most recent (direct parent)
- Level1, Level2, Level3 are all ancestors of Level4
- Algorithm filters out ancestors, selects Level4

Result: DerivedWithMultipleBases.parent = "Level4"
```

**Example 3: Missing Base Class Handling (Strict Validation)**
```
ExistingClass in model
NonExistentBase NOT in model

DerivedClass bases: [ExistingClass, NonExistentBase]

Analysis:
- Filter out NonExistentBase (doesn't exist in model)
- Only ExistingClass remains as valid base
- ExistingClass becomes the direct parent

Result: DerivedClass.parent = "ExistingClass"
```

**Root Class Definition**:
- Root classes are those with NO base classes (empty `bases` list)
- Typically only ARObject itself is a root class
- ARObject has `parent = None` and `bases = []`
- Classes with only ARObject as base have `parent = "ARObject"` (they're children of ARObject, not roots)

**Backward Compatibility**:
- For simple single inheritance, behavior is unchanged (parent is the only base)
- For multiple independent bases (no ancestry relationships), picks last base
- For complex hierarchies with ancestry relationships, correctly identifies direct parent

This requirement enables:
- Automatic parent-child relationship establishment with ancestry-based parent selection
- Distinguishing between direct parents and ancestors in complex inheritance hierarchies
- Correct hierarchy representation even with multiple inheritance and deep hierarchies
- Support for traversing the complete inheritance hierarchy by following parent references
- Strict validation to handle missing base classes gracefully

**Note**: This requirement complements SWR_MODEL_00022 (AUTOSAR Class Parent Attribute) by describing how the `parent` attribute is automatically populated during PDF parsing using ancestry analysis to find the actual direct parent (not just picking a base from the list). Subclasses validation is performed separately in SWR_PARSER_00029 to ensure consistency between the `subclasses` attribute and the inheritance hierarchy.

---

### SWR_PARSER_00018
**Title**: Multiple PDF Parsing with Complete Model Resolution

**Maturity**: accept

**Description**: When parsing multiple PDF files, the system shall extract all class definitions from all PDFs before building the package hierarchy and resolving parent/children relationships, to ensure complete model analysis.

The system shall:
1. When parsing multiple PDF files:
   - Extract all class definitions from all PDF files first (without resolving parent/children)
   - Accumulate all class definitions into a single list
   - Build the complete package hierarchy once from all accumulated class definitions
   - Resolve parent/children relationships once on the complete model
2. Ensure that parent classes are found even if they are defined in later PDFs
3. Support both single-PDF parsing (`parse_pdf()`) and multi-PDF parsing (`parse_pdfs()`)
4. Return a single `AutosarDoc` containing the complete merged model

**Workflow**:
- **Single PDF**: parse_pdf() → extract classes → build hierarchy → resolve parents → return AutosarDoc
- **Multiple PDFs**: parse_pdfs() → extract all classes → build complete hierarchy → resolve parents once → return AutosarDoc

**Rationale**:
- Parent/children relationships cannot be correctly resolved if only partial model is available
- A class in PDF1 may have a parent defined in PDF2, which would be missed with per-PDF resolution
- Resolving after all PDFs ensures complete and accurate inheritance hierarchy
- Prevents missing parent references due to parse order dependencies

This requirement enables:
- Correct parent/children resolution across multiple PDF files
- Complete model analysis regardless of PDF parse order
- Accurate inheritance hierarchy representation
- Support for large AUTOSAR specifications split across multiple PDFs

**Note**: This requirement works with SWR_PARSER_00017 (AUTOSAR Class Parent Resolution) to ensure parent/children are resolved on the complete model rather than partial per-PDF models.

---

### SWR_PARSER_00019
**Title**: PDF Library Warning Suppression

**Maturity**: accept

**Description**: The system shall suppress pdfplumber warnings that do not affect parsing functionality to prevent console noise from invalid PDF specifications.

The system shall:
1. Suppress pdfplumber warnings related to invalid color values and other non-critical PDF specification issues
2. Use Python's `warnings` module to filter pdfplumber warnings during PDF extraction
3. Only suppress warnings that do not affect the correctness of AUTOSAR model extraction
4. Allow critical errors (exceptions) to propagate normally

**Examples of Suppressed Warnings**:
- "Cannot set gray non-stroke color because /'P227' is an invalid float value"
- Invalid color space warnings
- Font rendering warnings (when they don't affect text extraction)
- Other pdfplumber/internal PDF specification warnings that don't affect parsing results

**Rationale**:
- Many AUTOSAR PDFs have minor PDF specification errors that don't affect text extraction
- These warnings create unnecessary console noise and may confuse users
- The extracted AUTOSAR model is still correct despite these warnings
- Users should only see warnings and errors that affect the actual parsing results

**Implementation**:
- Use `warnings.filterwarnings()` to suppress pdfplumber warnings
- Apply filtering in the `_extract_with_pdfplumber()` method
- Ensure actual parsing errors (exceptions) are not suppressed

This requirement ensures a clean user experience while maintaining correct parsing functionality.

---

### SWR_PARSER_00020
**Title**: Missing Base Class Logging with Deduplication

**Maturity**: accept

**Description**: The system shall collect and log warnings when base classes cannot be located in the model during parent resolution and ancestry traversal to help users identify incomplete or incorrect AUTOSAR models.

The system shall:
1. Build class registry and ancestry cache only once per parse operation (not per recursive call)
2. Collect missing base class errors into a buffer during parent resolution analysis (not immediate logging)
3. Collect missing class references during ancestry traversal into a shared buffer
4. Store each unique error only once (deduplication by class name)
5. Print all buffered warnings after the parent resolution analysis is complete
6. Log one warning per missing base class (not grouped by referencing class)
7. Log one warning per missing class from ancestry traversal (not per reference)

**Warning Messages**:
- For each missing base class from parent resolution: `"Class '<missing_base_class>' could not be located in the model"`
- For each missing class from ancestry traversal: `"Class '<missing_class>' referenced in base classes could not be located in the model during ancestry traversal. Ancestry analysis may be incomplete."`

**Rationale**:
- Incomplete AUTOSAR models may reference classes that are defined in other PDF files not included in the current parsing run
- Typo in base class names or missing definitions can lead to incomplete parent/children relationships
- Logging these warnings helps users identify and fix incomplete models
- Buffering and deduplication prevents log spam and provides cleaner, consolidated error reporting
- Building data structures once improves performance by avoiding redundant computation
- Sorting missing class names alphabetically ensures consistent output

**Implementation**:
- Check for missing base classes in `_set_parent_references()` method after filtering
- Buffer errors in a dictionary with keys as `"<classname> (in <packagename>)"` and values as sets of missing base class names
- Build class registry and ancestry cache only on initial call to `_set_parent_references()`, pass to recursive calls
- Collect missing classes from `_build_ancestry_cache()` into a shared buffer
- Use sets to ensure automatic deduplication of missing base class names
- Print one warning per unique missing base class after analysis completes
- Log at WARNING level to ensure visibility without being errors

This requirement enables users to identify and resolve incomplete or incorrect AUTOSAR model definitions through consolidated, non-repetitive warning messages while avoiding performance issues from redundant data structure building.

---

### SWR_PARSER_00021
**Title**: Multi-Line Attribute Parsing for AutosarClass

**Maturity**: accept

**Description**: The system shall handle multi-line parsing for various AutosarClass attributes in PDF class definitions to ensure complete extraction of all attribute values that span multiple lines.

The system shall:
1. Detect when AutosarClass attribute lists span multiple lines in the PDF due to table formatting
2. Apply multi-line parsing to the following class attributes:
   - **Base classes**: List of parent class names (comma-separated)
   - **Aggregated by**: List of class names that aggregate this class (comma-separated)
   - **Subclasses**: List of child class names explicitly listed in the PDF (comma-separated). The subclasses are descendants of this class that inherit from it. A subclass cannot be the parent of this class, and it also cannot be in the bases list of this class's parent.
   - Any other comma-separated class reference attributes that may be added in the future
3. For each attribute, recognize continuation lines that:
   - Come immediately after the attribute header line (e.g., "Base ", "Aggregated by ", "Subclasses ")
   - Do not match any known pattern (Class, Primitive, Enumeration, Package, Note, Attribute, etc.)
   - Look like comma-separated class names (contain commas or start with continuation of previous line)
4. Concatenate continuation lines with the attribute list
5. Handle word splitting across lines (e.g., "Packageable" at end of line + "Element" at start of next line = "PackageableElement")
   - The delimiter for class lists is a comma (,)
   - When a continuation line starts with a word that should be concatenated with the last item from the previous line (e.g., "NeedsBlueprintSet" after "Consistency"), concatenate them to form the complete class name
   - Detect continuation when the first word on the continuation line: starts with lowercase, is a known continuation fragment, contains a known AUTOSAR suffix (e.g., "Set", "Props", "Pool", "Info", "Element"), or is very short (<=3 characters)
   - Also detect continuation when the last item from the previous line is very short (<=3 characters) or ends with a known prefix
6. Stop continuation when encountering another known pattern (Note, Attribute, Class, Primitive, Enumeration, Package, or another attribute header)

**Example 1: Multi-Line Base Classes (from AUTOSAR_CP_TPS_SystemTemplate.pdf)**:
```
Class CanTpConfig
Package M2::AUTOSARTemplates::SystemTemplate::TransportProtocols
Base ARObject,CollectableElement,FibexElement,Identifiable,MultilanguageReferrable,Packageable
Element,Referrable,TpConfig
Note This element defines exactly one CANTPConfiguration.
```

The base classes list wraps across two lines:
- Line 1: `Base ARObject,CollectableElement,FibexElement,Identifiable,MultilanguageReferrable,Packageable`
- Line 2: `Element,Referrable,TpConfig` (continuation)

Without multi-line parsing, only the first line is read, resulting in:
- Missing: `PackageableElement` (should combine "Packageable" + "Element")
- Missing: `Referrable`
- Missing: `TpConfig` (the actual parent!)

With multi-line parsing, the complete base list is:
- ARObject, CollectableElement, FibexElement, Identifiable, MultilanguageReferrable
- PackageableElement (combined from "Packageable" + "Element")
- Referrable, TpConfig (critical for parent resolution)

**Example 2: Multi-Line Aggregated By**:
```
Class SwDataDefProps
Package M2::AUTOSAR::DataTypes
Aggregated by ApplicationSwComponentPrototype,InternalBehavior,Prototype,SwComponent
Type,Trigger,SwDataDefPropsConditional
```

The aggregated by list wraps across two lines:
- Line 1: `Aggregated by ApplicationSwComponentPrototype,InternalBehavior,Prototype,SwComponent`
- Line 2: `Type,Trigger,SwDataDefPropsConditional` (continuation)

Without multi-line parsing, only the first line is read, missing:
- SwComponentType (should combine "SwComponent" + "Type")
- Trigger
- SwDataDefPropsConditional

**Example 3: Multi-Line Subclasses**:
```
Class Identifiable
Package M2::AUTOSAR
Subclasses ApplicationSwComponentType,InternalBehavior,Prototype,Referrable,Trigger,
SwDataDefProps,SwComponentType
Note This class is the base for all identifiable elements.
```

The subclasses list wraps across two lines:
- Line 1: `Subclasses ApplicationSwComponentType,InternalBehavior,Prototype,Referrable,Trigger,SwDataDefProps,SwComponent`
- Line 2: `Type` (continuation)

Without multi-line parsing, only the first line is read, resulting in:
- Missing: `SwComponentType` (should combine "SwComponent" + "Type")

With multi-line parsing, the complete subclasses list is:
- ApplicationSwComponentType, InternalBehavior, Prototype, Referrable, Trigger
- SwComponentType (combined from "SwComponent" + "Type")

**Rationale**:
- PDF table formatting often causes attribute lists to wrap across multiple lines
- Missing attribute values leads to incomplete model representation
- Word splitting across line boundaries must be handled correctly (e.g., "Packageable" + "Element" = "PackageableElement")
- Without complete base class lists, parent resolution fails (e.g., CanTpConfig.parent would be incorrectly set)
- Without complete "aggregated by" lists, aggregation relationships are incomplete
- Without complete "subclasses" lists, the explicitly listed subclass relationships in the PDF are lost

**Implementation**:
- Track state when parsing each attribute section (generalized `in_attribute_section` flag)
- For each attribute type, maintain a pending list for continuation
- Track `last_item_name` to handle word splitting across lines
- Detect continuation lines by checking if line doesn't match known patterns
- Combine split words when first word of continuation line starts with lowercase or is a known continuation fragment
- Finalize attribute list when hitting Note, Attribute section, or class definition patterns
- Apply the same continuation logic to all comma-separated class reference attributes

This requirement ensures complete model representation by guaranteeing that all attribute values are extracted from multi-line attribute lists in PDFs, including base classes, aggregated by, subclasses, and future comma-separated class reference attributes.

---

### SWR_PARSER_00022
**Title**: PDF Source Location Extraction

**Maturity**: accept

**Description**: The PDF parser shall track source locations (PDF file and page number) during parsing. The parser shall:
- Extract PDF filename from the file path for cleaner output
- Track current page number during PDF processing (1-indexed)
- Attach source information to ClassDefinition objects when creating class definitions
- Transfer source info from ClassDefinition to model objects during hierarchy building

This requirement enables:
- Complete traceability of where each AUTOSAR type was defined

---

### SWR_PARSER_00023
**Title**: Abstract Base Parser for Common Functionality

**Maturity**: draft

**Description**: The system shall provide an abstract base parser class that defines common parsing functionality shared across all AUTOSAR type parsers. This shall include:
- Common regex patterns for parsing (CLASS_PATTERN, PRIMITIVE_PATTERN, ENUMERATION_PATTERN, PACKAGE_PATTERN, NOTE_PATTERN, ATTRIBUTE_HEADER_PATTERN, etc.)
- Common validation methods (package path validation, ATP marker validation, reference type detection, attribute filtering)
- Common attribute creation methods
- Constants for continuation types, fragment names, reference indicators
- Abstract methods for type-specific parsing

---

### SWR_PARSER_00024
**Title**: AutosarClass Specialized Parser

**Maturity**: draft

**Description**: The system shall provide a specialized parser for AutosarClass definitions that inherits from the abstract base parser. This parser shall:
- Maintain its own parsing state (pending attributes, class lists, etc.)
- Parse class definition patterns with ATP markers and abstract status
- Create AutosarClass objects directly (no intermediate ClassDefinition)
- Parse class-specific sections: base classes, subclasses, aggregated by, notes, attributes
- Handle multi-line attribute parsing
- Manage attribute parsing state across multiple pages

---

### SWR_PARSER_00025
**Title**: AutosarEnumeration Specialized Parser

**Maturity**: draft

**Description**: The system shall provide a specialized parser for AutosarEnumeration definitions that inherits from the abstract base parser. This parser shall:
- Maintain its own parsing state
- Parse enumeration definition patterns
- Create AutosarEnumeration objects directly (no intermediate ClassDefinition)
- Parse enumeration literal headers
- Parse enumeration literals with indices
- Extract literal indices from descriptions
- Handle enumeration literal section termination

---

### SWR_PARSER_00026
**Title**: AutosarPrimitive Specialized Parser

**Maturity**: draft

**Description**: The system shall provide a specialized parser for AutosarPrimitive definitions that inherits from the abstract base parser. This parser shall:
- Maintain its own parsing state
- Parse primitive definition patterns
- Create AutosarPrimitive objects directly (no intermediate ClassDefinition)
- Parse primitive attributes (simplified version)
- Parse primitive notes

---

### SWR_PARSER_00027
**Title**: Parser Backward Compatibility

**Maturity**: draft

**Description**: The refactored parser shall maintain 100% backward compatibility with the existing PdfParser API. All existing code using PdfParser shall continue to work without modification. The public interface shall remain identical.

---

### SWR_PARSER_00028
**Title**: Direct Model Creation by Specialized Parsers

**Maturity**: draft

**Description**: Specialized parsers shall create final model objects (AutosarClass, AutosarEnumeration, AutosarPrimitive) directly during parsing, without using an intermediate ClassDefinition dataclass. Each parser shall maintain its own parsing state and return the completed model object.

---

### SWR_PARSER_00029
**Title**: Subclasses Contradiction Validation

**Maturity**: accept

**Description**: During parent and base class list analysis, the system shall validate that the `subclasses` attribute of each class does not contain any contradictions with the inheritance hierarchy defined by the `bases` and `parent` attributes.

The system shall:
1. For each class that has a non-empty `subclasses` list, validate each listed subclass:
   - **Subclass Base Validation**: Verify that the subclass actually exists in the model
   - **Subclass Inheritance Validation**: Verify that the subclass has this class in its `bases` list (i.e., the subclass actually inherits from this class)
   - **Circular Relationship Validation**: Verify that the subclass is NOT in the `bases` list of this class (circular inheritance is invalid)
   - **Ancestor Validation**: Verify that the subclass is NOT in the `bases` list of this class's parent (which would make the subclass an ancestor, not a descendant)
   - **Parent Validation**: Verify that the subclass is NOT the parent of this class

2. Raise an exception when any contradiction is detected with a clear error message indicating:
   - The class name that has the invalid subclass
   - The subclass name that caused the contradiction
   - The type of contradiction found (e.g., "Subclass does not inherit from this class", "Circular inheritance detected", "Subclass is an ancestor, not a descendant")

3. Perform this validation after all parent relationships have been resolved to ensure complete inheritance hierarchy information is available

**Validation Rules**:
- A subclass MUST have the parent class in its `bases` list
- A subclass CANNOT be in the parent class's `bases` list (circular relationship)
- A subclass CANNOT be in the parent class's parent's `bases` list (would be an ancestor)
- A subclass CANNOT be the parent class itself

**Example 1: Valid Subclass Relationship**
```
ClassA (subclasses: [ClassB])
ClassB (bases: [ClassA])

Validation: PASS - ClassB has ClassA in its bases list
```

**Example 2: Invalid - Subclass Does Not Inherit**
```
ClassA (subclasses: [ClassB])
ClassB (bases: [ClassC])

Validation: FAIL - ClassB does not have ClassA in its bases list
Error: "Class 'ClassB' is listed as a subclass of 'ClassA' but does not inherit from it"
```

**Example 3: Invalid - Circular Relationship**
```
ClassA (subclasses: [ClassB], bases: [ClassB])
ClassB (bases: [ClassA])

Validation: FAIL - ClassB is in ClassA's bases list (circular)
Error: "Circular inheritance detected: 'ClassB' is both a subclass and a base of 'ClassA'"
```

**Example 4: Invalid - Subclass is an Ancestor**
```
ClassA (subclasses: [ClassB], parent: ClassC)
ClassB (bases: [ClassD])
ClassC (bases: [ClassB])

Validation: FAIL - ClassB is in ClassA's parent's bases list (ancestor)
Error: "Class 'ClassB' is listed as a subclass of 'ClassA' but is an ancestor (in bases of parent 'ClassC')"
```

**Rationale**:
- The `subclasses` attribute represents explicitly documented subclass relationships in the PDF
- These relationships must be consistent with the actual inheritance hierarchy defined by `bases` and `parent`
- Detecting contradictions early prevents incorrect model representation and helps identify errors in the PDF specification
- Subclasses are descendants that inherit from this class, not ancestors or siblings

**Implementation**:
- Perform validation in the parent resolution phase after all parent relationships are established
- Use the class registry for O(1) class lookup by name
- Raise `ValueError` with descriptive messages for each type of contradiction
- Validate all classes to ensure complete consistency across the model