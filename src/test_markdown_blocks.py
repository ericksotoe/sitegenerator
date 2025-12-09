import unittest

from markdown_blocks import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


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


class TestBlockToBlockType(unittest.TestCase):
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

    def test_headings_all_levels(self):
        # Test all heading levels (1-6)
        for i in range(1, 7):
            block = "#" * i + " heading"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block_variations(self):
        # Test code block with various content
        test_cases = [
            ("```\nprint('hello')\n```", BlockType.CODE),
            ("```python\ndef foo():\n    pass\n```", BlockType.CODE),
            ("```\nline1\nline2\nline3\n```", BlockType.CODE),
            # Should fail as code blocks (not single line)
            ("```not a code block```", BlockType.PARAGRAPH),
        ]

        for block, expected in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), expected)

    def test_list_valid_and_invalid(self):
        # Test ordered and unordered lists
        test_cases = [
            # Unordered lists
            ("- item1\n- item2\n- item3", BlockType.ULIST),
            ("- only one item", BlockType.ULIST),
            ("- item1\n- item2\nnot a list item", BlockType.PARAGRAPH),
            # Ordered lists
            ("1. first\n2. second\n3. third", BlockType.OLIST),
            ("1. only item", BlockType.OLIST),
            ("1. item1\n3. item3", BlockType.PARAGRAPH),  # Skipped number
            ("2. wrong start", BlockType.PARAGRAPH),  # Doesn't start with 1
            ("1. item1\n2. item2\nnot a list", BlockType.PARAGRAPH),
            # Edge cases
            ("-item without space", BlockType.PARAGRAPH),
            ("1.item without space", BlockType.PARAGRAPH),
            ("- ", BlockType.ULIST),  # Empty list item
            ("1. ", BlockType.OLIST),  # Empty ordered item
        ]

        for block, expected in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), expected)

    def test_paragraph_edge_cases(self):
        # Test various paragraph cases
        test_cases = [
            # Simple paragraphs
            ("just text", BlockType.PARAGRAPH),
            ("multiple\nlines\nof text", BlockType.PARAGRAPH),
            # Things that look like other blocks but aren't
            ("#not a heading", BlockType.PARAGRAPH),  # No space after #
            ("```code without closing", BlockType.PARAGRAPH),
            (">quote\nnot continued", BlockType.PARAGRAPH),
            # Empty or whitespace
            ("", BlockType.PARAGRAPH),
            ("   ", BlockType.PARAGRAPH),
            ("\n\n", BlockType.PARAGRAPH),
            # Mixed content
            ("Some text\n- but then a list", BlockType.PARAGRAPH),
            ("1. wrong\n- mixed", BlockType.PARAGRAPH),
        ]

        for block, expected in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), expected)

    def test_nested_or_special_markdown(self):
        # Test special Markdown cases
        test_cases = [
            # Indented code blocks (not fenced)
            ("    code block", BlockType.PARAGRAPH),  # 4 spaces
            # Horizontal rules
            ("---", BlockType.PARAGRAPH),
            ("***", BlockType.PARAGRAPH),
            # Mixed content
            (
                "# Heading\n\nParagraph",
                BlockType.HEADING,
            ),  # Actually should be separate blocks
            # Lists with sub-items
            ("- item\n  - subitem", BlockType.PARAGRAPH),  # Indented sub-item
            # Code block with empty lines
            ("```\n\n\n```", BlockType.CODE),  # Empty code block
        ]

        for block, expected in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), expected)


if __name__ == "__main__":
    unittest.main()
