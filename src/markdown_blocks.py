from enum import Enum
from inline_markdown import text_to_textnodes
from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import ParentNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                children.append(block_to_heading(block))
            case BlockType.CODE:
                children.append(block_to_code(block))
            case BlockType.QUOTE:
                children.append(block_to_quote(block))
            case BlockType.UNORDERED_LIST:
                children.append(block_to_unordered_list(block))
            case BlockType.ORDERED_LIST:
                children.append(block_to_ordered_list(block))
            case _:
                children.append(ParentNode("p", text_to_children(block.replace("\n", " "))))
    return ParentNode("div", children)


def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]


def text_to_children(text):
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]


def is_heading(block):
    if not block.startswith("#"):
        return False
    level = len(block) - len(block.lstrip("#"))
    return 1 <= level <= 6 and len(block) > level and block[level] == " "


def block_to_heading(block):
    text = block.lstrip("#")
    level = len(block) - len(text)
    return ParentNode(f"h{level}", text_to_children(text.lstrip(" ")))


def is_code(block):
    return block.startswith("```") and block.endswith("```")


def block_to_code(block):
    text = block[3:-3].strip("\n")
    return ParentNode("pre", [text_node_to_html_node(TextNode(text, TextType.CODE))])


def is_quote(block):
    return all(line.startswith(">") for line in block.split("\n"))


def block_to_quote(block):
    lines = block.split("\n")
    clean_lines = [line[1:].lstrip(" ") for line in lines]
    text = " ".join(clean_lines).strip()
    return ParentNode("blockquote", text_to_children(text))


def is_unordered_list(block):
    return all(line.startswith("- ") for line in block.split("\n"))


def block_to_unordered_list(block):
    lines = block.split("\n")
    nodes = []
    for line in lines:
        clean_line = line[1:].lstrip(" ")
        children = text_to_children(clean_line)
        nodes.append(ParentNode("li", children))
    return ParentNode("ul", nodes)


def is_ordered_list(block):
    lines = block.split("\n")
    return all(line.startswith(f"{i+1}. ") for i, line in enumerate(lines))


def block_to_ordered_list(block):
    lines = block.split("\n")
    nodes = []
    for line in lines:
        _, clean_line = line.split(". ", 1)
        children = text_to_children(clean_line)
        nodes.append(ParentNode("li", children))
    return ParentNode("ol", nodes)


def block_to_block_type(block):
    if is_heading(block):
        return BlockType.HEADING
    if is_code(block):
        return BlockType.CODE
    if is_quote(block):
        return BlockType.QUOTE
    if is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
