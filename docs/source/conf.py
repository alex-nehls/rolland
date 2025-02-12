# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Rolland'
copyright = '2025, Maximilian Mantel, Ennes Sarradj'
author = 'Maximilian Mantel, Ennes Sarradj'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',             # For automatic doc generation from docstrings
    'sphinx.ext.napoleon',            # Supports NumPy and Google style docstrings
    'sphinx.ext.viewcode',            # Links to source code
    'sphinx.ext.mathjax',             # For LaTeX math rendering
    'sphinxcontrib.bibtex',           # Citation support
    'sphinx.ext.autosummary',         # Generate autodoc summaries
    'autodoc_traits',                 # Support for traitlets
    'sphinx_design',                  # Debugging info
    'myst_parser',                    # Markdown support
]

# sphinxcontrib-bibtex extension settings
# ---------------------------------------
bibtex_bibfiles = ["literature/literature.bib"]
bibtex_default_style = 'unsrt'

templates_path = ['_templates']
exclude_patterns = []

autodoc_typehints = "description"       # Include type hints in the description
napoleon_google_docstring = False       # Use NumPy-style docstrings
napoleon_numpy_docstring = True

pygments_style = "default"  # Replace with a valid Pygments style for light mode
pygments_style_dark = "native"  # Replace with a valid Pygments style for dark mode

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinxawesome_theme'
html_permalinks_icon = "<span>¶</span>"

html_static_path = ["_static"]
html_css_files = ["custom.css"]

html_title = "Rolland Documentation"


from dataclasses import asdict
from sphinxawesome_theme import ThemeOptions

theme_options = ThemeOptions(

    # Add your theme options. For example:
    main_nav_links={"About": "/about"},
    show_scrolltop=True,
    show_prev_next=False,
    show_breadcrumbs=True,
    awesome_headerlinks=False,
)

html_theme_options = asdict(theme_options)