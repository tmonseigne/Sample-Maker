""" Fonctions de génération d'images Simulées """

from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.stats import multivariate_normal

from PatternGenerator import generate_mask, Pattern
from Utils import print_warning

MAX_INTENSITY = 65535  # Pour des entiers sur 16 bits


##################################################
def generate_sample(size: int = 256, pixel_size: int = 160, density: float = 1.0,
					pattern: Pattern = Pattern.NONE, pattern_options: Any = None,
					intensity: float = 100, variation: float = 10, astigmatism_ratio: float = 2.0,
					snr: float = 10.0) -> NDArray[float]:
	"""
	Calcule une répartition des molécules sur une image carrée en fonction de sa taille, de la taille d'un pixel et de la densité de molécules.
	Un masque est appliqué selon un pattern (prédéfini ou chargé à partir d'une image).
	Les molécules sont positionnées sur une image 2D.
	UNe simulation de bruit optique est ajouté afin d'avoir une image avec un SNR prédéfinie.

	:param size: Taille de l'image en pixels (par défaut : 256). Cela correspond à la dimension d'un côté de l'image carrée.
	:param pixel_size: Taille d'un pixel en nanomètres (par défaut : 160). Utilisé pour calculer la surface de l'image.
	:param density: Densité de molécules par micromètre carré (par défaut 1.0).
	:param pattern: Le motif à utiliser pour générer le masque (Pattern.STRIPES, Pattern.SQUARES, etc.).
	:param pattern_options: Dictionnaire contenant des options spécifiques au motif (longueur des bandes, effet miroir, etc.).
	:param intensity: Intensité de base du fluorophore (par défaut 100).
	:param variation: Variation d'intensité aléatoire appliquée à l'intensité du fluorophore (par défaut 10).
	:param astigmatism_ratio: Ratio de l'astigmatisme (par défaut 2 indique une déformation de X par rapport à Y de maximum 2).
	:param snr: Le rapport signal sur bruit désiré (par défaut 10 un excellent SNR).
	:return: Image 2D de taille (size, size) avec les molécules affichées.
	"""

	localisation = compute_molecule_localisation(size, pixel_size, density)
	mask = generate_mask(pattern, size, pattern_options)
	localisation = apply_mask(localisation, mask)
	sample = compute_psf(size, localisation, intensity, variation, astigmatism_ratio)
	sample = add_snr(sample, snr)
	return sample


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
	im_area = im_size ** 2					   # Calculer l'aire de l'image en micromètres carrés
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
	"""

	# Convertir les coordonnées x et y en entiers pour correspondre aux pixels dans le masque, clip permet d'éviter les positions en dehors du masque.
	x_int = np.clip(localisation[:, 0].astype(int), 0, mask.shape[0] - 1)
	y_int = np.clip(localisation[:, 1].astype(int), 0, mask.shape[1] - 1)

	# Sélectionner les positions des molécules dont le masque est "True" aux indices (x, y)
	valid_indices = mask[x_int, y_int]
	filtered_localisation = localisation[valid_indices]

	return filtered_localisation


##################################################
def compute_psf(size: int, localisation: NDArray[float], intensity: float = 100, variation: float = 10, astigmatism_ratio: float = 2.0) -> NDArray[float]:
	"""
	Calcule une image 2D avec la fonction de réponse impulsionnelle (PSF) de chaque molécule basée sur les coordonnées et un astigmatisme défini par z.

	:param size: Taille de l'image en pixels (size x size).
	:param localisation: Tableau numpy de positions des molécules de forme (N, 3), où chaque ligne est (x, y, z).
	:param intensity: Intensité de base pour chaque PSF (ie : intensité du fluorophore) (par défaut 100).
	:param variation: Variation d'intensité aléatoire appliquée à l'intensité (par défaut 10).
	:param astigmatism_ratio: Ratio de l'astigmatisme (par défaut 2 indique une déformation de X par rapport à Y de maximum 2).
	:return: Image 2D de taille (size, size) avec les PSF ajoutées pour chaque molécule.
	"""

	image = np.zeros((size, size), dtype=np.float32)
	if astigmatism_ratio <= 0:  # Si à un ratio négatif ce n'est pas logique
		print_warning("Le ratio d'astygmatisme doit être strictement positif, l'image sera noire.")
		return image

	# Déterminer les bornes pour le ratio d'aspect (si l'astigmatisme est inférieure à 1, on inverse l'étirement horizontal et vertical)
	min_ratio = min(astigmatism_ratio, 1 / astigmatism_ratio)
	max_ratio = max(astigmatism_ratio, 1 / astigmatism_ratio)

	for x, y, z in localisation:
		# Calculer le ratio linéairement en fonction de z, mais borné aux limites logiques en cas de valeurs abhérantes
		ratio = np.clip(1 + z * (astigmatism_ratio - 1), min_ratio, max_ratio)

		# Générer une intensité aléatoire autour de l'intensité de base
		i = intensity + np.random.normal(-variation, variation)

		# Calculer la gaussienne 2D autour de (x, y) avec l'astigmatisme
		x_coords = np.arange(size)
		y_coords = np.arange(size)
		x_mesh, y_mesh = np.meshgrid(x_coords, y_coords)
		pos = np.dstack((x_mesh, y_mesh))

		# Définir la gaussienne avec l'astigmatisme selon sigma_x et sigma_y
		rv = multivariate_normal(mean=[x, y], cov=[[ratio, 0], [0, 1 / ratio]])
		psf = i * rv.pdf(pos)

		# Ajouter la gaussienne à l'image résultante
		image += psf

	# Remplacer toutes les valeurs inférieures à 0 par 0.
	image = np.clip(image, 0, MAX_INTENSITY)

	return image


##################################################
def add_snr(image: NDArray[float], snr: float = 10.0):
	"""
	Ajoute du bruit gaussien et poissonien à une image pour atteindre un SNR donné.

	:param image: L'image d'entrée (en valeurs de pixels).
	:param snr: Le rapport signal sur bruit désiré (par défaut 10).
	:return: L'image bruitée avec un SNR approximatif.
	"""

	signal_mean = np.mean(image)												 # Calculer l'intensité moyenne du signal
	noise_std = signal_mean / snr												 # Calculer l'écart-type du bruit nécessaire pour le SNR
	gaussian_noise = np.random.normal(loc=0, scale=noise_std, size=image.shape)  # Ajouter du bruit gaussien avec l'écart-type calculé
	poisson_noise = np.random.poisson(image) 									 # Ajouter du bruit poissonien basé sur l'image
	noisy_image = image + gaussian_noise + poisson_noise						 # Somme du bruit gaussien et poissonien
	noisy_image = np.clip(noisy_image, 0, MAX_INTENSITY)						 # Clipper les valeurs pour éviter les débordements
	return noisy_image
