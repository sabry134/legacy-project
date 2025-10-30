# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'Legacy'
copyright = '2025, Legacy Contributors'
author = 'Legacy Contributors'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.mermaid'
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# Add custom HTML footer to remove copyright notice and "Built with Sphinx" footer
html_footer = ''

# Add custom HTML context to remove "Edit on GitHub" link
html_context = {
    'display_github': False,
}

# -- Options for EPUB output
epub_show_urls = 'footnote'

html_show_sourcelink = False

html_theme_options = {
    'display_version': False,
}

mermaid_params = [
    '--height', '400',
]