"""
基本测试文件：测试 pdf2txt 库的基本功能
"""
import pytest
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pdf2txt.core import convert_pdf_to_text, convert_pdf_to_text_advanced
from pdf2txt.utils import validate_pdf_path, sanitize_filename, get_pdf_info, format_file_size
from pdf2txt import __version__


def test_version():
    """测试版本号"""
    assert __version__ == "0.1.0"


def test_sanitize_filename():
    """测试文件名清理功能"""
    assert sanitize_filename("test<file>.pdf") == "test_file_.pdf"
    assert sanitize_filename("normal_file.pdf") == "normal_file.pdf"
    assert sanitize_filename("file|with?special*chars.pdf") == "file_with_special_chars.pdf"


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


if __name__ == "__main__":
    # 运行所有测试
    pytest.main([__file__])