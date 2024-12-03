""" Fichier des tests pour le Stacker : le générateur de pile d'échantillons """

import os
from pathlib import Path

from SampleMaker.Generator import Sampler, Stacker

INPUT_DIR = Path(__file__).parent / "Input"
OUTPUT_DIR = Path(__file__).parent / "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

SAMPLER = Sampler(size=128)


##################################################
def test_stacker():
	""" Test basique sur le générateur de stack. """
	stacker = Stacker(sampler=SAMPLER)
	print(f"\n{stacker}")
	stack = stacker.generate(10)
	print(stacker)
	stack.save(f"{OUTPUT_DIR}/test_stacker_base.tif")
	assert True
