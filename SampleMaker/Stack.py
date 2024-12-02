"""
Ce module définit la classe `Stack`, qui fournit une structure flexible pour gérer des piles
d'images ou d'échantillons 2D, représentées comme des tableaux 3D.

Fonctionnalités principales :

- **Manipulation d'échantillons** : Ajouter ou récupérer des échantillons 2D dans une pile 3D.
- **Entrée/Sortie (IO)** : Charger ou enregistrer des piles dans des fichiers TIF.
- **Affichage** : Générer une représentation textuelle décrivant la pile et son contenu.

"""

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

from SampleMaker.Tools import open_tif_as_stack, save_stack_as_tif


##################################################
@dataclass
class Stack:
	"""
	Classe permettant de stocker une pile d'images

	Attributs :
		- **stack (np.ndarray)** : Tableau numpy 3D stockant la pile d'images.
	"""
	stack: NDArray[np.float32] = field(init=False, default_factory=lambda: np.empty((0, 0, 0), dtype=np.float32))

	# ==================================================
	# region Sample Manipulation
	# ==================================================
	##################################################
	def add_sample(self, sample: NDArray[np.float32], index: int = -1):
		"""
		Ajoute un échantillon 2D à la pile 3D de la classe.

		L'échantillon est inséré à l'index spécifié. Si l'index est supérieur à la taille actuelle
		de la pile ou négatif, l'échantillon est ajouté à la fin de la pile.

		Si la pile est vide, une pile 3D est créée en ajoutant l'échantillon comme premier élément.
		Sinon, des vérifications de taille sont effectuées pour s'assurer de la compatibilité.

		:param sample: Tableau 2D représentant l'échantillon à ajouter.
		:param index: Position dans la pile où insérer l'échantillon.
		:raises ValueError: Si le tableau fourni n'est pas un tableau 2D.
		:raises ValueError: Si la taille de l'échantillon ne correspond pas à celle des échantillons
							déjà présents dans la pile.
		"""
		# Vérifie que le sample est un tableau 2D
		if sample.ndim != 2:
			raise ValueError(f"Le sample doit être un tableau 2D, mais un tableau de {sample.ndim} dimensions a été fourni.")

		# Si la pile est vide ou nulle, initialise la pile avec le sample
		if getattr(self, 'stack', None) is None or self.stack.size == 0:
			self.stack = sample[np.newaxis, :, :]  # Crée une pile 3D avec sample comme premier élément
			return

		# Vérifie la compatibilité de taille
		if sample.shape != self.stack.shape[1:]:
			raise ValueError(f"La taille de l'échantillon {sample.shape} ne correspond pas à la taille actuelle {self.stack.shape[1:]}.")

		# Ajuste l'index si nécessaire
		if index < 0 or index > self.stack.shape[0]: index = self.stack.shape[0]

		# Ajoute ou remplace l'échantillon dans la pile
		if index < self.stack.shape[0]: self.stack[index] = sample
		else: self.stack = np.concatenate((self.stack, sample[np.newaxis, :, :]), axis=0)

	##################################################
	def get_sample(self, index: int) -> NDArray[np.float32]:
		"""
		Récupère une couche de la pile.

		:param index: Index de la couche à récupérer.
		:return: La couche 2D correspondante.
		"""
		if not (0 <= index < self.stack.shape[0]): raise IndexError("Index hors de la profondeur de la pile.")
		return self.stack[index]

	# ==================================================
	# endregion Sample Manipulation
	# ==================================================

	# ==================================================
	# region IO
	# ==================================================
	def tostring(self) -> str:
		"""
		Retourne une représentation textuelle de la pile 3D (stack).

		:return: Chaîne décrivant la pile, incluant ses dimensions et son contenu si elle existe.
		"""
		if getattr(self, 'stack', None) is None or self.stack.size == 0:
			return "La pile est vide ou non initialisée."
		return f"Pile 3D : {self.stack.shape}\nContenu :\n{self.stack}"

	##################################################
	def __str__(self) -> str: return self.tostring()

	##################################################
	def save(self, filename):
		"""
		Enregistre le masque comme un fichier PNG.
		:param filename: Nom du fichier à enregistrer
		"""
		save_stack_as_tif(self.stack, filename)

	##################################################
	def open(self, filename):
		"""
		Ouvre un fichier PNG et le transforme en masque de booléen
		:param filename: Nom du fichier à ouvrir
		"""
		self.stack = open_tif_as_stack(filename)

	# ==================================================
	# endregion IO
	# ==================================================
