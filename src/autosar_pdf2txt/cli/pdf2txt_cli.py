"""
PDF conversion CLI
"""

import argparse
import sys
from pathlib import Path
from ..core import (
    convert_pdf_to_text,
    convert_pdf_to_text_advanced,
    convert_to_markdown,
    clean_special_characters,
    convert_table_to_markdown,
    convert_pdf_with_tables,
)


def main():
    """
    Main entry point for PDF conversion CLI
    """
    parser = argparse.ArgumentParser(description="Convert PDF files to text format")
    parser.add_argument(
        "input", help="Input PDF file or directory containing PDF files"
    )
    parser.add_argument(
        "-o", "--output", help="Output file or directory for converted text files"
    )
    parser.add_argument(
        "-p",
        "--pages",
        help="Specific pages to extract (e.g., '0,1,3' for pages 1,2,4 or '0-5' for pages 1-6)",
    )
    parser.add_argument(
        "--include-images",
        action="store_true",
        help="Include image metadata in output",
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="Overwrite existing output files"
    )
    parser.add_argument(
        "--skip-header",
        type=int,
        default=0,
        help="Number of lines to skip at beginning of each page (header)",
    )
    parser.add_argument(
        "--skip-footer",
        type=int,
        default=0,
        help="Number of lines to skip at end of each page (footer)",
    )
    parser.add_argument(
        "--format",
        choices=["txt", "markdown", "md"],
        default="txt",
        help="Output format: txt (plain text), markdown or md (markdown format)",
    )
    parser.add_argument(
        "--clean-special-chars",
        action="store_true",
        default=True,
        help="Clean special characters from output (default: True)",
    )
    parser.add_argument(
        "--no-clean", action="store_true", help="Disable special character cleaning"
    )
    parser.add_argument(
        "--extract-tables",
        action="store_true",
        help="Extract tables from PDF and format them as Markdown tables",
    )
    parser.add_argument(
        "--tables-only",
        action="store_true",
        help="Extract only tables, skip other text content",
    )

    args = parser.parse_args()

    # Handle --no-clean flag
    if args.no_clean:
        args.clean_special_chars = False

    input_path = Path(args.input)

    # Handle single file or directory
    if input_path.is_file():
        if input_path.suffix.lower() != ".pdf":
            print(f"Error: {input_path} is not a PDF file")
            sys.exit(1)

        handle_single_pdf(input_path, args)
    elif input_path.is_dir():
        handle_pdf_directory(input_path, args)
    else:
        print(f"Error: {input_path} does not exist")
        sys.exit(1)


def parse_page_range(page_str):
    """
    Parse page range string like '0,1,3' or '0-5' or '2-4,7,9'
    Returns a list of 0-indexed page numbers
    """
    if not page_str:
        return None

    result = []
    parts = page_str.split(",")
    for part in parts:
        if "-" in part:
            start, end = map(int, part.split("-"))
            result.extend(range(start, end + 1))
        else:
            result.append(int(part))

    # Convert to 0-indexed
    return [p - 1 for p in result if p >= 0]


def handle_single_pdf(pdf_path, args):
    """Handle conversion of a single PDF file"""
    output_path = args.output

    # Determine output file extension based on format
    output_ext = ".md" if args.format in ["markdown", "md"] else ".txt"

    # If no output specified, create output path based on input
    if not output_path:
        output_path = pdf_path.with_suffix(output_ext)
    else:
        output_path = Path(output_path)
        # If output is a directory, create output file inside it
        if output_path.is_dir():
            output_path = output_path / pdf_path.with_suffix(output_ext).name

    # Check if output file already exists
    if output_path.exists() and not args.force:
        print(
            f"Output file {output_path} already exists. Use -f to overwrite or specify a different output."
        )
        return

    try:
        result = None
        # Parse page range if specified
        page_range = parse_page_range(args.pages)

        # Convert PDF with or without table extraction
        if args.extract_tables or args.tables_only:
            result = convert_pdf_with_tables(
                str(pdf_path),
                output_format=args.format,
                page_range=page_range,
                skip_header_lines=args.skip_header,
                skip_footer_lines=args.skip_footer,
                include_tables=True,
            )

            if args.tables_only:
                # Extract only tables
                text = ""
                for table_info in result["tables"]:
                    text += f"\n\nTable on page {table_info['page'] + 1}:\n\n"
                    text += convert_table_to_markdown(table_info["table"])
                    text += "\n"
                print(f"Extracted {len(result['tables'])} tables from PDF")
            else:
                # Include both text and tables
                text = result["text"]
                # Append tables at end
                if result["tables"]:
                    text += "\n\n---\n\n## Extracted Tables\n\n"
                    for idx, table_info in enumerate(result["tables"], 1):
                        text += f"### Table {idx} (Page {table_info['page'] + 1})\n\n"
                        text += convert_table_to_markdown(table_info["table"])
                        text += "\n\n"
                    print(f"Extracted {len(result['tables'])} tables from PDF")
        else:
            # Regular conversion without table extraction
            if page_range or args.include_images:
                result = convert_pdf_to_text_advanced(
                    str(pdf_path),
                    page_range=page_range,
                    include_images=args.include_images,
                    skip_header_lines=args.skip_header,
                    skip_footer_lines=args.skip_footer,
                )
                text = result["text"]
            else:
                text = convert_pdf_to_text(
                    str(pdf_path),
                    skip_header_lines=args.skip_header,
                    skip_footer_lines=args.skip_footer,
                )

            # Clean special characters if enabled
            if args.clean_special_chars:
                text = clean_special_characters(text)

            # Convert to markdown if requested
            if args.format in ["markdown", "md"]:
                text = convert_to_markdown(text, preserve_structure=True)

        # Write to output file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(
            f"Successfully converted {pdf_path} to {output_path} ({args.format} format)"
        )

        if result and args.include_images and "images" in result:
            print(f"Found {len(result['images'])} images in PDF")

    except Exception as e:
        print(f"Error converting {pdf_path}: {str(e)}")
        sys.exit(1)


def handle_pdf_directory(pdf_dir, args):
    """Handle conversion of all PDF files in a directory"""
    pdf_dir = Path(pdf_dir)
    output_dir = Path(args.output) if args.output else pdf_dir

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all PDF files in directory
    pdf_files = list(pdf_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {pdf_dir}")
        return

    print(f"Found {len(pdf_files)} PDF files to convert")

    # Determine output file extension based on format
    output_ext = ".md" if args.format in ["markdown", "md"] else ".txt"

    for pdf_file in pdf_files:
        # Create output path in output directory
        output_path = output_dir / pdf_file.with_suffix(output_ext).name

        # Skip if output file exists and force flag is not set
        if output_path.exists() and not args.force:
            print(f"Skipping {pdf_file} (output already exists, use -f to overwrite)")
            continue

        try:
            text = convert_pdf_to_text(
                str(pdf_file),
                skip_header_lines=args.skip_header,
                skip_footer_lines=args.skip_footer,
            )

            # Clean special characters if enabled
            if args.clean_special_chars:
                text = clean_special_characters(text)

            # Convert to markdown if requested
            if args.format in ["markdown", "md"]:
                text = convert_to_markdown(text, preserve_structure=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(
                f"Converted: {pdf_file.name} -> {output_path.name} ({args.format} format)"
            )

        except Exception as e:
            print(f"Error converting {pdf_file}: {str(e)}")


if __name__ == "__main__":
    main()
