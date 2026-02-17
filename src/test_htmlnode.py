import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def setUp(self):
        self.node0 = HTMLNode()
        self.node1 = HTMLNode("p", "Hello")
        self.node2 = HTMLNode("a", "Click", None, {"href": "https://google.com"})
        self.node3 = HTMLNode("p", "Hello", None, {"class": "intro"})
        self.node4 = HTMLNode("p", "Hello", None, {"class": "intro"})


    def test_eq(self):
        self.assertEqual(self.node3, self.node4)


    def test_props_to_html(self):
        self.assertEqual(self.node2.props_to_html(), ' href="https://google.com"')


    def test_not_eq(self):
        self.assertNotEqual(self.node0, self.node1)


if __name__ == "__main__":
    unittest.main()
