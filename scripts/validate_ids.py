#!/usr/bin/env python3
"""Validate that all requirement and test IDs are unique."""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set


def extract_ids(file_path: Path) -> Dict[str, List[int]]:
    """Extract all requirement and test IDs from a file.

    Args:
        file_path: Path to the documentation file

    Returns:
        Dictionary mapping ID patterns to list of line numbers where they appear
    """
    ids: Dict[str, List[int]] = {}

    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Pattern for requirement IDs: SWR_<MODULE>_<NUMBER>
    req_pattern = re.compile(r"^#### (SWR_\w+_\d+)")

    # Pattern for unit test IDs: SWUT_<MODULE>_<NUMBER>
    test_pattern = re.compile(r"^#### (SWUT_\w+_\d+)")

    # Pattern for integration test IDs: SWIT_<NUMBER>
    itest_pattern = re.compile(r"^#### (SWIT_\d+)")

    for line_num, line in enumerate(lines, start=1):
        for match in req_pattern.finditer(line):
            req_id = match.group(1)
            if req_id not in ids:
                ids[req_id] = []
            ids[req_id].append(line_num)

        for match in test_pattern.finditer(line):
            test_id = match.group(1)
            if test_id not in ids:
                ids[test_id] = []
            ids[test_id].append(line_num)

        for match in itest_pattern.finditer(line):
            itest_id = match.group(1)
            if itest_id not in ids:
                ids[itest_id] = []
            ids[itest_id].append(line_num)

    return ids


def find_duplicates(ids: Dict[str, List[int]]) -> Dict[str, List[int]]:
    """Find IDs that appear more than once.

    Args:
        ids: Dictionary mapping IDs to line numbers

    Returns:
        Dictionary mapping duplicate IDs to their line numbers
    """
    return {id_: lines for id_, lines in ids.items() if len(lines) > 1}


def check_missing_sequence(ids: Dict[str, List[int]]) -> List[str]:
    """Check for gaps in ID sequences within each module.

    Args:
        ids: Dictionary mapping IDs to line numbers

    Returns:
        List of missing IDs
    """
    # Group by module
    modules: Dict[str, Set[int]] = {}

    for id_str in ids.keys():
        # Match SWR_<MODULE>_<NUMBER> or SWUT_<MODULE>_<NUMBER>
        match = re.match(r"^(SW[UT]_\w+)_(\d+)$", id_str)
        if match:
            module = match.group(1)
            number = int(match.group(2))

            if module not in modules:
                modules[module] = set()
            modules[module].add(number)

        # Match SWIT_<NUMBER> (integration tests)
        match_it = re.match(r"^(SWIT)_(\d+)$", id_str)
        if match_it:
            module = match_it.group(1)
            number = int(match_it.group(2))

            if module not in modules:
                modules[module] = set()
            modules[module].add(number)

    # Find gaps
    missing = []
    for module, numbers in modules.items():
        if numbers:
            min_num = min(numbers)
            max_num = max(numbers)

            for num in range(min_num, max_num + 1):
                if num not in numbers:
                    # Format with leading zeros for 5-digit numbers
                    missing.append(f"{module}_{num:05d}")

    return missing


def main() -> int:
    """Main entry point for ID validation."""
    docs_dir = Path(__file__).parent.parent / "docs"

    files_to_check = [
        docs_dir / "requirements" / "requirements.md",
        docs_dir / "test_cases" / "unit_tests.md",
        docs_dir / "test_cases" / "integration_tests.md",
    ]

    has_errors = False

    for file_path in files_to_check:
        if not file_path.exists():
            print(f"[WARN] {file_path} does not exist")
            continue

        print(f"\n[INFO] Checking {file_path.relative_to(docs_dir.parent)}...")

        ids = extract_ids(file_path)
        duplicates = find_duplicates(ids)
        missing = check_missing_sequence(ids)

        if duplicates:
            has_errors = True
            print(f"[ERROR] Found {len(duplicates)} duplicate ID(s):")
            for id_, lines in sorted(duplicates.items()):
                print(f"   {id_}: lines {', '.join(map(str, lines))}")
        else:
            print(f"[OK] No duplicate IDs found ({len(ids)} unique IDs)")

        if missing:
            print(f"[WARN] Found {len(missing)} gap(s) in sequence:")
            for missing_id in missing[:10]:  # Show first 10
                print(f"   {missing_id}")
            if len(missing) > 10:
                print(f"   ... and {len(missing) - 10} more")

    print("\n" + "=" * 70)

    if has_errors:
        print("[FAIL] Validation failed: Duplicate IDs found!")
        print("\nPlease fix duplicate IDs to ensure proper traceability.")
        print("Remember: All requirement and test IDs must be unique.")
        return 1
    else:
        print("[PASS] All IDs are unique!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
