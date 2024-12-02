"""
Fichier de la classe du générateur de pile d'échantillons simulés

Ce module contient la classe `Stacker`, qui est utilisée pour générer des piles d'échantillons
simulés basées sur un générateur d'échantillons (`Sampler`) et un modèle de pile (`StackModel`).

La classe permet de créer des piles 3D à partir des échantillons générés et peut être configurée
avec différents modèles pour varier la composition de la pile.

**Fonctionnalités** :

- Génération de piles d'échantillons simulés.
- Supporte l'extension avec différents types de modèles pour la pile.
- Méthodes de conversion en chaîne de caractères pour afficher les détails du générateur.

"""

from dataclasses import dataclass, field

from SampleMaker.Generator.Sampler import Sampler
from SampleMaker.Generator.StackModel import StackModel
from SampleMaker.Stack import Stack


##################################################
@dataclass
class Stacker:
	"""
	Classe permettant de générer une pile.

	Attributs :
		- **sampler (Sampler)** : Générateur de sample pré-configuré.
		- **stack_model (StackModel)** : Modèle à utiliser pour générer la pile.
	"""
	sampler: Sampler = field(default_factory=Sampler)
	stack_model: StackModel = field(default_factory=StackModel)

	# ==================================================
	# region Generate Stack
	# ==================================================
	##################################################
	def generate(self, size: int = 100) -> Stack:
		"""
		Génère une pile.

		:param size: Nombre d'éléments dans la pile.
		:return: Pile 3D définie par le sampler et le modèle du générateur.
		"""
		self.sampler.reset()
		# if self.stack_model.model == StackModelType.XXXX: return self._XXXX_model()
		# elif self.stack_model.model == StackModelType.XXXX: return self._XXXX_model()
		return self._none_model(size)

	##################################################
	def _none_model(self, size: int = 100):
		stack = Stack()
		for i in range(size): stack.add_sample(self.sampler.generate_sample())
		return stack

	# ==================================================
	# region Generate Stack
	# ==================================================

	# ==================================================
	# region IO
	# ==================================================
	##################################################
	def tostring(self) -> str:
		"""
		Retourne une chaîne de caractères correspondant aux caractéristiques du générateur.

		:return: Une description textuelle des attributs du fluorophore.
		"""
		return f"{self.stack_model}\nSampler: {self.sampler}"

	##################################################
	def __str__(self) -> str: return self.tostring()

# ==================================================
# endregion IO
# ==================================================
