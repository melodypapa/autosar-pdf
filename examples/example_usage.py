"""
示例文件：演示如何使用 pdf2txt 库
"""
from pdf2txt import convert_pdf_to_text
from pdf2txt.core import convert_pdf_to_text_advanced
from pdf2txt.utils import get_pdf_info


def example_usage():
    print("pdf2txt 使用示例")
    print("=" * 30)
    
    # 示例 1: 基本转换
    print("\n示例 1: 基本转换")
    try:
        # 注意：由于没有实际的 PDF 文件，这里只是展示 API 使用方式
        # text = convert_pdf_to_text("example.pdf")
        print("convert_pdf_to_text('example.pdf')  # 将 PDF 转换为文本")
        print("# 返回值: PDF 文件的文本内容")
    except Exception as e:
        print(f"示例执行出错: {e}")
        print("注意: 此示例需要一个实际的 PDF 文件才能运行")
    
    # 示例 2: 使用不同方法转换
    print("\n示例 2: 使用不同方法转换")
    print("convert_pdf_to_text('example.pdf', method='pdfplumber')  # 使用 pdfplumber 作为后端")
    
    # 示例 3: 高级转换功能
    print("\n示例 3: 高级转换功能")
    print("result = convert_pdf_to_text_advanced(")
    print("    'example.pdf',")
    print("    page_range=[0, 1, 2],    # 转换前3页")
    print("    include_images=True      # 包含图像信息")
    print(")")
    print("# 返回值: 包含文本、页数统计和图像信息的字典")
    
    # 示例 4: 获取 PDF 信息
    print("\n示例 4: 获取 PDF 文件信息")
    print("info = get_pdf_info('example.pdf')")
    print("# 返回值: 包含文件大小、页数、元数据等信息的字典")


if __name__ == "__main__":
    example_usage()
