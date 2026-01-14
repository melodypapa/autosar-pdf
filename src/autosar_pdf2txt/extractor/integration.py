"""
Integrated AUTOSAR extraction using class-based approach
"""

from .parser import AutosarParser
from .hierarchy import PackageHierarchyBuilder
from .writer import OutputWriter
from .models import Package, Class
from typing import Dict


class AutosarExtractor:
    """
    AUTOSAR extractor class for high-level extraction operations.

    This class combines parsing, hierarchy building, and output writing
    into a unified workflow for extracting AUTOSAR specifications.
    """

    def __init__(self, progress_callback=None):
        """
        Initialize AUTOSAR extractor.

        Args:
            progress_callback: Optional callback function for progress updates
        """
        self.parser = AutosarParser()
        self.hierarchy_builder = PackageHierarchyBuilder()
        self.writer = OutputWriter()
        self.progress_callback = progress_callback

    def extract_from_pdf(
        self,
        pdf_path: str,
        output_path: str,
        format: str = "markdown",
        method: str = "pdfplumber",
    ) -> Dict[str, int]:
        """
        Extract package and class information from PDF file and write to output.

        Args:
            pdf_path (str): Path to input PDF file
            output_path (str): Path to output file
            format (str): Output format - "markdown" or "text" (default: "markdown")
            method (str): PDF extraction method - "pdfplumber" or "pypdf2" (default: "pdfplumber")

        Returns:
            Dict[str, int]: Summary statistics with keys 'total_packages' and 'total_classes'

        Raises:
            FileNotFoundError: If PDF file does not exist
            ValueError: If format or method is invalid
        """
        from ..core.converter import convert_pdf_to_text
        from pathlib import Path

        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        if format not in ["markdown", "text"]:
            raise ValueError(f"Invalid format '{format}'. Use 'markdown' or 'text'.")

        if method not in ["pdfplumber", "pypdf2"]:
            raise ValueError(
                f"Invalid method '{method}'. Use 'pdfplumber' or 'pypdf2'."
            )

        text = convert_pdf_to_text(
            pdf_path, method=method, progress_callback=self.progress_callback
        )
        packages = self.parser.parse(text)

        if format == "markdown":
            tree = self.hierarchy_builder.build_tree(packages)
            self.writer.write_markdown_hierarchy(
                tree,
                output_path,
                title=f"Package and Class Reference - {pdf_file.stem}",
            )
        else:
            self.writer.write_text_summary(packages, output_path)

        total_packages = len(packages)
        total_classes = sum(pkg.total_classes for pkg in packages)

        return {"total_packages": total_packages, "total_classes": total_classes}

    def _resolve_pdf_files(self, pdf_paths):
        """
        Resolve PDF file paths from input.

        Args:
            pdf_paths: Path to directory with PDFs or list of PDF paths

        Returns:
            list: List of Path objects for PDF files

        Raises:
            FileNotFoundError: If PDF directory or file does not exist
            ValueError: If path is not a directory
        """
        from pathlib import Path

        if isinstance(pdf_paths, str):
            pdf_dir = Path(pdf_paths)
            if not pdf_dir.exists():
                raise FileNotFoundError(f"Directory not found: {pdf_paths}")
            if not pdf_dir.is_dir():
                raise ValueError(f"Path must be a directory: {pdf_paths}")
            return sorted(pdf_dir.glob("*.pdf"))
        else:
            pdf_files = [Path(p) for p in pdf_paths]
            for pdf_file in pdf_files:
                if not pdf_file.exists():
                    raise FileNotFoundError(f"PDF file not found: {pdf_file}")
            return pdf_files

    def _validate_extraction_params(self, format, method):
        """
        Validate extraction parameters.

        Args:
            format (str): Output format
            method (str): PDF extraction method

        Raises:
            ValueError: If format or method is invalid
        """
        if format not in ["markdown", "text"]:
            raise ValueError(f"Invalid format '{format}'. Use 'markdown' or 'text'.")

        if method not in ["pdfplumber", "pypdf2"]:
            raise ValueError(
                f"Invalid method '{method}'. Use 'pdfplumber' or 'pypdf2'."
            )

    def _extract_packages_from_pdf(self, pdf_file, method):
        """
        Extract packages from a single PDF file.

        Args:
            pdf_file (Path): Path to PDF file
            method (str): PDF extraction method

        Returns:
            list: List of Package objects
        """
        from ..core.converter import convert_pdf_to_text

        text = convert_pdf_to_text(
            str(pdf_file),
            method=method,
            progress_callback=self.progress_callback,
        )
        return self.parser.parse(text)

    def _merge_packages(self, pdf_files, method):
        """
        Merge packages from multiple PDF files.

        Args:
            pdf_files (list): List of PDF file paths
            method (str): PDF extraction method

        Returns:
            list: Merged list of Package objects
        """
        merged_packages_dict: dict[str, list[Class]] = {}

        for idx, pdf_file in enumerate(pdf_files):
            if self.progress_callback:
                self.progress_callback(idx, len(pdf_files), str(pdf_file.name))

            packages = self._extract_packages_from_pdf(pdf_file, method)

            for pkg in packages:
                if pkg.name not in merged_packages_dict:
                    merged_packages_dict[pkg.name] = []
                merged_packages_dict[pkg.name].extend(pkg.classes)

        return [
            Package(name=pkg_name, classes=classes)
            for pkg_name, classes in merged_packages_dict.items()
        ]

    def _write_merged_output(self, merged_packages, output_path, format):
        """
        Write merged packages to output file.

        Args:
            merged_packages (list): List of merged Package objects
            output_path (str): Path to output file
            format (str): Output format
        """
        if format == "markdown":
            tree = self.hierarchy_builder.build_tree(merged_packages)
            self.writer.write_markdown_hierarchy(
                tree, output_path, title="Merged Package and Class Reference"
            )
        else:
            self.writer.write_text_summary(merged_packages, output_path)

    def _write_single_pdf_output(self, packages, pdf_file, output_path, format):
        """
        Write packages from a single PDF to output file.

        Args:
            packages (list): List of Package objects
            pdf_file (Path): Path to source PDF file
            output_path (str or None): Path to output file
            format (str): Output format
        """
        if output_path is None:
            base_name = pdf_file.stem
            ext = ".md" if format == "markdown" else "_summary.txt"
            single_output = str(pdf_file.parent / f"{base_name}{ext}")
        else:
            single_output = output_path

        if format == "markdown":
            tree = self.hierarchy_builder.build_tree(packages)
            self.writer.write_markdown_hierarchy(
                tree,
                single_output,
                title=f"Package and Class Reference - {pdf_file.stem}",
            )
        else:
            self.writer.write_text_summary(packages, single_output)

    def _calculate_statistics(self, packages):
        """
        Calculate statistics for a list of packages.

        Args:
            packages (list): List of Package objects

        Returns:
            dict: Statistics with keys 'total_packages' and 'total_classes'
        """
        return {
            "total_packages": len(packages),
            "total_classes": sum(pkg.total_classes for pkg in packages),
        }

    def extract_from_multiple_pdfs(
        self,
        pdf_paths,
        output_path=None,
        format: str = "markdown",
        method: str = "pdfplumber",
        merge_output: bool = True,
    ):
        """
        Extract package and class information from multiple PDF files.

        Args:
            pdf_paths: Path to directory with PDFs or list of PDF paths
            output_path: Path to output file (for merged output) or None
            format (str): Output format - "markdown" or "text" (default: "markdown")
            method (str): PDF extraction method - "pdfplumber" or "pypdf2" (default: "pdfplumber")
            merge_output (bool): If True, merge all packages; if False, return separate results (default: True)

        Returns:
            If merge_output=True, returns dict with keys 'total_packages' and 'total_classes'.
            If merge_output=False, returns dict mapping pdf_file to statistics dict.

        Raises:
            FileNotFoundError: If PDF directory or file does not exist
            ValueError: If format or method is invalid
        """
        pdf_files = self._resolve_pdf_files(pdf_paths)
        self._validate_extraction_params(format, method)

        if merge_output:
            merged_packages = self._merge_packages(pdf_files, method)

            if output_path:
                self._write_merged_output(merged_packages, output_path, format)

            return self._calculate_statistics(merged_packages)
        else:
            results = {}

            for idx, pdf_file in enumerate(pdf_files):
                if self.progress_callback:
                    self.progress_callback(idx, len(pdf_files), str(pdf_file.name))

                packages = self._extract_packages_from_pdf(pdf_file, method)
                self._write_single_pdf_output(packages, pdf_file, output_path, format)

                results[str(pdf_file)] = self._calculate_statistics(packages)

            return results


