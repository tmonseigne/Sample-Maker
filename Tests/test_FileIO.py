""" Tests pour la génération de pattern """

import os
from pathlib import Path

import numpy as np

from FileIO import open_png_as_boolean_mask, open_png_as_sample, save_boolean_mask_as_png, save_sample_as_png
from Utils import print_warning

OUTPUT_DIR = Path(__file__).parent / "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

# np.random.seed(42) # Possibilité de fixer la graine du random pour avoir un aléatoire "controlé".
ref = np.random.rand(256, 256) * 255
ref_boolean_mask = ref > 128


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
	"""
	save_sample_as_png(ref, f"{OUTPUT_DIR}/test_save_sample.png", 0)
	save_sample_as_png(np.zeros((256, 256)), f"{OUTPUT_DIR}/test_save_sample_black.png")


##################################################
def test_open_png_as_sample():
	"""
	Test de la fonction open_png_as_sample.
	"""
	sample = open_png_as_sample(f"{OUTPUT_DIR}/test_save_sample.png")
	new_ref = ref.astype(np.uint8).astype(np.float32)  # cast forcé car les pixel ont des valeurs entières
	assert np.allclose(new_ref, sample, atol=1e-5), "L'échantillon devrait correspondre à la référence avec une tolérance d'erreur."

	sample = open_png_as_sample(f"{OUTPUT_DIR}/test_save_sample_black.png")
	assert np.allclose(sample, 0.0), "L'échantillon devrait être entièrement noir."


##################################################
def test_save_stack_as_tiff():
	"""
	Test de la fonction save_sample_as_png.

	.. todo:: A faire
	"""
	print_warning("TODO")

##################################################
def test_open_tiff_as_stack():
	"""
	Test de la fonction save_sample_as_png.

	.. todo:: A faire
	"""
	print_warning("TODO")

