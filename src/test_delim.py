import unittest

from textnode import TextNode
from textnode import TextType
from htmlnode import LeafNode
from functions import text_node_to_html_node
from functions import split_nodes_delimiter

class TestDelim(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a **bold** text node", TextType.TEXT)
        nodelist = [node, node2]
        nodes = split_nodes_delimiter(nodelist, "**", TextType.BOLD)
        self.assertEqual(nodes[0], TextNode("This is a text node", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("This is a ", TextType.TEXT))
        self.assertEqual(nodes[2], TextNode("bold", TextType.BOLD))
        self.assertEqual(nodes[3], TextNode(" text node", TextType.TEXT))

    def test_italic(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node3 = TextNode("This is a _italic_ text node", TextType.TEXT)
        nodelist = [node, node3]
        nodes = split_nodes_delimiter(nodelist, "_", TextType.ITALIC)
        self.assertEqual(nodes[0], TextNode("This is a text node", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("This is a ", TextType.TEXT))
        self.assertEqual(nodes[2], TextNode("italic", TextType.ITALIC))
        self.assertEqual(nodes[3], TextNode(" text node", TextType.TEXT))

    def test_code(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node4 = TextNode("This is a `code` text node", TextType.TEXT)
        nodelist = [node, node4]
        nodes = split_nodes_delimiter(nodelist, "`", TextType.CODE)
        self.assertEqual(nodes[0], TextNode("This is a text node", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("This is a ", TextType.TEXT))
        self.assertEqual(nodes[2], TextNode("code", TextType.CODE))
        self.assertEqual(nodes[3], TextNode(" text node", TextType.TEXT))

    def test_double_bold(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a **double**, **bold**, text node", TextType.TEXT)
        nodelist = [node, node2]
        nodes = split_nodes_delimiter(nodelist, "**", TextType.BOLD)
        self.assertEqual(nodes[0], TextNode("This is a text node", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("This is a ", TextType.TEXT))
        self.assertEqual(nodes[2], TextNode("double", TextType.BOLD))
        self.assertEqual(nodes[3], TextNode(", ", TextType.TEXT))
        self.assertEqual(nodes[4], TextNode("bold", TextType.BOLD))
        self.assertEqual(nodes[5], TextNode(", text node", TextType.TEXT))

    def test_edge(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("**Early bold** text node", TextType.TEXT)
        nodelist = [node, node2]
        nodes = split_nodes_delimiter(nodelist, "**", TextType.BOLD)
        self.assertEqual(nodes[0], TextNode("This is a text node", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("Early bold", TextType.BOLD))
        self.assertEqual(nodes[2], TextNode(" text node", TextType.TEXT))

    def test_combo(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a **bold** and _italic_ text node", TextType.TEXT)
        node3 = TextNode("This is a text node", TextType.TEXT)
        node4 = TextNode("This is a **bold** and _italic_ text node", TextType.TEXT)
        nodelist = [node, node2]
        nodes = split_nodes_delimiter(nodelist, "**", TextType.BOLD)
        self.assertEqual(nodes[0], TextNode("This is a text node", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("This is a ", TextType.TEXT))
        self.assertEqual(nodes[2], TextNode("bold", TextType.BOLD))
        self.assertEqual(nodes[3], TextNode(" and _italic_ text node", TextType.TEXT))
        nodelist2 = [node3, node4]
        nodes2 = split_nodes_delimiter(nodelist2, "_", TextType.ITALIC)
        self.assertEqual(nodes2[0], TextNode("This is a text node", TextType.TEXT))
        self.assertEqual(nodes2[1], TextNode("This is a **bold** and ", TextType.TEXT))
        self.assertEqual(nodes2[2], TextNode("italic", TextType.ITALIC))
        self.assertEqual(nodes2[3], TextNode(" text node", TextType.TEXT))

    def test_repeat(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a **bold** and _italic_ text node", TextType.TEXT)
        nodelist = [node, node2]
        nodes = split_nodes_delimiter(nodelist, "**", TextType.BOLD)
        nodes2 = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(nodes2[0], TextNode("This is a text node", TextType.TEXT))
        self.assertEqual(nodes2[1], TextNode("This is a ", TextType.TEXT))
        self.assertEqual(nodes2[2], TextNode("bold", TextType.BOLD))
        self.assertEqual(nodes2[3], TextNode(" and ", TextType.TEXT))
        self.assertEqual(nodes2[4], TextNode("italic", TextType.ITALIC))
        self.assertEqual(nodes2[5], TextNode(" text node", TextType.TEXT))



if __name__ == "__main__":
    unittest.main()