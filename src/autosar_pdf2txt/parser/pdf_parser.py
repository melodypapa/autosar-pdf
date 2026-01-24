"""PDF parser for extracting AUTOSAR class hierarchies from PDF files.

This module provides the main PdfParser class that orchestrates parsing
and delegates to specialized parsers for each AUTOSAR type.

Requirements:
    SWR_PARSER_00001: PDF Parser Initialization
    SWR_PARSER_00002: Backend Validation
    SWR_PARSER_00003: PDF File Parsing
    SWR_PARSER_00006: Package Hierarchy Building
    SWR_PARSER_00017: AUTOSAR Class Parent Resolution
    SWR_PARSER_00018: Ancestry Analysis for Parent Resolution
    SWR_PARSER_00019: Backend Warning Suppression
    SWR_PARSER_00022: PDF Source Location Extraction
    SWR_PARSER_00027: Parser Backward Compatibility
"""

import logging
import warnings
from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional, Union

from autosar_pdf2txt.models import (
    AutosarClass,
    AutosarDoc,
    AutosarEnumeration,
    AutosarPackage,
    AutosarPrimitive,
)

from autosar_pdf2txt.parser.class_parser import AutosarClassParser
from autosar_pdf2txt.parser.enumeration_parser import AutosarEnumerationParser
from autosar_pdf2txt.parser.primitive_parser import AutosarPrimitiveParser

logger = logging.getLogger(__name__)


