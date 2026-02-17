import unittest
from htmlnode import HTMLNode, LeafNode


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



class TestLeafNode(unittest.TestCase):
    def setUp(self):
        self.node0 = LeafNode(None, None)
        self.node1 = LeafNode("p", "Hello")
        self.node2 = LeafNode("a", "Click", {"href": "https://google.com"})
        self.node3 = LeafNode("p", "Hello", {"class": "intro"})
        self.node4 = LeafNode("p", "Hello", {"class": "intro"})
        self.node5 = LeafNode(None, "Just some raw text here")


    def test_leaf_to_html_p(self):
        self.assertEqual(self.node1.to_html(), "<p>Hello</p>")


    def test_eq(self):
        self.assertEqual(self.node3, self.node4)


    def test_to_html_no_tag(self):
        self.assertEqual(self.node5.to_html(), "Just some raw text here")


    def test_to_html_with_props(self):
        self.assertEqual(self.node2.to_html(), '<a href="https://google.com">Click</a>')


    def test_to_html_no_value(self):
        with self.assertRaises(ValueError):
            self.node0.to_html()


    def test_not_eq(self):
        self.assertNotEqual(self.node1, self.node2)


if __name__ == "__main__":
    unittest.main()
