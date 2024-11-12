""" Tests pour la génération de pattern """
import os
from pathlib import Path
import numpy as np

from FileIO import open_png_as_sample, save_sample_as_png
from Utils import add_grid, print_error, print_warning

INPUT_DIR = Path(__file__).parent / "Input"
OUTPUT_DIR = Path(__file__).parent / "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)


##################################################
def test_clean_extension():
	"""
	Test de la fonction clean extension.
	"""
	print("TODO")


##################################################
def test_print_error():
	"""
	Test de la fonction print error.
	"""

	print_error("Message d'erreur"), "L'affichage n'a pas pu être effectué"


##################################################
def test_print_warning():
	"""
	Test de la fonction print warning.
	"""

	print_warning("Message d'avertissement"), "L'affichage n'a pas pu être effectué"


##################################################
def test_add_grid():
	"""
	Test de la fonction add grid.
	"""

	size = 256
	image = np.zeros((size, size), dtype=np.float32)   # Image Noire
	image = add_grid(image, 30, 20, 255)   # Image avec la grille
	save_sample_as_png(image, f"{OUTPUT_DIR}/Grid.png")
	ref = open_png_as_sample(f"{INPUT_DIR}/Grid.png")
	assert np.allclose(ref, image), "L'imagee devrait correspondre à la référence."

