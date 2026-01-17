"""Markdown writer for AUTOSAR packages and classes."""

from io import StringIO
from typing import List

from autosar_pdf2txt.models import AutosarClass, AutosarPackage


class MarkdownWriter:
    """Write AUTOSAR packages and classes to markdown format.

    Requirements:
        SWR_Writer_00001: Markdown Writer Initialization

    The output format uses asterisks (*) for hierarchy with indentation
    to show nesting levels. Each level adds 2 spaces of indentation.
    Classes and subpackages are written at the same indentation level:

    * TopLevelPackage
      * SubPackage
        * Class
        * Class (abstract)
    """

    def __init__(self) -> None:
        """Initialize the markdown writer.

        Requirements:
            SWR_Writer_00001: Markdown Writer Initialization
        """

    def write_packages(self, packages: List[AutosarPackage]) -> str:
        """Write a list of top-level packages to markdown format.

        Requirements:
            SWR_Writer_00002: Markdown Package Hierarchy Output
            SWR_Writer_00004: Bulk Package Writing

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

        Requirements:
            SWR_Writer_00002: Markdown Package Hierarchy Output

        Args:
            pkg: The package to write.
            parent_path: List of parent package names.
            level: Current indentation level (0 for top-level).
            output: StringIO buffer to write to.
        """
        # Write package line
        indent = "  " * level
        output.write(f"{indent}* {pkg.name}\n")

        # Write classes at one level deeper than their parent package
        for cls in pkg.classes:
            self._write_class(cls, parent_path + [pkg.name], level + 1, output)

        # Write subpackages at one level deeper than their parent package
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

        Requirements:
            SWR_Writer_00003: Markdown Class Output Format

        Args:
            cls: The class to write.
            parent_path: List of parent package names.
            level: Current indentation level.
            output: StringIO buffer to write to.
        """
        # Write class line
        indent = "  " * level
        abstract_suffix = " (abstract)" if cls.is_abstract else ""
        output.write(f"{indent}* {cls.name}{abstract_suffix}\n")