def extract_from_pdf(
    pdf_path: str,
    output_path: str,
    format: str = "markdown",
    method: str = "pdfplumber",
    progress_callback=None,
) -> Dict[str, int]:
    """
    Extract package and class information from PDF file and write to output (backward compatibility function).

    Args:
        pdf_path (str): Path to input PDF file
        output_path (str): Path to output file
        format (str): Output format - "markdown" or "text" (default: "markdown")
        method (str): PDF extraction method - "pdfplumber" or "pypdf2" (default: "pdfplumber")
        progress_callback: Optional callback function for progress updates

    Returns:
        Dict[str, int]: Summary statistics with keys 'total_packages' and 'total_classes'

    Raises:
        FileNotFoundError: If PDF file does not exist
        ValueError: If format or method is invalid
    """
    extractor = AutosarExtractor(progress_callback=progress_callback)
    return extractor.extract_from_pdf(pdf_path, output_path, format, method)


def extract_from_multiple_pdfs(
    pdf_paths,
    output_path=None,
    format: str = "markdown",
    method: str = "pdfplumber",
    merge_output: bool = True,
    progress_callback=None,
):
    """
    Extract package and class information from multiple PDF files (backward compatibility function).

    Args:
        pdf_paths: Path to directory with PDFs or list of PDF paths
        output_path: Path to output file (for merged output) or None
        format (str): Output format - "markdown" or "text" (default: "markdown")
        method (str): PDF extraction method - "pdfplumber" or "pypdf2" (default: "pdfplumber")
        merge_output (bool): If True, merge all packages; if False, return separate results (default: True)
        progress_callback: Optional callback function for progress updates

    Returns:
        If merge_output=True, returns dict with keys 'total_packages' and 'total_classes'.
        If merge_output=False, returns dict mapping pdf_file to statistics dict.
    """
    extractor = AutosarExtractor(progress_callback=progress_callback)
    return extractor.extract_from_multiple_pdfs(
        pdf_paths, output_path, format, method, merge_output
    )
