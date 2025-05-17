import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_h1_props(self):
        node= LeafNode(tag="h1",value="Titulo",props={"class": "text_title"})
        self.assertEqual(node.to_html(),"<h1 class=\"text_title\">Titulo</h1>")
    def test_b_props(self):
        node= LeafNode(tag="b",value="Titulo",props={"class": "text_title bold"})
        self.assertEqual(node.to_html(),"<b class=\"text_title bold\">Titulo</b>")
if __name__ == "__main__":
    unittest.main()