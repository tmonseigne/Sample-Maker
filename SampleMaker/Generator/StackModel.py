""" Fichier des classes de modèles pour les piles """

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional, Union


# ==================================================
# region Stack Model Type
# ==================================================
###################################################
class StackModelType(Enum):
	"""
	Énumération représentant les différents modèles de piles disponibles.
	Chaque modèle est associé à un identifiant unique pour être utilisé dans la fonction `generate`.

	- NONE : Aucun modèle particulier (les échantillons sont indépendants les uns des autres).
	"""
	NONE = 0

	###################################################
	def tostring(self) -> str:
		"""
		Retourne une chaîne de caractères représentant le modèle correspondant.

		:return: Le nom du motif en français.
		"""
		return {
				StackModelType.NONE: "None",
				}[self]


# ==================================================
# endregion Stack Model Type
# ==================================================

# ==================================================
# region Stack Model Options
# ==================================================
# Classes d'options spécifiques pour chaque type de modèle
##################################################
@dataclass
class NoneOptions:
	"""
	Pas d'options pour le motif 'NONE'
	"""

	##################################################
	@staticmethod
	def tostring() -> str:
		"""
		Retourne une chaîne de caractères correspondant aux options.

		:return: La liste des options.
		"""
		return "No Options"

	##################################################
	def __str__(self) -> str: return self.tostring()


# ==================================================
# endregion Stack Model Options
# ==================================================

# ==================================================
# region Stack Model
# ==================================================
@dataclass
class StackModel:
	"""
	Class principale pour les modèles et leurs options.

	Attributs :
		- **model (StackModelType)** : Le modèle à utiliser.
		- **options (Dict)** : Dictionnaire contenant des options spécifiques au modèle.
	"""
	model: StackModelType = StackModelType.NONE
	options: Union[NoneOptions] = field(default_factory=NoneOptions)

	##################################################
	@classmethod
	def from_model(cls, model: StackModelType, options: Optional[Dict[str, Any]] = None) -> 'StackModel':
		"""
		Génère les options spécifiques selon le type de motif.

		:param model: Type de modèle de pile.
		:param options: Dictionnaire des options à appliquer (facultatif).
		:return: Instance de MaskOptions configurée pour le motif donné.
		"""
		return cls(model, NoneOptions())  # StackModelType.NONE ou autre

	##################################################
	def tostring(self) -> str:
		"""
		Conversion en chaine de caractère.
		"""
		return f"Model: {self.model}, Options: {self.options}"

	##################################################
	def __str__(self) -> str: return self.tostring()
# ==================================================
# endregion Stack Model
# ==================================================
