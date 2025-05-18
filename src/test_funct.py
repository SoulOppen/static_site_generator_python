import unittest
from funct import split_nodes_delimiter, extract_markdown_images,extract_markdown_links
from textnode import TextType,TextNode
class TestFunc(unittest.TestCase):

    def test_code_delimiter(self):
        node = TextNode("Here is `inline code` example", TextType.TEXT)
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("inline code", TextType.CODE),
            TextNode(" example", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, expected)

    def test_italic_delimiter(self):
        node = TextNode("An _italic_ word", TextType.TEXT)
        expected = [
            TextNode("An ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, expected)

    def test_multiple_delimiters(self):
        node = TextNode("A _italic_ and another _word_", TextType.TEXT)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and another ", TextType.TEXT),
            TextNode("word", TextType.ITALIC),
        ]
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, expected)

    def test_no_delimiters(self):
        node = TextNode("Plain text only", TextType.TEXT)
        expected = [TextNode("Plain text only", TextType.TEXT)]
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, expected)

    def test_non_text_node(self):
        node = TextNode("Already bold", TextType.BOLD)
        expected = [node]
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, expected)
    def test_image_with_alt_text(self):
        text = "Una imagen: ![Descripción](https://example.com/img.png)"
        expected = [("Descripción", "https://example.com/img.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_without_alt_text(self):
        text = "Sin texto alternativo: ![](https://example.com/img.png)"
        expected = [("", "https://example.com/img.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = "![Uno](url1) texto ![Dos](url2)"
        expected = [("Uno", "url1"), ("Dos", "url2")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_no_images(self):
        text = "Texto sin imágenes"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)
    def test_simple_link(self):
        text = "Un link: [Google](https://google.com)"
        expected = [("Google", "https://google.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = "[Uno](url1) y [Dos](url2)"
        expected = [("Uno", "url1"), ("Dos", "url2")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_ignores_image(self):
        text = "Esto es una imagen: ![img](url)"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_empty_text(self):
        text = "Link sin texto: [](https://ejemplo.com)"
        expected = [("", "https://ejemplo.com")]
        self.assertEqual(extract_markdown_links(text), expected)


if __name__ == "__main__":
    unittest.main()