"""Command-line interface for extracting AUTOSAR models from PDF files."""

import argparse
import logging
import sys
from pathlib import Path

from autosar_pdf2txt import PdfParser, MarkdownWriter


def main() -> int:
    """Main entry point for the CLI.

    Requirements:
        SWR_CLI_00001: CLI Entry Point
        SWR_CLI_00010: CLI Class File Output
        SWR_CLI_00011: CLI Class Files Flag
        SWR_CLI_00012: CLI Class Hierarchy Flag

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
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--include-class-details",
        action="store_true",
        help="Create separate markdown files for each class (requires -o/--output)",
    )
    parser.add_argument(
        "--include-class-hierarchy",
        action="store_true",
        help="Generate class inheritance hierarchy and write to a separate file (requires -o/--output)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output mode for detailed debug information",
    )

    args = parser.parse_args()

    # Configure logging based on verbose flag
    # SWR_CLI_00005: CLI Verbose Mode
    # SWR_CLI_00008: CLI Logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
    )

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
            logging.info(f"Found {len(pdf_files_in_dir)} PDF file(s) in directory: {input_path}")
        else:
            logging.error(f"Not a file or directory: {input_path}")
            return 1

    if not pdf_paths:
        logging.error("No PDF files to process")
        return 1

    try:
        # Parse all PDFs
        pdf_parser = PdfParser()
        all_docs = []

        for pdf_path in pdf_paths:
            # SWR_CLI_00007: CLI Progress Feedback
            logging.info(f"Parsing PDF: {pdf_path}")
            logging.debug(f"  Full path: {pdf_path.absolute()}")
            doc = pdf_parser.parse_pdf(str(pdf_path))
            all_docs.append(doc)
            logging.info(f"  Found {len(doc.packages)} top-level packages")
            logging.info(f"  Found {len(doc.root_classes)} root classes")
            if args.verbose:
                for pkg in doc.packages:
                    logging.debug(f"    - {pkg.name}")

        # Merge all documents into a single document
        # SWR_CLI_00007: CLI Progress Feedback
        merged_packages = []
        merged_root_classes = []
        for doc in all_docs:
            merged_packages.extend(doc.packages)
            merged_root_classes.extend(doc.root_classes)

        logging.info(f"Total: {len(merged_packages)} top-level packages")
        logging.info(f"Total: {len(merged_root_classes)} root classes")

        # Write to markdown
        writer = MarkdownWriter()
        markdown = writer.write_packages(merged_packages)

        # SWR_CLI_00012: CLI Class Hierarchy Flag
        # Generate class hierarchy if requested
        class_hierarchy = None
        if args.include_class_hierarchy:
            logging.info("Generating class hierarchy...")
            # Collect all classes from packages for building hierarchy
            all_classes = []
            for pkg in merged_packages:
                classes_from_pkg = writer._collect_classes_from_package(pkg)
                all_classes.extend(classes_from_pkg)

            logging.info(f"Collected {len(all_classes)} classes from {len(merged_packages)} packages")
            logging.debug(f"Root classes for hierarchy: {len(merged_root_classes)}")

            class_hierarchy = writer.write_class_hierarchy(merged_root_classes, all_classes)
            if class_hierarchy:
                logging.info(f"Generated class hierarchy for {len(merged_root_classes)} root classes")

        # SWR_CLI_00004: CLI Output File Option
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(markdown, encoding="utf-8")
            logging.info(f"Output written to: {args.output}")

            # SWR_CLI_00012: CLI Class Hierarchy Flag
            # Write class hierarchy to separate file if flag is enabled
            if class_hierarchy:
                # Generate hierarchy file name by inserting "-hierarchy" before the extension
                hierarchy_path = output_path.with_stem(f"{output_path.stem}-hierarchy")
                hierarchy_path.write_text(class_hierarchy, encoding="utf-8")
                logging.info(f"Class hierarchy written to: {hierarchy_path}")

            # SWR_CLI_00010: CLI Class File Output
            # SWR_CLI_00011: CLI Class Files Flag
            # Write each class to separate files if flag is enabled
            if args.include_class_details:
                writer.write_packages_to_files(merged_packages, output_path=output_path)
                logging.info(f"Class files written to directory: {output_path.parent}")
        else:
            print(markdown, end="")

        return 0

    except Exception as e:
        # SWR_CLI_00009: CLI Error Handling
        logging.error(f"{e}")
        if args.verbose:
            logging.exception("Detailed error traceback:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
