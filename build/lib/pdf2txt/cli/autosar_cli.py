"""
AUTOSAR extraction CLI
"""

import argparse
import sys
from pathlib import Path
from ..extractor import (
    extract_from_pdf,
    extract_package_and_class_info,
    build_package_hierarchy,
    write_markdown_hierarchy,
    write_text_summary,
)
from ..extractor.integration import extract_from_multiple_pdfs


def main():
    """
    Main entry point for AUTOSAR extraction CLI
    """
    parser = argparse.ArgumentParser(
        prog="autosar-extract",
        description="Extract AUTOSAR package and class information from PDF specifications",
    )

    # Positional arguments
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Input PDF file(s) or directory containing PDFs",
    )

    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output file path. For multiple inputs, this is used for merged output. "
        "If not specified with --merge, uses <input>.md for markdown format "
        "or <input>_summary.txt for text format for each file",
    )
    output_group.add_argument(
        "--merge",
        action="store_true",
        help="Merge all packages from multiple PDFs into a single output file",
    )
    output_group.add_argument(
        "-f",
        "--format",
        choices=["markdown", "md", "text", "txt"],
        default="markdown",
        help="Output format: markdown/md (hierarchical structure) or text/txt (flat summary) "
        "(default: markdown)",
    )
    output_group.add_argument(
        "--title",
        default="AUTOSAR Package and Class Reference",
        help="Document title for markdown output (default: 'AUTOSAR Package and Class Reference')",
    )

    # Extraction options
    extraction_group = parser.add_argument_group("Extraction Options")
    extraction_group.add_argument(
        "-m",
        "--method",
        choices=["pdfplumber", "pypdf2"],
        default="pdfplumber",
        help="PDF text extraction method. pdfplumber is recommended for better accuracy "
        "with complex layouts (default: pdfplumber)",
    )

    # Filter options
    filter_group = parser.add_argument_group("Filter Options")
    filter_group.add_argument(
        "--package-prefix",
        default=None,
        help="Filter packages by prefix (e.g., 'AUTOSARTemplates::BswModuleTemplate')",
    )
    filter_group.add_argument(
        "--exclude-empty",
        action="store_true",
        help="Exclude packages with no classes from output",
    )

    # Information options
    info_group = parser.add_argument_group("Information Options")
    info_group.add_argument(
        "-v", "--verbose", action="store_true", help="Show detailed extraction progress"
    )
    info_group.add_argument(
        "--stats-only",
        action="store_true",
        help="Only show statistics without writing output file",
    )

    args = parser.parse_args()

    try:
        validate_and_run_extraction(args)
    except KeyboardInterrupt:
        print("\n\nExtraction cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def validate_and_run_extraction(args):
    """
    Validate inputs and execute extraction

    Args:
        args: Parsed command-line arguments
    """
    inputs = args.inputs

    # Check if any input is a directory
    is_dir_input = any(Path(inp).is_dir() for inp in inputs)

    if is_dir_input:
        if len(inputs) > 1:
            raise ValueError("Cannot mix directory and file inputs")
        pdf_paths = inputs[0]
    else:
        pdf_paths = inputs

    # Validate all inputs
    for inp in inputs:
        input_path = Path(inp)
        if not input_path.exists():
            raise FileNotFoundError(f"Input not found: {input_path}")
        if input_path.suffix.lower() != ".pdf" and not input_path.is_dir():
            raise ValueError(f"Input must be a PDF or directory: {input_path}")

    # Determine output path
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        if is_dir_input or (len(inputs) > 1 and args.merge):
            input_name = Path(inputs[0]).name if inputs else "output"
            ext = ".md" if args.format in ["markdown", "md"] else "_summary.txt"
            output_path = Path(input_name).with_suffix(ext)
        elif len(inputs) == 1:
            ext = ".md" if args.format in ["markdown", "md"] else "_summary.txt"
            output_path = Path(inputs[0]).with_suffix(ext)
        else:
            ext = ".md" if args.format in ["markdown", "md"] else "_summary.txt"
            output_path = Path("merged" + ext)

    # Determine format
    format_type = "markdown" if args.format in ["markdown", "md"] else "text"

    if args.verbose:
        print("=" * 70)
        print("AUTOSAR Package and Class Extraction")
        print("=" * 70)
        if is_dir_input:
            print(f"\nInput directory: {pdf_paths}")
        elif len(inputs) > 1:
            print(f"\nInput files: {len(inputs)} PDFs")
        else:
            print(f"\nInput file:    {inputs[0]}")
        print(f"Output file:   {output_path}")
        print(f"Output format: {format_type}")
        print(f"Extraction method: {args.method}")
        if args.merge:
            print(f"Merge mode:    enabled")
        if args.package_prefix:
            print(f"Package filter: {args.package_prefix}")
        print()

    # Perform extraction
    from ..core.converter import convert_pdf_to_text
    from ..extractor import extract_from_multiple_pdfs

    if len(inputs) == 1 and Path(inputs[0]).suffix.lower() == ".pdf" and not args.merge:
        if args.verbose:
            print("Step 1: Extracting text from PDF...")

        text = convert_pdf_to_text(str(inputs[0]), method=args.method)

        if args.verbose:
            print("Step 2: Extracting package and class information...")

        packages = extract_package_and_class_info(text)

        # Apply package filter if specified
        if args.package_prefix:
            filtered_packages = [
                pkg for pkg in packages if pkg.name.startswith(args.package_prefix)
            ]
            if args.verbose:
                print(
                    f"  Filtered from {len(packages)} to {len(filtered_packages)} packages"
                )
            packages = filtered_packages

        # Apply empty package filter if specified
        if args.exclude_empty:
            filtered_packages = [pkg for pkg in packages if pkg.total_classes > 0]
            if args.verbose:
                print(
                    f"  Removed {len(packages) - len(filtered_packages)} empty packages"
                )
            packages = filtered_packages

        # Calculate statistics
        total_packages = len(packages)
        total_classes = sum(pkg.total_classes for pkg in packages)

        # Display statistics
        print_statistics(packages, total_packages, total_classes, args.verbose)

        # If stats-only, return early
        if args.stats_only:
            return

        # Write output
        if args.verbose:
            print("\nStep 3: Writing output file...")

        if format_type == "markdown":
            tree = build_package_hierarchy(packages)
            write_markdown_hierarchy(tree, str(output_path), title=args.title)
        else:
            write_text_summary(packages, str(output_path))

        print(f"\n[OK] Output written to: {output_path}")
    else:
        if args.verbose:
            print("Extracting from multiple PDFs...")

        results = extract_from_multiple_pdfs(
            pdf_paths=pdf_paths,
            output_path=str(output_path),
            format=format_type,
            method=args.method,
            merge_output=args.merge,
        )

        if args.merge:
            if args.verbose:
                print("Merged extraction completed")
            print(f"\n[OK] Output written to: {output_path}")
        else:
            if args.verbose:
                print("\nExtraction completed for all files")
            print("\n" + "=" * 70)
            print("Summary by File")
            print("=" * 70)
            for pdf_file, stats in results.items():
                print(f"\n{Path(pdf_file).name}:")
                print(f"  Packages: {stats['total_packages']}")
                print(f"  Classes:   {stats['total_classes']}")


def print_statistics(packages, total_packages, total_classes, verbose=False):
    """
    Print extraction statistics

    Args:
        packages: List of Package objects
        total_packages: Total number of packages
        total_classes: Total number of classes
        verbose: Show detailed breakdown if True
    """
    print("\n" + "=" * 70)
    print("Extraction Statistics")
    print("=" * 70)
    print(f"\nTotal Packages: {total_packages}")
    print(f"Total Classes:   {total_classes}")

    if verbose and packages:
        print("\nDetailed Breakdown:")
        print("-" * 70)
        for pkg in sorted(packages, key=lambda p: p.name):
            print(f"  {pkg.name}")
            print(f"    {pkg.total_classes} classes")
            if pkg.total_classes <= 10:
                for cls in sorted(pkg.classes, key=lambda c: c.name):
                    abstract_mark = " (abstract)" if cls.abstract else ""
                    print(f"      - {cls.name}{abstract_mark}")
            else:
                sorted_classes = sorted(pkg.classes, key=lambda c: c.name)
                for cls in sorted_classes[:5]:
                    abstract_mark = " (abstract)" if cls.abstract else ""
                    print(f"      - {cls.name}{abstract_mark}")
                print(f"      ... and {len(sorted_classes) - 5} more classes")
            print()


if __name__ == "__main__":
    main()
