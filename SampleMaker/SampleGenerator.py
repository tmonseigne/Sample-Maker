""" Fonctions de génération d'images simulées """

from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.stats import multivariate_normal

from .Mask import Mask
from .Utils import print_warning

MAX_INTENSITY = np.iinfo(np.uint16).max  # Pour des entiers sur 16 bits (soit 65535).


##################################################
def generate_sample(size: int = 256, pixel_size: int = 160, density: float = 1.0,
					mask: Mask = Mask(),
					intensity: float = 100, variation: float = 10, astigmatism_ratio: float = 2.0,
					snr: float = 10.0, base_background: float = 500, base_noise_std: float = 12) -> NDArray[np.float32]:
	"""
	Calcule une répartition des molécules sur une image carrée en fonction de sa taille, de la taille d'un pixel et de la densité de molécules.
	Un masque est appliqué selon un pattern (prédéfini ou chargé à partir d'une image).
	Les molécules sont positionnées sur une image 2D.
	Une simulation de bruit optique est ajoutée afin d'avoir une image avec un SNR prédéfini.

	:param size: Taille de l'image en pixels (par défaut : 256). Cela correspond à la dimension d'un côté de l'image carrée.
	:param pixel_size: Taille d'un pixel en nanomètres (par défaut : 160). Utilisé pour calculer la surface de l'image.
	:param mask: MAsque à appliquer (par défaut un masque blanc).
	:param density: Densité de molécules par micromètre carré (par défaut 1.0).
	:param intensity: Intensité de base du fluorophore (par défaut 100).
	:param variation: Variation d'intensité aléatoire appliquée à l'intensité du fluorophore (par défaut 10).
	:param astigmatism_ratio: Ratio de l'astigmatisme (par défaut 2 indique une déformation de X par rapport à Y de maximum 2).
	:param snr: Le rapport signal sur bruit désiré (par défaut 10 un excellent SNR).
	:param base_background: Intensité de fond de base du microscope, typiquement autour de 500.
	:param base_noise_std: Écart-type du bruit gaussien de fond.
	:return: Image 2D de taille (size, size) avec les molécules affichées.
	"""

	localisation = compute_molecule_localisation(size, pixel_size, density)
	localisation = apply_mask(localisation, mask)
	sample = compute_psf(size, localisation, intensity, variation, astigmatism_ratio)
	sample = add_snr(sample, snr, base_background, base_noise_std)
	return sample

##################################################
def compute_area(size: int = 256, pixel_size: int = 160):
	"""
	Calcul de l'aire de l'image en fonction de sa taille et de la taille des pixels

	:param size: Taille de l'image en pixels (par défaut : 256). Cela correspond à la dimension d'un côté de l'image carrée.
	:param pixel_size: Taille d'un pixel en nanomètres (par défaut : 160). Utilisé pour calculer la surface de l'image.
	:return: Aire de l'image en micromètre carré
	"""
	length = float(size * pixel_size) / 1000  # Calculer la taille de l'image en micromètres (conversion depuis la taille des pixels en nanomètres
	area = length ** 2						  # Calculer l'aire de l'image en micromètres carrés
	return area

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

	area = compute_area(size, pixel_size)  # Calculer l'aire de l'image en micromètre carré
	molecule_number = int(area * density)  # Calculer le nombre de molécules en fonction de la densité
	return molecule_number


