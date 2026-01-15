"""Parse AUTOSAR hierarchy from text."""

from typing import List, Tuple

from autosar_pdf2txt.models import AutosarClass, AutosarPackage


class HierarchyParser:
    """Parse AUTOSAR package/class hierarchy from text.

    The expected format is:
    * PackageName
      * SubPackageName
          * ClassName
          * ClassName (abstract)

    Indentation levels are determined by counting leading spaces and asterisks.
    """

    def __init__(self, text: str) -> None:
        """Initialize the parser with text content.

        Args:
            text: Text content containing the hierarchy.
        """
        self.text = text
        self.lines = text.split("\n")

    def parse(self) -> List[AutosarPackage]:
        """Parse the hierarchy and return list of top-level packages.

        Returns:
            List of AutosarPackage objects with their classes.

        Examples:
            >>> text = "* Package\\n    * Class\\n    * Class (abstract)"
            >>> parser = HierarchyParser(text)
            >>> packages = parser.parse()
        """
        return self._parse_hierarchy()

    def _parse_line(self, line: str) -> Tuple[int, str, bool]:
        """Parse a single hierarchy line.

        Args:
            line: A line from the hierarchy text.

        Returns:
            Tuple of (level, name, is_abstract).
            Level is -1 if not a valid hierarchy line.
        """
        # Count leading spaces
        stripped = line.lstrip(" ")
        leading_spaces = len(line) - len(stripped)

        # Check if line starts with asterisk
        if not stripped.startswith("*"):
            return (-1, "", False)

        # Remove asterisk and space after it
        content = stripped[1:].strip()
        if not content:
            return (leading_spaces, "", False)

        # Check for (abstract) suffix
        is_abstract = False
        if content.endswith("(abstract)"):
            is_abstract = True
            content = content[:-10].strip()  # Remove " (abstract)"

        name = content
        return (leading_spaces, name, is_abstract)

    def _parse_hierarchy(self) -> List[AutosarPackage]:
        """Parse hierarchy using a two-pass approach.

        Returns:
            List of AutosarPackage objects with nested subpackages.
        """
        # First pass: parse all lines into (level, name, is_abstract) tuples
        parsed_lines = []
        for line in self.lines:
            line = line.rstrip()
            if not line:
                continue

            level, name, is_abstract = self._parse_line(line)
            if level != -1 and name:
                parsed_lines.append((level, name, is_abstract))

        if not parsed_lines:
            return []

        # Determine base indentation (minimum level)
        base_level = min(level for level, _, _ in parsed_lines)

        # Second pass: build hierarchy with nested packages
        packages: List[AutosarPackage] = []
        package_stack: List[Tuple[int, AutosarPackage]] = []

        for i, (level, name, is_abstract) in enumerate(parsed_lines):
            # Normalize level relative to base
            normalized_level = level - base_level

            # Pop packages that are at or deeper than current level
            while package_stack and package_stack[-1][0] >= normalized_level:
                package_stack.pop()

            # Determine if this is a package or class
            # A line is a package if the next line is deeper
            is_package = self._is_package_line(parsed_lines, i)

            if is_package:
                pkg = AutosarPackage(name=name)
                if not package_stack:
                    # Top-level package
                    packages.append(pkg)
                else:
                    # Add as subpackage to parent
                    parent_level, parent_pkg = package_stack[-1]
                    # Check for duplicates before adding
                    if not parent_pkg.has_subpackage(name):
                        parent_pkg.add_subpackage(pkg)

                package_stack.append((normalized_level, pkg))
            else:
                # This is a class
                cls = AutosarClass(name=name, is_abstract=is_abstract)
                if package_stack:
                    _, parent_pkg = package_stack[-1]
                    # Check for duplicates before adding
                    if not parent_pkg.has_class(name):
                        parent_pkg.add_class(cls)
                elif not is_abstract:
                    # No parent package and not abstract - treat as empty package
                    pkg = AutosarPackage(name=name)
                    packages.append(pkg)

        return packages

    def _is_package_line(self, all_lines: List[Tuple[int, str, bool]], current_idx: int) -> bool:
        """Check if a line represents a package (has children).

        Args:
            all_lines: All parsed lines.
            current_idx: Index of the current line to check.

        Returns:
            True if this line has children (is a package).
        """
        # Look at next line
        if current_idx + 1 >= len(all_lines):
            return False  # Last line, no children

        current_level, _, _ = all_lines[current_idx]
        next_level, _, _ = all_lines[current_idx + 1]

        # If next line is deeper (greater indentation), this is a package
        return next_level > current_level


def parse_hierarchy(text: str) -> List[AutosarPackage]:
    """Functional interface for parsing AUTOSAR hierarchy.

    Args:
        text: Text content containing the hierarchy.

    Returns:
        List of AutosarPackage objects.

    Examples:
        >>> text = "* Package\\n    * Class\\n    * Class (abstract)"
        >>> packages = parse_hierarchy(text)
        >>> len(packages[0].classes)
        2
    """
    parser = HierarchyParser(text)
    return parser.parse()
