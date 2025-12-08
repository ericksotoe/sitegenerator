import unittest

from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownToHTML(unittest.TestCase):
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

    def test_markdown_to_blocks_newlines(self):
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

    # Test with empty input string
    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    # Test with only whitespace chars
    def test_only_whitespace(self):
        md = "   \n\t\n  \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    # Test with single block and no trailing newline
    def test_single_block_no_newline(self):
        md = "Single block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Single block"])

    # Test with single block with trailing newline
    def test_single_block_with_newline(self):
        md = "Single block\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Single block"])

    # Test blocks that have leading/trailing spaces
    def test_blocks_with_trailing_spaces(self):
        md = "   Block with spaces   \n\n  Another block  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block with spaces", "Another block"])

    # Test blocks that contain empty lines within them (not as separators)
    def test_blocks_with_empty_lines_inside(self):
        md = "Line 1\n\nLine 3\n\n\nLine 4"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Line 1", "Line 3", "Line 4"])

    # Test with many consecutive newlines as separators
    def test_very_long_separators(self):
        md = "First\n\n\n\n\n\n\n\nSecond"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First", "Second"])

    # Test markdown that starts with multiple newlines
    def test_blocks_starting_with_newlines(self):
        md = "\n\n\nFirst block\n\nSecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    # Test markdwon that ends with multiple newlines
    def test_blocks_ending_with_newlines(self):
        md = "First block\n\nSecond block\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    # Test with special characters that might affect parsing
    def test_special_characters_in_blocks(self):
        md = "Block with \\n escaped newline\n\nAnother block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block with \\n escaped newline", "Another block"])

    # Test if single newline is treated as part of the same block
    def test_single_newline_separation(self):
        md = "Line 1\nLine 2\n\nLine 3\nLine 4"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Line 1\nLine 2", "Line 3\nLine 4"])

    # Test with tab chars in content
    def test_tab_characters(self):
        md = "Block with\ttab\n\n\tIndented block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block with\ttab", "Indented block"])

    # Test with unicode chars
    def test_unicode_characters(self):
        md = "Block with emoji 😀\n\nAnother block with unicode: café"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks, ["Block with emoji 😀", "Another block with unicode: café"]
        )

    # Test with various markdown syntax elements
    def test_markdown_syntax_elements(self):
        md = "# Heading\n\nParagraph with **bold** and _italic_\n\n- List item 1\n- List item 2\n\n> Blockquote"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph with **bold** and _italic_",
                "- List item 1\n- List item 2",
                "> Blockquote",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
