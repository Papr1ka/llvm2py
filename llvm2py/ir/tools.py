class CodeMixin:
    """
    The class provides a field to store the code
    that the class is associated with for beautiful __str__ output
    """

    code: str

    def __init__(self, code: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = code

    def __str__(self):
        return self.code


def repr(node):
    node_name = node.__class__.__name__
    attrs = ", ".join(f"{attr}={getattr(node, attr)}" for attr in node._fields)
    return f"<{node_name} {attrs}>"
