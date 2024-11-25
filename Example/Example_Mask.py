"""Fichier d'exemple de création de pattern"""

import os
from pathlib import Path

from SampleMaker.Mask import Mask
from SampleMaker.Pattern import Pattern, PatternType

# Gestion des dossiers
INPUT_DIR = Path(__file__).parent / "Input"
OUTPUT_DIR = Path(__file__).parent / "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

##################################################
# Création d'un masque de type bande comme en radiologie pour déterminer la résolution de systèmes d'imagerie à rayons X
# Sprawls P (1995) Physical Principles of Medical Imaging: Medical Physics Publishing Corporation.
print("Génération d'un masque type bande.")
size = 256							 # Taille de l'image
lengths = [200, 100, 50, 25, 12, 6]  # Largeur des bandes
mirror = True						 # On définit l'option miroir pour que les bandes soient dessinées de façon décroissante puis croissante
orientation = True					 # On définit l'orientation à true pour avoir des bandes verticales
options = {"lengths": lengths, "mirror": mirror, "orientation": orientation}  # Création du dictionnaire d'options
mask = Mask(size, Pattern.from_pattern(PatternType.STRIPES, options))		  # Génération du masque
mask.save(f"{OUTPUT_DIR}/Mask_Radio.png")									  # Enregistrement du masque au format png

##################################################
# Création d'un masque de type carré afin de créer 4 spots dans notre masque
print("Génération d'un masque type carré.")
size = 256															   # Taille de l'image
options = {"size": 64}												   # Image avec des carrés de 32 pixels
mask = Mask(size, Pattern.from_pattern(PatternType.SQUARES, options))  # Génération du masque
mask.save(f"{OUTPUT_DIR}/Mask_Square.png")							   # Enregistrement du masque au format png

##################################################
# Création d'un masque de type Soleil afin d'alterner des triangles blanc et noir.
print("Génération d'un masque type soleil.")
size = 256														   # Taille de l'image
options = {"ray_count": 16}										   # Image avec 16 rayons
mask = Mask(size, Pattern.from_pattern(PatternType.SUN, options))  # Génération du masque
mask.save(f"{OUTPUT_DIR}/Mask_Sun.png")							   # Enregistrement du masque au format png

##################################################
# Création d'un masque à partir d'une image existante.
print("Génération d'un masque type image existante.")
size = 256																	  # Taille de l'image
options = {"path": f"{INPUT_DIR}/PALM.png"}									  # Chemin vers le fichier
mask = Mask(size, Pattern.from_pattern(PatternType.EXISTING_IMAGE, options))  # Génération du masque
mask.save(f"{OUTPUT_DIR}/Mask_Existing.png")								  # Enregistrement du masque au format png

##################################################
# Création d'un masque blanc (passe-tout)
print("Génération d'un masque blanc.")
size = 256												   # Taille de l'image
mask = Mask(size, Pattern.from_pattern(PatternType.NONE))  # Génération du masque
mask.save(f"{OUTPUT_DIR}/Mask_Blank.png")				   # Enregistrement du masque au format png

print("Fini")
