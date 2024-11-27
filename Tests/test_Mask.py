""" Fichier des tests pour la génération de masque """

import os
from pathlib import Path

import numpy as np
import pytest

from SampleMaker.Mask import Mask
from SampleMaker.Pattern import Pattern, PatternType
from SampleMaker.Tools.FileIO import open_png_as_boolean_mask

INPUT_DIR = Path(__file__).parent / "Input"
OUTPUT_DIR = Path(__file__).parent / "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)


##################################################
def test_mask():
	""" Test basique de la classe (constructeur, getter, setter) """
	mask = Mask()
	new_size = 128
	new_pattern = Pattern.from_pattern(PatternType.STRIPES)
	mask.size = new_size
	assert mask.size == 128, "Le masque n'a pas la taille attendue."
	mask.pattern = new_pattern
	assert mask.pattern == new_pattern, "Le masque n'a pas la taille attendue."
	print(f"\n{mask}")
	mask.save(f"{OUTPUT_DIR}/test_mask.png")


##################################################
def test_generate_mask_stripes():
	"""
	Test de la génération de masque pour le motif 'Bandes'.
	Vérifie que le masque est de la bonne taille, de type booléen et correspond à la référence.
	"""
	size = 256
	mask = Mask(size, Pattern.from_pattern(PatternType.STRIPES))
	ref = open_png_as_boolean_mask(f"{INPUT_DIR}/Stripes1_ref.png")

	assert mask.mask.shape == (size, size), "Le masque n'a pas la taille attendue."
	assert mask.mask.dtype == bool, "Le masque devrait être de type booléen."
	assert np.any(mask.mask), "Le masque devrait contenir des valeurs True."
	assert np.any(~mask.mask), "Le masque devrait contenir des valeurs False."
	assert np.array_equal(ref, mask.mask), "Le masque devrait correspondre à la référence."


##################################################
def test_stripes_mask_options():
	"""
	Test de la fonction stripes_mask avec des options spécifiques.
	Vérifie que les options de longueur et de miroir produisent un masque.
	"""
	size = 128
	options = {"lengths": [200, 100, 50], "mirror": False, "orientation": False}
	mask = Mask(size, Pattern.from_pattern(PatternType.STRIPES, options))
	ref = open_png_as_boolean_mask(f"{INPUT_DIR}/Stripes2_ref.png")

	assert mask.mask.shape == (size, size), "Le masque n'a pas la taille attendue."
	assert mask.mask.dtype == bool, "Le masque devrait être de type booléen."
	assert np.any(mask.mask), "Le masque devrait contenir des valeurs True."
	assert np.any(~mask.mask), "Le masque devrait contenir des valeurs False."
	assert np.array_equal(ref, mask.mask), "Le masque devrait correspondre à la référence."


##################################################
def test_stripes_mask_options_bad():
	"""
	Test de la fonction stripes_mask avec des options spécifiques mauvaises.
	"""
	mask = None
	size = 128
	options = {"Longueurs": [200, 100, 50], "Mirrored": False, "Orientation": False}
	with pytest.raises(TypeError) as exception_info:
		mask = Mask(size, Pattern.from_pattern(PatternType.STRIPES, options))

	assert exception_info.type == TypeError, "L'erreur relevé n'est pas correcte."
	assert mask is None, "Le masque a été créé au lieu de crash."


##################################################
def test_generate_mask_squares():
	"""
	Test de la génération de masque pour le motif 'Carrés'.
	Vérifie que le masque est de la bonne taille, de type booléen et correspond à la référence
	"""
	size = 256
	options = {"size": 32}
	mask = Mask(size, Pattern.from_pattern(PatternType.SQUARES, options))
	ref = open_png_as_boolean_mask(f"{INPUT_DIR}/Squares1_ref.png")

	assert mask.mask.shape == (size, size), "Le masque n'a pas la taille attendue."
	assert mask.mask.dtype == bool, "Le masque devrait être de type booléen."
	assert np.any(mask.mask), "Le masque devrait contenir des valeurs True."
	assert np.any(~mask.mask), "Le masque devrait contenir des valeurs False."
	assert np.array_equal(ref, mask.mask), "Le masque devrait correspondre à la référence."


##################################################
def test_squares_mask_options_little():
	"""
	Test de la fonction squares_mask avec des options spécifiques.
	Vérifie que les options de taille produisent un masque avec de nombreux petits carrés.
	"""
	size = 256
	options = {"size": 4}
	mask = Mask(size, Pattern.from_pattern(PatternType.SQUARES, options))
	ref = open_png_as_boolean_mask(f"{INPUT_DIR}/Squares2_ref.png")

	assert mask.mask.shape == (size, size), "Le masque n'a pas la taille attendue."
	assert mask.mask.dtype == bool, "Le masque devrait être de type booléen."
	assert np.any(mask.mask), "Le masque devrait contenir des valeurs True."
	assert np.any(~mask.mask), "Le masque devrait contenir des valeurs False."
	assert np.array_equal(ref, mask.mask), "Le masque devrait correspondre à la référence."


##################################################
def test_squares_mask_options_bad():
	"""
	Test de la fonction squares_mask avec des options spécifiques.
	Vérifie que les options de taille produisent un masque blanc si la taille est trop élevée.
	"""
	size = 128
	options = {"size": 65}  # Taille trop grande
	mask = Mask(size, Pattern.from_pattern(PatternType.SQUARES, options))

	assert mask.mask.shape == (size, size), "Le masque n'a pas la taille attendue."
	assert mask.mask.dtype == bool, "Le masque devrait être de type booléen."
	assert np.all(mask.mask), "Le masque devrait contenir uniquement des valeurs True."

	mask = None
	options = {"Taille": 4}  # Dictionnaire incorrect
	with pytest.raises(TypeError) as exception_info:
		mask = Mask(size, Pattern.from_pattern(PatternType.SQUARES, options))

	assert exception_info.type == TypeError, "L'erreur relevée n'est pas correcte."
	assert mask is None, "Le masque a été créé au lieu de crash."


