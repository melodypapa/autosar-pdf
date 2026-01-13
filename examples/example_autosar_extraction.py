#!/usr/bin/env python
"""
Example: Extract AUTOSAR Package and Class Information

This script demonstrates how to use the pdf2txt.extractor module
to extract AUTOSAR package and class metadata from PDF specification
documents.
"""

from pathlib import Path
from pdf2txt.extractor import (
    extract_package_and_class_info,
    build_package_hierarchy,
    write_markdown_hierarchy,
    write_text_summary,
    extract_from_pdf,
)
from pdf2txt.core import convert_pdf_to_text


def example_1_basic_extraction():
    """
    Example 1: Basic extraction from already extracted text.
    Useful when you need to process text from multiple sources.
    """
    print("Example 1: Basic extraction from text\n")

    # Step 1: Extract text from PDF
    pdf_path = "examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf"
    text = convert_pdf_to_text(pdf_path, method="pdfplumber")

    # Step 2: Extract package and class information
    packages = extract_package_and_class_info(text)

    # Step 3: Display summary
    print(f"Found {len(packages)} packages")
    for pkg_name, classes in list(packages.items())[:3]:
        print(f"  {pkg_name}: {len(classes)} classes")
    print()


def example_2_hierarchical_markdown():
    """
    Example 2: Extract and write hierarchical markdown structure.
    Best for documentation and reference materials.
    """
    print("Example 2: Hierarchical markdown output\n")

    pdf_path = "examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf"
    output_path = "example_output/packages_hierarchy.md"

    # Create output directory
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Extract text
    text = convert_pdf_to_text(pdf_path, method="pdfplumber")
    packages = extract_package_and_class_info(text)

    # Build hierarchy and write markdown
    tree = build_package_hierarchy(packages)
    write_markdown_hierarchy(
        tree, output_path, title="AUTOSAR Package and Class Reference"
    )

    print(f"Written hierarchical markdown to: {output_path}")


def example_3_text_summary():
    """
    Example 3: Extract and write plain text summary.
    Good for quick reference and logging.
    """
    print("Example 3: Text summary output\n")

    pdf_path = "examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf"
    output_path = "example_output/packages_summary.txt"

    # Create output directory
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Extract text
    text = convert_pdf_to_text(pdf_path, method="pdfplumber")
    packages = extract_package_and_class_info(text)

    # Write summary
    write_text_summary(packages, output_path)

    print(f"Written text summary to: {output_path}")


def example_4_convenience_function():
    """
    Example 4: Use the convenience function extract_from_pdf.
    Simple one-liner for common use cases.
    """
    print("Example 4: Using convenience function\n")

    pdf_path = "examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf"
    output_path = "example_output/convenience_extract.md"

    # Create output directory
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Extract using convenience function
    stats = extract_from_pdf(
        pdf_path=pdf_path,
        output_path=output_path,
        format="markdown",
        method="pdfplumber",
    )

    print(
        f"Extracted {stats['total_classes']} classes from {stats['total_packages']} packages"
    )
    print(f"Output written to: {output_path}")


def example_5_cli_usage():
    """
    Example 5: Using autosar-extract CLI from command line.

    Command line usage:
    -------------------
    Basic extraction (markdown format):
        autosar-extract input.pdf

    Specify output file:
        autosar-extract input.pdf -o output.md

    Text format instead of markdown:
        autosar-extract input.pdf --format text

    Use different extraction method:
        autosar-extract input.pdf --method pypdf2

    Show verbose progress:
        autosar-extract input.pdf -v

    Filter packages by prefix:
        autosar-extract input.pdf --package-prefix AUTOSARTemplates::BswModuleTemplate

    Exclude empty packages:
        autosar-extract input.pdf --exclude-empty

    Show statistics only:
        autosar-extract input.pdf --stats-only

    Custom title:
        autosar-extract input.pdf --title "My Reference" -o custom.md
    """
    print("Example 5: autosar-extract CLI usage\n")
    print("See the function docstring for command-line examples.")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("AUTOSAR Package and Class Extraction Examples")
    print("=" * 60)
    print()

    # Run examples
    example_1_basic_extraction()
    example_2_hierarchical_markdown()
    example_3_text_summary()
    example_4_convenience_function()
    example_5_cli_usage()

    print("=" * 60)
    print("All examples completed!")
    print("Check the 'example_output/' directory for generated files.")
