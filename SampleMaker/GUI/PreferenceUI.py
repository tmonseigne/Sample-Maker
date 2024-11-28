from PyQt5.QtWidgets import QDialog


class PreferencesDialog(QDialog):
    """Boîte de dialogue des préférences."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Préférences")
        self.setGeometry(200, 200, 400, 300)  # Position et taille (x, y, largeur, hauteur)
