""" Classe de génération de bruit """

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from .Utils import print_warning

MAX_INTENSITY = np.iinfo(np.uint16).max  # Pour des entiers sur 16 bits (soit 65535).


##################################################
@dataclass
class Noiser:
	"""
	Classe permettant de générer un bruit sur une image.

	Attributs :
		- **snr (float)** : Le rapport signal sur bruit désiré (par défaut 10 un excellent SNR).
		- **base_background (float)** : Intensité de fond de base du microscope, typiquement autour de 500.
		- **base_noise_std (float)** : Écart-type du bruit gaussien de fond en pourcent.
	"""
	snr: float = 10
	background: float = 500
	std: float = 10

	##################################################
	@staticmethod
	def create_noise(size: int, loc: float, scale: float) -> NDArray[np.float32]:
		"""
		Créé une image correspondant au bruit gaussien et poissonien pour simuler le bruit optique.

		:param size: Taille de l'image.
		:param loc: Moyenne (centre) de la distribution
		:param scale: Écart-type du bruit gaussien.
		:return: Bruit à ajouter à une image.
		"""
		noise = np.random.normal(loc=loc, scale=scale, size=(size, size))
		noise = np.nan_to_num(np.maximum(noise, 0), nan=0)  # Met à zéro toutes les valeurs négatives et remplace NaNs par 0 pour éviter les crash.
		noise = np.random.poisson(noise).astype(float)		# Ajouter le bruit poissonien (modèle pour le bruit photonique) au signal
		return noise

	##################################################
	def apply(self, image: NDArray[np.float32]):
		"""
		Ajoute du bruit gaussien et poissonien à une image pour atteindre un SNR donné.

		:param image: L'image d'entrée (en valeurs de pixels).
		:return: L'image bruitée avec un SNR approximatif.
		"""

		# Crée une image de fond (background) avec un bruit gaussien de base et un bruit poissonien
		background_noise = self.create_noise(image.shape[0], self.background, self.std)
		noisy = image + background_noise  # Ajout du bruit de fond au signal

		# Calcul du bruit requis pour obtenir le SNR
		signal_mean = np.mean(image[image > np.finfo(np.float32).eps])  # Moyenne des pixels non nuls pour éviter la majorité noire

		if np.fabs(signal_mean) <= np.finfo(np.float32).eps or np.isnan(signal_mean):
			print_warning("Attention : le signal moyen est nul, impossible d'ajouter du SNR. Un fond bruité est généré")
		else:
			noise_std = signal_mean / self.snr								# Calculer l'écart-type du bruit nécessaire pour le SNR
			signal_noise = self.create_noise(image.shape[0], 0, noise_std)  # Calcul du bruit du signal (en fonction du SNR)
			noisy += signal_noise											# Ajout du bruit du signal

		return np.clip(noisy, 0, MAX_INTENSITY)								# Clipper les valeurs pour éviter les débordements

	# ==================================================
	# region IO
	# ==================================================
	##################################################
	def tostring(self) -> str:
		"""
		Retourne une chaîne de caractères correspondant aux caractéristiques du bruiter.

		:return: Une description textuelle des attributs du fluorophore.
		"""
		return f"snr: {self.snr}, background: {self.background}, deviation: {self.std} %"

	##################################################
	def __str__(self) -> str: return self.tostring()

# ==================================================
# endregion IO
# ==================================================
