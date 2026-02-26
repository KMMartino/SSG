from sys import api_version
import re
from textnode import TextNode
from textnode import TextType
from htmlnode import LeafNode

def text_node_to_html_node(textnode):
    if textnode.text_type == TextType.TEXT:
        return LeafNode(None, textnode.text, None)
    elif textnode.text_type == TextType.BOLD:
        return LeafNode("b", textnode.text, None)
    elif textnode.text_type == TextType.ITALIC:
        return LeafNode("i", textnode.text, None)
    elif textnode.text_type == TextType.CODE:
        return LeafNode("code", textnode.text, None)
    elif textnode.text_type == TextType.LINK:
        return LeafNode("a", textnode.text, {"href": f"{textnode.url}"})
    elif textnode.text_type == TextType.IMG:
        return LeafNode("img", "", {"src": f"{textnode.url}", "alt": f"{textnode.text}"})
    else:
        raise Exception("Invalid textnode")
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif delimiter in node.text:
            splits = node.text.split(delimiter)
            if len(splits) % 2 == 0:
                raise Exception("Error: no closing for opened item")
            else:
                counter = 0
                for i in range(len(splits)):
                    if splits[i] == "":
                        counter += 1
                        continue
                    type = TextType.TEXT
                    if counter % 2 == 1:
                        type = text_type  
                    new_nodes.append(TextNode(splits[i], type))
                    counter += 1
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    returnlist = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            images = extract_markdown_images(node.text)
            if len(images) == 0:
                returnlist.append(node)
            else:
                current = node.text
                for i in range(len(images)):
                    img = images[i]
                    fulllink = f"![{img[0]}]({img[1]})"
                    splits = current.split(fulllink, 1)
                    if splits[0] != "":
                        returnlist.append(TextNode(splits[0], TextType.TEXT))
                    returnlist.append(TextNode(img[0], TextType.IMG, img[1]))
                    if i == len(images) - 1:
                        if splits[1] != "":
                            returnlist.append(TextNode(splits[1], TextType.TEXT))
                    else:
                        current = splits[1]
        else:
            returnlist.append(node)
    return returnlist


def split_nodes_link(old_nodes):
    returnlist = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)
            if len(links) == 0:
                returnlist.append(node)
            else:
                current = node.text
                for i in range(len(links)):
                    link = links[i]
                    fulllink = f"[{link[0]}]({link[1]})"
                    splits = current.split(fulllink, 1)
                    if splits[0] != "":
                        returnlist.append(TextNode(splits[0], TextType.TEXT))
                    returnlist.append(TextNode(link[0], TextType.LINK, link[1]))
                    if i == len(links) - 1:
                        if splits[1] != "":
                            returnlist.append(TextNode(splits[1], TextType.TEXT))
                    else:
                        current = splits[1]
        else:
            returnlist.append(node)
    return returnlist

def text_to_text_nodes(text):
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes