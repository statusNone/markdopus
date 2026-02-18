import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_text_type_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)


    def test_url_is_none(self):
        node = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node.url, None)


    def test_url_is_not_none(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.boot.dev")
        self.assertNotEqual(node.url, None)


if __name__ == "__main__":
    unittest.main()