##################################################
def test_squares_mask_options_only_one():
	"""
	Test de la fonction squares_mask avec des options spécifiques.
	Vérifie que les options de taille produisent un masque avec un seul carré central si la valeur est égale à taille / 2.
	"""
	size = 256
	options = {"size": 128}
	mask = Mask(size, Pattern.from_pattern(PatternType.SQUARES, options))
	ref = open_png_as_boolean_mask(f"{INPUT_DIR}/Squares3_ref.png")

	assert mask.mask.shape == (size, size), "Le masque n'a pas la taille attendue."
	assert mask.mask.dtype == bool, "Le masque devrait être de type booléen."
	assert np.any(mask.mask), "Le masque devrait contenir des valeurs True."
	assert np.any(~mask.mask), "Le masque devrait contenir des valeurs False."
	assert np.array_equal(ref, mask.mask), "Le masque devrait correspondre à la référence."


##################################################
def test_generate_mask_sun():
	"""
	Test de la génération de masque pour le motif 'Soleil'.
	Vérifie que le masque est de la bonne taille, de type booléen et correspond à la référence.
	"""
	size = 256
	options = {"ray_count": 16}
	mask = Mask(size, Pattern.from_pattern(PatternType.SUN, options))
	ref = open_png_as_boolean_mask(f"{INPUT_DIR}/Sun1_ref.png")

	assert mask.mask.shape == (size, size), "Le masque n'a pas la taille attendue."
	assert mask.mask.dtype == bool, "Le masque devrait être de type booléen."
	assert np.any(mask.mask), "Le masque devrait contenir des valeurs True."
	assert np.any(~mask.mask), "Le masque devrait contenir des valeurs False."
	assert np.array_equal(ref, mask.mask), "Le masque devrait correspondre à la référence."


##################################################
def test_sun_mask_options():
	"""
	Test de la fonction sun_mask avec des options spécifiques.
	Vérifie que les options de taille produisent un masque avec un seul carré central si la valeur est égale à taille / 2.
	"""
	size = 128
	options = {"ray_count": 4}
	mask = Mask(size, Pattern.from_pattern(PatternType.SUN, options))
	ref = open_png_as_boolean_mask(f"{INPUT_DIR}/Sun2_ref.png")

	assert mask.mask.shape == (size, size), "Le masque n'a pas la taille attendue."
	assert mask.mask.dtype == bool, "Le masque devrait être de type booléen."
	assert np.any(mask.mask), "Le masque devrait contenir des valeurs True."
	assert np.any(~mask.mask), "Le masque devrait contenir des valeurs False."
	assert np.array_equal(ref, mask.mask), "Le masque devrait correspondre à la référence."


##################################################
def test_sun_mask_options_bad():
	"""
	Test de la fonction sun_mask avec des options spécifiques.
	Vérifie que les options de nombre de rayons produisent un masque blanc si ce n'est un multiple de 2.
	"""
	size = 128
	options = {"ray_count": 3}
	mask = Mask(size, Pattern.from_pattern(PatternType.SUN, options))

	assert mask.mask.shape == (size, size), "Le masque n'a pas la taille attendue."
	assert mask.mask.dtype == bool, "Le masque devrait être de type booléen."
	assert np.all(mask.mask), "Le masque devrait contenir uniquement des valeurs True."


##################################################
def test_generate_mask_existing_image():
	"""
	Test de la génération de masque pour le motif 'Image existante'.
	Vérifie que le masque est de type booléen (la taille en entrée est théorique, car elle dépend du fichier en entrée).
	"""
	options = {"path": f"{INPUT_DIR}/PALM_ref.png"}
	mask = Mask(_pattern=Pattern.from_pattern(PatternType.EXISTING_IMAGE, options))

	assert mask.mask.dtype == bool, "Le masque devrait être de type booléen."
	assert np.any(mask.mask), "Le masque devrait contenir des valeurs True."
	assert np.any(~mask.mask), "Le masque devrait contenir des valeurs False."


##################################################
def test_existing_mask_options_bad_filename():
	"""
	Test de la génération de masque pour le motif 'Image existante'.
	Vérifie que le masque est de la bonne taille, de type booléen et est entièrement blanc.
	"""
	options = {"path": f"{INPUT_DIR}/bad_file.png"}
	mask = Mask(_pattern=Pattern.from_pattern(PatternType.EXISTING_IMAGE, options))

	assert mask.mask.shape == (256, 256), "Le masque n'a pas la taille attendue."
	assert mask.mask.dtype == bool, "Le masque devrait être de type booléen."
	assert np.all(mask.mask), "Le masque devrait contenir uniquement des valeurs True."


##################################################
def test_none_mask():
	"""
	Test de la génération d'un masque nulle (donc entièrement blanc).
	Vérifie que le masque est de la bonne taille, de type booléen et est blanc.
	"""
	mask = Mask()
	print(f"Test print mask setting: {mask}")
	assert mask.mask.shape == (256, 256), "Le masque n'a pas la taille attendue."
	assert mask.mask.dtype == bool, "Le masque devrait être de type booléen."
	assert np.all(mask.mask), "Le masque devrait contenir uniquement des valeurs True."
