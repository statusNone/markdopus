import re
from textnode import TextType, TextNode


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Error: Invalid markdown: formatted section not closed")

        split_nodes = [
            TextNode(section, TextType.TEXT if i % 2 == 0 else text_type)
            for i, section in enumerate(sections)
            if section
        ]

        new_nodes.extend(split_nodes)

    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^]]*)\]\(([^()]*)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        for match in matches:
            image_alt, image_link = match
            sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            remaining_text = sections[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^]]*)\]\(([^()]*)\)"
    return re.findall(pattern, text)


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        for match in matches:
            text, url = match
            sections = remaining_text.split(f"[{text}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            remaining_text = sections[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

