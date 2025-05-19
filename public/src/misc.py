from htmlnode import *
from textnode import *
import re


def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        
        case _:
            return ValueError("unknown text type")
        

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    cut = []

    for node in old_nodes:
        splitted = node.text.split(delimiter)
        for j in range(0, len(splitted)):
            if j%2 == 0:
                cut.append( TextNode(splitted[j], node.text_type, node.url) )
                continue
            cut.append( TextNode(splitted[j], text_type, node.url) )
    return cut

def extract_markdown_images(text):
    matches = list(map( lambda x: tuple(x.strip("!()[]").split('](')), re.findall(r"\!\[(?:.*?)\]\((?:.*?)\)", text) ))
    return matches

def extract_markdown_links(text):
    matches = list(map( lambda x: tuple(x.strip("!()[]").split('](')), re.findall(r"(?<!!)\[(?:.*?)\]\((?:.*?)\)", text) ))
    return matches

#might cause issues if not receiving extracted images left to right
def split_nodes_image(old_nodes):
    cut = []

    for node in old_nodes:
        to_parse = node.text
        md_images = extract_markdown_images(to_parse)

        for image in md_images:
            split = to_parse.split( f"![{image[0]}]({image[1]})" )

            cut.append(TextNode( split[0], node.text_type, node.url ))
            cut.append(TextNode( image[0], TextType.IMAGE, image[1] ))
            to_parse = split[1]

    if len(cut) == 0:
        return old_nodes
    return cut

#might cause issues if not receiving extracted links left to right
def split_nodes_link(old_nodes):
    cut = []

    for node in old_nodes:
        to_parse = node.text
        md_links = extract_markdown_links(to_parse)

        for image in md_links:
            split = to_parse.split( f"[{image[0]}]({image[1]})" )

            cut.append(TextNode( split[0], node.text_type, node.url ))
            cut.append(TextNode( image[0], TextType.LINK, image[1] ))
            to_parse = split[1]

    if len(cut) == 0:
        return old_nodes
    return cut