""" Fonctions de génération de pattern pour des masques de structure """

import math
import os
from enum import Enum
from itertools import accumulate
from typing import Any

import numpy as np
from numpy.typing import NDArray

from FileIO import open_png_as_boolean_mask
from Utils import print_warning

##################################################
class Pattern(Enum):
	"""
	Enumération représentant les différents motifs disponibles pour la génération de masque.
	Chaque motif est associé à un identifiant unique pour être utilisé dans la fonction `generate_mask`.

	- NONE : Aucun masque (ou plutôt un masque entièrement blanc).
	- STRIPES : Bandes verticales (alternance de bandes noires et blanches).
	- SQUARES : Carrés (pas encore implémenté).
	- SUN : Motif en forme de soleil (pas encore implémenté).
	- EXISTING_IMAGE : Charge une image existante pour créer le masque (pas encore implémenté).
	"""
	NONE = 0
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
				Pattern.NONE: 			"None",
				Pattern.STRIPES:        "Bandes",
				Pattern.SQUARES:        "Carrés",
				Pattern.SUN:            "Soleil",
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
	return np.full((size, size), True, dtype=bool)


##################################################
def stripes_mask(size: int = 256, options: Any = None) -> NDArray[np.bool_]:
	"""
	Génération d'un masque avec un motif de bandes de différentes largeurs.

	Les bandes sont alternées entre noire et blanche, et leur taille est spécifiée par le dictionnaire `options`.
	Si l'option `Mirrored` est activée, le motif est symétrique (miroir central).
	L'option `Orientation` détermine si les bandes sont verticales (True) ou horizontales (False).

	:param size: Taille de l'image (optionnelle), par défaut 256.
	:param options: Dictionnaire avec les options spécifiques au motif des bandes :
		- "Lengths" : Liste des longueurs des bandes.
		- "Mirrored" : Booléen indiquant si le motif est symétrique (miroir central).
		- "Orientation" : Booléen pour l'orientation des bandes (True pour verticale, False pour horizontale).

	:return: Masque sous forme de tableau numpy 2D de type booléen.
	"""
	# Options par défaut si aucunes en entrée
	if not options: options = dict(Lengths=[200, 100, 50, 25, 12, 6], Mirrored=True, Orientation=True)
	mask = np.full((size, size), False, dtype=bool) 				   # Masque "noir" par défaut

	# Vérifie que les options existent
	if "Lengths" not in options:
		print_warning("Les longueurs sont introuvables dans les options. Masque blanc généré.")
		return ~mask
	if "Mirrored" not in options:
		print_warning("L'option miroir est introuvable dans les options. Masque blanc généré.")
		return ~mask
	if "Orientation" not in options:
		print_warning("L'orientation est introuvable dans les options. Masque blanc généré.")
		return ~mask

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
	:param options: Dictionnaire avec les options spécifiques au motif des carrés :
		- "Size" : Taille des carrées (en pixel).

	:return: Masque sous forme de tableau numpy 2D de type booléen.

	.. todo:: Ajouter la possibilité d'avoir une option nombre de carrés. (en cas de double options priorité au nombre de carrés et bords plus grand)
	"""
	if not options: options = dict(Size=32)			 # Options par défaut si aucunes en entrée
	mask = np.full((size, size), False, dtype=bool)  # Masque "noir" par défaut

	# Vérifie que la taille existe
	if "Size" not in options:
		print_warning("La taille est introuvable ou manquant dans les options. Masque blanc généré.")
		return ~mask

	s = options["Size"]								 # Taille de chaque carré blanc
	if s * 2 > size: 				 				 # Si on ne peut même pas placer un carré, le masque reste noir
		print_warning("La taille est trop grande. Masque blanc généré.")
		return ~mask
	n = (size - s) // (s * 2) + 1  					 # Calcul du nombre de carrés dans chaque direction (+1 pour maximiser le nombre de carrés)

	start = (size - (n * (s * 2) - s)) // 2			 # Calcul de la position du premier carré
	# Remplissage des carrés dans le masque
	for i in range(n):
		for j in range(n):
			x_start = start + i * (s * 2)
			y_start = start + j * (s * 2)
			mask[x_start:x_start + s, y_start:y_start + s] = True
	return mask


##################################################
def sun_mask(size: int = 256, options: Any = None) -> NDArray[np.bool_]:
	"""
	Génération d'un masque avec un motif en forme de soleil (actuellement vide, à implémenter).

	:param size: Taille de l'image (optionnelle), par défaut 256.
	:param options: Dictionnaire avec les options spécifiques au motif du soleil.

	:return: Masque sous forme de tableau numpy 2D de type booléen.
	"""
	if not options: options = dict(Rays=16)			  # Options par défaut si aucunes en entrée
	mask = np.full((size, size), False, dtype=bool)   # Masque "noir" par défaut

	# Vérifie que rays existe et est une puissance de 2.
	if "Rays" not in options or not (options["Rays"] & (options["Rays"] - 1)) == 0:
		print_warning("Le nombre de rayon est introuvable ou manquant dans les options. Masque blanc généré.")
		return ~mask

	center = size // 2								  # Centre de l'image
	n_segments = options["Rays"] * 2				  # Nombre de segments
	angle_per_segment = 2 * math.pi / n_segments      # Calcul de l'angle par segment (en radians)

	# Remplissage du masque
	for x in range(size):
		for y in range(size):
			dx, dy = x - center, y - center			 					# Coordonnées par rapport au centre
			angle = (math.atan2(dy, dx) + 2 * math.pi) % (2 * math.pi)  # Calcul de l'angle en radians par rapport au centre
			segment = int(angle // angle_per_segment)					# Déterminer le segment dans lequel le point se situe
			mask[x, y] = segment % 2 == 0								# Alterner la couleur (noir ou blanc) selon le segment

	return mask


##################################################
def load_mask(size: int = 256, options: Any = None) -> NDArray[np.bool_]:
	"""
	Charge un masque à partir d'une image existante (actuellement vide, à implémenter).

	:param size: Taille de l'image (optionnelle), par défaut 256.
	:param options: Dictionnaire avec les options pour charger une image existante.

	:return: Masque sous forme de tableau numpy 2D de type booléen.
	"""
	if not options or "Filename" not in options or not os.path.isfile(options["Filename"]):
		print_warning("Aucun fichier spécifié ou le fichier est introuvable. Masque blanc généré.")
		return np.full((size, size), True, dtype=bool)
	return open_png_as_boolean_mask(options["Filename"])
