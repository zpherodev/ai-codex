import os
import re
from urllib.parse import quote


def find_markdown_files(root):
    md_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            if f.lower().endswith('.md'):
                md_files.append(os.path.join(dirpath, f))
    return md_files


SEE_PATTERN = re.compile(r"See:\s*Chapter\s*(\d+),\s*Article\s*(\d+)", re.IGNORECASE)


def extract_references(text):
    refs = set()
    for m in SEE_PATTERN.finditer(text):
        chapter, article = m.group(1), m.group(2)
        refs.add((chapter, article))
    return sorted(refs)


def build_link(chapter, article):
    path = f"Chapter {chapter}/Article {article}"
    return f"[Chapter {chapter}, Article {article}]({quote(path)})"


def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'See Also:' in content:
        return False

    refs = extract_references(content)
    if not refs:
        return False

    links = [f"- {build_link(c, a)}" for c, a in refs]
    see_also_section = '\n\n## See Also:\n' + '\n'.join(links) + '\n'

    with open(path, 'a', encoding='utf-8') as f:
        f.write(see_also_section)

    return True


def main():
    root = '.'
    md_files = find_markdown_files(root)
    changed = False
    for path in md_files:
        if process_file(path):
            print(f"Updated {path}")
            changed = True
    if not changed:
        print("No updates required")


if __name__ == '__main__':
    main()
