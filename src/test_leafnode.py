import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("div", "test")
        self.assertEqual(node.to_html(), "<div>test</div>")

    def test_leaf_to_html_empty_value(self):
        node = LeafNode("div", "")
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "test")
        self.assertEqual(node.to_html(), "test")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("div", None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_to_html_no_tag_no_value(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_to_html_with_props(self):
        node = LeafNode("div", "test", props={"class": "test"})
        self.assertEqual(node.to_html(), "<div class='test'>test</div>")

if __name__ == "__main__":
    unittest.main()
