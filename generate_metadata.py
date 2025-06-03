import os
import yaml
from datetime import datetime


def compute_word_count(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        return len(text.split())
    except Exception:
        return 0


def build_metadata(path):
    return {
        'title': os.path.basename(path),
        'path': path,
        'word_count': compute_word_count(path),
        'last_modified': datetime.fromtimestamp(os.path.getmtime(path)).isoformat(),
        'linked_nodes': []
    }


def main(base='.'):  # default to current directory
    for root, dirs, files in os.walk(base):
        # Skip version control and hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for name in files:
            if name.endswith('.meta.yaml'):
                continue
            file_path = os.path.join(root, name)
            meta = build_metadata(file_path)
            meta_path = os.path.join(root, f"{name}.meta.yaml")
            with open(meta_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(meta, f, sort_keys=False)
            print(f"Wrote {meta_path}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate metadata for files')
    parser.add_argument('base', nargs='?', default='.', help='Base directory')
    args = parser.parse_args()
    main(args.base)
