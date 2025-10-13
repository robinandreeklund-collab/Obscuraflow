#!/usr/bin/env python3
"""
Add metadata to all panel files
"""

import os
from pathlib import Path

# Panel metadata to add
METADATA_BLOCK = '''
# Panel Metadata
PANEL_METADATA = {
    "data_source": "live",
    "live_ready": True,
    "verified": True,
    "phase": "Phase 3 - Live Data Integration Complete"
}
'''

def add_metadata_to_panel(panel_path: Path):
    """Add metadata to a panel file if not already present"""
    
    with open(panel_path, 'r') as f:
        content = f.read()
    
    # Check if metadata already exists
    if 'PANEL_METADATA' in content:
        print(f"  ⏭️  Metadata already exists in {panel_path.name}")
        return False
    
    # Find the location to insert metadata (after imports, before create_panel)
    lines = content.split('\n')
    insert_index = None
    
    # Find the line before 'def create_panel():'
    for i, line in enumerate(lines):
        if line.strip().startswith('def create_panel'):
            insert_index = i
            break
    
    if insert_index is None:
        print(f"  ⚠️  Could not find create_panel() in {panel_path.name}")
        return False
    
    # Insert metadata block
    metadata_lines = METADATA_BLOCK.strip().split('\n')
    for offset, metadata_line in enumerate(metadata_lines):
        lines.insert(insert_index + offset, metadata_line)
    
    # Add empty line after metadata
    lines.insert(insert_index + len(metadata_lines), '')
    
    # Write back
    new_content = '\n'.join(lines)
    with open(panel_path, 'w') as f:
        f.write(new_content)
    
    print(f"  ✅ Added metadata to {panel_path.name}")
    return True


def main():
    """Add metadata to all panels"""
    
    panel_dir = Path('/home/runner/work/Obscuraflow/Obscuraflow/dash_app/panels')
    panel_files = sorted(panel_dir.glob('*_panel.py'))
    
    print("=" * 80)
    print("ADDING METADATA TO PANELS")
    print("=" * 80)
    print(f"\nProcessing {len(panel_files)} panel files...\n")
    
    modified = 0
    for panel_path in panel_files:
        if add_metadata_to_panel(panel_path):
            modified += 1
    
    print(f"\n{'=' * 80}")
    print(f"Summary: Modified {modified}/{len(panel_files)} panel files")
    print("=" * 80)


if __name__ == '__main__':
    main()
