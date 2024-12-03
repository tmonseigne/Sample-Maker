""" Fichier des tests pour l'interface utilisateur. """

import sys

import pytest
from PyQt5.QtCore import QCoreApplication, QLoggingCategory
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from SampleMaker.GUI import MainUI, SettingWidget
from pytestqt.qtbot import QtBot

import sys
import traceback

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
def test_main_ui():
	app = initialize()
	window = MainUI()
	window.update_status("New Status")
	# window.show_about_dialog() # Need to close and qtbot crash
	# window.open_preferences() # Need to close and qtbot crash


##################################################
def test_preference_ui():
	app = initialize()
	window = PreferencesDialog()


##################################################
def test_settings_ui():
	app = initialize()
	window = MainUI()
	widget = window.centralWidget()
	settings_ui = widget.settings.ui
	settings_ui["Dimension"][1].set_value(1) # On limite à 1 frame pour aller vite
	widget.generate_function()


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
