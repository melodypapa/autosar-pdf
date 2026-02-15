#!/usr/bin/env python3
"""
Validate Attribute Types Against Mapping

This script checks if all attribute types in the parsed JSON files
exist in the mapping.json file and reports any invalid types.

Usage:
    python scripts/validate_attribute_types.py [--fix]

Arguments:
    --fix    Automatically fix invalid types in JSON files:
            - Single suggestion: Replace with suggested type
            - Multiple/no suggestions: Wrap as any (type)

Output:
    - Summary statistics
    - Top N most common invalid types
    - Detailed list of all invalid types with their references
"""

import argparse
import json
import glob
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


def load_mapping_types(mapping_file: str) -> Set[str]:
    """Load all valid type names from mapping.json.

    Args:
        mapping_file: Path to mapping.json file.

    Returns:
        Set of valid type names.
    """
    with open(mapping_file, 'r') as f:
        data = json.load(f)
        return set(t['name'] for t in data['types'])


def find_type_suggestions(invalid_type: str, valid_types: Set[str]) -> List[str]:
    """Find potential valid type suggestions for an invalid type.

    Args:
        invalid_type: The invalid type name.
        valid_types: Set of valid type names.

    Returns:
        List of potential valid type suggestions.
    """
    suggestions = []
    invalid_lower = invalid_type.lower()
    
    for valid_type in valid_types:
        valid_lower = valid_type.lower()
        
        # Priority 1: Exact case-insensitive match
        if invalid_lower == valid_lower:
            return [valid_type]
        
        # Priority 2: Invalid type is prefix of valid type (e.g., "SwComponent" -> "SwComponentType")
        if valid_lower.startswith(invalid_lower):
            suggestions.append(valid_type)
        
        # Priority 3: Invalid type is suffix of valid type
        if valid_lower.endswith(invalid_lower):
            suggestions.append(valid_type)
        
        # Priority 4: Invalid type is contained in valid type
        if invalid_lower in valid_lower:
            suggestions.append(valid_type)
    
    # Remove duplicates and return
    return list(dict.fromkeys(suggestions))


def analyze_invalid_types(
    packages_dir: str,
    valid_types: Set[str],
    top_n: int = 20
) -> Tuple[Dict[str, List[Dict]], Dict[str, List[str]], int]:
    """Analyze attribute types in JSON files and identify invalid ones.

    Args:
        packages_dir: Directory containing package JSON files.
        valid_types: Set of valid type names from mapping.json.
        top_n: Number of top invalid types to include in summary.

    Returns:
        Tuple of (invalid_types_dict, suggestions_dict, total_invalid_count)
    """
    invalid_types: Dict[str, List[Dict]] = {}
    suggestions: Dict[str, List[str]] = {}
    invalid_count = 0

    for file in glob.glob(f'{packages_dir}/*.classes.json'):
        with open(file, 'r') as f:
            data = json.load(f)
            for cls in data.get('classes', []):
                class_name = cls.get('name', 'Unknown')
                package_path = cls.get('package', 'Unknown')
                
                for attr_name, attr_data in cls.get('attributes', {}).items():
                    attr_type = attr_data.get('type')
                    
                    if attr_type and attr_type not in valid_types:
                        invalid_count += 1
                        
                        if attr_type not in invalid_types:
                            invalid_types[attr_type] = []
                            # Find suggestions only once per invalid type
                            suggestions[attr_type] = find_type_suggestions(attr_type, valid_types)
                        
                        invalid_types[attr_type].append({
                            'class': class_name,
                            'package': package_path,
                            'attribute': attr_name,
                            'kind': attr_data.get('kind'),
                            'multiplicity': attr_data.get('multiplicity')
                        })
    
    return invalid_types, suggestions, invalid_count


