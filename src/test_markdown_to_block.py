import unittest
from markdown_to_block import markdown_to_block

class TestMarkdownToBlock(unittest.TestCase):
    def test_markdown_to_block(self):
        blocks = markdown_to_block("# Title\n\nThis is a paragraph")
        self.assertEqual(blocks, ["# Title", "This is a paragraph"])

    def test_markdown_to_block_empty(self):
        blocks = markdown_to_block("")
        self.assertEqual(blocks, [])

    def test_markdown_to_block_extra_whitespaces(self):
        blocks = markdown_to_block("# Title  \n\n  This is a paragraph   \n\n  ")
        self.assertEqual(blocks, ["# Title", "This is a paragraph"])

    def test_markdown_to_block_excessive_newlines(self):
        blocks = markdown_to_block("\n\n\n\n\n\n\n# Title\n\n\n\n\n\n\n\nThis is a paragraph\n\n\n\n\n\n\n\n")
        self.assertEqual(blocks, ["# Title", "This is a paragraph"])

    def test_markdown_to_block_with_multiple_paragraphs_and_unordered_lists(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_block(markdown)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items"
            ]
        )

if __name__ == '__main__':
    unittest.main()
