from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
	TEXT = "text"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"


class TextNode:
	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url= url

	def __eq__(self, Node):
		if self.text == Node.text and self.text_type == Node.text_type and self.url == Node.url:
			return True
		return False

	def __repr__(self):
		returnstring =  f"TextNode({self.text}, {self.text_type.value}, {self.url})"
		return returnstring

def text_node_to_html_node(text_node):
	match text_node.text_type:
		case TextType.TEXT:
			node = LeafNode(None, text_node.text)
			return node
		case TextType.BOLD:
			node = LeafNode("b", text_node.text)
			return node
		case TextType.ITALIC:
			node = LeafNode("i", text_node.text)
			return node
		case TextType.CODE:
			node = LeafNode("code", text_node.text)
			return node
		case TextType.LINK:
			node = LeafNode("a", text_node.text, {"href": text_node.url})
			return node
		case TextType.IMAGE:
			node = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
			return node
		case _:
			raise ValueError(f"invalid text type: {text_node.text}")
