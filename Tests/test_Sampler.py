""" Tests pour la génération de pattern """

import os
from pathlib import Path

from SampleMaker.FileIO import save_sample_as_png
from SampleMaker.Mask import Mask
from SampleMaker.Pattern import Pattern, PatternType
from SampleMaker.Sampler import Sampler

INPUT_DIR = Path(__file__).parent / "Input"
OUTPUT_DIR = Path(__file__).parent / "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)
SIZE = 256


##################################################
def test_sampler():
	""" Test basique sur le sampler. """
	sampler = Sampler()
	sample = sampler.generate_sample()
	save_sample_as_png(sample, f"{OUTPUT_DIR}/test_sampler_base.png")
	sample = sampler.generate_grid()
	save_sample_as_png(sample, f"{OUTPUT_DIR}/test_sampler_grid.png")
	print(f"\nSampler Print : \n{sampler}")
	print(f"Molecules générated : {sampler.n_molecules}")


##################################################
def test_sampler_masked():
	sampler = Sampler(mask=Mask(SIZE, Pattern.from_pattern(PatternType.STRIPES)))
	sample = sampler.generate_sample()
	save_sample_as_png(sample, f"{OUTPUT_DIR}/test_sampler_stripes.png")
	sampler = Sampler(mask=Mask(SIZE, Pattern.from_pattern(PatternType.SQUARES)))
	sample = sampler.generate_sample()
	save_sample_as_png(sample, f"{OUTPUT_DIR}/test_sampler_squares.png")
