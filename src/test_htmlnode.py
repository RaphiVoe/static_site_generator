import unittest
from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("div")
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode("div", props={"class": "test"})
        self.assertEqual(node.props_to_html(), " class='test'")

    def test_props_to_html_empty(self):
        node = HTMLNode("div")
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("div")
        self.assertEqual(repr(node), "Tag: div, Value: None, Children: [], Props: {}")

    def test_repr_with_value(self):
        node = HTMLNode("div", value="test")
        self.assertEqual(repr(node), "Tag: div, Value: test, Children: [], Props: {}")

    def test_repr_with_children(self):
        node = HTMLNode("div", children=[HTMLNode("span")])
        self.assertEqual(repr(node), "Tag: div, Value: None, Children: [Tag: span, Value: None, Children: [], Props: {}], Props: {}")

    def test_repr_with_props(self):
        node = HTMLNode("div", props={"class": "test"})
        self.assertEqual(repr(node), "Tag: div, Value: None, Children: [], Props: {'class': 'test'}")

if __name__ == "__main__":
    unittest.main()