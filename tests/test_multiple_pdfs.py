"""
测试多PDF文件提取功能
"""

import pytest
from pathlib import Path
from pdf2txt.extractor import extract_from_multiple_pdfs


def test_extract_from_multiple_pdfs_integration():
    """测试多PDF文件提取接口（集成测试）"""
    assert callable(extract_from_multiple_pdfs)


def test_extract_from_multiple_pdfs_with_files():
    """测试从多个PDF文件提取"""
    pdf_files = []
    for pdf_file in Path("examples").glob("*.pdf"):
        pdf_files.append(str(pdf_file))

    if len(pdf_files) >= 2:
        results = extract_from_multiple_pdfs(
            pdf_paths=pdf_files,
            output_path=None,
            format="markdown",
            method="pdfplumber",
            merge_output=False,
        )

        assert isinstance(results, dict)
        assert len(results) == len(pdf_files)
        for pdf_file, stats in results.items():
            assert "total_packages" in stats
            assert "total_classes" in stats
            assert stats["total_packages"] >= 0
            assert stats["total_classes"] >= 0
    else:
        pytest.skip("Not enough PDF files in examples directory")


def test_extract_from_multiple_pdfs_merged():
    """测试合并多个PDF文件提取结果"""
    pdf_files = []
    for pdf_file in Path("examples").glob("*.pdf"):
        pdf_files.append(str(pdf_file))

    if len(pdf_files) >= 2:
        results = extract_from_multiple_pdfs(
            pdf_paths=pdf_files,
            output_path=None,
            format="markdown",
            method="pdfplumber",
            merge_output=True,
        )

        assert isinstance(results, dict)
        assert "total_packages" in results
        assert "total_classes" in results
        assert results["total_packages"] >= 0
        assert results["total_classes"] >= 0
    else:
        pytest.skip("Not enough PDF files in examples directory")


def test_extract_from_multiple_pdfs_directory():
    """测试从目录提取所有PDF文件"""
    examples_dir = Path("examples")

    if examples_dir.exists():
        pdf_files = list(examples_dir.glob("*.pdf"))

        if len(pdf_files) >= 1:
            results = extract_from_multiple_pdfs(
                pdf_paths=str(examples_dir),
                output_path=None,
                format="text",
                method="pdfplumber",
                merge_output=False,
            )

            assert isinstance(results, dict)
            assert len(results) >= 1
        else:
            pytest.skip("No PDF files in examples directory")
    else:
        pytest.skip("examples directory does not exist")


def test_extract_from_multiple_pdfs_invalid_directory():
    """测试无效目录路径"""
    with pytest.raises(FileNotFoundError):
        extract_from_multiple_pdfs(
            pdf_paths="/nonexistent/directory",
            output_path=None,
            format="markdown",
            method="pdfplumber",
            merge_output=True,
        )


def test_extract_from_multiple_pdfs_invalid_format():
    """测试无效格式参数"""
    pdf_files = []
    for pdf_file in Path("examples").glob("*.pdf"):
        pdf_files.append(str(pdf_file))

    if len(pdf_files) >= 1:
        with pytest.raises(ValueError):
            extract_from_multiple_pdfs(
                pdf_paths=pdf_files,
                output_path=None,
                format="invalid_format",
                method="pdfplumber",
                merge_output=True,
            )
    else:
        pytest.skip("No PDF files in examples directory")
