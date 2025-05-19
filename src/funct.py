import re
import os
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextType,TextNode, text_node_to_html_node
from block import BlockType, block_to_block_type
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
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_images(text)
        if not matches:
            new_nodes.append(node)
            continue

        pos = 0
        for alt, url in matches:
            pattern = f"![{alt}]({url})"
            start = text.find(pattern, pos)
            if start > pos:
                new_nodes.append(TextNode(text[pos:start], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            pos = start + len(pattern)
        
        if pos < len(text):
            new_nodes.append(TextNode(text[pos:], TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_links(text)
        if not matches:
            new_nodes.append(node)
            continue

        pos = 0
        for label, url in matches:
            pattern = f"[{label}]({url})"
            start = text.find(pattern, pos)
            if start > pos:
                new_nodes.append(TextNode(text[pos:start], TextType.TEXT))
            new_nodes.append(TextNode(label, TextType.LINK, url))
            pos = start + len(pattern)
        
        if pos < len(text):
            new_nodes.append(TextNode(text[pos:], TextType.TEXT))

    return new_nodes
def text_to_children(text):
    """Convierte un texto markdown en una lista de LeafNode HTML."""
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_blocks = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            content = block.replace("\n", " ")
            children = text_to_children(content)
            html_blocks.append(ParentNode("p", children))

        elif block_type == BlockType.HEADING:
            heading_level = block.count("#", 0, block.find(" "))
            content = block[heading_level + 1:].strip()
            children = text_to_children(content)
            html_blocks.append(ParentNode(f"h{heading_level}", children))

        elif block_type == BlockType.CODE:
            content = block.strip("`\n") + "\n"
            html_blocks.append(ParentNode("pre", [LeafNode(content, "code")]))

        elif block_type == BlockType.QUOTE:
            lines = [line.lstrip("> ").strip() for line in block.split("\n")]
            content = " ".join(lines)
            children = text_to_children(content)
            html_blocks.append(ParentNode("blockquote", children))

        elif block_type == BlockType.UNORDERED_LIST:
            items = block.split("\n")
            list_items = [
                ParentNode("li", text_to_children(item[2:].strip()))
                for item in items
            ]
            html_blocks.append(ParentNode("ul", list_items))

        elif block_type == BlockType.ORDERED_LIST:
            items = block.split("\n")
            list_items = [
                ParentNode("li", text_to_children(item[item.find('.')+2:].strip()))
                for item in items
            ]
            html_blocks.append(ParentNode("ol", list_items))

    return ParentNode("div", html_blocks)

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Aplica cada tipo de división, en orden
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
def markdown_to_blocks(markdown):
    # Separar por doble salto de línea
    raw_blocks = markdown.split("\n\n")
    
    # Limpiar espacios en cada bloque y eliminar vacíos
    blocks = [block.strip() for block in raw_blocks if block.strip()]
    
    return blocks
def extract_title(markdown):
    lines=markdown.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '): 
            return line[2:].strip() 
    raise Exception("No title found")
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as file:
        text_from = file.read()
    content=markdown_to_html_node(text_from).to_html()
    title=extract_title(text_from)
    with open(template_path, "r", encoding="utf-8") as file:
        template_content = file.read()
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(final_html)
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)

        if os.path.isdir(source_path):
            # Si es carpeta, crear la ruta destino y llamar recursivamente
            new_dest_dir = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(source_path, template_path, new_dest_dir)
        elif os.path.isfile(source_path) and source_path.endswith(".md"):
            # Para cada archivo markdown, generar su archivo html equivalente
            filename_html = os.path.splitext(entry)[0] + ".html"
            dest_path = os.path.join(dest_dir_path, filename_html)
            generate_page(source_path, template_path, dest_path)