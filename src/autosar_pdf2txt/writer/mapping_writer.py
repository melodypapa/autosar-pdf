"""Mapping writer for AUTOSAR type-to-package mappings.

This module provides the MappingWriter class for generating type-to-package
mappings in both JSON and Markdown formats.
"""

import json
from io import StringIO
from typing import Dict, List, Literal

from autosar_pdf2txt.models import AutosarClass, AutosarEnumeration, AutosarPackage, AutosarPrimitive


class MappingWriter:
    """Write AUTOSAR type-to-package mappings in JSON and Markdown formats.

    Requirements:
        SWR_WRITER_00024: Mapping Writer Initialization
        SWR_WRITER_00025: JSON Mapping Output Format
        SWR_WRITER_00026: Markdown Mapping Table Output

    The mapping writer generates simple type-to-package mappings without
    detailed type information. The output contains only the type name,
    type category (Class/Enumeration/Primitive), and the full package path.
    """

    def __init__(self) -> None:
        """Initialize the mapping writer.

        Requirements:
            SWR_WRITER_00024: Mapping Writer Initialization
        """

    def write_mapping(
        self, packages: List[AutosarPackage], format: Literal["json", "markdown"]
    ) -> str:
        """Write type-to-package mapping in the specified format.

        Requirements:
            SWR_WRITER_00024: Mapping Writer Initialization
            SWR_WRITER_00025: JSON Mapping Output Format
            SWR_WRITER_00026: Markdown Mapping Table Output

        Args:
            packages: List of top-level AutosarPackage objects.
            format: Output format, either "json" or "markdown".

        Returns:
            String containing the mapping in the specified format.

        Raises:
            ValueError: If format is not "json" or "markdown".

        Examples:
            >>> writer = MappingWriter()
            >>> pkg = AutosarPackage("TestPackage")
            >>> pkg.add_type(AutosarClass("MyClass", "TestPackage", False))
            >>> json_output = writer.write_mapping([pkg], format="json")
            >>> md_output = writer.write_mapping([pkg], format="markdown")
        """
        # Collect all types from packages
        types = self._collect_mapping(packages)

        if format == "json":
            return self._write_mapping_json(types)
        elif format == "markdown":
            return self._write_mapping_markdown(types)
        else:
            raise ValueError(f"Invalid format: {format}. Must be 'json' or 'markdown'.")

    def _collect_mapping(self, packages: List[AutosarPackage]) -> List[Dict[str, str]]:
        """Collect all types from packages with their package paths.

        Requirements:
            SWR_WRITER_00024: Mapping Writer Initialization

        This method traverses the package hierarchy and collects all types
        (classes, enumerations, primitives) with their full package paths.

        Args:
            packages: List of top-level AutosarPackage objects.

        Returns:
            List of dictionaries with keys: name, type, package_path.
        """
        result = []

        def traverse_package(pkg: AutosarPackage) -> None:
            """Traverse a package and collect all types."""
            # Collect all types from current package
            for typ in pkg.types:
                if isinstance(typ, AutosarClass):
                    result.append({"name": typ.name, "type": "Class", "package_path": typ.package})
                elif isinstance(typ, AutosarEnumeration):
                    result.append({"name": typ.name, "type": "Enumeration", "package_path": typ.package})
                elif isinstance(typ, AutosarPrimitive):
                    result.append({"name": typ.name, "type": "Primitive", "package_path": typ.package})

            # Recursively process subpackages
            for subpkg in pkg.subpackages:
                traverse_package(subpkg)

        # Start traversal from top-level packages
        for pkg in packages:
            traverse_package(pkg)

        return result

    def _write_mapping_json(self, types: List[Dict[str, str]]) -> str:
        """Write mapping in JSON format.

        Requirements:
            SWR_WRITER_00025: JSON Mapping Output Format

        Args:
            types: List of type dictionaries with name, type, and package_path.

        Returns:
            JSON string with types array.
        """
        output = {"types": types}
        return json.dumps(output, indent=2, ensure_ascii=False)

    def _write_mapping_markdown(self, types: List[Dict[str, str]]) -> str:
        """Write mapping in Markdown table format.

        Requirements:
            SWR_WRITER_00026: Markdown Mapping Table Output

        Args:
            types: List of type dictionaries with name, type, and package_path.

        Returns:
            Markdown string with table header and rows.
        """
        output = StringIO()

        # Write header
        output.write("# Type to Package Mapping\n\n")

        # Write table header
        output.write("| Name | Type | Package Path |\n")
        output.write("|------|------|--------------|\n")

        # Write table rows
        for entry in types:
            output.write(f"| {entry['name']} | {entry['type']} | {entry['package_path']} |\n")

        return output.getvalue()
