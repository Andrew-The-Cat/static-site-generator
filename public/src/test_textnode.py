import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()