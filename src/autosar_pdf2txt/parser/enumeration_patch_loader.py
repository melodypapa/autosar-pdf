"""Enumeration Patch Loader for TOML-based corrections.

This module loads and applies manual patches to enumeration definitions
that cannot be automatically extracted from PDFs due to table structure issues.

Requirements:
    SWR_PARSER_00037: TOML-based Enumeration Patch Loading
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import toml

from autosar_pdf2txt.models import AutosarDoc, AutosarEnumeration, AutosarEnumLiteral

logger = logging.getLogger(__name__)


class EnumerationPatchLoader:
    """Loads and applies TOML-based enumeration patches.

    This class handles:
    1. Loading patch definitions from TOML files
    2. Creating missing enumerations
    3. Correcting literal names in existing enumerations

    Usage:
        loader = EnumerationPatchLoader()
        loader.load_patches("patches/enumeration_patches.toml")
        loader.apply_to_document(autosar_doc)
    """

    def __init__(self):
        """Initialize the patch loader."""
        self.patches: Dict[str, Any] = {}
        self.corrections: List[Dict[str, str]] = []

    def load_patches(self, patch_file: str) -> None:
        """Load enumeration patches from a TOML file.

        Args:
            patch_file: Path to the TOML patch file.

        Raises:
            FileNotFoundError: If patch file doesn't exist.
            toml.TomlDecodeError: If TOML parsing fails.
        """
        patch_path = Path(patch_file)
        if not patch_path.exists():
            raise FileNotFoundError(f"Patch file not found: {patch_file}")

        logger.info(f"Loading enumeration patches from {patch_file}")

        try:
            data = toml.load(patch_path)

            # Load missing enumerations
            if "enumerations" in data:
                for enum_def in data["enumerations"]:
                    enum_name = enum_def["name"]
                    self.patches[enum_name] = enum_def
                    logger.debug(f"Loaded patch for enumeration '{enum_name}'")

            # Load literal name corrections
            if "literal_corrections" in data:
                self.corrections = data["literal_corrections"]
                logger.debug(f"Loaded {len(self.corrections)} literal name corrections")

            logger.info(f"Loaded {len(self.patches)} enumeration patches and {len(self.corrections)} corrections")

        except Exception as e:
            logger.error(f"Failed to load patch file {patch_file}: {e}")
            raise

    def apply_to_document(self, document: AutosarDoc, pdf_file: str = "PATCH_FILE") -> int:
        """Apply loaded patches to an AutosarDoc.

        This method:
        1. Creates missing enumerations from patches
        2. Corrects literal names in existing enumerations
        3. Adds missing literals to existing enumerations

        Args:
            document: The AutosarDoc to apply patches to.
            pdf_file: Optional PDF file name for source tracking (defaults to "PATCH_FILE").

        Returns:
            Number of patches applied.
        """
        patches_applied = 0

        # Apply missing enumerations
        for enum_name, enum_def in self.patches.items():
            # Check if enumeration already exists
            existing_enum = self._find_enumeration(document, enum_name)

            if existing_enum is None:
                # Create new enumeration from patch
                new_enum = self._create_enumeration_from_patch(enum_def, pdf_file)
                self._add_enumeration_to_document(document, new_enum)
                patches_applied += 1
                logger.info(f"Created enumeration '{enum_name}' from patch")
            else:
                # Add missing literals to existing enumeration
                literals_added = self._add_missing_literals(existing_enum, enum_def)
                if literals_added > 0:
                    patches_applied += 1
                    logger.info(f"Added {literals_added} literals to existing enumeration '{enum_name}'")

        # Apply literal name corrections
        for correction in self.corrections:
            enum_name = correction["enumeration"]
            wrong_name = correction["wrong_name"]
            correct_name = correction["correct_name"]

            enum = self._find_enumeration(document, enum_name)
            if enum:
                corrected = self._correct_literal_name(enum, wrong_name, correct_name)
                if corrected:
                    patches_applied += 1
                    logger.info(f"Corrected literal name '{wrong_name}' -> '{correct_name}' in '{enum_name}'")

        logger.info(f"Applied {patches_applied} total patches")
        return patches_applied

    def _find_enumeration(self, document: AutosarDoc, enum_name: str) -> Optional[AutosarEnumeration]:
        """Find an enumeration by name in the document.

        Args:
            document: The AutosarDoc to search.
            enum_name: The enumeration name to find.

        Returns:
            The AutosarEnumeration if found, None otherwise.
        """
        def search_packages(packages) -> Optional[AutosarEnumeration]:
            for pkg in packages:
                enum = pkg.get_enumeration(enum_name)
                if enum:
                    return enum
                # Recursively search subpackages
                result = search_packages(pkg.subpackages)
                if result:
                    return result
            return None

        return search_packages(document.packages)

    def _create_enumeration_from_patch(self, enum_def: Dict[str, Any], pdf_file: str) -> AutosarEnumeration:
        """Create an AutosarEnumeration from a patch definition.

        Args:
            enum_def: The enumeration patch definition.
            pdf_file: PDF file name for source tracking.

        Returns:
            A new AutosarEnumeration object.
        """
        from autosar_pdf2txt.models.base import AutosarDocumentSource

        name = enum_def["name"]
        package = enum_def["package"]
        literals_def = enum_def.get("literals", [])

        # Create literal objects
        literals = []
        for lit_def in literals_def:
            literal = AutosarEnumLiteral(
                name=lit_def["name"],
                index=lit_def.get("index"),
                value=lit_def.get("value"),
                description=lit_def.get("description"),
                tags=lit_def.get("tags", {})
            )
            literals.append(literal)

        # Create source location for the patched enumeration
        # Use page 1 as default since we don't have exact page info from patch file
        source = AutosarDocumentSource(
            pdf_file=pdf_file,
            page_number=1,
            autosar_standard=None,
            standard_release=None
        )

        return AutosarEnumeration(
            name=name,
            package=package,
            enumeration_literals=literals,
            sources=[source]
        )

    def _add_enumeration_to_document(self, document: AutosarDoc, enumeration: AutosarEnumeration) -> None:
        """Add an enumeration to the document, creating package structure if needed.

        Args:
            document: The AutosarDoc to add to.
            enumeration: The AutosarEnumeration to add.
        """
        package_path = enumeration.package
        if not package_path:
            logger.warning(f"Cannot add enumeration '{enumeration.name}': no package path")
            return

        # Split package path into components
        parts = package_path.split("::")
        current_pkg = None

        # Navigate/create package hierarchy
        for i, part in enumerate(parts):
            if i == 0:
                # Root package
                for pkg in document.packages:
                    if pkg.name == part:
                        current_pkg = pkg
                        break
                if current_pkg is None:
                    from autosar_pdf2txt.models import AutosarPackage
                    current_pkg = AutosarPackage(name=part)
                    document.packages.append(current_pkg)
            else:
                # Subpackage
                if current_pkg is None:
                    logger.warning(f"Cannot add enumeration '{enumeration.name}': parent package is None")
                    return
                found = False
                for subpkg in current_pkg.subpackages:
                    if subpkg.name == part:
                        current_pkg = subpkg
                        found = True
                        break
                if not found:
                    from autosar_pdf2txt.models import AutosarPackage
                    new_subpkg = AutosarPackage(name=part)
                    current_pkg.subpackages.append(new_subpkg)
                    current_pkg = new_subpkg

        # Add enumeration to the final package
        if current_pkg:
            current_pkg.add_type(enumeration)
        else:
            logger.warning(f"Failed to create package structure for '{enumeration.name}'")

    def _add_missing_literals(self, enumeration: AutosarEnumeration, enum_def: Dict[str, Any]) -> int:
        """Add missing literals from patch to an existing enumeration.

        Args:
            enumeration: The existing AutosarEnumeration.
            enum_def: The patch definition with literals to add.

        Returns:
            Number of literals added.
        """
        existing_names = {lit.name for lit in enumeration.enumeration_literals}
        literals_def = enum_def.get("literals", [])

        added_count = 0
        new_literals = list(enumeration.enumeration_literals)

        for lit_def in literals_def:
            lit_name = lit_def["name"]
            if lit_name not in existing_names:
                literal = AutosarEnumLiteral(
                    name=lit_name,
                    index=lit_def.get("index"),
                    value=lit_def.get("value"),
                    description=lit_def.get("description"),
                    tags=lit_def.get("tags", {})
                )
                new_literals.append(literal)
                existing_names.add(lit_name)
                added_count += 1
                logger.debug(f"Added literal '{lit_name}' to enumeration '{enumeration.name}'")

        # Update enumeration with new literals
        if added_count > 0:
            enumeration.enumeration_literals = tuple(new_literals)

        return added_count

    def _correct_literal_name(self, enumeration: AutosarEnumeration, wrong_name: str, correct_name: str) -> bool:
        """Correct a literal name in an enumeration.

        Args:
            enumeration: The AutosarEnumeration to correct.
            wrong_name: The wrong literal name to find.
            correct_name: The correct literal name to replace with.

        Returns:
            True if correction was applied, False otherwise.
        """
        new_literals = []
        corrected = False

        for lit in enumeration.enumeration_literals:
            if lit.name == wrong_name:
                # Create new literal with corrected name
                corrected_lit = AutosarEnumLiteral(
                    name=correct_name,
                    index=lit.index,
                    value=lit.value,
                    description=lit.description,
                    tags=lit.tags.copy() if lit.tags else {}
                )
                new_literals.append(corrected_lit)
                corrected = True
                logger.debug(f"Corrected literal '{wrong_name}' -> '{correct_name}' in '{enumeration.name}'")
            else:
                new_literals.append(lit)

        if corrected:
            enumeration.enumeration_literals = tuple(new_literals)

        return corrected
