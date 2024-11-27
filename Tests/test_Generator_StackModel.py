""" Fichier des tests pour le Stacker : le générateur de pile d'échantillons """

from SampleMaker.Generator.StackModel import StackModel, StackModelType


##################################################
def test_stack_model_type():
	""" Test de l'objet StackModelType. """

	assert StackModelType.NONE.tostring() == "None", "La chaine de caractère ne correspond pas pour le pattern None"


##################################################
def test_pattern():
	""" Test de l'objet Pattern. """

	print()
	model = StackModel.from_model(StackModelType.NONE, None)
	assert model.model == StackModelType.NONE, "Ce n'est pas le bon type de pattern"
	print(model)
