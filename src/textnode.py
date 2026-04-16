from enum import Enum
import re

class TextType(Enum):
    TEXT = "Plain"
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code"
    LINK = "Link"
    IMAGE = "Image"
    
class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("Delimiter count mustn't be even")
            else:
                for i in range(len(parts)):
                    if parts[i] == "":
                        continue
                    elif i % 2 == 0:
                        new_nodes.append(TextNode(parts[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(parts[i], text_type))
        else:
            new_nodes.append(node)
                    
    return new_nodes

def split_nodes_image(old_nodes):
    
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            remaining = node.text
            matches = extract_markdown_images(node.text)
            if matches:
                for image_alt, image_url in matches:
                    sections = remaining.split(f"![{image_alt}]({image_url})", 1)
                    
                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                        
                    new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
                    remaining = sections[1]
                    
                if remaining != "":
                    new_nodes.append(TextNode(remaining, TextType.TEXT))
                else:
                    continue
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)

    return new_nodes

def split_nodes_link(old_nodes):
    
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            remaining = node.text
            matches = extract_markdown_links(node.text)
            if matches:
                for link_text, link_url in matches:
                    sections = remaining.split(f"[{link_text}]({link_url})", 1)
                    
                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                        
                    new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                    remaining = sections[1]
                    
                if remaining != "":
                    new_nodes.append(TextNode(remaining, TextType.TEXT))
                else:
                    continue
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches