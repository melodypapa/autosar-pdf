"""Abstract base class for AUTOSAR models.

Requirements:
    SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
    SWR_MODEL_00027: AUTOSAR Source Location Representation
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AutosarSource:
    """Represents a source location for an AUTOSAR type.

    Requirements:
        SWR_MODEL_00027: AUTOSAR Source Location Representation

    This dataclass tracks where a type was defined or where a base class
    was referenced in the PDF documentation.

    Attributes:
        pdf_file: Path to the PDF file (relative or absolute).
        page_number: Page number in the PDF (1-indexed).
        autosar_standard: Optional AUTOSAR standard identifier (e.g., "TPS_BSWModuleDescriptionTemplate").
        standard_release: Optional AUTOSAR standard release (e.g., "R21-11").

    Examples:
        >>> source = AutosarSource("AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf", 42)
        >>> source.pdf_file
        'AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf'
        >>> source.page_number
        42
        >>> source_with_standard = AutosarSource(
        ...     "AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf",
        ...     42,
        ...     autosar_standard="TPS_BSWModuleDescriptionTemplate",
        ...     standard_release="R21-11"
        ... )
        >>> source_with_standard.autosar_standard
        'TPS_BSWModuleDescriptionTemplate'
        >>> source_with_standard.standard_release
        'R21-11'
    """
    pdf_file: str
    page_number: int
    autosar_standard: Optional[str] = None
    standard_release: Optional[str] = None

    def __str__(self) -> str:
        """Return user-friendly string representation.

        Returns:
            Formatted string with PDF file, page number, and optional AUTOSAR
            standard and release information.
        """
        lines = [f"{self.pdf_file}, page {self.page_number}"]
        if self.autosar_standard:
            lines.append(f"AUTOSAR Standard: {self.autosar_standard}")
        if self.standard_release:
            lines.append(f"Standard Release: {self.standard_release}")
        return "\n".join(lines)


class AbstractAutosarBase(ABC):
    """Abstract base class for AUTOSAR type definitions.

    Requirements:
        SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
        SWR_MODEL_00027: AUTOSAR Source Location Representation

    This abstract class encapsulates common properties shared by all AUTOSAR type
    definitions, including regular classes and enumerations.

    Attributes:
        name: The name of the type.
        package: The full package path in PDF format (e.g., "M2::MSR::DataDictionary::RecordLayout").
        note: Optional documentation or comments about the type.
        source: Optional source location (pdf_file, page_number) where this type was defined.

    Examples:
        >>> type_obj = AbstractAutosarBase("MyType")  # This would fail - can't instantiate abstract class
        >>> # Instead, use AutosarClass or AutosarEnumeration
    """

    name: str
    package: str
    note: Optional[str]
    source: Optional[AutosarSource]

    def __init__(
        self,
        name: str,
        package: str,
        note: Optional[str] = None,
        source: Optional[AutosarSource] = None,
    ) -> None:
        """Initialize the abstract base class.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class
            SWR_MODEL_00027: AUTOSAR Source Location Representation

        Args:
            name: The name of the type.
            package: The full package path in PDF format.
            note: Optional documentation or comments about the type.
            source: Optional source location (PDF file and page number).

        Raises:
            ValueError: If name is empty or contains only whitespace.
        """
        if not name or not name.strip():
            raise ValueError("Type name cannot be empty")
        self.name = name
        self.package = package
        self.note = note
        self.source = source

    @abstractmethod
    def __str__(self) -> str:
        """Return string representation of the type.

        Requirements:
            SWR_MODEL_00018: AUTOSAR Type Abstract Base Class

        Returns:
            Type name with appropriate formatting.
        """
        pass  # pragma: no cover (abstract method)