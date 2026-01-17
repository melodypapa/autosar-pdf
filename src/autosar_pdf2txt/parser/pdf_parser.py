"""PDF parser for extracting AUTOSAR class hierarchies from PDF files."""

import re
from dataclasses import dataclass, field
from io import StringIO
from typing import List, Optional, Set, Tuple

from autosar_pdf2txt.models import AutosarClass, AutosarPackage


@dataclass
class ClassDefinition:
    """Represents a parsed class definition from PDF.

    Requirements:
        SWR_Parser_00005: Class Definition Data Model

    Attributes:
        name: The name of the class.
        package_path: Full package path (e.g., "M2::AUTOSARTemplates::BswModuleTemplate::BswBehavior").
        is_abstract: Whether the class is abstract.
        base_classes: List of base class names.
        subclasses: List of subclass names.
    """

    name: str
    package_path: str
    is_abstract: bool
    base_classes: List[str] = field(default_factory=list)
    subclasses: List[str] = field(default_factory=list)


class PdfParser:
    """Parse AUTOSAR PDF files to extract package and class hierarchies.

    Requirements:
        SWR_Parser_00001: PDF Parser Initialization

    The parser extracts class definitions from PDF files and builds
    AutosarPackage and AutosarClass objects using pdfplumber as the
    default PDF engine.

    Usage:
        >>> parser = PdfParser()
        >>> packages = parser.parse_pdf("path/to/file.pdf")
        >>> print(len(packages))
    """

    # Regex patterns for parsing class definitions
    # SWR_Parser_00004: Class Definition Pattern Recognition
    CLASS_PATTERN = re.compile(r"^Class\s+(.+?)(?:\s*\((abstract)\))?\s*$")
    PACKAGE_PATTERN = re.compile(r"^Package\s+(M2::)?(.+)$")
    BASE_PATTERN = re.compile(r"^Base\s+(.+)$")
    SUBCLASS_PATTERN = re.compile(r"^Subclasses\s+(.+)$")

    def __init__(self) -> None:
        """Initialize the PDF parser.

        Requirements:
            SWR_Parser_00001: PDF Parser Initialization
            SWR_Parser_00007: PDF Backend Support - pdfplumber

        Raises:
            ImportError: If pdfplumber is not installed.
        """
        self._validate_backend()

    def _validate_backend(self) -> None:
        """Validate that pdfplumber backend is available.

        Requirements:
            SWR_Parser_00002: Backend Validation
            SWR_Parser_00007: PDF Backend Support - pdfplumber

        Raises:
            ImportError: If pdfplumber is not installed.
        """
        try:
            import pdfplumber as _  # noqa: F401
        except ImportError:
            raise ImportError(
                "pdfplumber is not installed. Install it with: pip install pdfplumber"
            )

    def parse_pdf(self, pdf_path: str) -> List[AutosarPackage]:
        """Parse a PDF file and extract the package hierarchy.

        Requirements:
            SWR_Parser_00003: PDF File Parsing

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            List of top-level AutosarPackage objects.

        Raises:
            FileNotFoundError: If the PDF file doesn't exist.
            Exception: If PDF parsing fails.
        """
        # Extract class definitions from PDF
        class_defs = self._extract_class_definitions(pdf_path)

        # Build package hierarchy from class definitions
        return self._build_package_hierarchy(class_defs)

    def _extract_class_definitions(self, pdf_path: str) -> List[ClassDefinition]:
        """Extract all class definitions from the PDF.

        Requirements:
            SWR_Parser_00003: PDF File Parsing

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            List of ClassDefinition objects.
        """
        return self._extract_with_pdfplumber(pdf_path)

    def _extract_with_pdfplumber(self, pdf_path: str) -> List[ClassDefinition]:
        """Extract class definitions using pdfplumber.

        Requirements:
            SWR_Parser_00003: PDF File Parsing
            SWR_Parser_00007: PDF Backend Support - pdfplumber

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            List of ClassDefinition objects.
        """
        import pdfplumber

        class_defs: List[ClassDefinition] = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                text_buffer = StringIO()

                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_buffer.write(text + "\n")

                full_text = text_buffer.getvalue()
                class_defs = self._parse_class_text(full_text)

        except Exception as e:
            raise Exception(f"Failed to parse PDF with pdfplumber: {e}") from e

        return class_defs

    def _parse_class_text(self, text: str) -> List[ClassDefinition]:
        """Parse class definitions from extracted text.

        Requirements:
            SWR_Parser_00004: Class Definition Pattern Recognition

        Args:
            text: The extracted text from PDF.

        Returns:
            List of ClassDefinition objects.
        """
        class_defs: List[ClassDefinition] = []
        lines = text.split("\n")

        current_class: Optional[ClassDefinition] = None

        for line in lines:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Check for class definition
            class_match = self.CLASS_PATTERN.match(line)
            if class_match:
                # Save previous class if exists
                if current_class is not None:
                    class_defs.append(current_class)

                class_name = class_match.group(1).strip()
                is_abstract = class_match.group(2) is not None
                current_class = ClassDefinition(
                    name=class_name, package_path="", is_abstract=is_abstract
                )
                continue

            # Check for package definition
            package_match = self.PACKAGE_PATTERN.match(line)
            if package_match and current_class is not None:
                current_class.package_path = package_match.group(2).strip()
                continue

            # Check for base classes
            base_match = self.BASE_PATTERN.match(line)
            if base_match and current_class is not None:
                base_classes_str = base_match.group(1)
                current_class.base_classes = [
                    bc.strip() for bc in base_classes_str.split(",") if bc.strip()
                ]
                continue

            # Check for subclasses
            subclass_match = self.SUBCLASS_PATTERN.match(line)
            if subclass_match and current_class is not None:
                subclasses_str = subclass_match.group(1)
                current_class.subclasses = [
                    sc.strip() for sc in subclasses_str.split(",") if sc.strip()
                ]
                continue

        # Don't forget the last class
        if current_class is not None:
            class_defs.append(current_class)

        return class_defs

    def _build_package_hierarchy(
        self, class_defs: List[ClassDefinition]
    ) -> List[AutosarPackage]:
        """Build AutosarPackage hierarchy from class definitions.

        Requirements:
            SWR_Parser_00006: Package Hierarchy Building

        Args:
            class_defs: List of ClassDefinition objects.

        Returns:
            List of top-level AutosarPackage objects.
        """
        # Track all packages by their full path
        package_map: dict[str, AutosarPackage] = {}

        # Track which classes have been added to packages
        processed_classes: Set[Tuple[str, str]] = set()

        for class_def in class_defs:
            # Parse package path
            package_parts = [p.strip() for p in class_def.package_path.split("::")]

            # Create/get packages in hierarchy
            current_path = ""
            parent_package: Optional[AutosarPackage] = None

            for part in package_parts:
                if not part:
                    continue

                if current_path:
                    current_path += "::" + part
                else:
                    current_path = part

                # Get or create package
                if current_path not in package_map:
                    pkg = AutosarPackage(name=part)
                    package_map[current_path] = pkg

                    # Add to parent package if exists
                    if parent_package is not None:
                        try:
                            parent_package.add_subpackage(pkg)
                        except ValueError:
                            # Package already added, skip
                            pass

                parent_package = package_map[current_path]

            # Add class to the last package
            if parent_package is not None:
                class_key = (parent_package.name, class_def.name)
                if class_key not in processed_classes:
                    try:
                        autosar_class = AutosarClass(
                            name=class_def.name, is_abstract=class_def.is_abstract
                        )
                        parent_package.add_class(autosar_class)
                        processed_classes.add(class_key)
                    except ValueError:
                        # Class already exists, skip
                        pass

        # Return top-level packages (those with no "::" in path)
        top_level_packages = [
            pkg
            for path, pkg in package_map.items()
            if "::" not in path and pkg.classes or pkg.subpackages
        ]

        return top_level_packages
