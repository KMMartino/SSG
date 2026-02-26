import unittest

from textnode import TextNode
from textnode import TextType
from htmlnode import LeafNode
from functions import extract_markdown_images, split_nodes_link
from functions import extract_markdown_links
from functions import split_nodes_image

class TestDelim(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMG, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_consecutive(self):
        node = TextNode(
            "![img1](url1)![img2](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMG, "url1"),
                TextNode("img2", TextType.IMG, "url2"),
            ],
            new_nodes,
        )

    def test_split_links_edges(self):
        node = TextNode(
            "[link at start](url1) some text [link at end](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link at start", TextType.LINK, "url1"),
                TextNode(" some text ", TextType.TEXT),
                TextNode("link at end", TextType.LINK, "url2"),
            ],
            new_nodes,
        )

    def test_split_images_ignores_links(self):
        node = TextNode(
            "This is an ![image](url1) and this is a [link](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("image", TextType.IMG, "url1"),
                TextNode(" and this is a [link](url2)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_no_matches(self):
        node = TextNode("Just plain text with no special syntax.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Just plain text with no special syntax.")

if __name__ == "__main__":
    unittest.main()