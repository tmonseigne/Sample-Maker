""" Fonctions de manipulation de fichiers """

import os

import numpy as np
from numpy.typing import NDArray
from PIL import Image

MAX_UI_8 = np.iinfo(np.uint8).max
MAX_UI_16 = np.iinfo(np.uint16).max

# ==================================================
# region Boolean Mask IO
# ==================================================
##################################################
def save_boolean_mask_as_png(mask: NDArray[np.bool_], filename: str):
	"""
	Enregistre un masque binaire en tant qu'image PNG en niveaux de gris (noir et blanc).

	:param mask: Tableau numpy 2D de type booléen représentant le masque.
	:param filename: Chemin du fichier PNG de sortie.
	"""
	grayscale = (mask * MAX_UI_8).astype(np.uint8)	 # Convertir le masque booléen en image en niveaux de gris (255 pour True, 0 pour False)
	image = Image.fromarray(grayscale, mode='L')	 # L pour niveau de gris
	image.save(filename)


##################################################
def open_png_as_boolean_mask(filename: str) -> NDArray[np.bool_]:
	"""
	Ouvre une image PNG en niveaux de gris et la convertit en un masque booléen.

	:param filename: Chemin du fichier PNG d'entrée.
	:return: Tableau numpy 2D de type booléen représentant le masque (True pour les pixels blancs, False pour les pixels noirs).
	"""
	if not os.path.isfile(filename): raise OSError(f"Le fichier \"{filename}\" est introuvable.")
	image = Image.open(filename).convert("L")   # Charger l'image en niveaux de gris
	grayscale = np.array(image)				  	# Convertir l'image en tableau numpy
	boolean_mask = grayscale >= (MAX_UI_8 / 2)  # Convertir les niveaux de gris en booléen : True pour les pixels >= 128, False pour < 128
	return boolean_mask


# ==================================================
# endregion Boolean Mask IO
# ==================================================


# ==================================================
# region Sample PNG Image IO
# ==================================================
##################################################
def save_sample_as_png(sample: NDArray[np.float32], filename: str, percentile: float = 100):
	"""
	Enregistre un échantillon en tant qu'image PNG en niveaux de gris.
	On normalise le tableau par rapport au percentile passé en paramètre.
	Si le percentile est égale à 100, l'intensité max deviendra 255
	Si on réduit le percentile, on considère que les quelques pourcents supérieurs sont des abhérations.

	:param sample: Tableau numpy 2D de type flottant représentant l'échantillon.
	:param filename: Chemin du fichier PNG de sortie.
	:param percentile: Percentile de l'intensité max qui deviendra un pixel blanc (par défaut 99%).
	"""

	percentile = np.clip(percentile, 0, 100) 					  # On évite les options bizarres des utilisateurs.
	max_i = np.percentile(sample, percentile)					  # Calcul du percentile

	if max_i == 0:
		grayscale = np.zeros_like(sample, dtype=np.uint8)		  # Si le maximum est 0, on remplit l'image avec des valeurs nulles
	else:
		grayscale = (sample * MAX_UI_8 / max_i).astype(np.uint8)  # Normalisation entre 0 et 255
		grayscale = np.clip(grayscale, 0, MAX_UI_8)				  # On s'assure que toutes les valeurs sont entre 0 et 255.
	image = Image.fromarray(grayscale, mode='L')				  # L pour niveau de gris
	image.save(filename)


##################################################
def open_png_as_sample(filename: str, intensity_factor: float = 1.0) -> NDArray[float]:
	"""
	Ouvre une image PNG en niveaux de gris.

	:param filename: Chemin du fichier PNG d'entrée.
	:param intensity_factor: Factor multiplicatif d'intensité (la valeur max pour un png en niveau de gris est 255 l'intensité n'a pas la même échelle)
	:return: Tableau numpy 2D de type flottant représentant l'échantillon.
	"""
	if not os.path.isfile(filename): raise OSError(f"Le fichier \"{filename}\" est introuvable.")
	image = Image.open(filename).convert("L")   	# Charger l'image en niveaux de gris
	grayscale = np.array(image).astype(np.float32)  # Convertir l'image en tableau numpy
	grayscale *= intensity_factor					# Convertir les niveaux de gris en intensité
	return grayscale


# ==================================================
# endregion Sample PNG Image IO
# ==================================================


# ==================================================
# region Sample TIFF Stack IO
# ==================================================
##################################################
def save_stack_as_tiff(stack: NDArray[np.float32], filename: str):
	"""
	Enregistre un échantillon en tant que pile d'image TIFF en niveaux de gris.

	:param stack: Tableau numpy 2D de type flottant représentant l'échantillon.
	:param filename: Chemin du fichier PNG de sortie.

	.. note:: Une image simple sera enregistré comme une pile d'une image.
	"""
	np.clip(stack, 0, MAX_UI_16)				 # On s'assure que toutes les valeurs sont entre 0 et max uint16
	image = Image.fromarray(stack, mode='I;16')  # I;16 pour uint16
	image.save(filename)


##################################################
def open_tiff_as_stack(filename: str) -> NDArray[np.float32]:
	"""
	Ouvre une pile d'image TIFF en niveaux de gris.

	:param filename: Chemin du fichier TIFF d'entrée.
	:return: Tableau numpy 2D de type flottant représentant l'échantillon.

	.. note:: Une image simple sera ouverte comme une pile d'une image.
	"""
	if not os.path.isfile(filename): raise OSError(f"Le fichier \"{filename}\" est introuvable.")
	image = Image.open(filename).convert("I;16")  # "I;16" pour uint16
	stack = np.array(image)						  # Convertir l'image en tableau numpy
	return stack

# ==================================================
# endregion Sample TIFF Stack IO
# ==================================================
