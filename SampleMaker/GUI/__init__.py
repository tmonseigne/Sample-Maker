"""
Ce sous-module gère l'interface utilisateur pour le projet SampleMaker.

**Fonctionnalités principales** :

- Permet un accès direct aux classes principales via `from SampleMaker.GUI import <classe>`.
- Tous les modules peuvent être importés directement via `from SampleMaker.GUI import <module>`.

"""

# Importation explicite des classes pour qu'elles soient accessibles directement
from .MainUI import MainUI

# Définir la liste des symboles exportés
__all__ = ["Settings", "MainUI"]
