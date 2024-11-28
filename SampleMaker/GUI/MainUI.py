from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMessageBox, QDialog
from SampleMaker.GUI.PreferenceUI import PreferencesDialog


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

    def open_preferences(self):
        """Ouvre une fenêtre de préférences."""
        dialog = PreferencesDialog(self)
        dialog.exec_()  # Affiche la boîte de dialogue en mode modal

    def show_about_dialog(self):
        """Affiche une boîte de dialogue 'À propos'."""
        QMessageBox.about(
            self,
            "À propos de Sample Maker",
            "Sample Maker - Interface utilisateur\nVersion 1.0\n\nDéveloppé avec PyQt5.",
        )