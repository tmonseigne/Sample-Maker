""" Tests pour la génération d'images """

from pathlib import Path

import numpy as np

from FileIO import open_png_as_boolean_mask
from ImageGenerator import apply_mask, compute_molecule_number, compute_molecule_localisation
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


##################################################
def test_compute_molecule_localisation():
	"""
	Test de la fonction compute_molecule_localisation.
	"""

	res = compute_molecule_localisation(size=100, pixel_size=100, density=1.0)
	assert res.shape == (100, 3), f"Le résultat est {res.shape} au lieu de (100,3)"

	res = compute_molecule_localisation(256, 160, 0.25)
	assert res.shape == (419, 3), f"Le résultat est {res.shape} au lieu de (419,3)"


##################################################
def test_apply_mask():
	"""
	Test de la fonction compute_molecule_localisation.
	"""

	localisation = compute_molecule_localisation(256, 160, 0.25)
	mask = generate_mask(Pattern.SQUARES, 256)
	res = apply_mask(localisation, mask)
	assert res.shape[0] <= 419, f"Le résultat possède plus de molécule après application du masque."

	mask = generate_mask(Pattern.NONE, 256)
	res = apply_mask(localisation, mask)
	assert res.shape == (419, 3), f"Le résultat possède un nombre différent de molécules après application du masque blanc."

	res = apply_mask(localisation, ~mask)
	assert res.shape == (0, 3), f"Le résultat possède des molécules après application du masque noir."

