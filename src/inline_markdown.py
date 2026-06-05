import re
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node = []
    for nodes in old_nodes:
        if nodes.text_type != TextType.TEXT:
            new_node.append(nodes)
            continue
        splitline = nodes.text.split(delimiter)
        node_section =[]
        if len(splitline) %2 != 1:
            raise Exception("Unclosed delimiter")
        for i, line in enumerate(splitline):
            if line != "":
                if i %2 == 0:
                    splicetext = TextNode(line, TextType.TEXT)
                    node_section.append(splicetext)
                else:
                    splicetext = TextNode(line, text_type)
                    node_section.append(splicetext)
        new_node.extend(node_section)
    return new_node


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_section = []
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for alt, url in images:
            full_markdown = f"![{alt}]({url})"
            parts =remaining_text.split(full_markdown, 1)
            if parts[0] != "":
                noodle = TextNode(parts[0], TextType.TEXT)
                node_section.append(noodle)
            imagenode = TextNode(alt, TextType.IMAGE, url)
            node_section.append(imagenode)
            remaining_text = parts[1]
        if remaining_text != "":
            final_node = TextNode(remaining_text, TextType.TEXT)
            node_section.append(final_node)
        new_nodes.extend(node_section)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_section = []
        images = extract_markdown_links(node.text)
        if not images:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for alt, url in images:
            full_markdown = f"[{alt}]({url})"
            parts =remaining_text.split(full_markdown, 1)
            if parts[0] != "":
                noodle = TextNode(parts[0], TextType.TEXT)
                node_section.append(noodle)
            imagenode = TextNode(alt, TextType.LINK, url)
            node_section.append(imagenode)
            remaining_text = parts[1]
        if remaining_text != "":
            final_node = TextNode(remaining_text, TextType.TEXT)
            node_section.append(final_node)
        new_nodes.extend(node_section)
    return new_nodes


def text_to_textnodes(text):
    if not text:
        return []
    blank_node = TextNode(text, TextType.TEXT)
    checkbold = split_nodes_delimiter([blank_node], "**", TextType.BOLD)
    checkitalic = split_nodes_delimiter(checkbold, "_", TextType.ITALIC)
    checkcode = split_nodes_delimiter(checkitalic, "`", TextType.CODE)
    stepone = split_nodes_link(checkcode)
    steptwo = split_nodes_image(stepone)
    return steptwo
