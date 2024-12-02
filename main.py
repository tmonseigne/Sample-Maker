import sys
from PyQt5.QtWidgets import QApplication

from SampleMaker.GUI.MainUI import MainUI


def main():
    """Point d'entrée principal de l'application."""
    app = QApplication(sys.argv)  # Initialisation de l'application PyQt
    window = MainUI()        	  # Création de la fenêtre principale
    window.show()                 # Affichage de la fenêtre
    sys.exit(app.exec_())         # Exécution de la boucle d'événements


if __name__ == "__main__":
    main()
