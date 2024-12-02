"""
Ce sous-package contient des outils utilitaires pour le projet SampleMaker.

**Modules disponibles** :

- Decorators : Fournit des décorateurs personnalisés.
- Drawing : Fournit des fonctions de dessin génériques.
- FileIO : Fournit des fonctions de manipulation de fichiers génériques.
- Monitoring : Fournit un module de surveillance des ressources système pendant l'exécution de tests.
- Utils : Fournit des fonctions d'assistance génériques.

**Fonctionnalités principales** :

- Tous les modules peuvent être importés directement via `from SampleMaker.Tools import <module>`.

"""

# Exemple d'importation des modules pour un accès direct
from .Drawing import draw_test_section, get_color_map_by_name
from .FileIO import open_png_as_boolean_mask, open_png_as_sample, open_tif_as_stack, save_boolean_mask_as_png, save_sample_as_png, save_stack_as_tif
from .Monitoring import Monitoring
from .Utils import add_extension, add_grid, add_suffix, get_timestamp_for_files, print_error, print_warning

# Définir la liste des symboles exportés
__all__ = ["Decorators", "Drawing", "FileIO", "Monitoring", "Utils",
		   "draw_test_section", "get_color_map_by_name",
		   "open_png_as_boolean_mask", "open_png_as_sample", "open_tif_as_stack",
		   "save_boolean_mask_as_png","save_sample_as_png","save_stack_as_tif",
		   "add_extension", "add_grid", "add_suffix", "get_timestamp_for_files", "print_error", "print_warning"]
