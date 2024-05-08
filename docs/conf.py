"""Sphinx configuration."""

project = "Signhost Api Python Client"
author = "Jelmer Draaijer"
copyright = "2023, Jelmer Draaijer"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
