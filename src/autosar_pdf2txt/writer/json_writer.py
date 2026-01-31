"""JSON writer for AUTOSAR packages and classes."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

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
            SWR_WRITER_00013: JSON Index File Output

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

        # Write all packages
        for pkg in packages:
            self._write_package_to_files(pkg, packages_dir)

        # Write index.json
        self._write_index(packages, base_path)

    def _write_index(self, packages: List[AutosarPackage], base_path: Path) -> None:
        """Write the root index.json file.

        Requirements:
            SWR_WRITER_00013: JSON Index File Output

        Args:
            packages: List of top-level AutosarPackage objects.
            base_path: Base directory where index.json will be written.
        """
        # Collect metadata
        total_classes = 0
        total_enums = 0
        total_primitives = 0
        source_files = set()

        def count_entities(pkg: AutosarPackage) -> None:
            nonlocal total_classes, total_enums, total_primitives
            for typ in pkg.types:
                if hasattr(typ, "attributes"):  # AutosarClass or AutosarPrimitive
                    if typ.__class__.__name__ == "AutosarClass":
                        total_classes += 1
                    elif typ.__class__.__name__ == "AutosarPrimitive":
                        total_primitives += 1
                elif hasattr(typ, "enumeration_literals"):  # AutosarEnumeration
                    total_enums += 1

            # Collect source files
            for typ in pkg.types:
                if typ.sources:
                    for source in typ.sources:
                        source_files.add(source.pdf_file)

            # Recursively count subpackages
            for subpkg in pkg.subpackages:
                count_entities(subpkg)

        for pkg in packages:
            count_entities(pkg)

        # Build package references
        package_refs = []
        for pkg in packages:
            ref = {
                "name": pkg.name,
                "file": f"packages/{self._sanitize_filename(pkg.name)}.json",
                "class_count": 0,  # Will be calculated in package metadata
                "subpackages": [subpkg.name for subpkg in pkg.subpackages],
            }
            package_refs.append(ref)

        # Build index
        index = {
            "version": "1.0",
            "metadata": {
                "generated_at": datetime.utcnow().isoformat() + "Z",
                "source_files": sorted(list(source_files)),
                "total_packages": sum(1 for _ in packages),
                "total_classes": total_classes,
                "total_enumerations": total_enums,
                "total_primitives": total_primitives,
            },
            "packages": package_refs,
        }

        # Write index.json
        index_file = base_path / "index.json"
        with open(index_file, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

    def _write_package_to_files(self, pkg: AutosarPackage, parent_dir: Path, parent_path: Optional[List[str]] = None) -> None:
        """Write a package to directory structure with entity files.

        Requirements:
            SWR_WRITER_00011: JSON Directory Structure Creation
            SWR_WRITER_00014: JSON Package Metadata File Output

        Creates:
        - Package metadata JSON file with summary and file references
        - Separate entity files for classes, enumerations, primitives
        """
        if parent_path is None:
            parent_path = []

        # Build full package path for this package
        full_package_path = parent_path + [pkg.name]
        package_path_str = "::".join(full_package_path)

        # Sanitize package name for filename
        sanitized_name = self._sanitize_filename("::".join(full_package_path))

        # Count entities in this package
        class_count = sum(1 for typ in pkg.types if typ.__class__.__name__ == "AutosarClass")
        enum_count = sum(1 for typ in pkg.types if typ.__class__.__name__ == "AutosarEnumeration")
        primitive_count = sum(1 for typ in pkg.types if typ.__class__.__name__ == "AutosarPrimitive")

        # Build entity file references
        entity_files = {}
        if class_count > 0:
            entity_files["classes"] = f"packages/{sanitized_name}.classes.json"
        if enum_count > 0:
            entity_files["enumerations"] = f"packages/{sanitized_name}.enums.json"
        if primitive_count > 0:
            entity_files["primitives"] = f"packages/{sanitized_name}.primitives.json"

        # Build subpackage references
        subpackage_refs = []
        for subpkg in pkg.subpackages:
            sub_full_path = "::".join(full_package_path + [subpkg.name])
            subpackage_refs.append({
                "name": subpkg.name,
                "full_path": sub_full_path,
                "file": f"packages/{self._sanitize_filename(sub_full_path)}.json"
            })

        # Build package metadata
        package_metadata = {
            "name": package_path_str,
            "path": package_path_str,
            "files": entity_files,
            "subpackages": subpackage_refs,
            "summary": {
                "class_count": class_count,
                "enumeration_count": enum_count,
                "primitive_count": primitive_count
            }
        }

        # Write package metadata file
        package_file = parent_dir / f"{sanitized_name}.json"
        with open(package_file, "w", encoding="utf-8") as f:
            json.dump(package_metadata, f, indent=2, ensure_ascii=False)

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

        # Replace :: delimiter with single underscore
        sanitized = name.replace("::", "_")

        # Replace other invalid filename characters with underscores
        # Invalid chars: < > : " / \ | ? * and control characters
        # Note: using \\ in pattern to match literal backslash
        invalid_chars = r'[<>:"/|?*\x00-\x1f]'
        # First handle backslash separately since it's tricky in regex
        sanitized = sanitized.replace("\\", "_")
        # Then replace all other invalid characters
        sanitized = re.sub(invalid_chars, "_", sanitized)

        # Collapse multiple underscores into single underscore
        sanitized = re.sub(r"_+", "_", sanitized)

        # Ensure name doesn't start or end with spaces or dots
        sanitized = sanitized.strip(". ")

        # If the name becomes empty or only underscores, use a default
        if not sanitized or sanitized.replace("_", "") == "":
            sanitized = "UnnamedPackage"

        return sanitized
