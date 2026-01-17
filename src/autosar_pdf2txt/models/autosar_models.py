"""AUTOSAR data models for packages and classes."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class AutosarClass:
    """Represents an AUTOSAR class.

    Requirements:
        SWR_Model_00001: AUTOSAR Class Representation

    Attributes:
        name: The name of the class.
        is_abstract: Whether the class is abstract.

    Examples:
        >>> cls = AutosarClass("RunnableEntity", False)
        >>> abstract_cls = AutosarClass("InternalBehavior", True)
    """

    name: str
    is_abstract: bool

    def __post_init__(self) -> None:
        """Validate the class fields.

        Requirements:
            SWR_Model_00002: AUTOSAR Class Name Validation

        Raises:
            ValueError: If name is empty or contains only whitespace.
        """
        if not self.name or not self.name.strip():
            raise ValueError("Class name cannot be empty")

    def __str__(self) -> str:
        """Return string representation of the class.

        Requirements:
            SWR_Model_00003: AUTOSAR Class String Representation

        Returns:
            Class name with '(abstract)' suffix if abstract.
        """
        suffix = " (abstract)" if self.is_abstract else ""
        return f"{self.name}{suffix}"

    def __repr__(self) -> str:
        """Return detailed representation for debugging.

        Requirements:
            SWR_Model_00003: AUTOSAR Class String Representation
        """
        return f"AutosarClass(name='{self.name}', is_abstract={self.is_abstract})"


@dataclass
class AutosarPackage:
    """Represents an AUTOSAR package containing classes and subpackages.

    Requirements:
        SWR_Model_00004: AUTOSAR Package Representation

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
            SWR_Model_00005: AUTOSAR Package Name Validation

        Raises:
            ValueError: If name is empty or contains only whitespace.
        """
        if not self.name or not self.name.strip():
            raise ValueError("Package name cannot be empty")

    def add_class(self, cls: AutosarClass) -> None:
        """Add a class to the package.

        Requirements:
            SWR_Model_00006: Add Class to Package

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
            SWR_Model_00007: Add Subpackage to Package

        Args:
            pkg: The AutosarPackage to add as a subpackage.

        Raises:
            ValueError: If a subpackage with the same name already exists.
        """
        pkg_names = {p.name for p in self.subpackages}
        if pkg.name in pkg_names:
            raise ValueError(f"Subpackage '{pkg.name}' already exists in package '{self.name}'")
        self.subpackages.append(pkg)

    def get_class(self, name: str) -> AutosarClass | None:
        """Get a class by name.

        Requirements:
            SWR_Model_00008: Query Package Contents

        Args:
            name: The name of the class to find.

        Returns:
            The AutosarClass if found, None otherwise.
        """
        for cls in self.classes:
            if cls.name == name:
                return cls
        return None

    def get_subpackage(self, name: str) -> "AutosarPackage | None":
        """Get a subpackage by name.

        Requirements:
            SWR_Model_00008: Query Package Contents

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
            SWR_Model_00008: Query Package Contents

        Args:
            name: The name of the class to check.

        Returns:
            True if the class exists, False otherwise.
        """
        return any(cls.name == name for cls in self.classes)

    def has_subpackage(self, name: str) -> bool:
        """Check if a subpackage exists in the package.

        Requirements:
            SWR_Model_00008: Query Package Contents

        Args:
            name: The name of the subpackage to check.

        Returns:
            True if the subpackage exists, False otherwise.
        """
        return any(pkg.name == name for pkg in self.subpackages)

    def __str__(self) -> str:
        """Return string representation of the package.

        Requirements:
            SWR_Model_00009: Package String Representation
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
            SWR_Model_00009: Package String Representation
        """
        return (
            f"AutosarPackage(name='{self.name}', "
            f"classes={len(self.classes)}, subpackages={len(self.subpackages)})"
        )
