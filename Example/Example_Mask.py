"""Fichier d'exemple de création de pattern"""

import os
from pathlib import Path

from SampleMaker.FileIO import save_boolean_mask_as_png
from SampleMaker.Mask import Mask
from SampleMaker.Pattern import Pattern, PatternType

# Gestion des dossiers
INPUT_DIR = Path(__file__).parent / "Input"
OUTPUT_DIR = Path(__file__).parent / "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

##################################################
# Création d'un masque de type bande comme en radiologie pour déterminer la résolution de systèmes d'imagerie à rayons X
# Sprawls P (1995) Physical Principles of Medical Imaging: Medical Physics Publishing Corporation.
size = 256							 # Taille de l'image
lengths = [200, 100, 50, 25, 12, 6]  # Largeur des bandes
mirror = True						 # On définit l'option miroir pour que les bandes soient dessinées de façon décroissante puis croissante
orientation = True					 # On définit l'oriantation à true pour avoir des bandes verticales
options = {"lengths": lengths, "mirror": mirror, "orientation": orientation}  # Création du dictionnaire d'options
mask = Mask(size, Pattern.from_pattern(PatternType.STRIPES, options))
mask.save(f"{OUTPUT_DIR}/Mask_Radio.png")					# Enregistrement du masque au format png


##################################################
# Création d'un masque de type carré afin de créer 4 spots dans notre masque
size = 256														 # Taille de l'image
options = {"Size": 64}											 # Image avec des carrés de 32 pixels
mask = generate_mask(MaskPattern.SQUARES, size, options)			 # Génération du masque
save_boolean_mask_as_png(mask, f"{OUTPUT_DIR}/Mask_Square.png")  # Enregistrement du masque au format png


##################################################
# Création d'un masque de type Soleil afin d'alterner des triangles blanc et noir.
size = 256													  # Taille de l'image
options = {"Rays": 16}										  # Image avec 16 rayons
mask = generate_mask(MaskPattern.SUN, size, options)			  # Génération du masque
save_boolean_mask_as_png(mask, f"{OUTPUT_DIR}/Mask_Sun.png")  # Enregistrement du masque au format png


##################################################
# Création d'un masque à partir d'une image existante.
size = 256														   # Taille de l'image
options = {"Filename": f"{INPUT_DIR}/PALM.png"}					   # Chemin vers le fichier
mask = generate_mask(MaskPattern.EXISTING_IMAGE, size, options)		   # Génération du masque
save_boolean_mask_as_png(mask, f"{OUTPUT_DIR}/Mask_Existing.png")  # Enregistrement du masque au format png


##################################################
# Création d'un masque blanc (passe-tout)
size = 256														# Taille de l'image
mask = generate_mask(MaskPattern.NONE, size)						# Génération du masque
save_boolean_mask_as_png(mask, f"{OUTPUT_DIR}/Mask_Blank.png")  # Enregistrement du masque au format png
