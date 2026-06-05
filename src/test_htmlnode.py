import unittest

from textnode import TextNode, TextType
from htmlnode import *


class TestHTMLNode(unittest.TestCase):
	def test_props_to_html_Blank(self):
		Blank = HTMLNode()
		self.assertEqual(Blank.props_to_html(), "")

	def test_props_Example(self):
		Example = HTMLNode("a", "This is info text",props={"href": "https://boot.dev"})
		self.assertEqual(Example.props_to_html(),' href="https://boot.dev"')

	def test_props_parent(self):
		blank1 =HTMLNode()
		blank2= HTMLNode()
		parent = HTMLNode("p", "I hate typing these",[blank1,blank2], {"one": "two", "three": "four"})
		self.assertEqual(parent.props_to_html(), ' one="two" three="four"')

	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_leaf_to_html_h1(self):
		node = LeafNode("h1", "My coding website")
		self.assertEqual(node.to_html(), "<h1>My coding website</h1>")

	def test_leaf_to_html_link(self):
		node = LeafNode("a", "Proof Boots is evil", props={"href": "https://boot.dev"})
		self.assertEqual(node.to_html(), '<a href="https://boot.dev">Proof Boots is evil</a>')

	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>")

	def test_to_html_with_nothing(self):
		with self.assertRaises(ValueError):
			node = ParentNode("p", [])
			node.to_html()

	def test_to_html_with_childses(self):
		childone = LeafNode("h1", "this should be first")
		childtwo = LeafNode("p", "this should be second")
		parent_node = ParentNode("div", [childone, childtwo])
		self.assertEqual(parent_node.to_html(), "<div><h1>this should be first</h1><p>this should be second</p></div>")

if __name__ == "__main__":
	unittest.main()
