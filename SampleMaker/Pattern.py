""" Fichier des classes de motifs pour des masques de structure """

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

	##################################################
	def tostring(self) -> str:
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

	##################################################
	def __str__(self) -> str: return self.tostring()


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


##################################################
@dataclass
class StripesOptions:
	"""
	Options pour le motif de bandes.

	Les bandes sont alternées entre noire et blanche, et leur taille est spécifiée par le dictionnaire `options`.
	Si l'option `Mirrored` est activée, le motif est symétrique (miroir central).
	L'option `Orientation` détermine si les bandes sont verticales (True) ou horizontales (False).

	Attributs :
		- **lengths (List[int])** : Liste des longueurs des bandes.
		- **mirror (bool)** : Booléen indiquant si le motif est symétrique (miroir central).
		- **orientation (bool)** : Booléen pour l'orientation des bandes (True pour vertical, False pour horizontal).
	"""
	lengths: List[int] = field(default_factory=lambda: [200, 100, 50, 25, 12, 6])
	mirror: bool = True
	orientation: bool = True

	##################################################
	def tostring(self) -> str:
		"""
		Retourne une chaîne de caractères correspondant aux options.

		:return: La liste des options.
		"""
		return (f"Lengths: {self.lengths}, "
				f"{'mirrored' if self.mirror else 'not mirrored'}, "
				f"{'vertical' if self.orientation else 'horizontal'}")

	##################################################
	def __str__(self) -> str: return self.tostring()


##################################################
@dataclass
class SquaresOptions:
	"""
	Options pour le motif de carré.

	Un nombre de carrés maximum sera généré en fonction de la taille de ceux-ci.

	Attributs :
		- **size (int)** : Taille des carrées (en pixel).

	.. todo:: Ajouter la possibilité d'avoir une option nombre de carrés. (en cas de double options priorité au nombre de carrés et bords plus grand)
	"""
	size: int = 32

	##################################################
	def tostring(self) -> str:
		"""
		Retourne une chaîne de caractères correspondant aux options.

		:return: La liste des options.
		"""
		return f"Size: {self.size}"

	##################################################
	def __str__(self) -> str: return self.tostring()


##################################################
@dataclass
class SunOptions:
	"""
	Options pour le motif de soleil.

	Le masque aura des segments triangulaires définis par le nombre de rayons indiqué, ceux-ci se croisant au centre de l'image.

	Attributs :
		- **ray_count (int)** : Nombre de rayons du soleil.
	"""
	ray_count: int = 16

	##################################################
	def tostring(self) -> str:
		"""
		Retourne une chaîne de caractères correspondant aux options.

		:return: La liste des options.
		"""
		return f"Ray number: {self.ray_count}"

	##################################################
	def __str__(self) -> str: return self.tostring()


##################################################
@dataclass
class ExistingImageOptions:
	"""
	Options pour le motif Existing Image.

	Charge une image comme un masque.

	Attributs :
		- **path (str)** : Chemin du fichier.
	"""
	path: str = ""

	##################################################
	def tostring(self) -> str:
		"""
		Retourne une chaîne de caractères correspondant aux options.

		:return: La liste des options.
		"""
		return f"Path: {self.path}"

	##################################################
	def __str__(self) -> str: return self.tostring()


# ==================================================
# endregion Pattern Options
# ==================================================


# ==================================================
# region Pattern
# ==================================================
@dataclass
class Pattern:
	"""
	Class principale pour les motifs et leurs options.

	Attributs :
		- **pattern (Pattern)** : Le motif à utiliser.
		- **options (Dict)** : Dictionnaire contenant des options spécifiques au motif.
	"""
	pattern: PatternType = PatternType.NONE
	options: Union[NoneOptions, StripesOptions, SquaresOptions, SunOptions, ExistingImageOptions] = field(default_factory=NoneOptions)

	##################################################
	@classmethod
	def from_pattern(cls, pattern: PatternType, options: Optional[Dict[str, Any]] = None) -> 'Pattern':
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
	def tostring(self) -> str:
		"""
		Conversion en chaine de caractère.
		"""
		return f"Pattern: {self.pattern}, Options: {self.options}"

	##################################################
	def __str__(self) -> str: return self.tostring()

# ==================================================
# endregion Pattern
# ==================================================
