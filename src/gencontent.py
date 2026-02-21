import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[1:].strip(" ")
    raise Exception("No title found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        markdown = f.read()
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()
    with open(template_path, 'r') as f:
        template = f.read()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(template)


def generate_pages_recursive(content_dir_path, template_path, dest_dir_path):
    for content in os.listdir(content_dir_path):
        content_path = os.path.join(content_dir_path, content)
        dest_path = os.path.join(dest_dir_path, content).replace(".md", ".html")
        if os.path.isfile(content_path) and content_path.endswith(".md"):
            generate_page(content_path, template_path, dest_path)
        if os.path.isdir(content_path):
            os.mkdir(dest_path)
            generate_pages_recursive(content_path, template_path, dest_path)
