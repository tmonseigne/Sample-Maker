"""Fichier d'exemple de création de pattern"""

import os
from pathlib import Path

from SampleMaker import Fluorophore, Mask, Pattern, PatternType
from SampleMaker.Generator import Noiser, Sampler
from SampleMaker.Tools.FileIO import save_sample_as_png

# Gestion des dossiers
OUTPUT_DIR = Path(__file__).parent / "Output"
INPUT_DIR = Path(__file__).parent / "Input"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

##################################################
# Création d'un échantillon sans restriction

size = 256  # Taille de l'image, Cela correspond à la dimension d'un côté de l'image carrée.
mask = Mask(size, Pattern.from_pattern(PatternType.NONE))
fluorophore = Fluorophore(wavelength=600, intensity=5000, delta=10, flickering=50)
noiser = Noiser(snr=10, background=500, variation=20)
sampler = Sampler(size=size, pixel_size=160, density=0.25, astigmatism_ratio=2.0, fluorophore=fluorophore, mask=mask, noiser=noiser)
sample = sampler.generate_sample()
save_sample_as_png(sample, f"{OUTPUT_DIR}/Sample_Base.png")

##################################################
# Création d'un échantillon avec une structure et un snr faible

size = 256  # Taille de l'image, Cela correspond à la dimension d'un côté de l'image carrée.
mask = Mask(size, Pattern.from_pattern(PatternType.SQUARES, {"size": 64}))
fluorophore = Fluorophore(wavelength=600, intensity=5000, delta=10, flickering=50)
noiser = Noiser(snr=2.6, background=500, variation=20)
sampler = Sampler(size=size, pixel_size=160, density=0.25, astigmatism_ratio=2.0, fluorophore=fluorophore, mask=mask, noiser=noiser)
sample = sampler.generate_sample()
save_sample_as_png(sample, f"{OUTPUT_DIR}/Sample_Square_noisy.png", 100)  # Enregistrement de l'échantillon au format png

##################################################
# Création d'un échantillon avec une grille de PSF fixe et aucun bruit.

size = 256  # Taille de l'image, Cela correspond à la dimension d'un côté de l'image carrée.
mask = Mask(size, Pattern.from_pattern(PatternType.EXISTING_IMAGE, {"path": f"{INPUT_DIR}/PALM.png"}))
fluorophore = Fluorophore(wavelength=600, intensity=5000, delta=10, flickering=50)
noiser = Noiser(snr=0, background=0, variation=0)
sampler = Sampler(size=size, pixel_size=160, astigmatism_ratio=2.0, fluorophore=fluorophore, noiser=noiser)
sample = sampler.generate_sample()
save_sample_as_png(sample, f"{OUTPUT_DIR}/Sample_Palm.png", 100)  # Enregistrement de l'échantillon au format png

##################################################
# Création d'un échantillon avec une grille de PSF fixe et aucun bruit.

size = 128  # Taille de l'image, Cela correspond à la dimension d'un côté de l'image carrée.
fluorophore = Fluorophore(wavelength=600, intensity=5000, delta=10, flickering=50)
noiser = Noiser(snr=0, background=0, variation=0)
sampler = Sampler(size=size, pixel_size=160, astigmatism_ratio=2.0, fluorophore=fluorophore, noiser=noiser)
sample = sampler.generate_grid()
save_sample_as_png(sample, f"{OUTPUT_DIR}/Sample_Grid.png", 100)  # Enregistrement de l'échantillon au format png
