# 项目分析报告

## 项目概述

当前目录 `D:\workspace\pdf2txt` 是一个名为 "pdf2txt" 的 Python 项目，版本 0.1.0。该项目的目标是将 PDF 文件转换为文本格式，提供一个简单易用的命令行工具和 Python 库来实现 PDF 到文本的转换功能。

## 项目类型

这是一个使用 Python 开发的软件项目，专门用于处理 PDF 文件并将其转换为文本格式。项目提供了命令行工具和 Python API，支持从 PDF 文档中提取文本内容，并具备页眉页脚过滤等高级功能。

## 项目结构

```
D:\workspace\pdf2txt/
├── pdf2txt/                 # 主要包目录
│   ├── __init__.py         # 包初始化和API入口
│   ├── core.py             # 核心转换功能实现
│   ├── cli.py              # 命令行接口
│   └── utils.py            # 辅助函数工具
├── tests/                  # 测试目录
│   └── test_converter.py   # 转换功能测试
├── examples/               # 示例目录
│   ├── example_usage.py    # 使用示例
│   └── pdf/                # 示例PDF文件目录
│       ├── AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf
│       ├── AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.txt
│       ├── AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate_filtered.txt
│       ├── AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate_no_header_footer.txt
│       └── AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate_simple.txt
├── build/                  # 构建输出目录
├── pdf2txt.egg-info/       # 包信息目录
├── requirements.txt        # 项目依赖
├── setup.py                # 包配置
├── README.md               # 项目说明
└── IFLOW.md                # 项目上下文
```

## 当前状态

- ✅ 项目目录结构已建立，包含完整的 Python 包结构
- ✅ 包含核心源代码文件（core.py, cli.py, utils.py）
- ✅ 包含配置文件（requirements.txt, setup.py）
- ✅ 包含 README.md 项目说明文件
- ✅ 包含示例代码（examples/example_usage.py）
- ✅ 包含基本测试文件（tests/test_converter.py）
- ✅ 包含命令行接口实现
- ✅ 已配置控制台脚本入口点（pdf2txt 命令）
- ✅ 已包含示例 PDF 文件用于测试
- ✅ 已成功安装并测试命令行工具
- ✅ 已验证 PDF 转换功能正常工作
- ✅ 已添加页眉页脚过滤功能
- ✅ 已移除 CLI 中的方法选择参数（默认使用 pypdf2）
- ✅ 已生成多个不同处理方式的示例输出文件

## 技术栈

### 主要依赖库
- **pypdf** (>=4.0.0) - 主要的 PDF 处理库，用于文本提取和文档操作
- **pdfplumber** (>=0.9.0) - 替代的 PDF 处理库，特别适合提取表格和复杂布局
- **PyMuPDF (fitz)** - 用于获取 PDF 文件信息（在 utils.py 中使用）

### Python 版本要求
- Python 3.7 或更高版本（当前环境：Python 3.13.1）

## 核心功能

### 1. PDF 转文本转换
- 支持两种后端库：pypdf 和 pdfplumber
- 基本转换接口：`convert_pdf_to_text()`
- 高级转换接口：`convert_pdf_to_text_advanced()`（支持页面范围选择、图像信息提取）
- **页眉页脚过滤**：支持跳过每页开头的指定行数（页眉）和结尾的指定行数（页脚）

### 2. 辅助工具函数
- `validate_pdf_path()` - 验证 PDF 文件路径
- `sanitize_filename()` - 清理文件名中的非法字符
- `get_pdf_info()` - 获取 PDF 文件信息（大小、页数、元数据）
- `format_file_size()` - 格式化文件大小显示

### 3. 命令行接口
- 支持单文件和批量转换
- 支持指定输出文件/目录
- 支持选择转换方法（pypdf2 或 pdfplumber，通过 Python API）
- 支持指定页面范围
- 支持包含图像元数据
- 支持强制覆盖已存在文件
- **支持页眉页脚过滤**：通过 `--skip-header` 和 `--skip-footer` 参数
- 显示转换进度和结果信息

## 构建和运行

### 环境准备
- Python 3.7 或更高版本
- pip 包管理器

### 依赖安装
```bash
pip install -r requirements.txt
```

### 本地开发设置
```bash
# 克隆项目后安装为可编辑包
pip install -e .

# 或者直接安装所需库
pip install pypdf pdfplumber PyMuPDF
```

### 运行方式

