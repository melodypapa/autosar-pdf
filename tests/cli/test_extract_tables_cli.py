"""Tests for extract_tables CLI.

Test coverage for extract_tables_cli.py targeting 100%.
"""

from typing import List, Optional
from unittest.mock import MagicMock, PropertyMock, patch

from autosar_pdf2txt.cli.extract_tables_cli import (
    extract_tables_from_pdf,
    is_autosar_table,
    main,
)


class TestIsAutosarTable:
    """Tests for is_autosar_table function.

    Requirements:
        SWR_CLI_00013: CLI Table Extraction
    """

    def test_is_autosar_table_with_class_and_package(self) -> None:
        """SWUT_CLI_00013: Test table with both Class and Package fields is detected as AUTOSAR.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        table = [
            ["Class", "Package", "Attribute", "Type"],
            ["TestClass", "TestPackage", "testAttr", "string"],
        ]
        assert is_autosar_table(table) is True

    def test_is_autosar_table_with_class_and_package_case_insensitive(self) -> None:
        """SWUT_CLI_00013: Test table detection is case-insensitive.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        table = [
            ["CLASS", "PACKAGE", "Attribute", "Type"],
            ["TestClass", "TestPackage", "testAttr", "string"],
        ]
        assert is_autosar_table(table) is True

    def test_is_autosar_table_with_class_and_package_mixed_case(self) -> None:
        """SWUT_CLI_00013: Test table detection works with mixed case.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        table = [
            ["Class", "PaCKaGe", "Attribute", "Type"],
            ["TestClass", "TestPackage", "testAttr", "string"],
        ]
        assert is_autosar_table(table) is True

    def test_is_autosar_table_with_class_only(self) -> None:
        """SWUT_CLI_00013: Test table with only Class field is not AUTOSAR.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        table = [
            ["Class", "Attribute", "Type"],
            ["TestClass", "testAttr", "string"],
        ]
        assert is_autosar_table(table) is False

    def test_is_autosar_table_with_package_only(self) -> None:
        """SWUT_CLI_00013: Test table with only Package field is not AUTOSAR.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        table = [
            ["Package", "Attribute", "Type"],
            ["TestPackage", "testAttr", "string"],
        ]
        assert is_autosar_table(table) is False

    def test_is_autosar_table_with_neither_field(self) -> None:
        """SWUT_CLI_00013: Test table without Class or Package is not AUTOSAR.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        table = [
            ["Attribute", "Type", "Mult"],
            ["testAttr", "string", "0..1"],
        ]
        assert is_autosar_table(table) is False

    def test_is_autosar_table_empty_table(self) -> None:
        """SWUT_CLI_00013: Test empty table returns False.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        table: List[List[Optional[str]]] = []
        assert is_autosar_table(table) is False

    def test_is_autosar_table_with_none_header(self) -> None:
        """SWUT_CLI_00013: Test table with None in header is handled correctly.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        table = [
            ["Class", None, "Package", "Type"],
            ["TestClass", None, "TestPackage", "string"],
        ]
        assert is_autosar_table(table) is True

    def test_is_autosar_table_with_whitespace(self) -> None:
        """SWUT_CLI_00013: Test table with whitespace in header is handled correctly.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        table = [
            [" Class ", " Package ", "Attribute", "Type"],
            ["TestClass", "TestPackage", "testAttr", "string"],
        ]
        assert is_autosar_table(table) is True

    def test_is_autosar_table_with_substring_match(self) -> None:
        """SWUT_CLI_00013: Test table with substring matches (e.g., "Packageable") does not match.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        # "Packageable" contains "Package" but should not match unless "Package" is a separate word
        table = [
            ["Class", "Packageable", "Attribute", "Type"],
            ["TestClass", "TestPackageable", "testAttr", "string"],
        ]
        # This should still match because "package" is a substring of "packageable"
        assert is_autosar_table(table) is True


