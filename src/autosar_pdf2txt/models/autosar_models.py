"""AUTOSAR data models for packages and classes."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


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


@dataclass
class AutosarAttribute:
    """Represents an AUTOSAR class attribute.

    Requirements:
        SWR_MODEL_00010: AUTOSAR Attribute Representation

    Attributes:
        name: The name of the attribute.
        type: The data type of the attribute.
        is_ref: Whether the attribute is a reference type.

    Examples:
        >>> attr = AutosarAttribute("dataReadPort", "PPortPrototype", True)
        >>> non_ref_attr = AutosarAttribute("id", "uint32", False)
    """

    name: str
    type: str
    is_ref: bool

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
            Attribute name and type with '(ref)' suffix if reference type.
        """
        suffix = " (ref)" if self.is_ref else ""
        return f"{self.name}: {self.type}{suffix}"

    def __repr__(self) -> str:
        """Return detailed representation for debugging.

        Requirements:
            SWR_MODEL_00013: AUTOSAR Attribute String Representation
        """
        return f"AutosarAttribute(name='{self.name}', type='{self.type}', is_ref={self.is_ref})"


@dataclass
class AutosarClass:
    """Represents an AUTOSAR class.

    Requirements:
        SWR_MODEL_00001: AUTOSAR Class Representation

    Attributes:
        name: The name of the class.
        is_abstract: Whether the class is abstract.
        atp_type: ATP marker type enum indicating the AUTOSAR Tool Platform marker.
        attributes: Dictionary of AUTOSAR attributes (key: attribute name, value: AutosarAttribute).
        bases: List of base class names for inheritance tracking.
        note: Optional documentation or comments about the class.

    Examples:
        >>> cls = AutosarClass("RunnableEntity", False)
        >>> abstract_cls = AutosarClass("InternalBehavior", True)
        >>> attr = AutosarAttribute("dataReadPort", "PPortPrototype", True)
        >>> cls_with_attr = AutosarClass("Component", False, {"dataReadPort": attr})
        >>> cls_with_bases = AutosarClass("DerivedClass", False, bases=["BaseClass"])
        >>> cls_with_note = AutosarClass("MyClass", False, note="Documentation note")
        >>> cls_with_atp = AutosarClass("MyClass", False, atp_type=ATPType.ATP_VARIATION)
    """

    name: str
    is_abstract: bool
    atp_type: ATPType = ATPType.NONE
    attributes: Dict[str, AutosarAttribute] = field(default_factory=dict)
    bases: List[str] = field(default_factory=list)
    note: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate the class fields.

        Requirements:
            SWR_MODEL_00002: AUTOSAR Class Name Validation

        Raises:
            ValueError: If name is empty or contains only whitespace.
        """
        if not self.name or not self.name.strip():
            raise ValueError("Class name cannot be empty")

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
        """
        attrs_count = len(self.attributes)
        bases_count = len(self.bases)
        note_present = self.note is not None
        return (
            f"AutosarClass(name='{self.name}', is_abstract={self.is_abstract}, "
            f"atp_type={self.atp_type.name}, "
            f"attributes={attrs_count}, bases={bases_count}, note={note_present})"
        )


@dataclass
class AutosarPackage:
    """Represents an AUTOSAR package containing classes and subpackages.

    Requirements:
        SWR_MODEL_00004: AUTOSAR Package Representation

    Attributes:
        name: The name of the package.
        classes: List of classes in this package.
        subpackages: List of subpackages in this package.

    Examples:
        >>> pkg = AutosarPackage("BswBehavior")
        >>> pkg.add_class(AutosarClass("BswInternalBehavior", False))
        >>> subpkg = AutosarPackage("SubBehavior")
        >>> pkg.add_subpackage(subpkg)
    """

    name: str
    classes: List[AutosarClass] = field(default_factory=list)
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

    def add_class(self, cls: AutosarClass) -> None:
        """Add a class to the package.

        Requirements:
            SWR_MODEL_00006: Add Class to Package

        Args:
            cls: The AutosarClass to add.

        Raises:
            ValueError: If a class with the same name already exists.
        """
        class_names = {c.name for c in self.classes}
        if cls.name in class_names:
            raise ValueError(f"Class '{cls.name}' already exists in package '{self.name}'")
        self.classes.append(cls)

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

    def get_class(self, name: str) -> Optional[AutosarClass]:
        """Get a class by name.

        Requirements:
            SWR_MODEL_00008: Query Package Contents

        Args:
            name: The name of the class to find.

        Returns:
            The AutosarClass if found, None otherwise.
        """
        for cls in self.classes:
            if cls.name == name:
                return cls
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

    def has_class(self, name: str) -> bool:
        """Check if a class exists in the package.

        Requirements:
            SWR_MODEL_00008: Query Package Contents

        Args:
            name: The name of the class to check.

        Returns:
            True if the class exists, False otherwise.
        """
        return any(cls.name == name for cls in self.classes)

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
        """
        parts = [f"Package '{self.name}'"]
        if self.classes:
            parts.append(f"{len(self.classes)} classes")
        if self.subpackages:
            parts.append(f"{len(self.subpackages)} subpackages")
        return " (".join(parts) + ")"

    def __repr__(self) -> str:
        """Return detailed representation for debugging.

        Requirements:
            SWR_MODEL_00009: Package String Representation
        """
        return (
            f"AutosarPackage(name='{self.name}', "
            f"classes={len(self.classes)}, subpackages={len(self.subpackages)})"
        )
