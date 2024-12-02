SampleMaker API Documentation
==============================

SampleMaker : Un générateur d'images synthétiques pour des simulations en microscopie.

Ce package fournit une infrastructure complète pour générer des images artificielles basées sur des paramètres configurables,
incluant les caractéristiques des fluorophores, les modèles de bruit, et les patterns de distribution.

**Modules principaux** :

- `Fluorophore` : Gère les propriétés optiques des fluorophores simulés.
- `Generator` : Contient les outils pour créer des images synthétiques, y compris le bruit (Noiser), l'échantillonnage (Sampler), et la gestion des piles (Stacker, StackModel).
- `Mask` : Gère les masques appliqués aux images pour structurer la répartition des molécules.
- `Pattern` : Définit les motifs de répartition des molécules.
- `Tools` : Fournit des outils utilitaires pour la gestion des fichiers, la surveillance des ressources, et d'autres fonctions génériques.

**Fonctionnalités principales** :

- Configuration flexible des paramètres via une interface utilisateur ou des scripts Python.
- Génération d'images réalistes avec des options avancées pour le bruit, les patterns, et les structures optiques.
- Compatible avec les workflows d'analyse et de traitement en microscopie.

**Importation** :

Les composants peuvent être importés directement selon les besoins, par exemple :

.. code-block:: python

	from SampleMaker import Fluorophore, Generator


.. toctree::
   :maxdepth: 2

   SampleMaker.Generator
   SampleMaker.Tools

.. toctree::
   :maxdepth: 1

   SampleMaker.Fluorophore
   SampleMaker.Mask
   SampleMaker.Pattern
   SampleMaker.Stack
