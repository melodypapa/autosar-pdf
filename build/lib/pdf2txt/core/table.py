"""
Table extraction and conversion using class-based approach
"""

import pdfplumber
from typing import Union, List, Optional
from .cleaner import TextCleaner


class TableExtractor:
    """
    Table extractor class for extracting tables from PDF files.

    This class uses pdfplumber to extract tables from PDF documents
    and provides methods for table data processing and formatting.
    """

    def __init__(self, text_cleaner: Optional[TextCleaner] = None):
        """
        Initialize table extractor.

        Args:
            text_cleaner (Optional[TextCleaner]): Text cleaner instance for cleaning cell data
        """
        self.text_cleaner = text_cleaner or TextCleaner()

    def extract(
        self, pdf_path: str, page_range: Optional[List[int]] = None
    ) -> List[dict]:
        """
        Extract tables from PDF using pdfplumber.

        Args:
            pdf_path (str): Path to PDF file
            page_range (Optional[List[int]]): List of specific page numbers (0-indexed)

        Returns:
            List[dict]: List of tables with metadata
                Each dict contains:
                - 'page': Page number where table was found
                - 'table': Table data as list of lists
                - 'row_count': Number of rows
                - 'col_count': Number of columns
        """
        tables = []

        with pdfplumber.open(pdf_path) as pdf:
            pages = pdf.pages

            if page_range is not None:
                pages = [pdf.pages[i] for i in page_range if 0 <= i < len(pdf.pages)]

            for page_num, page in enumerate(pages):
                page_tables = page.extract_tables()

                if page_tables:
                    for table in page_tables:
                        cleaned_table = self._clean_table(table)
                        tables.append(
                            {
                                "page": page_num,
                                "table": cleaned_table,
                                "row_count": len(cleaned_table),
                                "col_count": len(cleaned_table[0])
                                if cleaned_table
                                else 0,
                            }
                        )

        return tables

    def _clean_table(self, table: List[List[Optional[str]]]) -> List[List[str]]:
        """
        Clean table data by handling None values and special characters.

        Args:
            table (List[List[Optional[str]]): Raw table data

        Returns:
            List[List[str]]: Cleaned table data
        """
        cleaned_table = []

        for row in table:
            cleaned_row = []
            for cell in row:
                if cell is None:
                    cleaned_row.append("")
                else:
                    cleaned_cell = self.text_cleaner.clean(str(cell))
                    cleaned_row.append(cleaned_cell.strip())
            cleaned_table.append(cleaned_row)

        return cleaned_table


class TableConverter:
    """
    Table converter class for converting table data to various formats.

    This class provides methods to convert table data to Markdown and other formats.
    """

    def to_markdown(
        self, table_data: List[List[str]], include_header: bool = True
    ) -> str:
        """
        Convert table data to Markdown table format.

        Args:
            table_data (List[List[str]]): Table data as list of lists
            include_header (bool): Whether to treat first row as header

        Returns:
            str: Markdown formatted table
        """
        if not table_data:
            return ""

        markdown_lines = []

        for row_idx, row in enumerate(table_data):
            escaped_row = []
            for cell in row:
                escaped = self._escape_markdown_cell(str(cell))
                escaped_row.append(escaped)

            markdown_line = "| " + " | ".join(escaped_row) + " |"
            markdown_lines.append(markdown_line)

            if row_idx == 0 and include_header and len(table_data) > 1:
                separator = self._create_separator_row(row)
                markdown_lines.append(separator)

        return "\n".join(markdown_lines)

    @staticmethod
    def _escape_markdown_cell(cell: str) -> str:
        """
        Escape special markdown characters in table cells.

        Args:
            cell (str): Cell content to escape

        Returns:
            str: Escaped cell content
        """
        escaped = cell.replace("|", "\\|").replace("\n", " ")
        escaped = escaped.replace("*", "\\*").replace("_", "\\_")
        return escaped

    @staticmethod
    def _create_separator_row(row: List[str]) -> str:
        """
        Create separator row for Markdown table.

        Args:
            row (List[str]): Reference row for column widths

        Returns:
            str: Markdown separator line
        """
        col_widths = [len(str(cell)) for cell in row]
        separator = "| " + " | ".join(["-" * (w + 2) for w in col_widths]) + " |"
        return separator


def extract_tables_from_pdf(
    pdf_path: str, page_range: Union[list, None] = None
) -> List[dict]:
    """
    Extract tables from PDF (backward compatibility function).

    Args:
        pdf_path (str): Path to PDF file
        page_range (list, optional): List of specific page numbers

    Returns:
        List[dict]: List of tables with metadata
    """
    extractor = TableExtractor()
    return extractor.extract(pdf_path, page_range)


def convert_table_to_markdown(
    table_data: List[List[str]], include_header: bool = True
) -> str:
    """
    Convert table data to Markdown (backward compatibility function).

    Args:
        table_data (List[List[str]]): Table data as list of lists
        include_header (bool): Whether to treat first row as header

    Returns:
        str: Markdown formatted table
    """
    converter = TableConverter()
    return converter.to_markdown(table_data, include_header)
