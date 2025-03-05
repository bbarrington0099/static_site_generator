import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        # If the node is not a text type, add it as-is
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue
        
        # Split the text by the delimiter
        sections = node.text.split(delimiter)
        
        # If odd number of sections, it means not all delimiters are closed
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid delimiter usage in text: {node.text}")
        
        # Process the sections
        for i, section in enumerate(sections):
            # Even indices are regular text, odd indices are to be converted
            if section:  # Only create nodes for non-empty sections
                if i % 2 == 0:
                    # Regular text sections remain as TEXT type
                    new_nodes.append(TextNode(section, TextType.TEXT))
                else:
                    # Sections between delimiters get the specified text type
                    new_nodes.append(TextNode(section, text_type))
    
    return new_nodes

def extract_markdown_images(text):
    # Regex pattern to match markdown images: ![alt text](url)
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    
    # Find all matches and return as list of tuples
    return re.findall(pattern, text)

def extract_markdown_links(text):
    # Regex pattern to match markdown links: [link text](url), 
    # but not images (negative lookahead to exclude images)
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    
    # Find all matches and return as list of tuples
    return re.findall(pattern, text)

def split_nodes_images(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        # If the node is not a text type, add it as-is
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue
        
        # Extract images from the text
        images = extract_markdown_images(node.text)
        
        # If no images, add the original node
        if not images:
            new_nodes.append(node)
            continue
        
        # Process the text with images
        remaining_text = node.text
        for image_alt, image_url in images:
            # Split the text around the first image markdown
            image_markdown = f"![{image_alt}]({image_url})"
            sections = remaining_text.split(image_markdown, 1)
            
            # Add text before image as TEXT node if non-empty
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            # Add image node
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            # Update remaining text
            remaining_text = sections[1] if len(sections) > 1 else ""
        
        # Add any remaining text as TEXT node
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        # If the node is not a text type, add it as-is
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue
        
        # Extract links from the text
        links = extract_markdown_links(node.text)
        
        # If no links, add the original node
        if not links:
            new_nodes.append(node)
            continue
        
        # Process the text with links
        remaining_text = node.text
        for link_text, link_url in links:
            # Split the text around the first link markdown
            link_markdown = f"[{link_text}]({link_url})"
            sections = remaining_text.split(link_markdown, 1)
            
            # Add text before link as TEXT node if non-empty
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            # Add link node
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            
            # Update remaining text
            remaining_text = sections[1] if len(sections) > 1 else ""
        
        # Add any remaining text as TEXT node
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_link(nodes)
    return nodes