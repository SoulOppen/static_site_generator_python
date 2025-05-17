class HTMLNode():
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag=tag
        self.value=value
        self.children=children
        self.props=props
    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")
    def props_to_html(self):

        if self.prop is None:
            return ""
        str = ""
        for key, value in self.props.items():
            str +=f" {key}=\"{value}\""
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
