""" Configuration file for the Sphinx documentation builder. """

# -- Gestion des fichiers à ajouter ------------------------------------------
import os
import sys
import shutil

# Ajout du chemin vers le dossier SampleMaker
sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('../SampleMaker'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Sample Maker'
copyright = '2024, Thibaut Monseigne'
author = 'Thibaut Monseigne'
language = 'fr'

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

# Copie des fichiers de rapport
# Spécifie les répertoires source et destination
source_dir = 'test_reports'
destination_dir = '_build/html/test_reports'

# Copie les fichiers si le dossier source existe
if os.path.exists(source_dir):
    # Crée le dossier de destination s'il n'existe pas.
    os.makedirs(destination_dir, exist_ok=True)
    # Copie récursivement les fichiers du dossier source vers le dossier de destination.
    shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)