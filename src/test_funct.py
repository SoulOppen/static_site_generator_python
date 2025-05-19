import unittest
from funct import markdown_to_html_node, split_nodes_delimiter, extract_markdown_images,extract_markdown_links,split_nodes_image,split_nodes_link,text_to_textnodes,markdown_to_blocks,extract_title

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
    def test_single_image(self):
        nodes = [TextNode("Esto es una ![imagen](url.jpg)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Esto es una ")
        self.assertEqual(result[1].text, "imagen")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "url.jpg")
    def test_multiple_images(self):
        nodes = [TextNode("Inicio ![uno](a.jpg) medio ![dos](b.jpg) fin", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[3].text_type, TextType.IMAGE)
    def test_no_images(self):
        nodes = [TextNode("Sin imágenes aquí", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(result, nodes)
    def test_non_text_node(self):
        nodes = [TextNode("imagen", TextType.IMAGE, "img.jpg")]
        result = split_nodes_image(nodes)
        self.assertEqual(result, nodes)
    def test_single_link(self):
        nodes = [TextNode("Ve a [Google](https://google.com)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Ve a ")
        self.assertEqual(result[1].text, "Google")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://google.com")
    def test_multiple_links(self):
        nodes = [TextNode("[Uno](1.com) y [Dos](2.com)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text_type, TextType.LINK)
        self.assertEqual(result[1].text, " y ")
        self.assertEqual(result[2].text_type, TextType.LINK)

    def test_no_links(self):
        nodes = [TextNode("Sin enlaces", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(result, nodes)

    def test_non_text_node(self):
        nodes = [TextNode("Google", TextType.LINK, "https://google.com")]
        result = split_nodes_link(nodes)
        self.assertEqual(result, nodes)
    
    def test_plain_text(self):
        text = "Just plain text."
        result = text_to_textnodes(text)
        self.assertEqual(result[0].text, text)
        self.assertEqual(result[0].text_type, TextType.TEXT)
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks_varied(self):
        md = """
# Heading 1

Paragraph with some text.

- Item 1
- Item 2

Another paragraph with **bold** text and a [link](https://example.com).

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading 1",
                "Paragraph with some text.",
                "- Item 1\n- Item 2",
                "Another paragraph with **bold** text and a [link](https://example.com).",
            ],
        )
    def test_basic_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_title_with_extra_spaces(self):
        self.assertEqual(extract_title("#    Hello World   "), "Hello World")

    def test_multiline_input(self):
        markdown = "Some text\n# Main Title\nMore text"
        self.assertEqual(extract_title(markdown), "Main Title")

    def test_no_title_raises_exception(self):
        with self.assertRaises(Exception) as context:
            extract_title("Just some text\n## Subheading")
        self.assertEqual(str(context.exception), "No title found")

    def test_ignores_multiple_hashes(self):
        markdown = "## Subtitle\n### Another\n# Actual Title"
        self.assertEqual(extract_title(markdown), "Actual Title")

    def test_title_not_at_start_of_line(self):
        markdown = "text before # not a real title"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_empty_input(self):
        with self.assertRaises(Exception):
            extract_title("")

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )
if __name__ == "__main__":
    unittest.main()