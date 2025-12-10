from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            return line.lstrip("#").strip()
    raise Exception("The markdown has no h1 header")


def block_to_block_type(block):
    # split the block into lines so we can check per-line patterns
    lines = block.split("\n")

    # checking to see if the block is a heading
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    # checking to see if the block is code
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    # checking to see if the block is a quote
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    # checking to see if the block is an unordered list
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST

    # checking to see if the block is an ordered list
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST

    # if nothing else matches just return paragraph
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    sections = markdown.split("\n\n")
    stripped = list(map(lambda x: x.strip(), sections))
    return list(filter(lambda x: x != "", stripped))


def count_heading(line):
    count = 0
    for i in range(len(line)):
        if line[i] == "#":
            count += 1
        # this break stops counting after the first occurances of #
        else:
            break
    return count


def text_to_children(text):
    # parse inline markdown into TextNodes
    text_nodes = text_to_textnodes(text)

    # convert each TextNode to an HTMLNode
    children = []
    for tn in text_nodes:
        child = text_node_to_html_node(tn)
        children.append(child)

    # return list of HTMLNode children
    return children


def markdown_to_html_node(markdown):
    div_node = ParentNode("div", children=[])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            heading_number = count_heading(block)
            heading_text = block.lstrip("#").strip()
            head_node = ParentNode(
                f"h{heading_number}", children=text_to_children(heading_text)
            )
            div_node.children.append(head_node)  # type: ignore

        elif block_type == BlockType.PARAGRAPH:
            lines = block.split("\n")
            paragraph_text = " ".join(lines)
            par_node = ParentNode("p", children=text_to_children(paragraph_text))
            div_node.children.append(par_node)  # type: ignore

        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            # drop the first and last ```
            inner_lines = lines[1:-1]

            val = "\n".join(inner_lines) + "\n"
            code_node = LeafNode("code", val)
            pre_node = ParentNode("pre", children=[code_node])
            div_node.children.append(pre_node)  # type: ignore
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            clean_lines = []
            for line in lines:
                clean_lines.append(line.lstrip(">").lstrip())
            clean_text = " ".join(clean_lines)

            bquote_node = ParentNode(
                "blockquote", children=text_to_children(clean_text)
            )
            div_node.children.append(bquote_node)  # type: ignore

        elif block_type == BlockType.ULIST:
            lines = block.split("\n")
            clean_lines = []
            for line in lines:
                if not line.strip():
                    continue
                clean_lines.append(line.lstrip("- "))

            li_nodes = []
            for item in clean_lines:
                li_node = ParentNode("li", children=text_to_children(item))
                li_nodes.append(li_node)
            ul_node = ParentNode("ul", children=li_nodes)
            div_node.children.append(ul_node)  # type: ignore

        elif block_type == BlockType.OLIST:
            lines = block.split("\n")
            clean_lines = []
            count = 1
            for line in lines:
                if not line.strip():
                    continue
                prefix = f"{count}."
                stripped = line.strip()
                if stripped.startswith(prefix):
                    without_num = stripped[len(prefix) :]
                    clean_lines.append(without_num.lstrip())
                else:
                    clean_lines.append(stripped)
                count += 1

            li_nodes = []
            for item in clean_lines:
                li_node = ParentNode("li", children=text_to_children(item))
                li_nodes.append(li_node)

            ol_node = ParentNode("ol", children=li_nodes)
            div_node.children.append(ol_node)  # type: ignore

    return div_node
