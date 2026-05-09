print("hello world")
from textnode import *

def main():
	Nodetest = Textnode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
	print(Nodetest)



main()
