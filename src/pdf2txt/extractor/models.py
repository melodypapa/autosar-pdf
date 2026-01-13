"""
AUTOSAR data models
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Class:
    """
    AUTOSAR class model.

    Attributes:
        name (str): Class name
        abstract (bool): Whether the class is abstract
    """

    name: str
    abstract: bool = False


@dataclass
class Package:
    """
    AUTOSAR package model.

    Attributes:
        name (str): Package name
        classes (List[Class]): List of classes in this package
    """

    name: str
    classes: List[Class]

    @property
    def total_classes(self) -> int:
        """Get total number of classes in this package."""
        return len(self.classes)

    @property
    def total_abstract_classes(self) -> int:
        """Get number of abstract classes in this package."""
        return sum(1 for cls in self.classes if cls.abstract)
