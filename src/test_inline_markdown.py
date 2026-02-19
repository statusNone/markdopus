import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    extract_markdown_images,
    extract_markdown_links,
)


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


class TestExtractMarkdown(unittest.TestCase):

    def test_extract_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjzJKk.png)"
        result = extract_markdown_images(text)
        expected = [("image", "https://i.imgur.com/zjjzJKk.png")]
        self.assertEqual(result, expected)


    def test_extract_images_multiple(self):
        text = "![img1](url1.png) and ![img2](url2.png)"
        result = extract_markdown_images(text)
        expected = [("img1", "url1.png"), ("img2", "url2.png")]
        self.assertEqual(result, expected)


    def test_extract_images_no_images(self):
        text = "Just plain text with no images"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])


    def test_extract_images_empty_alt(self):
        text = "![](/path/to/image.png)"
        result = extract_markdown_images(text)
        expected = [("", "/path/to/image.png")]
        self.assertEqual(result, expected)


    def test_extract_links(self):
        text = "This is text with a [link](https://google.com)"
        result = extract_markdown_links(text)
        expected = [("link", "https://google.com")]
        self.assertEqual(result, expected)


    def test_extract_links_multiple(self):
        text = "[link1](url1.com) and [link2](url2.com)"
        result = extract_markdown_links(text)
        expected = [("link1", "url1.com"), ("link2", "url2.com")]
        self.assertEqual(result, expected)


    def test_extract_links_no_links(self):
        text = "Just plain text with no links"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])


    def test_extract_links_excludes_images(self):
        text = "![alt](image.png) is not a [link](url.com)"
        result = extract_markdown_links(text)
        expected = [("link", "url.com")]
        self.assertEqual(result, expected)


    def test_extract_links_empty_text(self):
        text = "[](https://example.com)"
        result = extract_markdown_links(text)
        expected = [("", "https://example.com")]
        self.assertEqual(result, expected)


    def test_extract_links_with_special_chars_in_text(self):
        text = "A [link with spaces](https://example.com) and [bold **text**](url)"
        result = extract_markdown_links(text)
        expected = [("link with spaces", "https://example.com"), ("bold **text**", "url")]
        self.assertEqual(result, expected)


class TestSplitNodes(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

if __name__ == "__main__":
    unittest.main()

