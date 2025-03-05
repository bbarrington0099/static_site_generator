import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("This is a text node", "p")
        node2 = HTMLNode("This is a text node", "p")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = HTMLNode("This is a text node", "p")
        node2 = HTMLNode("This is a text node", "h1")
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = HTMLNode("This is a text node", "p")
        self.assertEqual(repr(node), "HTMLNode(This is a text node, p, None, None)")

if __name__ == "__main__":
    unittest.main()