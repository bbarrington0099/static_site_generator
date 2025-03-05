from enum import Enum
from leafnode import LeafNode
from parentnode import ParentNode
from textnode_parser import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    for i, block in enumerate(blocks):
        block = block.strip()
        if not block:
            blocks[i] = None
        else:
            blocks[i] = block
    return blocks

def block_to_block_type(block):
    dispatch = {
        "#": BlockType.HEADING,
        "```": BlockType.CODE,
        ">": BlockType.QUOTE,
        "-": BlockType.UNORDERED_LIST,
        "1.": BlockType.ORDERED_LIST,
    }
    for key, value in dispatch.items():
        if block.startswith(key):
            return value
    return BlockType.PARAGRAPH if block else None

def markdown_to_html_node(markdown):
    # Split the markdown into blocks based on two consecutive newlines
    blocks = markdown_to_blocks(markdown)
    
    # The parent div node
    parent_node = ParentNode('div', [])
    
    for block in blocks:
        if not block:
            continue
        
        block_type = block_to_block_type(block)
        block_node = None
        
        if block_type == BlockType.PARAGRAPH:
            # Paragraph: Handle inline markdown, without breaking into multiple blocks
            block_node = ParentNode('p', text_to_children(block.replace('\n', ' ')))

        elif block_type == BlockType.HEADING:
            level = block.count('#')  # Determine heading level by the number of '#'
            block_node = ParentNode(f'h{level}', text_to_children(block.lstrip('#').strip()))

        elif block_type == BlockType.CODE:
            # Code block: Strip the surrounding backticks and preserve newlines from the markdown
            block_content = block.strip("`").strip()
            block_node = ParentNode('pre', [LeafNode(block_content, 'code')])  # Preserve newlines here

        elif block_type == BlockType.QUOTE:
            # Decode any HTML entities and remove the '>' character from each line in the blockquote
            block_lines = block.split("\n")
            block_content = "\n".join([line.lstrip('>').strip() for line in block_lines])
            block_node = ParentNode('blockquote', text_to_children(block_content))

        elif block_type == BlockType.UNORDERED_LIST:
            # Remove the dashes and any leading whitespace from the list items
            list_items = [ParentNode('li', text_to_children(item.lstrip('-').strip())) for item in block.split('\n') if item.strip()]
            block_node = ParentNode('ul', list_items)

        elif block_type == BlockType.ORDERED_LIST:
            # Remove the numbers and periods from the ordered list items
            list_items = [ParentNode('li', text_to_children(item.lstrip('0123456789.').strip())) for item in block.split('\n') if item.strip()]
            block_node = ParentNode('ol', list_items)

        if block_node:
            parent_node.children.append(block_node)  # Add block node to parent div

    return parent_node

def text_to_children(text):
    nodes = text_to_textnodes(text)
    return nodes