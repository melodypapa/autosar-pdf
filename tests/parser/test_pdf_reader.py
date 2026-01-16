"""Tests for PDF reader.

Test coverage for pdf_reader.py targeting 100%.
"""

from unittest.mock import Mock, patch

import pytest

from autosar_pdf2txt.parser.pdf_reader import PDFReader, read_pdf


class TestPDFReader:
    """Tests for PDFReader class."""

    def test_init_auto_backend_with_pdfplumber(self) -> None:
        """Test auto-selecting pdfplumber backend."""
        with patch("autosar_pdf2txt.parser.pdf_reader.HAS_PDFPLUMBER", True):
            with patch("autosar_pdf2txt.parser.pdf_reader.HAS_FITZ", False):
                with patch("autosar_pdf2txt.parser.pdf_reader.HAS_PYPDF", False):
                    reader = PDFReader(backend="auto")
                    assert reader.backend == "pdfplumber"

    def test_init_auto_backend_with_fitz(self) -> None:
        """Test auto-selecting fitz backend."""
        with patch("autosar_pdf2txt.parser.pdf_reader.HAS_PDFPLUMBER", False):
            with patch("autosar_pdf2txt.parser.pdf_reader.HAS_FITZ", True):
                with patch("autosar_pdf2txt.parser.pdf_reader.HAS_PYPDF", False):
                    reader = PDFReader(backend="auto")
                    assert reader.backend == "fitz"

    def test_init_auto_backend_with_pypdf(self) -> None:
        """Test auto-selecting pypdf backend."""
        with patch("autosar_pdf2txt.parser.pdf_reader.HAS_PDFPLUMBER", False):
            with patch("autosar_pdf2txt.parser.pdf_reader.HAS_FITZ", False):
                with patch("autosar_pdf2txt.parser.pdf_reader.HAS_PYPDF", True):
                    reader = PDFReader(backend="auto")
                    assert reader.backend == "pypdf"

    def test_init_auto_backend_no_backend_available(self) -> None:
        """Test ValueError is raised when no backend is available."""
        with patch("autosar_pdf2txt.parser.pdf_reader.HAS_PDFPLUMBER", False):
            with patch("autosar_pdf2txt.parser.pdf_reader.HAS_FITZ", False):
                with patch("autosar_pdf2txt.parser.pdf_reader.HAS_PYPDF", False):
                    with pytest.raises(ValueError, match="No PDF backend available"):
                        PDFReader(backend="auto")

    def test_init_pdfplumber_backend_available(self) -> None:
        """Test specifying pdfplumber backend (available)."""
        with patch("autosar_pdf2txt.parser.pdf_reader.HAS_PDFPLUMBER", True):
            reader = PDFReader(backend="pdfplumber")
            assert reader.backend == "pdfplumber"

    def test_init_pdfplumber_backend_unavailable(self) -> None:
        """Test specifying pdfplumber backend (unavailable)."""
        with patch("autosar_pdf2txt.parser.pdf_reader.HAS_PDFPLUMBER", False):
            with pytest.raises(ValueError, match="pdfplumber backend not available"):
                PDFReader(backend="pdfplumber")

    def test_init_fitz_backend_available(self) -> None:
        """Test specifying fitz backend (available)."""
        with patch("autosar_pdf2txt.parser.pdf_reader.HAS_FITZ", True):
            reader = PDFReader(backend="fitz")
            assert reader.backend == "fitz"

    def test_init_fitz_backend_unavailable(self) -> None:
        """Test specifying fitz backend (unavailable)."""
        with patch("autosar_pdf2txt.parser.pdf_reader.HAS_FITZ", False):
            with pytest.raises(ValueError, match="fitz backend not available"):
                PDFReader(backend="fitz")

    def test_init_pypdf_backend_available(self) -> None:
        """Test specifying pypdf backend (available)."""
        with patch("autosar_pdf2txt.parser.pdf_reader.HAS_PYPDF", True):
            reader = PDFReader(backend="pypdf")
            assert reader.backend == "pypdf"

    def test_init_pypdf_backend_unavailable(self) -> None:
        """Test specifying pypdf backend (unavailable)."""
        with patch("autosar_pdf2txt.parser.pdf_reader.HAS_PYPDF", False):
            with pytest.raises(ValueError, match="pypdf backend not available"):
                PDFReader(backend="pypdf")

    def test_read_text_with_pdfplumber(self) -> None:
        """Test reading text with pdfplumber."""
        with patch("autosar_pdf2txt.parser.pdf_reader.HAS_PDFPLUMBER", True):
            reader = PDFReader(backend="pdfplumber")

            # Mock pdfplumber.open
            mock_page = Mock()
            mock_page.extract_text.return_value = "Sample text from PDF"

            mock_pdf = Mock()
            mock_pdf.__enter__ = Mock(return_value=mock_pdf)
            mock_pdf.__exit__ = Mock(return_value=False)
            mock_pdf.pages = [mock_page]

            with patch("autosar_pdf2txt.parser.pdf_reader.pdfplumber.open", return_value=mock_pdf):
                text = reader.read_text("test.pdf")
                assert "Sample text from PDF" in text

    def test_read_text_with_pdfplumber_error(self) -> None:
        """Test pdfplumber read error."""
        with patch("autosar_pdf2txt.parser.pdf_reader.HAS_PDFPLUMBER", True):
            reader = PDFReader(backend="pdfplumber")

            with patch("autosar_pdf2txt.parser.pdf_reader.pdfplumber.open", side_effect=Exception("Read error")):
                with pytest.raises(ValueError, match="Error reading PDF with pdfplumber"):
                    reader.read_text("test.pdf")

    def test_read_text_with_pypdf(self, tmp_path) -> None:
        """Test reading text with pypdf."""
        with patch("autosar_pdf2txt.parser.pdf_reader.HAS_PYPDF", True):
            reader = PDFReader(backend="pypdf")

            # Mock pypdf.PdfReader
            mock_page = Mock()
            mock_page.extract_text.return_value = "Sample text from pypdf"

            mock_pdf_reader = Mock()
            mock_pdf_reader.pages = [mock_page]

            with patch("pypdf.PdfReader", return_value=mock_pdf_reader):
                with open(tmp_path / "test.pdf", "wb") as f:
                    f.write(b"fake pdf content")

                text = reader.read_text(str(tmp_path / "test.pdf"))
                assert "Sample text from pypdf" in text

    def test_read_text_with_pypdf_file_not_found(self) -> None:
        """Test pypdf file not found."""
        with patch("autosar_pdf2txt.parser.pdf_reader.HAS_PYPDF", True):
            reader = PDFReader(backend="pypdf")

            with pytest.raises(FileNotFoundError):
                reader.read_text("/nonexistent/file.pdf")

    def test_read_text_with_pypdf_error(self, tmp_path) -> None:
        """Test pypdf read error."""
        with patch("autosar_pdf2txt.parser.pdf_reader.HAS_PYPDF", True):
            reader = PDFReader(backend="pypdf")

            with patch("builtins.open", side_effect=Exception("Read error")):
                with pytest.raises(ValueError, match="Error reading PDF with pypdf"):
                    reader.read_text(str(tmp_path / "test.pdf"))

    def test_read_text_with_fitz(self) -> None:
        """Test reading text with fitz."""
        # Mock fitz module and open
        mock_page = Mock()
        mock_page.get_text.return_value = "Sample text from fitz"

        mock_doc = Mock()
        mock_doc.__iter__ = Mock(return_value=iter([mock_page]))
        mock_doc.pages = [mock_page]
        mock_doc.close = Mock()

        mock_fitz = Mock()
        mock_fitz.open.return_value = mock_doc

        with patch("autosar_pdf2txt.parser.pdf_reader.HAS_FITZ", True):
            with patch.dict("sys.modules", {"fitz": mock_fitz}):
                import importlib
                import autosar_pdf2txt.parser.pdf_reader as pr
                importlib.reload(pr)

                reader = pr.PDFReader(backend="fitz")
                text = reader._read_with_fitz("test.pdf")
                assert "Sample text from fitz" in text

                importlib.reload(pr)

    def test_read_text_with_fitz_error(self) -> None:
        """Test fitz read error."""
        mock_fitz = Mock()
        mock_fitz.open.side_effect = Exception("Read error")

        with patch("autosar_pdf2txt.parser.pdf_reader.HAS_FITZ", True):
            with patch.dict("sys.modules", {"fitz": mock_fitz}):
                import importlib
                import autosar_pdf2txt.parser.pdf_reader as pr
                importlib.reload(pr)

                reader = pr.PDFReader(backend="fitz")
                with pytest.raises(ValueError, match="Error reading PDF with fitz"):
                    reader._read_with_fitz("test.pdf")

                importlib.reload(pr)

    def test_read_text_dispatches_to_correct_backend(self) -> None:
        """Test read_text dispatches to correct backend."""
        reader = PDFReader(backend="auto")
        reader.backend = "pdfplumber"

        with patch.object(reader, "_read_with_pdfplumber", return_value="pdfplumber text"):
            text = reader.read_text("test.pdf")
            assert text == "pdfplumber text"

    def test_read_text_unknown_backend(self) -> None:
        """Test read_text with unknown backend."""
        reader = PDFReader(backend="auto")
        reader.backend = "unknown"

        with pytest.raises(ValueError, match="Unknown backend"):
            reader.read_text("test.pdf")


class TestReadPDFFunctional:
    """Tests for read_pdf functional interface."""

    def test_read_pdf_functional(self) -> None:
        """Test functional interface."""
        with patch("autosar_pdf2txt.parser.pdf_reader.PDFReader") as mock_reader_class:
            mock_reader = Mock()
            mock_reader.read_text.return_value = "extracted text"
            mock_reader_class.return_value = mock_reader

            text = read_pdf("test.pdf", backend="pdfplumber")
            assert text == "extracted text"
            mock_reader_class.assert_called_once_with(backend="pdfplumber")
            mock_reader.read_text.assert_called_once_with("test.pdf")
