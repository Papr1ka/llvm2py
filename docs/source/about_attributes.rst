About attributes
################

In LLVM, there are various kinds of attributes.

All attributes related to instructions are accessible by the corresponding class attributes.

However, there are attributes such as
`parameter attributes <https://llvm.org/docs/LangRef.html#parameter-attributes>`_,
`function attributes <https://llvm.org/docs/LangRef.html#function-attributes>`_,
`call site attributes <https://llvm.org/docs/LangRef.html#call-site-attributes>`_ and
`global attributes <https://llvm.org/docs/LangRef.html#global-attributes>`_.

Attributes can be categorized into groups:

1. Attributes without arguments (zeroext, inreg, noalias...).

2. Attributes with a number argument (align(n), alignstack(n), ...).

3. Attributes with an type argument (byref(ty), preallocated(ty), ...).

4. Other attributes.

There is attributes with two params (vscale_range(min, max)).

All such attributes are stored in a dictionary,
where the key is the attribute name and the value is the attribute argument tuple.

.. code-block:: python

    attrs = {
        "zeroext": (),
        "align": n,
        "alignstack": n,
        "byref": ty,
        "preallocated": ty,
        "vscale": (min, max)
    }

You can find these attributes in the classes: 
:class:`llvm2py.ir.function.Function`,
:class:`llvm2py.ir.global_variable.GlobalVariable`,
:class:`llvm2py.ir.instruction.Invoke`,
:class:`llvm2py.ir.instruction.CallBr`,
:class:`llvm2py.ir.instruction.Call`.
