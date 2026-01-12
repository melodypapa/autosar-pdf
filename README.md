# pdf2txt

pdf2txt 是一个用于将 PDF 文件转换为文本格式的 Python 包。它提供了命令行工具和 Python API，支持多种 PDF 处理后端库。

## 功能特性

- 将单个或多个 PDF 文件转换为文本
- 支持多种 PDF 处理库（PyMuPDF、pdfplumber）
- 命令行界面，方便批量处理
- 支持指定页面范围提取
- 提供 Python API 用于程序化调用

## 安装

```bash
pip install -e .
```

或者直接安装所需依赖：

```bash
pip install PyMuPDF pdfplumber
```

## 使用方法

### 命令行使用

```bash
# 转换单个 PDF 文件
pdf2txt input.pdf

# 指定输出文件
pdf2txt input.pdf -o output.txt

# 使用 pdfplumber 作为后端库
pdf2txt input.pdf -m pdfplumber

# 仅转换特定页面 (例如第1、2、5页)
pdf2txt input.pdf -p "0,1,4"

# 转换目录中所有 PDF 文件
pdf2txt input_dir/ output_dir/

# 包含图像元数据信息
pdf2txt input.pdf --include-images
```

### Python API 使用

```python
from pdf2txt import convert_pdf_to_text

# 转换 PDF 为文本
text = convert_pdf_to_text("input.pdf")
print(text)

# 使用特定方法转换
text = convert_pdf_to_text("input.pdf", method="pdfplumber")

# 高级转换（指定页面范围）
from pdf2txt.core import convert_pdf_to_text_advanced

result = convert_pdf_to_text_advanced(
    "input.pdf", 
    page_range=[0, 1, 2],  # 转换前3页
    include_images=True
)
```

## 开发

### 项目结构

```
pdf2txt/
├── pdf2txt/                 # 主要包目录
│   ├── __init__.py         # 包初始化
│   ├── core.py             # 核心转换功能
│   ├── cli.py              # 命令行接口
│   └── utils.py            # 辅助函数
├── tests/                  # 测试目录
├── examples/               # 示例目录
├── requirements.txt        # 项目依赖
├── setup.py                # 包配置
└── IFLOW.md                # 项目上下文
```

### 运行测试

```bash
pip install pytest
pytest tests/
```

## 依赖库

- [PyMuPDF](https://pymupdf.readthedocs.io/) - 主要的 PDF 处理库
- [pdfplumber](https://github.com/jsvine/pdfplumber) - 用于替代的 PDF 处理库

## 许可证

MIT