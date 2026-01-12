"""
Core module for PDF to text conversion
"""
import PyPDF2
import pdfplumber
from typing import Union, List


def convert_pdf_to_text_pypdf2(pdf_path: str) -> str:
    """
    Convert PDF to text using PyPDF2
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
    return text


def convert_pdf_to_text_pdfplumber(pdf_path: str) -> str:
    """
    Convert PDF to text using pdfplumber
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def convert_pdf_to_text(pdf_path: str, method: str = "pypdf2") -> str:
    """
    Convert PDF to text using specified method
    
    Args:
        pdf_path (str): Path to the PDF file
        method (str): Method to use for conversion ("pypdf2" or "pdfplumber")
        
    Returns:
        str: Extracted text from the PDF
    """
    if method == "pypdf2":
        return convert_pdf_to_text_pypdf2(pdf_path)
    elif method == "pdfplumber":
        return convert_pdf_to_text_pdfplumber(pdf_path)
    else:
        raise ValueError(f"Unsupported method: {method}. Use 'pypdf2' or 'pdfplumber'.")


def convert_pdf_to_text_advanced(pdf_path: str, 
                                page_range: Union[List[int], None] = None,
                                include_images: bool = False) -> dict:
    """
    Advanced PDF to text conversion with additional options
    
    Args:
        pdf_path (str): Path to the PDF file
        page_range (List[int], optional): List of specific page numbers to extract (0-indexed)
        include_images (bool): Whether to extract image information as well (currently not implemented for PyPDF2)
        
    Returns:
        dict: Dictionary containing extracted text and additional information
    """
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        # If no page range specified, use all pages
        if page_range is None:
            page_range = list(range(len(pdf_reader.pages)))
        else:
            # Ensure page numbers are within valid range
            page_range = [p for p in page_range if 0 <= p < len(pdf_reader.pages)]
        
        result = {
            "text": "",
            "page_count": len(pdf_reader.pages),
            "pages_extracted": len(page_range),
            "images": [] if include_images else None
        }
        
        for page_num in page_range:
            page = pdf_reader.pages[page_num]
            result["text"] += page.extract_text() + "\n"
    
    return result
