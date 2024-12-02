""" Fichier de fonctions génériques """

from datetime import datetime

import numpy as np
from colorama import Fore, Style
from numpy.typing import NDArray


# ==================================================
# region File Management
# ==================================================
##################################################
def add_extension(filename: str, extension: str) -> str:
	"""
	Ajoute l'extension au fichier si ce n'est pas déjà l'extension actuelle

	:param filename: Nom du fichier
	:param extension: Extension finale du fichier
	"""
	if not extension.startswith('.'): extension = '.' + extension  # S'assurer que l'extension commence par un point
	if not filename.endswith(extension): filename += extension  # Si le fichier n'a pas déjà l'extension, on l'ajoute
	return filename


##################################################
def add_suffix(filename: str, suffix: str) -> str:
	"""
	Ajoute un suffixe à un nom de fichier (gère la possibilité d'une extension ou non au nom de fichier).

	:param filename: Nom de fichier d'origine.
	:param suffix: Suffixe à ajouter.
	:return: Nom de fichier avec l'horodatage ajouté.
	"""
	# Insérer le suffixe avant l'extension du fichier s'il y en a une
	if "." in filename:
		name, ext = filename.rsplit(".", 1)
		return f"{name}{suffix}.{ext}"
	return f"{filename}{suffix}"


##################################################
def get_timestamp_for_files(with_hour: bool = True) -> str:
	"""
	Créé un horodatage au format -AAAAMMJJ_HHMMSS pour un nom de fichier.

	:param with_hour: Ajoute ou non l'heure au timestamp
	:return: Horodatage.
	"""
	if with_hour: return datetime.now().strftime("-%Y%m%d_%H%M%S")  # Formater la date et l'heure
	return datetime.now().strftime("-%Y%m%d")  # Formater la date


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
