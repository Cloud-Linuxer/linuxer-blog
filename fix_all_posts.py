#!/usr/bin/env python3
"""
Fix all formatting issues in migrated posts
"""

import os
import re
from pathlib import Path

def fix_post(filepath):
    """Fix formatting issues in a single post"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Split front matter and body
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    front_matter = parts[1]
    body = parts[2]

    # Fix code blocks with \n escapes
    def fix_code_block(match):
        code = match.group(1)
        # Replace \n with actual newlines
        code = code.replace('\\n', '\n')
        return f'```\n{code}\n```'

    body = re.sub(r'```\n(.+?)\n```', fix_code_block, body, flags=re.DOTALL)

    # Fix standalone \n sequences
    body = re.sub(r'^\s*\\n\s*$', '', body, flags=re.MULTILINE)

    # Fix excessive blank lines
    body = re.sub(r'\n{4,}', '\n\n', body)

    # Fix list formatting - ensure proper spacing
    body = re.sub(r'\n(\d+\.|\*|-)\s+', r'\n\n\1 ', body)

    # Rebuild content
    fixed = f'---{front_matter}---{body}'

    # Only write if changed
    if fixed != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed)
        return True

    return False

def main():
    posts_dir = Path('content/posts')
    fixed_count = 0

    for filepath in posts_dir.glob('*.md'):
        if fix_post(filepath):
            fixed_count += 1
            print(f"Fixed: {filepath.name}")

    print(f"\n✓ Fixed {fixed_count} posts")

if __name__ == "__main__":
    main()
