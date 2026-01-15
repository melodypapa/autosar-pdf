---
description: Review code for style, security, and lint issues
argument-hint: [file-or-directory-paths]
allowed-tools: Bash(ruff*), Bash(mypy*), Read, Grep
---

## Tool Outputs

**Ruff Linting:**
!`ruff check src/autosar_pdf2txt/ tests/`

**Type Checking:**
!`mypy src/autosar_pdf2txt/`

**Flake8 Checks:**
!`ruff check --select F src/autosar_pdf2txt/ tests/`

## Context

@CLAUDE.md

## Your Task

Perform a comprehensive code review of the specified files focusing on:

### 1. Code Style & Conventions
- Type hints on all functions/methods (parameters and returns)
- Google-style docstrings with Args/Returns/Raises sections
- Import organization: standard library → third-party → local
- Naming: snake_case (functions), PascalCase (classes), UPPER_CASE (constants)
- Error handling: ValueError for invalid args, try-except for I/O
- Two-tier API: functional + class-based implementations
- English comments; Chinese test docstrings

### 2. Security Vulnerabilities
- Command injection (os.system, subprocess without sanitization)
- SQL injection risks
- Path traversal (unsanitized file paths)
- Hardcoded credentials/secrets
- Insecure deserialization
- XSS in web-related code

### 3. Project-Specific Patterns
- Backend abstraction (pypdf/pdfplumber/fitz)
- Progress reporting with ProgressReporter class
- PDF processing error handling

## Output Format

Provide a structured review with:

**🔴 Critical Issues** (security, blocking bugs)
**🟡 Style & Convention Violations** (CLAUDE.md compliance)
**🟠 Type Safety Issues** (missing type hints, mypy errors)
**💡 Suggestions** (improvements, refactoring opportunities)

For each issue, include:
- File location (file:line)
- Severity level
- Description
- Suggested fix (with code example if applicable)
