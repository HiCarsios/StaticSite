from enum import Enum
from textnode import *
from htmlnode import *
from inline_markdown import *

def markdown_to_blocks(markdown):
    sections = markdown.split("\n\n")
    returnlist = []
    for s in sections:
        section = s.strip()
        if section:
            returnlist.append(section)
    return returnlist

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown):
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if markdown.startswith(("```\n")) and markdown.endswith(("```")):
        return BlockType.CODE
    multiline = markdown.split("\n")
    quo = False
    uol = False
    ool = False
    for i,line in enumerate(multiline):
        if line.startswith((">", "> ")) and not uol and not ool:
            quo = True
            if i == len(multiline)-1:
                return BlockType.QUOTE
        elif line.startswith(("- ")) and not quo and not ool:
            uol = True
            if i == len(multiline)-1:
                return BlockType.UNORDERED_LIST
        elif line.startswith((f"{i+1}. ")) and not uol and not quo:
            ool = True
            if i == len(multiline)-1:
                return BlockType.ORDERED_LIST
        else:
            break
    return BlockType.PARAGRAPH

def headingno(mark):
    head = 0
    for char in  mark:
        if head == 6:
            return head
        if char == "#":
            head +=1
        else:
            return head

def markdown_to_html_node(markdown):
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                text = " ".join(block.splitlines())
                textnods = text_to_textnodes(text)
                children = [text_node_to_html_node(tn) for tn in textnods]
                section = ParentNode("p", children)
                nodes.append(section)
            case BlockType.HEADING:
                head = headingno(block)
                text = block[head + 1:]
                textnods = text_to_textnodes(text)
                children = [text_node_to_html_node(tn) for tn in textnods]
                h= f"h{head}"
                section = ParentNode(h, children)
                nodes.append(section)
            case BlockType.CODE:
                text = block[4:-3]
                textnode = TextNode(text, TextType.CODE)
                htmlnode = text_node_to_html_node(textnode)
                section = ParentNode("pre", [htmlnode])
                nodes.append(section)
            case BlockType.QUOTE:
                lines = [line.lstrip(">").strip() for line in block.split("\n")]
                text = " ".join(lines)
                textnods = text_to_textnodes(text)
                children = [text_node_to_html_node(tn) for tn in textnods]
                section = ParentNode("blockquote", children)
                nodes.append(section)
            case BlockType.ORDERED_LIST:
                list_items =[]
                for line in block.split("\n"):
                    text = line.partition(". ")[2]
                    textnods = text_to_textnodes(text)
                    children = [text_node_to_html_node(tn) for tn in textnods]
                    list_items.append(ParentNode("li", children))
                section = ParentNode("ol", list_items)
                nodes.append(section)
            case BlockType.UNORDERED_LIST:
                list_items =[]
                for line in block.split("\n"):
                    text = line[2:]
                    textnods = text_to_textnodes(text)
                    children = [text_node_to_html_node(tn) for tn in textnods]
                    list_items.append(ParentNode("li", children))
                section = ParentNode("ul", list_items)
                nodes.append(section)
    return ParentNode("div", nodes)