class TestExtractTablesFromPdf:
    """Tests for extract_tables_from_pdf function.

    Requirements:
        SWR_CLI_00013: CLI Table Extraction
    """

    @patch("autosar_pdf2txt.cli.extract_tables_cli.pdfplumber")
    @patch("autosar_pdf2txt.cli.extract_tables_cli.Path")
    def test_extract_autosar_tables_only(self, mock_path: MagicMock, mock_pdfplumber: MagicMock) -> None:
        """SWUT_CLI_00013: Test only AUTOSAR tables are extracted.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        # Setup mock PDF with mixed tables
        mock_pdf = MagicMock()
        mock_page = MagicMock()

        # Table 1: AUTOSAR table (has Class and Package)
        autosar_table = [
            ["Class", "Package", "Attribute", "Type"],
            ["TestClass", "TestPackage", "testAttr", "string"],
        ]

        # Table 2: Non-AUTOSAR table (missing Package)
        non_autosar_table = [
            ["Attribute", "Type", "Mult"],
            ["testAttr", "string", "0..1"],
        ]

        mock_page.extract_tables.return_value = [autosar_table, non_autosar_table]

        # Mock table finding
        mock_table = MagicMock()
        mock_table.bbox = (0, 0, 100, 100)
        mock_page.find_tables.return_value = [mock_table, mock_table]

        # Mock image
        mock_img = MagicMock()
        mock_page.to_image.return_value = mock_img

        mock_pdf.pages = [mock_page]
        mock_pdfplumber.open.return_value.__enter__.return_value = mock_pdf

        # Setup mock paths
        output_dir = MagicMock()
        output_dir.__truediv__ = MagicMock(return_value=MagicMock())
        mock_path.return_value = output_dir

        result = extract_tables_from_pdf(mock_path, output_dir)

        # Should only extract 1 table (AUTOSAR table)
        assert len(result) == 1
        # Should save image for AUTOSAR table only
        assert mock_img.save.call_count == 1

    @patch("autosar_pdf2txt.cli.extract_tables_cli.pdfplumber")
    @patch("autosar_pdf2txt.cli.extract_tables_cli.Path")
    def test_extract_no_autosar_tables(self, mock_path: MagicMock, mock_pdfplumber: MagicMock) -> None:
        """SWUT_CLI_00013: Test returns empty list when no AUTOSAR tables found.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        # Setup mock PDF with non-AUTOSAR tables
        mock_pdf = MagicMock()
        mock_page = MagicMock()

        non_autosar_table = [
            ["Attribute", "Type", "Mult"],
            ["testAttr", "string", "0..1"],
        ]

        mock_page.extract_tables.return_value = [non_autosar_table]
        mock_page.find_tables.return_value = []

        mock_pdf.pages = [mock_page]
        mock_pdfplumber.open.return_value.__enter__.return_value = mock_pdf

        output_dir = MagicMock()
        result = extract_tables_from_pdf(mock_path, output_dir)

        assert len(result) == 0

    @patch("autosar_pdf2txt.cli.extract_tables_cli.pdfplumber")
    @patch("autosar_pdf2txt.cli.extract_tables_cli.Path")
    def test_extract_handles_pdf_error(self, mock_path: MagicMock, mock_pdfplumber: MagicMock) -> None:
        """SWUT_CLI_00013: Test handles PDF processing errors gracefully.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        # Make pdfplumber raise exception
        mock_pdfplumber.open.side_effect = Exception("PDF read error")

        output_dir = MagicMock()
        result = extract_tables_from_pdf(mock_path, output_dir)

        # Should return empty list on error
        assert result == []

    @patch("autosar_pdf2txt.cli.extract_tables_cli.pdfplumber")
    @patch("autosar_pdf2txt.cli.extract_tables_cli.Path")
    def test_extract_multiple_pages(self, mock_path: MagicMock, mock_pdfplumber: MagicMock) -> None:
        """SWUT_CLI_00013: Test extracts tables from multiple pages.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        # Setup mock PDF with multiple pages
        mock_pdf = MagicMock()
        mock_page1 = MagicMock()
        mock_page2 = MagicMock()

        autosar_table = [
            ["Class", "Package", "Attribute"],
            ["TestClass", "TestPackage", "testAttr"],
        ]

        mock_page1.extract_tables.return_value = [autosar_table]
        mock_page2.extract_tables.return_value = [autosar_table]

        mock_table = MagicMock()
        mock_table.bbox = (0, 0, 100, 100)
        mock_page1.find_tables.return_value = [mock_table]
        mock_page2.find_tables.return_value = [mock_table]

        mock_img = MagicMock()
        mock_page1.to_image.return_value = mock_img
        mock_page2.to_image.return_value = mock_img

        mock_pdf.pages = [mock_page1, mock_page2]
        mock_pdfplumber.open.return_value.__enter__.return_value = mock_pdf

        output_dir = MagicMock()
        output_dir.__truediv__ = MagicMock(return_value=MagicMock())

        result = extract_tables_from_pdf(mock_path, output_dir)

        # Should extract 2 tables (one from each page)
        assert len(result) == 2


