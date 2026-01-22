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
- `package`: The full package path in PDF format (e.g., "M2::MSR::DataDictionary::RecordLayout")
- `is_abstract`: Boolean flag indicating whether the class is abstract
- `atp_type`: ATP marker type enum indicating the AUTOSAR Tool Platform marker (defaults to NONE)
- `attributes`: Dictionary of AUTOSAR attributes where key is the attribute name and value is the AUTOSAR attribute object
- `bases`: List of base class names for inheritance tracking (List[str], defaults to empty list)
- `parent`: Name of the immediate parent class from the bases list (Optional[str], None for root classes)
- `children`: List of child class names that inherit from this class (List[str], defaults to empty list)
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
- `types`: List of AutosarClass and AutosarEnumeration objects contained in the package (unified type collection)
- `subpackages`: List of AutosarPackage objects (nested packages)

**Note**: The `types` attribute provides a unified collection for both classes and enumerations. For backward compatibility, the package also provides class-specific methods (add_class, get_class, has_class) that work with this unified types collection.

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
- `multiplicity`: The multiplicity of the attribute (e.g., "0..1", "*", "0..*")
- `kind`: The kind of attribute as an AttributeKind enum value:
  - `AttributeKind.ATTR`: Regular attribute (non-aggregated)
  - `AttributeKind.AGGR`: Aggregated attribute (contains sub-attributes)
  - `AttributeKind.REF`: Reference attribute (points to another AUTOSAR element)
- `note`: The description or note for the attribute

The AttributeKind enum shall define the following values:
- `ATTR`: Represents a regular attribute with a simple data type
- `AGGR`: Represents an aggregated attribute that contains nested attributes
- `REF`: Represents a reference attribute that points to another AUTOSAR element

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
- A user-friendly string showing attribute name, type, reference indicator, multiplicity, kind, and note
- A debug representation showing all attributes (name, type, is_ref, multiplicity, kind, note)

---

#### SWR_MODEL_00014
**Title**: AUTOSAR Enumeration Literal Representation

**Maturity**: accept

**Description**: The system shall provide a data model to represent an AUTOSAR enumeration literal with the following attributes:
- `name`: The name of the enumeration literal (non-empty string)
- `index`: The optional index of the literal (int | None, defaults to None)
- `description`: Optional description of the literal (str | None, defaults to None)

---

#### SWR_MODEL_00015
**Title**: AUTOSAR Enumeration Literal Name Validation

**Maturity**: accept

**Description**: The system shall validate that enumeration literal names are non-empty and do not contain only whitespace upon initialization.

---

#### SWR_MODEL_00016
**Title**: AUTOSAR Enumeration Literal String Representation

**Maturity**: accept

**Description**: The system shall provide string representations of enumeration literals, including:
- A user-friendly string showing literal name with "(index=<n>)" suffix if index is present
- A debug representation showing all attributes (name, index, description)

---

#### SWR_MODEL_00017
**Title**: AUTOSAR Class Enumeration Literal Support

**Maturity**: invalid

**Description**: This requirement has been superseded by SWR_MODEL_00019 (AUTOSAR Enumeration Type Representation).

The original approach of adding enumeration literals to AutosarClass has been replaced with a dedicated AutosarEnumeration class that inherits from AbstractAutosarBase. This provides better type separation and clearer domain modeling.

**Superseded by**: SWR_MODEL_00019

---

#### SWR_MODEL_00018
**Title**: AUTOSAR Type Abstract Base Class

**Maturity**: accept

**Description**: The system shall provide an abstract base class (`AbstractAutosarBase`) that encapsulates common properties shared by all AUTOSAR type definitions, including regular classes and enumerations.

The abstract base class shall include the following attributes:
- `name`: The name of the type (non-empty string)
- `package`: The full package path in PDF format (e.g., "M2::MSR::DataDictionary::RecordLayout")
- `note`: Optional documentation or comments about the type (str | None, defaults to None)

The abstract base class shall provide:
- Name validation in `__post_init__` to ensure non-empty names
- Abstract `__str__()` method that derived classes must implement
- Common initialization logic for all derived types

This requirement enables a proper inheritance hierarchy where both `AutosarClass` and `AutosarEnumeration` inherit from `AbstractAutosarBase`, eliminating code duplication and ensuring consistent behavior across all AUTOSAR type definitions.

---

#### SWR_MODEL_00019
**Title**: AUTOSAR Enumeration Type Representation

**Maturity**: accept

