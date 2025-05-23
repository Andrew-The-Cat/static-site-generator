import unittest

from textnode import TextNode, TextType
from doc_parser import *

class TestMakrdownParser(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_parse_block_type(self):
        blocktype = block_to_block_type(
            """Hello! This is a paragraph""")
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

        blocktype = block_to_block_type(
            """```Hello! This is code```""")
        self.assertEqual(blocktype, BlockType.CODE)

        blocktype = block_to_block_type(
            """## Hello! This is a heading""")
        self.assertEqual(blocktype, BlockType.HEADING)

        blocktype = block_to_block_type(
            """>Hello! This is a paragraph
But whatever""")
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

        blocktype = block_to_block_type(
            """>Hello! This however is a quote""")
        self.assertEqual(blocktype, BlockType.QUOTE)

        blocktype = block_to_block_type(
            """- Hello! This is a list
- With two items
- and loads of fun""")
        self.assertEqual(blocktype, BlockType.UNORDERED_LIST)

        blocktype = block_to_block_type(
            """1. Hello! This is a ol
2. And it's working as intended!""")
        self.assertEqual(blocktype, BlockType.ORDERED_LIST)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = md_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = md_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):

        md = """
>Hello there
>I am quote
>this is quote right here
        """

        node = md_to_html(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>Hello there I am quote this is quote right here</blockquote></div>")

    def test_heading(self):
        md = """
### HELLO (h3)
"""
        node = md_to_html(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>HELLO (h3)</h3></div>")

    def test_ul(self):
        md = """
- Hello this is list
- this is element 2
- this is element 3
"""

        node = md_to_html(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>Hello this is list</li><li>this is element 2</li><li>this is element 3</li></ul></div>")

    def test_ol(self):
        md = """
1. Hello this is ordered list
2. this one contains _italic_ text
3. and this one ```code```
"""

        node = md_to_html(md)
        html = node.to_html()

        self.assertEqual(html, "<div><ol><li>Hello this is ordered list</li><li>this one contains <i>italic</i> text</li><li>and this one <code>code</code></li></ol></div>")

    def test_title(self):
        md = """
This is the number one
# super monkey fan club
that you will ever see!
"""

        extracrted = extract_title(md)
        self.assertEqual(extracrted, "super monkey fan club")

if __name__ == "__main__":
    unittest.main()