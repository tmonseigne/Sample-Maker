""" Tests pour la génération de pattern """

from Utils import print_error, print_warning


##################################################
def test_print_error():
	"""
	Test de la fonction print error.
	"""

	print_error("Message d'erreur"), "L'affichage n'a pas pu être effectué"


##################################################
def test_print_warning():
	"""
	Test de la fonction print warning.
	"""

	print_warning("Message d'avertissement"), "L'affichage n'a pas pu être effectué"
