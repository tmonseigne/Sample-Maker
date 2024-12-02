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

# Exemple d'importation des modules pour un accès direct
#from .Utils import add_extension, add_grid, add_suffix, get_timestamp_for_files, print_error, print_warning
#from .Decorators import reset_on_change

# Définir la liste des symboles exportés
__all__ = ["Noiser", "Sampler", "Stacker", "StackModel"]