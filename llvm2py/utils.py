from llvm2py import ir


def dump(node, annotate_fields=True, *, indent=None) -> str:
    """
    Return a formatted dump of the IR object.
    """
    ir_types = (
        ir.Module,
        ir.Function,
        ir.Value,
        ir.Type,
        ir.Block,
        ir.Argument,
        ir.Instruction
    )

    def _format(node, level=0):
        if indent is not None:
            level += 1
            prefix = '\n' + indent * level
            sep = ',\n' + indent * level
        else:
            prefix = ''
            sep = ', '

        if node.__class__ in ir_types:
            cls = type(node)
            args = []
            allsimple = True
            keywords = annotate_fields
            for name in node._fields:
                try:
                    value = getattr(node, name)
                except AttributeError:
                    keywords = True
                    continue
                if value is None and getattr(cls, name, ...) is None:
                    keywords = True
                    continue
                value, simple = _format(value, level)
                allsimple = allsimple and simple
                if keywords:
                    args.append('%s=%s' % (name, value))
                else:
                    args.append(value)
            if allsimple and len(args) <= 3:
                return '%s(%s)' % (
                    node.__class__.__name__, ', '.join(args)), not args
            return '%s(%s%s)' % (
                node.__class__.__name__, prefix, sep.join(args)), False
        elif isinstance(node, tuple):
            if not node:
                return '[]', True
            return '[%s%s]' % (
                prefix, sep.join(_format(x, level)[0] for x in node)), False
        return repr(node), True

    if node.__class__ not in ir_types:
        raise TypeError('expected llvm2py.ir.* object, got %r' %
                        node.__class__.__name__)
    if indent is not None and not isinstance(indent, str):
        indent = ' ' * indent
    return _format(node)[0]
