"""Markdown writer for AUTOSAR packages and classes."""

from io import StringIO
from typing import List

from autosar_pdf2txt.models import AutosarClass, AutosarPackage


class MarkdownWriter:
    """Write AUTOSAR packages and classes to markdown format.

    The output format uses asterisks (*) for hierarchy with indentation
    to show nesting levels:
    * Package
      * SubPackage
          * Class
          * Class (abstract)
    """

    def __init__(self, deduplicate: bool = True) -> None:
        """Initialize the markdown writer.

        Args:
            deduplicate: Whether to track and skip duplicate items during writing.
        """
        self.deduplicate = deduplicate
        self._seen_packages: set[tuple[str, ...]] = set()
        self._seen_classes: set[tuple[str, ...]] = set()

    def write_packages(self, packages: List[AutosarPackage]) -> str:
        """Write a list of top-level packages to markdown format.

        Args:
            packages: List of top-level AutosarPackage objects.

        Returns:
            Markdown formatted string representing the package hierarchy.

        Examples:
            >>> writer = MarkdownWriter()
            >>> pkg = AutosarPackage(name="TestPackage")
            >>> pkg.add_class(AutosarClass("MyClass", False))
            >>> markdown = writer.write_packages([pkg])
        """
        output = StringIO()
        for pkg in packages:
            self._write_package(pkg, [], 0, output)
        return output.getvalue()

    def _write_package(
        self,
        pkg: AutosarPackage,
        parent_path: List[str],
        level: int,
        output: StringIO,
    ) -> None:
        """Write a single package with its contents to the output.

        Args:
            pkg: The package to write.
            parent_path: List of parent package names for duplicate tracking.
            level: Current indentation level (0 for top-level).
            output: StringIO buffer to write to.
        """
        # Check for duplicate package
        if self.deduplicate:
            package_path = tuple(parent_path + [pkg.name])
            if package_path in self._seen_packages:
                return
            self._seen_packages.add(package_path)

        # Write package line
        indent = "  " * level
        output.write(f"{indent}* {pkg.name}\n")

        # Write classes first (add one more level for proper indentation)
        for cls in pkg.classes:
            self._write_class(cls, parent_path + [pkg.name], level + 2, output)

        # Write subpackages
        for subpkg in pkg.subpackages:
            self._write_package(subpkg, parent_path + [pkg.name], level + 1, output)

    def _write_class(
        self,
        cls: AutosarClass,
        parent_path: List[str],
        level: int,
        output: StringIO,
    ) -> None:
        """Write a single class to the output.

        Args:
            cls: The class to write.
            parent_path: List of parent package names for duplicate tracking.
            level: Current indentation level.
            output: StringIO buffer to write to.
        """
        # Check for duplicate class
        if self.deduplicate:
            class_path = tuple(parent_path + [cls.name])
            if class_path in self._seen_classes:
                return
            self._seen_classes.add(class_path)

        # Write class line
        indent = "  " * level
        abstract_suffix = " (abstract)" if cls.is_abstract else ""
        output.write(f"{indent}* {cls.name}{abstract_suffix}\n")
