import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    list_of_new_nodes = []

    for node in old_nodes:
        # if its not a text node add it as it is
        if node.text_type != TextType.TEXT:
            list_of_new_nodes.append(node)
            continue

        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(
                f"Unmatched {delimiter} delimiter. Every opening {delimiter} must have a closing {delimiter}."
            )
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            # even indecies are only of TextType.TEXT
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            # odd indecies can be bold, code, or italicized
            else:
                split_nodes.append(TextNode(sections[i], text_type))

        list_of_new_nodes.extend(split_nodes)

    return list_of_new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    list_of_new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            list_of_new_nodes.append(node)
            continue

        remaining_text = node.text
        alt_and_url = extract_markdown_images(node.text)

        if len(alt_and_url) == 0:
            list_of_new_nodes.append(node)
            continue

        for alt, url in alt_and_url:
            sections = remaining_text.split(f"![{alt}]({url})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")

            if sections[0] != "":
                list_of_new_nodes.append(TextNode(sections[0], TextType.TEXT))

            list_of_new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining_text = sections[1]
        if remaining_text != "":
            list_of_new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return list_of_new_nodes


def split_nodes_link(old_nodes):
    pass
