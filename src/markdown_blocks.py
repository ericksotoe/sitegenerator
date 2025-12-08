import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        return BlockType.QUOTE
    if block.startswith("- "):
        return BlockType.ULIST
    if re.match(r"^\d+\.\s", block):
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    sections = markdown.split("\n\n")
    stripped = list(map(lambda x: x.strip(), sections))
    return list(filter(lambda x: x != "", stripped))
