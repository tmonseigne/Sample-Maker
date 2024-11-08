""" Tests pour la génération d'images """

from pathlib import Path

import numpy as np

from FileIO import open_png_as_boolean_mask
from ImageGenerator import compute_molecule_number
from PatternGenerator import generate_mask, Pattern

SAMPLES_DIR = Path(__file__).parent / "Samples"


##################################################
def test_compute_molecule_numbert():
	"""
	Test de la fonction compute_molecule_numbert.
	"""

	res = compute_molecule_number(100, 100, 1.0)
	assert res == 100, f"le résultat est {res} au lieu de 100"

	res = compute_molecule_number(256, 160, 0.1)
	assert res == 167, f"le résultat est {res} au lieu de 167"

	res = compute_molecule_number(256, 160, 0.25)
	assert res == 419, f"le résultat est {res} au lieu de 419"

	res = compute_molecule_number(256, 160, 0.5)
	assert res == 838, f"le résultat est {res} au lieu de 838"

	res = compute_molecule_number(256, 160, 1.0)
	assert res == 1677, f"le résultat est {res} au lieu de 1677"
