#!/usr/bin/env python3
import os
import re
import glob

def determine_language(content):
    """Determine the language based on content"""
    # Check first few meaningful lines
    lines = [l.strip() for l in content.strip().split('\n')[:5] if l.strip()]

    # YAML indicators
    yaml_patterns = ['apiVersion:', 'kind:', 'metadata:', 'spec:', 'data:', 'rules:']
    for pattern in yaml_patterns:
        if any(pattern in line for line in lines):
            return 'yaml'

    # Bash/shell indicators
    bash_patterns = ['kubectl ', 'k get', 'k apply', 'docker ', 'helm ', 'aws ', 'export ', 'echo ', 'cd ', 'ls ', 'grep ']
    for pattern in bash_patterns:
        if any(pattern in line for line in lines):
            return 'bash'

    # Output/logs (no language specifier)
    if any('NAME' in line and 'STATUS' in line for line in lines):
        return ''  # Plain output
    if any('ERROR' in line or 'WARN' in line or 'INFO' in line for line in lines):
        return ''  # Logs

    # Default to bash for commands
    return 'bash'

def fix_code_blocks(content):
    """Fix all code block formatting issues"""
    lines = content.split('\n')
    fixed_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this line starts with ``` (code block delimiter)
        if line.strip().startswith('```'):
            # Extract any language specifier
            lang_match = re.match(r'^```(\w*)', line.strip())
            current_lang = lang_match.group(1) if lang_match else ''

            # If no language specified, try to determine it
            if current_lang == '':
                # Look ahead to determine language
                code_content = []
                j = i + 1
                while j < len(lines) and not lines[j].strip().startswith('```'):
                    code_content.append(lines[j])
                    j += 1

                if code_content:
                    detected_lang = determine_language('\n'.join(code_content))
                    if detected_lang:
                        fixed_lines.append(f'```{detected_lang}')
                    else:
                        fixed_lines.append('```')
                else:
                    fixed_lines.append('```')
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

        i += 1

    return '\n'.join(fixed_lines)

def process_file(filepath):
    """Process a single markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # First, fix any code blocks without language specifiers
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
    for filepath in sorted(files):
        filename = os.path.basename(filepath)

        # Check if file has code blocks without language specifiers
        with open(filepath, 'r') as f:
            content = f.read()
            if re.search(r'^```\s*$', content, re.MULTILINE):
                if process_file(filepath):
                    fixed_files.append(filename)
                    print(f"Fixed: {filename}")

    print(f"\nTotal files fixed: {len(fixed_files)}")
    return fixed_files

if __name__ == '__main__':
    main()