from typing import Any

from .enum import Attrs


def function_attributes(attrs: list):
    """
    Returns the attributes of the function.
    """
    return attrs[0]


def ret_attributes(attrs: list):
    """
    Returns the attributes of the returned value.
    """
    return attrs[1]


def arguments_attributes(attrs: list):
    """
    Returns the attributes of the arguments.
    """
    return attrs[2:]


def argument_attributes(attrs: list, arg_no: int):
    """
    Returns the argument attributes.
    """
    if arg_no + 3 > len(attrs):
        return None
    else:
        return attrs[2 + arg_no]


def attrs_to_dict(attrs: list[tuple]) -> Attrs:
    """Transforms attributes from tuple form to dict form.
    Conversation::

        [("nsw",), ("fmf", []), ("vscale_range", 1, 2)]
        ->
        {
            "nsw": (),
            "fmf": [],
            "vscale_range": (1, 2)
        }
    """
    new_attrs = {}
    if not attrs:  # empty
        return new_attrs
    for name, *values in attrs:
        if len(values) == 1:
            new_attrs[name] = values[0]
        else:
            new_attrs[name] = tuple(values)
    return new_attrs


def attrs_list_to_dict(attrs_list: list[list[tuple]]):
    return [attrs_to_dict(attrs) for attrs in attrs_list]
