import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("This is a text node", "p")
        node2 = LeafNode("This is a text node", "p")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = LeafNode("This is a text node", "p")
        node2 = LeafNode("This is a text node", "h1")
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = LeafNode("This is a text node", "p")
        self.assertEqual(repr(node), "HTMLNode(p, This is a text node, None, None)")

if __name__ == "__main__":
    unittest.main()