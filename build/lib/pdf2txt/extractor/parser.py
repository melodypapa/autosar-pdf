"""
AUTOSAR specification parser using class-based approach
"""

import re
from typing import List
from .models import Package, Class


class AutosarParser:
    """
    AUTOSAR specification parser for extracting package and class information.

    This class parses AUTOSAR specification PDFs to extract
    package hierarchies and their associated class definitions.
    """

    def __init__(self):
        """
        Initialize AUTOSAR parser.
        """
        self.package_pattern = re.compile(r"Package M2::([^\s]+)")
        self.class_pattern = re.compile(r"Class (\w+)")

    def parse(self, text: str) -> List[Package]:
        """
        Extract package and class information from PDF text content.

        Args:
            text (str): Extracted text content from PDF

        Returns:
            List[Package]: List of Package objects containing Class objects

        Example:
            >>> text = convert_pdf_to_text('autosar.pdf', method='pdfplumber')
            >>> parser = AutosarParser()
            >>> packages = parser.parse(text)
            >>> for pkg in packages:
            ...     print(f"{pkg.name}: {pkg.total_classes} classes")
        """
        lines = text.split("\n")
        packages_dict = {}
        current_package = None

        for line in lines:
            line = line.strip()

            if line.startswith("Package M2::"):
                current_package = self._extract_package_name(line)
                if current_package and current_package not in packages_dict:
                    packages_dict[current_package] = []

            elif line.startswith("Class "):
                class_name = self._extract_class_name(line)
                is_abstract = self._is_abstract_class(line)
                if class_name and current_package:
                    cls = Class(name=class_name, abstract=is_abstract)
                    packages_dict[current_package].append(cls)

        packages = [
            Package(name=pkg_name, classes=classes)
            for pkg_name, classes in packages_dict.items()
        ]
        return packages

    def _extract_package_name(self, line: str) -> str:
        """
        Extract package name from package declaration line.

        Args:
            line (str): Line containing package declaration

        Returns:
            str: Package name or empty string if not found
        """
        match = self.package_pattern.search(line)
        return match.group(1) if match else ""

    def _extract_class_name(self, line: str) -> str:
        """
        Extract class name from class declaration line.

        Args:
            line (str): Line containing class declaration

        Returns:
            str: Class name or empty string if not found
        """
        match = self.class_pattern.search(line)
        return match.group(1) if match else ""

    def _is_abstract_class(self, line: str) -> bool:
        """
        Check if class is abstract.

        Args:
            line (str): Line containing class declaration

        Returns:
            bool: True if class is abstract, False otherwise
        """
        return "abstract" in line.lower()


def extract_package_and_class_info(text: str) -> List[Package]:
    """
    Extract package and class information from PDF text content (backward compatibility function).

    Args:
        text (str): Extracted text content from PDF

    Returns:
        List[Package]: List of Package objects containing Class objects
    """
    parser = AutosarParser()
    return parser.parse(text)
