import unittest

from textnode import TextNode, TextType,text_node_to_html_node


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
        node = TextNode("This is a text node", TextType.TEXT,"https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.TEXT,"https://www.boot.dev")
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
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
if __name__ == "__main__":
    unittest.main()