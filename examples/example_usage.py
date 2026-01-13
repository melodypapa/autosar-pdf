"""
Example file: Demonstrates how to use the autosar_pdf2txt library
"""

from autosar_pdf2txt import (
    convert_pdf_to_text,
    convert_to_markdown,
    clean_special_characters,
    extract_tables_from_pdf,
    convert_table_to_markdown,
    convert_pdf_with_tables,
)
from autosar_pdf2txt.core import convert_pdf_to_text_advanced
from autosar_pdf2txt.utils import get_pdf_info


def example_usage():
    print("pdf2txt Usage Examples")
    print("=" * 30)

    # Example 1: Basic conversion
    print("\nExample 1: Basic conversion")
    try:
        # Note: Since there is no actual PDF file, this only demonstrates the API usage
        # text = convert_pdf_to_text("example.pdf")
        print("convert_pdf_to_text('example.pdf')  # Convert PDF to text")
        print("# Return value: Text content of the PDF file")
    except Exception as e:
        print(f"Example execution error: {e}")
        print("Note: This example requires an actual PDF file to run")

    # Example 2: Convert using different methods
    print("\nExample 2: Convert using different methods")
    print(
        "convert_pdf_to_text('example.pdf', method='pdfplumber')  # Use pdfplumber as backend"
    )

    # Example 3: Advanced conversion features
    print("\nExample 3: Advanced conversion features")
    print("result = convert_pdf_to_text_advanced(")
    print("    'example.pdf',")
    print("    page_range=[0, 1, 2],    # Convert first 3 pages")
    print("    include_images=True      # Include image information")
    print(")")
    print(
        "# Return value: Dictionary containing text, page count statistics, and image information"
    )

    # Example 4: Get PDF information
    print("\nExample 4: Get PDF file information")
    print("info = get_pdf_info('example.pdf')")
    print(
        "# Return value: Dictionary containing file size, page count, metadata, and other information"
    )

    # Example 5: Convert to markdown format
    print("\nExample 5: Convert to markdown format")
    print(
        "text = convert_pdf_to_text('example.pdf', skip_header_lines=3, skip_footer_lines=2)"
    )
    print("markdown_text = convert_to_markdown(text, preserve_structure=True)")
    print("# Return value: Markdown formatted text with headings and proper structure")

    # Example 6: Clean special characters
    print("\nExample 6: Clean special characters from text")
    print("text = convert_pdf_to_text('example.pdf')")
    print("cleaned_text = clean_special_characters(text)")
    print(
        "# Return value: Text with control characters and special symbols removed/replaced"
    )

    # Example 7: Extract tables from PDF
    print("\nExample 7: Extract tables from PDF")
    print("tables = extract_tables_from_pdf('example.pdf')")
    print(
        "# Return value: List of tables with metadata (page, table data, row count, col count)"
    )

    # Example 8: Convert table to Markdown
    print("\nExample 8: Convert table to Markdown format")
    print("table_data = [['Name', 'Age'], ['Alice', '25'], ['Bob', '30']]")
    print("markdown_table = convert_table_to_markdown(table_data, include_header=True)")
    print("# Return value: Markdown formatted table")

    # Example 9: Convert PDF with tables
    print("\nExample 9: Convert PDF with table extraction")
    print("result = convert_pdf_with_tables(")
    print("    'example.pdf',")
    print("    output_format='markdown',")
    print("    page_range=[0, 1, 2],")
    print("    include_tables=True")
    print(")")
    print("# Return value: Dictionary containing text, tables, and metadata")


if __name__ == "__main__":
    example_usage()
