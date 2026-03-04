from enum import Enum
import re
from htmlnode import ParentNode
from htmlnode import LeafNode
from textnode import TextNode
from textnode import TextType
from functions import text_node_to_html_node
from functions import text_to_text_nodes

class BlockType(Enum):
    PAR = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered list"
    OL = "ordered list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    newlist = []
    for block in blocks:
        if block != "":
            newlist.append(block.strip())
    return newlist

def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEAD
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")
    quoteness = True
    for line in lines:
        if line.startswith(">"):
            continue
        else:
            quoteness = False
            break
    if quoteness == True:
        return BlockType.QUOTE
    ulness = True
    for line in lines:
        if line.startswith("- "):
            continue
        else:
            ulness = False
            break
    if ulness == True:
        return BlockType.UL
    olness = True
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith(f"{i+1}. "):
            continue
        else:
            olness = False
            break
    if olness == True:
        return BlockType.OL
    return BlockType.PAR


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PAR:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEAD:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OL:
        return olist_to_html_node(block)
    if block_type == BlockType.UL:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_text_nodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)