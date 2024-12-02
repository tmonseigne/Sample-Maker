""" Fichier des tests pour la génération de pattern """

import os
from pathlib import Path

import numpy as np
import pytest

from SampleMaker.Tools import FileIO

OUTPUT_DIR = Path(__file__).parent / "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

# np.random.seed(42) # Possibilité de fixer la graine du random pour avoir un aléatoire "contrôlé".
SIZE = 512															   # Taille de l'image de test
NOISE_2D = np.random.rand(SIZE, SIZE) * 255 						   # Bruit sur une image 2D
REF_BOOLEAN_MASK = NOISE_2D > 128									   # Conversion en booléen
GRADIENT = np.linspace(0, 255, SIZE, dtype=np.float32)  			   # Création du dégradé croissant de 0 à 255
REF_GRADIENT = np.tile(GRADIENT, (SIZE, 1))							   # Répète le dégradé sur toutes les lignes
REF_STACK = np.stack((REF_GRADIENT, np.fliplr(REF_GRADIENT)), axis=0)  # Empilement du dégradé et son miroir horizontal


##################################################
def test_save_boolean_mask_as_png():
	""" Test de la fonction save_boolean_mask_as_png. """
	FileIO.save_boolean_mask_as_png(REF_BOOLEAN_MASK, f"{OUTPUT_DIR}/test_save_boolean_mask.png")


##################################################
def test_save_boolean_mask_as_png_bad_mask():
	""" Test de la fonction save_boolean_mask_as_png avec un mask à une dimension. """
	with pytest.raises(ValueError) as exception_info:
		FileIO.save_boolean_mask_as_png(REF_BOOLEAN_MASK[1, :], f"{OUTPUT_DIR}/test_save_bad_boolean_mask.png")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."


##################################################
def test_open_png_as_boolean_mask():
	""" Test de la fonction open_png_as_boolean_mask. """
	mask = FileIO.open_png_as_boolean_mask(f"{OUTPUT_DIR}/test_save_boolean_mask.png")
	assert np.array_equal(REF_BOOLEAN_MASK, mask), "Le masque devrait correspondre à la référence."


##################################################
def test_open_png_as_boolean_mask_bad_file():
	""" Test de la fonction open_png_as_boolean_mask avec un fichier inexistant. """
	with pytest.raises(OSError) as exception_info:
		mask = FileIO.open_png_as_boolean_mask("bad_filename.png")
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."


##################################################
def test_save_sample_as_png():
	""" Test de la fonction save_sample_as_png. """
	FileIO.save_sample_as_png(REF_GRADIENT, f"{OUTPUT_DIR}/test_save_sample.png", 0)
	FileIO.save_sample_as_png(REF_GRADIENT, f"{OUTPUT_DIR}/test_save_sample_normalized.png", 100)
	FileIO.save_sample_as_png(np.zeros((256, 256)).astype(np.float32), f"{OUTPUT_DIR}/test_save_sample_black.png")


##################################################
def test_save_sample_as_png_bad_sample():
	""" Test de la fonction save_sample_as_png.	"""
	with pytest.raises(ValueError) as exception_info:
		FileIO.save_sample_as_png(REF_GRADIENT[1, :], f"{OUTPUT_DIR}/test_save_bad_sample.png")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."


##################################################
def test_open_png_as_sample():
	""" Test de la fonction open_png_as_sample. """
	sample = FileIO.open_png_as_sample(f"{OUTPUT_DIR}/test_save_sample.png")
	new_ref = REF_GRADIENT.astype(np.uint8).astype(np.float32)  # cast forcée, car les pixels ont des valeurs entières.
	assert np.allclose(new_ref, sample, atol=1e-5), "L'échantillon devrait correspondre à la référence avec une tolérance d'erreur."

	sample = FileIO.open_png_as_sample(f"{OUTPUT_DIR}/test_save_sample_normalized.png")
	assert np.allclose(new_ref, sample, atol=1), "L'échantillon devrait correspondre à la référence avec une tolérance d'erreur."
	# La tolérance est de 1 degré d'intensité, car au hasard du bruit la plage de la ref pourrait être différente de [0;255] dans de très rares cas.

	sample = FileIO.open_png_as_sample(f"{OUTPUT_DIR}/test_save_sample_black.png")
	assert np.allclose(sample, 0.0), "L'échantillon devrait être entièrement noir."


##################################################
def test_open_png_as_sample_bad_file():
	""" Test de la fonction open_png_as_sample avec un fichier inexistant. """
	with pytest.raises(OSError) as exception_info:
		sample = FileIO.open_png_as_sample("bad_filename.png")
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."


##################################################
def test_save_stack_as_tif():
	"""	Test de la fonction save_stack_as_tif. """
	FileIO.save_stack_as_tif(REF_STACK, f"{OUTPUT_DIR}/test_save_stack.tif")


##################################################
def test_save_stack_as_tif_2d():
	""" Test de la fonction save_stack_as_tif avec une image 2D. """
	FileIO.save_stack_as_tif(REF_GRADIENT, f"{OUTPUT_DIR}/test_save_stack_2D.tif")


##################################################
def test_save_stack_as_tif_bad_stack():
	""" Test de la fonction save_stack_as_tif avec une image 1D. """
	with pytest.raises(ValueError) as exception_info:
		FileIO.save_stack_as_tif(REF_GRADIENT[1, :], f"{OUTPUT_DIR}/test_save_stack_1D.tif")
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."


##################################################
def test_open_tif_as_stack():
	""" Test de la fonction open_tif_as_stack. """
	stack = FileIO.open_tif_as_stack(f"{OUTPUT_DIR}/test_save_stack.tif")
	assert np.allclose(REF_STACK, stack, atol=1), "L'échantillon devrait correspondre à la référence avec une tolérance d'erreur."


##################################################
def test_open_tif_as_stack_bad_file():
	""" Test de la fonction open_tif_as_stack avec un fichier inexistant. """
	with pytest.raises(OSError) as exception_info:
		stack = FileIO.open_tif_as_stack("bad_filename.png")
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."
