""" Fichier de la classe Stack """

from enum import Enum
from typing import Any

import numpy as np
from numpy.typing import NDArray

from Mask import MaskPattern
from SampleGenerator import compute_area


##################################################
class StackModel(Enum):
	"""
	Énumération représentant les différents modèles de piles disponibles.
	Chaque modèle est associé à un identifiant unique pour être utilisé dans la fonction `generate`.

	- NONE : Aucun modèle particulier (les échantillons sont indépendants les uns des autres).
	"""
	NONE = 0

	def to_string(self) -> str:
		"""
		Retourne une chaîne de caractères représentant le motif correspondant.

		:return: Le nom du motif en français.
		"""
		return {
				StackModel.NONE: "None",
				}[self]

##################################################
class Stack:
	"""
	Classe permettant de stocker une pile d'images

	Attributs :
		- **pixel_size (int)** : Taille d'un pixel en nanomètres.
		- **density (float)** : Densité de molécules par micromètre carré.
		- **pattern (Pattern)** : Motif à utiliser pour générer le masque.
		- **pattern_options (Dict)** : Options spécifiques pour le motif.
		- **intensity (float)** : Intensité de base du fluorophore.
		- **variation (float)** : Variation d'intensité aléatoire.
		- **astigmatism_ratio (float)** : Ratio de l'astigmatisme.
		- **snr (float)** : Rapport signal sur bruit désiré.
		- **base_background (float)** : Intensité de fond de base du microscope, typiquement autour de 500.
		- **stack_model (StackModel)** : Modèle de la pile.
		- **stack_model_options (Dict)** : Options spécifiques pour le modèle de la pile.
		- **stack (np.ndarray)** : Tableau numpy 3D stockant la pile d'images.
	"""

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def __init__(self):
		"""
		Constructeur par défaut (vide)
		"""
		self.size = None
		self.pixel_size = None
		self.density = None
		self.pattern = None
		self.pattern_options = None
		self.intensity = None
		self.variation = None
		self.astigmatism_ratio = None
		self.snr = None
		self.base_background = None
		self.base_noise_std = None
		self.stack_model = None
		self.stack_model_options = None
		self.stack = None

	##################################################
	def initialize(self, size: int = 256, pixel_size: int = 160, density: float = 1.0,
				   pattern: MaskPattern = MaskPattern.NONE, pattern_options: Any = None,
				   intensity: float = 100, variation: float = 10, astigmatism_ratio: float = 2.0,
				   snr: float = 10.0, base_background: float = 500, base_noise_std: float = 12,
				   stack_model: StackModel = StackModel.NONE, stack_model_options: Any = None):
		"""
		Initialise une instance de la classe Stack avec un tableau numpy 3D de type float.

		:param size: Taille de l'image en pixels (par défaut : 256). Cela correspond à la dimension d'un côté de l'image carrée.
		:param pixel_size: Taille d'un pixel en nanomètres (par défaut : 160). Utilisé pour calculer la surface de l'image.
		:param density: Densité de molécules par micromètre carré (par défaut 1.0).
		:param pattern: Le motif à utiliser pour générer le masque (Pattern.STRIPES, Pattern.SQUARES, etc.).
		:param pattern_options: Dictionnaire contenant des options spécifiques au motif (longueur des bandes, effet miroir, etc.).
		:param intensity: Intensité de base du fluorophore (par défaut 100).
		:param variation: Variation d'intensité aléatoire appliquée à l'intensité du fluorophore (par défaut 10).
		:param astigmatism_ratio: Ratio de l'astigmatisme (par défaut 2 indique une déformation de X par rapport à Y de maximum 2).
		:param snr: Le rapport signal sur bruit désiré (par défaut 10 un excellent SNR).
		:param base_background: Intensité de fond de base du microscope, typiquement autour de 500.
		:param base_noise_std: Écart-type du bruit gaussien de fond.
		:param stack_model: Modèle de la pile.
		:param stack_model_options: Options spécifiques pour le modèle de la pile.
		"""
		self.size = size
		self.pixel_size = pixel_size
		self.density = density
		self.pattern = pattern
		self.pattern_options = pattern_options
		self.intensity = intensity
		self.variation = variation
		self.astigmatism_ratio = astigmatism_ratio
		self.snr = snr
		self.base_background = base_background
		self.base_noise_std = base_noise_std
		self.stack_model = stack_model
		self.stack_model_options = stack_model_options
		self.stack = np.zeros((size, size, 0), dtype=np.float32)

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Layer Manipulation
	# ==================================================
	##################################################
	def add_layer(self, layer: NDArray[np.float32], index: int):
		"""
		Ajoute une couche à la pile d'images.

		:param layer: Une couche 2D à ajouter à la pile.
		:param index: Index de la profondeur où ajouter la couche.
		"""
		if index < 0: index = self.stack.shape[0]  										  # Un index négatif permet de placer à la fin
		if layer.shape != self.stack.shape[1:]: raise ValueError(f"La taille de la couche doit être {self.stack.shape[1:]} pour correspondre à la pile.")
		if index < self.stack.shape[0]: self.stack[index] = layer 						  # Si l'index est dans les limites, remplace la couche
		else: self.stack = np.concatenate((self.stack, layer[np.newaxis, :, :]), axis=0)  # Si l'index est au-delà, ajoute la couche à la fin

	##################################################
	def get_layer(self, index: int) -> NDArray[np.float32]:
		"""
		Récupère une couche de la pile.

		:param index: Index de la couche à récupérer.
		:return: La couche 2D correspondante.
		"""
		if not (0 <= index < self.stack.shape[0]): raise IndexError("Index hors de la profondeur de la pile.")
		return self.stack[index]

	# ==================================================
	# endregion Layer Manipulation
	# ==================================================

	# ==================================================
	# region Stack Generator
	# ==================================================
	##################################################
	def generate(self, n: int):
		"""
		Génère une pile de n échantillons
		:param n: Nombre d'échantillons de la pile

		.. todo:: A faire
		"""
		# générer un sample
		# Ajouter le sample à la pile
		print("TODO")

	# ==================================================
	# endregion Stack Generator
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
				f"Stack Summary:\n"
				f"  Pixel size: {self.pixel_size} nm, Surface: {compute_area(self.size, self.pixel_size)} um², Density: {self.density}\n"
				f"  Pattern: {self.pattern}, Options: {self.pattern_options}\n"
				f"  Intensity: {self.intensity}, Varition: {self.variation}, Astigmatisme Ratio: {self.astigmatism_ratio}\n"
				f"  SNR: {self.snr}, Background: {self.base_background}, Deviation: {self.base_noise_std}\n"
				f"  Stack Model: {self.stack_model}, Options: {self.stack_model_options}\n"
				f"  Shape: {self.stack.shape if self.stack is not None else 'None'}\n"
				f"  Max Value: {self.stack.max() if self.stack is not None else 'None'}\n"
				f"  Min Value: {self.stack.min() if self.stack is not None else 'None'}"
		)
		return summary

	##################################################
	def save(self, filename):
		print("TODO")

	##################################################
	def open(self, filename):
		print("TODO")

	# ==================================================
	# endregion IO
	# ==================================================
