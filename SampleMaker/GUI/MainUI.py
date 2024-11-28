import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sample Maker")  # Titre de la fenêtre
        self.setGeometry(100, 100, 800, 600)  # Position et taille (x, y, largeur, hauteur)
        self.init_ui()

    def init_ui(self):
        """Initialisation de l'interface utilisateur."""
        # Ajoutez ici vos widgets et configurations d'interface
        self.statusBar().showMessage("Prêt")  # Barre de statut avec message par défaut
        self.create_menu_bar()               # Ajout de la barre de menu

    def create_menu_bar(self):
        """Création de la barre de menu."""
        menu_bar = self.menuBar()  # Barre de menu principale

        # Menu Fichier
        file_menu = menu_bar.addMenu("Fichier")

        # Action Quitter
        quit_action = QAction("Quitter", self)
        quit_action.setShortcut("Ctrl+Q")  # Raccourci clavier
        quit_action.triggered.connect(self.close)  # Quitte l'application
        file_menu.addAction(quit_action)  # Ajoute l'action au menu