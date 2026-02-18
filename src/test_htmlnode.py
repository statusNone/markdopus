import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentClass(unittest.TestCase):
    def setUp(self):
        self.node0 = LeafNode("b", "leafnode")
        self.node1 = ParentNode("span", [self.node0])
        self.node2 = ParentNode("div", [self.node1])
        self.node3 = ParentNode("p", [self.node2])


    def test_to_html_single_child(self):
        result = self.node1.to_html()
        self.assertEqual(result, "<span><b>leafnode</b></span>")


    def test_to_html_nested_children(self):
        result = self.node2.to_html()
        self.assertEqual(result, "<div><span><b>leafnode</b></span></div>")


    def test_to_html_deep_nesting(self):
        result = self.node3.to_html()
        self.assertEqual(result, "<p><div><span><b>leafnode</b></span></div></p>")


    def test_to_html_with_props(self):
        node = ParentNode("div", [self.node0], props={"class": "container"})
        result = node.to_html()
        self.assertEqual(result, '<div class="container"><b>leafnode</b></div>')


    def test_to_html_multiple_children(self):
        leaf1 = LeafNode("b", "bold")
        leaf2 = LeafNode("i", "italic")
        node = ParentNode("p", [leaf1, leaf2])
        result = node.to_html()
        self.assertEqual(result, "<p><b>bold</b><i>italic</i></p>")


    def test_to_html_empty_children(self):
        node = ParentNode("div", [])
        result = node.to_html()
        self.assertEqual(result, "<div></div>")


    def test_to_html_no_tag_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [self.node0]).to_html()


    def test_to_html_none_children_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()


    def test_eq(self):
        node_a = ParentNode("div", [LeafNode("b", "text")])
        node_b = ParentNode("div", [LeafNode("b", "text")])
        self.assertEqual(node_a, node_b)


    def test_not_eq(self):
        node_a = ParentNode("div", [self.node0])
        node_b = ParentNode("span", [self.node0])
        self.assertNotEqual(node_a, node_b)


if __name__ == "__main__":
    unittest.main()
