import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if not old_nodes:
        raise ValueError("Nodes cannot be empty")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = node.text.split(delimiter)
        delimiter_active = False
        for i in range(len(split_nodes)):
            if delimiter_active:
                delimiter_active = False
                new_nodes.append(TextNode(split_nodes[i], text_type))
                continue
            if not delimiter_active:
                delimiter_active = True
                if len(split_nodes[i]) > 0:
                    new_nodes.append(TextNode(split_nodes[i], TextType.TEXT))

        if len(split_nodes) % 2 != 1:
            raise ValueError("No closing delimiter found")
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)]\((.*?)\)", text)

def split_nodes_link(nodes):
    new_nodes = []
    for node in nodes:
        remaining_text = node.text
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        for alt, link in extract_markdown_links(node.text):
            link_text = f"[{alt}]({link})"
            text_split = remaining_text.split(link_text, maxsplit=1)
            if len(text_split[0]) > 0:
                new_nodes.append(TextNode(text_split[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, link))
            remaining_text = text_split[1]
        if len(remaining_text) > 0:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_image(nodes):
    new_nodes = []
    for node in nodes:
        remaining_text = node.text
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        for alt, link in extract_markdown_images(node.text):
            image_text = f"![{alt}]({link})"
            text_split = remaining_text.split(image_text, maxsplit=1)
            if len(text_split[0]) > 0:
                new_nodes.append(TextNode(text_split[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, link))
            remaining_text = text_split[1]
        if len(remaining_text) > 0:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    for node in new_nodes:
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    for node in new_nodes:
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    for node in new_nodes:
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    for node in new_nodes:
        new_nodes = split_nodes_link(new_nodes)
    for node in new_nodes:
        new_nodes = split_nodes_image(new_nodes)
    return new_nodes