#### 作为命令行工具
```bash
# 转换单个PDF文件
pdf2txt input.pdf

# 指定输出文件
pdf2txt input.pdf -o output.txt

# 跳过页眉页脚（例如跳过每页前3行和后2行）
pdf2txt input.pdf --skip-header 3 --skip-footer 2

# 仅转换特定页面 (例如第1、2、5页)
pdf2txt input.pdf -p "0,1,4"

# 转换目录中所有 PDF 文件
pdf2txt input_dir/ output_dir/

# 包含图像元数据信息
pdf2txt input.pdf --include-images

# 强制覆盖已存在文件
pdf2txt input.pdf -o output.txt -f

# 组合使用：跳过页眉页脚并指定页面范围
pdf2txt input.pdf --skip-header 3 --skip-footer 2 -p "0-5"
```

#### 作为 Python 库使用
```python
from pdf2txt import convert_pdf_to_text

# 转换PDF内容为文本
text = convert_pdf_to_text("input.pdf")
print(text)

# 使用特定方法转换
text = convert_pdf_to_text("input.pdf", method="pdfplumber")

# 跳过页眉页脚
text = convert_pdf_to_text(
    "input.pdf", 
    skip_header_lines=3,  # 跳过每页前3行
    skip_footer_lines=2   # 跳过每页后2行
)

# 高级转换（指定页面范围）
from pdf2txt.core import convert_pdf_to_text_advanced

result = convert_pdf_to_text_advanced(
    "input.pdf", 
    page_range=[0, 1, 2],  # 转换前3页
    include_images=True,
    skip_header_lines=3,
    skip_footer_lines=2
)
```

### 测试
```bash
# 运行所有测试
pytest tests/

# 运行单个测试文件
pytest tests/test_converter.py

# 显示详细输出
pytest tests/ -v
```

## 开发规范

### 代码注释
- 所有代码注释必须使用英文编写

### 测试
- 所有测试用例必须使用 pytest 框架实现
- 测试文件位于 `tests/` 目录

### 项目元信息
- 版本：0.1.0
- 作者：Melodypapa
- 邮箱：melodypapa@outlook.com
- 许可证：MIT

## 项目特性

### 已实现功能
- ✅ 基本的 PDF 到文本转换
- ✅ 多种后端支持（pypdf、pdfplumber）
- ✅ 命令行接口
- ✅ Python API
- ✅ 页面范围选择
- ✅ 批量文件处理
- ✅ 文件信息获取
- ✅ 完整的测试套件
- ✅ 使用示例和文档
- ✅ **页眉页脚过滤功能**（skip_header_lines 和 skip_footer_lines）
- ✅ 已修复 CLI 默认方法问题（从 pymupdf 改为 pypdf2）
- ✅ 已移除 CLI 中的方法选择参数（简化用户界面）
- ✅ 已验证转换功能正常工作
- ✅ 已生成多个示例输出文件展示不同处理方式

### API 导出
```python
from pdf2txt import (
    convert_pdf_to_text,
    convert_pdf_to_text_advanced,
    validate_pdf_path,
    sanitize_filename,
    get_pdf_info
)
```

### 最近更新
- **新增功能**：页眉页脚过滤
  - 在 `convert_pdf_to_text()` 函数中添加了 `skip_header_lines` 和 `skip_footer_lines` 参数
  - 在 `convert_pdf_to_text_advanced()` 函数中添加了相同的参数
  - CLI 中新增 `--skip-header` 和 `--skip-footer` 命令行参数
  - 两个后端库（pypdf 和 pdfplumber）都支持此功能

- **CLI 优化**：
  - 移除了 `-m/--method` 参数，简化命令行界面
  - 默认使用 pypdf2 作为后端库
  - 所有转换函数都支持页眉页脚过滤

- **示例文件**：
  - 添加了多个不同处理方式的示例输出文件：
    - `AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.txt` - 原始转换输出
    - `AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate_filtered.txt` - 过滤后的输出
    - `AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate_no_header_footer.txt` - 无页眉页脚的输出
    - `AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate_simple.txt` - 简化处理的输出

## 已知问题和解决方案

### CLI 默认方法问题（已解决）
- **问题**：CLI 默认使用 "pymupdf" 方法，但 core.py 只支持 "pypdf2" 和 "pdfplumber"
- **解决方案**：已移除 CLI 中的方法选择参数，直接使用 pypdf2 作为默认方法

## 待办事项

基于当前项目状态，以下是一些可能的改进方向：
- 添加更多 PDF 处理功能（如表格提取、图像提取）
- 优化文本提取的准确性
- 添加更多测试用例
- 支持更多 PDF 处理库（如 PyMuPDF 作为主要后端）
- 添加进度显示功能
- 支持输出格式化选项（如保留段落结构）
- 改进页眉页脚自动识别功能（基于模式匹配而非固定行数）
- 支持输出到不同格式（如 JSON、CSV）
- 添加 OCR 支持以处理扫描的 PDF
- 添加单元测试覆盖页眉页脚过滤功能