import unittest
from gencontent import *


class test_generate_content(unittest.TestCase):
    def test_markdown_one(self):
        markdown = "# basic header  "
        title = extract_title(markdown)
        self.assertEqual(
            "basic header",
            title,
        )
    
    def test_markdown_error(self):
        markdown ="""
        this should have no header
        ### This is not a header
        """
        with self.assertRaises(Exception):
            title = extract_title(markdown)

    def test_markdown_extended(self):
        markdown ="""
this is a longer text
# Header
extra text here
and here
"""
        title = extract_title(markdown)
        self.assertEqual("Header", title)
