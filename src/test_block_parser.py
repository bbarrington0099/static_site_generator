import unittest

from block_parser import *

class TestBlockParser(unittest.TestCase):
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

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("regular paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```python\nprint('Hello, World!')"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- List item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. List item"), BlockType.ORDERED_LIST)

    
    def test_markdown_to_html_node(self):
        markdown = "This is a simple paragraph."
        result = markdown_to_html_node(markdown)
        expected_html = "<div><p>This is a simple paragraph.</p></div>"
        self.assertEqual(result.to_html(), expected_html)

        markdown = "# Heading\n\nThis is a paragraph below the heading."
        result = markdown_to_html_node(markdown)
        expected_html = "<div><h1>Heading</h1><p>This is a paragraph below the heading.</p></div>"
        self.assertEqual(result.to_html(), expected_html)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
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

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )
   

    

if __name__ == "__main__":
    unittest.main()