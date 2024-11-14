""" Fonctions de génération de pattern pour des masques de structure """

import math
import os
from dataclasses import dataclass, field
from itertools import accumulate

import numpy as np
from numpy.typing import NDArray

from SampleMaker.FileIO import open_png_as_boolean_mask, save_boolean_mask_as_png
from SampleMaker.Pattern import Pattern, PatternType
from SampleMaker.Utils import print_warning


##################################################
@dataclass
class Mask:
	"""
	Classe permettant de créer et stocker un masque.

	Attributs :
		- **size (int)** : Taille du masque.
		- **pattern (Pattern)** : Motif à utiliser pour générer le masque.
	"""
	size: int = 256
	pattern: Pattern = field(default_factory=Pattern)
	mask: NDArray[np.bool_] = field(init=False)

	# ==================================================
	# region Initialisation / Setter
	# ==================================================
	##################################################
	def __post_init__(self):
		"""
		Méthode appelée automatiquement après l'initialisation du dataclass.
		Initialise le masque avec le motif spécifié.
		"""
		self._generate()

	##################################################
	def set_size(self, size: int):
		"""
		Change la taille du masque et le (re)génère.

		:param size: Nouvelle taille du masque.
		"""
		self.size = size
		self._generate()

	##################################################
	def set_pattern(self, pattern: Pattern):
		"""
		Change le motif du masque et le (re)génère.

		:param pattern: Nouveau motif du masque.
		"""
		self.pattern = pattern
		self._generate()

	# ==================================================
	# endregion Initialisation / Setter
	# ==================================================

	# ==================================================
	# region Mask Generator
	# ==================================================
	##################################################
	def _generate(self):
		"""
		Génère un masque
		"""
		# Création de l'image selon le motif
		if self.pattern.pattern == PatternType.STRIPES: self._stripes_mask()
		elif self.pattern.pattern == PatternType.SQUARES: self._squares_mask()
		elif self.pattern.pattern == PatternType.SUN: self._sun_mask()
		elif self.pattern.pattern == PatternType.EXISTING_IMAGE: self.open(self.pattern.options.path)
		else: self.mask = np.full((self.size, self.size), True, dtype=bool)

	##################################################
	def _stripes_mask(self):
		"""
		Génération d'un masque avec un motif de bandes.
		"""
		self.mask = np.full((self.size, self.size), False, dtype=bool)				 # Masque "noir" par défaut
		limits = [float(x) for x in self.pattern.options.lengths for _ in range(2)]  # Dupliquer chaque élément (bande noire et blanche de même taille)
		if self.pattern.options.mirror: limits.extend([1] + limits[::-1])			 # Ajout du miroir
		cumulative_limits = list(accumulate(limits))								 # Les limites sont cumulées pour avoir leur position par rapport à 0.
		ratio = float(self.size) / cumulative_limits[-1]							 # Calcul du ratio pixel / longueur
		pixel_limits = [0] + [int(x * ratio) for x in cumulative_limits]			 # Conversion des positions en pixel
		for i in range(0, len(pixel_limits) - 1, 2):								 # Parcours des Bandes Blanches
			start, end = pixel_limits[i], pixel_limits[i + 1]						 # Définition des limites en pixel
			# Les X sont les colonnes et les Y les lignes dans un tableau donc attention aux indices.
			if self.pattern.options.orientation: self.mask[:, start:end] = True
			else:   self.mask[start:end, :] = True

	##################################################
	def _squares_mask(self):
		"""
		Génération d'un masque avec un motif de carrés.
		"""
		self.mask = np.full((self.size, self.size), False, dtype=bool)  # Masque "noir" par défaut

		s = self.pattern.options.size  # Taille de chaque carré blanc
		if s * 2 > self.size:		   # Si on ne peut même pas placer un carré, le masque reste noir
			print_warning("La taille est trop grande. Masque blanc généré.")
			self.mask = ~self.mask	   # Transformation en masque blanc
			return

		n = (self.size - s) // (s * 2) + 1  # Calcul du nombre de carrés dans chaque direction (+1 pour maximiser le nombre de carrés)
		# Remplissage des carrés dans le masque
		start = (self.size - (n * (s * 2) - s)) // 2  # Calcul de la position du premier carré
		for i in range(n):
			for j in range(n):
				x_start = start + i * (s * 2)
				y_start = start + j * (s * 2)
				self.mask[x_start:x_start + s, y_start:y_start + s] = True

	##################################################
	def _sun_mask(self):
		"""
		Génération d'un masque avec un motif en forme de soleil.
		"""
		self.mask = np.full((self.size, self.size), False, dtype=bool)  # Masque "noir" par défaut

		r = self.pattern.options.ray_count
		if not (r & r - 1) == 0:											# Vérifie que rays est une puissance de 2.
			print_warning("Le nombre de rayon est introuvable ou manquant dans les options. Masque blanc généré.")
			self.mask = ~self.mask											# Transformation en masque blanc
			return

		center = self.size // 2												# Centre de l'image
		n_segments = r * 2													# Nombre de segments
		angle_per_segment = 2 * math.pi / n_segments						# Calcul de l'angle par segment (en radians)

		# Remplissage du masque
		for x in range(self.size):
			for y in range(self.size):
				dx, dy = x - center, y - center								# Coordonnées par rapport au centre
				angle = (math.atan2(dy, dx) + 2 * math.pi) % (2 * math.pi)  # Calcul de l'angle en radians par rapport au centre
				segment = int(angle // angle_per_segment)					# Déterminer le segment dans lequel le point se situe
				self.mask[x, y] = segment % 2 == 0							# Alterner la couleur (noir ou blanc) selon le segment

	# ==================================================
	# endregion Mask Generator
	# ==================================================

	# ==================================================
	# region IO
	# ==================================================
	##################################################
	def __str__(self):
		"""
		Retourne un résumé des caractéristiques de la pile.
		"""
		summary = (
				f"Size: {self.size}, {self.pattern}"
		)
		return summary

	##################################################
	def save(self, filename):
		"""
		Enregistre le masque comme un fichier png.
		:param filename: Nom du fichier à enregistrer
		"""
		save_boolean_mask_as_png(self.mask, filename)

	##################################################
	def open(self, filename):
		"""
		Ouvre un fichier png et le transforme en masque de booléen
		:param filename: Nom du fichier à ouvrir
		"""
		self.pattern = Pattern.from_pattern(PatternType.EXISTING_IMAGE, {"path": filename})
		if not os.path.isfile(self.pattern.options.path):
			print_warning(f"Aucun fichier spécifié ou le fichier est introuvable. Masque blanc de taille {self.size} généré.")
			self.mask = np.full((self.size, self.size), True, dtype=bool)
		else:
			self.mask = open_png_as_boolean_mask(filename)
			self.size = self.mask.shape[0]

# ==================================================
# endregion IO
# ==================================================
