import unittest
from textnode import TextNode, TextType
from textsplitter import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes
)

class TestTextSplitter(unittest.TestCase):
    def test_split_nodes_bold_delimiter(self):
        nodes = [TextNode("This is a text node with **bold** text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_nodes_bold_delimiter_end_of_text(self):
        nodes = [TextNode("This is a text node with **bold**", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD)
            ],
            new_nodes
        )

    def test_split_nodes_bold_delimiter_full_text(self):
        nodes = [TextNode("**This is a text node with bold**", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is a text node with bold", TextType.BOLD)
            ],
            new_nodes
        )

    def test_split_nodes_bold_delimiter_start_of_text(self):
        nodes = [TextNode("**Bold** text node at start of text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Bold", TextType.BOLD),
                TextNode(" text node at start of text", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_nodes_bold_delimiter_no_closing_delimiter(self):
        nodes = [TextNode("This is a text node with **bold", TextType.TEXT)]
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter(nodes, "**", TextType.BOLD)
            self.assertEqual("No closing delimiter found", str(context.exception))

    def test_split_nodes_empty_nodes(self):
        nodes = []
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter(nodes, "**", TextType.BOLD)
            self.assertEqual("Nodes cannot be empty", str(context.exception))

    def test_split_nodes_no_delimiter(self):
        nodes = [TextNode("This is a text node without delimiters", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertListEqual(nodes, new_nodes)

    def test_split_nodes_italics_delimiter(self):
        nodes = [TextNode("This is a text node with _italic_ text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_nodes_code_delimiter(self):
        nodes = [TextNode("This is a text node with `code` text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_nodes_bold_delimiter_multiple_delimiters(self):
        nodes = [TextNode("This is a text node with **bold** text with **multiple bold** parts", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text with ", TextType.TEXT),
                TextNode("multiple bold", TextType.BOLD),
                TextNode(" parts", TextType.TEXT)
            ],
            new_nodes
        )

    def test_extract_markdown_images(self):
        images = extract_markdown_images("![alt text](image.png)")
        self.assertEqual(images, [("alt text", "image.png")])

    def test_extract_markdown_images_no_images(self):
        images = extract_markdown_images("This is a text without images")
        self.assertEqual(images, [])

    def test_extract_markdown_images_multiple_images(self):
        images = extract_markdown_images("this is text with some images ![alt text 1](image1.png) inside it ![alt text 2](image2.png) to test")
        self.assertEqual(images, [("alt text 1", "image1.png"), ("alt text 2", "image2.png")])

    def test_extract_markdown_image_from_link(self):
        images = extract_markdown_images("text with [link text](www.link.com)")
        self.assertEqual(images, [])

    def test_extract_markdown_links(self):
        links = extract_markdown_links("[link text](www.link.com)")
        self.assertEqual(links, [("link text", "www.link.com")])

    def test_extract_markdown_links_no_links(self):
        links = extract_markdown_links("This is a text without links")
        self.assertEqual(links, [])

    def test_extract_markdown_links_multiple_links(self):
        links = extract_markdown_links("this is text with some links [link text 1](www.link1.com) inside it [link text 2](www.link2.com) to test")
        self.assertEqual(links, [("link text 1", "www.link1.com"), ("link text 2", "www.link2.com")])

    def test_extract_markdown_link_from_image(self):
        links = extract_markdown_links("text with ![image text](image.png)")
        self.assertEqual(links, [])

    def test_split_nodes_link(self):
        nodes = [TextNode("This is a text node with [link text](www.link.com) text", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "www.link.com"),
                TextNode(" text", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_nodes_link_no_links(self):
        nodes = [TextNode("This is a text node without links", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(nodes, new_nodes)

    def test_split_nodes_link_multiple_links(self):
        nodes = [TextNode("This is a text node with [link text 1](www.link1.com) and [link text 2](www.link2.com) inside it", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("link text 1", TextType.LINK, "www.link1.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link text 2", TextType.LINK, "www.link2.com"),
                TextNode(" inside it", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_nodes_link_at_start_of_text(self):
        nodes = [TextNode("[link text](www.link.com) text node at start of text", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("link text", TextType.LINK, "www.link.com"),
                TextNode(" text node at start of text", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_nodes_link_full_text(self):
        nodes = [TextNode("[link text](www.link.com)", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("link text", TextType.LINK, "www.link.com")
            ],
            new_nodes
        )

    def test_split_nodes_link_end_of_text(self):
        nodes = [TextNode("This is a text node with [link text](www.link.com)", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "www.link.com")
            ], new_nodes
        )

    def test_split_nodes_link_no_closing_delimiter(self):
        nodes = [TextNode("This is a text node with [link text", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(nodes, new_nodes)

    def test_split_nodes_link_from_image(self):
        nodes = [TextNode("text with ![image text](image.png)", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(nodes, new_nodes)

    def test_split_nodes_image(self):
        nodes = [TextNode("This is a text node with ![image text](image.png) text", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("image text", TextType.IMAGE, "image.png"),
                TextNode(" text", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_nodes_image_no_images(self):
        nodes = [TextNode("This is a text node without images", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(nodes, new_nodes)

    def test_split_nodes_image_multiple_images(self):
        nodes = [TextNode("This is a text node with ![image text 1](image1.png) and ![image text 2](image2.png) inside it", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("image text 1", TextType.IMAGE, "image1.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("image text 2", TextType.IMAGE, "image2.png"),
                TextNode(" inside it", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_nodes_image_at_start_of_text(self):
        nodes = [TextNode("![image text](image.png) text node at start of text", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("image text", TextType.IMAGE, "image.png"),
                TextNode(" text node at start of text", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_nodes_image_full_text(self):
        nodes = [TextNode("![image text](image.png)", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("image text", TextType.IMAGE, "image.png")
            ],
            new_nodes
        )

    def test_split_nodes_image_end_of_text(self):
        nodes = [TextNode("This is a text node with ![image text](image.png)", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("image text", TextType.IMAGE, "image.png")
            ],
            new_nodes
        )

    def test_split_nodes_image_no_closing_delimiter(self):
        nodes = [TextNode("This is a text node with ![image text", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(nodes, new_nodes)

    def test_split_nodes_image_from_link(self):
        nodes = [TextNode("text with [link text](www.link.com)", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(nodes, new_nodes)

    def test_text_to_textnodes_only_delimiters(self):
        nodes = text_to_textnodes("This is a **bold** text with _italic_ text and `code` text")
        new_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertListEqual(nodes, new_nodes)

    def test_text_to_textnodes_with_links_and_images(self):
        node = text_to_textnodes("This is a text with ![image text](image.png) and [link text](www.link.com)")
        new_nodes = [
            TextNode("This is a text with ", TextType.TEXT),
            TextNode("image text", TextType.IMAGE, "image.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link text", TextType.LINK, "www.link.com")
        ]
        self.assertListEqual(node, new_nodes)

    def test_text_to_textnodes_with_delimiters_links_and_images(self):
        node = text_to_textnodes("This is a text with **bold** text with _italic_ text, with `code` text, with ![image text](image.png) and [link text](www.link.com) text")
        new_nodes = [
            TextNode("This is a text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text, with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text, with ", TextType.TEXT),
            TextNode("image text", TextType.IMAGE, "image.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link text", TextType.LINK, "www.link.com"),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertListEqual(node, new_nodes)

    def test_text_to_textnodes_with_multiple_everything(self):
        node = text_to_textnodes("This is a text with **bold** text with _italic_ text, with `code` text, with ![image text](image.png) and [link text](www.link.com) text with ![image text 2](image2.png) and [link text 2](www.link2.com) text as well as more **bold** text, _italic_ text and `code` text")
        new_nodes = [
            TextNode("This is a text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text, with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text, with ", TextType.TEXT),
            TextNode("image text", TextType.IMAGE, "image.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link text", TextType.LINK, "www.link.com"),
            TextNode(" text with ", TextType.TEXT),
            TextNode("image text 2", TextType.IMAGE, "image2.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link text 2", TextType.LINK, "www.link2.com"),
            TextNode(" text as well as more ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text, ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertListEqual(node, new_nodes)

if __name__ == "__main__":
    unittest.main()
