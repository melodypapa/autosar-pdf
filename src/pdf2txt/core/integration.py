"""
Integrated conversion using class-based approach
"""

from .converter import PdfConverter
from .table import TableExtractor
from .cleaner import TextCleaner
from .markdown import MarkdownConverter
from typing import Union, Optional


class PdfConverterWithTables:
    """
    Integrated PDF converter with table extraction support.

    This class combines text conversion, table extraction,
    and format conversion into a unified workflow.
    """

    def __init__(
        self,
        text_cleaner: Optional[TextCleaner] = None,
        table_extractor: Optional[TableExtractor] = None,
        markdown_converter: Optional[MarkdownConverter] = None,
    ):
        """
        Initialize integrated PDF converter.

        Args:
            text_cleaner (Optional[TextCleaner]): Text cleaner instance
            table_extractor (Optional[TableExtractor]): Table extractor instance
            markdown_converter (Optional[MarkdownConverter]): Markdown converter instance
        """
        self.text_cleaner = text_cleaner or TextCleaner()
        self.table_extractor = table_extractor or TableExtractor(self.text_cleaner)
        self.markdown_converter = markdown_converter or MarkdownConverter(
            self.text_cleaner
        )
        self.pdf_converter = PdfConverter(method="pdfplumber")

    def convert(
        self,
        pdf_path: str,
        output_format: str = "markdown",
        page_range: Optional[list] = None,
        skip_header_lines: int = 0,
        skip_footer_lines: int = 0,
        include_tables: bool = True,
    ) -> dict:
        """
        Convert PDF to text with table extraction support.

        Args:
            pdf_path (str): Path to PDF file
            output_format (str): Output format ("markdown", "txt")
            page_range (Optional[list]): List of specific page numbers (0-indexed)
            skip_header_lines (int): Number of lines to skip at beginning
            skip_footer_lines (int): Number of lines to skip at end
            include_tables (bool): Whether to extract and format tables

        Returns:
            dict: Conversion result containing:
                - 'text': Text content
                - 'tables': List of extracted tables (if include_tables=True)
                - 'page_count': Total number of pages
                - 'pages_extracted': Number of pages processed
        """
        result = {"text": "", "tables": [], "page_count": 0, "pages_extracted": 0}

        # Extract basic text
        if page_range is None:
            text = self.pdf_converter.convert(
                pdf_path, skip_header_lines, skip_footer_lines
            )
        else:
            # For specific page range, use advanced conversion
            adv_result = self.pdf_converter.convert_advanced(
                pdf_path, page_range, False, skip_header_lines, skip_footer_lines
            )
            text = adv_result["text"]
            result["page_count"] = adv_result["page_count"]
            result["pages_extracted"] = adv_result["pages_extracted"]

        # Get page count if not already set
        if result["page_count"] == 0:
            result["page_count"] = PdfConverter.get_page_count(pdf_path)
            result["pages_extracted"] = (
                result["page_count"] if page_range is None else len(page_range)
            )

        # Extract tables if requested
        if include_tables:
            tables = self.table_extractor.extract(pdf_path, page_range)
            result["tables"] = tables

        # Format output
        if output_format == "markdown":
            cleaned_text = self.text_cleaner.clean(text)
            result["text"] = self.markdown_converter.convert(
                cleaned_text, preserve_structure=True
            )
        else:
            result["text"] = self.text_cleaner.clean(text)

        return result


def convert_pdf_with_tables(
    pdf_path: str,
    output_format: str = "markdown",
    page_range: Union[list, None] = None,
    skip_header_lines: int = 0,
    skip_footer_lines: int = 0,
    include_tables: bool = True,
) -> dict:
    """
    Convert PDF to text with table extraction support (backward compatibility function).

    Args:
        pdf_path (str): Path to PDF file
        output_format (str): Output format ("markdown", "txt")
        page_range (list, optional): List of specific page numbers
        skip_header_lines (int): Number of lines to skip at beginning
        skip_footer_lines (int): Number of lines to skip at end
        include_tables (bool): Whether to extract and format tables

    Returns:
        dict: Conversion result containing text and metadata
    """
    converter = PdfConverterWithTables()
    return converter.convert(
        pdf_path,
        output_format,
        page_range,
        skip_header_lines,
        skip_footer_lines,
        include_tables,
    )
