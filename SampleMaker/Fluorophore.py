""" Fichier de la classe Fluorophore """

import random
from dataclasses import dataclass
from typing import Dict


##################################################
@dataclass
class Fluorophore:
	"""
	Classe contenant différentes informations sur le fluorophore.

	Attributs :
		- **wavelength (int)** : Longueur d'onde d'émission du fluorophore (nécessaire au calcul de la taille de la PSF).
		- **intensity (int)** : Intensité de base du fluorophore.
		- **delta (int)** : Variation maximale d'intensité en pourcentage.
		- **flickering (int)** : Vitesse de scintillement en millisecondes.
	"""
	wavelength: int = 600
	intensity: int = 5000
	delta: int = 10
	flickering: int = 50

	##################################################
	def get_intensity(self, variation: bool = False) -> int:
		"""
		Calcule l'intensité actuelle du fluorophore.

		:param variation: Si `True`, applique une variation aléatoire à l'intensité de base.
		:return: Intensité du fluorophore (avec ou sans variation).
		"""
		if variation:
			# Variation en pourcentage entre -delta et +delta
			variation_percent = random.uniform(-self.delta, self.delta) / 100
			return max(0, int(self.intensity * (1 + variation_percent)))
		return max(0, self.intensity)

	# ==================================================
	# region IO
	# ==================================================
	##################################################
	def tostring(self) -> str:
		"""
		Retourne une chaîne de caractères correspondant aux caractéristiques du fluorophore.

		:return: Une description textuelle des attributs du fluorophore.
		"""
		return (
				f"- Longueur d'onde (wavelength): {self.wavelength} nm\n"
				f"- Intensité de base: {self.intensity}\n"
				f"- Variation maximale (delta): ±{self.delta}%\n"
				f"- Scintillement (flickering): {self.flickering} ms"
		)

	##################################################
	def __str__(self) -> str: return self.tostring()


# ==================================================
# endregion IO
# ==================================================


##################################################
# Dictionnaire contenant les fluorophores prédéfinis
PREDEFINED_FLUOROPHORES: Dict[str, Fluorophore] = {
		"GFP":      Fluorophore(wavelength=509, intensity=4000, delta=5, flickering=30),
		"RFP":      Fluorophore(wavelength=582, intensity=4500, delta=10, flickering=50),
		"CFP":      Fluorophore(wavelength=475, intensity=3500, delta=7, flickering=40),
		"YFP":      Fluorophore(wavelength=527, intensity=3800, delta=6, flickering=35),
		"Alexa488": Fluorophore(wavelength=495, intensity=6000, delta=3, flickering=25),
		}
