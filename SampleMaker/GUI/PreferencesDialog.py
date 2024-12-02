"""
Fichier de gestion des préférences de l'application.

Ce module contient la classe `PreferencesDialog`, qui définit une boîte de dialogue permettant à l'utilisateur
de configurer les préférences de l'application. La boîte de dialogue est une fenêtre modale qui permet de modifier
les paramètres utilisateur dans une interface simple et claire.

La classe `PreferencesDialog` hérite de `QDialog` de PyQt5 et fournit des mécanismes pour afficher une fenêtre de
préférences avec des widgets et des options configurables.
"""

from PyQt5.QtWidgets import QDialog


##################################################
class PreferencesDialog(QDialog):
	"""Boîte de dialogue des préférences.

	Cette classe crée une fenêtre de préférences permettant à l'utilisateur de définir des options de configuration
	pour l'application. Elle hérite de `QDialog` et permet de personnaliser l'apparence et le comportement de l'interface.

	.. note:: Cette boite de dialogue est pour le moment inutile.
	"""

	##################################################
	def __init__(self, parent=None):
		"""
		Initialise la boîte de dialogue des préférences.

		Cette méthode définit le titre, la géométrie (position et taille) de la boîte de dialogue,
		ainsi que les éléments de base de l'interface utilisateur.

		:param parent: QWidget (optionnel) : Le widget parent. Par défaut, il est `None`.
		"""
		super().__init__(parent)
		self.setWindowTitle("Préférences")
		self.setGeometry(200, 200, 400, 300)  # Position et taille (x, y, largeur, hauteur)
