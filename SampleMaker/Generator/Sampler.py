"""
Fichier contenant la classe du générateur d'échantillons simulés.

La classe `Sampler` permet de simuler la distribution de molécules dans une image 2D, en prenant en compte des paramètres physiques comme la taille de l'image,
la taille des pixels, l'ouverture numérique (NA), la densité des molécules, ainsi que l'astigmatisme.
Elle utilise un fluorophore pour définir les propriétés optiques des molécules et applique des masques pour simuler des motifs de dispersion.

Les principales fonctionnalités de la classe incluent :
- La génération aléatoire ou en grille des positions des molécules dans l'image.
- Le calcul des fonctions de réponse impulsionnelle (PSF) de chaque molécule.
- L'ajout de bruit optique simulé pour obtenir une image avec un rapport signal/bruit (SNR) prédéfini.
"""

from dataclasses import dataclass, field
from typing import List

import numpy as np
from numpy.typing import NDArray
from scipy.stats import multivariate_normal

from SampleMaker.Fluorophore import Fluorophore
from SampleMaker.Generator.Noiser import Noiser
from SampleMaker.Mask import Mask
from SampleMaker.Pattern import PatternType
from SampleMaker.Tools.Decorators import reset_on_change
from SampleMaker.Tools.Utils import print_warning

MAX_INTENSITY = np.iinfo(np.uint16).max  # Pour des entiers sur 16 bits (soit 65535).
FWHM_SIGMA_RATIO = 2.355  # Valeur pour passer du FWHM à un sigma pour la PSF 2*sqrt(2*ln(2)) = 2.35482004503...


