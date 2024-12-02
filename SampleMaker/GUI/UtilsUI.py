"""
Fichier de fonctions génériques pour l'interface utilisateur.

Ce module contient des fonctions utilitaires pour la création de composants d'interface utilisateur basés sur PyQt5,
tels que des sections de mise en page et des boîtes de saisie numériques.
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDoubleSpinBox, QHBoxLayout, QLabel, QLayout, QSpinBox, QVBoxLayout


# ==================================================
# region Layout
# ==================================================
##################################################
def create_section(title: str, layout: QLayout) -> QVBoxLayout:
	"""
	Crée une section verticale composée d'un titre et d'une mise en page donnée.

	Cette fonction est utile pour organiser des groupes d'éléments dans une	interface utilisateur.
	Elle ajoute un titre sous forme de texte enrichi (<b> pour le gras) au-dessus du layout spécifié.

	:param title: Texte du titre à afficher au-dessus de la mise en page.
	:param layout: Mise en page (layout) à inclure sous le titre.
	:return: Un `QVBoxLayout` contenant le titre et le layout fourni.
	"""
	res = QVBoxLayout()
	res.setAlignment(Qt.AlignTop)
	res.addWidget(QLabel(f"<b>{title}</b>"))
	res.addLayout(layout)
	return res


##################################################
def create_line_settings_layout(settings) -> QHBoxLayout:
	"""
	Crée une mise en page horizontale avec des éléments d'interface	utilisateur à partir des paramètres fournis.

	Cette fonction permet d'ajouter une série d'éléments à une mise en page horizontale,
	où chaque élément est défini par un titre (texte) et un widget associé.
	Les widgets seront ajoutés dans l'ordre où ils apparaissent dans la liste `settings`.

	:param settings: Liste de tuples, chaque tuple contient un titre (chaîne de caractères)
	                 et un widget (comme un QLabel, QSpinBox, etc.) à ajouter à la mise en page.
	                 Exemple : `[("Titre1", widget1), ("Titre2", widget2)]`.

	:return: Un objet `QHBoxLayout` qui contient les widgets et titres fournis.
	        Les titres et widgets sont ajoutés à la mise en page de gauche à droite.
	"""
	res = QHBoxLayout()
	# Définir l'alignement du layout à gauche
	res.setAlignment(Qt.AlignLeft)
	for setting in settings:
		res.addWidget(QLabel(setting[0]))  # Ajoute le titre
		res.addWidget(setting[1])  # Ajoute le widget associé
	return res


# ==================================================
# endregion Layout
# ==================================================


# ==================================================
# region Inputs box
# ==================================================
##################################################
def create_spin_box(min_val: int = 0, max_val: int = 100, default_val: int = 0, step: int = 1) -> QSpinBox:
	"""
	Crée une boîte de saisie numérique entière avec des valeurs minimales, maximales et un pas personnalisables.

	:param min_val: Valeur minimale autorisée (par défaut : 0).
	:param max_val: Valeur maximale autorisée (par défaut : 100).
	:param default_val: Valeur par défaut de l'entrée (par défaut : 0).
	:param step: Incrément à utiliser lors du changement de valeur (par défaut : 1).
	:return: Un objet `QSpinBox` configuré selon les paramètres.
	"""
	res = QSpinBox()
	res.setRange(min_val, max_val)
	res.setSingleStep(step)
	res.setValue(default_val)
	return res


##################################################
def create_double_spin_box(min_val: float = 0.0, max_val: float = 100.0, default_val: float = 0.0,
						   step: float = 0.01, precision: int = 2) -> QDoubleSpinBox:
	"""
	Crée une boîte de saisie numérique flottante avec des valeurs minimales, maximales, un pas, et une précision personnalisables.

	:param min_val: Valeur minimale autorisée (par défaut : 0.0).
	:param max_val: Valeur maximale autorisée (par défaut : 100.0).
	:param default_val: Valeur par défaut de l'entrée (par défaut : 0).
	:param step: Incrément à utiliser lors du changement de valeur (par défaut : 0.01).
	:param precision: Nombre de décimales à afficher (par défaut : 2).
	:return: Un objet `QDoubleSpinBox` configuré selon les paramètres.
	"""
	res = QDoubleSpinBox()
	res.setRange(min_val, max_val)
	res.setSingleStep(step)
	res.setDecimals(precision)
	res.setValue(default_val)
	return res

# ==================================================
# end region Inputs box
# ==================================================
