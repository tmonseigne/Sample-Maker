""" Fonctions génériques """

from colorama import Fore, Style


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
