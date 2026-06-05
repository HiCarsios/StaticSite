import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_text(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is also a text node", TextType.BOLD)
		self.assertNotEqual(node, node2)

	def test_type(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.ITALIC)
		self.assertNotEqual(node,node2)

	def test_url(self):
		node = TextNode("This is a url text", TextType.LINK, None)
		node2 = TextNode("This is a url text", TextType.LINK)
		self.assertEqual(node, node2)

	def test_texttype(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")

	def test_Italic(self):
		node = TextNode("this is an italic node", TextType.ITALIC)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "i")
		self.assertEqual(html_node.value, "this is an italic node")

	def test_Image(self):
		node = TextNode("this is a picture", TextType.IMAGE, "this is an image")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "img")
		self.assertEqual(html_node.value, "")
		self.assertEqual(html_node.props["src"], "this is an image")

if __name__ == "__main__":
	unittest.main()