class PdfParser:
    """Parse AUTOSAR PDF files to extract package and class hierarchies.

    Requirements:
        SWR_PARSER_00001: PDF Parser Initialization

    The parser extracts class definitions from PDF files and builds
    AutosarPackage and AutosarClass objects using specialized parsers
    for each AUTOSAR type.

    Usage:
        >>> parser = PdfParser()
        >>> packages = parser.parse_pdf("path/to/file.pdf")
        >>> print(len(packages))
    """

    def __init__(self) -> None:
        """Initialize the PDF parser.

        Requirements:
            SWR_PARSER_00001: PDF Parser Initialization
            SWR_PARSER_00007: PDF Backend Support - pdfplumber

        Raises:
            ImportError: If pdfplumber is not installed.
        """
        self._validate_backend()

        # Instantiate specialized parsers
        self._class_parser = AutosarClassParser()
        self._enum_parser = AutosarEnumerationParser()
        self._primitive_parser = AutosarPrimitiveParser()

    def _validate_backend(self) -> None:
        """Validate that pdfplumber backend is available.

        Requirements:
            SWR_PARSER_00002: Backend Validation
            SWR_PARSER_00007: PDF Backend Support - pdfplumber

        Raises:
            ImportError: If pdfplumber is not installed.
        """
        try:
            import pdfplumber as _  # noqa: F401
        except ImportError:  # pragma: no cover
            raise ImportError(
                "pdfplumber is not installed. Install it with: pip install pdfplumber"
            )

    def parse_pdf(self, pdf_path: str) -> AutosarDoc:
        """Parse a PDF file and extract the package hierarchy.

        This is a convenience method for parsing a single PDF. Internally calls
        parse_pdfs() to ensure consistent behavior whether parsing one or many PDFs.

        Requirements:
            SWR_PARSER_00003: PDF File Parsing

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            AutosarDoc containing packages and root classes.

        Raises:
            FileNotFoundError: If the PDF file doesn't exist.
            Exception: If PDF parsing fails.
        """
        return self.parse_pdfs([pdf_path])

    def parse_pdfs(self, pdf_paths: List[str]) -> AutosarDoc:
        """Parse multiple PDF files and extract the complete package hierarchy.

        This method parses all PDFs first, then builds the package hierarchy and
        resolves parent/children relationships on the complete model. This ensures
        that parent classes are found even if they are defined in later PDFs.

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00006: Package Hierarchy Building
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution

        Args:
            pdf_paths: List of paths to PDF files.

        Returns:
            AutosarDoc containing packages and root classes from all PDFs.

        Raises:
            FileNotFoundError: If any PDF file doesn't exist.
            Exception: If PDF parsing fails.
        """
        # Phase 1: Extract all model objects from ALL PDFs first
        all_models: List[Union[AutosarClass, AutosarEnumeration, AutosarPrimitive]] = []
        for pdf_path in pdf_paths:
            logger.info(f"  - {pdf_path}")
            models = self._extract_models(pdf_path)
            all_models.extend(models)

        # Phase 2: Build complete package hierarchy once
        return self._build_package_hierarchy(all_models)

    def _extract_models(self, pdf_path: str) -> List[Union[AutosarClass, AutosarEnumeration, AutosarPrimitive]]:
        """Extract all model objects from the PDF.

        Requirements:
            SWR_PARSER_00003: PDF File Parsing

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            List of model objects (AutosarClass, AutosarEnumeration, AutosarPrimitive).
        """
        return self._extract_with_pdfplumber(pdf_path)

    def _extract_with_pdfplumber(self, pdf_path: str) -> List[Union[AutosarClass, AutosarEnumeration, AutosarPrimitive]]:
        """Extract model objects using pdfplumber.

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00007: PDF Backend Support - pdfplumber
            SWR_PARSER_00009: Proper Word Spacing in PDF Text Extraction
            SWR_PARSER_00019: PDF Backend Warning Suppression
            SWR_MODEL_00027: AUTOSAR Source Location Representation
            SWR_PARSER_00022: PDF Source Location Extraction

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            List of model objects with source information.
        """
        import pdfplumber

        models: List[Union[AutosarClass, AutosarEnumeration, AutosarPrimitive]] = []

        # Extract PDF filename for source tracking
        pdf_filename = Path(pdf_path).name

        # SWR_PARSER_00019: Suppress pdfplumber warnings that don't affect parsing
        # Many AUTOSAR PDFs have minor PDF specification errors that generate warnings
        # but don't affect text extraction correctness
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning, module="pdfplumber")

            try:
                with pdfplumber.open(pdf_path) as pdf:
                    # Process each page individually to track page numbers for source information
                    # Maintain parsing state across pages for multi-page definitions
                    current_models: Dict[int, Union[AutosarClass, AutosarEnumeration, AutosarPrimitive]] = {}
                    model_parsers: Dict[int, str] = {}  # Maps model index to parser type

                    for page_num, page in enumerate(pdf.pages, start=1):
                        text_buffer = StringIO()

                        # Use extract_words() with x_tolerance=1 to properly extract words with spaces
                        # This fixes the issue where words are concatenated without spaces
                        words = page.extract_words(x_tolerance=1)

                        if words:
                            # Reconstruct text from words, preserving line breaks
                            # Group words by their vertical position (top coordinate)
                            current_y = None
                            for word in words:
                                text = word['text']
                                top = word['top']

                                # Check if we've moved to a new line
                                if current_y is not None and abs(top - current_y) > 5:
                                    text_buffer.write("\n")

                                text_buffer.write(text + " ")
                                current_y = top

                            # Add newline after each page
                            text_buffer.write("\n")

                        page_text = text_buffer.getvalue()
                        # Parse text and get models with their parsers
                        page_models = self._parse_page_text(
                            page_text,
                            pdf_filename=pdf_filename,
                            page_number=page_num,
                            current_models=current_models,
                            model_parsers=model_parsers,
                        )
                        models.extend(page_models)

            except Exception as e:
                raise Exception(f"Failed to parse PDF with pdfplumber: {e}") from e

        return models

    def _parse_page_text(
        self,
        text: str,
        pdf_filename: Optional[str] = None,
        page_number: Optional[int] = None,
        current_models: Optional[Dict[int, Union[AutosarClass, AutosarEnumeration, AutosarPrimitive]]] = None,
        model_parsers: Optional[Dict[int, str]] = None,
    ) -> List[Union[AutosarClass, AutosarEnumeration, AutosarPrimitive]]:
        """Parse model definitions from extracted text.

        This method processes the text from a single page and:
        1. Detects new type definitions (Class, Enumeration, Primitive)
        2. Delegates to the appropriate specialized parser
        3. Continues parsing for existing models across pages

        Requirements:
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00013: Recognition of Primitive and Enumeration Class Definition Patterns
            SWR_PARSER_00012: Multi-Line Attribute Handling
            SWR_PARSER_00014: Enumeration Literal Header Recognition
            SWR_PARSER_00015: Enumeration Literal Extraction from PDF
            SWR_PARSER_00016: Enumeration Literal Section Termination
            SWR_MODEL_00027: AUTOSAR Source Location Representation
            SWR_PARSER_00022: PDF Source Location Extraction

        Args:
            text: The extracted text from PDF.
            pdf_filename: Optional PDF filename for source tracking.
            page_number: Optional page number for source tracking.
            current_models: Dictionary of current models being parsed (for multi-page support).
            model_parsers: Dictionary mapping model indices to parser types.

        Returns:
            List of model objects parsed from this page.
        """
        if current_models is None:
            current_models = {}
        if model_parsers is None:
            model_parsers = {}

        models: List[Union[AutosarClass, AutosarEnumeration, AutosarPrimitive]] = []
        lines = text.split("\n")

        i = 0
        new_model: Optional[Union[AutosarClass, AutosarEnumeration, AutosarPrimitive]] = None
        while i < len(lines):
            line = lines[i].strip()

            if not line:
                i += 1
                continue

            # Try to match type definition patterns
            class_match = self._class_parser.CLASS_PATTERN.match(line)
            primitive_match = self._primitive_parser.PRIMITIVE_PATTERN.match(line)
            enumeration_match = self._enum_parser.ENUMERATION_PATTERN.match(line)

            if class_match or primitive_match or enumeration_match:
                # This is a new type definition
                # Delegate to appropriate parser
                if class_match:
                    new_model = self._class_parser.parse_definition(
                        lines, i, pdf_filename, page_number
                    )
                    parser_type = "class"
                elif primitive_match:
                    new_model = self._primitive_parser.parse_definition(
                        lines, i, pdf_filename, page_number
                    )
                    parser_type = "primitive"
                else:  # enumeration_match
                    new_model = self._enum_parser.parse_definition(
                        lines, i, pdf_filename, page_number
                    )
                    parser_type = "enumeration"

                if new_model:
                    # Store the model for continuation parsing
                    model_index = len(models)
                    current_models[model_index] = new_model
                    model_parsers[model_index] = parser_type
                    models.append(new_model)

                    # Continue parsing with this model
                    i += 1
                    while i < len(lines):
                        # Use the appropriate parser to continue parsing
                        if parser_type == "class":
                            new_i, is_complete = self._class_parser.continue_parsing(
                                new_model, lines, i
                            )
                        elif parser_type == "primitive":
                            new_i, is_complete = self._primitive_parser.continue_parsing(
                                new_model, lines, i
                            )
                        else:  # enumeration
                            new_i, is_complete = self._enum_parser.continue_parsing(
                                new_model, lines, i
                            )

                        i = new_i

                        if is_complete:
                            # Remove from current_models as parsing is complete
                            if model_index in current_models:
                                del current_models[model_index]
                                del model_parsers[model_index]
                            # Advance past the line that caused completion
                            i += 1
                            break
                    continue

            # Try to continue parsing existing models
            if current_models:
                for model_index, current_model in list(current_models.items()):
                    parser_type = model_parsers[model_index]
                    
                    if parser_type == "class":
                        new_i, is_complete = self._class_parser.continue_parsing(
                            current_model, lines, i
                        )
                    elif parser_type == "primitive":
                        new_i, is_complete = self._primitive_parser.continue_parsing(
                            current_model, lines, i
                        )
                    else:  # enumeration
                        new_i, is_complete = self._enum_parser.continue_parsing(
                            current_model, lines, i
                        )

                    i = new_i

                    if is_complete:
                        # Remove from current_models as parsing is complete
                        del current_models[model_index]
                        del model_parsers[model_index]
                        # Advance past the line that caused completion
                        i += 1
                    else:
                        # Model still being parsed, don't advance i
                        break
            else:
                i += 1

        return models

    def _build_package_hierarchy(self, models: List[Union[AutosarClass, AutosarEnumeration, AutosarPrimitive]]) -> AutosarDoc:
        """Build complete package hierarchy from model objects.

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building
            SWR_MODEL_00023: AUTOSAR Document Model

        Args:
            models: List of model objects (AutosarClass, AutosarEnumeration, AutosarPrimitive).

        Returns:
            AutosarDoc containing packages and root classes.
        """
        # Filter out invalid models (those with empty or whitespace names)
        valid_models = [
            model for model in models
            if model.name and not model.name.isspace()
        ]

        # Create a dictionary to track packages by path
        packages_dict: Dict[str, AutosarPackage] = {}

        # Process each model and build package hierarchy
        for model in valid_models:
            # Get or create package chain
            current_pkg = self._get_or_create_package_chain(
                model.package, packages_dict
            )

            # Add model to package
            if isinstance(model, AutosarClass):
                current_pkg.add_type(model)
            elif isinstance(model, AutosarEnumeration):
                current_pkg.add_type(model)
            elif isinstance(model, AutosarPrimitive):
                current_pkg.add_type(model)

        # Collect root packages (those that are not subpackages of any other package)
        all_subpackages: set[str] = set()
        for pkg in packages_dict.values():
            all_subpackages.update(subpkg.name for subpkg in pkg.subpackages)

        root_packages = [
            pkg for pkg in packages_dict.values()
            if pkg.name not in all_subpackages
        ]

        # Collect root classes (classes with no bases)
        root_classes = [
            model for model in valid_models
            if isinstance(model, AutosarClass) and not model.bases
        ]

        # Create AutosarDoc
        doc = AutosarDoc(packages=root_packages, root_classes=root_classes)

        # Resolve parent/children references (pass all packages, not just root)
        all_packages = list(packages_dict.values())
        self._resolve_parent_references(all_packages)

        return doc

    def _get_or_create_package_chain(
        self, package_path: str, packages_dict: Dict[str, AutosarPackage]
    ) -> AutosarPackage:
        """Get or create package chain for a given package path.

        Requirements:
            SWR_PARSER_00006: Package Hierarchy Building

        Args:
            package_path: The package path (e.g., "M2::AUTOSAR::DataTypes").
            packages_dict: Dictionary of existing packages.

        Returns:
            The leaf package in the chain.
        """
        # Remove M2:: prefix if present
        if package_path.startswith("M2::"):
            package_path = package_path[4:]

        # Split by ::
        parts = package_path.split("::")

        # Build package chain
        current_path = ""
        current_pkg: Optional[AutosarPackage] = None

        for part in parts:
            if current_path:
                current_path += "::"
            current_path += part

            if current_path not in packages_dict:
                new_pkg = AutosarPackage(name=part)
                packages_dict[current_path] = new_pkg

                if current_pkg:
                    current_pkg.add_subpackage(new_pkg)

            current_pkg = packages_dict[current_path]

        # current_pkg is guaranteed to be non-None here because we always create packages
        assert current_pkg is not None
        return current_pkg

    def _resolve_parent_references(self, packages: List[AutosarPackage]) -> List[AutosarClass]:
        """Resolve parent and children references for all classes.

        Requirements:
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution
            SWR_PARSER_00018: Ancestry Analysis for Parent Resolution

        Args:
            packages: List of packages to process.

        Returns:
            List of root classes (classes without parents).
        """
        # Build ancestry cache for efficient parent lookup
        ancestry_cache = self._build_ancestry_cache(packages)

        # Track warned base classes for deduplication
        warned_bases: set[str] = set()

        # Set parent references for all classes
        root_classes: List[AutosarClass] = []
        for pkg in packages:
            for typ in pkg.types:
                if isinstance(typ, AutosarClass):
                    self._set_parent_references(typ, ancestry_cache, packages, warned_bases)
                    if typ.parent is None:
                        root_classes.append(typ)

        # Populate children lists
        self._populate_children_lists(ancestry_cache, packages)

        return root_classes

    def _build_ancestry_cache(self, packages: List[AutosarPackage]) -> Dict[str, List[str]]:
        """Build a cache of ancestry relationships for efficient parent lookup.

        Requirements:
            SWR_PARSER_00018: Ancestry Analysis for Parent Resolution

        Args:
            packages: List of packages to process.

        Returns:
            Dictionary mapping class names to lists of base class names.
        """
        cache: Dict[str, List[str]] = {}
        for pkg in packages:
            for typ in pkg.types:
                if isinstance(typ, AutosarClass):
                    cache[typ.name] = typ.bases
        return cache

    def _set_parent_references(
        self,
        cls: AutosarClass,
        ancestry_cache: Dict[str, List[str]],
        packages: List[AutosarPackage],
        warned_bases: set[str],
    ) -> None:
        """Set parent reference for a class by finding the actual direct parent.

        Requirements:
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution
            SWR_PARSER_00018: Ancestry Analysis for Parent Resolution

        Args:
            cls: The class to set parent for.
            ancestry_cache: Cache of ancestry relationships.
            packages: List of all packages.
            warned_bases: Set of base classes that have already been warned about.
        """
        if not cls.bases:
            return

        # Try to find the most specific parent by filtering out ARObject
        # and choosing the last (most specific) base class
        filtered_bases = [b for b in cls.bases if b != "ARObject"]

        # If we have bases after filtering ARObject, use the most specific one
        # Otherwise, fall back to the original bases (may include ARObject)
        bases_to_check = filtered_bases if filtered_bases else cls.bases

        # Find the last (most specific) base class that exists in the model
        # Also warn about ALL missing bases (not just until first found)
        parent_found = False
        for base_name in reversed(bases_to_check):
            base_class = self._find_class_in_all_packages(base_name, packages)
            if base_class is not None and not parent_found:
                cls.parent = base_class.name
                parent_found = True
            else:
                # Base class not found - log warning if not already warned
                if base_name not in warned_bases:
                    logger.warning(
                        "Class '%s' references base class '%s' which could not be located in the model",
                        cls.name,
                        base_name,
                    )
                    warned_bases.add(base_name)

    def _populate_children_lists(
        self, ancestry_cache: Dict[str, List[str]], packages: List[AutosarPackage]
    ) -> None:
        """Populate children lists for all classes.

        Requirements:
            SWR_PARSER_00017: AUTOSAR Class Parent Resolution

        Args:
            ancestry_cache: Cache of ancestry relationships.
            packages: List of all packages.
        """
        # Build a parent-to-children mapping (O(n) complexity)
        parent_to_children: Dict[str, List[str]] = {}
        for pkg in packages:
            for typ in pkg.types:
                if isinstance(typ, AutosarClass) and typ.parent:
                    if typ.parent not in parent_to_children:
                        parent_to_children[typ.parent] = []
                    parent_to_children[typ.parent].append(typ.name)
        
        # Populate children lists using the mapping
        for pkg in packages:
            for typ in pkg.types:
                if isinstance(typ, AutosarClass) and typ.name in parent_to_children:
                    typ.children = parent_to_children[typ.name]

    def _find_class_in_all_packages(
        self, class_name: str, packages: List[AutosarPackage]
    ) -> Optional[AutosarClass]:
        """Find a class by name across all packages.

        Args:
            class_name: Name of the class to find.
            packages: List of packages to search.

        Returns:
            The AutosarClass if found, None otherwise.
        """
        for pkg in packages:
            cls = pkg.get_class(class_name)
            if cls is not None:
                return cls
        return None