**Description**: The system shall provide a dedicated data model (`AutosarEnumeration`) to represent AUTOSAR enumeration types, inheriting from the `AbstractAutosarBase` abstract base class.

The `AutosarEnumeration` class shall include:
- All inherited attributes from `AbstractAutosarBase` (name, package, note)
- `enumeration_literals`: List of enumeration literal values (List[AutosarEnumLiteral], defaults to empty list)

The class shall:
- Inherit validation logic from `AbstractAutosarBase`
- Implement the abstract `__str__()` method to return the enumeration name
- Provide a debug representation showing all attributes including enumeration literals count

This allows the system to properly represent enumeration types like `EcucDestinationUriNestingContractEnum` from AUTOSAR CP TPS ECUConfiguration as a distinct type from regular classes, improving type safety and code clarity.

---

#### SWR_MODEL_00020
**Title**: AUTOSAR Package Type Support

**Maturity**: accept

**Description**: The system shall update the `AutosarPackage` data model to support both classes and enumerations through a unified `types` collection.

The `AutosarPackage` class shall:
- Replace the `classes` attribute with `types`: List[Union[AutosarClass, AutosarEnumeration]]
- Provide the following methods:
  - `add_type(typ)`: Add any type (class or enumeration) to the package
  - `add_class(cls)`: Add a class to the package (backward compatibility)
  - `add_enumeration(enum)`: Add an enumeration to the package
  - `get_type(name)`: Get any type by name
  - `get_class(name)`: Get a class by name (returns only AutosarClass instances)
  - `get_enumeration(name)`: Get an enumeration by name (returns only AutosarEnumeration instances)
  - `has_type(name)`: Check if any type exists
  - `has_class(name)`: Check if a class exists
  - `has_enumeration(name)`: Check if an enumeration exists
- Prevent duplicate type names across all types (both classes and enumerations)
- Update string representation to show "X types" instead of "X classes"

This requirement provides a unified interface for managing both classes and enumerations while maintaining backward compatibility through the `add_class()` method.

---

#### SWR_MODEL_00021
**Title**: AUTOSAR Class Multi-Level Inheritance Hierarchy

**Maturity**: accept

**Description**: The system shall support multi-level inheritance hierarchies for AUTOSAR classes, where a class can inherit from a base class, which in turn can inherit from its own base class, and so on (parent → grandparent → great-grandparent → ...).

The `AutosarClass` data model shall:
- Maintain the existing `bases` attribute (List[str]) that stores the immediate parent class names
- Support inheritance chains of arbitrary depth through the base class references
- Allow classes to have multiple immediate base classes (multiple inheritance)
- Preserve the complete inheritance path from the most derived class to the root ancestor(s)

This requirement enables the system to represent complex AUTOSAR class hierarchies such as:
- `SwComponentPrototype` → `Prototype` → `Identifiable` (3-level inheritance)
- `SwcInternalBehavior` → `InternalBehavior` → `Behavior` → `Identifiable` (4-level inheritance)
- Classes with multiple inheritance paths where a class inherits from multiple base classes

The inheritance hierarchy is represented through the `bases` list in each `AutosarClass`, which contains the names of the immediate parent classes. To traverse the complete inheritance chain, the system must recursively follow the `bases` references through all ancestor classes.

---

#### SWR_MODEL_00022
**Title**: AUTOSAR Class Parent Attribute

**Maturity**: accept

**Description**: The system shall provide a `parent` attribute in the `AutosarClass` data model to indicate the parent of this class.

The `AutosarClass` data model shall:
- Add a `parent` attribute that stores the name of the immediate parent class as a string
- The `parent` attribute shall be optional (None for root classes with no parent)
- The `parent` attribute shall be a single string value (not a list), representing the name of the first base class
- When a class has multiple bases (multiple inheritance), the `parent` attribute shall contain the name of the first/primary parent
- The `parent` attribute value must be one of the values in the `bases` list

This requirement enables:
- Direct reference to the parent class by name
- Simplified parent traversal without requiring object references
- Efficient parent-child relationship queries

**Note**: This attribute complements the existing `bases` attribute (which stores all parent class names as a list) by providing a direct reference to the primary parent.

---

#### SWR_MODEL_00023
**Title**: AUTOSAR Document Model (AutosarDoc)

**Maturity**: accept

**Description**: The system shall provide a data model (`AutosarDoc`) to represent the complete AUTOSAR model extracted from PDF files. The `AutosarDoc` class shall serve as the container for all parsed AUTOSAR data.

The `AutosarDoc` data model shall:

