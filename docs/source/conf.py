# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from collections import _tuplegetter

sys.path.insert(0, os.path.abspath("../../"))

project = "llvm2py"
copyright = "2025, Papr1ka"
author = "Papr1ka"
release = "0.2.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
]

add_module_names = False

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]


def skip_properties(app, what, name, obj, skip, options):
    # Skip NamedTuple properties with non-informative __doc__ string
    return skip or isinstance(obj, _tuplegetter)


def setup(app):
    app.connect("autodoc-skip-member", skip_properties)
