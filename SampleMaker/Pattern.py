""" Fonctions de génération de pattern pour des masques de structure """

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union

# ==================================================
# region Pattern Type
# ==================================================
##################################################
class PatternType(Enum):
	"""
	Enumération représentant les différents motifs disponibles pour la génération de masque.
	Chaque motif est associé à un identifiant unique pour être utilisé par la classe mask.

	- NONE : Aucun masque (ou plutôt un masque entièrement blanc).
	- STRIPES : Bandes verticales (alternance de bandes noires et blanches).
	- SQUARES : Carrés (pas encore implémenté).
	- SUN : Motif en forme de soleil (pas encore implémenté).
	- EXISTING_IMAGE : Charge une image existante pour créer le masque (pas encore implémenté).
	"""
	NONE = 0
	STRIPES = 1
	SQUARES = 2
	SUN = 3
	EXISTING_IMAGE = 4

	def to_string(self) -> str:
		"""
		Retourne une chaîne de caractères représentant le motif correspondant.

		:return: Le nom du motif en français.
		"""
		return {
				PatternType.NONE:           "None",
				PatternType.STRIPES:        "Bandes",
				PatternType.SQUARES:        "Carrés",
				PatternType.SUN:            "Soleil",
				PatternType.EXISTING_IMAGE: "Image existante"
				}[self]

# ==================================================
# endregion Pattern Type
# ==================================================


# ==================================================
# region Pattern Options
# ==================================================
# Classes d'options spécifiques pour chaque type de masque
##################################################
@dataclass
class NoneOptions:
	"""
	Pas d'options pour le motif 'NONE'
	"""
	pass


##################################################
@dataclass
class StripesOptions:
	"""
	Options pour le motif bandes.

	Attributs :
		- **lengths (List[int])** : Liste des longueurs des bandes.
		- **mirror (bool)** : Booléen indiquant si le motif est symétrique (miroir central).
		- **orientation (bool)** : Booléen pour l'orientation des bandes (True pour vertical, False pour horizontal).
	"""
	lengths: List[int] = field(default_factory=lambda: [200, 100, 50, 25, 12, 6])
	mirror: bool = True
	orientation: bool = True


##################################################
@dataclass
class SquaresOptions:
	"""
	Options pour le motif carré.

	Attributs :
		- **size (int)** : Taille des carrées (en pixel).
	"""
	size: int = 32


##################################################
@dataclass
class SunOptions:
	"""
	Options pour le motif soleil.

	Attributs :
		- **ray_count (int)** : Nombre de rayons du soleil.
	"""
	ray_count: int = 16


##################################################
@dataclass
class ExistingImageOptions:
	"""
	Options pour le motif soleil.

	Attributs :
		- **path (str)** : Chemin du fichier.
	"""
	path: str = ""


##################################################
# Classe principale pour les options de masque
@dataclass
class PatternOptions:
	"""
	Class générique pour les options de motif.

	Attributs :
		- **pattern (Pattern)** : Le motif à utiliser.
		- **options (Dict)** : Dictionnaire contenant des options spécifiques au motif.
	"""
	pattern: PatternType
	options: Union[NoneOptions, StripesOptions, SquaresOptions, SunOptions, ExistingImageOptions] = field(default_factory=NoneOptions)

	##################################################
	@classmethod
	def from_pattern(cls, pattern: PatternType, options: Optional[Dict[str, Any]] = None) -> 'PatternOptions':
		"""
		Génère les options spécifiques selon le type de motif.

		:param pattern: Type de motif (Pattern).
		:param options: Dictionnaire des options à appliquer (facultatif).
		:return: Instance de MaskOptions configurée pour le motif donné.
		"""
		if pattern == PatternType.STRIPES: return cls(pattern, StripesOptions(**(options or {})))
		elif pattern == PatternType.SQUARES: return cls(pattern, SquaresOptions(**(options or {})))
		elif pattern == PatternType.SUN: return cls(pattern, SunOptions(**(options or {})))
		elif pattern == PatternType.EXISTING_IMAGE: return cls(pattern, ExistingImageOptions(**(options or {})))
		else: return cls(pattern, NoneOptions())  # MaskPattern.NONE ou autre

	##################################################
	def to_str(self) -> str:
		"""
		Conversiont en chaine de caractère.
		"""
		return (f"PatternOptions:\n"
				f"  Pattern: {self.pattern}\n"
				f"  Options: {self.options}")

	##################################################
	def __str__(self):
		"""
		Surcharge de l'affichage de l'objet pour un résumé détaillé.
		"""
		return self.to_str()

# ==================================================
# endregion Pattern Options
# ==================================================

# ==================================================
# region Pattern
# ==================================================
##################################################
@dataclass
class Pattern:
	"""
	Objet Motif principal contenant le type et les options associées.

	Attributs :
		- **type (PatternType)** : Type de motif.
		- **options (PatternOptions)** : Options du motif.
	"""
	type: PatternType = PatternType.NONE
	options: PatternOptions = field(default_factory=NoneOptions)

# ==================================================
# endregion Pattern
# ==================================================
