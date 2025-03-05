from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag must be set")
        if not self.children:
            raise ValueError("Children must be set")
        children = "".join([child.to_html() for child in self.children])
        props = self.props_to_html()
        return f"<{self.tag}{' ' if self.props else ''}{props}>{children}</{self.tag}>"