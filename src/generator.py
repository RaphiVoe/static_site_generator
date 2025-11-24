import os

from extract_title import extract_title
from markdown_to_html import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = open(from_path, "r").read()
    template = open(template_path, "r").read()
    html_node = markdown_to_html_node(md)
    html = html_node.to_html()
    title = extract_title(md)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    open(dest_path, "w").write(page)

def generate_all(from_dir, template_path, dest_dir):
    for file in os.listdir(from_dir):
        if os.path.isfile(os.path.join(from_dir, file)):
            generate_page(os.path.join(from_dir, file), template_path, os.path.join(dest_dir, file.replace(".md", ".html")))
        else:
            generate_all(os.path.join(from_dir, file), template_path, os.path.join(dest_dir, file))
