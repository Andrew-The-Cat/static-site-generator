from textnode import *
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 0
    HEADING = 1
    CODE = 2
    QUOTE = 3
    UNORDERED_LIST = 4
    ORDERED_LIST = 5

class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props =props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        return " ".join(map( lambda tup: f'{tup[0]}="{tup[1]}"', self.props.items()))
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children},\n{str(self.props)}\n)"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("all leaf nodes must have a value")
        
        if self.tag == None:
            return str(self.value)
        
        html_props = self.props_to_html()
        if len(html_props) > 0:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("all parent nodes must have a tag")
        if self.children == None or len(self.children) == 0:
            raise ValueError("parent nodes must have at least one child")
        
        html_props = self.props_to_html()
        children_html = "".join( list(map(lambda node: node.to_html(), self.children)))

        if len(html_props) > 0:
            return f"<{self.tag} {self.props_to_html()}>{children_html}</{self.tag}>"
        return f"<{self.tag}>{children_html}</{self.tag}>"
    
