""" Tests pour la génération de pattern """

from pathlib import Path

import numpy as np

from FileIO import open_png_as_boolean_mask, save_boolean_mask_as_png
from PatternGenerator import generate_mask, Pattern

SAMPLES_DIR = Path(__file__).parent / "Samples"


##################################################
def test_generate_mask_stripes():
	"""
	Test de la génération de masque pour le motif 'Bandes'.
	Vérifie que le masque est de la bonne taille et de type booléen.
	"""
	options = {"Lengths": [200, 100, 50, 25, 12, 6], "Mirrored": True, "Orientation": True}
	size = 256
	mask = generate_mask(Pattern.STRIPES, size, options)
	ref = open_png_as_boolean_mask(f"{SAMPLES_DIR}/Stripes1_ref.png")

	assert mask.shape == (size, size), "Le masque n'a pas la taille attendue."
	assert mask.dtype == bool, "Le masque devrait être de type booléen."
	assert np.any(mask), "Le masque devrait contenir des valeurs True."
	assert np.any(~mask), "Le masque devrait contenir des valeurs False."
	assert np.array_equal(ref, mask), "Le masque devrait correspondre à la référence."


##################################################
def test_stripes_mask_options():
	"""
	Test de la fonction stripes_mask avec des options spécifiques.
	Vérifie que les options de longueur et de miroir produisent un masque.
	"""
	options = {"Lengths": [200, 100, 50], "Mirrored": False, "Orientation": False}
	size = 128
	mask = generate_mask(Pattern.STRIPES, size, options)
	ref = open_png_as_boolean_mask(f"{SAMPLES_DIR}/Stripes2_ref.png")

	assert mask.shape == (size, size), "Le masque n'a pas la taille attendue."
	assert mask.dtype == bool, "Le masque devrait être de type booléen."
	assert np.any(mask), "Le masque des bandes devrait contenir des valeurs True."
	assert np.any(~mask), "Le masque devrait contenir des valeurs False."
	assert np.array_equal(ref, mask), "Le masque devrait correspondre à la référence."


##################################################
def test_generate_mask_squares():
	"""
	Test de la génération de masque pour le motif 'Carrés'.
	Vérifie que le masque est de la bonne taille et de type booléen.
	"""
	options = {"Size": 32}
	size = 256
	mask = generate_mask(Pattern.SQUARES)
	ref = open_png_as_boolean_mask(f"{SAMPLES_DIR}/Squares1_ref.png")

	assert mask.shape == (size, size), "Le masque n'a pas la taille attendue."
	assert mask.dtype == bool, "Le masque devrait être de type booléen."
	assert np.any(mask), "Le masque devrait contenir des valeurs True."
	assert np.any(~mask), "Le masque devrait contenir des valeurs False."
	assert np.array_equal(ref, mask), "Le masque devrait correspondre à la référence."

##################################################
def test_squares_mask_options_little():
	"""
	Test de la fonction squares_mask avec des options spécifiques.
	Vérifie que les options de taille produisent un masque avec de nombreux petits carrés.
	"""
	options = {"Size": 4}
	size = 256
	mask = generate_mask(Pattern.SQUARES, size, options)
	ref = open_png_as_boolean_mask(f"{SAMPLES_DIR}/Squares2_ref.png")

	assert mask.shape == (size, size), "Le masque n'a pas la taille attendue."
	assert mask.dtype == bool, "Le masque devrait être de type booléen."
	assert np.any(mask), "Le masque des bandes devrait contenir des valeurs True."
	assert np.any(~mask), "Le masque devrait contenir des valeurs False."
	assert np.array_equal(ref, mask), "Le masque devrait correspondre à la référence."

##################################################
def test_squares_mask_options_too_big():
	"""
	Test de la fonction squares_mask avec des options spécifiques.
	Vérifie que les options de taille produisent un masque noir si la taille et trop elevé.
	"""
	options = {"Size": 129}
	size = 256
	mask = generate_mask(Pattern.SQUARES, size, options)

	assert mask.shape == (size, size), "Le masque n'a pas la taille attendue."
	assert mask.dtype == bool, "Le masque devrait être de type booléen."
	assert np.all(~mask), "Le masque devrait contenir uniquement des valeurs False."

##################################################
def test_squares_mask_options_only_one():
	"""
	Test de la fonction squares_mask avec des options spécifiques.
	Vérifie que les options de taille produisent un masque avec un seul carré central si la valeur est égale à taille / 2.
	"""
	options = {"Size": 128}
	size = 256
	mask = generate_mask(Pattern.SQUARES, size, options)
	ref = open_png_as_boolean_mask(f"{SAMPLES_DIR}/Squares3_ref.png")

	assert mask.shape == (size, size), "Le masque n'a pas la taille attendue."
	assert mask.dtype == bool, "Le masque devrait être de type booléen."
	assert np.any(mask), "Le masque des bandes devrait contenir des valeurs True."
	assert np.any(~mask), "Le masque devrait contenir des valeurs False."
	assert np.array_equal(ref, mask), "Le masque devrait correspondre à la référence."


##################################################
def test_generate_mask_sun():
	"""
	Test de la génération de masque pour le motif 'Soleil'.
	Vérifie que le masque est de la bonne taille et de type booléen.
	"""
	size = 256
	mask = generate_mask(Pattern.SUN, size)

	assert mask.shape == (size, size), "Le masque n'a pas la taille attendue."
	assert mask.dtype == bool, "Le masque devrait être de type booléen."


##################################################
def test_generate_mask_existing_image():
	"""
	Test de la génération de masque pour le motif 'Image existante'.
	Vérifie que le masque est de la bonne taille et de type booléen.
	"""
	size = 256
	mask = generate_mask(Pattern.EXISTING_IMAGE, size)

	assert mask.shape == (size, size), "Le masque n'a pas la taille attendue."
	assert mask.dtype == bool, "Le masque devrait être de type booléen."
