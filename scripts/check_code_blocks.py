#!/usr/bin/env python3
import os
import glob
import re

def find_posts_with_code_blocks():
    posts_dir = '/home/linuxer-hugo/content/posts'
    files = glob.glob(os.path.join(posts_dir, '*.md'))

    posts_with_yaml = []
    posts_with_bash = []
    posts_with_plain = []
    posts_with_other = []

    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

            # Find all code blocks
            code_blocks = re.findall(r'```(\w*)', content)

            if code_blocks:
                filename = os.path.basename(filepath)
                slug_match = re.search(r'^slug:\s*"([^"]+)"', content, re.MULTILINE)
                slug = slug_match.group(1) if slug_match else filename.replace('.md', '')

                for lang in code_blocks:
                    if lang == 'yaml':
                        posts_with_yaml.append((filename, slug))
                        break
                    elif lang == 'bash':
                        posts_with_bash.append((filename, slug))
                        break
                    elif lang == '':
                        posts_with_plain.append((filename, slug))
                        break
                    elif lang:
                        posts_with_other.append((filename, slug, lang))
                        break

    return {
        'yaml': posts_with_yaml[:5],
        'bash': posts_with_bash[:5],
        'plain': posts_with_plain[:5],
        'other': posts_with_other[:5]
    }

def main():
    results = find_posts_with_code_blocks()

    print("Posts with YAML code blocks:")
    for filename, slug in results['yaml']:
        print(f"  {filename} -> /posts/{slug}/")

    print("\nPosts with Bash code blocks:")
    for filename, slug in results['bash']:
        print(f"  {filename} -> /posts/{slug}/")

    print("\nPosts with plain code blocks:")
    for filename, slug in results['plain']:
        print(f"  {filename} -> /posts/{slug}/")

    print("\nPosts with other language code blocks:")
    for filename, slug, lang in results['other']:
        print(f"  {filename} ({lang}) -> /posts/{slug}/")

if __name__ == '__main__':
    main()