def fix_invalid_types(
    packages_dir: str,
    suggestions: Dict[str, List[str]],
    dry_run: bool = False
) -> Tuple[int, int, int]:
    """Fix invalid types in JSON files.

    Args:
        packages_dir: Directory containing package JSON files.
        suggestions: Dictionary of suggestions for each invalid type.
        dry_run: If True, don't actually modify files, just report what would be done.

    Returns:
        Tuple of (files_modified, single_fixes, multi_fixes)
    """
    files_modified = 0
    single_fixes = 0
    multi_fixes = 0
    
    for file in glob.glob(f'{packages_dir}/*.classes.json'):
        with open(file, 'r') as f:
            data = json.load(f)
        
        file_changed = False
        
        for cls in data.get('classes', []):
            for attr_name, attr_data in cls.get('attributes', {}).items():
                attr_type = attr_data.get('type')
                
                if attr_type and attr_type in suggestions:
                    type_suggestions = suggestions[attr_type]
                    
                    if len(type_suggestions) == 1:
                        # Single suggestion: replace with suggested type
                        new_type = type_suggestions[0]
                        if not dry_run:
                            attr_data['type'] = new_type
                        file_changed = True
                        single_fixes += 1
                    else:
                        # Multiple or no suggestions: wrap as any (type)
                        new_type = f"any ({attr_type})"
                        if not dry_run:
                            attr_data['type'] = new_type
                        file_changed = True
                        multi_fixes += 1
        
        if file_changed and not dry_run:
            # Write modified file
            with open(file, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write('\n')  # Add trailing newline
            
            files_modified += 1
    
    return files_modified, single_fixes, multi_fixes


def print_summary(
    valid_count: int,
    invalid_type_count: int,
    invalid_ref_count: int,
    top_n: int,
    invalid_types: Dict[str, List[Dict]],
    suggestions: Dict[str, List[str]]
) -> None:
    """Print summary statistics.

    Args:
        valid_count: Number of valid types in mapping.json.
        invalid_type_count: Number of invalid attribute types.
        invalid_ref_count: Total number of invalid attribute references.
        top_n: Number of top invalid types to display.
        invalid_types: Dictionary of invalid types with their references.
        suggestions: Dictionary of suggestions for each invalid type.
    """
    print("# Attribute Type Validation Summary")
    print()
    print("## Overview")
    print()
    print(f"- **Valid types in mapping.json**: {valid_count:,}")
    print(f"- **Invalid attribute types**: {invalid_type_count:,}")
    print(f"- **Total invalid attribute references**: {invalid_ref_count:,}")
    print()
    
    # Calculate fixability statistics
    single_fix_count = sum(1 for s in suggestions.values() if len(s) == 1)
    multi_fix_count = sum(1 for s in suggestions.values() if len(s) != 1)
    
    print("## Fixability Analysis")
    print()
    if invalid_type_count > 0:
        print(f"- **Types with single suggestion**: {single_fix_count} ({100.0 * single_fix_count / invalid_type_count:.1f}%)")
        print(f"- **Types with multiple/no suggestions**: {multi_fix_count} ({100.0 * multi_fix_count / invalid_type_count:.1f}%)")
    else:
        print(f"- **Types with single suggestion**: {single_fix_count}")
        print(f"- **Types with multiple/no suggestions**: {multi_fix_count}")
    print()
    
    # Calculate percentages
    print("## Statistics")
    print()
    if invalid_ref_count > 0:
        print(f"- **Percentage of invalid type refs**: {100.0 * invalid_ref_count / (invalid_ref_count + 10000):.1f}%")
    else:
        print(f"- **Percentage of invalid type refs**: 0.0%")
    print()
    
    # Top N invalid types
    if invalid_types:
        print(f"## Top {min(top_n, len(invalid_types))} Most Common Invalid Types")
        print()
        print("| # | Type | Occurrences | Fixable |")
        print("|---|------|-------------|---------|")
        
        sorted_types = sorted(
            invalid_types.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        for i, (type_name, refs) in enumerate(sorted_types[:top_n], 1):
            type_suggestions = suggestions.get(type_name, [])
            fixable = "✅" if len(type_suggestions) == 1 else "⚠️"
            print(f"| {i:2d} | `{type_name}` | {len(refs):3d} | {fixable} |")
        print()


def print_detailed_report(
    invalid_types: Dict[str, List[Dict]],
    suggestions: Dict[str, List[str]],
    output_file: str = None
) -> None:
    """Print detailed report of all invalid types.

    Args:
        invalid_types: Dictionary of invalid types with their references.
        suggestions: Dictionary of suggestions for each invalid type.
        output_file: Optional file path to save detailed report (must be .md).
    """
    print("## Detailed Invalid Type Report")
    print()
    
    sorted_types = sorted(
        invalid_types.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )
    
    for type_name, refs in sorted_types:
        print(f"### `{type_name}` ({len(refs)} occurrences)")
        print()
        
        # Display suggestions
        type_suggestions = suggestions.get(type_name, [])
        if type_suggestions:
            if len(type_suggestions) == 1:
                print(f"**Suggestion**: `{type_name}` shall be corrected to `{type_suggestions[0]}`")
            else:
                print(f"**Potential types**: `{type_name}` may refer to:")
                for suggestion in type_suggestions:
                    print(f"  - `{suggestion}`")
                print(f"**Fix action**: `{type_name}` will be marked as `any ({type_name})`")
        else:
            print("**Suggestion**: No similar types found in mapping.json")
            print(f"**Fix action**: `{type_name}` will be marked as `any ({type_name})`")
        print()
        
        for ref in refs:
            print(f"- **{ref['class']}.{ref['attribute']}**")
            print(f"  - Package: `{ref['package']}`")
            print(f"  - Kind: `{ref['kind']}`, Multiplicity: `{ref['multiplicity']}`")
        print()
    
    if output_file:
        with open(output_file, 'w') as f:
            if invalid_types:
                f.write("# Invalid Attribute Types Report\n\n")
                f.write("## Overview\n\n")
                f.write(f"- **Total invalid types**: {len(invalid_types)}\n")
                f.write(f"- **Total invalid references**: {sum(len(refs) for refs in invalid_types.values())}\n\n")
                
                for type_name, refs in sorted_types:
                    f.write(f"### `{type_name}` ({len(refs)} occurrences)\n\n")
                    
                    # Write suggestions
                    type_suggestions = suggestions.get(type_name, [])
                    if type_suggestions:
                        if len(type_suggestions) == 1:
                            f.write(f"**Suggestion**: `{type_name}` shall be corrected to `{type_suggestions[0]}`\n\n")
                        else:
                            f.write(f"**Potential types**: `{type_name}` may refer to:\n\n")
                            for suggestion in type_suggestions:
                                f.write(f"- `{suggestion}`\n")
                            f.write(f"**Fix action**: `{type_name}` will be marked as `any ({type_name})`\n\n")
                    else:
                        f.write("**Suggestion**: No similar types found in mapping.json\n\n")
                        f.write(f"**Fix action**: `{type_name}` will be marked as `any ({type_name})`\n\n")
                    
                    for ref in refs:
                        f.write(f"- **{ref['class']}.{ref['attribute']}**\n")
                        f.write(f"  - Package: `{ref['package']}`\n")
                        f.write(f"  - Kind: `{ref['kind']}`, Multiplicity: `{ref['multiplicity']}`\n")
                    f.write("\n")
            else:
                f.write("# Invalid Attribute Types Report\n\n")
                f.write("## Overview\n\n")
                f.write("- **Total invalid types**: 0\n")
                f.write("- **Total invalid references**: 0\n\n")
                f.write("## ✅ Result\n\n")
                f.write("All attribute types are valid!\n")
        
        print(f"Detailed report saved to: {output_file}")


def main():
    """Main entry point."""
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Validate and optionally fix attribute types in JSON files"
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Automatically fix invalid types in JSON files'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be fixed without modifying files'
    )
    parser.add_argument(
        '--packages-dir',
        type=str,
        default=None,
        help='Path to directory containing package JSON files (default: data/packages)'
    )
    parser.add_argument(
        '--mapping-file',
        type=str,
        default=None,
        help='Path to mapping.json file (default: data/mapping.json)'
    )
    parser.add_argument(
        '--output-file',
        type=str,
        default=None,
        help='Path to output report file (default: scripts/report/invalid_attribute_types.md)'
    )
    args = parser.parse_args()
    
    # Paths
    project_root = Path(__file__).parent.parent
    
    # Use provided paths or defaults
    if args.packages_dir:
        packages_dir = Path(args.packages_dir)
    else:
        packages_dir = project_root / 'data' / 'packages'
    
    if args.mapping_file:
        mapping_file = Path(args.mapping_file)
    else:
        mapping_file = project_root / 'data' / 'mapping.json'
    
    if args.output_file:
        output_file = Path(args.output_file)
    else:
        output_file = project_root / 'scripts/report/invalid_attribute_types.md'
    
    # Validate paths exist
    if not mapping_file.exists():
        print(f"Error: mapping.json not found at {mapping_file}")
        sys.exit(1)
    
    if not packages_dir.exists():
        print(f"Error: packages directory not found at {packages_dir}")
        sys.exit(1)
    
    # Load valid types
    valid_types = load_mapping_types(str(mapping_file))
    
    # Analyze invalid types
    invalid_types, suggestions, invalid_count = analyze_invalid_types(
        str(packages_dir),
        valid_types,
        top_n=20
    )
    
    # Print summary
    print_summary(
        valid_count=len(valid_types),
        invalid_type_count=len(invalid_types),
        invalid_ref_count=invalid_count,
        top_n=20,
        invalid_types=invalid_types,
        suggestions=suggestions
    )
    
    # Print detailed report
    print_detailed_report(invalid_types, suggestions, str(output_file))
    
    # Handle fixing
    if args.fix or args.dry_run:
        if invalid_types:
            print()
            if args.dry_run:
                print("## Dry Run Mode")
                print()
                print("The following changes would be made:")
                print()
            
            files_modified, single_fixes, multi_fixes = fix_invalid_types(
                str(packages_dir),
                suggestions,
                dry_run=args.dry_run
            )
            
            if args.dry_run:
                print(f"- **Files that would be modified**: {files_modified}")
                print(f"- **Single fixes (automatic)**: {single_fixes}")
                print(f"- **Multi/no fixes (marked as any (type))**: {multi_fixes}")
            else:
                print("## Fix Applied")
                print()
                print(f"✅ **Successfully fixed invalid types in {files_modified} file(s)**")
                print()
                print(f"- **Single fixes applied**: {single_fixes}")
                print(f"- **Multi/no fixes marked**: {multi_fixes}")
            
            if not args.dry_run:
                print()
                print("To verify the fixes, run:")
                print("  python scripts/validate_attribute_types.py")
        else:
            print()
            print("## No Fixes Needed")
            print()
            print("All attribute types are valid!")
            sys.exit(0)
    elif invalid_types:
        print()
        print("## Analysis")
        print()
        print("⚠️ **Found invalid attribute types!**")
        print()
        print(f"- **{len(invalid_types)}** unique invalid types")
        print(f"- **{invalid_count}** total invalid references")
        print()
        print("### Fix Options")
        print()
        print("Run with `--fix` to automatically fix:")
        print("  python scripts/validate_attribute_types.py --fix")
        print()
        print("Run with `--dry-run` to preview changes:")
        print("  python scripts/validate_attribute_types.py --dry-run")
        print()
        print("### Important Notes")
        print()
        print("These types are **correctly parsed from the PDF** but do not exist in the AUTOSAR metamodel (mapping.json). They represent:")
        print()
        print("- **Abstract type references** used in the AUTOSAR specification")
        print("- **General concepts** that can refer to multiple concrete types")
        print("- **Semantic type hints** that provide context but aren't defined as separate classes")
        print()
        print("### Examples")
        print()
        print("- `SwComponent`: Can refer to either `SwComponentType` or `SwComponentPrototype`")
        print("- `SwcService`: General reference to a service within a software component")
        print("- `ParameterData`: Generic reference to parameter data (may be `ParameterDataPrototype`)")
        print()
        sys.exit(1)
    else:
        print()
        print("## ✅ Result")
        print()
        print("All attribute types are valid!")
        sys.exit(0)


if __name__ == '__main__':
    main()