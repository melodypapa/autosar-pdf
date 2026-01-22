#!/usr/bin/env python3
"""Validate markdown files with extracted table images.

This script:
1. Calls autosar-extract to generate class markdown files and hierarchy from PDFs
2. Calls autosar-extract-table to extract all tables from the same PDFs
3. Extracts class names from the class hierarchy markdown file
4. Extracts class names from table images using OCR
5. Compares class names between hierarchy and tables to validate extraction
6. Generates a markdown report with validation results

Usage:
    python scripts/validate_with_jpg.py <pdf_file_or_dir> [output_dir]

Examples:
    # Validate a single PDF (uses default output: data)
    python scripts/validate_with_jpg.py examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf

    # Validate all PDFs in a directory (uses default output: data)
    python scripts/validate_with_jpg.py examples/pdf/

    # Specify custom output directory
    python scripts/validate_with_jpg.py examples/pdf/ data/custom_output/

Note:
    OCR functionality requires pytesseract and pillow:
    pip install pytesseract pillow
    Tesseract binary is also required:
    - macOS: brew install tesseract
    - Ubuntu/Debian: sudo apt-get install tesseract-ocr
    - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
"""

import argparse
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration.

    Args:
        verbose: Enable verbose logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
    )


def run_command(cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command.

    Args:
        cmd: Command to run as a list of strings
        check: Whether to raise an exception on non-zero exit code

    Returns:
        Completed process result
    """
    logging.debug(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        logging.debug(result.stdout)
    if result.stderr:
        logging.debug(result.stderr)
    if check and result.returncode != 0:
        logging.error(f"Command failed with exit code {result.returncode}")
        logging.error(f"Command: {' '.join(cmd)}")
        if result.stderr:
            logging.error(f"Error output: {result.stderr}")
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result


def collect_pdf_files(input_path: Path) -> List[Path]:
    """Collect PDF files from input path.

    Args:
        input_path: Path to PDF file or directory

    Returns:
        List of PDF file paths
    """
    if not input_path.exists():
        logging.error(f"Path not found: {input_path}")
        sys.exit(1)

    if input_path.is_file():
        if input_path.suffix.lower() != ".pdf":
            logging.error(f"Not a PDF file: {input_path}")
            sys.exit(1)
        return [input_path]
    elif input_path.is_dir():
        pdf_files = sorted(input_path.glob("*.pdf"))
        if not pdf_files:
            logging.error(f"No PDF files found in directory: {input_path}")
            sys.exit(1)
        logging.info(f"Found {len(pdf_files)} PDF file(s) in {input_path}")
        return pdf_files
    else:
        logging.error(f"Not a file or directory: {input_path}")
        sys.exit(1)


def generate_markdown_files(pdf_files: List[Path], output_dir: Path, include_class_details: bool = True) -> None:
    """Generate markdown files using autosar-extract.

    Args:
        pdf_files: List of PDF file paths
        output_dir: Output directory for markdown files
        include_class_details: Whether to generate individual class files
    """
    logging.info("Generating markdown files with autosar-extract...")

    output_file = output_dir / "autosar_models.md"
    cmd = [
        "autosar-extract",
        "-o", str(output_file),
        "--include-class-details",
        "--include-class-hierarchy",
    ]

    cmd.extend([str(pdf) for pdf in pdf_files])

    try:
        run_command(cmd)
        logging.info(f"Markdown files generated in {output_dir}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to generate markdown files: {e}")
        sys.exit(1)


def extract_table_images(pdf_files: List[Path], output_dir: Path) -> None:
    """Extract table images using autosar-extract-table.

    Args:
        pdf_files: List of PDF file paths
        output_dir: Output directory for table images
    """
    logging.info("Extracting table images with autosar-extract-table...")

    tables_dir = output_dir / "tables"
    cmd = [
        "autosar-extract-table",
        "-o", str(tables_dir),
    ]

    cmd.extend([str(pdf) for pdf in pdf_files])

    try:
        run_command(cmd)
        logging.info(f"Table images extracted to {tables_dir}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to extract table images: {e}")
        sys.exit(1)


def find_markdown_files(output_dir: Path) -> List[Path]:
    """Find all markdown files in output directory.

    Args:
        output_dir: Output directory

    Returns:
        List of markdown file paths
    """
    markdown_files = list(output_dir.rglob("*.md"))
    # Exclude the main output file (if it exists)
    markdown_files = [f for f in markdown_files if f.parent != output_dir]
    logging.debug(f"Found {len(markdown_files)} markdown files")
    return markdown_files


def find_table_images(tables_dir: Path) -> List[Path]:
    """Find all table image files in tables directory.

    Args:
        tables_dir: Tables directory

    Returns:
        List of table image paths
    """
    table_images = list(tables_dir.glob("*.png"))
    logging.debug(f"Found {len(table_images)} table images")
    return table_images


def parse_markdown_for_classes(markdown_file: Path) -> List[str]:
    """Parse markdown file to extract class names.

    Args:
        markdown_file: Path to markdown file

    Returns:
        List of class names found in the file
    """
    content = markdown_file.read_text(encoding="utf-8")
    classes = []

    # Look for class names in markdown headers (## ClassName)
    import re
    for line in content.split("\n"):
        match = re.match(r"^##\s+(.+?)(?:\s+\(abstract\))?$", line)
        if match:
            class_name = match.group(1).strip()
            classes.append(class_name)

    return classes


def parse_hierarchy_for_classes(hierarchy_file: Path) -> List[str]:
    """Parse class hierarchy markdown file to extract class names.

    Args:
        hierarchy_file: Path to class hierarchy markdown file

    Returns:
        List of class names found in the hierarchy
    """
    content = hierarchy_file.read_text(encoding="utf-8")
    classes = []

    # Look for class names in the hierarchy (lines with asterisks and indentation)
    # Classes are leaf nodes (items without children) at level 3+ (6+ spaces before *)
    import re
    lines = content.split("\n")

    for i, line in enumerate(lines):
        # Match lines with asterisks that look like class definitions
        # Classes have 3 or more levels of indentation (6+ spaces before *)
        match = re.match(r"^\s{6,}\*\s+(.+?)$", line)
        if match:
            class_name = match.group(1).strip()
            # Check if this is a leaf node (next line has less indentation or is empty)
            is_leaf = True
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                next_match = re.match(r"^(\s*)\*", next_line)
                if next_match:
                    next_indent = len(next_match.group(1))
                    current_indent = len(re.match(r"^(\s*)\*", line).group(1))
                    # If next line has more indentation, this is a package (not a leaf)
                    if next_indent > current_indent:
                        is_leaf = False

            if is_leaf and class_name:
                classes.append(class_name)

    return classes


def check_and_install_ocr_packages() -> bool:
    """Check if OCR packages and tesseract binary are installed.

    Returns:
        True if packages are available, False otherwise
    """
    # Check Python packages
    try:
        import PIL
        import pytesseract
    except ImportError:
        logging.warning("OCR packages not found. Attempting to install...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "pytesseract", "pillow"],
                check=True,
                capture_output=True
            )
            logging.info("Successfully installed pytesseract and pillow")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install OCR packages: {e}")
            logging.error("Please install manually: pip install pytesseract pillow")
            return False

    # Check tesseract binary
    try:
        import shutil
        tesseract_path = shutil.which("tesseract")
        if not tesseract_path:
            logging.warning("tesseract binary not found in PATH")
            logging.warning("OCR functionality will be limited")
            logging.warning("To install tesseract:")
            logging.warning("  macOS: brew install tesseract")
            logging.warning("  Ubuntu/Debian: sudo apt-get install tesseract-ocr")
            logging.warning("  Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
            return False
        logging.info(f"Found tesseract at: {tesseract_path}")
        return True
    except Exception as e:
        logging.warning(f"Failed to check tesseract: {e}")
        return False


def extract_class_name_from_image(image_path: Path) -> Optional[str]:
    """Extract class name from a table image using OCR.

    Args:
        image_path: Path to the table image

    Returns:
        Extracted class name or None if extraction failed
    """
    try:
        from PIL import Image
        import pytesseract

        # Open the image
        img = Image.open(image_path)

        # Extract text using OCR
        text = pytesseract.image_to_string(img)

        # Look for class name patterns in the extracted text
        # Class names typically appear at the beginning of the text
        lines = text.strip().split("\n")
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and len(line) > 2 and not line.startswith("Attribute"):
                # Filter out common non-class text
                if line not in ["Element", "SizeProfile", "Note", "Type", "Mult.", "Kind"]:
                    return line

        return None
    except ImportError:
        logging.warning(f"OCR libraries not available. Install with: pip install pytesseract pillow")
        return None
    except Exception as e:
        logging.warning(f"Failed to extract class name from {image_path.name}: {e}")
        return None


def validate_markdown_with_tables(markdown_files: List[Path], table_images: List[Path], hierarchy_file: Path, ocr_available: bool) -> Tuple[int, int, List[str], List[str], List[str], set, set, set]:
    """Validate markdown files against table images.

    Args:
        markdown_files: List of markdown file paths
        table_images: List of table image paths
        hierarchy_file: Path to class hierarchy markdown file
        ocr_available: Whether OCR functionality is available

    Returns:
        Tuple of (total_classes, total_tables, validation_messages, hierarchy_classes, table_classes, matching_classes, missing_in_tables, missing_in_hierarchy)
    """
    total_classes = 0
    total_tables = len(table_images)
    validation_messages = []

    logging.info("Validating markdown files with table images...")

    # Extract class names from hierarchy file
    hierarchy_classes = parse_hierarchy_for_classes(hierarchy_file)
    logging.info(f"Found {len(hierarchy_classes)} classes in hierarchy file")

    # Extract class names from table images (only if OCR is available)
    table_classes = []
    if ocr_available:
        # Skip OCR if there are too many tables (likely includes UML diagrams)
        if len(table_images) > 150:
            logging.warning(f"Too many table images ({len(table_images)}). Skipping OCR to avoid performance issues.")
            logging.warning("This likely includes UML diagrams and other non-class tables.")
        else:
            for img_path in table_images:
                class_name = extract_class_name_from_image(img_path)
                if class_name:
                    table_classes.append(class_name)
                    logging.debug(f"{img_path.name}: {class_name}")
            logging.info(f"Extracted {len(table_classes)} class names from table images")
    else:
        logging.info("Skipping OCR extraction (tesseract not available)")

    # Compare class names
    hierarchy_set = set(hierarchy_classes)
    table_set = set(table_classes)

    matching_classes = hierarchy_set & table_set
    missing_in_tables = hierarchy_set - table_set
    missing_in_hierarchy = table_set - hierarchy_set

    validation_messages.append(f"Total markdown files: {len(markdown_files)}")
    validation_messages.append(f"Total classes in hierarchy: {len(hierarchy_classes)}")
    validation_messages.append(f"Total table images: {total_tables}")
    validation_messages.append(f"Classes extracted from tables: {len(table_classes)}")

    # Compare total table images with markdown class files
    if len(markdown_files) == total_tables:
        validation_messages.append(f"[SUCCESS] Number of markdown files ({len(markdown_files)}) matches number of table images ({total_tables})")
    else:
        validation_messages.append(f"[WARNING] Mismatch: {len(markdown_files)} markdown files vs {total_tables} table images (difference: {abs(len(markdown_files) - total_tables)})")

    if matching_classes:
        validation_messages.append(f"Matching classes: {len(matching_classes)}")
        if len(matching_classes) < 20:  # Only list if not too many
            validation_messages.append(f"  {', '.join(sorted(matching_classes))}")

    if missing_in_tables:
        validation_messages.append(f"[WARNING] Classes in hierarchy but not found in tables: {len(missing_in_tables)}")
        if len(missing_in_tables) <= 10:  # Only list if not too many
            validation_messages.append(f"  {', '.join(sorted(missing_in_tables))}")

    if missing_in_hierarchy:
        validation_messages.append(f"[WARNING] Classes in tables but not in hierarchy: {len(missing_in_hierarchy)}")
        if len(missing_in_hierarchy) <= 10:  # Only list if not too many
            validation_messages.append(f"  {', '.join(sorted(missing_in_hierarchy))}")

    # Overall validation result
    if len(missing_in_tables) == 0 and len(missing_in_hierarchy) == 0:
        validation_messages.append("[SUCCESS] All classes match between hierarchy and tables!")
    elif len(matching_classes) > 0:
        validation_messages.append(f"[INFO] {len(matching_classes)} classes match, but there are discrepancies")

    return len(hierarchy_classes), total_tables, validation_messages, hierarchy_classes, table_classes, matching_classes, missing_in_tables, missing_in_hierarchy


def generate_markdown_report(
    validation_messages: List[str],
    output_dir: Path,
    input_path: Path,
    hierarchy_classes: List[str],
    table_classes: List[str],
    matching_classes: set,
    missing_in_tables: set,
    missing_in_hierarchy: set,
) -> None:
    """Generate a markdown report with validation results.

    Args:
        validation_messages: List of validation messages
        output_dir: Output directory
        input_path: Input PDF file or directory
        hierarchy_classes: List of classes from hierarchy
        table_classes: List of classes extracted from tables
        matching_classes: Set of matching class names
        missing_in_tables: Set of classes in hierarchy but not in tables
        missing_in_hierarchy: Set of classes in tables but not in hierarchy
    """
    report_file = output_dir / "validation_report.md"

    from datetime import datetime

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# Validation Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Input:** `{input_path}`\n\n")
        f.write("---\n\n")

        f.write("## Summary\n\n")
        for msg in validation_messages:
            # Convert [SUCCESS], [WARNING], [INFO] to markdown format
            if "[SUCCESS]" in msg:
                msg = msg.replace("[SUCCESS]", "✅ **SUCCESS**")
            elif "[WARNING]" in msg:
                msg = msg.replace("[WARNING]", "⚠️ **WARNING**")
            elif "[INFO]" in msg:
                msg = msg.replace("[INFO]", "ℹ️ **INFO**")
            f.write(f"- {msg}\n")

        f.write("\n---\n\n")

        # Detailed comparison
        f.write("## Detailed Comparison\n\n")

        f.write(f"### Classes in Hierarchy ({len(hierarchy_classes)})\n\n")
        if len(hierarchy_classes) <= 50:
            for cls in sorted(hierarchy_classes):
                status = "✅" if cls in matching_classes else "❌"
                f.write(f"- {status} `{cls}`\n")
        else:
            f.write(f"*Showing first 50 of {len(hierarchy_classes)} classes*\n\n")
            for cls in sorted(hierarchy_classes)[:50]:
                status = "✅" if cls in matching_classes else "❌"
                f.write(f"- {status} `{cls}`\n")

        f.write("\n### Classes Extracted from Tables ({len(table_classes)})\n\n")
        if table_classes:
            for cls in sorted(table_classes):
                status = "✅" if cls in matching_classes else "❓"
                f.write(f"- {status} `{cls}`\n")
        else:
            f.write("*No classes extracted from tables (OCR libraries not installed)*\n")

        f.write("\n### Matching Classes ({len(matching_classes)})\n\n")
        if matching_classes:
            for cls in sorted(matching_classes):
                f.write(f"- ✅ `{cls}`\n")
        else:
            f.write("*No matching classes found*\n")

        f.write("\n### Classes in Hierarchy but Missing in Tables ({len(missing_in_tables)})\n\n")
        if missing_in_tables:
            for cls in sorted(missing_in_tables):
                f.write(f"- ❌ `{cls}`\n")
        else:
            f.write("*All classes in hierarchy found in tables*\n")

        f.write(f"\n### Classes in Tables but Missing in Hierarchy ({len(missing_in_hierarchy)})\n\n")
        if missing_in_hierarchy:
            for cls in sorted(missing_in_hierarchy):
                f.write(f"- ❓ `{cls}`\n")
        else:
            f.write("*All classes from tables found in hierarchy*\n")

    logging.info(f"Validation report generated: {report_file}")


def main() -> int:
    """Main entry point for validation script.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="Validate markdown files with extracted table images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate a single PDF (uses default output: data)
  python scripts/validate_with_jpg.py examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf

  # Validate all PDFs in a directory (uses default output: data)
  python scripts/validate_with_jpg.py examples/pdf/

  # Specify custom output directory
  python scripts/validate_with_jpg.py examples/pdf/ data/custom_output/

Note:
  OCR functionality requires pytesseract and pillow:
  pip install pytesseract pillow
        """
    )

    parser.add_argument(
        "input",
        type=str,
        help="Path to PDF file or directory containing PDFs"
    )

    parser.add_argument(
        "output",
        type=str,
        nargs="?",
        default="data",
        help="Output directory for markdown and table files (default: data)"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    setup_logging(args.verbose)

    # Check and install OCR packages if needed
    ocr_available = check_and_install_ocr_packages()

    input_path = Path(args.input)
    output_dir = Path(args.output)

    # Create output directory
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        logging.info(f"Output directory: {output_dir}")
    except Exception as e:
        logging.error(f"Failed to create output directory: {e}")
        return 1

    # Collect PDF files
    pdf_files = collect_pdf_files(input_path)

    # Generate markdown files
    generate_markdown_files(pdf_files, output_dir, include_class_details=True)

    # Extract table images
    extract_table_images(pdf_files, output_dir)

    # Find generated files
    markdown_files = find_markdown_files(output_dir)
    tables_dir = output_dir / "tables"
    table_images = find_table_images(tables_dir)
    hierarchy_file = output_dir / "autosar_models.md"

    # Validate
    total_classes, total_tables, validation_messages, hierarchy_classes, table_classes, matching_classes, missing_in_tables, missing_in_hierarchy = validate_markdown_with_tables(
        markdown_files, table_images, hierarchy_file, ocr_available
    )

    # Generate markdown report
    generate_markdown_report(
        validation_messages,
        output_dir,
        input_path,
        hierarchy_classes,
        table_classes,
        matching_classes,
        missing_in_tables,
        missing_in_hierarchy,
    )

    # Print validation summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    for msg in validation_messages:
        print(msg)
    print("=" * 70)

    logging.info(f"Validation complete. Results saved to: {output_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
