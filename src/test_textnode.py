import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is some anchor text", TextType.BOLD)
        node2 = TextNode("This is some anchor text", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_text_not_eq(self):
        node1 = TextNode("This is some anchor text", TextType.BOLD)
        node2 = TextNode("This is some other anchor text", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_type_not_eq(self):
        node1 = TextNode("This is some anchor text", TextType.BOLD)
        node2 = TextNode("This is some anchor text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_url_not_eq(self):
        node1 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is some anchor text", TextType.LINK)
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = TextNode("This is some anchor text", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is some anchor text, BOLD, None)")

    def test_repr_with_url(self):
        node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(repr(node), "TextNode(This is some anchor text, LINK, https://www.boot.dev)")


if __name__ == "__main__":
    unittest.main()