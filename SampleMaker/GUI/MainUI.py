"""
Fichier principal pour l'interface utilisateur de Sample Maker.

Ce module définit la classe `MainUI`, qui représente la fenêtre principale de l'application.
Elle gère la barre de menu, la barre d'état, ainsi que le widget central et les interactions principales.
"""

from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QMessageBox

from SampleMaker.GUI.PreferencesDialog import PreferencesDialog
from SampleMaker.GUI.SettingWidget import SettingWidget


##################################################
class MainUI(QMainWindow):
	"""
	Classe représentant la fenêtre principale de l'application.

	Cette classe définit la structure principale de l'interface utilisateur, y compris :
	- Une barre de menu avec des options pour gérer l'application.
	- Une barre d'état pour afficher des messages de statut.
	- Un widget central pour afficher le contenu principal.
	"""

	##################################################
	def __init__(self):
		"""
		Initialise la fenêtre principale.

		Définit le titre, la taille initiale, et configure les composants principaux de l'interface utilisateur.
		"""
		super().__init__()
		self.setWindowTitle("Sample Maker")  # Titre de la fenêtre
		self.setGeometry(100, 100, 800, 600)  # Position et taille (x, y, largeur, hauteur)
		self.init_ui()
		self.adjustSize()  # Ajuster la taille de la fenêtre selon le contenu

	##################################################
	def init_ui(self):
		"""
		Initialisation de l'interface utilisateur.

		Configure les composants principaux de l'application, notamment :
		- La barre de menu.
		- La barre d'état.
		- Le widget central.
		"""
		self.statusBar().showMessage("Prêt")  # Barre de statut avec message par défaut
		self.create_menu_bar()  # Ajout de la barre de menu
		self.setCentralWidget(SettingWidget(self))  # Contenu principal

	##################################################
	def create_menu_bar(self):
		"""
		Création de la barre de menu.

		Définit et ajoute les menus principaux :
		- Fichier : Quitter l'application.
		- Édition : Accéder aux préférences.
		- Aide : Afficher des informations à propos de l'application.
		"""
		menu_bar = self.menuBar()  # Barre de menu principale

		# Menu Fichier
		file_menu = menu_bar.addMenu("Fichier")
		quit_action = QAction("Quitter", self)
		quit_action.setShortcut("Ctrl+Q")  # Raccourci clavier
		quit_action.triggered.connect(self.close)  # Quitte l'application
		file_menu.addAction(quit_action)  # Ajoute l'action au menu

		# Menu Édition
		edit_menu = menu_bar.addMenu("Édition")
		preferences_action = QAction("Préférences", self)
		preferences_action.triggered.connect(self.open_preferences)  # Ouvre la fenêtre des préférences
		edit_menu.addAction(preferences_action)

		# Menu Aide
		help_menu = menu_bar.addMenu("Aide")
		about_action = QAction("À propos", self)
		about_action.setShortcut("Ctrl+H")  # Raccourci clavier
		about_action.triggered.connect(self.show_about_dialog)  # Affiche une boîte de dialogue "À propos"
		help_menu.addAction(about_action)

	##################################################
	def open_preferences(self):  # pragma: no cover
		"""
		Ouvre une fenêtre de préférences.

		Affiche une boîte de dialogue modale permettant de modifier les préférences de l'application.
		"""
		dialog = PreferencesDialog(self)
		dialog.exec_()  # Affiche la boîte de dialogue en mode modal

	##################################################
	def show_about_dialog(self):  # pragma: no cover
		"""
		Affiche une boîte de dialogue 'À propos'.

		Présente des informations sur l'application, telles que son nom, sa version, et l'équipe de développement.
		"""
		QMessageBox.about(self, "À propos de Sample Maker", "Sample Maker - Interface utilisateur\nVersion 1.0\n\nDéveloppé avec PyQt5.", )

	##################################################
	def update_status(self, msg):
		"""
		Met à jour le message dans la barre de statut de la fenêtre principale.

		Cette méthode envoie un message à la barre de statut, ce qui permet de communiquer l'état de l'application à l'utilisateur,
		notamment pendant des opérations longues comme la génération.

		:param msg: Le message à afficher dans la barre de statut.
		"""
		self.statusBar().showMessage(msg)
		QApplication.processEvents()  # Force l'interface à se rafraîchir
		print(msg)
