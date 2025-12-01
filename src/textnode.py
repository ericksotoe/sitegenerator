from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        check1 = self.text == other.text
        check2 = self.text_type == other.text_type
        check3 = self.url == other.url
        return check1 and check2 and check3

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
