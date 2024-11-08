""" Fonctions de génération d'images Simulées """

import math
import os
from enum import Enum
from itertools import accumulate
from typing import Any

import numpy as np
from numpy.typing import NDArray

from FileIO import open_png_as_boolean_mask
from PatternGenerator import Pattern
from Utils import print_warning


##################################################
def generate_sample(size: int = 256, pixel_size: int = 160, density: float = 1.0, snr: float = 10.0, pattern=Pattern.NONE):
	print("TODO")


##################################################
def compute_molecule_number(size: int = 256, pixel_size: int = 160, density: float = 1.0) -> int:
	"""
	Calcule le nombre estimé de molécules dans une image carrée en fonction de sa taille, de la taille d'un pixel et de la densité de molécules.

	Cette fonction est utile pour estimer la quantité totale de molécules dans une région d'image en fonction de paramètres physiques.

	:param size: Taille de l'image en pixels (par défaut : 256). Cela correspond à la dimension d'un côté de l'image carrée.
	:param pixel_size: Taille d'un pixel en nanomètres (par défaut : 160). Utilisé pour calculer la surface de l'image.
	:param density: Densité de molécules par micromètre carré (par défaut 1.0).
	:return: Nombre estimé de molécules dans l'image.
	"""
	im_size = float(size * pixel_size) / 1000  # Calculer la taille de l'image en micromètres (conversion depuis la taille des pixels en nanomètres
	im_area = im_size ** 2  				   # Calculer l'aire de l'image en micromètres carrés
	molecule_number = int(im_area * density)   # Calculer le nombre de molécules en fonction de la densité
	return molecule_number


##################################################
def compute_molecule_localisation(size: int = 256, pixel_size: int = 160, density: float = 1.0) -> NDArray[float]:
	"""
	Génère un tableau de positions 3D aléatoires pour les molécules en fonction de la taille de l'image,
	de la taille d'un pixel et de la densité des molécules. la coordonnée Z sera comprise entre -1 et 1.

	:param size: Taille de l'image en pixels (par défaut 256), qui correspond à la dimension d'un côté de l'image carrée.
	:param pixel_size: Taille d'un pixel en nanomètres (par défaut 160).
	:param density: Densité de molécules par micromètre carré (par défaut 1.0).
	:return: Un tableau numpy de N lignes et 3 colonnes, où chaque ligne représente les coordonnées (x, y, z) d'une molécule.
	"""
	# Calculer le nombre total de molécules à partir des paramètres donnés
	n_molecules = compute_molecule_number(size, pixel_size, density)

	# Générer des positions aléatoires pour chaque molécule
	# x et y sont des positions flottantes aléatoires dans l'espace 2D de l'image (0 à size)
	# z est une position flottante aléatoire entre -1 et 1.
	x = np.random.uniform(0, size, n_molecules)
	y = np.random.uniform(0, size, n_molecules)
	z = np.random.uniform(-1, 1, n_molecules)

	# Combiner les coordonnées dans un tableau de forme (n_molecules, 3)
	molecule_positions = np.vstack((x, y, z)).T

	return molecule_positions


##################################################
def apply_mask(localisation: NDArray[float], mask: NDArray[np.bool_]) -> NDArray[float]:
	"""
	Filtre les positions des molécules en fonction d'un masque booléen 2D, ne conservant que celles dont les coordonnées
	(x arrondi, y arrondi) correspondent à des positions "True" dans le masque.

	:param localisation: Tableau numpy de positions des molécules de forme (N, 3), où chaque ligne contient les coordonnées (x, y, z).
	                     Les coordonnées x et y sont en flottants et doivent être dans les limites de `mask`.
	:param mask: Tableau numpy 2D de type booléen indiquant les zones de validité (True) pour les molécules.
	             La forme de `mask` doit être (size, size), où `size` correspond à la taille de l'image.
	:return: Tableau numpy filtré de positions de molécules (x, y, z) où seules les molécules dans les zones "True" du masque sont conservées.
	:rtype: NDArray[float]

	:example:
	>>> localisation = np.array([[10.5, 20.2, 0.3], [5.0, 15.1, -0.2], [250.4, 140.5, 0.0]])
	>>> mask = np.random.choice([True, False], size=(256, 256))
	>>> filtered_positions = apply_mask(localisation, mask)
	"""

	# Convertir les coordonnées x et y en entiers pour correspondre aux pixels dans le masque, clip permet d'éviter les positions en dehors du masque.
	x_int = np.clip(localisation[:, 0].astype(int), 0, mask.shape[0] - 1)
	y_int = np.clip(localisation[:, 1].astype(int), 0, mask.shape[1] - 1)

	# Sélectionner les positions des molécules dont le masque est "True" aux indices (x, y)
	valid_indices = mask[x_int, y_int]
	filtered_localisation = localisation[valid_indices]

	return filtered_localisation


##################################################
def add_psf(image):
	print("TODO")


##################################################
def add_snr(image, snr: float = 10.0):
	print("TODO")

