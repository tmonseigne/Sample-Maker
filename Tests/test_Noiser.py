""" Tests pour la génération de pattern """

import os
from pathlib import Path

import numpy as np

from SampleMaker.FileIO import save_sample_as_png
from SampleMaker.Noiser import Noiser

INPUT_DIR = Path(__file__).parent / "Input"
OUTPUT_DIR = Path(__file__).parent / "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)						# Créer le dossier de sorties (la première fois, il n'existe pas)
size, n_tile = 512, 2										# Taille de l'image de test
up = np.linspace(0, 255, size // n_tile, dtype=np.float32)  # Création du dégradé croissant de 0 à 255
gradient = np.tile(up, n_tile)								# Répète en N tuiles
ref_image = np.tile(gradient, (size, 1))					# Répète le dégradé sur toutes les lignes


##################################################
def test_noiser():
	""" Test basique sur le noiser. """
	noiser = Noiser(10, 20, 10)
	print(noiser)
	res = noiser.apply(ref_image)
	save_sample_as_png(res, f"{OUTPUT_DIR}/test_noiser_base.png", 0)


##################################################
def test_noiser_no_noise():
	""" Test sur le noiser avec uniquement le snr. """
	for snr in range(10):
		noiser = Noiser(snr=0, background=0, variation=0)
		res = noiser.apply(ref_image)
		save_sample_as_png(res, f"{OUTPUT_DIR}/test_noiser_no_noise.png", 0)
		assert np.allclose(res, ref_image, atol=1e-5), "L'échantillon devrait correspondre à la référence avec une tolérance d'erreur."


##################################################
def test_noiser_only_snr():
	""" Test sur le noiser avec uniquement le snr. """
	for snr in [1, 2.5, 5, 10.3]:
		noiser = Noiser(snr=snr, background=0, variation=0)
		res = noiser.apply(ref_image)
		save_sample_as_png(res, f"{OUTPUT_DIR}/test_noiser_snr_{snr}.png", 0)


##################################################
def test_noiser_only_background():
	""" Test sur le noiser avec uniquement le snr. """
	noiser = Noiser(0, 50, 50)
	res = noiser.apply(ref_image)
	save_sample_as_png(res, f"{OUTPUT_DIR}/test_noiser_background.png", 0)
