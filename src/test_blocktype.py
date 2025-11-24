import unittest
from blocktype import BlockType, block_to_block_type

class TestBlockNode(unittest.TestCase):
    def test_block_to_block_type_heading_one(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_six(self):
        block = "###### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "```python\nprint('Hello World!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = "> Quote Line 1\n> Quote Line 2\n> Quote Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_quote_wrong(self):
        block = "> Quote Line 1\nQuote Line 2\nQuote Line 3"
        self.assertNotEqual(block_to_block_type(block), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        block = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_wrong(self):
        block = "- Item 1\nItem 2"
        self.assertNotEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        block = "1. Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_wrong(self):
        block = "1. Item 1\nItem 2"
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_wrong_number(self):
        block = "1. Item 1\n2. Item 2\n4. Item 3"
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == '__main__':
    unittest.main()
