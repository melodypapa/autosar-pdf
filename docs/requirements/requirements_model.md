# Model Requirements

This document contains all software requirements for the autosar-pdf2txt data model.

## Maturity Levels

Each requirement has a maturity level that indicates its status:

- **draft**: Newly created requirement, under review, or not yet implemented
- **accept**: Accepted requirement, implemented in the codebase
- **invalid**: Deprecated requirement, superseded, or no longer applicable

---

### SWR_MODEL_00001
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
- `subclasses`: List of subclass names explicitly listed in the PDF source document (List[str], defaults to empty list)
- `aggregated_by`: List of class names that aggregate this class (List[str], defaults to empty list)
- `note`: Optional free-form text for documentation or comments (str | None, defaults to None)

The ATP type enum shall support the following values:
- `NONE`: No ATP marker present
- `ATP_MIXED_STRING`: The class has the <<atpMixedString>> marker
- `ATP_VARIATION`: The class has the <<atpVariation>> marker
- `ATP_MIXED`: The class has the <<atpMixed>> marker

---

### SWR_MODEL_00002
**Title**: AUTOSAR Class Name Validation

**Maturity**: accept

**Description**: The system shall validate that AUTOSAR class names are non-empty and do not contain only whitespace upon initialization.

---

### SWR_MODEL_00003
**Title**: AUTOSAR Class String Representation

**Maturity**: accept

**Description**: The system shall provide string representations of AUTOSAR classes, including:
- A user-friendly string with "(abstract)" suffix for abstract classes
- A debug representation showing all attributes

---

### SWR_MODEL_00004
**Title**: AUTOSAR Package Representation

**Maturity**: accept

**Description**: The system shall provide a data model to represent an AUTOSAR package with the following attributes:
- `name`: The name of the package (non-empty string)
- `types`: List of AutosarClass and AutosarEnumeration objects contained in the package (unified type collection)
- `subpackages`: List of AutosarPackage objects (nested packages)

**Note**: The `types` attribute provides a unified collection for both classes and enumerations. For backward compatibility, the package also provides class-specific methods (add_class, get_class, has_class) that work with this unified types collection.

---

### SWR_MODEL_00005
**Title**: AUTOSAR Package Name Validation

**Maturity**: accept

**Description**: The system shall validate that AUTOSAR package names are non-empty and do not contain only whitespace upon initialization.

---

### SWR_MODEL_00006
**Title**: Add Class to Package

**Maturity**: accept

**Description**: The system shall provide functionality to add an AutosarClass to an AutosarPackage. The system shall check for duplicate classes by class name. If a class with the same name already exists in the package, the class shall not be added again.

---

### SWR_MODEL_00007
**Title**: Add Subpackage to Package

**Maturity**: accept

**Description**: The system shall provide functionality to add an AutosarPackage as a subpackage to another AutosarPackage. The system shall check for duplicate subpackages by subpackage name. If a subpackage with the same name already exists in the parent package, the subpackage shall not be added again.

---

### SWR_MODEL_00008
**Title**: Query Package Contents

**Maturity**: accept

**Description**: The system shall provide query methods to:
- Get a class by name from a package
- Get a subpackage by name from a package
- Check if a class exists in a package
- Check if a subpackage exists in a package

---

### SWR_MODEL_00009
**Title**: Package String Representation

**Maturity**: accept

**Description**: The system shall provide string representations of AUTOSAR packages, including summary information about the number of classes and subpackages.

---

### SWR_MODEL_00010
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

### SWR_MODEL_00011
**Title**: AUTOSAR Attribute Name Validation

**Maturity**: accept

**Description**: The system shall validate that AUTOSAR attribute names are non-empty and do not contain only whitespace upon initialization.

---

### SWR_MODEL_00012
**Title**: AUTOSAR Attribute Type Validation

**Maturity**: accept

**Description**: The system shall validate that AUTOSAR attribute types are non-empty and do not contain only whitespace upon initialization.

---

### SWR_MODEL_00013
**Title**: AUTOSAR Attribute String Representation

**Maturity**: accept

**Description**: The system shall provide string representations of AUTOSAR attributes, including:
- A user-friendly string showing attribute name, type, reference indicator, multiplicity, kind, and note
- A debug representation showing all attributes (name, type, is_ref, multiplicity, kind, note)

---

### SWR_MODEL_00014
**Title**: AUTOSAR Enumeration Literal Representation

**Maturity**: accept

**Description**: The system shall provide a data model to represent an AUTOSAR enumeration literal with the following attributes:
- `name`: The name of the enumeration literal (non-empty string)
- `index`: The optional index of the literal (int | None, defaults to None)
- `description`: Optional description of the literal (str | None, defaults to None)

---

### SWR_MODEL_00015
**Title**: AUTOSAR Enumeration Literal Name Validation

**Maturity**: accept

**Description**: The system shall validate that enumeration literal names are non-empty and do not contain only whitespace upon initialization.

---

### SWR_MODEL_00016
**Title**: AUTOSAR Enumeration Literal String Representation

**Maturity**: accept

**Description**: The system shall provide string representations of enumeration literals, including:
- A user-friendly string showing literal name with "(index=<n>)" suffix if index is present
- A debug representation showing all attributes (name, index, description)

---

### SWR_MODEL_00017
**Title**: AUTOSAR Class Enumeration Literal Support

**Maturity**: invalid

**Description**: This requirement has been superseded by SWR_MODEL_00019 (AUTOSAR Enumeration Type Representation).

The original approach of adding enumeration literals to AutosarClass has been replaced with a dedicated AutosarEnumeration class that inherits from AbstractAutosarBase. This provides better type separation and clearer domain modeling.

**Superseded by**: SWR_MODEL_00019

---

### SWR_MODEL_00018
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

### SWR_MODEL_00019
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

### SWR_MODEL_00020
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

### SWR_MODEL_00021
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

### SWR_MODEL_00022
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

### SWR_MODEL_00023
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

### SWR_MODEL_00024
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

### SWR_MODEL_00025
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

### SWR_MODEL_00026
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

### SWR_MODEL_00027
**Title**: AUTOSAR Source Location Representation

**Maturity**: accept

**Description**: The system shall provide a data model to represent source location information for AUTOSAR types. The source location shall include:
- `pdf_file`: Path to the PDF file (relative or absolute)
- `page_number`: Page number in the PDF (1-indexed)
- `autosar_standard`: Optional AUTOSAR standard identifier (e.g., "Foundation", "Classic Platform", "Adaptive Platform", "Methodology")
- `standard_release`: Optional AUTOSAR standard release (e.g., "R23-11", "R22-11", "R24-03")

The source location shall be:
- Immutable (frozen dataclass)
- Optional for all AUTOSAR types (backward compatibility)
- Attachable to any type inheriting from AbstractAutosarBase