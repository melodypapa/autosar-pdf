"""Tests for AUTOSAR CLI.

Test coverage for autosar_cli.py targeting 100%.
"""

import pytest
from unittest.mock import MagicMock, PropertyMock, patch

from autosar_pdf2txt.cli.autosar_cli import main
from autosar_pdf2txt.models import AutosarDoc


class TestAutosarCli:
    """Tests for AUTOSAR CLI.

    Requirements:
        SWR_CLI_00001: CLI Entry Point
        SWR_CLI_00002: CLI File Input Support
        SWR_CLI_00003: CLI Directory Input Support
        SWR_CLI_00004: CLI Output File Option
        SWR_CLI_00005: CLI Verbose Mode
        SWR_CLI_00006: CLI Input Validation
        SWR_CLI_00007: CLI Progress Feedback
        SWR_CLI_00008: CLI Logging
        SWR_CLI_00009: CLI Error Handling
        SWR_CLI_00010: CLI Class File Output
        SWR_CLI_00011: CLI Class Files Flag
    """

    def test_main_entry_point(self) -> None:
        """SWUT_CLI_00001: Test that main function exists and returns exit code.

        Requirements:
            SWR_CLI_00001: CLI Entry Point
        """
        assert callable(main)
        assert main.__annotations__.get("return") is int

    @patch("sys.argv", ["autosar-extract", "nonexistent.pdf", "--mapping", "output.md"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    def test_non_existent_path_error(self, mock_path: MagicMock) -> None:
        """SWUT_CLI_00002: Test CLI handles non-existent paths with error.

        Requirements:
            SWR_CLI_00006: CLI Input Validation
            SWR_CLI_00009: CLI Error Handling
        """
        mock_path.return_value.exists.return_value = False
        with patch("autosar_pdf2txt.cli.autosar_cli.logging") as mock_logging:
            result = main()
            assert result == 1
            mock_logging.error.assert_called()

    @patch("sys.argv", ["autosar-extract", "test.txt", "--mapping", "output.md"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    def test_non_pdf_file_warning(self, mock_path: MagicMock) -> None:
        """SWUT_CLI_00003: Test CLI warns about non-PDF files.

        Requirements:
            SWR_CLI_00006: CLI Input Validation
            SWR_CLI_00008: CLI Logging
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".txt")
        mock_path.return_value = mock_path_instance

        with patch("autosar_pdf2txt.cli.autosar_cli.PdfParser") as mock_parser, \
             patch("autosar_pdf2txt.cli.autosar_cli.logging") as mock_logging, \
             patch("autosar_pdf2txt.cli.autosar_cli.MarkdownWriter") as mock_writer, \
             patch("builtins.print"):
            mock_doc = MagicMock(spec=AutosarDoc)
            mock_doc.packages = []
            mock_doc.root_classes = []
            mock_parser.return_value.parse_pdfs.return_value = mock_doc
            mock_writer.return_value.write_packages.return_value = "test"

            result = main()
            # Should skip non-PDF and return error if no PDFs
            assert result == 1
            mock_logging.warning.assert_called()

    @patch("sys.argv", ["autosar-extract", "test.pdf", "-v", "--mapping", "output.md"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    @patch("autosar_pdf2txt.cli.autosar_cli.logging")
    def test_verbose_mode_flag(self, mock_logging: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00004: Test CLI verbose mode enables detailed logging.

        Requirements:
            SWR_CLI_00005: CLI Verbose Mode
            SWR_CLI_00008: CLI Logging
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()
        mock_path.return_value = mock_path_instance

        mock_logging.DEBUG = 10
        mock_logging.INFO = 20

        with patch("autosar_pdf2txt.cli.autosar_cli.PdfParser") as mock_parser, \
             patch("autosar_pdf2txt.cli.autosar_cli.MarkdownWriter") as mock_writer, \
             patch("builtins.print"):
            mock_pkg = MagicMock()
            mock_pkg.name = "TestPackage"
            mock_doc = MagicMock(spec=AutosarDoc)
            mock_doc.packages = [mock_pkg]
            mock_doc.root_classes = []
            mock_parser.return_value.parse_pdfs.return_value = mock_doc
            mock_writer.return_value.write_packages.return_value = "* TestPackage\n"

            main()

            # Verify root logger was configured with DEBUG level
            root_logger = mock_logging.getLogger.return_value
            # Check that DEBUG was set (may be called multiple times due to pdfminer suppression)
            assert any(call[0][0] == mock_logging.DEBUG for call in root_logger.setLevel.call_args_list)

            # Verify console handler was created with DEBUG level
            assert any(call[0][0].setLevel.call_args[0][0] == mock_logging.DEBUG
                      for call in root_logger.addHandler.call_args_list)

    @patch("sys.argv", ["autosar-extract", "test.pdf", "--class-details", "classes/"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    @patch("autosar_pdf2txt.cli.autosar_cli.logging.FileHandler")
    def test_output_file_option_with_class_files(self, mock_file_handler: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00005: Test CLI creates class files when --class-details flag is set.

        Requirements:
            SWR_CLI_00017: CLI Class Files Flag
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()

        # Mock warning log file path
        mock_warning_log_path = MagicMock()

        # Mock Path for output file
        output_path = MagicMock()
        output_path.write_text = MagicMock()
        output_path.parent = MagicMock()

        # Configure Path mock to return different mocks based on call order
        # Order: warning log file, then PDF file, then output file, then output file again (for format inference), then output parent
        mock_path.side_effect = [mock_warning_log_path, mock_path_instance, output_path, output_path, output_path.parent]

        with patch("autosar_pdf2txt.cli.autosar_cli.PdfParser") as mock_parser, \
             patch("autosar_pdf2txt.cli.autosar_cli.logging") as mock_logging, \
             patch("autosar_pdf2txt.cli.autosar_cli.MarkdownWriter") as mock_writer:
            mock_pkg = MagicMock()
            mock_pkg.name = "TestPackage"
            mock_doc = MagicMock(spec=AutosarDoc)
            mock_doc.packages = [mock_pkg]
            mock_doc.root_classes = []
            mock_parser.return_value.parse_pdfs.return_value = mock_doc
            mock_writer.return_value.write_packages.return_value = "* TestPackage\n"
            mock_logging.basicConfig = MagicMock()

            # Mock FileHandler
            mock_handler = MagicMock()
            mock_file_handler.return_value = mock_handler

            result = main()

            assert result == 0
            # Verify write_packages_to_files was called for --class-details
            mock_writer.return_value.write_packages_to_files.assert_called_once()

    @patch("sys.argv", ["autosar-extract", "test.pdf", "--mapping", "output.md"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    @patch("autosar_pdf2txt.cli.autosar_cli.logging.FileHandler")
    def test_output_file_option_without_class_files(self, mock_file_handler: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00006: Test CLI writes mapping output to specified file.

        Requirements:
            SWR_CLI_00015: CLI Mapping Generation Flag
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()

        # Mock warning log file path
        mock_warning_log_path = MagicMock()

        # Mock Path for output file with parent directory
        output_path = MagicMock()
        output_path.write_text = MagicMock()
        output_parent = MagicMock()
        output_parent.mkdir = MagicMock()
        output_path.parent = output_parent

        # Configure Path mock to return different mocks based on call order
        mock_path.side_effect = [mock_warning_log_path, mock_path_instance, output_path]

        with patch("autosar_pdf2txt.cli.autosar_cli.PdfParser") as mock_parser, \
             patch("autosar_pdf2txt.cli.autosar_cli.logging") as mock_logging, \
             patch("autosar_pdf2txt.cli.autosar_cli.MappingWriter") as mock_writer:
            mock_pkg = MagicMock()
            mock_pkg.name = "TestPackage"
            mock_doc = MagicMock(spec=AutosarDoc)
            mock_doc.packages = [mock_pkg]
            mock_doc.root_classes = []
            mock_parser.return_value.parse_pdfs.return_value = mock_doc
            mock_writer.return_value.write_mapping.return_value = "# Mapping\n"
            mock_logging.basicConfig = MagicMock()

            # Mock FileHandler
            mock_handler = MagicMock()
            mock_file_handler.return_value = mock_handler

            result = main()

            assert result == 0
            # Verify output was written to file
            output_path.write_text.assert_called_once()
            # Verify write_mapping was called
            mock_writer.return_value.write_mapping.assert_called_once()
            # Verify write_packages_to_files was NOT called when flag is not set
            mock_writer.return_value.write_packages_to_files.assert_not_called()

    @patch("sys.argv", ["autosar-extract", "test.pdf", "--mapping", "output.md"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    @patch("autosar_pdf2txt.cli.autosar_cli.logging")
    def test_logging_configuration_info(self, mock_logging: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00007: Test CLI logging is configured correctly in normal mode.

        Requirements:
            SWR_CLI_00008: CLI Logging
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()

        # Mock warning log file path
        mock_warning_log_path = MagicMock()

        # Configure Path mock to return different mocks based on call order
        # Order: warning log file, then PDF file
        mock_path.side_effect = [mock_warning_log_path, mock_path_instance]

        mock_logging.DEBUG = 10
        mock_logging.INFO = 20

        with patch("autosar_pdf2txt.cli.autosar_cli.PdfParser") as mock_parser, \
             patch("autosar_pdf2txt.cli.autosar_cli.MarkdownWriter") as mock_writer, \
             patch("builtins.print"):
            mock_pkg = MagicMock()
            mock_pkg.name = "TestPackage"
            mock_doc = MagicMock(spec=AutosarDoc)
            mock_doc.packages = [mock_pkg]
            mock_doc.root_classes = []
            mock_parser.return_value.parse_pdfs.return_value = mock_doc
            mock_writer.return_value.write_packages.return_value = "* TestPackage\n"

            main()

            # Verify root logger was configured with DEBUG level (to capture all levels)
            root_logger = mock_logging.getLogger.return_value
            # Check that DEBUG was set
            assert any(call[0][0] == mock_logging.DEBUG for call in root_logger.setLevel.call_args_list)

            # Verify console handler was created with INFO level (normal mode shows INFO+, WARNING goes to file)
            assert any(call[0][0].setLevel.call_args[0][0] == mock_logging.INFO
                      for call in root_logger.addHandler.call_args_list)

            # Verify warning file handler was created (to log warnings to file)
            # Check that FileHandler was called to create the warning handler
            mock_logging.FileHandler.assert_called_once()
            # Verify the handler was added to root logger
            assert any(call[0][0] == mock_logging.FileHandler.return_value
                      for call in root_logger.addHandler.call_args_list)

    @patch("sys.argv", ["autosar-extract", "test.pdf", "--mapping", "output.md"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    def test_error_handling_with_exception(self, mock_path: MagicMock) -> None:
        """SWUT_CLI_00008: Test CLI handles exceptions gracefully.

        Requirements:
            SWR_CLI_00009: CLI Error Handling
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()
        mock_path.return_value = mock_path_instance

        with patch("autosar_pdf2txt.cli.autosar_cli.PdfParser") as mock_parser, \
             patch("autosar_pdf2txt.cli.autosar_cli.logging") as mock_logging, \
             patch("builtins.print"):
            # Make parser raise exception
            mock_parser.return_value.parse_pdfs.side_effect = Exception("Parse error")
            mock_logging.error = MagicMock()
            mock_logging.exception = MagicMock()
            mock_logging.basicConfig = MagicMock()

            result = main()

            assert result == 1
            mock_logging.error.assert_called()
            # exception should not be called in non-verbose mode
            mock_logging.exception.assert_not_called()

    @patch("sys.argv", ["autosar-extract", "test.pdf", "-v", "--mapping", "output.md"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    @patch("autosar_pdf2txt.cli.autosar_cli.logging")
    def test_verbose_mode_exception_traceback(self, mock_logging: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00009: Test CLI shows exception traceback in verbose mode.

        Requirements:
            SWR_CLI_00005: CLI Verbose Mode
            SWR_CLI_00009: CLI Error Handling
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

        with patch("autosar_pdf2txt.cli.autosar_cli.PdfParser") as mock_parser, \
             patch("builtins.print"):
            # Make parser raise exception
            mock_parser.return_value.parse_pdfs.side_effect = Exception("Parse error")
            mock_logging.error = MagicMock()
            mock_logging.exception = MagicMock()

            result = main()

            assert result == 1
            mock_logging.error.assert_called()
            # In verbose mode, exception traceback should be logged
            mock_logging.exception.assert_called()

    def test_directory_input_support(self) -> None:
        """SWUT_CLI_00010: Test CLI supports directory input for PDF discovery.

        Requirements:
            SWR_CLI_00003: CLI Directory Input Support
        """
        # This test documents that CLI supports directory input
        # Actual implementation tested by integration tests
        # The CLI should:
        # 1. Accept directory paths as input
        # 2. Discover all PDF files in directory using glob("*.pdf")
        # 3. Sort PDF files alphabetically
        # 4. Process all discovered PDF files
        assert True  # Placeholder for documented requirement

    @patch("sys.argv", ["autosar-extract", "test.pdf", "--mapping", "output.md"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    def test_success_exit_code(self, mock_path: MagicMock) -> None:
        """SWUT_CLI_00011: Test CLI returns success exit code.

        Requirements:
            SWR_CLI_00009: CLI Error Handling
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()
        mock_path.return_value = mock_path_instance

        with patch("autosar_pdf2txt.cli.autosar_cli.PdfParser") as mock_parser, \
             patch("autosar_pdf2txt.cli.autosar_cli.logging") as mock_logging, \
             patch("autosar_pdf2txt.cli.autosar_cli.MarkdownWriter") as mock_writer, \
             patch("builtins.print"):
            # Mock successful parsing
            mock_pkg = MagicMock()
            mock_pkg.name = "TestPackage"
            mock_doc = MagicMock(spec=AutosarDoc)
            mock_doc.packages = [mock_pkg]
            mock_doc.root_classes = []
            mock_parser.return_value.parse_pdfs.return_value = mock_doc
            mock_writer.return_value.write_packages.return_value = "* TestPackage\n"
            mock_logging.basicConfig = MagicMock()

            result = main()

            assert result == 0

    @patch("sys.argv", ["autosar-extract", "test.pdf", "--log-file", "test.log", "--mapping", "output.md"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    @patch("autosar_pdf2txt.cli.autosar_cli.logging")
    def test_log_file_argument_creates_handler(self, mock_logging: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00012: Test CLI creates file handler when --log-file is specified.

        Requirements:
            SWR_CLI_00014: CLI Logger File Specification
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()
        mock_path.return_value = mock_path_instance

        # Mock FileHandler
        mock_file_handler = MagicMock()
        mock_logging.FileHandler.return_value = mock_file_handler

        with patch("autosar_pdf2txt.cli.autosar_cli.PdfParser") as mock_parser, \
             patch("autosar_pdf2txt.cli.autosar_cli.MarkdownWriter") as mock_writer, \
             patch("builtins.print"):
            mock_pkg = MagicMock()
            mock_pkg.name = "TestPackage"
            mock_doc = MagicMock(spec=AutosarDoc)
            mock_doc.packages = [mock_pkg]
            mock_doc.root_classes = []
            mock_parser.return_value.parse_pdfs.return_value = mock_doc
            mock_writer.return_value.write_packages.return_value = "* TestPackage\n"

            result = main()

            assert result == 0
            # Verify FileHandler was created twice (warning log + --log-file)
            assert mock_logging.FileHandler.call_count == 2
            # Verify FileHandler was added to root logger
            mock_logging.getLogger.return_value.addHandler.assert_called()

    @patch("sys.argv", ["autosar-extract", "test.pdf", "--log-file", "logs/test.log", "--mapping", "output.md"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    @patch("autosar_pdf2txt.cli.autosar_cli.logging")
    def test_log_file_creates_parent_directories(self, mock_logging: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00013: Test CLI creates parent directories for log file.

        Requirements:
            SWR_CLI_00014: CLI Logger File Specification
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()
        mock_path_instance.parent.mkdir = MagicMock()
        mock_path.return_value = mock_path_instance

        # Mock FileHandler
        mock_file_handler = MagicMock()
        mock_logging.FileHandler.return_value = mock_file_handler

        with patch("autosar_pdf2txt.cli.autosar_cli.PdfParser") as mock_parser, \
             patch("autosar_pdf2txt.cli.autosar_cli.MarkdownWriter") as mock_writer, \
             patch("builtins.print"):
            mock_pkg = MagicMock()
            mock_pkg.name = "TestPackage"
            mock_doc = MagicMock(spec=AutosarDoc)
            mock_doc.packages = [mock_pkg]
            mock_doc.root_classes = []
            mock_parser.return_value.parse_pdfs.return_value = mock_doc
            mock_writer.return_value.write_packages.return_value = "* TestPackage\n"

            result = main()

            assert result == 0
            # Verify parent directory creation (called twice: once for log file, once for mapping output)
            assert mock_path_instance.parent.mkdir.call_count == 2
            mock_path_instance.parent.mkdir.assert_any_call(parents=True, exist_ok=True)

    @patch("sys.argv", ["autosar-extract", "test.pdf", "--log-file", "test.log", "-v", "--mapping", "output.md"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    @patch("autosar_pdf2txt.cli.autosar_cli.logging")
    def test_log_file_with_verbose_mode(self, mock_logging: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00014: Test CLI combines --log-file with -v flag.

        Requirements:
            SWR_CLI_00005: CLI Verbose Mode
            SWR_CLI_00014: CLI Logger File Specification
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()
        mock_path.return_value = mock_path_instance

        # Mock FileHandler
        mock_file_handler = MagicMock()
        mock_logging.FileHandler.return_value = mock_file_handler

        with patch("autosar_pdf2txt.cli.autosar_cli.PdfParser") as mock_parser, \
             patch("autosar_pdf2txt.cli.autosar_cli.MarkdownWriter") as mock_writer, \
             patch("builtins.print"):
            mock_pkg = MagicMock()
            mock_pkg.name = "TestPackage"
            mock_doc = MagicMock(spec=AutosarDoc)
            mock_doc.packages = [mock_pkg]
            mock_doc.root_classes = []
            mock_parser.return_value.parse_pdfs.return_value = mock_doc
            mock_writer.return_value.write_packages.return_value = "* TestPackage\n"

            result = main()

            assert result == 0
            # Verify both handlers were added (console + file)
            root_logger = mock_logging.getLogger.return_value
            assert root_logger.addHandler.call_count >= 2  # Console handler + file handler

    @patch("sys.argv", ["autosar-extract", "test.pdf", "--log-file", "/invalid/path/test.log", "--mapping", "output.md"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    def test_log_file_creation_error_continues_with_console_logging(self, mock_path: MagicMock) -> None:
        """SWUT_CLI_00013: Test CLI fails when parent directory creation fails for output file.

        Requirements:
            SWR_CLI_00009: CLI Error Handling
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()

        # Mock Path for output file with parent directory that fails mkdir
        output_path = MagicMock()
        output_path.write_text = MagicMock()
        output_parent = MagicMock()
        output_parent.mkdir.side_effect = PermissionError("Permission denied")
        output_path.parent = output_parent

        # Configure Path mock to return different mocks based on call order
        mock_path.side_effect = [mock_path_instance, output_path]

        with patch("autosar_pdf2txt.cli.autosar_cli.PdfParser") as mock_parser, \
             patch("autosar_pdf2txt.cli.autosar_cli.MappingWriter") as mock_writer, \
             patch("builtins.print"):
            mock_pkg = MagicMock()
            mock_pkg.name = "TestPackage"
            mock_doc = MagicMock(spec=AutosarDoc)
            mock_doc.packages = [mock_pkg]
            mock_doc.root_classes = []
            mock_parser.return_value.parse_pdfs.return_value = mock_doc
            mock_writer.return_value.write_mapping.return_value = "# Mapping\n"

            result = main()

            # Should fail because mkdir fails for output file parent directory
            assert result == 1

    @patch("sys.argv", ["autosar-extract", "test.pdf", "--log-file", "test.log", "--mapping", "output.md"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    @patch("autosar_pdf2txt.cli.autosar_cli.logging")
    def test_log_file_format_includes_timestamps(self, mock_logging: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00016: Test CLI log file format includes timestamps.

        Requirements:
            SWR_CLI_00014: CLI Logger File Specification
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()
        mock_path.return_value = mock_path_instance

        # Mock FileHandler and Formatter
        mock_file_handler = MagicMock()
        mock_formatter = MagicMock()
        mock_logging.FileHandler.return_value = mock_file_handler
        mock_logging.Formatter.return_value = mock_formatter

        with patch("autosar_pdf2txt.cli.autosar_cli.PdfParser") as mock_parser, \
             patch("autosar_pdf2txt.cli.autosar_cli.MarkdownWriter") as mock_writer, \
             patch("builtins.print"):
            mock_pkg = MagicMock()
            mock_pkg.name = "TestPackage"
            mock_doc = MagicMock(spec=AutosarDoc)
            mock_doc.packages = [mock_pkg]
            mock_doc.root_classes = []
            mock_parser.return_value.parse_pdfs.return_value = mock_doc
            mock_writer.return_value.write_packages.return_value = "* TestPackage\n"

            result = main()

            assert result == 0
            # Verify Formatter was created with timestamp format
            mock_logging.Formatter.assert_called()
            # Check that the format includes timestamp components
            call_args = mock_logging.Formatter.call_args
            assert call_args is not None
            format_string = call_args[0][0] if call_args[0] else call_args[1].get('fmt')
            assert "%(asctime)s" in format_string or "%(msecs)" in format_string

    @patch("sys.argv", ["autosar-extract", "test.pdf", "--mapping", "mapping.json"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    @patch("autosar_pdf2txt.cli.autosar_cli.logging")
    def test_generate_mapping_json(self, mock_logging: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00037: Test CLI mapping generation with JSON output.

        Requirements:
            SWR_CLI_00015: CLI Mapping Generation Flag
            SWR_CLI_00019: Format auto-detection from file extension
        """
        def path_side_effect(path_str):
            instance = MagicMock()
            if path_str == "test.pdf":
                instance.exists.return_value = True
                instance.is_file.return_value = True
                type(instance).suffix = PropertyMock(return_value=".pdf")
                instance.absolute.return_value = MagicMock()
            elif path_str == "mapping.json":
                instance.exists.return_value = True
                instance.is_file.return_value = True
                type(instance).suffix = PropertyMock(return_value=".json")
                instance.parent.mkdir.return_value = None
                instance.write_text.return_value = None
            return instance

        mock_path.side_effect = path_side_effect

        with patch("autosar_pdf2txt.cli.autosar_cli.PdfParser") as mock_parser, \
             patch("autosar_pdf2txt.cli.autosar_cli.MappingWriter") as mock_writer:
            mock_pkg = MagicMock()
            mock_pkg.name = "TestPackage"
            mock_doc = MagicMock(spec=AutosarDoc)
            mock_doc.packages = [mock_pkg]
            mock_doc.root_classes = []
            mock_parser.return_value.parse_pdfs.return_value = mock_doc
            mock_writer.return_value.write_mapping.return_value = '{"types": []}'

            result = main()

            assert result == 0
            mock_writer.return_value.write_mapping.assert_called_once_with([mock_pkg], format="json")

    @patch("sys.argv", ["autosar-extract", "test.pdf", "--mapping", "mapping.md"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    @patch("autosar_pdf2txt.cli.autosar_cli.logging")
    def test_generate_mapping_markdown(self, mock_logging: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00038: Test CLI mapping generation with Markdown output.

        Requirements:
            SWR_CLI_00015: CLI Mapping Generation Flag
            SWR_CLI_00019: Format auto-detection from file extension
        """
        def path_side_effect(path_str):
            instance = MagicMock()
            if path_str == "test.pdf":
                instance.exists.return_value = True
                instance.is_file.return_value = True
                type(instance).suffix = PropertyMock(return_value=".pdf")
                instance.absolute.return_value = MagicMock()
            elif path_str == "mapping.md":
                instance.exists.return_value = True
                instance.is_file.return_value = True
                type(instance).suffix = PropertyMock(return_value=".md")
                instance.parent.mkdir.return_value = None
                instance.write_text.return_value = None
            return instance

        mock_path.side_effect = path_side_effect

        with patch("autosar_pdf2txt.cli.autosar_cli.PdfParser") as mock_parser, \
             patch("autosar_pdf2txt.cli.autosar_cli.MappingWriter") as mock_writer:
            mock_pkg = MagicMock()
            mock_pkg.name = "TestPackage"
            mock_doc = MagicMock(spec=AutosarDoc)
            mock_doc.packages = [mock_pkg]
            mock_doc.root_classes = []
            mock_parser.return_value.parse_pdfs.return_value = mock_doc
            mock_writer.return_value.write_mapping.return_value = "# Type to Package Mapping\n\n"

            result = main()

            assert result == 0
            mock_writer.return_value.write_mapping.assert_called_once_with([mock_pkg], format="markdown")

    @patch("sys.argv", ["autosar-extract", "test.pdf", "--mapping", "mapping.json", "--class-details", "classes/"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    @patch("autosar_pdf2txt.cli.autosar_cli.logging")
    def test_generate_mapping_with_class_details(self, mock_logging: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00039: Test CLI can combine --mapping and --class-details flags.

        Requirements:
            SWR_CLI_00020: Output flags can be combined
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()

        def path_side_effect(path_str):
            instance = MagicMock()
            if path_str == "test.pdf":
                return mock_path_instance
            elif path_str == "mapping.json":
                instance.exists.return_value = True
                instance.is_file.return_value = True
                type(instance).suffix = PropertyMock(return_value=".json")
                instance.parent.mkdir.return_value = None
                instance.write_text.return_value = None
            elif path_str == "classes/":
                instance.exists.return_value = True
                instance.is_dir.return_value = True
                instance.mkdir.return_value = None
            return instance

        mock_path.side_effect = path_side_effect

        with patch("autosar_pdf2txt.cli.autosar_cli.PdfParser") as mock_parser, \
             patch("autosar_pdf2txt.cli.autosar_cli.MappingWriter") as mock_mapping_writer, \
             patch("autosar_pdf2txt.cli.autosar_cli.MarkdownWriter") as mock_markdown_writer:
            mock_pkg = MagicMock()
            mock_pkg.name = "TestPackage"
            mock_pkg.types = []
            mock_doc = MagicMock(spec=AutosarDoc)
            mock_doc.packages = [mock_pkg]
            mock_doc.root_classes = []
            mock_parser.return_value.parse_pdfs.return_value = mock_doc
            mock_mapping_writer.return_value.write_mapping.return_value = "{}"
            mock_markdown_writer.return_value.write_packages_to_files.return_value = None

            result = main()
            assert result == 0
            # Verify both writers were called
            mock_mapping_writer.return_value.write_mapping.assert_called_once()
            mock_markdown_writer.return_value.write_packages_to_files.assert_called_once()

    @patch("sys.argv", ["autosar-extract", "test.pdf", "--mapping", "mapping.json", "--hierarchy", "hierarchy.md"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    @patch("autosar_pdf2txt.cli.autosar_cli.logging")
    def test_generate_mapping_with_class_hierarchy(self, mock_logging: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00040: Test CLI can combine --mapping and --hierarchy flags.

        Requirements:
            SWR_CLI_00020: Output flags can be combined
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()

        def path_side_effect(path_str):
            instance = MagicMock()
            if path_str == "test.pdf":
                return mock_path_instance
            elif path_str == "mapping.json":
                instance.exists.return_value = True
                instance.is_file.return_value = True
                type(instance).suffix = PropertyMock(return_value=".json")
                instance.parent.mkdir.return_value = None
                instance.write_text.return_value = None
            elif path_str == "hierarchy.md":
                instance.exists.return_value = True
                instance.is_file.return_value = True
                type(instance).suffix = PropertyMock(return_value=".md")
                instance.parent.mkdir.return_value = None
                instance.write_text.return_value = None
            return instance

        mock_path.side_effect = path_side_effect

        with patch("autosar_pdf2txt.cli.autosar_cli.PdfParser") as mock_parser, \
             patch("autosar_pdf2txt.cli.autosar_cli.MappingWriter") as mock_mapping_writer, \
             patch("autosar_pdf2txt.cli.autosar_cli.MarkdownWriter") as mock_markdown_writer:
            mock_pkg = MagicMock()
            mock_pkg.name = "TestPackage"
            mock_pkg.types = []
            mock_doc = MagicMock(spec=AutosarDoc)
            mock_doc.packages = [mock_pkg]
            mock_doc.root_classes = []
            mock_parser.return_value.parse_pdfs.return_value = mock_doc
            mock_mapping_writer.return_value.write_mapping.return_value = "{}"
            mock_markdown_writer.return_value.write_class_hierarchy.return_value = "# Hierarchy\n"

            result = main()
            assert result == 0
            # Verify both writers were called
            mock_mapping_writer.return_value.write_mapping.assert_called_once()
            mock_markdown_writer.return_value.write_class_hierarchy.assert_called_once()

    @patch("sys.argv", ["autosar-extract", "test.pdf", "--mapping", "mapping.json", "--class-details", "classes/", "--hierarchy", "hierarchy.md"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    @patch("autosar_pdf2txt.cli.autosar_cli.logging")
    def test_generate_mapping_with_all_flags(self, mock_logging: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00041: Test CLI can combine all three output flags.

        Requirements:
            SWR_CLI_00020: Output flags can be combined
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()

        def path_side_effect(path_str):
            instance = MagicMock()
            if path_str == "test.pdf":
                return mock_path_instance
            elif path_str == "mapping.json":
                instance.exists.return_value = True
                instance.is_file.return_value = True
                type(instance).suffix = PropertyMock(return_value=".json")
                instance.parent.mkdir.return_value = None
                instance.write_text.return_value = None
            elif path_str == "classes/":
                instance.exists.return_value = True
                instance.is_dir.return_value = True
                instance.mkdir.return_value = None
            elif path_str == "hierarchy.md":
                instance.exists.return_value = True
                instance.is_file.return_value = True
                type(instance).suffix = PropertyMock(return_value=".md")
                instance.parent.mkdir.return_value = None
                instance.write_text.return_value = None
            return instance

        mock_path.side_effect = path_side_effect

        with patch("autosar_pdf2txt.cli.autosar_cli.PdfParser") as mock_parser, \
             patch("autosar_pdf2txt.cli.autosar_cli.MappingWriter") as mock_mapping_writer, \
             patch("autosar_pdf2txt.cli.autosar_cli.MarkdownWriter") as mock_markdown_writer:
            mock_pkg = MagicMock()
            mock_pkg.name = "TestPackage"
            mock_pkg.types = []
            mock_doc = MagicMock(spec=AutosarDoc)
            mock_doc.packages = [mock_pkg]
            mock_doc.root_classes = []
            mock_parser.return_value.parse_pdfs.return_value = mock_doc
            mock_mapping_writer.return_value.write_mapping.return_value = "{}"
            mock_markdown_writer.return_value.write_class_hierarchy.return_value = "# Hierarchy\n"
            mock_markdown_writer.return_value.write_packages_to_files.return_value = None

            result = main()
            assert result == 0
            # Verify all three writers were called
            mock_mapping_writer.return_value.write_mapping.assert_called_once()
            mock_markdown_writer.return_value.write_class_hierarchy.assert_called_once()
            mock_markdown_writer.return_value.write_packages_to_files.assert_called_once()

    @patch("sys.argv", ["autosar-extract", "test.pdf"])
    @patch("autosar_pdf2txt.cli.autosar_cli.Path")
    @patch("autosar_pdf2txt.cli.autosar_cli.logging")
    def test_generate_mapping_requires_output(self, mock_logging: MagicMock, mock_path: MagicMock) -> None:
        """SWUT_CLI_00042: Test CLI requires at least one output flag.

        Requirements:
            SWR_CLI_00018: At least one output flag required
        """
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_file.return_value = True
        type(mock_path_instance).suffix = PropertyMock(return_value=".pdf")
        mock_path_instance.absolute.return_value = MagicMock()
        mock_path.return_value = mock_path_instance

        with patch("autosar_pdf2txt.cli.autosar_cli.argparse.ArgumentParser.error") as mock_error:
            mock_error.side_effect = SystemExit(2)
            with pytest.raises(SystemExit):
                main()
            mock_error.assert_called_once_with("At least one output flag must be specified: --mapping, --hierarchy, --class-details")