##################################################
def compute_molecule_localisation(size: int = 256, pixel_size: int = 160, density: float = 1.0) -> NDArray[np.float32]:
	"""
	Génère un tableau de positions 3D aléatoires pour les molécules en fonction de la taille de l'image,
	de la taille d'un pixel et de la densité des molécules. La coordonnée Z sera comprise entre -1 et 1.

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
def compute_molecule_grid(size: int = 256, shift: int = 10) -> NDArray[np.float32]:
	"""
	Génère un tableau de positions 3D pour les molécules sur une grille en fonction de la taille de l'image et de l'espacement entre les molécules
	la coordonnée Z sera comprise entre -1 et 1 le long de la grille.

	:param size: Taille de l'image en pixels (par défaut 256), qui correspond à la dimension d'un côté de l'image carrée.
	:param shift: Espace en pixel entre 2 molécules (par défaut 10). On peut considérer que chaque molécule est au centre d'un carré de taille shift.
	:return: Un tableau numpy de N lignes et 3 colonnes, où chaque ligne représente les coordonnées (x, y, z) d'une molécule.
	"""

	start = int(shift / 2)  					   # Position de départ
	coord = np.arange(start, size - start, shift)  # On voit le centre des carrés de taille shift present dans notre image.
	n_molecules = len(coord) ** 2				   # On a NxN molécules.
	x, y = np.meshgrid(coord, coord)			   # Grille de coordonnées X et Y.
	x = x.flatten()								   # Aplatir les coordonnées X pour les transformer en une liste de points.
	y = y.flatten()								   # Aplatir les coordonnées Y pour les transformer en une liste de points.
	z = np.linspace(-1, 1, n_molecules)			   # Tous les Z possibles sur cette grille.
	molecule_grid = np.vstack((x, y, z)).T		   # Combiner les coordonnées dans un tableau de forme (n_molecules, 3).
	return molecule_grid


##################################################
def apply_mask(localisation: NDArray[np.float32], mask: Mask) -> NDArray[np.float32]:
	"""
	Filtre les positions des molécules en fonction d'un masque booléen 2D, ne conservant que celles dont les coordonnées
	(x arrondi, y arrondi) correspondent à des positions "True" dans le masque.

	:param localisation: Tableau numpy de positions des molécules de forme (N, 3), où chaque ligne contient les coordonnées (x, y, z).
		Les coordonnées x et y sont en flottants et doivent être dans les limites de `mask`.
	:param mask: Tableau numpy 2D de type booléen indiquant les zones de validité (True) pour les molécules.
		La forme de `mask` doit être (size, size), où `size` corresponds à la taille de l'image.
	:return: Tableau numpy filtré de positions de molécules (x, y, z) où seules les molécules dans les zones "True" du masque sont conservées.
	"""

	# Convertir les coordonnées x et y en type entier pour correspondre aux pixels dans le masque, clip permet d'éviter les positions en dehors du masque.
	x_int = np.clip(localisation[:, 0].astype(int), 0, mask.mask.shape[0] - 1)
	y_int = np.clip(localisation[:, 1].astype(int), 0, mask.mask.shape[1] - 1)

	# Sélectionner les positions des molécules dont le masque est "True" aux indices (x, y)
	valid_indices = mask[x_int, y_int]
	filtered_localisation = localisation[valid_indices]

	return filtered_localisation


##################################################
def compute_psf(size: int, localisation: NDArray[np.float32],
				intensity: float = 100, variation: float = 10, astigmatism_ratio: float = 2.0) -> NDArray[np.float32]:
	"""
	Calcule une image 2D avec la fonction de réponse impulsionnelle (PSF) de chaque molécule basée sur les coordonnées et un astigmatisme défini par z.

	:param size: Taille de l'image en pixels (size x size).
	:param localisation: Tableau numpy de positions des molécules de forme (N, 3), où chaque ligne est (x, y, z).
	:param intensity: Intensité de base pour chaque PSF (i.e. : intensité du fluorophore) (par défaut 100).
	:param variation: Variation d'intensité aléatoire appliquée à l'intensité (par défaut 10).
	:param astigmatism_ratio: Ratio de l'astigmatisme (par défaut 2 indique une déformation de X par rapport à Y de maximum 2).
	:return: Image 2D de taille (size, size) avec les PSF ajoutées pour chaque molécule.

	.. todo:: Régler la taille des psf plus précisément avec une option psf_size. Le ratio de la matrice de covariance va influer la taille de la psf.
		Il faudra faire des tests et voir comment régler précisément la taille des psf pour se rapprocher de données réelles.
	"""

	image = np.zeros((size, size), dtype=np.float32)
	if astigmatism_ratio <= 0:  # Si à un ratio négatif ce n'est pas logique
		print_warning("Le ratio d'astigmatisme doit être strictement positif, l'image sera noire.")
		return image

	# Déterminer les bornes pour le ratio d'aspect (si l'astigmatisme est inférieur à 1, on inverse l'étirement horizontal et vertical)
	min_ratio = min(astigmatism_ratio, 1 / astigmatism_ratio)
	max_ratio = max(astigmatism_ratio, 1 / astigmatism_ratio)

	for x, y, z in localisation:
		# Calculer le ratio linéairement en fonction de z, mais borné aux limites logiques en cas de valeurs aberrantes
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

def create_noise(size: int = 256, base_background: float = 500, base_noise_std: float = 12) -> NDArray[np.float32]:
	"""
	Créé du bruit gaussien et poissonien.

	:param size: Taille de l'image.
	:param base_background: Intensité de fond de base du microscope, typiquement autour de 500.
	:param base_noise_std: Écart-type du bruit gaussien de fond.
	:return: Bruit à ajouter à une image.
	"""

	noisy = np.random.normal(loc=base_background, scale=base_noise_std, size=(size, size))
	noisy = np.nan_to_num(np.maximum(noisy, 0), nan=0)  # Met à zéro toutes les valeurs négatives et remplace NaNs par 0 pour éviter les crash.
	noisy = np.random.poisson(noisy).astype(float)		# Ajouter le bruit poissonien (modèle pour le bruit photonique) au signal
	return noisy


##################################################
def add_snr(image: NDArray[np.float32], snr: float = 10.0, base_background: float = 500, base_noise_std: float = 12) -> NDArray[np.float32]:
	"""
	Ajoute du bruit gaussien et poissonien à une image pour atteindre un SNR donné.

	:param image: L'image d'entrée (en valeurs de pixels).
	:param snr: Le rapport signal sur bruit désiré (par défaut 10).
	:param base_background: Intensité de fond de base du microscope, typiquement autour de 500.
	:param base_noise_std: Écart-type du bruit gaussien de fond.
	:return: L'image bruitée avec un SNR approximatif.
	"""

	# Crée une image de fond (background) avec un bruit gaussien de base et un bruit poissonien
	background_noise = create_noise(image.shape[0], base_background, base_noise_std)
	noisy = image + background_noise							    # Ajout du bruit de fond au signal

	# Calcul du bruit requis pour obtenir le SNR
	signal_mean = np.mean(image[image > np.finfo(np.float32).eps])  # Moyenne des pixels non nuls pour éviter la majorité noire
	signal_std = np.std(image[image > np.finfo(np.float32).eps])    # Écart-type des pixels non nuls pour éviter la majorité noire

	if np.fabs(signal_mean) <= np.finfo(np.float32).eps or np.isnan(signal_mean):
		print_warning("Attention : le signal moyen est nul, impossible d'ajouter du SNR. Un fond bruité est généré")
	elif np.fabs(signal_std) <= np.finfo(np.float32).eps or np.isnan(signal_std):
		print_warning("Attention : le signal est constant, impossible d'ajouter du SNR. Un fond bruité est généré")
	else:
		noise_std = signal_mean / snr							   # Calculer l'écart-type du bruit nécessaire pour le SNR
		print(noise_std)
		signal_noise = create_noise(image.shape[0], 0, noise_std)  # Calcul du bruit du signal (en fonction du SNR)
		noisy += signal_noise			   						   # Ajout du bruit du signal

	noisy = np.clip(noisy, 0, MAX_INTENSITY)				   # Clipper les valeurs pour éviter les débordements
	return noisy
