from .instruction import Attrs


def function_attributes(attrs: list[Attrs]):
    """
    Returns the attributes of the function
    """
    return attrs[0]


def ret_attributes(attrs: list[Attrs]):
    """
    Returns the attributes of the returned value
    """
    return attrs[1]


def arguments_attributes(attrs: list[Attrs]):
    """
    Returns the attributes of the arguments
    """
    return attrs[2:]


def argument_attributes(attrs: list[Attrs], arg_no: int):
    """
    Returns the argument attributes
    """
    if arg_no + 3 > len(attrs):
        return None
    else:
        return attrs[2 + arg_no]
