import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello World"), "Hello World")

    def test_extract_title_no_title(self):
        with self.assertRaises(ValueError) as context:
            extract_title("Hello World")
            self.assertEqual(context.exception.args[0], "No title found")

if __name__ == "__main__":
    unittest.main()
