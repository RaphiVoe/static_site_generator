from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.tag == "img":
            return f"<img src=\"{self.props['src']}\" alt=\"{self.props['alt']}\"/>"
        if not self.value:
            raise ValueError("Value cannot be empty")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"