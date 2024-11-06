import numpy as np
from enum import Enum

##################################################
class Pattern(Enum):
    STRIPES = 1
    SQUARES = 2
    SUN = 3
    EXISTING_IMAGE = 4

    def to_string(self):
        return {
                Pattern.STRIPES:        "Bandes",
                Pattern.SQUARES:        "Carrés",
                Pattern.SUN:            "Soleil 3D",
                Pattern.EXISTING_IMAGE: "Image existante"
                }[self]

##################################################
def generate_mask(pattern, size, options):
    print(f"Generation d'un masque selon la sélection : {pattern.to_string()}")
    # Création de l'image selon le motif
    if pattern == Pattern.STRIPES: return stripes_mask(size, options)
    if pattern == Pattern.SQUARES: return squares_mask(size, options)
    if pattern == Pattern.SUN: return sun_mask(size, options)
    if pattern == Pattern.EXISTING_IMAGE: return load_mask(size, options)


##################################################
def stripes_mask(size, options):
    print("")
    return np.ndarray(size)

##################################################
def squares_mask(size, options):
    return np.ndarray(size)

##################################################
def sun_mask(size, options):
    return np.ndarray(size)

##################################################
def load_mask(size, options):
    return np.ndarray(size)
