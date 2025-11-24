import unittest
from markdown_to_html import markdown_to_html_node
from parentnode import ParentNode

class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = "This is **bolded** paragraph\ntext in a p\ntag here\n\nThis is another paragraph with _italic_ text and `code` here\n"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_paragraph_with_link(self):
        md = "In this paragraph is a link. [This is a link](https://www.google.com)."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>In this paragraph is a link. <a href=\'https://www.google.com\'>This is a link</a>.</p></div>")

    def test_codeblock(self):
        md = "```This is text that _should_ remain\nthe **same** even with inline stuff\n```"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()
