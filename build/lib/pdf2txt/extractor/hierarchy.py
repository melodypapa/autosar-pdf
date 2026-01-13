"""
Package hierarchy building using class-based approach
"""

from typing import List, Dict
from .models import Package, Class


class PackageHierarchyBuilder:
    """
    Package hierarchy builder for creating nested tree structures.

    This class provides methods to build hierarchical trees
    from flat package and class data.
    """

    def build_tree(self, packages: List[Package]) -> dict:
        """
        Build hierarchical tree structure from package paths.

        Args:
            packages (List[Package]): List of Package objects

        Returns:
            dict: Nested tree structure with '__classes__' key at leaf nodes

        Example:
            >>> from pdf2txt.extractor.models import Package, Class
            >>> packages = [
            ...     Package('AUTOSARTemplates::BswModuleTemplate', [Class('ClassA'), Class('ClassB')]),
            ...     Package('AUTOSARTemplates::CommonStructure', [Class('ClassC')])
            ... ]
            >>> builder = PackageHierarchyBuilder()
            >>> tree = builder.build_tree(packages)
            >>> print(tree['AUTOSARTemplates']['BswModuleTemplate']['__classes__'])
            [Class(name='ClassA', abstract=False), Class(name='ClassB', abstract=False)]
        """
        tree = {}
        for pkg in packages:
            parts = pkg.name.split("::")
            current = tree
            for part in parts:
                if part not in current:
                    current[part] = {"__classes__": []}
                current = current[part]
            current["__classes__"] = pkg.classes
        return tree

    def build_dict(self, packages: List[Package]) -> Dict[str, List[Class]]:
        """
        Build flat dictionary mapping package names to class lists.

        Args:
            packages (List[Package]): List of Package objects

        Returns:
            Dict[str, List[Class]]: Dictionary mapping package names to Class objects

        Example:
            >>> from pdf2txt.extractor.models import Package, Class
            >>> packages = [Package('Pkg1', [Class('A')])]
            >>> builder = PackageHierarchyBuilder()
            >>> result = builder.build_dict(packages)
            >>> result['Pkg1']
            [Class(name='A', abstract=False)]
        """
        return {pkg.name: pkg.classes for pkg in packages}


def build_package_hierarchy(packages: List[Package]) -> dict:
    """
    Build hierarchical tree structure from package paths (backward compatibility function).

    Args:
        packages (List[Package]): List of Package objects

    Returns:
        dict: Nested tree structure with '__classes__' key at leaf nodes
    """
    builder = PackageHierarchyBuilder()
    return builder.build_tree(packages)


def build_package_hierarchy_dict(packages: List[Package]) -> Dict[str, List[Class]]:
    """
    Build flat dictionary mapping package names to class lists (backward compatibility function).

    Args:
        packages (List[Package]): List of Package objects

    Returns:
        Dict[str, List[Class]]: Dictionary mapping package names to Class objects
    """
    builder = PackageHierarchyBuilder()
    return builder.build_dict(packages)
