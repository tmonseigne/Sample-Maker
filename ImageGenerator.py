""" Fonctions de génération d'images Simulées """

import math
import os
from enum import Enum
from itertools import accumulate
from typing import Any

import numpy as np
from numpy.typing import NDArray

from FileIO import open_png_as_boolean_mask
from PatternGenerator import Pattern
from Utils import print_warning


##################################################
def generate_sample(size: int = 256, pixel_size: int = 160, density: float = 1.0, snr: float = 10.0, pattern=Pattern.NONE):
	print("TODO")


##################################################
def compute_molecule_number(size: int = 256, pixel_size: int = 160, density: float = 1.0) -> int:
	"""
	Calcule le nombre estimé de molécules dans une image carrée en fonction de sa taille, de la taille d'un pixel et de la densité de molécules.

	Cette fonction est utile pour estimer la quantité totale de molécules dans une région d'image en fonction de paramètres physiques.

	:param size: Taille de l'image en pixels (par défaut : 256). Cela correspond à la dimension d'un côté de l'image carrée.
	:param pixel_size: Taille d'un pixel en nanomètres (par défaut : 160). Utilisé pour calculer la surface de l'image.
	:param density: Densité de molécules par micromètre carré (par défaut 1.0).
	:return: Nombre estimé de molécules dans l'image.
	"""
	im_size = float(size * pixel_size) / 1000  # Calculer la taille de l'image en micromètres (conversion depuis la taille des pixels en nanomètres
	im_area = im_size ** 2  				   # Calculer l'aire de l'image en micromètres carrés
	molecule_number = int(im_area * density)   # Calculer le nombre de molécules en fonction de la densité
	return molecule_number


##################################################
def molecule_localisation_map(size: int = 256, pixel_size: int = 160, density: float = 1.0, pattern=Pattern.NONE):
	print("TODO")


##################################################
def add_psf(image):
	print("TODO")


##################################################
def add_snr(image, snr: float = 10.0):
	print("TODO")

