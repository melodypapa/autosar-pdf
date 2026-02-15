"""Command-line interface for extracting AUTOSAR models from PDF files."""

import argparse
import logging
import sys
from pathlib import Path

from autosar_pdf2txt import PdfParser
from autosar_pdf2txt.writer import MappingWriter, MarkdownWriter, JsonWriter
from autosar_pdf2txt.models import AutosarClass, AutosarEnumeration, AutosarPrimitive


def main() -> int:
    """Main entry point for the CLI.

    Requirements:
        SWR_CLI_00001: CLI Entry Point
        SWR_CLI_00014: CLI Logger File Specification
        SWR_CLI_00015: --mapping FILE argument
        SWR_CLI_00016: --hierarchy FILE argument
        SWR_CLI_00017: --class-details DIR argument
        SWR_CLI_00018: At least one output flag required
        SWR_CLI_00019: Format auto-detection from file extension
        SWR_CLI_00020: Output flags can be combined

    Returns:
        Exit code (0 for success, 1 for error).
    """
    parser = argparse.ArgumentParser(
        description="Extract AUTOSAR package and class hierarchies from PDF files."
    )
    parser.add_argument(
        "pdf_files",
        type=str,
        nargs="+",
        help="Path(s) to PDF file(s) or director(y/ies) containing PDFs to parse",
    )
    # Output arguments (at least one required)
    output_group = parser.add_argument_group("output arguments")
    output_group.add_argument(
        "--mapping",
        metavar="FILE",
        help="Generate type-to-package mapping to FILE",
    )
    output_group.add_argument(
        "--hierarchy",
        metavar="FILE",
        help="Generate class inheritance hierarchy to FILE",
    )
    output_group.add_argument(
        "--class-details",
        metavar="DIR",
        help="Generate individual class files to DIR/",
    )
    output_group.add_argument(
        "--json",
        action="store_true",
        help="Generate class details in JSON format (requires --class-details)",
    )
    output_group.add_argument(
        "--markdown",
        action="store_true",
        help="Generate class details in Markdown format (requires --class-details)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output mode for detailed debug information",
    )
    parser.add_argument(
        "--log-file",
        type=str,
        help="Write log messages to the specified file (in addition to stderr)",
    )

    args = parser.parse_args()

    # SWR_CLI_00018: At least one output flag required
    # Validate at least one output flag is specified
    if not any([args.mapping, args.hierarchy, args.class_details]):
        parser.error("At least one output flag must be specified: --mapping, --hierarchy, --class-details")

    # Validate format flags
    if args.json or args.markdown:
        if not args.class_details:
            parser.error("--json and --markdown flags require --class-details to be specified")
        if args.json and args.markdown:
            parser.error("Cannot specify both --json and --markdown. Choose one format.")

    # Configure logging based on verbose flag
    # SWR_CLI_00005: CLI Verbose Mode
    # SWR_CLI_00008: CLI Logging
    # SWR_CLI_00014: CLI Logger File Specification
    log_level = logging.DEBUG if args.verbose else logging.INFO
    log_format = "%(levelname)s: %(message)s"
    log_file_format = "%(asctime)s.%(msecs)03d: %(levelname)s: %(message)s"
    log_date_format = "%Y-%m-%d %H:%M:%S"

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels

    # Console handler (stderr)
    # In verbose mode: show DEBUG and above
    # In normal mode: show INFO and above (WARNING goes to file only)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(log_level if args.verbose else logging.INFO)
    # Filter out WARNING level messages from console (they go to file instead)
    if not args.verbose:
        console_handler.addFilter(lambda record: record.levelno != logging.WARNING)
    console_handler.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(console_handler)

    # WARNING file handler - always log WARNING messages to a file
    # In normal mode, this keeps console output clean while preserving warnings for debugging
    # In verbose mode, warnings are shown on console AND logged to file
    if not args.verbose:
        warning_log_file = Path("autosar_pdf_warnings.log")
        try:
            warning_handler = logging.FileHandler(warning_log_file, mode='w', encoding='utf-8')
            warning_handler.setLevel(logging.WARNING)
            warning_handler.setFormatter(logging.Formatter(log_file_format, datefmt=log_date_format))
            root_logger.addHandler(warning_handler)
        except Exception as e:
            # If we can't create the warning log, just log to console
            logging.error(f"Failed to create warning log file '{warning_log_file}': {e}")

    # File handler (if --log-file is specified)
    # SWR_CLI_00014: CLI Logger File Specification
    if args.log_file:
        try:
            log_file_path = Path(args.log_file)
            # Create parent directories if they don't exist
            log_file_path.parent.mkdir(parents=True, exist_ok=True)

            # Create file handler with timestamps
            file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')
            file_handler.setLevel(log_level)
            file_handler.setFormatter(logging.Formatter(log_file_format, datefmt=log_date_format))
            root_logger.addHandler(file_handler)
        except Exception as e:
            logging.error(f"Failed to create log file '{args.log_file}': {e}")
            # Continue with console-only logging

    # Suppress pdfminer warnings about invalid color values in PDF files
    # These warnings don't affect text extraction functionality
    logging.getLogger("pdfminer").setLevel(logging.ERROR)

    # Validate and collect input paths (files and directories)
    # SWR_CLI_00006: CLI Input Validation
    pdf_paths = []
    for input_path in args.pdf_files:
        path = Path(input_path)
        if not path.exists():
            logging.error(f"Path not found: {input_path}")
            return 1

        if path.is_file():
            # It's a file, add directly
            if path.suffix.lower() != ".pdf":
                logging.warning(f"Skipping non-PDF file: {input_path}")
                continue
            pdf_paths.append(path)
        elif path.is_dir():
            # It's a directory, find all PDF files
            # SWR_CLI_00003: CLI Directory Input Support
            pdf_files_in_dir = sorted(path.glob("*.pdf"))
            if not pdf_files_in_dir:
                logging.warning(f"No PDF files found in directory: {input_path}")
                continue
            pdf_paths.extend(pdf_files_in_dir)
            logging.info(f"📂 Found {len(pdf_files_in_dir)} PDF file(s) in directory: {input_path}")
        else:
            logging.error(f"Not a file or directory: {input_path}")
            return 1

    if not pdf_paths:
        logging.error("No PDF files to process")
        return 1

    try:
        # Parse all PDFs using parse_pdfs() to ensure parent/child relationships
        # are resolved after all models are loaded (not per-PDF)
        pdf_parser = PdfParser()

        # SWR_CLI_00007: CLI Progress Feedback
        logging.info(f"🔄 Parsing {len(pdf_paths)} PDF file(s)...")

        pdf_path_strings = [str(pdf_path) for pdf_path in pdf_paths]

        # Parse all PDFs at once - parent/children resolution happens on complete model
        doc = pdf_parser.parse_pdfs(pdf_path_strings)

        # Calculate statistics
        total_classes = 0
        total_enums = 0
        total_primitives = 0
        total_types = 0
        for pkg in doc.packages:
            for typ in pkg.types:
                if isinstance(typ, AutosarClass):
                    total_classes += 1
                elif isinstance(typ, AutosarEnumeration):
                    total_enums += 1
                elif isinstance(typ, AutosarPrimitive):
                    total_primitives += 1
                total_types += 1

        logging.info(f"📦 Total: {len(doc.packages)} top-level packages")
        logging.info(f"🏛️  Total: {len(doc.root_classes)} root classes")
        logging.info(f"📊 Extracted: {total_classes} classes, {total_enums} enumerations, {total_primitives} primitives ({total_types} total types)")

        if args.verbose:
            for pkg in doc.packages:
                logging.debug(f"  - {pkg.name}")

        # Generate outputs based on specified flags
        # SWR_CLI_00015: --mapping FILE argument
        # SWR_CLI_00016: --hierarchy FILE argument
        # SWR_CLI_00017: --class-details DIR argument
        # SWR_CLI_00019: Format auto-detection from file extension
        # SWR_CLI_00020: Output flags can be combined
        outputs = []

        if args.mapping:
            from autosar_pdf2txt.utils import detect_format

            mapping_writer = MappingWriter()
            format_str = detect_format(args.mapping)
            logging.info(f"📊 Generating type-to-package mapping in {format_str.upper()} format...")

            mapping = mapping_writer.write_mapping(doc.packages, format=format_str)  # type: ignore[arg-type]

            # Ensure parent directory exists
            Path(args.mapping).parent.mkdir(parents=True, exist_ok=True)

            with open(args.mapping, "w", encoding="utf-8") as f:
                f.write(mapping)
            outputs.append(args.mapping)

        if args.hierarchy:
            from autosar_pdf2txt.utils import detect_format

            hierarchy_format = detect_format(args.hierarchy)
            logging.info(f"🏛️  Generating class inheritance hierarchy in {hierarchy_format.upper()} format...")

            # Collect all classes for building hierarchy
            markdown_writer = MarkdownWriter()
            all_classes = []
            for pkg in doc.packages:
                classes_from_pkg = markdown_writer._collect_classes_from_package(pkg)
                all_classes.extend(classes_from_pkg)

            # Generate hierarchy content
            hierarchy_content = markdown_writer.write_class_hierarchy(doc.root_classes, all_classes)

            # Ensure parent directory exists
            Path(args.hierarchy).parent.mkdir(parents=True, exist_ok=True)

            with open(args.hierarchy, "w", encoding="utf-8") as f:
                f.write(hierarchy_content)
            outputs.append(args.hierarchy)

        if args.class_details:
            # Determine format
            if args.json:
                format_name = "JSON"
                json_writer = JsonWriter()
                json_writer.write_packages_to_files(doc.packages, base_dir=Path(args.class_details))
            else:
                # Default to Markdown (either explicitly requested or as default)
                format_name = "Markdown"
                markdown_writer = MarkdownWriter()
                markdown_writer.write_packages_to_files(doc.packages, base_dir=Path(args.class_details))

            logging.info(f"📝 Generating individual class files in {format_name} format...")

            # Ensure directory exists
            Path(args.class_details).mkdir(parents=True, exist_ok=True)

            outputs.append(args.class_details)

        # Log success
        if outputs:
            logging.info(f"✅ Generated {len(outputs)} output(s): {', '.join(outputs)}")

        return 0

    except Exception as e:
        # SWR_CLI_00009: CLI Error Handling
        logging.error(f"{e}")
        if args.verbose:
            logging.exception("Detailed error traceback:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
