import unittest
from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        node.props_to_html == node2.props_to_html
    def test_eq2(self):
        node = HTMLNode(tag="p")
        node2 = HTMLNode(tag="p")
        node.props_to_html == node2.props_to_html
    def test_not_eq1(self):
        node = HTMLNode("p")
        node2 = HTMLNode("h1")
        node.props_to_html != node2.props_to_html
   
if __name__ == "__main__":
    unittest.main()