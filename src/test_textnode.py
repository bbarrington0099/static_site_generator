import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")

    def test_to_html_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node.to_html(), "This is a text node")

    def test_to_html_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.to_html(), "<b>This is a text node</b>")

    def test_to_html_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node.to_html(), "<i>This is a text node</i>")

    def test_to_html_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node.to_html(), "<code>This is a text node</code>")

    def test_to_html_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.example.com")
        self.assertEqual(node.to_html(), '<a href="https://www.example.com">This is a text node</a>')
    
    def test_to_html_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.example.com/image.jpg")
        self.assertEqual(node.to_html(), '<img src="https://www.example.com/image.jpg" alt="This is a text node" />')



if __name__ == "__main__":
    unittest.main()