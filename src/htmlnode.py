


class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        value = ""
        if self.props != None:
            for item in self.props:
                value+= f' {item}="{self.props[item]}"'
        return value

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag = tag, value = value, children = None, props = props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("no value set")
        elif self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag = tag, value = None, children = children, props = props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("no tag set")
        elif self.children == None:
            raise ValueError("no children set")
        else:
            internal = ""
            for child in self.children:
                internal += child.to_html()
            return f"<{self.tag}{self.props_to_html()}>{internal}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"