""" Tests pour la génération de pattern """

from pathlib import Path

import numpy as np

from FileIO import open_png_as_boolean_mask, save_boolean_mask_as_png

SAMPLES_DIR = Path(__file__).parent / "Samples"
ref_boolean_mask = np.random.rand(256, 256) > 0.5


##################################################
def test_save_boolean_mask_as_png():
	"""
	Test de la fonction save_boolean_mask_as_png.
	"""
	save_boolean_mask_as_png(ref_boolean_mask, f"{SAMPLES_DIR}/test_save_boolean_mask.png")


##################################################
def test_open_png_as_boolean_mask():
	"""
	Test de la fonction open_png_as_boolean_mask.
	"""
	mask = open_png_as_boolean_mask(f"{SAMPLES_DIR}/test_save_boolean_mask.png")
	assert np.array_equal(ref_boolean_mask, mask), "Le masque devrait correspondre à la référence."
