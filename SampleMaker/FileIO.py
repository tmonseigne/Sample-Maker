""" Fichier de fonctions de manipulation de fichiers """

import os

import numpy as np
import tifffile as tiff
from numpy.typing import NDArray
from PIL import Image

from SampleMaker.Utils import add_extension

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
	name = add_extension(filename, ".png")
	grayscale = (mask * MAX_UI_8).astype(np.uint8)  # Convertir le masque booléen en image en niveaux de gris (255 pour True, 0 pour False)
	image = Image.fromarray(grayscale, mode='L')    # L pour niveau de gris
	image.save(name)


##################################################
def open_png_as_boolean_mask(filename: str) -> NDArray[np.bool_]:
	"""
	Ouvre une image PNG en niveaux de gris et la convertie en un masque booléen.

	:param filename: Chemin du fichier PNG d'entrée.
	:return: Tableau numpy 2D de type booléen représentant le masque (True pour les pixels blancs, False pour les pixels noirs).
	"""
	name = add_extension(filename, ".png")
	if not os.path.isfile(name): raise OSError(f"Le fichier \"{name}\" est introuvable.")
	image = Image.open(name).convert("L")		# Charger l'image en niveaux de gris
	grayscale = np.array(image)					# Convertir l'image en tableau numpy
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
	Si le percentile est égal à 100, l'intensité maximum deviendra 255
	Si on réduit le percentile, on considère que les quelques pour cent supérieurs sont des aberrations.

	:param sample: Tableau numpy 2D de type flottant représentant l'échantillon.
	:param filename: Chemin du fichier PNG de sortie.
	:param percentile: Percentile de l'intensité max qui deviendra un pixel blanc (par défaut 99%).
	"""

	percentile = np.clip(percentile, 0, 100)								# On évite les options bizarres des utilisateurs.
	if np.fabs(percentile) <= np.finfo(np.float32).eps: grayscale = sample  # Si le percentile est 0 il n'y a pas de mise à l'échelle

	else:  # Sinon mise à l'échelle
		max_i = np.percentile(sample, percentile)							# Calcul du percentile
		if max_i == 0: grayscale = np.zeros_like(sample, dtype=np.uint8)    # Si le maximum est 0, on remplit l'image avec des valeurs nulles
		else: grayscale = (sample * MAX_UI_8 / max_i)						# Normalisation entre 0 et 255

	grayscale = np.clip(grayscale, 0, MAX_UI_8).astype(np.uint8)			# On s'assure que toutes les valeurs sont entre 0 et 255.
	image = Image.fromarray(grayscale, mode='L')							# L pour niveau de gris
	image.save(filename)


##################################################
def open_png_as_sample(filename: str, intensity_factor: float = 1.0) -> NDArray[float]:
	"""
	Ouvre une image PNG en niveaux de gris.

	:param filename: Chemin du fichier PNG d'entrée.
	:param intensity_factor: Factor multiplicatif d'intensité (la valeur maximum pour un PNG en niveau de gris est 255 l'intensité n'a pas la même échelle)
	:return: Tableau numpy 2D de type flottant représentant l'échantillon.
	"""
	if not os.path.isfile(filename): raise OSError(f"Le fichier \"{filename}\" est introuvable.")
	image = Image.open(filename).convert("L")		# Charger l'image en niveaux de gris
	grayscale = np.array(image).astype(np.float32)  # Convertir l'image en tableau numpy
	grayscale *= intensity_factor					# Convertir les niveaux de gris en intensité
	return grayscale


# ==================================================
# endregion Sample PNG Image IO
# ==================================================


# ==================================================
# region Sample TIF Stack IO
# ==================================================
##################################################
def save_stack_as_tif(stack: NDArray[np.float32], filename: str):
	"""
	Sauvegarde un tableau 3D (ou 2D converti en 3D) dans un fichier TIFF multi-frame avec tifffile.

	:param stack: Tableau contenant l'image ou les frames :
	              - Si 2D (hauteur x largeur), convertit en pile 3D avec une seule frame.
	              - Si 3D (frames x hauteur x largeur), sauvegarde les frames en multi-frame.
	:param filename: Nom du fichier TIFF de sortie.
	"""
	if stack.ndim == 2: stack = stack[np.newaxis, ...]		# Si le tableau est 2D, le transformer en 3D avec une seule frame
	if stack.ndim != 3: raise ValueError("Le tableau doit être 2D (hauteur, largeur) ou 3D (frames, hauteur, largeur).")
	stack = np.clip(stack, 0, MAX_UI_16).astype(np.uint16)   # S'assure que les valeurs sont bien entre 0 et MAX_UI_16 et de type uint16
	tiff.imwrite(filename, stack, photometric="minisblack")	 # Sauvegarde la pile avec tifffile


##################################################
def open_tif_as_stack(filename: str) -> NDArray[np.float32]:
	"""
	Ouvre un fichier TIFF en tant que pile 3D (frames x hauteur x largeur).
    Si le fichier contient une seule image 2D, ajoute une dimension pour en faire une pile 3D.

    :param filename: Chemin du fichier TIFF à ouvrir.
    :return: Tableau 3D contenant les données TIFF.
	"""
	if not os.path.isfile(filename): raise OSError(f"Le fichier \"{filename}\" est introuvable.")
	stack = tiff.imread(filename)						# Lecture du fichier avec tifffile
	if stack.ndim == 2: stack = stack[np.newaxis, ...]  # Vérification des dimensions et conversion en pile 3D si nécessaire
	if stack.ndim != 3: raise ValueError(f"Fichier {filename} invalide : attendu 2D ou 3D, trouvé {stack.ndim} dimensions.")
	return stack.astype(np.float32)						# Retour avec conversion en float

# ==================================================
# endregion Sample TIF Stack IO
# ==================================================
