import unittest

from textnode import TextNode, TextType
from doc_parser import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_dif(self):
        node = TextNode("This is text", TextType.TEXT, "http://localhost")
        node2 = TextNode("This is other text", TextType.TEXT, "http://localhost")
        self.assertNotEqual(node, node2)
        node = TextNode("This is text", TextType.TEXT)
        node2 = TextNode("This is text", TextType.TEXT, "http://localhost")
        self.assertNotEqual(node, node2)
        node = TextNode("This is text", TextType.BOLD)
        node2 = TextNode("This is text", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("sth", TextType.CODE)
        self.assertEqual(node.url, None)

    def test_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

        nodes = [
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("This is another text with an _itallic block_ word", TextType.TEXT)
        ]

        new_nodes = split_nodes_delimiter(split_nodes_delimiter(nodes, '`', TextType.CODE), '_', TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT, None), TextNode("code block", TextType.CODE, None), TextNode(" word", TextType.TEXT, None), TextNode("This is another text with an ", TextType.TEXT, None), TextNode("itallic block", TextType.ITALIC, None), TextNode(" word", TextType.TEXT, None)])

if __name__ == "__main__":
    unittest.main()