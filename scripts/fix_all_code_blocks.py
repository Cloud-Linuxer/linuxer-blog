#!/usr/bin/env python3
import os
import re
import glob

def fix_code_blocks(content):
    """Fix all code block formatting issues"""
    lines = content.split('\n')
    fixed_lines = []
    in_code_block = False
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if we're starting a code block
        if line.strip().startswith('```'):
            # If there's text before the code block on the same line
            if not line.startswith('```'):
                # Split the line at the code block
                parts = line.split('```', 1)
                if parts[0].strip():
                    fixed_lines.append(parts[0].strip())

                # Start the code block on a new line
                if len(parts) > 1 and parts[1]:
                    # Check if there's content after ```
                    remaining = parts[1]
                    if remaining and not remaining.strip():
                        fixed_lines.append('```yaml')
                    elif 'apiVersion' in remaining or 'kind:' in remaining:
                        fixed_lines.append('```yaml')
                        fixed_lines.append(remaining)
                    else:
                        fixed_lines.append('```bash')
                        if remaining.strip():
                            fixed_lines.append(remaining)
                else:
                    fixed_lines.append('```yaml' if 'apiVersion' in ''.join(lines[i:i+3]) else '```bash')
            else:
                # Line starts with ```
                if line == '```':
                    # Check next few lines to determine language
                    next_content = '\n'.join(lines[i+1:min(i+4, len(lines))])
                    if 'apiVersion' in next_content or 'kind:' in next_content or 'metadata:' in next_content:
                        fixed_lines.append('```yaml')
                    elif 'kubectl' in next_content or 'k get' in next_content or 'k apply' in next_content:
                        fixed_lines.append('```bash')
                    elif 'NAME' in next_content and 'READY' in next_content:
                        fixed_lines.append('```')  # Keep plain for output
                    else:
                        fixed_lines.append('```bash')
                elif line.startswith('```') and not in_code_block:
                    # Already has language specifier
                    fixed_lines.append(line)
                else:
                    fixed_lines.append(line)
            in_code_block = not in_code_block
        else:
            # Check for multi-line code blocks that got collapsed
            if 'apiVersion:' in line and 'kind:' in line and 'metadata:' in line:
                # This looks like YAML that got collapsed onto one line
                # Split it properly
                parts = re.split(r'(?=[a-z]+:)', line)
                fixed_lines.append('```yaml')
                for part in parts:
                    if part.strip():
                        fixed_lines.append(part.strip())
                fixed_lines.append('```')
            elif line.count('```') >= 2:
                # Multiple code blocks on same line
                parts = line.split('```')
                for j, part in enumerate(parts):
                    if j % 2 == 0:
                        if part.strip():
                            fixed_lines.append(part.strip())
                    else:
                        # This is code content
                        if 'apiVersion' in part or 'kind:' in part:
                            fixed_lines.append('```yaml')
                        else:
                            fixed_lines.append('```bash')
                        fixed_lines.append(part.strip())
                        fixed_lines.append('```')
            else:
                fixed_lines.append(line)
        i += 1

    return '\n'.join(fixed_lines)

def process_file(filepath):
    """Process a single markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    fixed = fix_code_blocks(content)

    if original != fixed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed)
        return True
    return False

def main():
    posts_dir = '/home/linuxer-hugo/content/posts'
    files = glob.glob(os.path.join(posts_dir, '*.md'))

    fixed_files = []
    for filepath in files:
        filename = os.path.basename(filepath)
        if process_file(filepath):
            fixed_files.append(filename)
            print(f"Fixed: {filename}")

    print(f"\nTotal files fixed: {len(fixed_files)}")
    return fixed_files

if __name__ == '__main__':
    main()