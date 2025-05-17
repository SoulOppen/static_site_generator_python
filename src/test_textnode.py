import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD,"https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD,"https://www.boot.dev")
        self.assertEqual(node, node2)
    def test_eq3(self):
        node = TextNode("This is a text node", TextType.NORMAL,"https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.NORMAL,"https://www.boot.dev")
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("This is a text", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_eq4(self):
        node = TextNode("This is a text", TextType.BOLD,None)
        node2 = TextNode("This is a text", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_not_eq2(self):
        node = TextNode("This is a text", TextType.ITALIC)
        node2 = TextNode("This is a text", TextType.BOLD)
        self.assertNotEqual(node, node2)
if __name__ == "__main__":
    unittest.main()