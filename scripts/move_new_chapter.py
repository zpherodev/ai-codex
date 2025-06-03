#!/usr/bin/env python3
"""Move new_chapter_additions.md into the chapters directory if present."""

import os
import shutil


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = os.path.join(repo_root, "new_chapter_additions.md")
    dst_dir = os.path.join(repo_root, "chapters")

    if os.path.exists(src):
        os.makedirs(dst_dir, exist_ok=True)
        dst = os.path.join(dst_dir, os.path.basename(src))
        shutil.move(src, dst)
        print(f"Moved {src} -> {dst}")
    else:
        print("No new_chapter_additions.md file found.")


if __name__ == "__main__":
    main()
