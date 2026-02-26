import unittest

from textnode import TextNode
from textnode import TextType
from htmlnode import LeafNode
from functions import extract_markdown_images
from functions import extract_markdown_links

class TestDelim(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_double_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and [link2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual(("link", "https://i.imgur.com/zjjcJKZ.png"), matches[0])
        self.assertEqual(("link2", "https://i.imgur.com/zjjcJKZ.png"), matches[1])

    def test_double_images(self):
        matches = extract_markdown_images(
            "This is text with an ![img](https://i.imgur.com/zjjcJKZ.png) and ![img2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual(("img", "https://i.imgur.com/zjjcJKZ.png"), matches[0])
        self.assertEqual(("img2", "https://i.imgur.com/zjjcJKZ.png"), matches[1])

    def test_both_img(self):
        matches = extract_markdown_images(
            "This is text with an ![img](https://i.imgur.com/zjjcJKZ.png) and [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual(("img", "https://i.imgur.com/zjjcJKZ.png"), matches[0])

    def test_both_link(self):
        matches = extract_markdown_links(
            "This is text with an ![img](https://i.imgur.com/zjjcJKZ.png) and [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual(("link", "https://i.imgur.com/zjjcJKZ.png"), matches[0])




if __name__ == "__main__":
    unittest.main()