import sys, os, shutil
from textnode import TextType, TextNode
from gencontent import generate_pages_recursive

def main():
    source = "./static"
    destination = "./docs"
    base_path = sys.argv[0] or "/"
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    copy_dir_contents(source, destination)
    generate_pages_recursive(base_path, "content/", "template.html", "public/")

def copy_dir_contents(source, destination):
    contents = os.listdir(source)
    for content in os.listdir(source):
        content_source = os.path.join(source, content)
        content_destination = os.path.join(destination, content)
        if os.path.isfile(content_source):
            shutil.copy(content_source, content_destination)
        if os.path.isdir(content_source):
            os.mkdir(content_destination)
            copy_dir_contents(content_source, content_destination)


if __name__ == "__main__":
    main()
