"""Fichier d'exemple de création de pattern"""

import os
from pathlib import Path

from FileIO import save_sample_as_png
from PatternGenerator import Pattern
from SampleGenerator import add_snr, compute_molecule_grid, compute_psf, generate_sample

# Gestion des dossiers
OUTPUT_DIR = Path(__file__).parent / "Output"
INPUT_DIR = Path(__file__).parent / "Input"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)


##################################################
# Création d'un échantillon sans restriction

size = 256				# Taille de l'image, Cela correspond à la dimension d'un côté de l'image carrée.
pixel_size = 160		# Taille d'un pixel en nanomètres.
density = 0.25			# Densité de molécules par micromètre carré.
pattern = Pattern.NONE  # Aucun motif à utiliser pour générer le masque
pattern_options = None  # Aucune option pour ce motif
intensity = 5000		# Intensité de base du fluorophore.
variation = 500			# Variation d'intensité du fluorophore.
astigmatism_ratio = 2   # Ratio de l'astigmatisme.
snr = 10				# Le rapport signal sur bruit désiré.

sample = generate_sample(size, pixel_size, density, pattern, pattern_options, intensity, variation, astigmatism_ratio, snr)
save_sample_as_png(sample, f"{OUTPUT_DIR}/Sample_Base.png", 100)  # Enregistrement de l'échantillon au format png

##################################################
# Création d'un échantillon avec une structure et un snr faible

size = 256					   # Taille de l'image, Cela correspond à la dimension d'un côté de l'image carrée.
pixel_size = 160			   # Taille d'un pixel en nanomètres.
density = 0.25				   # Densité de molécules par micromètre carré.
pattern = Pattern.SQUARES	   # Aucun motif à utiliser pour générer le masque
pattern_options ={"Size": 64}  # Aucune option pour ce motif
intensity = 5000			   # Intensité de base du fluorophore.
variation = 500				   # Variation d'intensité du fluorophore.
astigmatism_ratio = 2   	   # Ratio de l'astigmatisme.
snr = 2.6					   # Le rapport signal sur bruit désiré.

sample = generate_sample(size, pixel_size, density, pattern, pattern_options, intensity, variation, astigmatism_ratio, snr)
save_sample_as_png(sample, f"{OUTPUT_DIR}/Sample_Square_noisy.png", 100)  # Enregistrement de l'échantillon au format png

##################################################
# Création d'un échantillon avec une molécule toutes les N cases.

size = 256					   # Taille de l'image, Cela correspond à la dimension d'un côté de l'image carrée.
pixel_size = 160			   # Taille d'un pixel en nanomètres.
density = 0.25				   # Densité de molécules par micromètre carré.
pattern = Pattern.SQUARES	   # Aucun motif à utiliser pour générer le masque
pattern_options ={"Size": 64}  # Aucune option pour ce motif
intensity = 5000			   # Intensité de base du fluorophore.
variation = 500				   # Variation d'intensité du fluorophore.
astigmatism_ratio = 2   	   # Ratio de l'astigmatisme.
snr = 2.6					   # Le rapport signal sur bruit désiré.

sample = generate_sample(size, pixel_size, density, pattern, pattern_options, intensity, variation, astigmatism_ratio, snr)
save_sample_as_png(sample, f"{OUTPUT_DIR}/Sample_Square_noisy.png", 100)  # Enregistrement de l'échantillon au format png

##################################################
# Création d'un échantillon avec une grille de PSF fixe.

size = 128					   # Taille de l'image, Cela correspond à la dimension d'un côté de l'image carrée.
shift = 20					   # Espacement en pixel entre les molécules (ou plus simplement chaque molécule est au centre d'un carré de taille shift).
intensity = 5000			   # Intensité de base du fluorophore.
variation = 500				   # Variation d'intensité du fluorophore.
astigmatism_ratio = 2   	   # Ratio de l'astigmatisme.
snr = 10					   # Le rapport signal sur bruit désiré.

localisation = compute_molecule_grid(size, shift)
sample = compute_psf(size, localisation, intensity, variation, astigmatism_ratio)
sample = add_snr(sample, snr)
save_sample_as_png(sample, f"{OUTPUT_DIR}/Sample_Grid.png", 100)  # Enregistrement de l'échantillon au format png

