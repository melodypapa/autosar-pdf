"""JSON writer for AUTOSAR packages and classes."""

from pathlib import Path
from typing import List, Optional, Union

from autosar_pdf2txt.models import AutosarPackage


class JsonWriter:
    """Write AUTOSAR packages and classes to JSON format.

    Requirements:
        SWR_WRITER_00010: JSON Writer Initialization

    The output format uses separate JSON files for different entity types
    to keep file sizes manageable and enable efficient querying:

    - index.json: Root index with overview and package references
    - packages/{name}.json: Package metadata with entity file references
    - packages/{name}.classes.json: All classes in the package
    - packages/{name}.enums.json: All enumerations in the package
    - packages/{name}.primitives.json: All primitives in the package

    File naming sanitizes package names for filesystem safety by replacing
    invalid characters (< > : " / \\ | ? *) with underscores.
    """

    def __init__(self) -> None:
        """Initialize the JSON writer.

        Requirements:
            SWR_WRITER_00010: JSON Writer Initialization
        """

    def write_packages_to_files(
        self, packages: List[AutosarPackage], output_path: Optional[Union[str, Path]] = None, base_dir: Optional[Union[str, Path]] = None
    ) -> None:
        """Write packages to separate JSON files organized in directory structure.

        Requirements:
            SWR_WRITER_00011: JSON Directory Structure Creation

        For each package:
        - Creates a packages/ directory in the output location
        - Creates a package metadata JSON file
        - Creates separate JSON files for classes, enumerations, and primitives
        - Maintains nested directory structure for subpackages

        The root directory for the file structure is the same as the output JSON file location.
        If output_path is provided, the directory containing that file is used as the root.
        If base_dir is provided, it is used directly as the root directory.

        Args:
            packages: List of top-level AutosarPackage objects.
            output_path: Path to the output JSON file. The root directory will be
                the directory containing this file. Cannot be used with base_dir.
            base_dir: Base directory path where the package structure will be created.
                Cannot be used with output_path.

        Raises:
            OSError: If directory creation or file writing fails.
            ValueError: If both output_path and base_dir are provided, or if neither is provided,
                or if the path is empty.

        Examples:
            >>> writer = JsonWriter()
            >>> pkg = AutosarPackage(name="TestPackage")
            >>> pkg.add_class(AutosarClass("MyClass", "TestPackage", False))
            >>> # Using output file path (root is dir of output.json)
            >>> writer.write_packages_to_files([pkg], output_path="/tmp/output.json")
            >>> # Using base directory directly
            >>> writer.write_packages_to_files([pkg], base_dir="/tmp/output")
        """
        if output_path is not None and base_dir is not None:
            raise ValueError("Cannot specify both output_path and base_dir")
        if output_path is None and base_dir is None:
            raise ValueError("Must specify either output_path or base_dir")
        if output_path is not None and not output_path:
            raise ValueError("output_path cannot be empty")
        if base_dir is not None and not base_dir:
            raise ValueError("base_dir cannot be empty")

        # Determine base path from output_path or base_dir
        if output_path is not None:
            output_file = Path(output_path)
            base_path = output_file.parent
        else:
            base_path = Path(base_dir)  # type: ignore

        # Create packages directory
        packages_dir = base_path / "packages"
        packages_dir.mkdir(parents=True, exist_ok=True)

        for pkg in packages:
            self._write_package_to_files(pkg, packages_dir)

    def _write_package_to_files(self, pkg: AutosarPackage, parent_dir: Path, parent_path: Optional[List[str]] = None) -> None:
        """Write a package to directory structure with entity files.

        Requirements:
            SWR_WRITER_00011: JSON Directory Structure Creation

        Args:
            pkg: The package to write.
            parent_dir: Parent directory path where the package directory will be created.
            parent_path: List of parent package names for constructing full package path.
        """
        if parent_path is None:
            parent_path = []

        # Build full package path for this package
        full_package_path = parent_path + [pkg.name]
        package_path_str = "::".join(full_package_path)

        # For now, just create a placeholder file
        # Will implement full functionality in subsequent tasks
        sanitized_name = self._sanitize_filename(pkg.name)
        package_file = parent_dir / f"{sanitized_name}.json"
        package_file.write_text('{"name": "' + pkg.name + '"}', encoding="utf-8")

        # Recursively write subpackages
        for subpkg in pkg.subpackages:
            self._write_package_to_files(subpkg, parent_dir, full_package_path)

    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a package or class name for use as a filename.

        Requirements:
            SWR_WRITER_00012: JSON File Naming and Sanitization

        Removes or replaces characters that are invalid in file paths on Windows
        and other operating systems. This ensures that package names with special
        characters can still be written to the filesystem.

        Args:
            name: The package or class name to sanitize.

        Returns:
            A sanitized version of the name safe for use in file paths.

        Examples:
            >>> writer = JsonWriter()
            >>> writer._sanitize_filename("M2::AUTOSAR::DataTypes")
            'M2_AUTOSAR_DataTypes'
        """
        import re

        # Replace invalid filename characters with underscores
        # Invalid chars: < > : " / \ | ? * and control characters
        # Note: using \\ in pattern to match literal backslash
        invalid_chars = r'[<>:"/|?*\x00-\x1f]'
        # First handle backslash separately since it's tricky in regex
        sanitized = name.replace("\\", "_")
        # Then replace all other invalid characters
        sanitized = re.sub(invalid_chars, "_", sanitized)

        # Ensure name doesn't start or end with spaces or dots
        sanitized = sanitized.strip(". ")

        # If the name becomes empty or only underscores, use a default
        if not sanitized or sanitized.replace("_", "") == "":
            sanitized = "UnnamedPackage"

        return sanitized
