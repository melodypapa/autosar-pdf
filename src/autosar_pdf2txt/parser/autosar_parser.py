"""AUTOSAR PDF parser - extract packages and classes from PDF files."""

from autosar_pdf2txt.models import AutosarPackage
from autosar_pdf2txt.parser.pdf_reader import PDFReader
from autosar_pdf2txt.parser.hierarchy_parser import parse_hierarchy


class AutosarParser:
    """Parse AUTOSAR package and class hierarchies from PDF files.

    This class combines PDF text extraction with hierarchy parsing.

    Attributes:
        pdf_reader: The PDF reader instance.

    Examples:
        >>> parser = AutosarParser()
        >>> packages = parser.parse_pdf("autosar_spec.pdf")
        >>> for pkg in packages:
        ...     print(f"{pkg.name}: {len(pkg.classes)} classes")
    """

    def __init__(self, pdf_backend: str = "auto") -> None:
        """Initialize the AUTOSAR parser.

        Args:
            pdf_backend: PDF library to use ('auto', 'pdfplumber', 'fitz', 'pypdf').
        """
        self.pdf_reader = PDFReader(backend=pdf_backend)

    def parse_pdf(self, pdf_path: str) -> list[AutosarPackage]:
        """Parse an AUTOSAR PDF file and extract package/class hierarchy.

        Args:
            pdf_path: Path to the AUTOSAR PDF specification file.

        Returns:
            List of AutosarPackage objects with their classes.

        Raises:
            FileNotFoundError: If the PDF file doesn't exist.
            ValueError: If the PDF cannot be read or parsed.

        Examples:
            >>> parser = AutosarParser()
            >>> packages = parser.parse_pdf("AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf")
            >>> print(f"Found {len(packages)} top-level packages")
        """
        # Extract text from PDF
        text = self.pdf_reader.read_text(pdf_path)

        # Parse hierarchy
        packages = parse_hierarchy(text)

        return packages

    def parse_pdf_to_text(self, pdf_path: str) -> str:
        """Parse PDF and return extracted text without parsing hierarchy.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            Raw text extracted from the PDF.

        Raises:
            FileNotFoundError: If the PDF file doesn't exist.
            ValueError: If the PDF cannot be read.
        """
        return self.pdf_reader.read_text(pdf_path)


def parse_autosar_pdf(pdf_path: str, pdf_backend: str = "auto") -> list[AutosarPackage]:
    """Functional interface for parsing AUTOSAR PDF files.

    Args:
        pdf_path: Path to the AUTOSAR PDF specification file.
        pdf_backend: PDF library to use ('auto', 'pdfplumber', 'fitz', 'pypdf').

    Returns:
        List of AutosarPackage objects with their classes.

    Examples:
        >>> from autosar_pdf2txt.parser import parse_autosar_pdf
        >>> packages = parse_autosar_pdf("autosar_spec.pdf")
        >>> for pkg in packages:
        ...     for cls in pkg.classes:
        ...         print(f"{pkg.name} / {cls.name}")
    """
    parser = AutosarParser(pdf_backend=pdf_backend)
    return parser.parse_pdf(pdf_path)


def extract_pdf_text(pdf_path: str, pdf_backend: str = "auto") -> str:
    """Extract text from a PDF file without parsing.

    Args:
        pdf_path: Path to the PDF file.
        pdf_backend: PDF library to use ('auto', 'pdfplumber', 'fitz', 'pypdf').

    Returns:
        Raw text extracted from the PDF.

    Examples:
        >>> from autosar_pdf2txt.parser import extract_pdf_text
        >>> text = extract_pdf_text("document.pdf")
        >>> print(text[:100])  # First 100 characters
    """
    reader = PDFReader(backend=pdf_backend)
    return reader.read_text(pdf_path)
