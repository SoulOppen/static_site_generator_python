from enum import Enum
from leafnode import LeafNode
class TextType(Enum):
  TEXT="normal" 
  BOLD="bold"
  ITALIC="italic"
  CODE="Code"
  LINK="link"
  IMAGE="image"
class TextNode():
  def __init__(self,text,text_type,url=None):
    self.text=text
    self.text_type=text_type
    self.url=url
  def __eq__(self,other):
    return self.text==other.text and self.text_type==other.text_type and self.url==other.url
  
  def __repr__(self):
    return f"TextNode({self.text}, {self.text_type}, {self.url})"
def text_node_to_html_node(node):
    match(node.text_type):
      case TextType.TEXT:
        return LeafNode(value=node.text)
      case TextType.BOLD:
        return LeafNode(tag="b",value=node.text)
      case TextType.ITALIC:
        return LeafNode(tag="i",value=node.text)
      case TextType.CODE:
        return LeafNode(tag="code",value=node.text)
      case TextType.LINK:
        return LeafNode(tag="a",value=node.text,props={"href":node.url})
      case TextType.IMAGE:
        return LeafNode(tag="img",props={"src":node.url,"alt":node.text})
      case _:
        raise Exception("Not a valid text type available")
