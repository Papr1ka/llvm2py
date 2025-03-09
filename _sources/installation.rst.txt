Installation
############

Preferred way
=============

.. code-block:: bash

    pip install llvm2py

Supported versions

CPython3.10 - CPython3.13

On Windows 64bit and manylinux x86_64 platforms.

Manual installation
===================

1. Dependencies

* For correct build you need **CMake >= 3.27**

* C and C++ compilers.

* The system must also have libraries **libffi** и **libtinfo**.

.. note::
    
    If the libraries are not found, you can add them manually, example [CMakeLists.txt](./CMakeLists.txt), lines 12-15.

* Preferred build system **Ninja**

2. Cloning llvm2py

.. code-block:: bash
    
    git clone git@github.com:Papr1ka/llvm2py.git
    cd llvm2py

3. LLVM setup

You must have the static library **LLVM** version >= 16 installed on the system.

This can be done via the distribution's package manager.
--------------------------------------------------------

Example:

.. code-block:: bash

    sudo dnf install llvm
    sudo dnf install llvm-devel

Or you can build LLVM manually and specify the path to the cmake folder, line 21
--------------------------------------------------------------------------------
.. code-block:: bash

    LLVM_DIR = "/usr/lib/llvm-18/cmake" # Path to cmake folder of llvm library

Or you can download compiled libraries
--------------------------------------

* Deb packages https://apt.llvm.org/
* Windows https://packages.msys2.org/package/mingw-w64-x86_64-llvm

4. Run setup.py

in the directory with setup.py:

.. code-block:: bash

    python -m pip install .
