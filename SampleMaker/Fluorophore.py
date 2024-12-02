"""
Ce module définit la classe `Fluorophore` et un ensemble de fluorophores prédéfinis.
Un fluorophore est une entité ayant des propriétés optiques spécifiques, telles que sa longueur d'onde d'émission
et son intensité, qui peuvent être utilisées pour des simulations ou des calculs en microscopie et en imagerie.

Structure :

1. **Classe `Fluorophore`**

   - Modélise les caractéristiques d'un fluorophore, comme sa longueur d'onde, son intensité et son comportement
     de scintillement. Elle inclut également une méthode pour calculer l'intensité avec des variations aléatoires.

2. **Fluorophores prédéfinis**

   - Fournit un dictionnaire de fluorophores couramment utilisés, chacun configuré avec des paramètres spécifiques
     (par exemple, GFP, RFP, Alexa488, etc.).

Fonctionnalités :

- Création d'instances de fluorophores personnalisées.
- Calcul de l'intensité avec ou sans variation aléatoire.
- Conversion des propriétés d'un fluorophore en chaîne de caractères lisible.
- Accès rapide à des fluorophores prédéfinis via le dictionnaire `PREDEFINED_FLUOROPHORES`.

"""

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
		- **intensity (float)** : Intensité de base du fluorophore.
		- **delta (float)** : Variation maximale d'intensité en pourcentage.
		- **flickering (int)** : Vitesse de scintillement en millisecondes.
	"""
	wavelength: int = 600
	intensity: float = 5000
	delta: float = 10
	flickering: int = 50

	##################################################
	def get_intensity(self, variation: bool = False) -> float:
		"""
		Calcule l'intensité actuelle du fluorophore.

		:param variation: Si `True`, applique une variation aléatoire à l'intensité de base.
		:return: Intensité du fluorophore (avec ou sans variation).
		"""
		if variation:
			# Variation en pourcentage entre -delta et +delta
			variation_percent = random.uniform(-self.delta, self.delta) / 100
			return max(0.0, (self.intensity * (1 + variation_percent)))
		return max(0.0, self.intensity)

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
