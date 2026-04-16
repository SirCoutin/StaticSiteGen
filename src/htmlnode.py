from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value to convert to HTML")
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}>{self.props_to_html()}{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to convert to HTML")
        if self.children is None:
            raise ValueError("ParentNode must have children to convert to HTML")
        
        result = f"<{self.tag}>"
        
        for child in self.children:
            result += child.to_html()
            
        return result + f"</{self.tag}>"
    
def text_node_to_html_node(TextNode):
    match TextNode.text_type:
        case TextType.TEXT:
            return LeafNode(None, TextNode.text)
        case TextType.BOLD:
            return LeafNode("b", TextNode.text)
        case TextType.ITALIC:
            return LeafNode("i", TextNode.text)
        case TextType.CODE:
            return LeafNode("code", TextNode.text)
        case TextType.LINK:
            return LeafNode("a", TextNode.text, {"href": TextNode.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src": TextNode.url, "alt": TextNode.text})
        case _:
            raise ValueError(f"Unsupported TextType: {TextNode.text_type}")