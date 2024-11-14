""" Configuration file for the Sphinx documentation builder. """

# -- Gestion des fichiers à ajouter ------------------------------------------
import os
import sys

# Ajout du chemin vers le dossier SampleMaker
sys.path.insert(0, os.path.abspath('../SampleMaker'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Sample Maker'
copyright = '2024, Thibaut Monseigne'
author = 'Thibaut Monseigne'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
		'sphinx.ext.autodoc',
		'sphinx.ext.autosummary',
		'sphinx.ext.napoleon',
		'sphinx.ext.todo',
		'sphinx.ext.viewcode',
		]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Automatisation ----------------------------------------------------------
autosummary_generate = True
autodoc_default_options = {
		'members':          True,
		'undoc-members':    True,
		'show-inheritance': True,
		}
autodoc_member_order = 'bysource'

todo_include_todos = True