##################################################
@dataclass
@reset_on_change("size")
@reset_on_change("pixel_size")
@reset_on_change("na")
@reset_on_change("density")
@reset_on_change("astigmatism_ratio")
@reset_on_change("fluorophore")
class Sampler:
	"""
	Classe permettant de générer un échantillon.

	Attributs :
		- **size (int)** : Taille de l'image.
		- **pixel_size (int)** : Taille d'un pixel en nanomètres (par défaut : 160).
		- **na (float)** : Ouverture numérique (par défaut 1.4).
		- **density (float)** : Densité de molécules par micromètre carré (par défaut 0.25).
		- **astigmatism_ratio (float)** : Ratio de l'astigmatisme (par défaut 2 indique une déformation de X par rapport à Y de maximum 2).
		- **fluorophore (Fluorophore)** : Caractéristiques du fluorophore (intensité, variation).
		- **mask (Mask)** : Masque utilisé pour la dispersion des molécules.
		- **noise (Noiser)** : Caractéristiques du bruit (base, déviation, SNR souhaité).
		- **n_molecules (List[int])** : Nombre de molécules sur chaque image généré par le sampler.
		- **last_localisations (np.array[float])** : Dernières positions des molécules.
	"""
	_size: int = 256
	_pixel_size: int = 160
	_na: float = 1.4
	_density: float = 0.25
	_astigmatism_ratio: float = 2.0
	_fluorophore: Fluorophore = field(default_factory=Fluorophore)
	mask: Mask = field(default_factory=Mask)
	noiser: Noiser = field(default_factory=Noiser)

	# Attributs d'état du générateur
	n_molecules: List[int] = field(init=False, default_factory=list)
	last_localisations: NDArray[np.float32] = field(init=False, default_factory=lambda: np.empty((0, 3), dtype=np.float32))

	# Attributs de pré-calcul interne
	_area: float = field(init=False, default=0.0)
	_max_molecules: int = field(init=False, default=0)
	_sigma_base: float = field(init=False, default=1)
	_astigmatism: [float, float] = field(init=False, default_factory=lambda: [1.0, 1.0])

	# ==================================================
	# region Initialization / Setter
	# ==================================================
	##################################################
	def __init__(self, size: int = 256, pixel_size: int = 160, na: float = 1.4, density: float = 0.25, astigmatism_ratio: float = 2.0,
				 fluorophore: Fluorophore = Fluorophore(), mask: Mask = Mask(), noiser: Noiser = Noiser()):
		"""
		Constructeur personnalisé avec possibilité d'initialiser certains attributs manuellement.

		:param size: Taille de l'image (par défaut : 256).
		:param pixel_size: Taille d'un pixel en nanomètres (par défaut : 160).
		:param na: Ouverture numérique (par défaut 1.4).
		:param density: Densité de molécules par micromètre carré (par défaut 0.25).
		:param astigmatism_ratio: Ratio de l'astigmatisme (par défaut 2 indique une déformation de X par rapport à Y de maximum 2).
		:param fluorophore: Caractéristiques du fluorophore (longueur d'onde, intensité...).
		:param mask: Masque utilisé pour la dispersion des molécules.
		:param noiser: Caractéristiques du bruit (base, déviation, SNR souhaité).
		"""
		self._size = size
		self._pixel_size = pixel_size
		self._na = na
		self._density = density
		self._astigmatism_ratio = astigmatism_ratio
		self._fluorophore = fluorophore
		self.mask = mask
		self.noiser = noiser
		# Initialisation des champs "init=False"
		self.n_molecules = []
		self.last_localisations = np.empty((0, 3), dtype=np.float32)
		self._area = 0.0
		self._max_molecules = 0
		self._sigma_base = 1.0
		self._astigmatism = [1.0, 1.0]
		self.reset()

	##################################################
	def _set_area(self):
		"""
		Calcul de l'aire de l'image en fonction de sa taille et de la taille des pixels
		On commence par calculer la taille de l'image en micromètres (conversion depuis la taille des pixels en nanomètres) avant de le mettre au carré
		"""
		self._area = (float(self._size * self._pixel_size) / 1000) ** 2

	##################################################
	def _set_max_molecule_number(self):
		"""
		Calcule le nombre estimé de molécules dans une image carrée en fonction de sa taille, de la taille d'un pixel et de la densité de molécules.
		Cette fonction est utile pour estimer la quantité totale de molécules dans une région d'image en fonction de paramètres physiques.
		"""
		self._max_molecules = int(self._area * self._density)  # Calculer le nombre de molécules en fonction de la densité

	##################################################
	def _set_psf_parameters(self):
		"""
		Calcul des différents paramètres nécessaire au calcul des PSF.
		"""
		fwhm = (0.61 * self._fluorophore.wavelength) / self._na	 # Calcul de la largeur à mi-hauteur (FWHM) pour une PSF circulaire
		self._sigma_base = fwhm / FWHM_SIGMA_RATIO  			 # Convertir la largeur à mi-hauteur en variance (sigma)
		self._sigma_base /= self._pixel_size					 # Convertir sigma_base en pixels (par rapport à la taille du pixel)

		# Déterminer les bornes pour le ratio d'aspect (si l'astigmatisme est inférieur à 1, on inverse l'étirement horizontal et vertical)
		self._astigmatism[0] = min(self._astigmatism_ratio, 1.0 / self._astigmatism_ratio)
		self._astigmatism[1] = max(self._astigmatism_ratio, 1.0 / self._astigmatism_ratio)

	##################################################
	def reset(self):
		"""
		Réinitialise la dernière position et la liste de molécules.
		(Utile dans le cas de plusieurs utilisations du même sampler avec des paramètres différents.)
		"""
		self.n_molecules.clear()
		self.last_localisations = np.empty((0, 3), dtype=np.float32)
		self._set_area()
		self._set_max_molecule_number()
		self._set_psf_parameters()

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
		x = np.random.uniform(0, self._size, self._max_molecules)
		y = np.random.uniform(0, self._size, self._max_molecules)
		z = np.random.uniform(-1, 1, self._max_molecules)
		localisation = np.vstack((x, y, z)).T  # Combiner les coordonnées dans un tableau de forme (n_molecules, 3)

		if apply_mask and self.mask.pattern.pattern != PatternType.NONE:
			# Convertir les coordonnées x et y en type entier pour correspondre aux pixels dans le masque,
			# clip permet d'éviter les positions en dehors du masque.
			x_int = np.clip(localisation[:, 0].astype(int), 0, self._size - 1)
			y_int = np.clip(localisation[:, 1].astype(int), 0, self._size - 1)
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

		start = int(shift / 2)								 # Position de départ
		coord = np.arange(start, self._size - start, shift)  # On voit le centre des carrés de taille shift present dans notre image.
		n_molecules = len(coord) ** 2						 # On a NxN molécules.
		x, y = np.meshgrid(coord, coord)					 # Grille de coordonnées X et Y.
		x, y = x.flatten(), y.flatten()						 # Aplatir les coordonnées X et Y pour les transformer en une liste de points.
		z = np.linspace(-1, 1, n_molecules)					 # Tous les Z possibles sur cette grille.
		return np.vstack((x, y, z)).T						 # Combiner les coordonnées dans un tableau de forme (n_molecules, 3).

	# ==================================================
	# endregion Compute localisation
	# ==================================================

	# ==================================================
	# region Generate Image
	# ==================================================
	##################################################
	def generate_psf(self, localisation) -> NDArray[np.float32]:
		"""
		Calcule une image 2D avec la fonction de réponse impulsionnelle (PSF) de chaque molécule basée sur les coordonnées et un astigmatisme défini par z.

		:param localisation: Tableau numpy de positions des molécules de forme (N, 3), où chaque ligne est (x, y, z).
		:return: Image 2D de taille (size, size) avec les PSF ajoutées pour chaque molécule.
		"""

		image = np.zeros((self._size, self._size), dtype=np.float32)
		if self._astigmatism_ratio <= 0:  # Si à un ratio négatif ce n'est pas logique
			print_warning("Le ratio d'astigmatisme doit être strictement positif, l'image sera noire.")
			return image

		for x, y, z in localisation:
			# Calculer le ratio linéairement en fonction de z, mais borné aux limites logiques en cas de valeurs aberrantes
			ratio = np.clip(1 + z * (self._astigmatism_ratio - 1), self._astigmatism[0], self._astigmatism[1])
			sigma_x = self._sigma_base * ratio
			sigma_y = self._sigma_base / ratio

			# Création d'une grille pour la gaussienne 2D autour de (x, y)
			x_coords = np.arange(self._size)
			y_coords = np.arange(self._size)
			x_mesh, y_mesh = np.meshgrid(x_coords, y_coords)
			pos = np.dstack((x_mesh, y_mesh))

			rv = multivariate_normal(mean=[x, y], cov=[[sigma_x ** 2, 0], [0, sigma_y ** 2]])  # Définir la gaussienne avec l'astigmatisme selon le ratio
			psf = self._fluorophore.get_intensity(True) * rv.pdf(pos)						   # Générer une intensité et appliquer la gaussienne
			image += psf																	   # Ajouter la PSF à l'image

		return np.clip(image, 0, MAX_INTENSITY)  # Clipper les valeurs pour éviter les débordements

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
	# endregion Generate Image
	# ==================================================

	# ==================================================
	# region IO
	# ==================================================
	##################################################
	def tostring(self) -> str:
		"""
		Retourne une chaîne de caractères correspondant aux caractéristiques du générateur.

		:return: Une description textuelle des attributs du générateur.
		"""
		return (
				f"size: {self._size}, Pixel Size: {self._pixel_size} nm, Molecule Density : {self._density}\n"
				f"Area: {self._area}, Maximum molecule number: {self._max_molecules}\n"
				f"Mask: {self.mask}\n"
				f"Fluorophore: {self._fluorophore}\n"
				f"Noise: {self.noiser}\n"
				f"Generation number : {len(self.n_molecules)}"
		)

	##################################################
	def __str__(self) -> str: return self.tostring()

# ==================================================
# endregion IO
# ==================================================
