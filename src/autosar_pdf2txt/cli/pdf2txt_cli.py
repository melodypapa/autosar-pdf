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
from ..progress import ProgressReporter


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
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed progress information",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress all output except errors",
    )

    args = parser.parse_args()

    # Handle --no-clean flag
    if args.no_clean:
        args.clean_special_chars = False

    # Create progress reporter
    verbose = args.verbose and not args.quiet
    progress = ProgressReporter(verbose=verbose)

    input_path = Path(args.input)

    # Handle single file or directory
    if input_path.is_file():
        if input_path.suffix.lower() != ".pdf":
            print(f"Error: {input_path} is not a PDF file")
            sys.exit(1)

        handle_single_pdf(input_path, args, progress)
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


def determine_output_path(pdf_path, args):
    """
    Determine the output file path based on input arguments.

    Args:
        pdf_path (Path): Path to input PDF file
        args: Parsed command-line arguments

    Returns:
        Path: Resolved output file path
    """
    output_ext = ".md" if args.format in ["markdown", "md"] else ".txt"

    if not args.output:
        return pdf_path.with_suffix(output_ext)

    output_path = Path(args.output)
    if output_path.is_dir():
        return output_path / pdf_path.with_suffix(output_ext).name

    return output_path


def check_output_file_exists(output_path, force, progress):
    """
    Check if output file exists and handle accordingly.

    Args:
        output_path (Path): Path to output file
        force (bool): Whether to overwrite existing files
        progress: Progress reporter instance

    Returns:
        bool: True if should proceed with conversion, False otherwise
    """
    if output_path.exists() and not force:
        progress.warning(
            f"Output file {output_path} already exists. Use -f to overwrite or specify a different output."
        )
        return False
    return True


def extract_tables_only(result, progress):
    """
    Extract only tables from conversion result.

    Args:
        result (dict): Conversion result from convert_pdf_with_tables
        progress: Progress reporter instance

    Returns:
        str: Text containing only tables
    """
    progress.step("Processing tables", 2, 3)
    text = ""
    for table_info in result["tables"]:
        text += f"\n\nTable on page {table_info['page'] + 1}:\n\n"
        text += convert_table_to_markdown(table_info["table"])
        text += "\n"
    progress.info(f"Extracted {len(result['tables'])} tables from PDF")
    return text


def extract_text_with_tables(result, progress):
    """
    Extract text with tables appended at the end.

    Args:
        result (dict): Conversion result from convert_pdf_with_tables
        progress: Progress reporter instance

    Returns:
        str: Text with tables appended
    """
    progress.step("Processing tables", 2, 3)
    text = result["text"]

    if result["tables"]:
        text += "\n\n---\n\n## Extracted Tables\n\n"
        for idx, table_info in enumerate(result["tables"], 1):
            text += f"### Table {idx} (Page {table_info['page'] + 1})\n\n"
            text += convert_table_to_markdown(table_info["table"])
            text += "\n\n"
        progress.info(f"Extracted {len(result['tables'])} tables from PDF")

    return text


def convert_pdf_with_table_extraction(pdf_path, args, page_range, progress):
    """
    Convert PDF with table extraction enabled.

    Args:
        pdf_path (Path): Path to input PDF file
        args: Parsed command-line arguments
        page_range (list): Optional list of page numbers to extract
        progress: Progress reporter instance

    Returns:
        tuple: (text, result) where text is the converted text and result contains metadata
    """
    progress.step("Extracting PDF content", 1, 3)

    result = convert_pdf_with_tables(
        str(pdf_path),
        output_format=args.format,
        page_range=page_range,
        skip_header_lines=args.skip_header,
        skip_footer_lines=args.skip_footer,
        include_tables=True,
    )

    if args.tables_only:
        text = extract_tables_only(result, progress)
    else:
        text = extract_text_with_tables(result, progress)

    return text, result


def convert_pdf_basic(pdf_path, args, page_range, progress):
    """
    Convert PDF without table extraction.

    Args:
        pdf_path (Path): Path to input PDF file
        args: Parsed command-line arguments
        page_range (list): Optional list of page numbers to extract
        progress: Progress reporter instance

    Returns:
        tuple: (text, result) where text is the converted text and result contains metadata
    """
    progress.step("Extracting PDF content", 1, 2)

    def progress_callback(current, total):
        progress.page_progress(current, total, "Extracting")

    result = None
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
            progress_callback=progress_callback,
        )

    return text, result


