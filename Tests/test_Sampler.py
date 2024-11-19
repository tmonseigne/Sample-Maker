""" Tests pour la génération de pattern """

import os
from pathlib import Path

import numpy as np

from SampleMaker.FileIO import save_sample_as_png
from SampleMaker.Noiser import Noiser
from SampleMaker.Sampler import Sampler

INPUT_DIR = Path(__file__).parent / "Input"
OUTPUT_DIR = Path(__file__).parent / "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)						# Créer le dossier de sorties (la première fois, il n'existe pas)


##################################################
def test_sampler():
	""" Test basique sur le sampler. """
	sampler = Sampler()
	print(f"\nSampler Print : \n{sampler}")
