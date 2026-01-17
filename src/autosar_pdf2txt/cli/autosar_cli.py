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
        "--write-class-files",
        action="store_true",
        help="Create separate markdown files for each class (requires -o/--output)",
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
        all_packages = []

        for pdf_path in pdf_paths:
            # SWR_CLI_00007: CLI Progress Feedback
            logging.info(f"Parsing PDF: {pdf_path}")
            logging.debug(f"  Full path: {pdf_path.absolute()}")
            packages = pdf_parser.parse_pdf(str(pdf_path))
            all_packages.extend(packages)
            logging.info(f"  Found {len(packages)} top-level packages")
            if args.verbose:
                for pkg in packages:
                    logging.debug(f"    - {pkg.name}")

        # SWR_CLI_00007: CLI Progress Feedback
        logging.info(f"Total: {len(all_packages)} top-level packages")

        # Write to markdown
        writer = MarkdownWriter()
        markdown = writer.write_packages(all_packages)

        # SWR_CLI_00004: CLI Output File Option
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(markdown, encoding="utf-8")
            logging.info(f"Output written to: {args.output}")

            # SWR_CLI_00010: CLI Class File Output
            # SWR_CLI_00011: CLI Class Files Flag
            # Write each class to separate files if flag is enabled
            if args.write_class_files:
                writer.write_packages_to_files(all_packages, output_path=output_path)
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
