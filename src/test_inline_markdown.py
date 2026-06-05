from textnode import *
from htmlnode import *
from inline_markdown import *
import unittest

class TestTextNode(unittest.TestCase):
    def test_split_on_tildes(self):
        # Pretend ~ is our delimiter for "strikethrough" text (hypothetical!)
        node = TextNode("Hello ~world~ today", TextType.TEXT)
        result = split_nodes_delimiter([node], "~", TextType.TEXT)

        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.TEXT),
            TextNode(" today", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_on_stars(self):
        # Pretend ** is our delimiter for "Bold" text
        node = TextNode("Hello **world** today", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode(" today", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_delimiter_error(self):
        # Improper Delimiter
        node = TextNode("Hello **world** today**", TextType.TEXT)
        with self.assertRaisesRegex(Exception, "Unclosed delimiter"):
            result = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_multiple_split(self):
        # Pretend ** is our delimiter for "Bold" text but longer
        node = TextNode("Hello **world** today, **more BOLDER**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode(" today, ", TextType.TEXT),
            TextNode("more BOLDER", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_split_with_blank(self):
        # Pretend ** is our delimiter for "Bold" text
        node = TextNode("Hello **world**** today**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode(" today", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_no_split(self):
        # Pretend ** is our delimiter for "Bold" text
        node = TextNode("Hello world today", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("Hello world today", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def text_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://boot.dev)")
        self.assertListEqual([("link", "https://boot.dev")], matches)

    def test_text_extract_markdown_multilinks(self):
        matches = extract_markdown_links("Favorite Websites: [link](https://boot.dev), [link](youtube.com)")
        self.assertListEqual([("link", "https://boot.dev"),("link", "youtube.com")], matches)

    def test_markdown_empty(self):
        matches = extract_markdown_images("This is text with a [link](https://boot.dev)")
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_break_links(self):
        node = TextNode("[My favorite place](boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual( [TextNode("My favorite place", TextType.LINK, "boot.dev")], new_nodes)

    def test_multinodes(self):
        nodeone = TextNode("This is the [first part](google.com)", TextType.TEXT)
        nodetwo = TextNode("can this break it?", TextType.BOLD)
        nodethree = TextNode("I bet this will", TextType.TEXT)
        nodefour = TextNode("check me out at[my channel](youtube.com), remember to like and subscribe", TextType.TEXT)
        nodes = [nodeone, nodetwo, nodethree, nodefour]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("This is the ", TextType.TEXT),
                TextNode("first part", TextType.LINK, "google.com"),
                TextNode("can this break it?", TextType.BOLD),
                TextNode("I bet this will", TextType.TEXT),
                TextNode("check me out at", TextType.TEXT),
                TextNode("my channel", TextType.LINK, "youtube.com"),
                TextNode(", remember to like and subscribe", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_error_textnode(self):
        text = "this shoulde **break the code"
        with self.assertRaisesRegex(Exception, "Unclosed delimiter"):
            new_nodes = text_to_textnodes(text)

    def test_basic_text(self):
        text = "this should **work** right ![boots](boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("this should ", TextType.TEXT),
                TextNode("work", TextType.BOLD),
                TextNode(" right ", TextType.TEXT),
                TextNode("boots", TextType.IMAGE,"boot.dev"),
            ],
            new_nodes,
        )

    def test_more_basic_text(self):
        text = "this should **work** right ![boots](boot.dev), but can it _work_ _work_ like _REALLY_ work?"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("this should ", TextType.TEXT),
                TextNode("work", TextType.BOLD),
                TextNode(" right ", TextType.TEXT),
                TextNode("boots", TextType.IMAGE,"boot.dev"),
                TextNode(", but can it ", TextType.TEXT),
                TextNode("work", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("work", TextType.ITALIC),
                TextNode(" like ", TextType.TEXT),
                TextNode("REALLY",TextType.ITALIC),
                TextNode(" work?", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_loud_noises(self):
        text = "**Loud Noises**"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Loud Noises", TextType.BOLD),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
