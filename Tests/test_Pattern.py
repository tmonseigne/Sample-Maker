""" Fichier des tests pour la génération de pattern """

from SampleMaker import Pattern, PatternType, SquaresOptions


##################################################
def test_pattern_type():
	""" Test de l'objet PatternType. """
	assert PatternType.NONE.tostring() == "None", "La chaine de caractère ne correspond pas pour le pattern None"
	assert PatternType.STRIPES.tostring() == "Bandes", "La chaine de caractère ne correspond pas pour le pattern Bandes"
	assert PatternType.SQUARES.tostring() == "Carrés", "La chaine de caractère ne correspond pas pour le pattern Carrés"
	assert PatternType.SUN.tostring() == "Soleil", "La chaine de caractère ne correspond pas pour le pattern Soleil"
	assert PatternType.EXISTING_IMAGE.tostring() == "Image existante", "La chaine de caractère ne correspond pas pour le pattern Image existante"


##################################################
def test_pattern():
	""" Test de l'objet Pattern. """
	pattern = Pattern.from_pattern(PatternType.NONE, None)
	assert pattern.pattern == PatternType.NONE, "Ce n'est pas le bon type de pattern"
	print(pattern)

	pattern = Pattern.from_pattern(PatternType.STRIPES, {"lengths": [200, 100, 50, 25, 12, 6], "mirror": True, 'orientation': True})
	assert pattern.pattern == PatternType.STRIPES, "Ce n'est pas le bon type de pattern."
	print(pattern)

	pattern = Pattern.from_pattern(PatternType.SQUARES, None)  # Si aucune option, il va prendre celles par défaut
	assert pattern.pattern == PatternType.SQUARES, "Ce n'est pas le bon type de pattern."
	assert pattern.options.size == SquaresOptions.size, "Ce n'est pas la taille par défaut du motif."
	print(pattern)

	pattern = Pattern.from_pattern(PatternType.SUN, {"ray_count": 8})
	assert pattern.pattern == PatternType.SUN, "Ce n'est pas le bon type de pattern."
	assert pattern.options.ray_count == 8, "Ce n'est pas la bonne valeur pour le membre ray_count."
	print(pattern)

	pattern = Pattern.from_pattern(PatternType.EXISTING_IMAGE, {"path": ""})
	assert pattern.pattern == PatternType.EXISTING_IMAGE, "Ce n'est pas le bon type de pattern."
	print(pattern)
