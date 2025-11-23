import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        node = ParentNode(None, [])
        with self.assertRaises(ValueError) as context:
            node.to_html()
            self.assertEqual("Tag cannot be empty", str(context.exception))

    def test_to_html_no_children(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError) as context:
            node.to_html()
            self.assertEqual("Children cannot be empty", str(context.exception))

    def test_to_html_simple(self):
        node = ParentNode("div", [LeafNode("p", "test")])
        self.assertEqual("<div><p>test</p></div>", node.to_html())

    def test_to_html_with_props(self):
        node = ParentNode("div", [LeafNode("p", "test")], props={"class": "test"})
        self.assertEqual("<div class='test'><p>test</p></div>", node.to_html())

    def test_to_html_with_children(self):
        node = ParentNode("div", [LeafNode("p", "test"), LeafNode("p", "test2")])
        self.assertEqual("<div><p>test</p><p>test2</p></div>", node.to_html())

    def test_to_html_with_children_with_value_and_props(self):
        node = ParentNode("div", [LeafNode("p", "Test", props={"class": "test"})])
        self.assertEqual("<div><p class='test'>Test</p></div>", node.to_html())

    def test_to_html_with_multiple_children_with_value_and_props(self):
        node = ParentNode("div", [LeafNode("p", "Test", props={"class": "test"}), LeafNode("p", "Test2")])
        self.assertEqual("<div><p class='test'>Test</p><p>Test2</p></div>", node.to_html())

    def test_to_html_with_parent_node_as_child(self):
        node = ParentNode("div", [ParentNode("p", [LeafNode("span", "test")])])
        self.assertEqual("<div><p><span>test</span></p></div>", node.to_html())

    def test_to_html_with_multiple_parent_nodes_as_child(self):
        node = ParentNode("div", [ParentNode("p", [LeafNode("span", "test")]), ParentNode("p", [LeafNode("span", "test2")])])
        self.assertEqual("<div><p><span>test</span></p><p><span>test2</span></p></div>", node.to_html())

    def test_to_html_with_multiple_parent_nodes_as_child_with_props(self):
        node = ParentNode("div", [ParentNode("p", [LeafNode("span", "test", props={"class": "test"})], props={"class": "middle_test"})], props={"class": "outer_test"})
        self.assertEqual("<div class='outer_test'><p class='middle_test'><span class='test'>test</span></p></div>", node.to_html())

    def test_to_html_with_multiple_parent_nodes_as_child_with_props_and_children(self):
        node = ParentNode(
            "div",
            [ParentNode(
                "p",
                [LeafNode(
                    "span",
                    "test",
                    props={"class": "test"}
                ), LeafNode(
                    "b",
                    "bold text"
                )],
                props={"class": "middle_test"}
            ), ParentNode(
                "a",
                [LeafNode(
                    "span",
                    "link"
                )],
                props={"href": "https://www.google.com"}
            ), LeafNode(
                "p",
                "test2"
            )],
            props={"class": "outer_test"}
        )
        self.assertEqual("<div class='outer_test'><p class='middle_test'><span class='test'>test</span><b>bold text</b></p><a href='https://www.google.com'><span>link</span></a><p>test2</p></div>", node.to_html())

if __name__ == "__main__":
    unittest.main()
