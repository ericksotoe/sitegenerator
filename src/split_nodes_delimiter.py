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
