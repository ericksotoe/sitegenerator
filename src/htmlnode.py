class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_string = ""
        if self.props:
            for k, v in self.props.items():
                html_string = html_string + f' {k}="{v}"'
        return html_string

    def __repr__(self):
        html_string = f"tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}"
        return html_string
