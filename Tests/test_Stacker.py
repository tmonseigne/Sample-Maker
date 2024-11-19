""" Fichier des tests pour le Stacker : le générateur de pile d'échantillons """

import os
from pathlib import Path


INPUT_DIR = Path(__file__).parent / "Input"
OUTPUT_DIR = Path(__file__).parent / "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)
SIZE = 256

##################################################
def test_stacker():
	""" Test basique sur le générateur de stack. """
	print("TODO")