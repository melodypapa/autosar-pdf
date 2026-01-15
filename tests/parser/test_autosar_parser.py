"""Tests for AUTOSAR parser integration.

Test coverage for autosar_parser.py targeting 100%.
"""

from unittest.mock import Mock, patch

from autosar_pdf2txt.models import AutosarPackage
from autosar_pdf2txt.parser.autosar_parser import (
    AutosarParser,
    extract_pdf_text,
    parse_autosar_pdf,
)


class TestAutosarParser:
    """Tests for AutosarParser class."""

    def test_init_default_backend(self) -> None:
        """Test initialization with default backend."""
        with patch("autosar_pdf2txt.parser.autosar_parser.PDFReader"):
            parser = AutosarParser()
            assert parser.pdf_reader is not None

    def test_init_custom_backend(self) -> None:
        """Test initialization with custom backend."""
        with patch("autosar_pdf2txt.parser.autosar_parser.PDFReader"):
            parser = AutosarParser(pdf_backend="pdfplumber")
            assert parser.pdf_reader is not None

    def test_parse_pdf_success(self, tmp_path) -> None:
        """Test successful PDF parsing."""
        # Create a mock parser
        parser = AutosarParser()

        # Mock the pdf_reader to return hierarchy text
        mock_reader = Mock()
        hierarchy_text = """* TestPackage
    * TestClass"""
        mock_reader.read_text.return_value = hierarchy_text
        parser.pdf_reader = mock_reader

        # Parse
        packages = parser.parse_pdf("test.pdf")

        # Verify
        assert len(packages) == 1
        assert packages[0].name == "TestPackage"
        assert len(packages[0].classes) == 1
        assert packages[0].classes[0].name == "TestClass"
        mock_reader.read_text.assert_called_once_with("test.pdf")

    def test_parse_pdf_with_nested_structure(self, tmp_path) -> None:
        """Test parsing PDF with nested structure."""
        parser = AutosarParser()

        mock_reader = Mock()
        hierarchy_text = """* RootPackage
  * SubPackage
      * ConcreteClass
      * AbstractClass (abstract)"""
        mock_reader.read_text.return_value = hierarchy_text
        parser.pdf_reader = mock_reader

        packages = parser.parse_pdf("test.pdf")

        assert len(packages) == 1
        root = packages[0]
        assert root.name == "RootPackage"
        assert len(root.subpackages) == 1
        assert root.subpackages[0].name == "SubPackage"
        assert len(root.subpackages[0].classes) == 2
        assert root.subpackages[0].classes[0].is_abstract is False
        assert root.subpackages[0].classes[1].is_abstract is True

    def test_parse_pdf_empty_result(self, tmp_path) -> None:
        """Test parsing PDF with no hierarchy."""
        parser = AutosarParser()

        mock_reader = Mock()
        mock_reader.read_text.return_value = "No hierarchy here\nJust plain text"
        parser.pdf_reader = mock_reader

        packages = parser.parse_pdf("test.pdf")

        assert len(packages) == 0

    def test_parse_pdf_to_text(self, tmp_path) -> None:
        """Test parse_pdf_to_text method."""
        parser = AutosarParser()

        mock_reader = Mock()
        mock_reader.read_text.return_value = "Extracted text from PDF"
        parser.pdf_reader = mock_reader

        text = parser.parse_pdf_to_text("test.pdf")

        assert text == "Extracted text from PDF"
        mock_reader.read_text.assert_called_once_with("test.pdf")


class TestFunctionalInterface:
    """Tests for functional interfaces."""

    def test_parse_autosar_pdf(self, tmp_path) -> None:
        """Test parse_autosar_pdf function."""
        with patch("autosar_pdf2txt.parser.autosar_parser.AutosarParser") as mock_parser_class:
            mock_parser = Mock()
            mock_packages = [AutosarPackage(name="TestPackage")]
            mock_parser.parse_pdf.return_value = mock_packages
            mock_parser_class.return_value = mock_parser

            packages = parse_autosar_pdf("test.pdf", pdf_backend="pdfplumber")

            assert packages == mock_packages
            mock_parser_class.assert_called_once_with(pdf_backend="pdfplumber")
            mock_parser.parse_pdf.assert_called_once_with("test.pdf")

    def test_extract_pdf_text(self, tmp_path) -> None:
        """Test extract_pdf_text function."""
        with patch("autosar_pdf2txt.parser.autosar_parser.PDFReader") as mock_reader_class:
            mock_reader = Mock()
            mock_reader.read_text.return_value = "PDF text content"
            mock_reader_class.return_value = mock_reader

            text = extract_pdf_text("test.pdf", pdf_backend="fitz")

            assert text == "PDF text content"
            mock_reader_class.assert_called_once_with(backend="fitz")
            mock_reader.read_text.assert_called_once_with("test.pdf")

    def test_extract_pdf_text_default_backend(self, tmp_path) -> None:
        """Test extract_pdf_text with default backend."""
        with patch("autosar_pdf2txt.parser.autosar_parser.PDFReader") as mock_reader_class:
            mock_reader = Mock()
            mock_reader.read_text.return_value = "PDF text"
            mock_reader_class.return_value = mock_reader

            text = extract_pdf_text("test.pdf")

            assert text == "PDF text"
            mock_reader_class.assert_called_once_with(backend="auto")


class TestIntegration:
    """Integration tests."""

    def test_full_workflow(self, tmp_path) -> None:
        """Test complete workflow."""
        # Create a test file with hierarchy
        hierarchy_text = """* AUTOSARTemplates
  * BswModuleTemplate
    * BswBehavior
        * BswInternalBehavior
        * ExecutableEntity (abstract)"""

        parser = AutosarParser()

        with patch.object(parser.pdf_reader, "read_text", return_value=hierarchy_text):
            packages = parser.parse_pdf("test.pdf")

            assert len(packages) == 1
            root = packages[0]
            assert root.name == "AUTOSARTemplates"
            assert len(root.subpackages) == 1

            bsw = root.subpackages[0]
            assert bsw.name == "BswModuleTemplate"
            assert len(bsw.subpackages) == 1

            behavior = bsw.subpackages[0]
            assert behavior.name == "BswBehavior"
            assert len(behavior.classes) == 2
            assert behavior.classes[0].name == "BswInternalBehavior"
            assert behavior.classes[1].name == "ExecutableEntity"
            assert behavior.classes[1].is_abstract is True
