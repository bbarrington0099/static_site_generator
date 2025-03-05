from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag is None:
            return self.value
        if self.tag == "img":
            return f"<{self.tag}{' ' if self.props else ''}{self.props_to_html()} />"
        return f"<{self.tag}{' ' if self.props else ''}{self.props_to_html()}>{self.value}</{self.tag}>"