import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_basic_single_delimiter_pair(self):
        node = TextNode("Hello `world` there", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.BOLD)

        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode(" there", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


    def test_no_delimiters(self):
        node = TextNode("Hello world there", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.BOLD)

        expected = [TextNode("Hello world there", TextType.TEXT)]
        self.assertEqual(result, expected)


    def test_multiple_delimiter_pairs(self):
        node = TextNode("Hello `world` and `friend`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.BOLD)

        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("friend", TextType.BOLD),
        ]
        self.assertEqual(result, expected)


    def test_non_text_nodes_pass_through(self):
        bold_node = TextNode("Bold text", TextType.BOLD)
        link_node = TextNode("Click here", TextType.LINK, "https://example.com")

        result = split_nodes_delimiter([bold_node, link_node], "`", TextType.BOLD)

        expected = [bold_node, link_node]
        self.assertEqual(result, expected)


    def test_mixed_text_and_non_text_nodes(self):
        text_node = TextNode("Hello `world`", TextType.TEXT)
        bold_node = TextNode("Already bold", TextType.BOLD)

        result = split_nodes_delimiter([text_node, bold_node], "`", TextType.ITALIC)

        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.ITALIC),
            TextNode("Already bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)


    def test_unclosed_delimiter_raises_error(self):
        node = TextNode("Hello `world", TextType.TEXT)

        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.BOLD)

        self.assertIn("Invalid markdown", str(context.exception))


    def test_leading_delimiter(self):
        node = TextNode("`bold` text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.BOLD)

        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


    def test_trailing_delimiter(self):
        node = TextNode("text `bold`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.BOLD)

        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)


    def test_empty_input_list(self):
        result = split_nodes_delimiter([], "`", TextType.BOLD)
        self.assertEqual(result, [])


    def test_code_text_type(self):
        node = TextNode("Hello `code` here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()

