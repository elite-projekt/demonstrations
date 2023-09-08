# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
import pathlib
p = pathlib.Path(__file__).parent.parent.parent
sys.path.insert(0, str(p))

project = 'ELITE Demonstrations'
copyright = '2022, ELITE'
author = 'ELITE'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        'myst_parser',
        'sphinx.ext.autodoc',
        'sphinx.ext.autosummary']
source_suffix = ['.rst', '.md']
autosummary_generate = True

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static', 'virt-package.deb', 'kvm_config_example.xml']
