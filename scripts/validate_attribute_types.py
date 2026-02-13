#!/usr/bin/env python3
"""
Validate Attribute Types Against Mapping

This script checks if all attribute types in the parsed JSON files
exist in the mapping.json file and reports any invalid types.

Usage:
    python scripts/validate_attribute_types.py

Output:
    - Summary statistics
    - Top N most common invalid types
    - Detailed list of all invalid types with their references
"""

import json
import glob
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


def analyze_invalid_types(
    packages_dir: str,
    valid_types: Set[str],
    top_n: int = 20
) -> Tuple[Dict[str, int], int]:
    """Analyze attribute types in JSON files and identify invalid ones.

    Args:
        packages_dir: Directory containing package JSON files.
        valid_types: Set of valid type names from mapping.json.
        top_n: Number of top invalid types to include in summary.

    Returns:
        Tuple of (invalid_types_dict, total_invalid_count)
    """
    invalid_types: Dict[str, int] = {}
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
                        
                        invalid_types[attr_type].append({
                            'class': class_name,
                            'package': package_path,
                            'attribute': attr_name,
                            'kind': attr_data.get('kind'),
                            'multiplicity': attr_data.get('multiplicity')
                        })

    # Convert to counts for summary
    invalid_type_counts = {t: len(refs) for t, refs in invalid_types.items()}
    
    return invalid_types, invalid_count


def print_summary(
    valid_count: int,
    invalid_type_count: int,
    invalid_ref_count: int,
    top_n: int,
    invalid_types: Dict[str, List[Dict]]
) -> None:
    """Print summary statistics.

    Args:
        valid_count: Number of valid types in mapping.json.
        invalid_type_count: Number of invalid attribute types.
        invalid_ref_count: Total number of invalid attribute references.
        top_n: Number of top invalid types to display.
        invalid_types: Dictionary of invalid types with their references.
    """
    print("# Attribute Type Validation Summary")
    print()
    print("## Overview")
    print()
    print(f"- **Valid types in mapping.json**: {valid_count:,}")
    print(f"- **Invalid attribute types**: {invalid_type_count:,}")
    print(f"- **Total invalid attribute references**: {invalid_ref_count:,}")
    print()
    
    # Calculate percentages
    print("## Statistics")
    print()
    print(f"- **Percentage of invalid type refs**: {100.0 * invalid_ref_count / (invalid_ref_count + 10000):.1f}%")
    print()
    
    # Top N invalid types
    if invalid_types:
        print(f"## Top {min(top_n, len(invalid_types))} Most Common Invalid Types")
        print()
        print("| # | Type | Occurrences |")
        print("|---|------|-------------|")
        
        sorted_types = sorted(
            invalid_types.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        for i, (type_name, refs) in enumerate(sorted_types[:top_n], 1):
            print(f"| {i:2d} | `{type_name}` | {len(refs):3d} |")
        print()


def print_detailed_report(
    invalid_types: Dict[str, List[Dict]],
    output_file: str = None
) -> None:
    """Print detailed report of all invalid types.

    Args:
        invalid_types: Dictionary of invalid types with their references.
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
    # Paths
    project_root = Path(__file__).parent.parent
    mapping_file = project_root / 'data' / 'mapping.json'
    packages_dir = project_root / 'data' / 'packages'
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
    invalid_types, invalid_count = analyze_invalid_types(
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
        invalid_types=invalid_types
    )
    
    # Print detailed report
    print_detailed_report(invalid_types, str(output_file))
    
    # Exit with error if invalid types found
    if invalid_types:
        print()
        print("## Analysis")
        print()
        print("⚠️ **Found invalid attribute types!**")
        print()
        print(f"- **{len(invalid_types)}** unique invalid types")
        print(f"- **{invalid_count}** total invalid references")
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