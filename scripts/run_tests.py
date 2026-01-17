#!/usr/bin/env python3
"""Test runner script for autosar-pdf2txt.

This script provides convenient options to run tests and generate coverage reports:
- Run all tests
- Run only integration tests
- Run only unit tests
- Generate markdown coverage report

Usage:
    python scripts/run_tests.py --all
    python scripts/run_tests.py --integration
    python scripts/run_tests.py --unit
    python scripts/run_tests.py --coverage-report
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List


def _get_test_env() -> Dict[str, str]:
    """Get environment with PYTHONPATH configured for testing.

    Returns:
        Environment dictionary with PYTHONPATH set.
    """
    import os
    env = os.environ.copy()
    project_root = Path(__file__).parent.parent
    src_path = project_root / "src"
    env["PYTHONPATH"] = str(src_path) + os.pathsep + env.get("PYTHONPATH", "")
    return env


def run_command(cmd: List[str], capture: bool = True, env: Dict[str, str] | None = None) -> subprocess.CompletedProcess:
    """Run a command and return the result.

    Args:
        cmd: Command to run as a list of strings.
        capture: Whether to capture stdout and stderr.
        env: Optional environment variables to pass to subprocess.

    Returns:
        Completed process result.
    """
    print(f"\n{'='*70}")
    print(f"Running: {' '.join(cmd)}")
    print(f"{'='*70}\n")

    return subprocess.run(
        cmd,
        capture_output=capture,
        text=True,
        check=False,
        env=env
    )


def run_all_tests() -> int:
    """Run all tests.

    Returns:
        Exit code from pytest.
    """
    env = _get_test_env()

    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--cov=autosar_pdf2txt",
        "--cov-report=term",
        "--cov-report=json:cov_report.json"
    ]
    result = run_command(cmd, capture=False, env=env)
    return result.returncode


def run_integration_tests() -> int:
    """Run integration tests only.

    Returns:
        Exit code from pytest.
    """
    env = _get_test_env()

    cmd = [
        sys.executable, "-m", "pytest",
        "tests/integration/",
        "-v",
        "--cov=autosar_pdf2txt",
        "--cov-report=term",
        "--cov-report=json:cov_report.json"
    ]
    result = run_command(cmd, capture=False, env=env)
    return result.returncode


def run_unit_tests() -> int:
    """Run unit tests only.

    Returns:
        Exit code from pytest.
    """
    env = _get_test_env()

    cmd = [
        sys.executable, "-m", "pytest",
        "tests/models/",
        "tests/parser/",
        "tests/writer/",
        "tests/cli/",
        "-v",
        "--cov=autosar_pdf2txt",
        "--cov-report=term",
        "--cov-report=json:cov_report.json",
        "--cov-report=xml:coverage.xml"
    ]
    result = run_command(cmd, capture=False, env=env)
    return result.returncode


def parse_coverage_report(json_path: Path) -> Dict[str, Dict]:
    """Parse coverage JSON report.

    Args:
        json_path: Path to coverage JSON file.

    Returns:
        Dictionary with coverage data for each file.
    """
    if not json_path.exists():
        print(f"Error: Coverage report not found at {json_path}")
        print("Please run tests with coverage first:")
        print("  python scripts/run_tests.py --all")
        sys.exit(1)

    with open(json_path) as f:
        data = json.load(f)

    return data.get("files", {})


def generate_markdown_coverage_report(output_file: str | None = None) -> None:
    """Generate markdown coverage report and print to stdout or save to file.

    Args:
        output_file: Optional path to save the markdown report. If None, prints to stdout.

    The report includes:
    - Table of all source files with coverage
    - Table of files with less than 100% coverage
    """
    # Parse coverage JSON report
    cov_path = Path("cov_report.json")
    files_data = parse_coverage_report(cov_path)

    # Calculate coverage for each file
    file_coverage = []
    for file_path, data in files_data.items():
        # Convert to relative path from src/
        if "src/" in file_path:
            relative_path = file_path.split("src/autosar_pdf2txt/")[1]
        else:
            relative_path = file_path

        summary = data.get("summary", {})
        total = summary.get("num_statements", 0)
        covered = summary.get("covered_lines", 0)
        missing = summary.get("missing_lines", 0)
        coverage_percent = summary.get("percent_covered", 0.0)

        file_coverage.append({
            "path": relative_path,
            "statements": total,
            "covered": covered,
            "missing": missing,
            "percent": coverage_percent
        })

    # Sort by file path
    file_coverage.sort(key=lambda x: x["path"])

    # Build report lines
    lines = []
    lines.append("="*70)
    lines.append("COVERAGE REPORT - MARKDOWN FORMAT")
    lines.append("="*70)
    lines.append("")

    # Overall coverage
    total_statements = sum(f["statements"] for f in file_coverage)
    total_covered = sum(f["covered"] for f in file_coverage)
    total_missing = sum(f["missing"] for f in file_coverage)
    overall_percent = (total_covered / total_statements * 100) if total_statements > 0 else 0

    lines.append(f"## Overall Coverage: {overall_percent:.1f}%")
    lines.append("")
    lines.append(f"**Total Statements**: {total_statements}")
    lines.append("")
    lines.append(f"**Statements Covered**: {total_covered}")
    lines.append("")
    lines.append(f"**Statements Missing**: {total_missing}")
    lines.append("")

    # Table 1: All source files coverage
    lines.append("## All Source Files Coverage")
    lines.append("")
    lines.append("| Source File | Statements | Covered | Missing | Coverage |")
    lines.append("|-------------|-----------|---------|---------|----------|")

    for file in file_coverage:
        status = "✓" if file["percent"] == 100 else "✗"
        lines.append(f"| {status} `{file['path']}` | {file['statements']} | {file['covered']} | {file['missing']} | {file['percent']:.1f}% |")

    # Table 2: Files with less than 100% coverage
    incomplete_coverage = [f for f in file_coverage if f["percent"] < 100.0]

    if incomplete_coverage:
        lines.append("")
        lines.append("## Files with Less Than 100% Coverage")
        lines.append("")
        lines.append("| Source File | Coverage | Missing Statements |")
        lines.append("|-------------|----------|-------------------|")

        for file in incomplete_coverage:
            # Calculate percent missing
            missing_percent = 100.0 - file["percent"]
            lines.append(f"| `{file['path']}` | {file['percent']:.1f}% ({file['covered']}/{file['statements']}) | {file['missing']} stmts ({missing_percent:.1f}%) |")
    else:
        lines.append("")
        lines.append("## SUCCESS: All Files Have 100% Coverage!")

    lines.append("")
    lines.append("="*70)
    lines.append("")

    # Output report
    report_text = "\n".join(lines)

    if output_file:
        # Write to file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report_text, encoding="utf-8")
        print(f"Coverage report saved to: {output_file}")
    else:
        # Print to stdout
        print(report_text)

    # Clean up the JSON report file
    try:
        cov_path.unlink()
        print(f"Cleaned up temporary file: {cov_path}")
    except FileNotFoundError:
        # JSON file doesn't exist, skip cleanup
        pass
    except Exception as e:
        # Log warning but don't fail
        print(f"Warning: Could not delete temporary file {cov_path}: {e}")


def main() -> int:
    """Main entry point for the test runner script.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    parser = argparse.ArgumentParser(
        description="Test runner script for autosar-pdf2txt",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all tests with coverage
  python scripts/run_tests.py --all

  # Run only integration tests
  python scripts/run_tests.py --integration

  # Run only unit tests
  python scripts/run_tests.py --unit

Note: Coverage report is automatically generated after tests complete
and saved to scripts/report/coverage.md
        """
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all tests with coverage"
    )

    parser.add_argument(
        "--integration",
        action="store_true",
        help="Run integration tests only with coverage"
    )

    parser.add_argument(
        "--unit",
        action="store_true",
        help="Run unit tests only with coverage"
    )

    args = parser.parse_args()

    # Ensure we're in the project root directory
    project_root = Path(__file__).parent.parent
    import os
    os.chdir(project_root)

    # Handle mutually exclusive options
    if sum([args.all, args.integration, args.unit]) > 1:
        print("Error: Only one option can be specified at a time.")
        parser.print_help()
        return 1

    if not any([args.all, args.integration, args.unit]):
        parser.print_help()
        return 0

    # Execute requested action and generate coverage report
    if args.all:
        exit_code = run_all_tests()
    elif args.integration:
        exit_code = run_integration_tests()
    elif args.unit:
        exit_code = run_unit_tests()
    else:
        exit_code = 0

    # Generate coverage report after tests complete
    if exit_code == 0:
        print("\n" + "="*70)
        print("Generating coverage report...")
        print("="*70 + "\n")
        generate_markdown_coverage_report("scripts/report/coverage.md")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
