#!/usr/bin/env python
"""
Utility script to remove UTF-8 BOM from YAML configuration files.
Run this before committing or if you encounter BOM issues.
"""

import os
import glob

def remove_bom_from_yaml():
    """Remove UTF-8 BOM from all YAML files in the project."""
    yaml_files = glob.glob('*.yaml') + glob.glob('*.yml')
    
    removed_count = 0
    for file_path in yaml_files:
        with open(file_path, 'rb') as f:
            content = f.read()
        
        if content.startswith(b'\xef\xbb\xbf'):
            content = content[3:]
            with open(file_path, 'wb') as f:
                f.write(content)
            print(f"✓ BOM removed from {file_path}")
            removed_count += 1
        else:
            print(f"- No BOM found in {file_path}")
    
    return removed_count

if __name__ == '__main__':
    removed = remove_bom_from_yaml()
    if removed > 0:
        print(f"\nTotal files fixed: {removed}")
    else:
        print("\nNo BOM issues found!")
