import os
import shutil

from block_parser import markdown_to_html_node

def copy_static_to_public():
    static_dir = "static"
    public_dir = "public"

    shutil.rmtree(public_dir, ignore_errors=True)
    shutil.os.mkdir(public_dir)
    shutil.copytree(static_dir, public_dir, dirs_exist_ok=True)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    with open(dest_path, "w") as f:
        f.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                # Make sure the destination path has the same subdirectory structure
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, relative_path.replace(".md", ".html"))
                
                # Ensure the destination directory exists
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                # Generate the page
                generate_page(from_path, template_path, dest_path)