- **Package Hierarchy Storage**: Contain the package hierarchy as a list of top-level `AutosarPackage` objects
- **Root Class Collection**: Contain a list of root `AutosarClass` objects (classes with empty `bases` list)
- **Query Methods**: Provide methods to query:
  - Packages by name via `get_package()`
  - Root classes by name via `get_root_class()`

The `AutosarDoc` class shall provide the following attributes:

- `packages`: List of top-level `AutosarPackage` objects representing the package hierarchy
- `root_classes`: List of root `AutosarClass` objects (classes with no bases)

The `AutosarDoc` class shall validate that:
- No duplicate package names exist in the packages list
- No duplicate root class names exist in the root_classes list

This requirement enables:
- Structured access to all parsed AUTOSAR data
- Easy identification of root classes (classes with no parent)
- Simplified data access for the parser, writer, and CLI components

---

#### SWR_MODEL_00024
**Title**: AUTOSAR Primitive Type Representation

**Maturity**: accept

**Description**: The system shall provide a dedicated data model (`AutosarPrimitive`) to represent AUTOSAR primitive types, inheriting from the `AbstractAutosarBase` abstract base class.

The `AutosarPrimitive` class shall include:
- All inherited attributes from `AbstractAutosarBase` (name, package, note)
- `attributes`: Dictionary of AUTOSAR attributes (key: attribute name, value: AutosarAttribute)

The class shall:
- Inherit validation logic from `AbstractAutosarBase`
- Implement the abstract `__str__()` method to return the primitive type name
- Provide a debug representation showing all attributes including attributes count and note presence

This allows the system to properly represent primitive types like `Limit` from AUTOSAR CP TPS ECUConfiguration as a distinct type from regular classes and enumerations, improving type safety and code clarity.

---

#### SWR_MODEL_00025
**Title**: AUTOSAR Package Primitive Type Support

**Maturity**: accept

**Description**: The system shall update the `AutosarPackage` data model to support classes, enumerations, and primitives through a unified `types` collection.

The `AutosarPackage` class shall:
- Update the `types` attribute type to `List[Union[AutosarClass, AutosarEnumeration, AutosarPrimitive]]`
- Provide the following methods:
  - `add_type(typ)`: Add any type (class, enumeration, or primitive) to the package
  - `add_class(cls)`: Add a class to the package (backward compatibility)
  - `add_enumeration(enum)`: Add an enumeration to the package
  - `add_primitive(primitive)`: Add a primitive type to the package
  - `get_type(name)`: Get any type by name
  - `get_class(name)`: Get a class by name (returns only AutosarClass instances)
  - `get_enumeration(name)`: Get an enumeration by name (returns only AutosarEnumeration instances)
  - `get_primitive(name)`: Get a primitive type by name (returns only AutosarPrimitive instances)
  - `has_type(name)`: Check if any type exists
  - `has_class(name)`: Check if a class exists
  - `has_enumeration(name)`: Check if an enumeration exists
  - `has_primitive(name)`: Check if a primitive type exists
- Prevent duplicate type names across all types (classes, enumerations, and primitives)
- Update string representation to show "X types" instead of "X classes"

This requirement provides a unified interface for managing classes, enumerations, and primitives while maintaining backward compatibility through the existing `add_class()` and `add_enumeration()` methods.

---

#### SWR_MODEL_00026
**Title**: AUTOSAR Class Children Attribute

**Maturity**: accept

**Description**: The system shall provide a `children` attribute in the `AutosarClass` data model to track child classes that inherit from this class.

The `AutosarClass` data model shall:
- Add a `children` attribute that stores a list of child class names (List[str])
- The `children` attribute shall default to an empty list
- Child class names are strings representing the names of classes that have this class in their `bases` list
- The `children` attribute complements the `bases` attribute by providing a reverse reference for navigation

This requirement enables:
- Direct reference to all child classes by name
- Efficient parent-child relationship queries in both directions
- Simplified traversal of the inheritance hierarchy from parent to children

**Note**: This attribute complements the existing `bases` attribute (which stores parent class names) and `parent` attribute (which stores the immediate parent name) by providing a list of all direct children of this class.

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

#### SWR_PARSER_00005
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

#### SWR_PARSER_00006
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

#### SWR_PARSER_00007
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
3. Create AutosarAttribute objects with the extracted name, type, multiplicity, kind, and note
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
7. Create AutosarPrimitive objects for primitive type definitions
8. Create AutosarEnumeration objects for enumeration type definitions
9. Create AutosarClass objects for regular class definitions

