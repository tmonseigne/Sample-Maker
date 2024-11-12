"""Fichier d'exemple de création de pattern"""

import os
from pathlib import Path

from FileIO import save_boolean_mask_as_png
from PatternGenerator import generate_mask, Pattern

# Gestion des dossiers
OUTPUT_DIR = Path(__file__).parent / "Output"
INPUT_DIR = Path(__file__).parent / "Input"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

##################################################
# Création d'un masque de type bande comme en radiologie pour déterminer la résolution de systèmes d'imagerie à rayons X
# Sprawls P (1995) Physical Principles of Medical Imaging: Medical Physics Publishing Corporation.
size = 256							 # Taille de l'image
lengths = [200, 100, 50, 25, 12, 6]  # Largeur des bandes
mirror = True						 # On définit l'option miroir pour que les bandes soient déssinée de façon décroissante puis croissante
oriantation = True					 # On définit l'oriantation à true pour avoir des bandes verticales
options = {"Lengths": lengths, "Mirrored": mirror, "Orientation": oriantation}  # Création du dictionnaire d'options
mask = generate_mask(Pattern.STRIPES, size, options)							# Génération du masque
save_boolean_mask_as_png(mask, f"{OUTPUT_DIR}/Radio_mask.png")					# Enregistrement du masque au format png


##################################################
# Création d'un masque de type carré afin de créer 4 spots dans notre masque
size = 256														 # Taille de l'image
options = {"Size": 64}											 # Image avec des carrés de 32 pixels
mask = generate_mask(Pattern.SQUARES, size, options)			 # Génération du masque
save_boolean_mask_as_png(mask, f"{OUTPUT_DIR}/Square_mask.png")  # Enregistrement du masque au format png


##################################################
# Création d'un masque de type SOleil afin d'alterner des triangles blanc et noir.
size = 256													  # Taille de l'image
options = {"Rays": 16}										  # Image avec 16 rayons
mask = generate_mask(Pattern.SUN, size, options)			  # Génération du masque
save_boolean_mask_as_png(mask, f"{OUTPUT_DIR}/Sun_mask.png")  # Enregistrement du masque au format png


##################################################
# Création d'un masque à partir d'une image existante.
size = 256														   # Taille de l'image
options = {"Filename": f"{INPUT_DIR}/PALM.png"}					   # Chemin vers le fichier
mask = generate_mask(Pattern.EXISTING_IMAGE, size, options)		   # Génération du masque
save_boolean_mask_as_png(mask, f"{OUTPUT_DIR}/Existing_mask.png")  # Enregistrement du masque au format png


##################################################
# Création d'un masque blanc (passe-tout)
size = 256														   # Taille de l'image
mask = generate_mask(Pattern.NONE, size)						   # Génération du masque
save_boolean_mask_as_png(mask, f"{OUTPUT_DIR}/Blank_mask.png")  # Enregistrement du masque au format png
