""" Fonctions génériques """

import numpy as np
from colorama import Fore, Style
from numpy.typing import NDArray


# ==================================================
# region File Management
# # ==================================================
##################################################
def clean_extension(filename: str, extension: str):
	"""
	Ajoute l'extension au fichier si ce n'est pas déjà l'extension actuelle

	:param filename: Nom du fichier
	:param extension: Extension finale du fichier

	.. todo:: Fonction actuellement vide.
	"""
	print("TODO")


# ==================================================
# endregion File Management
# ==================================================


# ==================================================
# region Prints
# ==================================================
##################################################
def print_error(msg: str):
	"""
	Affiche un message avec une couleur rouge

	:param msg: message à afficher
	"""
	print(Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)


##################################################
def print_warning(msg: str):
	"""
	Affiche un message avec une couleur jaune

	:param msg: message à afficher
	"""
	print(Fore.YELLOW + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL)


# ==================================================
# endregion Prints
# ==================================================


# ==================================================
# region Drawing
# ==================================================
##################################################
def add_grid(image: NDArray[np.float32], size_x: int = 10, size_y: int = 10, color: int = 255) -> NDArray[np.float32]:
	"""
	Ajoute une grille sur l'image

	:param image: L'image d'entrée (en valeurs de pixels).
	:param size_x: Espacement de la grille sur X (par défaut 10).
	:param size_y: Espacement de la grille sur Y (par défaut 10).
	:param color: Couleur de la grille (par défaut 255, blanc).
	:return: L'image avec une grille.

	.. note:: Par principe cette fonction sera utilisée plus tard sur une image RVB ou pour un calque d'affichage
	"""

	grid = image
	size = grid.shape[0]
	coord_x = np.arange(size_x, size, size_x)
	coord_y = np.arange(size_y, size, size_y)
	grid[coord_y, :] = color
	grid[:, coord_x] = color

	return grid

# ==================================================
# endregion Drawing
# ==================================================