def process_text_post_conversion(text, args, progress, total_steps=2):
    """
    Apply post-conversion text processing (cleaning and markdown conversion).

    Args:
        text (str): Input text
        args: Parsed command-line arguments
        progress: Progress reporter instance (can be None)
        total_steps (int): Total number of steps for progress display

    Returns:
        str: Processed text
    """
    if args.clean_special_chars:
        if progress:
            step_num = 1 if args.format in ["markdown", "md"] else 2
            progress.step("Cleaning text", step_num, total_steps)
        text = clean_special_characters(text)

    if args.format in ["markdown", "md"]:
        if progress:
            step_num = 2 if args.clean_special_chars else 1
            progress.step("Converting to markdown", step_num, total_steps)
        text = convert_to_markdown(text, preserve_structure=True)

    return text


def write_output_file(text, output_path, progress):
    """
    Write converted text to output file.

    Args:
        text (str): Text to write
        output_path (Path): Path to output file
        progress: Progress reporter instance
    """
    progress.step("Writing output file", 3, 3)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


def display_conversion_results(pdf_path, output_path, result, args, progress):
    """
    Display conversion success message and additional information.

    Args:
        pdf_path (Path): Path to input PDF file
        output_path (Path): Path to output file
        result (dict): Conversion result containing metadata
        args: Parsed command-line arguments
        progress: Progress reporter instance
    """
    progress.finish(f"Converting {pdf_path.name}")

    if not args.quiet:
        progress.success(
            f"Successfully converted {pdf_path} to {output_path} ({args.format} format)"
        )

    if result and args.include_images and "images" in result:
        progress.info(f"Found {len(result['images'])} images in PDF")


def handle_single_pdf(pdf_path, args, progress):
    """
    Handle conversion of a single PDF file.

    Args:
        pdf_path (Path): Path to input PDF file
        args: Parsed command-line arguments
        progress: Progress reporter instance
    """
    output_path = determine_output_path(pdf_path, args)

    if not check_output_file_exists(output_path, args.force, progress):
        return

    try:
        progress.start(f"Converting {pdf_path.name}")

        page_range = parse_page_range(args.pages)

        if args.extract_tables or args.tables_only:
            text, result = convert_pdf_with_table_extraction(pdf_path, args, page_range, progress)
        else:
            text, result = convert_pdf_basic(pdf_path, args, page_range, progress)
            total_steps = 3 if args.format in ["markdown", "md"] and args.clean_special_chars else 2
            text = process_text_post_conversion(text, args, progress, total_steps)

        write_output_file(text, output_path, progress)
        display_conversion_results(pdf_path, output_path, result, args, progress)

    except Exception as e:
        progress.error(f"Error converting {pdf_path}: {str(e)}")
        sys.exit(1)


def convert_pdf_for_directory(pdf_file, output_dir, args):
    """
    Convert a single PDF file for directory batch processing.

    Args:
        pdf_file (Path): Path to input PDF file
        output_dir (Path): Directory for output files
        args: Parsed command-line arguments

    Returns:
        tuple: (success: bool, output_path: Path or None, error_message: str or None)
    """
    output_ext = ".md" if args.format in ["markdown", "md"] else ".txt"
    output_path = output_dir / pdf_file.with_suffix(output_ext).name

    if output_path.exists() and not args.force:
        return False, None, f"Skipping {pdf_file} (output already exists, use -f to overwrite)"

    try:
        text = convert_pdf_to_text(
            str(pdf_file),
            skip_header_lines=args.skip_header,
            skip_footer_lines=args.skip_footer,
        )

        text = process_text_post_conversion(text, args, progress=None, total_steps=2)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        return True, output_path, None

    except Exception as e:
        return False, None, f"Error converting {pdf_file}: {str(e)}"


def handle_pdf_directory(pdf_dir, args):
    """
    Handle conversion of all PDF files in a directory.

    Args:
        pdf_dir (Path): Directory containing PDF files
        args: Parsed command-line arguments
    """
    pdf_dir = Path(pdf_dir)
    output_dir = Path(args.output) if args.output else pdf_dir

    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = list(pdf_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {pdf_dir}")
        return

    print(f"Found {len(pdf_files)} PDF files to convert")

    for pdf_file in pdf_files:
        success, output_path, message = convert_pdf_for_directory(pdf_file, output_dir, args)

        if success:
            print(
                f"Converted: {pdf_file.name} -> {output_path.name} ({args.format} format)"
            )
        else:
            print(message)


if __name__ == "__main__":
    main()
