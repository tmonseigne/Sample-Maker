"""
Fichier contenant la classe `Setting` et ses sous-classes pour la gestion des paramètres d'interface utilisateur.

Ce module définit la classe abstraite `Setting`, qui sert de base pour la création de différents types de paramètres dans une interface utilisateur PyQt5.
Les sous-classes permettent de gérer des paramètres spécifiques tels que les entiers, les flottants et les listes déroulantes.
Ces classes sont utilisées pour créer et configurer des widgets de paramètres dans une interface graphique.

Classes :

    - Setting : Classe de base pour un paramètre d'interface utilisateur.
    - ComboSetting : Paramètre de type liste déroulante avec options.
    - FileSetting : Paramètre de Type ouverture de fichier.
    - FloatSetting : Paramètre de type flottant (float).
    - IntSetting : Paramètre de type entier (integer).
"""

import os
from dataclasses import dataclass, field
from typing import Any, List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QDoubleSpinBox, QFileDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QSpinBox


# ==================================================
# region Setting
# ==================================================
##################################################
@dataclass
class Setting:
	"""
	Classe mère abstraite pour la gestion des paramètres dans l'interface utilisateur.

	Cette classe représente un paramètre d'interface utilisateur avec un layout spécifique. Elle est utilisée comme
	base pour des paramètres plus spécifiques. Chaque paramètre pourra hériter de cette classe pour définir son
	comportement et ses options spécifiques.

	Attributs :
		- **label (str)** : Nom du paramètre.
		- **_layout (QHBoxLayout)** : Le layout associé à ce paramètre, initialisé par défaut à un QHBoxLayout.
	"""

	label: str = ""
	_layout: QFormLayout = field(init=False, default_factory=QFormLayout)

	##################################################
	def __post_init__(self):
		""" Méthode appelée automatiquement après l'initialisation du dataclass. """
		self.initialize()

	##################################################
	def get_layout(self) -> QFormLayout:
		"""
		Retourne le layout associé à ce paramètre.

		Cette méthode permet d'accéder au layout pour intégrer le paramètre dans l'interface utilisateur.

		:return: Le layout associé à ce paramètre.
		"""
		return self._layout

	##################################################
	def get_value(self) -> Any:
		"""
		Retourne la valeur du paramètre.

		Cette méthode permet d'accéder à la valeur du paramètre pour la récupérer dans l'interface utilisateur.

		:return: La valeur associée à ce paramètre.
		"""
		return None

	##################################################
	def initialize(self):
		"""
		Méthode abstraite pour initialiser le paramètre.

		Cette méthode doit être implémentée dans les sous-classes pour définir le comportement de réinitialisation du paramètre spécifique.
		"""
		self._layout = QFormLayout()
		self._layout.setAlignment(Qt.AlignLeft)  # Définir l'alignement du layout à gauche

	##################################################
	def add_row(self, box):
		"""
		Ajoute la ligne avec le label et l'input

		:param box: Input à ajouter
		"""
		self._layout.addRow(QLabel(self.label + " : "), box)  # Ajoute le setting

	##################################################
	def reset(self):
		"""
		Méthode abstraite pour réinitialiser le paramètre à sa valeur par défaut.

		Cette méthode doit être implémentée dans les sous-classes pour définir le comportement de réinitialisation
		du paramètre spécifique.
		"""
		return


# ==================================================
# endregion Setting
# ==================================================

# ==================================================
# region Setting Int
# ==================================================
##################################################
@dataclass
class IntSetting(Setting):
	""" Classe pour un paramètre spécifique de type SpinBox Entier. """
	min: int = 0
	max: int = 100
	default: int = 0
	step: int = 1
	box: QSpinBox = field(init=False, default_factory=QSpinBox)

	##################################################
	def get_value(self) -> int: return self.box.value()

	##################################################
	def initialize(self):
		super().initialize()  # Appelle l'initialisation de la classe mère
		self.box = QSpinBox()
		self.box.setAlignment(Qt.AlignLeft)  # Définir l'alignement du layout à gauche
		self.box.setRange(self.min, self.max)
		self.box.setSingleStep(self.step)
		self.box.setValue(self.default)
		self.add_row(self.box)  # Ajoute le spin

	##################################################
	def reset(self):
		self.box.setValue(self.default)

# ==================================================
# endregion Setting Int
# ==================================================

