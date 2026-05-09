from enum import Enum

class TextType(Enum):
	PLAIN = "text"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"


class Textnode:
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
