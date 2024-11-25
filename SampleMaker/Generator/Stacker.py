""" Fichier de la classe du générateur de pile d'échantillons simulés """

from enum import Enum
from typing import Any

import numpy as np
from numpy.typing import NDArray

from dataclasses import dataclass, field
from typing import List

import numpy as np
from numpy.typing import NDArray
from scipy.stats import multivariate_normal

from SampleMaker.Fluorophore import Fluorophore
from SampleMaker.Generator.Noiser import Noiser
from SampleMaker.Generator.Sampler import Sampler
from SampleMaker.Generator.StackModel import StackModel
from SampleMaker.Mask import Mask
from SampleMaker.Stack import Stack
from SampleMaker.Tools.Utils import print_warning

MAX_INTENSITY = np.iinfo(np.uint16).max  # Pour des entiers sur 16 bits (soit 65535).

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
	def generate(self, size:int = 100) -> Stack:
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
