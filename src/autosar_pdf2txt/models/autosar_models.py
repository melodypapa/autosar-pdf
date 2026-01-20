"""AUTOSAR data models for packages and classes."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Union


class ATPType(Enum):
    """AUTOSAR Tool Platform marker type.

    Requirements:
        SWR_MODEL_00001: AUTOSAR Class Representation

    This enum represents the ATP (AUTOSAR Tool Platform) marker type that can be
    associated with AUTOSAR classes.

    Attributes:
        NONE: No ATP marker present
        ATP_MIXED_STRING: The class has the <<atpMixedString>> marker
        ATP_VARIATION: The class has the <<atpVariation>> marker
        ATP_MIXED: The class has the <<atpMixed>> marker
    """

    NONE = "none"
    ATP_MIXED_STRING = "atpMixedString"
    ATP_VARIATION = "atpVariation"
    ATP_MIXED = "atpMixed"


class AttributeKind(Enum):
    """AUTOSAR attribute kind enumeration.

    Requirements:
        SWR_MODEL_00010: AUTOSAR Attribute Representation

    This enum represents the kind of AUTOSAR attribute, indicating whether it is
    a regular attribute or an aggregated attribute.

    Attributes:
        ATTR: Regular attribute
        AGGR: Aggregated attribute
    """

    ATTR = "attr"
    AGGR = "aggr"


@dataclass
class AutosarEnumLiteral:
    """Represents an enumeration literal value.

    Requirements:
        SWR_MODEL_00014: AUTOSAR Enumeration Literal Representation

    Attributes:
        name: The name of the enumeration literal.
        index: The optional index of the literal (e.g., atp.EnumerationLiteralIndex=0).
        description: Optional description of the literal.

    Examples:
        >>> literal = AutosarEnumLiteral("leafOfTargetContainer", 0, "Elements directly owned by target container")
        >>> literal_no_index = AutosarEnumLiteral("targetContainer", description="Target container")
    """

    name: str
    index: Optional[int] = None
    description: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate the literal fields.

        Requirements:
            SWR_MODEL_00015: AUTOSAR Enumeration Literal Name Validation

        Raises:
            ValueError: If name is empty or contains only whitespace.
        """
        if not self.name or not self.name.strip():
            raise ValueError("Enumeration literal name cannot be empty")

    def __str__(self) -> str:
        """Return string representation of the literal.

        Requirements:
            SWR_MODEL_00016: AUTOSAR Enumeration Literal String Representation

        Returns:
            Literal name with index suffix if present.
        """
        suffix = f" (index={self.index})" if self.index is not None else ""
        return f"{self.name}{suffix}"

    def __repr__(self) -> str:
        """Return detailed representation for debugging.

        Requirements:
            SWR_MODEL_00016: AUTOSAR Enumeration Literal String Representation
        """
        return (
            f"AutosarEnumLiteral(name='{self.name}', "
            f"index={self.index}, description={self.description is not None})"
        )


