# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'spark-page'
copyright = '2023, esse LL'
author = 'esse LL'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "nbsphinx",
    "myst_parser",
    "sphinx_design",
    "sphinx_copybutton",
    "notfound.extension",
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

# html_theme = 'sphinx_rtd_theme'
html_theme = 'sphinx_book_theme'
# html_theme = 'sphinx_material'
html_logo = "_static/pf-prism.png"
html_title = "Spark Page"
html_copy_source = True
html_favicon = '_static/sp-icon.png'# "https://spark.apache.org/images/spark-logo-rev.svg"

html_static_path = ["_static"]
# html_css_files = ["custom.css"]
# pygments_style = 'xcode'
html_theme_options = {
    'logo': '_static/pf-prism.png',
}

# -- Options for EPUB output
epub_show_urls = 'footnote'

latex_engine = "xelatex"
latex_use_xindy = False
latex_elements = {
    "preamble": "\\usepackage[UTF8]{ctex}\n",
}

notfound_template = "404.rst"