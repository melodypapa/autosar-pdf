"""Abstract base class for AUTOSAR models.

Requirements:
    SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
"""

from abc import ABC, abstractmethod
from typing import Optional


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
    note: Optional[str]

    def __init__(self, name: str, package: str, note: Optional[str] = None) -> None:
        """Initialize the abstract base class.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class

        Args:
            name: The name of the type.
            package: The full package path in PDF format.
            note: Optional documentation or comments about the type.

        Raises:
            ValueError: If name is empty or contains only whitespace.
        """
        if not name or not name.strip():
            raise ValueError("Type name cannot be empty")
        self.name = name
        self.package = package
        self.note = note

    @abstractmethod
    def __str__(self) -> str:
        """Return string representation of the type.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class

        Returns:
            Type name with appropriate formatting.
        """
        pass  # pragma: no cover (abstract method)