from leafnode import LeafNode
from textnode import TextNode, TextType
from markdown_to_block import markdown_to_block
from parentnode import ParentNode
from textsplitter import text_to_textnodes
from blocktype import block_to_block_type, BlockType
from converter import  text_node_to_html_node

def markdown_to_html_node(markdown):
    blocks = markdown_to_block(markdown)
    parent_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                parent_nodes.append(node_from_paragraph(block))
            case BlockType.HEADING:
                parent_nodes.append(node_from_heading(block))
            case BlockType.CODE:
                parent_nodes.append(node_from_code(block))
            case BlockType.QUOTE:
                parent_nodes.append(node_from_quote(block))
            case BlockType.UNORDERED_LIST:
                parent_nodes.append(node_from_unordered_list(block))
            case BlockType.ORDERED_LIST:
                parent_nodes.append(node_from_ordered_list(block))
    html_node = ParentNode("div", parent_nodes)
    return html_node

def text_to_children(block):
    textnodes = text_to_textnodes(block)
    htmlnodes = []
    for node in textnodes:
        htmlnodes.append(text_node_to_html_node(node))
    return htmlnodes

def node_from_paragraph(block):
    child_blocks = block.splitlines()
    return ParentNode("p", text_to_children(" ".join(child_blocks)))

def node_from_heading(block):
    level = block.index(" ")
    children = text_to_children(block[level+1:])
    return ParentNode(f"h{level}", children)

def node_from_code(block):
    return ParentNode("pre", [text_node_to_html_node(TextNode(block[3:-3], TextType.CODE))])

def node_from_quote(block):
    children = []
    for line in block.splitlines():
        gen_children = text_to_children(line[2:])
        if len(gen_children) == 0:
            children.append(text_node_to_html_node(TextNode(" ", TextType.TEXT)))
            continue
        if len(gen_children) == 1:
            children.append(gen_children[0])
            continue
        children.extend(gen_children)
    return ParentNode("blockquote", children)

def node_from_unordered_list(block):
    children = []
    for line in block.splitlines():
        children.append(ParentNode("li", text_to_children(line[2:])))
    return ParentNode("ul", children)

def node_from_ordered_list(block):
    children = []
    for line in block.splitlines():
        children.append(ParentNode("li", text_to_children(line[line.index(". ")+2:])))
    return ParentNode("ol", children)