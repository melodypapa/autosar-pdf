#!/usr/bin/env python3
"""Bump the package version based on commit type following semantic versioning.

Usage:
    python scripts/bump_version.py <commit_type>

Commit Types:
    feat     - Increment MINOR version (0.1.0 -> 0.2.0)
    fix      - Increment PATCH version (0.1.0 -> 0.1.1)
    breaking - Increment MAJOR version (0.1.0 -> 1.0.0)
    docs     - No version bump (display current version)
    style    - No version bump (display current version)
    refactor - No version bump (display current version)
    test     - No version bump (display current version)
    chore    - No version bump (display current version)
"""

import re
import sys
from pathlib import Path


def get_current_version() -> str:
    """Get the current version from __init__.py.

    Returns:
        Current version string (e.g., "0.1.0")
    """
    init_file = Path(__file__).parent.parent / "src" / "autosar_pdf2txt" / "__init__.py"

    content = init_file.read_text(encoding="utf-8")

    # Match __version__ = "x.y.z"
    match = re.search(r'__version__\s*=\s*"([^"]+)"', content)
    if not match:
        print("[ERROR] Could not find __version__ in __init__.py", file=sys.stderr)
        sys.exit(1)

    return match.group(1)


def get_setup_py_version() -> str:
    """Get the current version from setup.py.

    Returns:
        Current version string (e.g., "0.1.0")
    """
    setup_file = Path(__file__).parent.parent / "setup.py"

    content = setup_file.read_text(encoding="utf-8")

    # Match version="x.y.z"
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if not match:
        print("[ERROR] Could not find version in setup.py", file=sys.stderr)
        sys.exit(1)

    return match.group(1)


def validate_versions() -> bool:
    """Validate that __init__.py and setup.py have the same version.

    Returns:
        True if versions match, False otherwise
    """
    init_version = get_current_version()
    setup_version = get_setup_py_version()

    if init_version != setup_version:
        print(f"[WARN] Version mismatch detected!", file=sys.stderr)
        print(f"[WARN] __init__.py has version: {init_version}", file=sys.stderr)
        print(f"[WARN] setup.py has version: {setup_version}", file=sys.stderr)
        print(f"[WARN] Using __init__.py version as source of truth", file=sys.stderr)
        return False

    return True


def update_version(new_version: str) -> None:
    """Update the version in both __init__.py and setup.py.

    Args:
        new_version: New version string (e.g., "0.2.0")
    """
    # Update __init__.py
    init_file = Path(__file__).parent.parent / "src" / "autosar_pdf2txt" / "__init__.py"

    content = init_file.read_text(encoding="utf-8")

    # Replace __version__ = "x.y.z" with new version
    new_content = re.sub(
        r'__version__\s*=\s*"([^"]+)"',
        f'__version__ = "{new_version}"',
        content,
    )

    init_file.write_text(new_content, encoding="utf-8")
    print(f"[INFO] Updated version to {new_version} in src/autosar_pdf2txt/__init__.py")

    # Update setup.py
    setup_file = Path(__file__).parent.parent / "setup.py"

    setup_content = setup_file.read_text(encoding="utf-8")

    # Replace version="x.y.z" with new version
    new_setup_content = re.sub(
        r'version\s*=\s*"([^"]+)"',
        f'version="{new_version}"',
        setup_content,
    )

    setup_file.write_text(new_setup_content, encoding="utf-8")
    print(f"[INFO] Updated version to {new_version} in setup.py")


def bump_version(commit_type: str) -> str:
    """Bump the version based on commit type.

    Args:
        commit_type: The commit type (feat, fix, breaking, etc.)

    Returns:
        The new version string
    """
    current_version = get_current_version()

    # Parse version string
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)", current_version)
    if not match:
        print(f"[ERROR] Invalid version format: {current_version}", file=sys.stderr)
        sys.exit(1)

    major, minor, patch = map(int, match.groups())

    # Determine version bump based on commit type
    if commit_type == "feat":
        # New feature - increment MINOR version
        minor += 1
        patch = 0
    elif commit_type == "fix":
        # Bug fix - increment PATCH version
        patch += 1
    elif commit_type == "breaking":
        # Breaking change - increment MAJOR version
        major += 1
        minor = 0
        patch = 0
    else:
        # No version bump needed
        print(f"[INFO] Commit type '{commit_type}' does not require version bump")
        print(f"[INFO] Current version: {current_version}")
        return current_version

    new_version = f"{major}.{minor}.{patch}"
    update_version(new_version)
    return new_version


def main() -> int:
    """Main entry point for version bumping."""
    if len(sys.argv) != 2:
        print("Usage: python scripts/bump_version.py <commit_type>", file=sys.stderr)
        print("\nCommit types:", file=sys.stderr)
        print("  feat     - Increment MINOR version (0.1.0 -> 0.2.0)", file=sys.stderr)
        print("  fix      - Increment PATCH version (0.1.0 -> 0.1.1)", file=sys.stderr)
        print("  breaking - Increment MAJOR version (0.1.0 -> 1.0.0)", file=sys.stderr)
        print("\nOther types (docs, style, refactor, test, chore): No version bump", file=sys.stderr)
        return 1

    commit_type = sys.argv[1].lower()

    # Validate commit type
    valid_types = ["feat", "fix", "breaking", "docs", "style", "refactor", "test", "chore"]
    if commit_type not in valid_types:
        print(f"[ERROR] Invalid commit type: {commit_type}", file=sys.stderr)
        print(f"[ERROR] Valid types: {', '.join(valid_types)}", file=sys.stderr)
        return 1

    # Validate that both files have the same version
    validate_versions()

    old_version = get_current_version()
    setup_version = get_setup_py_version()

    print(f"[INFO] Current version in __init__.py: {old_version}")
    print(f"[INFO] Current version in setup.py: {setup_version}")

    # Bump version
    new_version = bump_version(commit_type)

    if commit_type in ["feat", "fix", "breaking"]:
        print(f"[SUCCESS] Version bumped: {old_version} -> {new_version}")
        print(f"[INFO] Both files updated successfully")
    else:
        print(f"[INFO] Version unchanged: {new_version}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
