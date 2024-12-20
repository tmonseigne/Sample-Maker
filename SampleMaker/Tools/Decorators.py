"""
Fichier de décorateurs personnalisés.

Ce module contient un décorateur utilitaire pour étendre le comportement des classes Python.
Il permet d'automatiser certaines tâches, comme l'appel d'une méthode lors de la modification d'un attribut spécifique.

**Fonctionnalités** :

1. **`reset_on_change`**

   - Décorateur conçu pour déclencher automatiquement une méthode `reset` lors du changement d'un attribut.
   - Il crée un getter et un setter pour un attribut donné, avec la logique d'appel de la méthode `reset` lorsque le setter est invoqué.
"""


##################################################
def reset_on_change(attribute_name: str):
	"""
	    Décorateur permettant de déclencher automatiquement une méthode `reset` lors du changement d'un attribut spécifique.

	    Ce décorateur ajoute un getter et un setter pour un attribut donné. Lorsqu'une nouvelle valeur est assignée à cet attribut,
	    la méthode `reset` de la classe est appelée automatiquement.

	    :param attribute_name: Nom de l'attribut pour lequel le comportement doit être modifié.
	                           Cet attribut doit exister dans la classe sous une forme privée (préfixée par un underscore, par ex. `_nom_attribut`).
	    :return: La classe modifiée avec un getter et un setter pour l'attribut spécifié.
	    """

	def decorator(cls):
		private_name = f"_{attribute_name}"

		@property
		def prop(self):
			return getattr(self, private_name)

		@prop.setter
		def prop(self, value):
			setattr(self, private_name, value)
			self.reset()

		setattr(cls, attribute_name, prop)
		return cls

	return decorator