This requirement ensures that the parser correctly handles the three types of class definitions used in AUTOSAR PDF specification documents:
- Regular classes: `Class ImplementationDataType`
- Primitive types: `Primitive Limit`
- Enumeration types: `Enumeration IntervalTypeEnum`

Without this requirement, the parser would fail to recognize when a new class starts after "Primitive" or "Enumeration" definitions, causing attributes from subsequent classes to be incorrectly added to the previous class. For example, without recognizing "Primitive Limit" as a new class, the `intervalType` attribute from the Limit class would be incorrectly added to the ImplementationDataType class.

---

#### SWR_PARSER_00014
**Title**: Enumeration Literal Header Recognition

**Maturity**: accept

**Description**: The system shall recognize enumeration literal table headers in PDF files to identify when enumeration literals should be extracted.

The system shall:
1. Recognize the "Literal Description" header pattern that indicates the start of an enumeration literal table
2. Track when parsing is within the enumeration literal section
3. Initialize enumeration literal parsing state when the header is detected

---

#### SWR_PARSER_00015
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

#### SWR_PARSER_00016
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

#### SWR_PARSER_00017
**Title**: AUTOSAR Class Parent Resolution

**Maturity**: accept

**Description**: After parsing all classes from a PDF file and building the AUTOSAR class hierarchy tree, the system shall automatically set the `parent` attribute for each class to reference the correct parent `AutosarClass` object.

The system shall:
1. After building the complete package hierarchy with all `AutosarClass` objects
2. For each class that has a non-empty `bases` list:
   - Search through all packages to find the parent `AutosarClass` object by name
   - Set the `parent` attribute to reference the first base class in the `bases` list
   - If the parent class is not found in any package, leave `parent` as None
3. For classes with an empty `bases` list, set `parent` to None (root classes)
4. Process classes in dependency order to ensure parent classes are resolved before child classes

This requirement enables:
- Automatic parent-child relationship establishment during parsing
- Direct object reference navigation from child to parent without searching
- Support for traversing the complete inheritance hierarchy by following parent references

**Note**: This requirement complements SWR_MODEL_00022 (AUTOSAR Class Parent Attribute) by describing how the `parent` attribute is automatically populated during PDF parsing.

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
- Attributes displayed in a table format with columns: Attribute | Type | Mult. | Kind | Note

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
- Parent: The immediate parent class name from the parent attribute (included only when parent is not None)
- ATP Type section: List of ATP markers based on the ATP type enum value, included only when the ATP type is not NONE
- Base classes: List of base class names that this class inherits from
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

---

#### SWR_WRITER_00007
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

**Description**: When the `--include-class-details` flag is specified along with the `-o` / `--output` option, the CLI shall create separate markdown files for each AUTOSAR class in a directory structure that mirrors the package hierarchy. The root directory for the class files shall be the same as the output markdown file location.

---

#### SWR_CLI_00011
**Title**: CLI Class Files Flag

**Maturity**: accept

**Description**: The CLI shall support a `--include-class-details` flag to enable creation of separate markdown files for each class. This flag only has effect when used with the `-o` / `--output` option. When not specified, only the main hierarchy output file is created.

---

#### SWR_CLI_00012
**Title**: CLI Class Hierarchy Flag

**Maturity**: accept

**Description**: The CLI shall support a `--include-class-hierarchy` flag to enable generation of class inheritance hierarchy in a separate markdown file. When this flag is specified along with the `-o` / `--output` option, the system shall:
- Collect all classes from parsed packages
- Generate a class hierarchy section showing inheritance relationships from root classes
- Write the class hierarchy to a separate markdown file named `<output-file>-hierarchy.md`
- Not modify the main package hierarchy output file

The separate hierarchy file shall be created in the same directory as the main output file, with the filename generated by inserting "-hierarchy" before the file extension.

---

### 5. Package

#### SWR_PACKAGE_00001
**Title**: Package API Export

**Maturity**: accept

**Description**: The system shall export the following public API from the root package:
- `AttributeKind` (Enum)
- `AutosarAttribute` (Dataclass)
- `AutosarClass` (Dataclass)
- `AutosarDoc` (Dataclass)
- `AutosarEnumLiteral` (Dataclass)
- `AutosarEnumeration` (Dataclass)
- `AutosarPackage` (Dataclass)
- `AutosarPrimitive` (Dataclass)
- `PdfParser` (Class)
- `MarkdownWriter` (Class)
- `__version__` (String)

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
