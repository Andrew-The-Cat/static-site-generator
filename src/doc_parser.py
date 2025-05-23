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

#higher order functions yaaaaaaay
def split_complex_nodes(extraction_func, delimiter_func, text_type):

    def inner(old_nodes):
        cut = []

        def parse_node(node):
            nonlocal cut
            to_parse = node.text
            extracted = extraction_func(to_parse)

            if len(to_parse) == 0:
                return

            if len(extracted) == 0:
                cut.append(TextNode( to_parse, node.text_type, node.url ))
                return

            split = to_parse.split( delimiter_func(extracted[0]), 1 )
            cut.append(TextNode( split[0], node.text_type, node.url ))
            cut.append(TextNode( extracted[0][0], text_type, extracted[0][1] ))

            parse_node(TextNode( split[1], node.text_type, node.url ))

        for node in old_nodes:
            parse_node(node)
        return cut

    return inner


#might cause issues if not receiving extracted images left to right
def split_nodes_image(old_nodes):
    return split_complex_nodes( extract_markdown_images, lambda x: f"![{x[0]}]({x[1]})", TextType.IMAGE )(old_nodes)

#might cause issues if not receiving extracted links left to right
def split_nodes_link(old_nodes):
    return split_complex_nodes( extract_markdown_links, lambda x: f"[{x[0]}]({x[1]})", TextType.LINK )(old_nodes)

#I have no idea how much memory this takes but I do not believe I care :3
def text_to_textnodes(text):
    return split_nodes_image(split_nodes_link(split_nodes_delimiter( split_nodes_delimiter( split_nodes_delimiter([TextNode(text, TextType.TEXT)], '`', TextType.CODE), '**', TextType.BOLD ), '_', TextType.ITALIC )))


def markdown_to_blocks(markdown):
    return list(filter (lambda x: x != '', map(lambda y: y.strip(), markdown.split('\n\n')) ) )

def block_to_block_type(block):
    split = block.split('\n')

    if len(re.findall(r'#{1,6} ', block)) != 0:
        return BlockType.HEADING
    
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    
    num_quote = 0
    num_ul = 0
    num_ol = 1
    for line in split:
        if line.startswith('>'):
            num_quote += 1

        if line.startswith('- '):
            num_ul += 1

        if line.startswith(f'{num_ol}. '):
            num_ol += 1

    if num_quote == len(split):
        return BlockType.QUOTE

    if num_ul == len(split):
        return BlockType.UNORDERED_LIST
    
    if num_ol - 1 == len(split):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def block_to_children(block):
    children = list(map(text_node_to_html_node, text_to_textnodes(" ".join(map ( lambda x: x.lstrip('>-#123456789. ') ,block.split('\n')) ))))

    return children

def md_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match(block_type):
            case BlockType.PARAGRAPH:
                nodes.append(ParentNode("p", block_to_children(block), None))
            case BlockType.QUOTE:
                nodes.append(ParentNode("blockquote", block_to_children(block), None))
            case BlockType.UNORDERED_LIST:
                nodes.append(ParentNode("ul", list( map( lambda line: ParentNode('li', block_to_children(line)), block.split('\n'))), None))
            case BlockType.ORDERED_LIST:
                nodes.append(ParentNode("ol", list( map( lambda line: ParentNode('li', block_to_children(line)), block.split('\n'))), None))
            case BlockType.HEADING:
                nodes.append(ParentNode(f"h{block.count('#')}", block_to_children(block), None))
            case BlockType.CODE:
                nodes.append(ParentNode("pre", [text_node_to_html_node( TextNode(block.strip('`').lstrip(), TextType.CODE) )], None))

    
    return ParentNode("div", nodes)