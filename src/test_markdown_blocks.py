from markdown_blocks import *
import unittest



class Test_Markdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_with_empty(self):
        md = """
This is a line

 

This is another line
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a line",
                "This is another line",
            ],
        )

    def test_markdown_with_no_breaks(self):
        md = """
This is a long paragraph
But everything goes together
this should just be one thing
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a long paragraph\nBut everything goes together\nthis should just be one thing",
            ],
        )

    def test_block_block(self):
        md = "This is a paragraph"
        blcktype = block_to_block_type(md)
        self.assertEqual(blcktype, BlockType.PARAGRAPH)

    def test_block_code(self):
        md = "```\nhttps\\:boot.dev```"
        blcktype = block_to_block_type(md)
        self.assertEqual(blcktype, BlockType.CODE)

    def test_block_orderd(self):
        md = "1. this is line one\n2. this is line two"
        blcktype = block_to_block_type(md)
        self.assertEqual(blcktype, BlockType.ORDERED_LIST)

    def test_changed_list(self):
        md = "- this is line one\n1. this is the real line one"
        blcktype = block_to_block_type(md)
        self.assertEqual(blcktype, BlockType.PARAGRAPH)


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        print("this is being tested")
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_ordered_list(self):
            md = """
1. What comes after one?
2. What comes after two?
3. What comes after three?
4. FOOOOOOOOOUUUUUR
"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ol><li>What comes after one?</li><li>What comes after two?</li><li>What comes after three?</li><li>FOOOOOOOOOUUUUUR</li></ol></div>",

            )
    def test_heading(self):
        md = """
        ### This is a basic heading
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is a basic heading</h3></div>"
        )

    def test_quote(self):
        md = """
>I hate writing these
>I know responded Boots
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>I hate writing these I know responded Boots</blockquote></div>"
        )