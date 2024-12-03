""" Fichier des tests pour l'interface utilisateur. """

import platform
import sys

from PyQt5.QtCore import QCoreApplication, Qt, QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

from SampleMaker.GUI import MainUI
from SampleMaker.GUI.PreferencesDialog import PreferencesDialog


##################################################
def initialize():
	"""Fixture pour initialiser l'application Qt"""
	# Si nous sommes dans un environnement CI, forcez l'application à ne pas afficher les fenêtres graphiques
	if not sys.stdout.isatty():  # Vérifie si on est dans un terminal (et donc potentiellement CI)
		QCoreApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
		QApplication.setAttribute(Qt.AA_Use96Dpi)

	app = QApplication([])  # Initialisation de QApplication
	return app


##################################################
def close_messagebox():
	# Recherche la boîte de dialogue QMessageBox affichée
	for widget in QApplication.instance().topLevelWidgets():
		if isinstance(widget, QMessageBox):
			widget.accept()  # Simule un clic sur "OK"


##################################################
def close_dialog(dialog):
	if dialog: dialog.accept()


##################################################
def test_main_ui():
	""" Test basique de l'interface principale """
	app = initialize()
	window = MainUI()
	window.update_status("New Status")
	if platform.system() != "Darwin":
		QTimer.singleShot(100, close_messagebox)  # Ferme automatiquement le QMessageBox
		window.show_about_dialog()
		QTimer.singleShot(100, lambda: close_dialog(window.findChild(QDialog)))  # Ferme automatiquement le QDialog
		window.open_preferences()
	assert True


##################################################
def test_preference_ui():
	""" Test basique de l'interface de préférence """
	app = initialize()
	window = PreferencesDialog()
	assert True


##################################################
def test_settings_ui():
	""" Test basique du widget principal """
	app = initialize()
	window = MainUI()
	widget = window.centralWidget()
	settings_ui = widget.settings.ui
	settings_ui["Dimension"][1].set_value(1)  # On limite à 1 frame pour aller vite
	widget.generate_function()
	assert True

# qtbot crash
###################################################
# def test_preference_dialog(qtbot, app):
#	window = app
#	window.show()
#
#	# Simuler un clic sur le menu Édition -> Préférences
#	menu_bar = window.menuBar()
#	edit_menu = menu_bar.findChild(QMenu, "Édition")  # Ajustez le nom du menu
#	preferences_action = edit_menu.findChild(QAction, "Préférences")  # Ajustez le nom de l'action
#	qtbot.mouseClick(preferences_action, Qt.LeftButton)
#
#	# Vérifier que la fenêtre Préférences est ouverte
#	preference_window = window.findChild(QDialog, "PreferencesDialog")
#	assert preference_window.isVisible() is True
#
#	# Simuler la fermeture de la fenêtre Préférences
#	close_button = preference_window.findChild(QPushButton, "Fermer")  # Ajustez le bouton de fermeture
#	qtbot.mouseClick(close_button, Qt.LeftButton)
#
#	# Vérifier que la fenêtre Préférences est fermée
#	assert preference_window.isVisible() is False
#
###################################################
# def test_about(qtbot, app):
#	window = app
#	window.show()
#
#	# Simuler un clic sur le menu Aide -> À propos
#	menu_bar = window.menuBar()
#	help_menu = menu_bar.findChild(QMenu, "Aide")  # Ajustez le nom du menu
#	about_action = help_menu.findChild(QAction, "À propos")  # Ajustez le nom de l'action
#	qtbot.mouseClick(about_action, Qt.LeftButton)
#
#	# Vérifier que la fenêtre À propos est ouverte
#	about_window = window.findChild(QDialog, "AboutDialog")  # Assurez-vous de l'identifiant correct
#	assert about_window.isVisible() is True
#
#	# Simuler la fermeture de la fenêtre À propos
#	close_button = about_window.findChild(QPushButton, "Fermer")  # Ajustez le bouton de fermeture
#	qtbot.mouseClick(close_button, Qt.LeftButton)
#
#	# Vérifier que la fenêtre À propos est fermée
#	assert about_window.isVisible() is False
#
###################################################
#
###################################################
#
