""" Fichier des tests pour le Stacker : le générateur de pile d'échantillons """

from SampleMaker.Generator import StackModel, StackModelType


##################################################
def test_stack_model_type():
	""" Test de l'objet StackModelType. """
	assert StackModelType.RANDOM.tostring() == "Aléatoire", "La chaine de caractère ne correspond pas pour le pattern None"


##################################################
def test_pattern():
	""" Test de l'objet Pattern. """
	print()
	model = StackModel.from_model(StackModelType.RANDOM, None)
	assert model.model == StackModelType.RANDOM, "Ce n'est pas le bon type de pattern"
	print(model)
