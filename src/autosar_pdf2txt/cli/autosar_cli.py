"""Command-line interface for extracting AUTOSAR models from PDF files."""

import argparse
import sys
from pathlib import Path

from autosar_pdf2txt import PdfParser, MarkdownWriter


def main() -> int:
    """Main entry point for the CLI.

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
        help="Path(s) to the PDF file(s) to parse",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--no-deduplicate",
        action="store_true",
        help="Disable deduplication of packages and classes",
    )

    args = parser.parse_args()

    # Validate input files
    pdf_paths = []
    for pdf_file in args.pdf_files:
        pdf_path = Path(pdf_file)
        if not pdf_path.exists():
            print(f"Error: PDF file not found: {pdf_file}", file=sys.stderr)
            return 1
        if not pdf_path.is_file():
            print(f"Error: Not a file: {pdf_file}", file=sys.stderr)
            return 1
        pdf_paths.append(pdf_path)

    try:
        # Parse all PDFs
        pdf_parser = PdfParser()
        all_packages = []

        for pdf_path in pdf_paths:
            print(f"Parsing PDF: {pdf_path}", file=sys.stderr)
            packages = pdf_parser.parse_pdf(str(pdf_path))
            all_packages.extend(packages)
            print(f"  Found {len(packages)} top-level packages", file=sys.stderr)

        print(f"Total: {len(all_packages)} top-level packages", file=sys.stderr)

        # Write to markdown
        writer = MarkdownWriter(deduplicate=not args.no_deduplicate)
        markdown = writer.write_packages(all_packages)

        # Output
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(markdown, encoding="utf-8")
            print(f"Output written to: {args.output}", file=sys.stderr)
        else:
            print(markdown, end="")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
