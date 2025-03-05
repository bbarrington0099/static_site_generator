import unittest

from textnode import TextNode, TextType
from textnode_parser import *

class TestTextNodeParser(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)        
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with _italic words_", TextType.TEXT)        
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("italic words", TextType.ITALIC)
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("**Bold words** at the beginning", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Bold words", TextType.BOLD),
            TextNode(" at the beginning", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)

    def test_extract_markdown_image(self):
        text = "This is a ![sample image](https://example.com/image.jpg)"
        images = extract_markdown_images(text)
        expected = [("sample image", "https://example.com/image.jpg")]
        self.assertEqual(images, expected)

    def test_extract_markdown_multiple_images(self):
        text = "![image1](https://example.com/image1.jpg) and ![image2](https://example.com/image2.jpg)"
        images = extract_markdown_images(text)
        expected = [
            ("image1", "https://example.com/image1.jpg"),
            ("image2", "https://example.com/image2.jpg"),
        ]
        self.assertEqual(images, expected)

    def test_extract_markdown_link(self):
        text = "This is a [link](https://example.com)"
        links = extract_markdown_links(text)
        expected = [("link", "https://example.com")]
        self.assertEqual(links, expected)

    def test_extract_markdown_multiple_links(self):
        text = "[link1](https://example.com) and [link2](https://example.com)"
        links = extract_markdown_links(text)
        expected = [
            ("link1", "https://example.com"),
            ("link2", "https://example.com"),
        ]
        self.assertEqual(links, expected)

    def test_split_node_images(self):
        node_image = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes_image = split_nodes_images([node_image])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertEqual(new_nodes_image, expected)

    def test_split_node_links(self):
        node_link = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes_link = split_nodes_link([node_link])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(new_nodes_link, expected)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)

if __name__ == "__main__":
    unittest.main()