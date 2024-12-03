""" Fichier des tests pour l'interface utilisateur. """

import sys
from pathlib import Path

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from SampleMaker.GUI.Settings import Settings, UI
from SampleMaker.Tools import print_warning

INPUT_DIR = Path(__file__).parent / "Input"


##################################################
def initialize():
	"""Fixture pour initialiser l'application Qt"""
	# Si nous sommes dans un environnement CI, forcez l'application à ne pas afficher les fenêtres graphiques
	if not sys.stdout.isatty():  # Vérifie si on est dans un terminal (et donc potentiellement CI)
		QCoreApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
		QApplication.setAttribute(Qt.AA_Use96Dpi)

	app = QApplication([])  # Initialisation de QApplication
	return app


def setting_base_test(setting: UI.Setting, change, default_expected, change_expected):
	assert setting.get_value() == default_expected, "Valeur par défaut non valide."
	setting.set_value(change)
	assert setting.get_value() == change_expected, "Valeur défini non valide."
	setting.reset()
	assert setting.get_value() == default_expected, "Valeur par défaut non valide."


###################################################
def test_setting():
	""" Test basique de la classe (constructeur, getter, setter) """
	app = initialize()
	setting = UI.Setting()
	setting_base_test(setting, None, None, None)
	assert True


###################################################
def test_int_setting():
	""" Test basique de la classe (constructeur, getter, setter) """
	app = initialize()
	setting = UI.IntSetting("Test", 0, 10, 1, 1)
	setting_base_test(setting, 5, 1, 5)
	assert True


###################################################
def test_float_setting():
	""" Test basique de la classe (constructeur, getter, setter) """
	app = initialize()
	setting = UI.FloatSetting("Test", 0.0, 10.0, 1.0, 1.0)
	setting_base_test(setting, 5.0, 1.0, 5.0)
	assert True


###################################################
def test_combo_setting():
	""" Test basique de la classe (constructeur, getter, setter) """
	app = initialize()
	setting = UI.ComboSetting(label="Test", choices=["Choix 1", "Choix 2"], options=[UI.Setting(), UI.IntSetting(label="Option du choix 2")])
	setting_base_test(setting, 1, [0, None], [1, 0])
	setting = UI.ComboSetting(label="Test", choices=["Choix 1", "Choix 2"], options=[])
	setting_base_test(setting, 1, [0, None], [1, None])
	assert True


###################################################
def test_file_setting():
	""" Test basique de la classe (constructeur, getter, setter) """
	app = initialize()
	setting = UI.FileSetting(label="Test")
	setting_base_test(setting, "filename.extension", "", "filename.extension")
	assert True


###################################################
def test_settings():
	""" Test basique de la classe (constructeur, getter, setter) """
	app = initialize()
	settings = Settings()
	ui = settings.ui
	settings.reset_ui()
	res = settings.parse_settings()
	stacker = settings.get_stacker()
	print(settings)
	assert True


###################################################
def test_settings_pattern_management():
	""" Test sur le reglage du pattern """
	app = initialize()
	settings = Settings()
	# Change Pattern Options
	ui = settings.ui
	# Stripes
	ui["Structure"][2].set_value(1)
	res = settings.parse_settings()
	# Squares
	ui["Structure"][2].set_value(2)
	res = settings.parse_settings()
	ui["Structure"][2].options[2].set_value(500)  # Bad Size
	res = settings.parse_settings()
	print_warning(res)
	# Sun
	ui["Structure"][2].set_value(3)
	res = settings.parse_settings()
	ui["Structure"][2].options[3].set_value(3)  # Bad Count
	res = settings.parse_settings()
	print_warning(res)
	# File
	ui["Structure"][2].set_value(4)
	ui["Structure"][2].options[4].set_value(f"{INPUT_DIR}/PALM_ref.png")  # Good Filename
	res = settings.parse_settings()
	ui["Structure"][2].options[4].set_value("")   # No Filename
	res = settings.parse_settings()
	print_warning(res)
	ui["Structure"][2].options[4].set_value("filename")  # Bad Filename
	res = settings.parse_settings()
	print_warning(res)
	# Out of index
	ui["Structure"][2].set_value(5)
	res = settings.parse_settings()
	print_warning(res)
	assert True


###################################################
def test_settings_stack_management():
	""" Test sur le reglage du modèle """
	app = initialize()
	settings = Settings()
	# Change Stack Options
	ui = settings.ui
	# Out of index
	ui["Structure"][3].set_value(1)
	res = settings.parse_settings()
	print_warning(res)
	assert True
