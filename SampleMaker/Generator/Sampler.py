""" Fichier de la classe du générateur d'échantillons simulés """

from dataclasses import dataclass, field
from typing import List

import numpy as np
from numpy.typing import NDArray
from scipy.stats import multivariate_normal

from SampleMaker.Fluorophore import Fluorophore
from SampleMaker.Generator.Noiser import Noiser
from SampleMaker.Mask import Mask
from SampleMaker.Tools.Utils import print_warning

MAX_INTENSITY = np.iinfo(np.uint16).max  # Pour des entiers sur 16 bits (soit 65535).


##################################################
@dataclass
class Sampler:
	"""
	Classe permettant de générer un échantillon.

	Attributs :
		- **size (int)** : Taille de l'image.
		- **pixel_size (int)** : Taille d'un pixel en nanomètres (par défaut : 160). Utilisé pour calculer la surface de l'image.
		- **density (float)** : Densité de molécules par micromètre carré (par défaut 1.0).
		- **astigmatism_ratio (float)** : Ratio de l'astigmatisme (par défaut 2 indique une déformation de X par rapport à Y de maximum 2).
		- **mask (Mask)** : Masque utilisé pour la dispersion des molécules.
		- **fluorophore (Fluorophore)** : Caractéristiques du fluorophore (intensité, variation).
		- **noise (Noiser)** : Caractéristiques du bruit (base, déviation, SNR souhaité).
	"""
	size: int = 256
	pixel_size: int = 160
	density: float = 1.0
	astigmatism_ratio: float = 2.0
	mask: Mask = field(default_factory=Mask)
	fluorophore: Fluorophore = field(default_factory=Fluorophore)
	noiser: Noiser = field(default_factory=Noiser)

	area: float = field(init=False, default=0.0)
	max_molecules: int = field(init=False, default=0)
	n_molecules: List[int] = field(init=False, default_factory=list)
	last_localisations: NDArray[np.float32] = field(init=False, default_factory=lambda: np.empty((0, 3), dtype=np.float32))

	# ==================================================
	# region Initialization / Setter
	# ==================================================
	##################################################
	def __post_init__(self):
		"""
		Méthode appelée automatiquement après l'initialisation du dataclass.
		Initialise l'aire et le nombre de molécules max.
		"""
		self._set_area()
		self._set_max_molecule_number()

	##################################################
	def _set_area(self):
		"""
		Calcul de l'aire de l'image en fonction de sa taille et de la taille des pixels
		On commence par calculer la taille de l'image en micromètres (conversion depuis la taille des pixels en nanomètres) avant de le mettre au carré
		:return: Aire de l'image en micromètre carré
		"""
		self.area = (float(self.size * self.pixel_size) / 1000) ** 2

	##################################################
	def _set_max_molecule_number(self):
		"""
		Calcule le nombre estimé de molécules dans une image carrée en fonction de sa taille, de la taille d'un pixel et de la densité de molécules.
		Cette fonction est utile pour estimer la quantité totale de molécules dans une région d'image en fonction de paramètres physiques.
		:return: Nombre estimé de molécules dans l'image.
		"""
		self.max_molecules = int(self.area * self.density)  # Calculer le nombre de molécules en fonction de la densité

	# ==================================================
	# endregion Initialization / Setter
	# ==================================================

	# ==================================================
	# region Compute localisation
	# ==================================================
	##################################################
	def generate_localisation(self, apply_mask=True) -> NDArray[np.float32]:
		"""
		Génère un tableau de positions 3D aléatoires pour les molécules en fonction de la taille de l'image,
		de la taille d'un pixel et de la densité des molécules. La coordonnée Z sera comprise entre -1 et 1.
		:return: Un tableau numpy de N lignes et 3 colonnes, où chaque ligne représente les coordonnées (x, y, z) d'une molécule.
		"""
		# Générer des positions aléatoires pour chaque molécule
		# x et y sont des positions flottantes aléatoires dans l'espace 2D de l'image (0 à size)
		# z est une position flottante aléatoire entre -1 et 1.
		x = np.random.uniform(0, self.size, self.max_molecules)
		y = np.random.uniform(0, self.size, self.max_molecules)
		z = np.random.uniform(-1, 1, self.max_molecules)
		localisation = np.vstack((x, y, z)).T  # Combiner les coordonnées dans un tableau de forme (n_molecules, 3)

		if apply_mask:
			# Convertir les coordonnées x et y en type entier pour correspondre aux pixels dans le masque,
			# clip permet d'éviter les positions en dehors du masque.
			x_int = np.clip(localisation[:, 0].astype(int), 0, self.size - 1)
			y_int = np.clip(localisation[:, 1].astype(int), 0, self.size - 1)
			valid_indices = self.mask.mask[x_int, y_int]  # Sélectionner les positions des molécules dont le masque est "True" aux indices (x, y)
			localisation = localisation[valid_indices]	  # Ne garder que les molécules qui sont dans le masque
		return localisation

	##################################################
	def generate_grid_localisation(self, shift: int = 10) -> NDArray[np.float32]:
		"""
		Génère un tableau de positions 3D pour les molécules sur une grille en fonction de la taille de l'image et de l'espacement entre les molécules
		la coordonnée Z sera comprise entre -1 et 1 le long de la grille.

		:param shift: Espace en pixel entre 2 molécules (par défaut 10). On peut considérer que chaque molécule est au centre d'un carré de taille shift.
		:return: Un tableau numpy de N lignes et 3 colonnes, où chaque ligne représente les coordonnées (x, y, z) d'une molécule.
		"""

		start = int(shift / 2)								# Position de départ
		coord = np.arange(start, self.size - start, shift)  # On voit le centre des carrés de taille shift present dans notre image.
		n_molecules = len(coord) ** 2						# On a NxN molécules.
		x, y = np.meshgrid(coord, coord)					# Grille de coordonnées X et Y.
		x, y = x.flatten(), y.flatten()						# Aplatir les coordonnées X et Y pour les transformer en une liste de points.
		z = np.linspace(-1, 1, n_molecules)					# Tous les Z possibles sur cette grille.
		return np.vstack((x, y, z)).T						# Combiner les coordonnées dans un tableau de forme (n_molecules, 3).

	# ==================================================
	# endregion Compute Positions
	# ==================================================
	##################################################
	def generate_psf(self, localisation) -> NDArray[np.float32]:
		"""
		Calcule une image 2D avec la fonction de réponse impulsionnelle (PSF) de chaque molécule basée sur les coordonnées et un astigmatisme défini par z.

		:param localisation: Tableau numpy de positions des molécules de forme (N, 3), où chaque ligne est (x, y, z).
		:return: Image 2D de taille (size, size) avec les PSF ajoutées pour chaque molécule.

		.. todo:: Régler la taille des psf plus précisément avec La longueur d'onde d'émission du fluorophore.
		"""

		image = np.zeros((self.size, self.size), dtype=np.float32)
		if self.astigmatism_ratio <= 0:  # Si à un ratio négatif ce n'est pas logique
			print_warning("Le ratio d'astigmatisme doit être strictement positif, l'image sera noire.")
			return image

		# Déterminer les bornes pour le ratio d'aspect (si l'astigmatisme est inférieur à 1, on inverse l'étirement horizontal et vertical)
		min_ratio = min(self.astigmatism_ratio, 1 / self.astigmatism_ratio)
		max_ratio = max(self.astigmatism_ratio, 1 / self.astigmatism_ratio)

		for x, y, z in localisation:
			# Création d'une grille pour la gaussienne 2D autour de (x, y)
			x_coords = np.arange(self.size)
			y_coords = np.arange(self.size)
			x_mesh, y_mesh = np.meshgrid(x_coords, y_coords)
			pos = np.dstack((x_mesh, y_mesh))

			# Calculer le ratio linéairement en fonction de z, mais borné aux limites logiques en cas de valeurs aberrantes
			ratio = np.clip(1 + z * (self.astigmatism_ratio - 1), min_ratio, max_ratio)

			rv = multivariate_normal(mean=[x, y], cov=[[ratio, 0], [0, 1 / ratio]])  # Définir la gaussienne avec l'astigmatisme selon le ratio
			psf = self.fluorophore.get_intensity(True) * rv.pdf(pos)				 # Générer une intensité et appliquer la gaussienne
			image += psf															 # Ajouter la gaussienne à l'image

		return np.clip(image, 0, MAX_INTENSITY)										 # Clipper les valeurs pour éviter les débordements

	##################################################
	def generate_grid(self, shift: int = 10) -> NDArray[np.float32]:
		"""
		Calcule une répartition des molécules sur une grille.
		Positionne les molécules sur une image 2D et calcule leur psf.
		Simule un bruit optique afin d'avoir une image avec un SNR prédéfini.

		:param shift: Espace en pixel entre 2 molécules (par défaut 10). On peut considérer que chaque molécule est au centre d'un carré de taille shift.
		:return: Image 2D de taille (size, size) avec les molécules affichées.
		"""
		self.last_localisations = self.generate_grid_localisation(shift)
		self.n_molecules.append(self.last_localisations.shape[0])
		return self.noiser.apply(self.generate_psf(self.last_localisations))

	##################################################
	def generate_sample(self) -> NDArray[np.float32]:
		"""
		Calcule une répartition des molécules sur une image carrée en fonction des paramètres du sampler et applique le masque.
		Positionne les molécules sur une image 2D et calcule leur psf.
		Simule un bruit optique afin d'avoir une image avec un SNR prédéfini.

		:return: Image 2D de taille (size, size) avec les molécules affichées.
		"""
		self.last_localisations = self.generate_localisation()
		self.n_molecules.append(self.last_localisations.shape[0])
		return self.noiser.apply(self.generate_psf(self.last_localisations))

	# ==================================================
	# region Compute Image
	# ==================================================
	##################################################

	# ==================================================
	# endregion Compute Image
	# ==================================================

	# ==================================================
	# region IO
	# ==================================================
	##################################################
	def tostring(self) -> str:
		"""
		Retourne une chaîne de caractères correspondant aux caractéristiques du bruiter.

		:return: Une description textuelle des attributs du fluorophore.
		"""
		return (
				f"size: {self.size}, Pixel Size: {self.pixel_size} nm, Molecule Density : {self.density}\n"
				f"Area: {self.area}, Maximum molecule number: {self.max_molecules}\n"
				f"Mask: {self.mask}\n"
				f"Fluorophore: {self.fluorophore}\n"
				f"Noise: {self.noiser}\n"
				f"Generation number : {len(self.n_molecules)}"
		)

	##################################################
	def __str__(self) -> str: return self.tostring()

# ==================================================
# endregion IO
# ==================================================