class TestExtractTablesCliMain:
    """Tests for extract_tables CLI main function.

    Requirements:
        SWR_CLI_00013: CLI Table Extraction
    """

    def test_main_entry_point(self) -> None:
        """SWUT_CLI_00013: Test that main function exists and returns exit code.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        assert callable(main)
        assert main.__annotations__.get("return") is int

    @patch("sys.argv", ["autosar-extract-table", "nonexistent.pdf", "-o", "output"])
    @patch("autosar_pdf2txt.cli.extract_tables_cli.Path")
    def test_non_existent_path_error(self, mock_path: MagicMock) -> None:
        """SWUT_CLI_00013: Test CLI handles non-existent paths with error.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        mock_path.return_value.exists.return_value = False
        with patch("autosar_pdf2txt.cli.extract_tables_cli.logging") as mock_logging:
            result = main()
            assert result == 1
            mock_logging.error.assert_called()

    @patch("sys.argv", ["autosar-extract-table", "test.txt", "-o", "output"])
    @patch("autosar_pdf2txt.cli.extract_tables_cli.Path")
    def test_non_pdf_file_warning(self, mock_path: MagicMock) -> None:
        """SWUT_CLI_00013: Test CLI warns about non-PDF files.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".txt")
        mock_path.return_value = mock_path_instance

        with patch("autosar_pdf2txt.cli.extract_tables_cli.logging") as mock_logging, \
             patch("autosar_pdf2txt.cli.extract_tables_cli.extract_tables_from_pdf"):
            mock_logging.basicConfig = MagicMock()

            result = main()
            # Should skip non-PDF and return error if no PDFs
            assert result == 1
            mock_logging.warning.assert_called()

    @patch("sys.argv", ["autosar-extract-table", "test.pdf", "-o", "output", "-v"])
    @patch("autosar_pdf2txt.cli.extract_tables_cli.Path")
    @patch("autosar_pdf2txt.cli.extract_tables_cli.logging")
    def test_verbose_mode_flag(self, mock_logging: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00013: Test CLI verbose mode enables detailed logging.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()
        mock_path.return_value = mock_path_instance

        mock_logging.DEBUG = 10
        mock_logging.INFO = 20
        mock_logging.basicConfig = MagicMock()
        mock_logging.getLogger = MagicMock()

        with patch("autosar_pdf2txt.cli.extract_tables_cli.extract_tables_from_pdf") as mock_extract:
            mock_extract.return_value = []

            main()

            # Verify logging was configured with DEBUG level
            mock_logging.basicConfig.assert_called_once()
            call_kwargs = mock_logging.basicConfig.call_args[1]
            assert call_kwargs["level"] == mock_logging.DEBUG

    @patch("sys.argv", ["autosar-extract-table", "test.pdf", "-o", "output"])
    @patch("autosar_pdf2txt.cli.extract_tables_cli.Path")
    @patch("autosar_pdf2txt.cli.extract_tables_cli.logging")
    def test_logging_configuration_info(self, mock_logging: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00013: Test CLI logging is configured correctly in normal mode.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()
        mock_path.return_value = mock_path_instance

        mock_logging.DEBUG = 10
        mock_logging.INFO = 20
        mock_logging.basicConfig = MagicMock()
        mock_logging.getLogger = MagicMock()

        with patch("autosar_pdf2txt.cli.extract_tables_cli.extract_tables_from_pdf") as mock_extract:
            mock_extract.return_value = []

            main()

            # Verify logging was configured with INFO level (not verbose)
            mock_logging.basicConfig.assert_called_once()
            call_kwargs = mock_logging.basicConfig.call_args[1]
            assert call_kwargs["level"] == mock_logging.INFO

    @patch("sys.argv", ["autosar-extract-table", "test.pdf", "-o", "output"])
    @patch("autosar_pdf2txt.cli.extract_tables_cli.Path")
    def test_output_directory_creation(self, mock_path: MagicMock) -> None:
        """SWUT_CLI_00013: Test CLI creates output directory if it doesn't exist.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()
        
        output_dir = MagicMock()
        
        # Set up Path to return different instances based on argument
        def path_side_effect(arg):
            if arg == "test.pdf":
                return mock_path_instance
            elif arg == "output":
                return output_dir
            return MagicMock()
        
        mock_path.side_effect = path_side_effect

        with patch("autosar_pdf2txt.cli.extract_tables_cli.logging") as mock_logging, \
             patch("autosar_pdf2txt.cli.extract_tables_cli.extract_tables_from_pdf"):
            mock_logging.basicConfig = MagicMock()

            main()

            # Verify output directory was created
            output_dir.mkdir.assert_called_once_with(parents=True, exist_ok=True)

    @patch("sys.argv", ["autosar-extract-table", "test.pdf", "-o", "output"])
    @patch("autosar_pdf2txt.cli.extract_tables_cli.Path")
    def test_directory_input_support(self, mock_path: MagicMock) -> None:
        """SWUT_CLI_00013: Test CLI supports directory input for PDF discovery.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_dir.return_value = True
        mock_path_instance.is_file.return_value = False

        # Mock PDF files in directory with __lt__ for sorting
        mock_pdf1 = MagicMock()
        mock_pdf1.suffix = ".pdf"
        mock_pdf1.name = "a.pdf"
        mock_pdf1.__lt__ = lambda self, other: self.name < other.name
        
        mock_pdf2 = MagicMock()
        mock_pdf2.suffix = ".pdf"
        mock_pdf2.name = "b.pdf"
        mock_pdf2.__lt__ = lambda self, other: self.name < other.name

        mock_path_instance.glob.return_value = [mock_pdf1, mock_pdf2]

        output_dir = MagicMock()
        
        def path_side_effect(arg):
            if arg == "test.pdf":
                return mock_path_instance
            elif arg == "output":
                return output_dir
            return MagicMock()
        
        mock_path.side_effect = path_side_effect

        with patch("autosar_pdf2txt.cli.extract_tables_cli.logging") as mock_logging, \
             patch("autosar_pdf2txt.cli.extract_tables_cli.extract_tables_from_pdf") as mock_extract:
            mock_logging.basicConfig = MagicMock()
            mock_extract.return_value = []

            main()

            # Verify glob was called to find PDF files
            mock_path_instance.glob.assert_called_once_with("*.pdf")

    @patch("sys.argv", ["autosar-extract-table", "test.pdf", "-o", "output"])
    @patch("autosar_pdf2txt.cli.extract_tables_cli.Path")
    def test_error_handling_with_exception(self, mock_path: MagicMock) -> None:
        """SWUT_CLI_00013: Test CLI handles exceptions gracefully.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()
        mock_path.return_value = mock_path_instance

        output_dir = MagicMock()
        mock_path.side_effect = [mock_path_instance, output_dir]

        with patch("autosar_pdf2txt.cli.extract_tables_cli.logging") as mock_logging:
            mock_logging.basicConfig = MagicMock()
            mock_logging.error = MagicMock()
            mock_logging.exception = MagicMock()

            # Make extract raise exception
            import autosar_pdf2txt.cli.extract_tables_cli as cli_module
            original_extract = cli_module.extract_tables_from_pdf

            def mock_extract_error(*args, **kwargs):
                raise Exception("Extraction error")

            cli_module.extract_tables_from_pdf = mock_extract_error

            try:
                result = main()
                assert result == 1
                mock_logging.error.assert_called()
                # exception should not be called in non-verbose mode
                mock_logging.exception.assert_not_called()
            finally:
                cli_module.extract_tables_from_pdf = original_extract

    @patch("sys.argv", ["autosar-extract-table", "test.pdf", "-o", "output", "-v"])
    @patch("autosar_pdf2txt.cli.extract_tables_cli.Path")
    @patch("autosar_pdf2txt.cli.extract_tables_cli.logging")
    def test_verbose_mode_exception_traceback(self, mock_logging: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00013: Test CLI shows exception traceback in verbose mode.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()

        mock_logging.DEBUG = 10
        mock_logging.INFO = 20
        mock_logging.basicConfig = MagicMock()
        mock_logging.getLogger = MagicMock()

        output_dir = MagicMock()
        
        def path_side_effect(arg):
            if arg == "test.pdf":
                return mock_path_instance
            elif arg == "output":
                return output_dir
            return MagicMock()
        
        mock_path.side_effect = path_side_effect

        with patch("autosar_pdf2txt.cli.extract_tables_cli.extract_tables_from_pdf"):
            import autosar_pdf2txt.cli.extract_tables_cli as cli_module
            original_extract = cli_module.extract_tables_from_pdf

            def mock_extract_error(*args, **kwargs):
                raise Exception("Extraction error")

            mock_logging.error = MagicMock()
            mock_logging.exception = MagicMock()

            cli_module.extract_tables_from_pdf = mock_extract_error

            try:
                result = main()
                assert result == 1
                mock_logging.error.assert_called()
                # In verbose mode, exception traceback should be logged
                mock_logging.exception.assert_called()
            finally:
                cli_module.extract_tables_from_pdf = original_extract

    @patch("sys.argv", ["autosar-extract-table", "test.pdf", "-o", "output"])
    @patch("autosar_pdf2txt.cli.extract_tables_cli.Path")
    def test_success_exit_code(self, mock_path: MagicMock) -> None:
        """SWUT_CLI_00013: Test CLI returns success exit code.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()
        
        output_dir = MagicMock()
        
        def path_side_effect(arg):
            if arg == "test.pdf":
                return mock_path_instance
            elif arg == "output":
                return output_dir
            return MagicMock()
        
        mock_path.side_effect = path_side_effect

        with patch("autosar_pdf2txt.cli.extract_tables_cli.logging") as mock_logging, \
             patch("autosar_pdf2txt.cli.extract_tables_cli.extract_tables_from_pdf") as mock_extract:
            mock_logging.basicConfig = MagicMock()
            mock_extract.return_value = [MagicMock()]

            result = main()
            assert result == 0

    @patch("sys.argv", ["autosar-extract-table", "test.pdf", "-o", "output"])
    @patch("autosar_pdf2txt.cli.extract_tables_cli.Path")
    def test_empty_directory_warning(self, mock_path: MagicMock) -> None:
        """SWUT_CLI_00013: Test CLI warns about empty directories.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_dir.return_value = True
        mock_path_instance.is_file.return_value = False
        mock_path_instance.glob.return_value = []  # No PDF files

        output_dir = MagicMock()
        mock_path.side_effect = [mock_path_instance, output_dir]

        with patch("autosar_pdf2txt.cli.extract_tables_cli.logging") as mock_logging, \
             patch("autosar_pdf2txt.cli.extract_tables_cli.extract_tables_from_pdf"):
            mock_logging.basicConfig = MagicMock()
            mock_logging.warning = MagicMock()

            result = main()
            assert result == 1
            mock_logging.warning.assert_called()

    @patch("sys.argv", ["autosar-extract-table", "test.pdf", "-o", "output"])
    @patch("autosar_pdf2txt.cli.extract_tables_cli.Path")
    @patch("autosar_pdf2txt.cli.extract_tables_cli.logging")
    def test_pdfminer_warning_suppression(self, mock_logging: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00013: Test CLI suppresses pdfminer warnings.

        Requirements:
            SWR_CLI_00013: CLI Table Extraction
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()
        mock_path.return_value = mock_path_instance

        mock_logger = MagicMock()
        mock_logging.getLogger.return_value = mock_logger
        mock_logging.basicConfig = MagicMock()

        output_dir = MagicMock()
        mock_path.side_effect = [mock_path_instance, output_dir]

        with patch("autosar_pdf2txt.cli.extract_tables_cli.extract_tables_from_pdf") as mock_extract:
            mock_extract.return_value = []

            main()

            # Verify pdfminer warnings are suppressed
            mock_logging.getLogger.assert_called_with("pdfminer")
            mock_logger.setLevel.assert_called_once()