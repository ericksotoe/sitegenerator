import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    # Test basic tag rendering
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    # Test empty value handling - Based on your code, it raises error
    def test_empty_value_raises_error(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "LeafNode must have a value")

    def test_none_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "LeafNode must have a value")

    # Test with no tag but empty string value
    def test_no_tag_empty_value_raises_error(self):
        node = LeafNode(None, "")
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "LeafNode must have a value")

    # Test various HTML tags
    def test_leaf_to_html_heading(self):
        node = LeafNode("h1", "Main Title")
        self.assertEqual(node.to_html(), "<h1>Main Title</h1>")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Content here")
        self.assertEqual(node.to_html(), "<div>Content here</div>")

    def test_leaf_to_html_span(self):
        node = LeafNode("span", "inline content")
        self.assertEqual(node.to_html(), "<span>inline content</span>")

    def test_leaf_to_html_li(self):
        node = LeafNode("li", "List item")
        self.assertEqual(node.to_html(), "<li>List item</li>")

    # Test with multiple props
    def test_leaf_to_html_multiple_props(self):
        node = LeafNode(
            "button",
            "Submit",
            {"type": "submit", "class": "btn btn-primary", "id": "submit-btn"},
        )
        html = node.to_html()
        self.assertIn("<button", html)
        self.assertIn(">Submit</button>", html)
        self.assertIn('type="submit"', html)
        self.assertIn('class="btn btn-primary"', html)
        self.assertIn('id="submit-btn"', html)

    # Test with boolean attributes - Note: these elements need non-empty values
    def test_leaf_to_html_boolean_props_with_value(self):
        node = LeafNode(
            "input", "value", {"type": "checkbox", "checked": "", "disabled": ""}
        )
        html = node.to_html()
        self.assertIn("<input", html)
        self.assertIn(">value</input>", html)
        self.assertIn('type="checkbox"', html)
        self.assertIn('checked=""', html)
        self.assertIn('disabled=""', html)

    # Test self-closing tags - These need non-empty values
    def test_leaf_to_html_img_with_value(self):
        node = LeafNode(
            "img",
            " ",
            {  # Space as value
                "src": "image.jpg",
                "alt": "An image",
            },
        )
        html = node.to_html()
        self.assertIn("<img", html)
        self.assertIn("> </img>", html)
        self.assertIn('src="image.jpg"', html)
        self.assertIn('alt="An image"', html)

    # Test with special characters in value
    def test_leaf_to_html_special_characters(self):
        node = LeafNode("p", "Special & < > \" ' characters")
        html = node.to_html()
        self.assertEqual(html, "<p>Special & < > \" ' characters</p>")

    # Test with special characters in props
    def test_leaf_to_html_special_characters_in_props(self):
        node = LeafNode(
            "a",
            "Link",
            {
                "href": "https://example.com?q=test&id=1",
                "data-info": 'some "quoted" text',
            },
        )
        html = node.to_html()
        self.assertIn('href="https://example.com?q=test&id=1"', html)
        self.assertIn('data-info="some "quoted" text"', html)

    # Test initialization with different parameter combinations
    def test_init_no_props(self):
        node = LeafNode("p", "text")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "text")
        self.assertEqual(node.props, None)  # LeafNode passes None to parent
        self.assertEqual(node.children, None)  # LeafNode explicitly passes None

    def test_init_with_props(self):
        props = {"class": "highlight", "id": "para1"}
        node = LeafNode("p", "text", props)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "text")
        self.assertEqual(node.props, props)

    # Test __repr__ method - matches your actual output
    def test_repr_no_props(self):
        node = LeafNode("p", "text")
        expected = "LeafNode(p, text, None)"
        self.assertEqual(repr(node), expected)

    def test_repr_with_props(self):
        node = LeafNode("a", "link", {"href": "https://example.com"})
        expected = "LeafNode(a, link, {'href': 'https://example.com'})"
        self.assertEqual(repr(node), expected)

    def test_repr_no_tag(self):
        node = LeafNode(None, "raw text")
        expected = "LeafNode(None, raw text, None)"
        self.assertEqual(repr(node), expected)

    # Test edge cases with whitespace in value
    def test_leaf_to_html_with_whitespace(self):
        node = LeafNode("pre", "  indented text\n  with newline  ")
        self.assertEqual(node.to_html(), "<pre>  indented text\n  with newline  </pre>")

    # Test that children is always None (as per LeafNode definition)
    def test_leaf_node_children_is_none(self):
        node = LeafNode("p", "text")
        self.assertEqual(node.children, None)  # LeafNode passes None to parent

    # Test props_to_html inheritance
    def test_props_to_html_inherited(self):
        node = LeafNode("a", "link", {"href": "#", "class": "btn"})
        props_html = node.props_to_html()
        self.assertIn('href="#"', props_html)
        self.assertIn('class="btn"', props_html)

    # Test props_to_html with None props
    def test_props_to_html_none_props(self):
        node = LeafNode("p", "text")  # props defaults to None
        self.assertEqual(node.props_to_html(), "")

    # Test empty tag name
    def test_leaf_to_html_empty_string_tag(self):
        node = LeafNode("", "content")
        self.assertEqual(node.to_html(), "<>content</>")

    # Test numeric values
    def test_leaf_to_html_numeric_value(self):
        node = LeafNode("span", 123)
        self.assertEqual(node.to_html(), "<span>123</span>")

    def test_leaf_to_html_none_value_in_repr(self):
        node = LeafNode("p", None)
        # Value should be None in repr even though it won't render
        self.assertIn("None", repr(node))

    # Test that to_html doesn't modify instance state
    def test_to_html_immutable(self):
        node = LeafNode("p", "text", {"class": "test"})
        html1 = node.to_html()
        html2 = node.to_html()
        self.assertEqual(html1, html2)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "text")
        self.assertEqual(node.props, {"class": "test"})

    # Test with very long values
    def test_leaf_to_html_long_value(self):
        long_text = "a" * 1000
        node = LeafNode("div", long_text)
        expected = f"<div>{long_text}</div>"
        self.assertEqual(node.to_html(), expected)

    # Test that empty string is not valid for any tag
    def test_leaf_no_empty_values_allowed(self):
        # Test a few different tags
        for tag in ["p", "div", "span", "a", "h1"]:
            node = LeafNode(tag, "")
            with self.assertRaises(ValueError):
                node.to_html()

    # Test spaces are valid values
    def test_leaf_space_is_valid_value(self):
        node = LeafNode("p", " ")
        self.assertEqual(node.to_html(), "<p> </p>")


if __name__ == "__main__":
    unittest.main()