# ==================================================
# region Setting Float
# ==================================================
##################################################
@dataclass
class FloatSetting(Setting):
	""" Classe pour un paramètre spécifique de type SpinBox réel. """
	min: float = 0.0
	max: float = 100.0
	default: float = 0.0
	step: float = 1.0
	precision: int = 2
	box: QDoubleSpinBox = field(init=False, default_factory=QDoubleSpinBox)

	##################################################
	def get_value(self) -> float: return self.box.value()

	##################################################
	def initialize(self):
		super().initialize()  # Appelle l'initialisation de la classe mère
		self.box = QDoubleSpinBox()
		self.box.setAlignment(Qt.AlignLeft)  # Définir l'alignement du layout à gauche
		self.box.setRange(self.min, self.max)
		self.box.setSingleStep(self.step)
		self.box.setDecimals(self.precision)
		self.box.setValue(self.default)
		self.add_row(self.box)  # Ajoute le spin

	##################################################
	def reset(self): self.box.setValue(self.default)

# ==================================================
# endregion Setting Float
# ==================================================

# ==================================================
# region Setting List with or without options
# ==================================================
##################################################
@dataclass
class ComboSetting(Setting):
	""" Classe pour un paramètre spécifique de type Liste déroulante avec affichage d'options. """
	choices: List[str] = field(default_factory=lambda: ["No Setting"])
	options: List[Setting] = field(default_factory=lambda: [])  # Liste de settings
	box: QComboBox = field(init=False, default_factory=QComboBox)

	##################################################
	def get_value(self) -> Any:
		index = self.box.currentIndex()
		if index < len(self.options):
			return [index, self.options[index].get_value()]
		return [index, None]

	##################################################
	def initialize(self):
		super().initialize()  # Appelle l'initialisation de la classe mère
		self.box = QComboBox()
		self.box.setFixedWidth(150)  # Réduire la largeur du combo
		self.box.addItems(self.choices)
		self.add_row(self.box)  # Ajoute la liste déroulante
		if len(self.options) != 0:
			self.box.currentIndexChanged.connect(self.update_options)
			self.update_options(0)  # Initialise les options pour "Choix 1"

	##################################################
	def reset(self):
		self.box.setCurrentIndex(0)

	##################################################
	def update_options(self, index):
		while self._layout.rowCount() > 1: self._layout.removeRow(1)
		for option in self.options: option.initialize()  # recréer version fonctionnelle du layout de l'option
		self._layout.addRow(QLabel("Options : "), self.options[index].get_layout())

# ==================================================
# endregion Setting List with or without options
# ==================================================

# ==================================================
# region Setting File
# ==================================================
##################################################
@dataclass
class FileSetting(Setting):
	""" Classe pour un paramètre spécifique de type Ouverture de fichier. """
	box: QLineEdit = field(init=False, default_factory=QLineEdit)  # Boîte de texte pour afficher le chemin

	##################################################
	def initialize(self):
		"""
		Initialise le paramètre pour ouvrir un fichier.

		Si le chemin par défaut est incorrect ou inexistant, il sera remplacé par
		le chemin du dossier principal du projet (ou autre chemin par défaut).
		"""
		super().initialize()  # Appelle l'initialisation de la classe mère
		self.box = QLineEdit()
		self.box.setAlignment(Qt.AlignLeft)  # Définir l'alignement du layout à gauche

		# Ajouter un bouton à côté pour permettre de choisir le fichier
		browse_button = QPushButton("Choisir un fichier")
		browse_button.clicked.connect(self.browse_file)  # Connecter le bouton à la méthode de sélection

		# Disposer le QLineEdit et le bouton dans un layout horizontal
		layout = QHBoxLayout()
		layout.setAlignment(Qt.AlignLeft)  # Définir l'alignement du layout à gauche
		layout.addWidget(self.box)
		layout.addWidget(browse_button)

		self.add_row(layout)		# Ajouter au layout principal du setting

	##################################################
	def browse_file(self):
		"""
		Ouvre un dialogue de sélection de fichier et met à jour la boîte avec le chemin sélectionné.
		"""
		current = self.get_value()
		# Si le chemin par défaut n'est pas valide, on utilise le chemin principal du projet
		if not os.path.exists(current) or current == "": current = os.getcwd()
		path, _ = QFileDialog.getOpenFileName(self.box, "Sélectionner un fichier", current)
		if path: self.box.setText(path)  # Met à jour le chemin dans la boîte de texte

	##################################################
	def get_value(self) -> str:
		"""
		Retourne le chemin du fichier sélectionné.
		:return: Le chemin du fichier sous forme de chaîne.
		"""
		return self.box.text()

	def reset(self):
		"""Réinitialise le paramètre à son chemin par défaut."""
		self.box.setText("")  # Remet le texte dans la boîte de saisie au chemin par défaut

# ==================================================
# endregion Setting File
# ==================================================
