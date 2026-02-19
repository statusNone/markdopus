from textnode import TextType, TextNode


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
