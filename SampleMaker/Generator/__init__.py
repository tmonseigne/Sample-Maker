"""
Ce sous-package contient des outils pour la génération d'images et de données dans le projet SampleMaker.

**Modules disponibles** :

- Noiser : Permet d'ajouter du bruit gaussien et poissonien à des images pour simuler des conditions réalistes.
- Sampler : Fournit des outils pour échantillonner et générer des images à partir de données.
- Stacker : Fournit des fonctions pour empiler plusieurs images ou données dans une structure plus complexe.
- StackModel : Modélise et génère des empilements d'images ou de données, souvent utilisés pour des simulations ou des analyses multidimensionnelles.

**Fonctionnalités principales** :

- Tous les modules peuvent être importés directement via `from SampleMaker.Generator import <module>`.

"""

# Importation explicite des classes pour qu'elles soient accessibles directement
from .Noiser import Noiser
from .Sampler import Sampler
from .Stacker import Stacker
from .StackModel import StackModel, StackModelType, NoneOptions

# Définir la liste des symboles exportés
__all__ = ["Noiser", "Sampler", "Stacker", "StackModel", "StackModelType", "NoneOptions"]