"""
Output file writing using class-based approach
"""

from pathlib import Path
from typing import List
from .models import Package, Class


class OutputWriter:
    """
    Output writer class for writing package and class information to files.

    This class provides methods to write output in various formats
    including Markdown and text summaries.
    """

    def __init__(self):
        """
        Initialize output writer.
        """
        pass

    def write_markdown_hierarchy(
        self,
        tree: dict,
        output_path: str,
        title: str = "AUTOSAR Package and Class Reference",
    ) -> None:
        """
        Write package hierarchy to markdown file.

        Args:
            tree (dict): Hierarchical tree structure from build_package_hierarchy
            output_path (str): Path to output markdown file
            title (str): Document title (default: "AUTOSAR Package and Class Reference")
        """
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(
                "This document contains all class and package references extracted from AUTOSAR specification.\n\n"
            )
            self._write_tree_node(tree, 0, f)

    def _write_tree_node(self, node: dict, indent_level: int, file) -> None:
        """
        Write a tree node recursively to file.

        Args:
            node (dict): Current tree node
            indent_level (int): Indentation level
            file: File object to write to
        """
        keys = sorted([k for k in node.keys() if k != "__classes__"])
        indent = "  " * indent_level

        for key in keys:
            file.write(f"{indent}* {key}\n")
            self._write_tree_node(node[key], indent_level + 1, file)

        classes = node.get("__classes__", [])
        if classes:
            for cls in classes:
                abstract_mark = " (abstract)" if cls.abstract else ""
                file.write(f"{indent}  * {cls.name}{abstract_mark}\n")

    def write_text_summary(self, packages: List[Package], output_path: str) -> None:
        """
        Write simple text summary of packages and classes.

        Args:
            packages (List[Package]): List of Package objects
            output_path (str): Path to output text file
        """
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            self._write_summary_header(f, packages)
            self._write_packages(f, packages)

    def _write_summary_header(self, file, packages: List[Package]) -> None:
        """
        Write summary header to file.

        Args:
            file: File object to write to
            packages (List[Package]): List of Package objects
        """
        total_packages = len(packages)
        total_classes = sum(pkg.total_classes for pkg in packages)
        total_abstract_classes = sum(pkg.total_abstract_classes for pkg in packages)

        file.write("AUTOSAR Package and Class Summary\n")
        file.write("=" * 50 + "\n\n")
        file.write(f"Total Packages: {total_packages}\n")
        file.write(f"Total Classes: {total_classes}\n")
        file.write(f"Abstract Classes: {total_abstract_classes}\n\n")
        file.write("-" * 50 + "\n\n")

    def _write_packages(self, file, packages: List[Package]) -> None:
        """
        Write package details to file.

        Args:
            file: File object to write to
            packages (List[Package]): List of Package objects
        """
        for pkg in sorted(packages, key=lambda p: p.name):
            file.write(f"{pkg.name}\n")
            file.write(f"  Classes ({pkg.total_classes}):\n")
            for cls in pkg.classes:
                abstract_mark = " [abstract]" if cls.abstract else ""
                file.write(f"    - {cls.name}{abstract_mark}\n")
            file.write("\n")


def write_markdown_hierarchy(
    tree: dict, output_path: str, title: str = "AUTOSAR Package and Class Reference"
) -> None:
    """
    Write package hierarchy to markdown file (backward compatibility function).

    Args:
        tree (dict): Hierarchical tree structure from build_package_hierarchy
        output_path (str): Path to output markdown file
        title (str): Document title (default: "AUTOSAR Package and Class Reference")
    """
    writer = OutputWriter()
    writer.write_markdown_hierarchy(tree, output_path, title)


def write_text_summary(packages: List[Package], output_path: str) -> None:
    """
    Write simple text summary of packages and classes (backward compatibility function).

    Args:
        packages (List[Package]): List of Package objects
        output_path (str): Path to output text file
    """
    writer = OutputWriter()
    writer.write_text_summary(packages, output_path)
