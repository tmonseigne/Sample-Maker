"""
Fichier des classes de modèles pour les piles

Ce module définit les structures de données et les classes nécessaires pour modéliser et gérer
les piles (stacks) avec différents types de modèles et leurs options associées.

Il fournit :

- Une énumération pour identifier les types de modèles disponibles.
- Des classes de configuration pour les options spécifiques à chaque modèle.
- Une classe principale pour encapsuler un modèle de pile et ses options.

**Structure** :

1. **Stack Model Type**

   - `StackModelType` : Énumération pour les types de modèles (actuellement un modèle aléatoire).

2. **Stack Model Options**

   - `NoneOptions` : Classe d'options utilisée lorsque le modèle ne nécessite aucune configuration particulière.

3. **Stack Model**

   - `StackModel` : Classe principale pour représenter un modèle de pile avec son type et ses options.

Fonctionnalités :

- Conversion des modèles et options en chaînes lisibles.
- Méthodes utilitaires pour instancier un modèle avec ses options.

Classes :

- **`StackModelType`** : Enumération des modèles disponibles.
- **`NoneOptions`** : Classe d'options vide pour le modèle par défaut.
- **`StackModel`** : Classe principale pour gérer les modèles et options de piles.
"""

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
	RANDOM = 0

	###################################################
	def tostring(self) -> str:
		"""
		Retourne une chaîne de caractères représentant le modèle correspondant.

		:return: Le nom du motif en français.
		"""
		return {
				StackModelType.RANDOM: "Aléatoire",
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
	model: StackModelType = StackModelType.RANDOM
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
