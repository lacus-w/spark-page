# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'spark-page'
copyright = '2023, esse LL'
author = 'esse LL'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    "nbsphinx",
    "myst_parser",
    # "sphinx_design",
    "sphinx_copybutton",
    'sphinx_favicon',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'
# html_theme = "sphinx_book_theme"
# html_theme = sphinx_material

# -- Options for EPUB output
epub_show_urls = 'footnote'

latex_engine = "xelatex"
latex_use_xindy = False
latex_elements = {
    "preamble": "\\usepackage[UTF8]{ctex}\n",
}

favicons = [
#    {
#       "sizes": "16x16",
#       "href": "https://secure.example.com/favicon/favicon-16x16.png",
#    },
#    {
#       "sizes": "32x32",
#       "href": "https://secure.example.com/favicon/favicon-32x32.png",
#    },
   {
      "rel": "pink-floyd-icon",
      "sizes": "512x512",
      "href": "pink-floyd-icon.png",  # use a local file in _static
   },
]