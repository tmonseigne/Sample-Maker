"""
Ce fichier définit la classe `Settings`, utilisée pour gérer et enregistrer les paramètres nécessaires
à la configuration du générateur d'images et des données dans le projet SampleMaker.

**Fonctionnalités principales** :

- Permet le parsing et l'enregistrement des paramètres liés à l'interface utilisateur.
- Fournit une gestion structurée des dimensions, des propriétés optiques, des fluorophores, des bruits et des modèles d'empilement.
- Inclut des méthodes pour générer des objets associés, tels que des échantillonneurs, des masques, des bruiteurs et des fluorophores.

**Usage** :

La classe `Settings` est conçue pour interagir directement avec l'interface utilisateur,
en facilitant le paramétrage et en générant des objets prêts à l'emploi pour les différentes étapes de simulation ou d'analyse.
"""

import os
from dataclasses import dataclass, field

from SampleMaker import Fluorophore, Mask, Pattern, PatternType
from SampleMaker.Generator import Noiser, Sampler, Stacker, StackModelType
from SampleMaker.GUI.Settings import UI

MIN_SIZE, MAX_SIZE = 32, 4096


##################################################
@dataclass
class Settings:
	"""Classe nécessaire au parsing et enregistrement des différents settings de l'interface

	Dimension : Taille (px), Nombre de Frames
	Setup : Taille des pixels (nm), Ouverture Numérique
	Fluorophore : Longueur d'onde, Intensité (lux ?), Variation (%), Scintillement (ms)
	Répartition : Densité (molécules/µm²), Ratio Astigmatisme, Pattern, options du pattern,
	Bruit : Intensité du bruit de fond (lux ?), Variation du bruit de fond (%), SNR Final
	"""

	size: int = field(init=False, repr=False)
	n_frames: int = field(init=False, repr=False)
	pixel_size: int = field(init=False, repr=False)
	na: float = field(init=False, repr=False)

	wavelength: int = field(init=False, repr=False)
	intensity: float = field(init=False, repr=False)
	delta: float = field(init=False, repr=False)
	flickering: int = field(init=False, repr=False)

	density: float = field(init=False, repr=False)
	astigmatism_ratio: float = field(init=False, repr=False)
	pattern: Pattern = field(init=False, repr=False)
	stack_model_type: StackModelType = field(init=False, repr=False)
	stack_model_options: dict = field(init=False, repr=False)

	snr: float = field(init=False, repr=False)
	background: float = field(init=False, repr=False)
	variation: float = field(init=False, repr=False)

	parsing: bool = field(init=False, repr=False, default=False)

	_ui: dict[str, list[UI.Setting]] = field(init=False, repr=False, default_factory=lambda: dict[str, list[UI.Setting]])

	# ==================================================
	# region Initialization
	# ==================================================
	##################################################
	def __post_init__(self):
		"""
		Méthode appelée automatiquement après l'initialisation du dataclass.
		Initialise les interfaces.
		"""
		self._ui = {
				"Dimension":   [UI.IntSetting(label="Taille (px)", min=MIN_SIZE, max=MAX_SIZE, default=256, step=2),
								UI.IntSetting(label="Nombre de Frames", min=1, max=10000, default=10, step=1)],

				"Setup":       [UI.IntSetting(label="Taille des pixels (nm)", min=1, max=500, default=160, step=10),
								UI.FloatSetting(label="Ouverture Numérique", min=0.05, max=2.0, default=1.4, step=0.2)],

				"Fluorophore": [UI.IntSetting(label="Longueur d'onde (nm)", min=400, max=800, default=600, step=10),
								UI.IntSetting(label="Intensité (lux ?)", min=1, max=10000, default=5000, step=1),
								UI.FloatSetting(label="Variation (%)", min=1, max=100, default=10, step=1),
								UI.IntSetting(label="Scintillement (ms)", min=1, max=100, default=50, step=1)],

				"Structure":   [UI.FloatSetting(label="Densité (molécules/µm²) ", min=0.01, max=2.0, default=0.25, step=0.05),
								UI.FloatSetting(label="Ratio Astigmatisme", min=1, max=5, default=2, step=0.5),
								UI.ComboSetting(label="Masque de répartition",
												choices=[PatternType.NONE.tostring(),
														 PatternType.STRIPES.tostring(),
														 PatternType.SQUARES.tostring(),
														 PatternType.SUN.tostring(),
														 PatternType.EXISTING_IMAGE.tostring()],
												options=[UI.Setting(),
														 UI.IntSetting(label="Longueurs"),
														 UI.IntSetting(label="Taille (px)", min=4, max=MAX_SIZE, default=64, step=2),
														 UI.IntSetting(label="Nombre de Rayons", min=1, max=MAX_SIZE, default=16, step=2),
														 UI.FileSetting(label="Filename")]),
								UI.ComboSetting(label="Style de pile", choices=[StackModelType.RANDOM.tostring()]),
								],

				"Noise":       [UI.IntSetting(label="Intensité du bruit de fond (lux ?)", min=1, max=10000, default=500, step=1),
								UI.FloatSetting(label="Variation du bruit de fond (%)", min=1, max=100, default=10, step=1),
								UI.FloatSetting(label="SNR", min=1, max=20, default=10, step=0.1)]
				}

	##################################################
	@property
	def ui(self) -> dict[str, list[UI.Setting]]:
		"""
		Getter pour les interfaces utilisateurs.

		:return: Le dictionnaire des interfaces.
		"""
		return self._ui

	##################################################
	def reset_ui(self):
		"""
		Réinitialise tous les paramètres aux valeurs par défaut.

		Cette méthode parcourt toutes les sections et appelle la méthode `reset` sur chaque paramètre.
		"""
		for key, value in self._ui.items():
			for setting in value:
				setting.reset()

	# ==================================================
	# endregion Initialization
	# ==================================================

	# ==================================================
	# region Parsing
	# ==================================================
	##################################################
	def parse_settings(self) -> str:
		self.size = self._ui["Dimension"][0].get_value()
		self.n_frames = self._ui["Dimension"][1].get_value()

		self.pixel_size = self._ui["Setup"][0].get_value()
		self.na = self._ui["Setup"][1].get_value()

		self.wavelength = self._ui["Fluorophore"][0].get_value()
		self.intensity = self._ui["Fluorophore"][1].get_value()
		self.delta = self._ui["Fluorophore"][2].get_value()
		self.flickering = self._ui["Fluorophore"][3].get_value()

		self.density = self._ui["Structure"][0].get_value()
		self.astigmatism_ratio = self._ui["Structure"][1].get_value()
		msg = self.parsing_pattern(self._ui["Structure"][2].get_value())
		if msg != "": return msg

		# parsing du Stack Model
		msg = self.parsing_stack_model(self._ui["Structure"][3].get_value())
		if msg != "": return msg

		self.snr = self._ui["Noise"][2].get_value()
		self.background = self._ui["Noise"][0].get_value()
		self.variation = self._ui["Noise"][1].get_value()

		self.parsing = True
		return ""

	##################################################
	def parsing_pattern(self, setting) -> str:
		if setting[0] == 0:
			self.pattern = Pattern.from_pattern(PatternType.NONE)

		# Vérifications pour les bandes
		elif setting[0] == 1:
			self.pattern = Pattern.from_pattern(PatternType.STRIPES)

		# Vérifications pour les carrés
		elif setting[0] == 2:
			s = setting[1]
			if s * 2 > self.size:
				return (f"La taille des carrés est trop élevé\n"
						f"(limite pour un échantillon de taille {self.size}: {self.size // 2}")
			self.pattern = Pattern.from_pattern(PatternType.SQUARES, {"size": s})

		# Vérifications pour le soleil
		elif setting[0] == 3:
			r = setting[1]
			if not (r & r - 1) == 0:
				return (f"Le nombre de rayon doit être une puissance de 2\n"
						f"Ex : 1, 2, 4, 8, 16...)")
			self.pattern = Pattern.from_pattern(PatternType.SUN, {"ray_count": r})

		# Vérifications pour le fichier existant
		elif setting[0] == 4:
			filename = setting[1]
			if filename=="": return f"Aucun fichier n'est spécifié."
			if not os.path.isfile(filename): return f"Le fichier \"{filename}\" est introuvable."
			self.pattern = Pattern.from_pattern(PatternType.EXISTING_IMAGE, {"path": filename})

		else : return "Masque de répartition non reconnu"

		return ""

	##################################################
	def parsing_stack_model(self, setting) -> str:
		if setting[0] == 0:
			self.stack_model_type = StackModelType.RANDOM
			self.stack_model_options = {}
		else: return "Modèle non reconnu."
		return ""

	# ==================================================
	# endregion Parsing
	# ==================================================

	# ==================================================
	# region Meta Object Getter
	# ==================================================
	##################################################
	def get_stacker(self) -> Stacker:
		return Stacker(self.get_sampler())

	##################################################
	def get_sampler(self) -> Sampler:
		return Sampler(size=self.size, pixel_size=self.pixel_size, na=self.na, density=self.density, astigmatism_ratio=self.astigmatism_ratio,
					   fluorophore=self.get_fluorophore(), mask=self.get_mask(), noiser=self.get_noiser())

	##################################################
	def get_fluorophore(self) -> Fluorophore:
		return Fluorophore(wavelength=self.wavelength, intensity=self.intensity, delta=self.delta, flickering=self.flickering)

	##################################################
	def get_mask(self) -> Mask:
		return Mask(_size=self.size, _pattern=self.pattern)

	##################################################
	def get_noiser(self) -> Noiser:
		return Noiser(snr=self.snr, background=self.background, variation=self.variation)

	# ==================================================
	# endregion Meta Object Getter
	# ==================================================

	# ==================================================
	# region IO
	# ==================================================
	##################################################
	def tostring(self) -> str:
		"""
		Retourne une chaîne de caractères correspondant à la liste des settings.

		:return: Une description textuelle des attributs du bruiteur.
		"""
		# if not self.parsing: return "Paramètres non parsés"
		msg = f"Settings :\n"
		for key, settings in self._ui.items():
			msg += f"  - {key} :\n"
			for s in settings:
				msg += f"    - {s.label} : {s.get_value()}\n"

		return msg

	##################################################
	def __str__(self) -> str: return self.tostring()

# ==================================================
# endregion IO
# ==================================================
