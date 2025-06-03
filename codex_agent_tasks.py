# codex_agent_tasks.py

"""
Codex Agent Task 1: Generate a Contents Table
"""
import os

def generate_contents_table(repo_root):
    output_lines = ["# \U0001F4D8 Codex of Emergence: Contents Table\n"]
    for root, dirs, files in os.walk(repo_root):
        if ".git" in root:
            continue
        depth = root.replace(repo_root, "").count(os.sep)
        indent = "  " * depth
        folder_name = os.path.basename(root)
        if folder_name:
            output_lines.append(f"{indent}- **{folder_name}**")
        for file in sorted(files):
            if file.endswith((".md", ".pdf")):
                rel_path = os.path.relpath(os.path.join(root, file), repo_root)
                output_lines.append(f"{indent}  - [{file}]({rel_path})")
    with open("contents-table.md", "w") as f:
        f.write("\n".join(output_lines))

"""
Codex Agent Task 2: Generate meta.yaml for each markdown or text file
"""
import yaml
from datetime import datetime

def create_meta_yaml(file_path):
    meta = {
        "title": os.path.splitext(os.path.basename(file_path))[0],
        "path": file_path,
        "word_count": sum(1 for _ in open(file_path)) if file_path.endswith(".md") else "n/a",
        "last_modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
        "linked_nodes": []
    }
    with open(os.path.join(os.path.dirname(file_path), "meta.yaml"), "w") as f:
        yaml.dump(meta, f)

def generate_all_meta():
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith((".md", ".txt")) and file != "meta.yaml":
                create_meta_yaml(os.path.join(root, file))

"""
Codex Agent Task 3: Cross-reference generator
"""
import re

def scan_and_link_refs():
    ref_pattern = re.compile(r"Chapter (\d+), Article (\d+)", re.IGNORECASE)
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    content = f.read()
                matches = ref_pattern.findall(content)
                if matches and "## See Also:" not in content:
                    section = "\n\n## See Also:\n"
                    for ch, art in set(matches):
                        ref_path = f"Chapter {ch}/Article {art}/Article {art}.md"
                        if os.path.exists(ref_path):
                            section += f"- [Chapter {ch}, Article {art}]({ref_path})\n"
                    with open(path, "a") as f:
                        f.write(section)

# Example usage (comment/uncomment as needed)
# generate_contents_table(".")
# generate_all_meta()
# scan_and_link_refs()
