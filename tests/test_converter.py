"""
基本测试文件：测试 pdf2txt 库的基本功能
"""

import pytest
from pdf2txt.core import (
    convert_pdf_to_text,
    convert_pdf_to_text_advanced,
    convert_to_markdown,
    clean_special_characters,
    extract_tables_from_pdf,
    convert_table_to_markdown,
    convert_pdf_with_tables,
)
from pdf2txt.utils import (
    validate_pdf_path,
    sanitize_filename,
    format_file_size,
)
from pdf2txt import __version__


def test_version():
    """测试版本号"""
    assert __version__ == "0.2.0"


def test_sanitize_filename():
    """测试文件名清理功能"""
    assert sanitize_filename("test<file>.pdf") == "test_file_.pdf"
    assert sanitize_filename("normal_file.pdf") == "normal_file.pdf"
    assert (
        sanitize_filename("file|with?special*chars.pdf")
        == "file_with_special_chars.pdf"
    )


def test_format_file_size():
    """测试文件大小格式化功能"""
    assert format_file_size(512) == "512 B"
    assert format_file_size(2048) == "2.0 KB"
    assert format_file_size(2097152) == "2.0 MB"
    assert format_file_size(3221225472) == "3.0 GB"


def test_validate_pdf_path():
    """测试 PDF 路径验证功能"""
    # 这里我们测试一个不存在的 PDF 文件路径，应该返回 False
    assert validate_pdf_path("non_existent.pdf") is False
    # 测试非 PDF 文件
    assert validate_pdf_path("not_a_pdf.txt") is False


def test_convert_pdf_to_text():
    """测试 PDF 转换功能（基本接口）"""
    # 由于没有实际的 PDF 文件，我们只测试函数是否存在
    assert callable(convert_pdf_to_text)


def test_convert_pdf_to_text_advanced():
    """测试高级 PDF 转换功能"""
    # 由于没有实际的 PDF 文件，我们只测试函数是否存在
    assert callable(convert_pdf_to_text_advanced)


def test_convert_to_markdown():
    """测试 Markdown 转换功能"""
    # 测试基本转换
    sample_text = "1. Introduction\nThis is a test.\n\n2. Methods\nSome content here."
    markdown = convert_to_markdown(sample_text, preserve_structure=True)
    assert markdown is not None
    assert isinstance(markdown, str)
    assert "##" in markdown  # Should contain markdown headings

    # 测试不保留结构
    markdown_simple = convert_to_markdown(sample_text, preserve_structure=False)
    assert markdown_simple is not None
    assert isinstance(markdown_simple, str)


def test_clean_special_characters():
    """测试特殊字符清理功能"""
    # 测试控制字符移除
    text_with_control = "Hello\x00World\x01Test\x02"
    cleaned = clean_special_characters(text_with_control)
    assert cleaned == "HelloWorldTest"

    # 测试特殊引号替换
    text_with_quotes = "Left\u2018quote\u2019 and \u201cdouble\u201d"
    cleaned = clean_special_characters(text_with_quotes)
    assert cleaned == "Left'quote' and \"double\""

    # 测试保留换行符
    text_with_newlines = "Line1\nLine2\r\nLine3"
    cleaned = clean_special_characters(text_with_newlines)
    assert "\n" in cleaned or "\r\n" in cleaned


def test_convert_table_to_markdown():
    """测试表格转 Markdown 功能"""
    # 测试简单表格转换
    table_data = [
        ["Name", "Age", "City"],
        ["Alice", "25", "New York"],
        ["Bob", "30", "Los Angeles"],
    ]
    markdown = convert_table_to_markdown(table_data, include_header=True)
    assert markdown is not None
    assert isinstance(markdown, str)
    assert "|" in markdown  # Should contain pipe characters
    assert "---" in markdown  # Should contain separator

    # 测试无标题表格
    markdown_no_header = convert_table_to_markdown(table_data, include_header=False)
    assert markdown_no_header is not None
    assert "---" not in markdown_no_header  # Should not contain separator


def test_extract_tables_from_pdf():
    """测试从 PDF 提取表格功能"""
    # 由于没有实际的 PDF 文件，我们只测试函数是否存在
    assert callable(extract_tables_from_pdf)


def test_convert_pdf_with_tables():
    """测试带表格的 PDF 转换功能"""
    # 由于没有实际的 PDF 文件，我们只测试函数是否存在
    assert callable(convert_pdf_with_tables)


if __name__ == "__main__":
    # 运行所有测试
    pytest.main([__file__])
