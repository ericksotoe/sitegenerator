import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    # Test initialization with default values
    def test_init_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    # Test initialization with all parameters
    def test_init_with_all_params(self):
        props = {"href": "https://example.com", "target": "_blank"}
        children = [HTMLNode("p", "Child 1"), HTMLNode("p", "Child 2")]
        node = HTMLNode("a", "Click me", children, props)
        
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click me")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    # Test initialization with only some parameters
    def test_init_partial_params(self):
        node = HTMLNode("p", "Some text")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Some text")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    # Test props_to_html with no props
    def test_props_to_html_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    # Test props_to_html with one prop
    def test_props_to_html_one_prop(self):
        node = HTMLNode(props={"href": "https://example.com"})
        expected = ' href="https://example.com"'
        self.assertEqual(node.props_to_html(), expected)

    # Test props_to_html with multiple props
    def test_props_to_html_multiple_props(self):
        props = {"href": "https://example.com", "class": "btn", "id": "link1"}
        node = HTMLNode(props=props)
        result = node.props_to_html()
        
        self.assertIn('href="https://example.com"', result)
        self.assertIn('class="btn"', result)
        self.assertIn('id="link1"', result)
        self.assertTrue(result.startswith(" "))
        self.assertEqual(len(result.split()), 3)  # Should have 3 key-value pairs with spaces

    # Test props_to_html with empty props dict
    def test_props_to_html_empty_dict(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    # Test to_html raises NotImplementedError
    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    # Test __repr__ with all fields
    def test_repr_complete(self):
        props = {"href": "https://example.com"}
        children = [HTMLNode("span", "child")]
        node = HTMLNode("a", "link", children, props)
        
        repr_string = repr(node)
        self.assertIn("tag: a", repr_string)
        self.assertIn("value: link", repr_string)
        self.assertIn("children: [", repr_string)
        self.assertIn("props: {'href': 'https://example.com'}", repr_string)

    # Test __repr__ with None values
    def test_repr_none_values(self):
        node = HTMLNode()
        repr_string = repr(node)
        self.assertIn("tag: None", repr_string)
        self.assertIn("value: None", repr_string)
        self.assertIn("children: None", repr_string)
        self.assertIn("props: None", repr_string)

    # Test __repr__ with empty children list
    def test_repr_empty_children(self):
        node = HTMLNode("div", children=[])
        repr_string = repr(node)
        self.assertIn("children: []", repr_string)

    # Test __repr__ with empty props dict
    def test_repr_empty_props(self):
        node = HTMLNode("div", props={})
        repr_string = repr(node)
        self.assertIn("props: {}", repr_string)

    # Test with different types of children
    def test_children_mixed_types(self):
        child1 = HTMLNode("span", "inline")
        child2 = HTMLNode("div", "block")
        node = HTMLNode("body", None, [child1, child2])
        
        self.assertEqual(len(node.children), 2)
        self.assertEqual(node.children[0].tag, "span")
        self.assertEqual(node.children[1].tag, "div")

    # Test nested children structure
    def test_nested_children(self):
        grandchild = HTMLNode("span", "grandchild")
        child = HTMLNode("div", None, [grandchild])
        parent = HTMLNode("body", None, [child])
        
        self.assertEqual(parent.children[0].tag, "div")
        self.assertEqual(parent.children[0].children[0].tag, "span")

    # Test props with boolean attributes (common in HTML)
    def test_props_boolean_attributes(self):
        props = {"disabled": "", "checked": "", "required": ""}
        node = HTMLNode("input", props=props)
        result = node.props_to_html()
        
        # Should render as disabled="" etc.
        self.assertIn('disabled=""', result)
        self.assertIn('checked=""', result)
        self.assertIn('required=""', result)

    # Test props with numeric values
    def test_props_numeric_values(self):
        props = {"width": "100", "height": 200, "tabindex": 1}
        node = HTMLNode("img", props=props)
        result = node.props_to_html()
        
        self.assertIn('width="100"', result)
        self.assertIn('height="200"', result)
        self.assertIn('tabindex="1"', result)

    # Test that props_to_html doesn't modify original props
    def test_props_to_html_immutable(self):
        original_props = {"href": "https://example.com", "class": "link"}
        node = HTMLNode(props=original_props.copy())
        
        # Call props_to_html multiple times
        result1 = node.props_to_html()
        result2 = node.props_to_html()
        
        self.assertEqual(result1, result2)
        self.assertEqual(node.props, original_props)

if __name__ == "__main__":
    unittest.main()