@dataclass
class AbstractAutosarBase(ABC):
    """Abstract base class for AUTOSAR type definitions.

    Requirements:
        SWR_MODEL_00018: AUTOSAR Type Abstract Base Class

    This abstract class encapsulates common properties shared by all AUTOSAR type
    definitions, including regular classes and enumerations.

    Attributes:
        name: The name of the type.
        package: The full package path in PDF format (e.g., "M2::MSR::DataDictionary::RecordLayout").
        note: Optional documentation or comments about the type.

    Examples:
        >>> type_obj = AbstractAutosarBase("MyType")  # This would fail - can't instantiate abstract class
        >>> # Instead, use AutosarClass or AutosarEnumeration
    """

    name: str
    package: str
    note: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate the type fields.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class

        Raises:
            ValueError: If name is empty or contains only whitespace.
        """
        if not self.name or not self.name.strip():
            raise ValueError("Type name cannot be empty")

    @abstractmethod
    def __str__(self) -> str:
        """Return string representation of the type.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class

        Returns:
            Type name with appropriate formatting.
        """
        pass  # pragma: no cover (abstract method)


@dataclass
class AutosarAttribute:
    """Represents an AUTOSAR class attribute.

    Requirements:
        SWR_MODEL_00010: AUTOSAR Attribute Representation

    Attributes:
        name: The name of the attribute.
        type: The data type of the attribute.
        is_ref: Whether the attribute is a reference type.
        multiplicity: The multiplicity of the attribute (e.g., "0..1", "*", "0..*").
        kind: The kind of attribute (attr or aggr).
        note: The description or note for the attribute.

    Examples:
        >>> attr = AutosarAttribute("dataReadPort", "PPortPrototype", True, "0..1", AttributeKind.ATTR, "Data read port")
        >>> non_ref_attr = AutosarAttribute("id", "uint32", False, "0..1", AttributeKind.ATTR, "Unique identifier")
    """

    name: str
    type: str
    is_ref: bool
    multiplicity: str
    kind: AttributeKind
    note: str

    def __post_init__(self) -> None:
        """Validate the attribute fields.

        Requirements:
            SWR_MODEL_00011: AUTOSAR Attribute Name Validation
            SWR_MODEL_00012: AUTOSAR Attribute Type Validation

        Raises:
            ValueError: If name or type is empty or contains only whitespace.
        """
        if not self.name or not self.name.strip():
            raise ValueError("Attribute name cannot be empty")
        if not self.type or not self.type.strip():
            raise ValueError("Attribute type cannot be empty")

    def __str__(self) -> str:
        """Return string representation of the attribute.

        Requirements:
            SWR_MODEL_00013: AUTOSAR Attribute String Representation

        Returns:
            Attribute name and type with '(ref)' suffix if reference type,
            plus multiplicity, kind, and note.
        """
        ref_suffix = " (ref)" if self.is_ref else ""
        return f"{self.name}: {self.type}{ref_suffix} [{self.multiplicity}] ({self.kind.value}) - {self.note}"

    def __repr__(self) -> str:
        """Return detailed representation for debugging.

        Requirements:
            SWR_MODEL_00013: AUTOSAR Attribute String Representation
        """
        return (
            f"AutosarAttribute(name='{self.name}', type='{self.type}', "
            f"is_ref={self.is_ref}, multiplicity='{self.multiplicity}', "
            f"kind={self.kind}, note='{self.note}')"
        )


@dataclass
class AutosarClass(AbstractAutosarBase):
    """Represents an AUTOSAR class.

    Requirements:
        SWR_MODEL_00001: AUTOSAR Class Representation
        SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
        SWR_MODEL_00022: AUTOSAR Class Parent Attribute

    Inherits from AbstractAutosarBase to provide common type properties (name, package, note)
    and adds class-specific attributes including inheritance support and ATP markers.

    Attributes:
        name: The name of the class (inherited from AbstractAutosarBase).
        package: The full package path (inherited from AbstractAutosarBase).
        is_abstract: Whether the class is abstract.
        atp_type: ATP marker type enum indicating the AUTOSAR Tool Platform marker.
        attributes: Dictionary of AUTOSAR attributes (key: attribute name, value: AutosarAttribute).
        bases: List of base class names for inheritance tracking.
        parent: Name of the immediate parent class from the bases list (None for root classes).
        note: Optional documentation or comments (inherited from AbstractAutosarBase).

    Examples:
        >>> cls = AutosarClass("RunnableEntity", "M2::SWR", False)
        >>> abstract_cls = AutosarClass("InternalBehavior", "M2::SWR", True)
        >>> attr = AutosarAttribute("dataReadPort", "PPortPrototype", True)
        >>> cls_with_attr = AutosarClass("Component", "M2::SWR", False, attributes={"dataReadPort": attr})
        >>> cls_with_bases = AutosarClass("DerivedClass", "M2::SWR", False, bases=["BaseClass"])
        >>> cls_with_parent = AutosarClass("ChildClass", "M2::SWR", False, bases=["BaseClass"], parent="BaseClass")
        >>> cls_with_note = AutosarClass("MyClass", "M2::SWR", False, note="Documentation note")
        >>> cls_with_atp = AutosarClass("MyClass", "M2::SWR", False, atp_type=ATPType.ATP_VARIATION)
    """

    is_abstract: bool = False
    atp_type: ATPType = ATPType.NONE
    attributes: Dict[str, AutosarAttribute] = field(default_factory=dict)
    bases: List[str] = field(default_factory=list)
    parent: Optional[str] = None

    def __str__(self) -> str:
        """Return string representation of the class.

        Requirements:
            SWR_MODEL_00003: AUTOSAR Class String Representation

        Returns:
            Class name with '(abstract)' suffix if abstract.
        """
        suffix = " (abstract)" if self.is_abstract else ""
        return f"{self.name}{suffix}"

    def __repr__(self) -> str:
        """Return detailed representation for debugging.

        Requirements:
            SWR_MODEL_00003: AUTOSAR Class String Representation
            SWR_MODEL_00022: AUTOSAR Class Parent Attribute
        """
        attrs_count = len(self.attributes)
        bases_count = len(self.bases)
        note_present = self.note is not None
        return (
            f"AutosarClass(name='{self.name}', is_abstract={self.is_abstract}, "
            f"atp_type={self.atp_type.name}, "
            f"attributes={attrs_count}, bases={bases_count}, parent={self.parent}, note={note_present})"
        )


@dataclass
class AutosarEnumeration(AbstractAutosarBase):
    """Represents an AUTOSAR enumeration type.

    Requirements:
        SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
        SWR_MODEL_00019: AUTOSAR Enumeration Type Representation

    Inherits from AbstractAutosarBase to provide common type properties (name, package, note)
    and adds enumeration-specific literals.

    Attributes:
        name: The name of the enumeration (inherited from AbstractAutosarBase).
        package: The full package path (inherited from AbstractAutosarBase).
        enumeration_literals: List of enumeration literal values.
        note: Optional documentation or comments (inherited from AbstractAutosarBase).

    Examples:
        >>> enum = AutosarEnumeration("EcucDestinationUriNestingContractEnum", "M2::ECUC")
        >>> enum_with_literals = AutosarEnumeration(
        ...     "MyEnum",
        ...     "M2::ECUC",
        ...     enumeration_literals=[
        ...         AutosarEnumLiteral("VALUE1", 0, "First value"),
        ...         AutosarEnumLiteral("VALUE2", 1, "Second value")
        ...     ]
        ... )
    """

    enumeration_literals: List[AutosarEnumLiteral] = field(default_factory=list)

    def __str__(self) -> str:
        """Return string representation of the enumeration.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
            SWR_MODEL_00019: AUTOSAR Enumeration Type Representation

        Returns:
            Enumeration name.
        """
        return f"{self.name}"

    def __repr__(self) -> str:
        """Return detailed representation for debugging.

        Requirements:
            SWR_MODEL_00019: AUTOSAR Enumeration Type Representation
        """
        literals_count = len(self.enumeration_literals)
        note_present = self.note is not None
        return (
            f"AutosarEnumeration(name='{self.name}', "
            f"package='{self.package}', "
            f"enumeration_literals={literals_count}, note={note_present})"
        )


@dataclass
class AutosarPrimitive(AbstractAutosarBase):
    """Represents an AUTOSAR primitive type.

    Requirements:
        SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
        SWR_MODEL_00024: AUTOSAR Primitive Type Representation

    Inherits from AbstractAutosarBase to provide common type properties (name, package, note)
    and represents primitive data types in AUTOSAR.

    Attributes:
        name: The name of the primitive type (inherited from AbstractAutosarBase).
        package: The full package path (inherited from AbstractAutosarBase).
        note: Optional documentation or comments (inherited from AbstractAutosarBase).
        attributes: Dictionary of AUTOSAR attributes (key: attribute name, value: AutosarAttribute).

    Examples:
        >>> primitive = AutosarPrimitive("Limit", "M2::DataTypes")
        >>> primitive_with_note = AutosarPrimitive("Interval", "M2::DataTypes", note="Interval type")
        >>> attr = AutosarAttribute("intervalType", "String", False)
        >>> primitive_with_attr = AutosarPrimitive("Limit", "M2::DataTypes", attributes={"intervalType": attr})
    """

    attributes: Dict[str, AutosarAttribute] = field(default_factory=dict)

    def __str__(self) -> str:
        """Return string representation of the primitive type.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
            SWR_MODEL_00024: AUTOSAR Primitive Type Representation

        Returns:
            Primitive type name.
        """
        return f"{self.name}"

    def __repr__(self) -> str:
        """Return detailed representation for debugging.

        Requirements:
            SWR_MODEL_00024: AUTOSAR Primitive Type Representation
        """
        attrs_count = len(self.attributes)
        note_present = self.note is not None
        return (
            f"AutosarPrimitive(name='{self.name}', "
            f"package='{self.package}', "
            f"attributes={attrs_count}, note={note_present})"
        )


@dataclass
class AutosarPackage:
    """Represents an AUTOSAR package containing types and subpackages.

    Requirements:
        SWR_MODEL_00004: AUTOSAR Package Representation
        SWR_MODEL_00020: AUTOSAR Package Type Support
        SWR_MODEL_00025: AUTOSAR Package Primitive Type Support

    Attributes:
        name: The name of the package.
        types: List of types (AutosarClass, AutosarEnumeration, or AutosarPrimitive) in this package.
        subpackages: List of subpackages in this package.

    Examples:
        >>> pkg = AutosarPackage("BswBehavior")
        >>> pkg.add_type(AutosarClass("BswInternalBehavior", False))
        >>> pkg.add_type(AutosarEnumeration("MyEnum", False))
        >>> pkg.add_type(AutosarPrimitive("Limit", "M2::DataTypes"))
        >>> subpkg = AutosarPackage("SubBehavior")
        >>> pkg.add_subpackage(subpkg)
    """

    name: str
    types: List[Union[AutosarClass, AutosarEnumeration, AutosarPrimitive]] = field(default_factory=list)
    subpackages: List["AutosarPackage"] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate the package fields.

        Requirements:
            SWR_MODEL_00005: AUTOSAR Package Name Validation

        Raises:
            ValueError: If name is empty or contains only whitespace.
        """
        if not self.name or not self.name.strip():
            raise ValueError("Package name cannot be empty")

    def add_type(self, typ: Union[AutosarClass, AutosarEnumeration, AutosarPrimitive]) -> None:
        """Add a type (class, enumeration, or primitive) to the package.

        Requirements:
            SWR_MODEL_00006: Add Class to Package
            SWR_MODEL_00020: AUTOSAR Package Type Support
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support

        Args:
            typ: The AutosarClass, AutosarEnumeration, or AutosarPrimitive to add.

        Raises:
            ValueError: If a type with the same name already exists.
        """
        type_names = {t.name for t in self.types}
        if typ.name in type_names:
            raise ValueError(f"Type '{typ.name}' already exists in package '{self.name}'")
        self.types.append(typ)

    def add_class(self, cls: AutosarClass) -> None:
        """Add a class to the package.

        Requirements:
            SWR_MODEL_00006: Add Class to Package
            SWR_MODEL_00020: AUTOSAR Package Type Support

        Args:
            cls: The AutosarClass to add.

        Raises:
            ValueError: If a class with the same name already exists.

        Note:
            This method is maintained for backward compatibility and delegates to add_type().
        """
        self.add_type(cls)

    def add_enumeration(self, enum: AutosarEnumeration) -> None:
        """Add an enumeration to the package.

        Requirements:
            SWR_MODEL_00020: AUTOSAR Package Type Support

        Args:
            enum: The AutosarEnumeration to add.

        Raises:
            ValueError: If an enumeration with the same name already exists.
        """
        self.add_type(enum)

    def add_subpackage(self, pkg: "AutosarPackage") -> None:
        """Add a subpackage to this package.

        Requirements:
            SWR_MODEL_00007: Add Subpackage to Package

        Args:
            pkg: The AutosarPackage to add as a subpackage.

        Raises:
            ValueError: If a subpackage with the same name already exists.
        """
        pkg_names = {p.name for p in self.subpackages}
        if pkg.name in pkg_names:
            raise ValueError(f"Subpackage '{pkg.name}' already exists in package '{self.name}'")
        self.subpackages.append(pkg)

    def get_type(self, name: str) -> Optional[Union[AutosarClass, AutosarEnumeration, AutosarPrimitive]]:
        """Get a type (class, enumeration, or primitive) by name.

        Requirements:
            SWR_MODEL_00008: Query Package Contents
            SWR_MODEL_00020: AUTOSAR Package Type Support
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support

        Args:
            name: The name of the type to find.

        Returns:
            The AutosarClass, AutosarEnumeration, or AutosarPrimitive if found, None otherwise.
        """
        for typ in self.types:
            if typ.name == name:
                return typ
        return None

    def get_class(self, name: str) -> Optional[AutosarClass]:
        """Get a class by name.

        Requirements:
            SWR_MODEL_00008: Query Package Contents
            SWR_MODEL_00020: AUTOSAR Package Type Support

        Args:
            name: The name of the class to find.

        Returns:
            The AutosarClass if found, None otherwise.

        Note:
            This method is maintained for backward compatibility and returns only AutosarClass instances.
        """
        for typ in self.types:
            if isinstance(typ, AutosarClass) and typ.name == name:
                return typ
        return None

    def get_enumeration(self, name: str) -> Optional[AutosarEnumeration]:
        """Get an enumeration by name.

        Requirements:
            SWR_MODEL_00020: AUTOSAR Package Type Support

        Args:
            name: The name of the enumeration to find.

        Returns:
            The AutosarEnumeration if found, None otherwise.
        """
        for typ in self.types:
            if isinstance(typ, AutosarEnumeration) and typ.name == name:
                return typ
        return None

    def add_primitive(self, primitive: AutosarPrimitive) -> None:
        """Add a primitive type to the package.

        Requirements:
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support

        Args:
            primitive: The AutosarPrimitive to add.

        Raises:
            ValueError: If a primitive type with the same name already exists.
        """
        self.add_type(primitive)

    def get_primitive(self, name: str) -> Optional[AutosarPrimitive]:
        """Get a primitive type by name.

        Requirements:
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support

        Args:
            name: The name of the primitive type to find.

        Returns:
            The AutosarPrimitive if found, None otherwise.
        """
        for typ in self.types:
            if isinstance(typ, AutosarPrimitive) and typ.name == name:
                return typ
        return None

    def get_subpackage(self, name: str) -> Optional["AutosarPackage"]:
        """Get a subpackage by name.

        Requirements:
            SWR_MODEL_00008: Query Package Contents

        Args:
            name: The name of the subpackage to find.

        Returns:
            The AutosarPackage if found, None otherwise.
        """
        for pkg in self.subpackages:
            if pkg.name == name:
                return pkg
        return None

    def has_type(self, name: str) -> bool:
        """Check if a type (class, enumeration, or primitive) exists in the package.

        Requirements:
            SWR_MODEL_00008: Query Package Contents
            SWR_MODEL_00020: AUTOSAR Package Type Support
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support

        Args:
            name: The name of the type to check.

        Returns:
            True if the type exists, False otherwise.
        """
        return any(typ.name == name for typ in self.types)

    def has_class(self, name: str) -> bool:
        """Check if a class exists in the package.

        Requirements:
            SWR_MODEL_00008: Query Package Contents
            SWR_MODEL_00020: AUTOSAR Package Type Support

        Args:
            name: The name of the class to check.

        Returns:
            True if the class exists, False otherwise.

        Note:
            This method is maintained for backward compatibility and checks only for AutosarClass instances.
        """
        return any(isinstance(typ, AutosarClass) and typ.name == name for typ in self.types)

    def has_enumeration(self, name: str) -> bool:
        """Check if an enumeration exists in the package.

        Requirements:
            SWR_MODEL_00020: AUTOSAR Package Type Support

        Args:
            name: The name of the enumeration to check.

        Returns:
            True if the enumeration exists, False otherwise.
        """
        return any(isinstance(typ, AutosarEnumeration) and typ.name == name for typ in self.types)

    def has_primitive(self, name: str) -> bool:
        """Check if a primitive type exists in the package.

        Requirements:
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support

        Args:
            name: The name of the primitive type to check.

        Returns:
            True if the primitive type exists, False otherwise.
        """
        return any(isinstance(typ, AutosarPrimitive) and typ.name == name for typ in self.types)

    def has_subpackage(self, name: str) -> bool:
        """Check if a subpackage exists in the package.

        Requirements:
            SWR_MODEL_00008: Query Package Contents

        Args:
            name: The name of the subpackage to check.

        Returns:
            True if the subpackage exists, False otherwise.
        """
        return any(pkg.name == name for pkg in self.subpackages)

    def __str__(self) -> str:
        """Return string representation of the package.

        Requirements:
            SWR_MODEL_00009: Package String Representation
            SWR_MODEL_00020: AUTOSAR Package Type Support
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support
        """
        parts = [f"Package '{self.name}'"]
        if self.types:
            parts.append(f"{len(self.types)} types")
        if self.subpackages:
            parts.append(f"{len(self.subpackages)} subpackages")
        return " (".join(parts) + ")"

    def __repr__(self) -> str:
        """Return detailed representation for debugging.

        Requirements:
            SWR_MODEL_00009: Package String Representation
            SWR_MODEL_00020: AUTOSAR Package Type Support
            SWR_MODEL_00025: AUTOSAR Package Primitive Type Support
        """
        return (
            f"AutosarPackage(name='{self.name}', "
            f"types={len(self.types)}, subpackages={len(self.subpackages)})"
        )


