""" Fichier des tests pour la classe Fluorophore """

from SampleMaker import Fluorophore, PREDEFINED_FLUOROPHORES


##################################################
def test_fluorophore():
	""" Test basique sur les fluorophores. """
	fluo = Fluorophore(wavelength=100, intensity=100, delta=100, flickering=100)

	assert fluo.wavelength == 100, "La longueur d'onde ne correspond pas."
	assert fluo.intensity == 100, "L'intensité ne correspond pas."
	assert fluo.delta == 100, "La variation d'intensité ne correspond pas."
	assert fluo.flickering == 100, "La vitesse de scintillement ne correspond pas."

	intensity = fluo.get_intensity()
	assert intensity == 100, "La récupération d'une intensité sans variation ne correspond pas."
	intensity = fluo.get_intensity(True)
	assert 0 <= intensity <= 200, "La récupération d'une intensité avec variation ne correspond pas."


##################################################
def test_predefined_fluorophores():
	""" Récupération des fluorophores prédéfinis """

	for name, fluorophore in PREDEFINED_FLUOROPHORES.items():
		print(f"\n{name}:\n{fluorophore}")
