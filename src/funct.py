import re
from textnode import TextType,TextNode
def split_nodes_delimiter(old_nodes, delimiter="", text_type=TextType.TEXT):
    new_nodes=[]
    for node in old_nodes:
        if node.text_type!=TextType.TEXT:
            new_nodes.append(node)
            continue
        parts=node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(f"Invalid Markdown: Unmatched delimiter '{delimiter}' in text '{node.text}'")
        for i, part in enumerate(parts):
            if i % 2 == 0:
                # Texto fuera del delimitador
                if part:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Texto dentro del delimitador
                if part:
                    new_nodes.append(TextNode(part, text_type))

    return new_nodes
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
            