@dataclass
class AutosarDoc:
    """Represents an AUTOSAR document containing packages and root classes.

    Requirements:
        SWR_MODEL_00023: AUTOSAR Document Representation

    This class encapsulates the complete AUTOSAR model structure including
    the package hierarchy and root classes (classes with no bases).

    Attributes:
        packages: List of top-level AutosarPackage objects.
        root_classes: List of root AutosarClass objects (classes with empty bases).

    Examples:
        >>> doc = AutosarDoc(packages=[pkg1, pkg2], root_classes=[root_cls])
    """

    packages: List[AutosarPackage]
    root_classes: List[AutosarClass]

    def __post_init__(self) -> None:
        """Validate the document fields.

        Requirements:
            SWR_MODEL_00023: AUTOSAR Document Representation

        Raises:
            ValueError: If packages or root_classes contain duplicate names.
        """
        # Check for duplicate package names
        pkg_names = [pkg.name for pkg in self.packages]
        if len(pkg_names) != len(set(pkg_names)):
            raise ValueError("Duplicate package names found in packages")

        # Check for duplicate root class names
        root_cls_names = [cls.name for cls in self.root_classes]
        if len(root_cls_names) != len(set(root_cls_names)):
            raise ValueError("Duplicate root class names found in root_classes")

    def get_package(self, name: str) -> Optional[AutosarPackage]:
        """Get a package by name.

        Requirements:
            SWR_MODEL_00023: AUTOSAR Document Representation

        Args:
            name: The name of the package to find.

        Returns:
            The AutosarPackage if found, None otherwise.
        """
        for pkg in self.packages:
            if pkg.name == name:
                return pkg
        return None

    def get_root_class(self, name: str) -> Optional[AutosarClass]:
        """Get a root class by name.

        Requirements:
            SWR_MODEL_00023: AUTOSAR Document Representation

        Args:
            name: The name of the root class to find.

        Returns:
            The AutosarClass if found, None otherwise.
        """
        for cls in self.root_classes:
            if cls.name == name:
                return cls
        return None

    def __str__(self) -> str:
        """Return string representation of the document.

        Requirements:
            SWR_MODEL_00023: AUTOSAR Document Representation

        Returns:
            Document summary with package and root class counts.
        """
        return f"AutosarDoc({len(self.packages)} packages, {len(self.root_classes)} root classes)"

    def __repr__(self) -> str:
        """Return detailed representation for debugging.

        Requirements:
            SWR_MODEL_00023: AUTOSAR Document Representation
        """
        return (
            f"AutosarDoc(packages={len(self.packages)}, root_classes={len(self.root_classes)})"
        )
