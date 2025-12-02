import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    # Test equality
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    # Test different texttypes
    def test_not_eq(self):
        node = TextNode("this is node 1", TextType.BOLD)
        node2 = TextNode("this is node 2", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    # Test URL equality
    def test_eq_with_url(self):
        node = TextNode("Click here", TextType.LINK, "https://www.example.com")
        node2 = TextNode("Click here", TextType.LINK, "https://www.example.com")
        self.assertEqual(node, node2)

    def test_not_eq_different_urls(self):
        node = TextNode("Click here", TextType.LINK, "https://www.example.com")
        node2 = TextNode("Click here", TextType.LINK, "https://www.different.com")
        self.assertNotEqual(node, node2)

    # Test one node with URL, one without
    def test_not_eq_url_none_vs_set(self):
        node = TextNode("Same text", TextType.TEXT)
        node2 = TextNode("Same text", TextType.TEXT, "https://example.com")
        self.assertNotEqual(node, node2)

    # Test different text types with same text
    def test_not_eq_different_types(self):
        node = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    # Test all properties different
    def test_not_eq_all_different(self):
        node = TextNode("Text 1", TextType.BOLD, "url1")
        node2 = TextNode("Text 2", TextType.ITALIC, "url2")
        self.assertNotEqual(node, node2)

    # Test repr method
    def test_repr(self):
        node = TextNode("Hello World", TextType.CODE, "https://example.com")
        expected = "TextNode(Hello World, code, https://example.com)"
        self.assertEqual(repr(node), expected)

    def test_repr_no_url(self):
        node = TextNode("Hello World", TextType.TEXT)
        expected = "TextNode(Hello World, text, None)"
        self.assertEqual(repr(node), expected)

    # Test different text cases
    def test_eq_case_sensitive(self):
        node = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("hello", TextType.TEXT)
        self.assertNotEqual(node, node2)  # Should be case sensitive

    # Test empty string handling
    def test_eq_empty_text(self):
        node = TextNode("", TextType.TEXT)
        node2 = TextNode("", TextType.TEXT)
        self.assertEqual(node, node2)

    # Test None URL vs empty string URL
    def test_eq_none_url_vs_empty_string(self):
        node = TextNode("Text", TextType.TEXT)
        node2 = TextNode("Text", TextType.TEXT, "")
        self.assertNotEqual(node, node2)

    # Test all TextType enum values
    def test_all_text_types(self):
        for text_type in TextType:
            node = TextNode("Test", text_type)
            # Just ensure no errors
            self.assertEqual(node.text_type, text_type)
            self.assertEqual(node.text, "Test")

    # Test initialization defaults
    def test_default_url_is_none(self):
        node = TextNode("Test", TextType.TEXT)
        self.assertIsNone(node.url)


if __name__ == "__main__":
    unittest.main()
