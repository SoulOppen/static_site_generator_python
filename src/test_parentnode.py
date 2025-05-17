import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_parent_node_with_two_children(self):
        child1 = LeafNode(tag="p",value="Hola")
        child2 = LeafNode(tag="p", value="Mundo")
        parent = ParentNode("div", [child1, child2])
        expected_html = "<div><p>Hola</p><p>Mundo</p></div>"
        self.assertEqual(parent.to_html(), expected_html)

    def test_parent_node_with_props(self):
        child = LeafNode(tag="span",value="Texto")
        parent = ParentNode("div", [child], {"class": "box"})
        expected_html = '<div class="box"><span>Texto</span></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_parent_node_not_equal(self):
        child1 = LeafNode(tag="p", value="Uno")
        child2 = LeafNode(tag="p", value="Dos")
        parent = ParentNode("div", [child1, child2])
        not_expected = "<div><p>Uno</p><p>Dos</div>"  # Mal cierre
        self.assertNotEqual(parent.to_html(), not_expected)
    def test_to_html_with_children(self):
        child_node = LeafNode(tag="span",value="child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        
    def  test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
if __name__ == "__main__":
    unittest.main()