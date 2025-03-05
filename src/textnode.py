from enum import Enum
from leafnode import LeafNode

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
        self.text_type = text_type.value
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def to_html(self):
        text_type = TextType(self.text_type)

        dispatch = {
            TextType.TEXT: lambda: LeafNode(self.text, None),
            TextType.BOLD: lambda: LeafNode(self.text, "b"),
            TextType.ITALIC: lambda: LeafNode(self.text, "i"),
            TextType.CODE: lambda: LeafNode(self.text, "code"),
            TextType.LINK: lambda: LeafNode(self.text, "a", {"href": self.url}),
            TextType.IMAGE: lambda: LeafNode("","img", {"src": self.url, "alt": self.text}),
        }

        if text_type not in dispatch:
            raise ValueError(f"Unsupported TextType: {self.text_type}")

        return dispatch[text_type]().to_html()