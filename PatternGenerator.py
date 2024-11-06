""" Fonctions de génération de pattern pour des masques de structure """

from enum import Enum
from itertools import accumulate
from typing import Any

import numpy as np
from numpy.typing import NDArray


##################################################
class Pattern(Enum):
	"""
	Enumération représentant les différents motifs disponibles pour la génération de masque.
	Chaque motif est associé à un identifiant unique pour être utilisé dans la fonction `generate_mask`.

	- STRIPES : Bandes verticales (alternance de bandes noires et blanches).
	- SQUARES : Carrés (pas encore implémenté).
	- SUN : Motif en forme de soleil 3D (pas encore implémenté).
	- EXISTING_IMAGE : Charge une image existante pour créer le masque (pas encore implémenté).
	"""
	STRIPES = 1
	SQUARES = 2
	SUN = 3
	EXISTING_IMAGE = 4

	def to_string(self) -> str:
		"""
		Retourne une chaîne de caractères représentant le motif correspondant.
		:return: Le nom du motif en français.
		"""
		return {
				Pattern.STRIPES:        "Bandes",
				Pattern.SQUARES:        "Carrés",
				Pattern.SUN:            "Soleil 3D",
				Pattern.EXISTING_IMAGE: "Image existante"
				}[self]


##################################################
def generate_mask(pattern: Pattern, size: int = 256, options: Any = None) -> NDArray[np.bool_]:
	"""
	Génère un masque en fonction du motif sélectionné.

	:param pattern: Le motif à utiliser pour générer le masque (Pattern.STRIPES, Pattern.SQUARES, etc.).
	:param size: Taille de l'image (optionnelle), par défaut 256.
	:param options: Dictionnaire contenant des options spécifiques au motif (longueur des bandes, effet miroir, etc.).
	:return: Masque sous forme de tableau numpy 2D de type booléen.
	"""
	# Création de l'image selon le motif
	if pattern == Pattern.STRIPES: return stripes_mask(size, options)
	if pattern == Pattern.SQUARES: return squares_mask(size, options)
	if pattern == Pattern.SUN: return sun_mask(size, options)
	if pattern == Pattern.EXISTING_IMAGE: return load_mask(size, options)
	return np.full((size, size), False, dtype=bool)


##################################################
def stripes_mask(size: int = 256, options: Any = None) -> NDArray[np.bool_]:
	"""
	Génération d'un masque avec un motif de bandes de différentes largeurs.

	Les bandes sont alternées entre noire et blanche, et leur taille est spécifiée par le dictionnaire `options`.
	Si l'option `Mirrored` est activée, le motif est symétrique (miroir central).
	L'option `Orientation` détermine si les bandes sont verticales (True) ou horizontales (False).

	:param size: Taille de l'image (optionnelle), par défaut 256.
	:param options: Dictionnaire avec les clés :
		- "Lengths" : Liste des longueurs des bandes (en nanomètres).
		- "Mirrored" : Booléen indiquant si le motif est symétrique (miroir central).
		- "Orientation" : Booléen pour l'orientation des bandes (True pour verticale, False pour horizontale).
	:return: Masque sous forme de tableau numpy 2D de type booléen.
	"""
	if not options: options = dict(Lengths=[200, 100, 50, 25, 12, 6], Mirrored=True, Orientation=True)
	mask = np.full((size, size), False, dtype=bool)
	limits = [float(x) for x in options["Lengths"] for _ in range(2)]  # Dupliquer chaque élément (bande noire et blanche de même taille)
	if options["Mirrored"]: limits.extend([1] + limits[::-1])  		   # Ajout du miroir
	cumulative_limits = list(accumulate(limits))  					   # Les limites sont cumulées pour avoir leur position par rapport à 0.
	ratio = float(size) / cumulative_limits[-1]  					   # Calcul du ratio pixel / longueur (la dernière case des limites cumulatives donne la somme des limites
	pixel_limits = [0] + [int(x * ratio) for x in cumulative_limits]   # Conversion des positions en pixel
	for i in range(0, len(pixel_limits) - 1, 2):  					   # Parcours des Bandes Blanches
		start, end = pixel_limits[i], pixel_limits[i + 1]  			   # Définition des limites en pixel
		if options["Orientation"]: mask[:, start:end] = True  		   # Les X sont les colonnes et les Y les lignes dans un tableau donc on inverse les indices
		else:   mask[start:end, :] = True
	return mask


##################################################
def squares_mask(size: int = 256, options: Any = None) -> NDArray[np.bool_]:
	"""
	Génération d'un masque avec un motif de carrés (actuellement vide, à implémenter).
	:param size: Taille de l'image (optionnelle), par défaut 256.
	:param options: Dictionnaire avec les options spécifiques au motif des carrés.
	:return: Masque sous forme de tableau numpy 2D de type booléen.
	"""
	mask = np.full((size, size), False, dtype=bool)
	return mask


##################################################
def sun_mask(size: int = 256, options: Any = None) -> NDArray[np.bool_]:
	"""
	Génération d'un masque avec un motif en forme de soleil 3D (actuellement vide, à implémenter).
	:param size: Taille de l'image (optionnelle), par défaut 256.
	:param options: Dictionnaire avec les options spécifiques au motif du soleil.
	:return: Masque sous forme de tableau numpy 2D de type booléen.
	"""
	mask = np.full((size, size), False, dtype=bool)
	return mask


##################################################
def load_mask(size: int = 256, options: Any = None) -> NDArray[np.bool_]:
	"""
	Charge un masque à partir d'une image existante (actuellement vide, à implémenter).
	:param size: Taille de l'image (optionnelle), par défaut 256.
	:param options: Dictionnaire avec les options pour charger une image existante.
	:return: Masque sous forme de tableau numpy 2D de type booléen.
	"""
	mask = np.full((size, size), False, dtype=bool)
	return mask
