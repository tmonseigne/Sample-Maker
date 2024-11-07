""" Fonctions de manipulation de fichiers """

import os

import numpy as np
from numpy.typing import NDArray
from PIL import Image


# ==================================================
# region Boolean Mask IO
# ==================================================
##################################################
def save_boolean_mask_as_png(mask: NDArray[np.bool_], filename: str):
	"""
	Enregistre un masque binaire en tant qu'image PNG en niveaux de gris (noir et blanc) avec Pillow.

	:param mask: Tableau numpy 2D de type booléen représentant le masque.
	:param filename: Chemin du fichier PNG de sortie.
	"""
	grayscale_mask = (mask * 255).astype(np.uint8)     # Convertir le masque booléen en image en niveaux de gris (255 pour True, 0 pour False)
	image = Image.fromarray(grayscale_mask, mode='L')  # L pour niveau de gris
	image.save(filename)


##################################################
def open_png_as_boolean_mask(filename: str) -> NDArray[np.bool_]:
	"""
	Ouvre une image PNG en niveaux de gris et la convertit en un masque booléen.

	:param filename: Chemin du fichier PNG d'entrée.

	:return: Tableau numpy 2D de type booléen représentant le masque (True pour les pixels blancs, False pour les pixels noirs).
	"""
	if not os.path.isfile(filename): raise OSError(f"Le fichier \"{filename}\" est introuvable.")
	image = Image.open(filename).convert("L")  # Charger l'image en niveaux de gris
	grayscale_array = np.array(image)		   # Convertir l'image en tableau numpy
	boolean_mask = grayscale_array >= 128	   # Convertir les niveaux de gris en booléen : True pour les pixels >= 128, False pour < 128
	return boolean_mask

# ==================================================
# endregion Boolean Mask IO
# ==================================================
