"""
Test coverage report generator
"""

import subprocess
import json
import sys
from pathlib import Path


def run_pytest_with_coverage():
    """
    Run pytest with coverage and generate JSON report.

    Returns:
        bool: True if successful, False otherwise
    """
    print("Running pytest with coverage...")
    cmd = [
        "pytest",
        "--cov=pdf2txt",
        "--cov-report=json",
        "--cov-report=term-missing",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode == 0


def parse_coverage_from_json():
    """
    Parse coverage from JSON report file.

    Returns:
        dict: Coverage data from JSON report
    """
    json_file = Path("coverage.json")
    if not json_file.exists():
        print(f"Error: Coverage JSON file not found: {json_file}")
        return None

    with open(json_file) as f:
        coverage_data = json.load(f)

    if "files" not in coverage_data:
        print("Error: 'files' key not found in coverage.json")
        return None

    result = {}
    files_dict = coverage_data["files"]

    for file_path in files_dict.keys():
        file_data = files_dict[file_path]
        filename = file_path.replace("pdf2txt/", "").replace("pdf2txt\\", "")
        percent_covered = file_data["summary"]["percent_covered"]
        missing_lines = file_data.get("missing_lines", [])

        result[filename] = {
            "coverage": round(percent_covered, 1),
            "covered_lines": file_data["summary"]["covered_lines"],
            "num_statements": file_data["summary"]["num_statements"],
            "missing_lines": len(missing_lines)
            if isinstance(missing_lines, list)
            else 0,
        }

    return result


def generate_markdown_report(coverage_data):
    """
    Generate markdown coverage report.

    Args:
        coverage_data (dict): Coverage data with filenames and coverage info

    Returns:
        str: Markdown formatted report
    """
    if not coverage_data:
        return "# Error: No coverage data available\n"

    lines = [
        "# Test Coverage Report\n\n",
        "## Overall Coverage Summary\n\n",
        "This report shows the test coverage for the pdf2txt package.\n\n",
        "## Coverage by File\n\n",
        "| File | Coverage | Covered Lines | Total Lines | Missing Lines |\n",
        "|------|----------|---------------|-------------|---------------|\n",
    ]

    sorted_files = sorted(coverage_data.keys())
    for filename in sorted_files:
        data = coverage_data[filename]
        coverage = data["coverage"]
        covered_lines = data["covered_lines"]
        num_statements = data["num_statements"]
        missing_lines = (
            data["missing_lines"]
            if isinstance(data["missing_lines"], int)
            else len(data["missing_lines"])
        )

        lines.append(
            f"| {filename} | {coverage}% | {covered_lines} | {num_statements} | {missing_lines} |\n"
        )

    lines.append("\n## Files with Incomplete Coverage\n\n")
    lines.append("| File | Coverage | Covered Lines | Total Lines | Missing Lines |\n")
    lines.append("|------|----------|---------------|-------------|---------------|\n")

    incomplete_files = [(f, d) for f, d in coverage_data.items() if d["coverage"] < 100]
    sorted_incomplete = sorted(
        incomplete_files, key=lambda x: x[1]["coverage"], reverse=True
    )

    for filename, data in sorted_incomplete:
        coverage = data["coverage"]
        covered_lines = data["covered_lines"]
        num_statements = data["num_statements"]
        missing_lines = (
            data["missing_lines"]
            if isinstance(data["missing_lines"], int)
            else len(data["missing_lines"])
        )

        lines.append(
            f"| {filename} | {coverage}% | {covered_lines} | {num_statements} | {missing_lines} |\n"
        )

    lines.append("\n## Summary\n\n")

    total_files = len(coverage_data)
    complete_files = len([f for f, d in coverage_data.items() if d["coverage"] == 100])
    incomplete_count = total_files - complete_files

    total_statements = sum(d["num_statements"] for d in coverage_data.values())
    total_covered = sum(d["covered_lines"] for d in coverage_data.values())
    overall_coverage = (
        (total_covered / total_statements * 100) if total_statements > 0 else 0
    )

    lines.append(f"- **Total Files**: {total_files}\n")
    lines.append(f"- **Fully Covered**: {complete_files}\n")
    lines.append(f"- **Partially Covered**: {incomplete_count}\n")
    lines.append(f"- **Overall Coverage**: {overall_coverage:.1f}%\n")
    lines.append(f"- **Total Lines**: {total_statements}\n")
    lines.append(f"- **Covered Lines**: {total_covered}\n\n")

    if incomplete_count > 0:
        lines.append("## Recommendations\n\n")
        lines.append(
            "Consider adding tests for the following files to improve coverage:\n\n"
        )
        for filename, _ in sorted_incomplete[:10]:
            lines.append(f"- `{filename}`\n")

        if len(sorted_incomplete) > 10:
            lines.append(f"\n... and {len(sorted_incomplete) - 10} more files\n")

    return "".join(lines)


def write_coverage_report():
    """
    Main function to run tests and generate coverage report.
    """
    print("=" * 70)
    print("Test Coverage Report Generator")
    print("=" * 70)
    print()

    success = run_pytest_with_coverage()

    if not success:
        print("\nError: Pytest failed")
        print("=" * 70)
        return

    print("\nParsing coverage data...")

    coverage_data = parse_coverage_from_json()

    if not coverage_data:
        print("Error: Could not parse coverage data")
        print("=" * 70)
        return

    markdown_report = generate_markdown_report(coverage_data)

    output_file = Path("..") / "coverage.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_report)

    print(f"\nCoverage report generated: {output_file}")
    print("=" * 70)


if __name__ == "__main__":
    write_coverage_report()
