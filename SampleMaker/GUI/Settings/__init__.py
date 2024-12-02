"""
Ce sous-module gère les paramètres de configuration et l'interface utilisateur de ces paramètres pour le projet SampleMaker.

**Composants principaux** :

- `Settings` : Classe principale pour la gestion des paramètres du générateur, incluant le parsing, l'enregistrement et la génération des objets associés.
- `UI` : Ensemble de classes et d'outils pour créer et manipuler les éléments de l'interface utilisateur, tels que les paramètres ajustables.

**Fonctionnalités principales** :

- Permet un accès direct aux classes principales via `from SampleMaker.GUI.Settings import <classe>`.
- Tous les modules peuvent être importés directement via `from SampleMaker.GUI.Settings import <module>`.

"""

# Importation explicite des classes pour qu'elles soient accessibles directement
from .Settings import Settings

# Définir la liste des symboles exportés
__all__ = ["Settings", "UI"]
