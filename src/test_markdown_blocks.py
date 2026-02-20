import unittest
from markdown_blocks import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
)


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_paragraph(self):
            block = "This is just a paragraph"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_heading_1(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)


    def test_heading_6(self):
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)


    def test_heading_invalid(self):
        block = "####### Too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_heading_no_space(self):
        block = "#NoSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_code(self):
        block = "```\nsome code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)


    def test_code_single_line(self):
        block = "```inline code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)


    def test_quote(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)


    def test_quote_multiline(self):
        block = "> Line one\n> Line two\n> Line three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)


    def test_quote_with_space(self):
        block = ">  Quote with leading space"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)


    def test_quote_invalid(self):
        block = "> First line\nNot a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_unordered_list(self):
        block = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)


    def test_unordered_list_single(self):
        block = "- Single item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)


    def test_unordered_list_invalid(self):
        block = "- Item one\nNot a list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)


    def test_ordered_list_single(self):
        block = "1. Just one item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)


    def test_ordered_list_starts_at_1(self):
        block = "2. Starts at 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_ordered_list_invalid_sequence(self):
        block = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_ordered_list_invalid(self):
        block = "1. First\nNot ordered"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
