import unittest

from block import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):

    def test_heading_block(self):
        block = "# Heading text"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = "```\nprint('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote\n> Continued quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list_block(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph_block(self):
        block = "This is a regular paragraph with **bold** text and more."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_heading_is_paragraph(self):
        block = "####### Too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_mixed_list_not_valid(self):
        block = "- Item 1\n2. Mixed item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    

if __name__ == "__main__":
    unittest.main()
