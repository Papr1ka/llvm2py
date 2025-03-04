def function_attributes(attrs: list):
    """
    Returns the attributes of the function
    """
    return attrs[0]


def ret_attributes(attrs: list):
    """
    Returns the attributes of the returned value
    """
    return attrs[1]


def arguments_attributes(attrs: list):
    """
    Returns the attributes of the arguments
    """
    return attrs[2:]


def argument_attributes(attrs: list, arg_no: int):
    """
    Returns the argument attributes
    """
    if arg_no + 3 > len(attrs):
        return None
    else:
        return attrs[2 + arg_no]


def attrs_to_dict(attrs: list[tuple]):
    new_attrs = {}
    for name, *values in attrs:
        if len(values) == 1:
            new_attrs[name] = values[0]
        else:
            new_attrs[name] = tuple(values)
    return new_attrs
