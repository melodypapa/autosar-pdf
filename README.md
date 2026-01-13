# pdf2txt

pdf2txt 是一个用于将 PDF 文件转换为文本格式的 Python 包。它提供了命令行工具和 Python API，支持多种 PDF 处理后端库，并支持 Markdown 格式输出。

包含两个独立的命令行工具：
- **pdf2txt** - PDF 文本和表格转换工具
- **autosar-extract** - AUTOSAR 规范包和类信息提取工具

## 功能特性

### pdf2txt 工具
- 将单个或多个 PDF 文件转换为文本
- 支持多种 PDF 处理库（pypdf、pdfplumber）
- 命令行界面，方便批量处理
- 支持指定页面范围提取
- 提供 Python API 用于程序化调用
- **支持 Markdown 格式输出，自动识别标题和结构**
- 支持页眉页脚过滤功能
- **自动清理特殊字符和控制符号，提高输出可读性**
- **支持表格提取和 Markdown 表格格式转换**

### autosar-extract 工具
- **从 AUTOSAR 规范 PDF 中提取包和类信息**
- 支持层级 Markdown 和文本摘要两种输出格式
- 提供包过滤和统计功能
- 详细提取进度显示

## 安装

```bash
pip install -e .
```

或者直接安装所需依赖：

```bash
pip install pypdf pdfplumber
```

## 使用方法

### pdf2txt 工具 - PDF 转换

```bash
# 转换单个 PDF 文件
pdf2txt input.pdf

# 指定输出文件
pdf2txt input.pdf -o output.txt

# 仅转换特定页面 (例如第1、2、5页)
pdf2txt input.pdf -p "0,1,4"

# 转换目录中所有 PDF 文件
pdf2txt input_dir/ output_dir/

# 包含图像元数据信息
pdf2txt input.pdf --include-images

# 输出为 Markdown 格式
pdf2txt input.pdf --format markdown -o output.md

# 输出为 Markdown 格式并跳过页眉页脚
pdf2txt input.pdf --format md --skip-header 3 --skip-footer 2 -o output.md

# 禁用特殊字符清理（默认启用）
pdf2txt input.pdf --no-clean -o output.txt

# 提取表格并转换为 Markdown 格式
pdf2txt input.pdf --extract-tables --format markdown -o output.md

# 仅提取表格，不包含其他文本
pdf2txt input.pdf --tables-only --format markdown -o tables.md
```

### autosar-extract 工具 - AUTOSAR 信息提取

```bash
# 基本提取（Markdown 格式，层级结构）
autosar-extract autosar_spec.pdf

# 指定输出文件
autosar-extract autosar_spec.pdf -o packages.md

# 使用文本摘要格式
autosar-extract autosar_spec.pdf --format text -o summary.txt

# 使用 pypdf2 提取方法
autosar-extract autosar_spec.pdf --method pypdf2

# 过滤特定包（仅提取 BSW 模板包）
autosar-extract autosar_spec.pdf --package-prefix AUTOSARTemplates::BswModuleTemplate

# 排除空包
autosar-extract autosar_spec.pdf --exclude-empty

# 显示详细进度
autosar-extract autosar_spec.pdf -v

# 仅显示统计信息，不写入文件
autosar-extract autosar_spec.pdf --stats-only

# 自定义文档标题
autosar-extract autosar_spec.pdf --title "My AUTOSAR Reference" -o custom.md
```

### Python API 使用

```python
from autosar_pdf2txt import convert_pdf_to_text

# 转换 PDF 为文本
text = convert_pdf_to_text("input.pdf")
print(text)

# 使用特定方法转换
text = convert_pdf_to_text("input.pdf", method="pdfplumber")

# 高级转换（指定页面范围）
from autosar_pdf2txt.core import convert_pdf_to_text_advanced

result = convert_pdf_to_text_advanced(
    "input.pdf", 
    page_range=[0, 1, 2],  # 转换前3页
    include_images=True
)

# 转换为 Markdown 格式
from autosar_pdf2txt import convert_to_markdown

text = convert_pdf_to_text("input.pdf", skip_header_lines=3, skip_footer_lines=2)
markdown_text = convert_to_markdown(text, preserve_structure=True)

# 清理特殊字符
from autosar_pdf2txt import clean_special_characters

cleaned_text = clean_special_characters(text)

# 提取表格
from autosar_pdf2txt import extract_tables_from_pdf, convert_table_to_markdown, convert_pdf_with_tables

# 提取所有表格
tables = extract_tables_from_pdf("input.pdf")

# 转换表格为 Markdown 格式
markdown_table = convert_table_to_markdown(tables[0]['table'])

# 转换 PDF 并提取表格
result = convert_pdf_with_tables(
    "input.pdf",
    output_format="markdown",
    include_tables=True
)

# 提取 AUTOSAR 包和类信息
from autosar_pdf2txt import extract_from_pdf

stats = extract_from_pdf(
    pdf_path="autosar_spec.pdf",
    output_path="packages.md",
    format="markdown",
    method="pdfplumber"
)
print(f"Extracted {stats['total_classes']} classes from {stats['total_packages']} packages")

# 手动提取和处理
from autosar_pdf2txt import extract_package_and_class_info, build_package_hierarchy, write_markdown_hierarchy

text = convert_pdf_to_text("autosar_spec.pdf")
packages = extract_package_and_class_info(text)
tree = build_package_hierarchy(packages)
write_markdown_hierarchy(tree, "output.md", title="AUTOSAR Reference")
```

## 开发

### 项目结构

```
pdf2txt/
 ├── pdf2txt/                 # 主要包目录
 │   ├── __init__.py         # 主包导出
 │   ├── cli/                # CLI 模块
 │   │   ├── __init__.py
 │   │   ├── pdf2txt_cli.py    # PDF 转换 CLI
 │   │   └── autosar_cli.py    # AUTOSAR 提取 CLI
 │   ├── core/               # 核心转换模块
 │   │   ├── __init__.py
 │   │   ├── converter.py      # PDF 转换函数
 │   │   ├── table.py          # 表格提取和转换
 │   │   ├── cleaner.py        # 文本清理
 │   │   ├── markdown.py       # Markdown 格式转换
 │   │   └── integration.py    # 集成功能
 │   ├── extractor/           # AUTOSAR 提取模块
 │   │   ├── __init__.py
 │   │   ├── parser.py         # 解析文本
 │   │   ├── hierarchy.py     # 构建层级
 │   │   ├── writer.py         # 写入输出
 │   │   └── integration.py    # 集成功能
 │   └── utils.py            # 通用工具函数
 ├── tests/                  # 测试目录
 ├── examples/               # 示例目录
 ├── requirements.txt        # 项目依赖
 ├── setup.py                # 包配置和 CLI 入口点
 └── IFLOW.md                # 项目上下文
```

### 运行测试

```bash
pip install pytest
pytest tests/
```

## 依赖库

- [pypdf](https://pypdf.readthedocs.io/) - 主要的 PDF 处理库
- [pdfplumber](https://github.com/jsvine/pdfplumber) - 用于替代的 PDF 处理库，特别适合提取表格和复杂布局

## 许可证

MIT