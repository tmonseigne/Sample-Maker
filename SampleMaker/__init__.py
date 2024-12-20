"""
SampleMaker : Un générateur d'images synthétiques pour des simulations en microscopie.

Ce package fournit une infrastructure complète pour générer des images artificielles basées sur des paramètres configurables,
incluant les caractéristiques des fluorophores, les modèles de bruit, et les patterns de distribution.

**Modules principaux** :

- `Fluorophore` : Gère les propriétés optiques des fluorophores simulés.
- `Generator` : Contient les outils pour créer des images synthétiques, y compris le bruit (Noiser), l'échantillonnage (Sampler), et la gestion des piles (
Stacker, StackModel).
- `GUI` : Fournit une interface utilisateur pour configurer et gérer les paramètres.
- `Mask` : Gère les masques appliqués aux images pour structurer la répartition des molécules.
- `Pattern` : Définit les motifs de répartition des molécules.
- `Tools` : Fournit des outils utilitaires pour la gestion des fichiers, la surveillance des ressources, et d'autres fonctions génériques.

**Fonctionnalités principales** :

- Configuration flexible des paramètres via une interface utilisateur ou des scripts Python.
- Génération d'images réalistes avec des options avancées pour le bruit, les patterns, et les structures optiques.
- Compatible avec les workflows d'analyse et de traitement en microscopie.

**Importation** :

Les composants peuvent être importés directement selon les besoins, par exemple :
```python
from SampleMaker import Fluorophore, Generator
```

"""

# Importation explicite des classes pour qu'elles soient accessibles directement
from .Fluorophore import Fluorophore, PREDEFINED_FLUOROPHORES
from .Mask import Mask
from .Pattern import Pattern, PatternType, ExistingImageOptions, NoneOptions, SquaresOptions, StripesOptions, SunOptions
from .Stack import Stack

# Définir la liste des symboles exportés
__all__ = ["Generator", "GUI", "Tools", "Fluorophore", "PREDEFINED_FLUOROPHORES", "Mask", "Pattern", "PatternType", "Stack",
		   "ExistingImageOptions", "NoneOptions", "SquaresOptions", "StripesOptions", "SunOptions"]
