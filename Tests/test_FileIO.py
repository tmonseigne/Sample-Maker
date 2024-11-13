""" Tests pour la génération de pattern """

import os
from pathlib import Path

import numpy as np

from FileIO import open_png_as_boolean_mask, save_boolean_mask_as_png

OUTPUT_DIR = Path(__file__).parent / "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

# np.random.seed(42) # Possibilité de fixer la graine du random pour avoir un aléatoire "controlé".
ref_boolean_mask = np.random.rand(256, 256) > 0.5


##################################################
def test_save_boolean_mask_as_png():
	"""
	Test de la fonction save_boolean_mask_as_png.
	"""
	save_boolean_mask_as_png(ref_boolean_mask, f"{OUTPUT_DIR}/test_save_boolean_mask.png")


##################################################
def test_open_png_as_boolean_mask():
	"""
	Test de la fonction open_png_as_boolean_mask.
	"""
	mask = open_png_as_boolean_mask(f"{OUTPUT_DIR}/test_save_boolean_mask.png")
	assert np.array_equal(ref_boolean_mask, mask), "Le masque devrait correspondre à la référence."


##################################################
def test_save_sample_as_png():
	"""
	Test de la fonction save_sample_as_png.

	.. todo:: A faire
	"""
	print("TODO")


##################################################
def test_open_png_as_sample():
	"""
	Test de la fonction open_png_as_sample.

	.. todo:: A faire
	"""
	print("TODO")


##################################################
def test_save_stack_as_tiff():
	"""
	Test de la fonction save_sample_as_png.

	.. todo:: A faire
	"""
	print("TODO")

##################################################
def test_open_tiff_as_stack():
	"""
	Test de la fonction save_sample_as_png.

	.. todo:: A faire
	"""
	print("TODO")

