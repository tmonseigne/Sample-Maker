"""Fichier d'exemple de création de pattern"""

import os
from pathlib import Path

from SampleMaker.Fluorophore import Fluorophore
from SampleMaker.Generator.Noiser import Noiser
from SampleMaker.Generator.Sampler import Sampler
from SampleMaker.Generator.Stacker import Stacker
from SampleMaker.Mask import Mask
from SampleMaker.Pattern import Pattern, PatternType

# Gestion des dossiers
OUTPUT_DIR = Path(__file__).parent / "Output"
INPUT_DIR = Path(__file__).parent / "Input"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

##################################################
# Création d'une pile d'échantillons sans restriction

size = 256  # Taille de l'image, Cela correspond à la dimension d'un côté de l'image carrée.
mask = Mask(size, Pattern.from_pattern(PatternType.NONE))  # Masque vide
fluorophore = Fluorophore(wavelength=600,  # Longueur d'onde d'émission du fluorophore.
						  intensity=5000,  # Intensité de base du fluorophore.
						  delta=10,  # Variation maximale d'intensité en pourcentage.
						  flickering=50)  # Vitesse de scintillement en millisecondes.
noiser = Noiser(snr=10, background=500, variation=20)
sampler = Sampler(size=size, pixel_size=160, density=0.25, astigmatism_ratio=2.0, fluorophore=fluorophore, mask=mask, noiser=noiser)
stacker = Stacker(sampler=sampler)
stack = stacker.generate(10)
stack.save(f"{OUTPUT_DIR}/Stack_Base.tif")

##################################################
# Création d'un échantillon avec une structure et un snr faible

size = 256  # Taille de l'image, Cela correspond à la dimension d'un côté de l'image carrée.
mask = Mask(size, Pattern.from_pattern(PatternType.SQUARES, {"size": 64}))
fluorophore = Fluorophore(wavelength=600, intensity=5000, delta=10, flickering=50)
noiser = Noiser(snr=2.6, background=500, variation=10)
sampler = Sampler(size=size, pixel_size=160, density=0.25, astigmatism_ratio=2.0, _fluorophore=fluorophore, mask=mask, noiser=noiser)
stacker = Stacker(sampler=sampler)
stack = stacker.generate(10)
stack.save(f"{OUTPUT_DIR}/Stack_Square_noisy.tif")
