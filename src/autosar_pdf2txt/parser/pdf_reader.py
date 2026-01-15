"""PDF text extraction with backend abstraction."""


try:
    import pdfplumber

    HAS_PDFPLUMBER = True
except ImportError:  # pragma: no cover
    HAS_PDFPLUMBER = False

try:
    import pypdf

    HAS_PYPDF = True
except ImportError:  # pragma: no cover
    HAS_PYPDF = False

try:
    import fitz  # type: ignore[import-not-found]  # PyMuPDF

    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False


class PDFReader:
    """Read text from PDF files with multiple backend support.

    Supported backends (in order of preference):
    1. pdfplumber - Best table extraction, good text quality
    2. fitz/PyMuPDF - Fastest, good text quality
    3. pypdf - Fallback, widely available

    Attributes:
        backend: The PDF library being used.
    """

    def __init__(self, backend: str = "auto") -> None:
        """Initialize the PDF reader.

        Args:
            backend: PDF library to use ('auto', 'pdfplumber', 'fitz', 'pypdf').

        Raises:
            ValueError: If the specified backend is not available.
        """
        self.backend = self._select_backend(backend)

    def _select_backend(self, backend: str) -> str:
        """Select the PDF backend based on availability.

        Args:
            backend: Preferred backend name.

        Returns:
            The selected backend name.

        Raises:
            ValueError: If no suitable backend is available.
        """
        if backend == "auto":
            if HAS_PDFPLUMBER:
                return "pdfplumber"
            elif HAS_FITZ:
                return "fitz"
            elif HAS_PYPDF:
                return "pypdf"
            else:
                raise ValueError(
                    "No PDF backend available. Install one of: pdfplumber, PyMuPDF, pypdf"
                )

        if backend == "pdfplumber" and not HAS_PDFPLUMBER:
            raise ValueError("pdfplumber backend not available. Install: pip install pdfplumber")
        if backend == "fitz" and not HAS_FITZ:
            raise ValueError("fitz backend not available. Install: pip install PyMuPDF")
        if backend == "pypdf" and not HAS_PYPDF:
            raise ValueError("pypdf backend not available. Install: pip install pypdf")

        return backend

    def read_text(self, pdf_path: str) -> str:
        """Extract all text from a PDF file.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            Extracted text as a single string with pages separated by form feeds.

        Raises:
            FileNotFoundError: If the PDF file doesn't exist.
            ValueError: If there's an error reading the PDF.
        """
        if self.backend == "pdfplumber":
            return self._read_with_pdfplumber(pdf_path)
        elif self.backend == "fitz":  # pragma: no cover
            return self._read_with_fitz(pdf_path)
        elif self.backend == "pypdf":
            return self._read_with_pypdf(pdf_path)
        else:
            raise ValueError(f"Unknown backend: {self.backend}")

    def _read_with_pdfplumber(self, pdf_path: str) -> str:
        """Extract text using pdfplumber.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            Extracted text.

        Raises:
            ValueError: If pdfplumber is not available or reading fails.
        """
        if not HAS_PDFPLUMBER:  # pragma: no cover
            raise ValueError("pdfplumber is not available")

        try:
            with pdfplumber.open(pdf_path) as pdf:
                pages_text = []
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        pages_text.append(text)
                return "\f\n".join(pages_text)
        except Exception as e:
            raise ValueError(f"Error reading PDF with pdfplumber: {e}")

    def _read_with_fitz(self, pdf_path: str) -> str:
        """Extract text using PyMuPDF (fitz).

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            Extracted text.

        Raises:
            ValueError: If fitz is not available or reading fails.
        """
        if not HAS_FITZ:  # pragma: no cover
            raise ValueError("fitz is not available")

        try:
            doc = fitz.open(pdf_path)
            pages_text = []
            for page in doc:
                text = page.get_text()
                if text:
                    pages_text.append(text)
            doc.close()
            return "\f\n".join(pages_text)
        except Exception as e:
            raise ValueError(f"Error reading PDF with fitz: {e}")

    def _read_with_pypdf(self, pdf_path: str) -> str:
        """Extract text using pypdf.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            Extracted text.

        Raises:
            ValueError: If pypdf is not available or reading fails.
        """
        if not HAS_PYPDF:  # pragma: no cover
            raise ValueError("pypdf is not available")

        try:
            with open(pdf_path, "rb") as f:
                pdf_reader = pypdf.PdfReader(f)
                pages_text = []
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        pages_text.append(text)
                return "\f\n".join(pages_text)
        except FileNotFoundError:
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        except Exception as e:
            raise ValueError(f"Error reading PDF with pypdf: {e}")


def read_pdf(pdf_path: str, backend: str = "auto") -> str:
    """Functional interface for reading PDF files.

    Args:
        pdf_path: Path to the PDF file.
        backend: PDF library to use ('auto', 'pdfplumber', 'fitz', 'pypdf').

    Returns:
        Extracted text.

    Examples:
        >>> text = read_pdf("document.pdf")
        >>> text = read_pdf("document.pdf", backend="pdfplumber")
    """
    reader = PDFReader(backend=backend)
    return reader.read_text(pdf_path)
