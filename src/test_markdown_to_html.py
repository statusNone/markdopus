import unittest
from markdown_blocks import (
    BlockType,
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
    block_to_heading,
    block_to_code,
    block_to_quote,
    block_to_unordered_list,
    block_to_ordered_list,
)
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_empty_markdown(self):
        """Empty markdown should return an empty div."""
        result = markdown_to_html_node("")
        expected = ParentNode("div", [])
        self.assertEqual(result, expected)


    def test_single_paragraph(self):
        """Single paragraph block becomes <p> with inline-processed children."""
        markdown = "This is a simple paragraph."
        result = markdown_to_html_node(markdown)

        self.assertIsInstance(result, ParentNode)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)

        p = result.children[0]
        self.assertIsInstance(p, ParentNode)
        self.assertEqual(p.tag, "p")
        # text_to_children("This is a simple paragraph.") should yield [LeafNode(None, "This is a simple paragraph.")]
        self.assertEqual(len(p.children), 1)
        self.assertIsInstance(p.children[0], LeafNode)
        self.assertEqual(p.children[0].value, "This is a simple paragraph.")
        # No inline, so tag is None and value is plain text


    def test_paragraph_with_internal_newlines(self):
        """Internal newlines in a single block are replaced with spaces."""
        markdown = "Line one\nLine two with **bold**"
        result = markdown_to_html_node(markdown)

        p = result.children[0]
        self.assertEqual(p.tag, "p")
        self.assertGreater(len(p.children), 1)
        self.assertEqual(p.children[-1].tag, "b")  # Last should be bold node
        self.assertIn("Line one Line two with ", p.children[0].value)


    def test_single_heading(self):
        """Single heading becomes <hN> with processed children."""
        markdown = "# Heading Level 1"
        result = markdown_to_html_node(markdown)
        
        self.assertEqual(len(result.children), 1)
        heading = result.children[0]
        self.assertIsInstance(heading, ParentNode)
        self.assertEqual(heading.tag, "h1")
        self.assertEqual(len(heading.children), 1)
        self.assertIsInstance(heading.children[0], LeafNode)
        self.assertEqual(heading.children[0].value, "Heading Level 1")
        self.assertIsNone(heading.children[0].tag)  # Plain text unless inline


    def test_multiple_headings(self):
        """Multiple headings of different levels."""
        markdown = "# H1\n\n## H2\n\n### H3"
        result = markdown_to_html_node(markdown)
        
        self.assertEqual(len(result.children), 3)
        
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(result.children[0].children[0].value, "H1")
        
        self.assertEqual(result.children[1].tag, "h2")
        self.assertEqual(result.children[1].children[0].value, "H2")
        
        self.assertEqual(result.children[2].tag, "h3")
        self.assertEqual(result.children[2].children[0].value, "H3")


    def test_heading_invalid_falls_to_paragraph(self):
        """Invalid heading (e.g., too many # or no space) becomes <p>."""
        markdown = "#NoSpace Here\n\n####### Invalid H7"
        result = markdown_to_html_node(markdown)
        
        self.assertEqual(len(result.children), 2)
        
        p1 = result.children[0]
        self.assertEqual(p1.tag, "p")
        self.assertEqual(p1.children[0].value, "#NoSpace Here")
        
        p2 = result.children[1]
        self.assertEqual(p2.tag, "p")
        self.assertEqual(p2.children[0].value, "####### Invalid H7")


    def test_single_code_block(self):
        """Code block becomes <pre><code>...</code></pre>."""
        markdown = "```\nprint('Hello')\n```"
        result = markdown_to_html_node(markdown)
        
        self.assertEqual(len(result.children), 1)
        pre = result.children[0]
        self.assertIsInstance(pre, ParentNode)
        self.assertEqual(pre.tag, "pre")
        self.assertEqual(len(pre.children), 1)
        
        code = pre.children[0]
        self.assertIsInstance(code, LeafNode)
        self.assertEqual(code.tag, "code")  # text_node_to_html_node for CODE -> <code>
        self.assertEqual(code.value, "print('Hello')")  # Strips outer \n


    def test_code_single_line(self):
        """Single-line code block."""
        markdown = "```inline code```"
        result = markdown_to_html_node(markdown)
        
        code = result.children[0].children[0]
        self.assertEqual(code.tag, "code")
        self.assertEqual(code.value, "inline code")


    def test_single_quote_block(self):
        """Quote becomes <blockquote> with joined text (flattened)."""
        markdown = "> This is a quote\n> On two lines."
        result = markdown_to_html_node(markdown)
        
        self.assertEqual(len(result.children), 1)
        blockquote = result.children[0]
        self.assertIsInstance(blockquote, ParentNode)
        self.assertEqual(blockquote.tag, "blockquote")
        # Your block_to_quote joins with " ", so "This is a quote On two lines."
        # text_to_children processes that (assume plain for now)
        self.assertEqual(len(blockquote.children), 1)
        self.assertIsInstance(blockquote.children[0], LeafNode)
        self.assertEqual(blockquote.children[0].value, "This is a quote On two lines.")


    def test_quote_with_inline(self):
        """Quote with inline Markdown."""
        markdown = "> **Bold** quote"
        result = markdown_to_html_node(markdown)
        
        blockquote = result.children[0]
        self.assertEqual(blockquote.tag, "blockquote")
        # "Bold quote" joined, text_to_children -> multiple children with <b>
        self.assertGreater(len(blockquote.children), 1)
        self.assertEqual(blockquote.children[0].tag, "b")
        self.assertEqual(blockquote.children[0].value, "Bold")


    def test_quote_multiline_with_empty(self):
        """Multiline quote with empty line (joins with space)."""
        markdown = "> Line 1\n>\n> Line 3"
        result = markdown_to_html_node(markdown)
        
        blockquote = result.children[0]
        # Joins: "Line 1  Line 3" (empty becomes space)
        self.assertEqual(blockquote.children[0].value, "Line 1  Line 3")


    def test_single_unordered_list(self):
        """Unordered list becomes <ul><li>...</li></ul>."""
        markdown = "- Item one\n- Item two"
        result = markdown_to_html_node(markdown)
        
        self.assertEqual(len(result.children), 1)
        ul = result.children[0]
        self.assertIsInstance(ul, ParentNode)
        self.assertEqual(ul.tag, "ul")
        self.assertEqual(len(ul.children), 2)  # Two <li>
        
        li1 = ul.children[0]
        self.assertIsInstance(li1, ParentNode)
        self.assertEqual(li1.tag, "li")
        self.assertEqual(len(li1.children), 1)
        self.assertEqual(li1.children[0].value, "Item one")  # Assuming line[2:].lstrip(" ")
        
        li2 = ul.children[1]
        self.assertEqual(li2.children[0].value, "Item two")


    def test_unordered_list_with_inline(self):
        """List item with inline Markdown."""
        markdown = "- **Bold** item"
        result = markdown_to_html_node(markdown)

        li = result.children[0].children[0]
        self.assertEqual(li.tag, "li")
        self.assertGreater(len(li.children), 1)  # Inline bold
        self.assertEqual(li.children[0].tag, "b")


    def test_unordered_list_invalid_falls_to_paragraph(self):
        """Invalid list becomes paragraph."""
        markdown = "- Item one\nNot a list"
        result = markdown_to_html_node(markdown)

        p = result.children[0]
        self.assertEqual(p.tag, "p")
        self.assertEqual(p.children[0].value, "- Item one Not a list")


    def test_single_ordered_list(self):
        """Ordered list becomes <ol><li>...</li></ol>."""
        markdown = "1. Item one\n2. Item two"
        result = markdown_to_html_node(markdown)

        self.assertEqual(len(result.children), 1)
        ol = result.children[0]
        self.assertIsInstance(ol, ParentNode)
        self.assertEqual(ol.tag, "ol")
        self.assertEqual(len(ol.children), 2)

        li1 = ol.children[0]
        self.assertEqual(li1.tag, "li")
        self.assertEqual(li1.children[0].value, "Item one")  # After ". "

        li2 = ol.children[1]
        self.assertEqual(li2.children[0].value, "Item two")


    def test_ordered_list_with_inline(self):
        """Ordered list with inline."""
        markdown = "1. **Bold** item"
        result = markdown_to_html_node(markdown)

        li = result.children[0].children[0]
        self.assertGreater(len(li.children), 1)
        self.assertEqual(li.children[0].tag, "b")


    def test_ordered_list_invalid_sequence_falls_to_paragraph(self):
        """Non-sequential numbering becomes paragraph."""
        markdown = "1. First\n3. Third"
        result = markdown_to_html_node(markdown)

        p = result.children[0]
        self.assertEqual(p.tag, "p")
        self.assertEqual(p.children[0].value, "1. First 3. Third")


    def test_blocks_splitting_with_extra_newlines(self):
        """Test markdown_to_blocks handles excessive \n\n (from your existing tests)."""
        # This indirectly tests markdown_to_html_node uses clean blocks
        md = "Para 1\n\n\nPara 2\n\n- List\n- Item"
        result = markdown_to_html_node(md)

        self.assertEqual(len(result.children), 3)  # p, p, ul (ignores extra \n\n)
        self.assertEqual(result.children[1].tag, "p")
        self.assertEqual(result.children[2].tag, "ul")


    def test_paragraph_with_code_inline_in_list_item(self):
        """Edge case: inline code in list (tests full pipeline)."""
        markdown = "- Item with `code` inline"
        result = markdown_to_html_node(markdown)

        li = result.children[0].children[0]
        self.assertEqual(li.tag, "li")
        # text_to_children handles `code` -> <code> node
        self.assertGreater(len(li.children), 1)
        self.assertEqual(li.children[1].tag, "code")  # Assuming position of inline code
        self.assertEqual(li.children[1].value, "code")


    def test_block_to_heading_isolation(self):
        """Test block_to_heading directly."""
        block = "# Level 1"
        result = block_to_heading(block)
        self.assertEqual(result.tag, "h1")
        self.assertEqual(result.children[0].value, "Level 1")


    def test_block_to_code_isolation(self):
        """Test block_to_code directly."""
        block = "```\ncode\n```"
        result = block_to_code(block)
        self.assertEqual(result.tag, "pre")
        self.assertEqual(result.children[0].tag, "code")
        self.assertEqual(result.children[0].value, "code")


    def test_block_to_quote_isolation(self):
        """Test block_to_quote directly (note: flattens to single line)."""
        block = "> Quote 1\n> Quote 2"
        result = block_to_quote(block)
        self.assertEqual(result.tag, "blockquote")
        self.assertEqual(result.children[0].value, "Quote 1 Quote 2")  # Joined with space


    def test_block_to_unordered_list_isolation(self):
        """Test block_to_unordered_list directly."""
        block = "- Item 1\n- Item 2"
        result = block_to_unordered_list(block)
        self.assertEqual(result.tag, "ul")
        self.assertEqual(len(result.children), 2)
        self.assertEqual(result.children[0].tag, "li")
        self.assertEqual(result.children[0].children[0].value, "Item 1")


        def test_block_to_ordered_list_isolation(self):
            """Test block_to_ordered_list directly."""
            block = "1. Item 1\n2. Item 2"
            result = block_to_ordered_list(block)
            self.assertEqual(result.tag, "ol")
            self.assertEqual(len(result.children), 2)
            self.assertEqual(result.children[0].children[0].value, "Item 1")  # After ". "


if __name__ == "__main__":
    unittest.main()


