"""
Module contenant la classe `MainWidget` pour l'interface principale de l'application.

Ce module définit la classe `MainWidget`, qui crée et gère l'interface utilisateur principale de l'application.
Elle contient des sections de paramètres organisées sous forme de layout,
permettant de modifier différents paramètres pour la génération de fichiers et l'affichage des résultats.
Le widget principal gère également la barre de statut et les actions associées aux boutons de l'interface utilisateur.
"""

import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLayout, QMessageBox, QPushButton, QVBoxLayout, QWidget

from SampleMaker.GUI.Settings.Settings import Settings
from SampleMaker.Tools.Utils import add_suffix, get_timestamp_for_files

# Gestion des dossiers
OUTPUT_DIR = "Output"
MIN_SIZE, MAX_SIZE = 32, 4096


##################################################
class MainWidget(QWidget):
	""" Widget principal gérant toute l'interface """

	##################################################
	def __init__(self, parent=None):
		"""
		Initialise le widget principal de l'interface utilisateur.

		Cette méthode configure l'interface en ajoutant différentes sections de paramètres dans la mise en page.
		Elle crée également les boutons "Reset" et "Générer" et relie les actions correspondantes.

		:param parent: Widget parent de ce widget, généralement la fenêtre principale (MainUI).
		"""
		super().__init__(parent)  # Initialise QWidget avec le parent
		self.parent = parent  # Stocke une référence à MainUI

		# Mise en page principale
		self.main_layout = QVBoxLayout()
		self.main_layout.setAlignment(Qt.AlignTop)

		# Liste des settings
		##################################################
		self.settings = Settings()

		# Section Dimensions
		setting_layout = QHBoxLayout()
		setting_layout.setAlignment(Qt.AlignLeft)  # Définir l'alignement du layout à gauche
		for s in self.settings.ui["Dimension"]: setting_layout.addLayout(s.get_layout())
		self.main_layout.addLayout(self.create_section("Dimensions", setting_layout))

		# Section Setup
		setting_layout = QHBoxLayout()
		setting_layout.setAlignment(Qt.AlignLeft)  # Définir l'alignement du layout à gauche
		for s in self.settings.ui["Setup"]: setting_layout.addLayout(s.get_layout())
		self.main_layout.addLayout(self.create_section("Installation", setting_layout))

		# Section Fluorophore
		setting_layout = QHBoxLayout()
		setting_layout.setAlignment(Qt.AlignLeft)  # Définir l'alignement du layout à gauche
		for s in self.settings.ui["Fluorophore"]: setting_layout.addLayout(s.get_layout())
		self.main_layout.addLayout(self.create_section("Fluorophore", setting_layout))

		# Section Répartition
		setting_layout = QVBoxLayout()
		setting_layout.setAlignment(Qt.AlignLeft)  # Définir l'alignement du layout à gauche
		first_part = QHBoxLayout()
		first_part.setAlignment(Qt.AlignLeft)  # Définir l'alignement du layout à gauche
		first_part.addLayout(self.settings.ui["Structure"][0].get_layout())
		first_part.addLayout(self.settings.ui["Structure"][1].get_layout())
		setting_layout.addLayout(first_part)
		setting_layout.addLayout(self.settings.ui["Structure"][2].get_layout())
		setting_layout.addLayout(self.settings.ui["Structure"][3].get_layout())
		self.main_layout.addLayout(self.create_section("Structure", setting_layout))

		# Section Bruit
		setting_layout = QHBoxLayout()
		setting_layout.setAlignment(Qt.AlignLeft)  # Définir l'alignement du layout à gauche
		for s in self.settings.ui["Noise"]: setting_layout.addLayout(s.get_layout())
		self.main_layout.addLayout(self.create_section("Bruit", setting_layout))

		# Ajouter les boutons Reset et Générer
		buttons_layout = QHBoxLayout()
		reset_button = QPushButton("Reset")
		reset_button.clicked.connect(self.settings.reset_ui)
		generate_button = QPushButton("Générer")
		generate_button.clicked.connect(self.generate_function)
		buttons_layout.addWidget(reset_button)
		buttons_layout.addWidget(generate_button)

		self.main_layout.addLayout(buttons_layout)

		# Appliquer la mise en page principale
		self.setLayout(self.main_layout)

	##################################################
	def create_section(self, title: str, layout: QLayout) -> QVBoxLayout:
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
	def generate_function(self):
		"""
		Fonction de génération appelée lors du clic sur le bouton "Générer".

		Cette méthode récupère les valeurs des paramètres, effectue les calculs nécessaires
		et génère les fichiers de sortie en utilisant les valeurs des paramètres actuels.
		Elle met à jour la barre de statut pour informer l'utilisateur de l'état d'avancement.
		"""
		# Cette fonction sera appelée quand le bouton "Générer" est cliqué
		self.parent.update_status("Génération en cours...")
		msg = self.settings.parse_settings()
		if msg != "":
			self.warning_popup("Erreur de paramètres", msg)
			return

		self.parent.update_status("Génération en cours... Paramètres récupérés...")
		print(self.settings)

		# Création du générateur
		stacker = self.settings.get_stacker()
		self.parent.update_status("Génération en cours... Paramètres récupérés... Paramétrisation effectué...")

		# Génération de la pile
		stack = stacker.generate(self.settings.n_frames)
		os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)
		timestamp = get_timestamp_for_files()
		stack.save(f"{OUTPUT_DIR}/{add_suffix("stack.tif", timestamp)}")
		self.save_log(f"{OUTPUT_DIR}/{add_suffix("stack.log", timestamp)}")
		self.parent.update_status("Génération terminée")

	##################################################
	def save_log(self, filename: str):
		"""
		Sauvegarde les paramètres dans un fichier log avec les valeurs actuelles.

		Cette méthode écrit les paramètres actuels dans un fichier texte, ce qui permet de garder une trace des paramètres
		utilisés pour une génération particulière.

		:param filename: Le chemin du fichier où enregistrer le log.
		"""
		with open(filename, "w", encoding="utf-8") as f:
			f.write(self.settings.tostring())

	##################################################
	def warning_popup(self, title: str, msg: str):
		"""
		Affiche une fenêtre contextuelle d'avertissement avec un titre et un message spécifié.

		Cette fonction est utilisée pour afficher une boîte de dialogue contenant un message d'avertissement pour l'utilisateur.
		Elle est particulièrement utile pour avertir l'utilisateur de problèmes ou erreurs lors de l'exécution.

		:param title: Le titre de la fenêtre d'avertissement.
		:param msg: Le message à afficher dans la boîte de dialogue.
		"""
		# Création de la boîte de message
		msg_box = QMessageBox(self)
		msg_box.setIcon(QMessageBox.Warning)  # Icône de type avertissement
		msg_box.setWindowTitle(title)  # Titre de la boîte de dialogue
		msg_box.setText(msg)  # Message d'avertissement
		msg_box.setStandardButtons(QMessageBox.Ok)  # Bouton OK pour fermer la boîte

		# Afficher la boîte de message et attendre la réponse de l'utilisateur
		msg_box.exec_()

