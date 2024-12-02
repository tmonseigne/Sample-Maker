""" Fichier des tests pour la classe Stack """

import os
from pathlib import Path

import numpy as np
import pytest

from SampleMaker import Stack

INPUT_DIR = Path(__file__).parent / "Input"
OUTPUT_DIR = Path(__file__).parent / "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)
SIZE = 256


##################################################
def test_stack():
	""" Test basique sur la classe. """
	# Initialisation de la classe
	stack = Stack()
	print(f"\n{stack}")  # Affiche "La pile est vide ou non initialisée."

	# Création d'échantillons
	sample1 = np.ones((2, 2)).astype(np.float32)
	sample2 = np.ones((2, 2)).astype(np.float32) * 2

	# Ajout des échantillons
	stack.add_sample(sample1)  # Premier échantillon
	stack.add_sample(sample2)  # Deuxième échantillon ajouté à la fin (car indice <0)

	print(stack)  # Affiche Pile 3D : (2, 2, 2) Contenu : [[1, 1, 1, 1], [2, 2, 2, 2]]


##################################################
def test_stack_setter_getter():
	""" Test sur l'ajout et la récupération de sample. """
	# Initialisation de la classe
	stack = Stack()

	# Création d'échantillons
	sample1 = np.ones((2, 2)).astype(np.float32)
	sample2 = np.ones((2, 2)).astype(np.float32) * 2
	sample3 = np.ones((2, 2)).astype(np.float32) * 3
	sample4 = np.ones((2, 2)).astype(np.float32) * 4

	# Ajout des échantillons
	stack.add_sample(sample1)			 # Premier échantillon
	stack.add_sample(sample2, -1)		 # Deuxième échantillon ajouté à la fin (car indice <0)
	stack.add_sample(sample3, index=42)  # Troisième échantillon ajouté à la fin (car indice trop élevé)
	stack.add_sample(sample4, index=0)   # Remplace le premier échantillon

	print(f"\n{stack}")  # Affiche Pile 3D : (3, 2, 2) Contenu : [[4, 4, 4, 4], [2, 2, 2, 2], [3, 3, 3, 3]]

	# Ajoute un mauvais échantillon
	bad = np.ones((5, 5)).astype(np.float32)
	with pytest.raises(ValueError) as exception_info: stack.add_sample(bad)
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."

	bad = np.ones(5).astype(np.float32)
	with pytest.raises(ValueError) as exception_info: stack.add_sample(bad)
	assert exception_info.type == ValueError, "L'erreur relevé n'est pas correcte."

	# récupère un échantillon
	sample = stack.get_sample(0)
	assert np.allclose(sample, sample4, atol=1e-5), "L'échantillon devrait correspondre à la référence avec une tolérance d'erreur."
	with pytest.raises(IndexError) as exception_info: stack.get_sample(-1)
	assert exception_info.type == IndexError, "L'erreur relevé n'est pas correcte."
	with pytest.raises(IndexError) as exception_info: stack.get_sample(42)
	assert exception_info.type == IndexError, "L'erreur relevé n'est pas correcte."


##################################################
def test_stack_save():
	""" Test sur l'enregistrement d'une pile. """
	# Initialisation de la classe
	stack = Stack()
	stack.add_sample(np.zeros((2, 2)).astype(np.float32))
	stack.add_sample(np.ones((2, 2)).astype(np.float32))
	stack.save(f"{OUTPUT_DIR}/test_stack.tif")


##################################################
def test_stack_open():
	""" Test sur l'enregistrement d'une pile. """
	# Initialisation de la classe
	stack = Stack()
	stack.open(f"{OUTPUT_DIR}/test_stack.tif")
	ref = Stack()
	ref.add_sample(np.zeros((2, 2)).astype(np.float32))
	ref.add_sample(np.ones((2, 2)).astype(np.float32))
	assert np.allclose(ref.stack, stack.stack, atol=1), "La pile devrait correspondre à la référence avec une tolérance d'erreur."


##################################################
def test_stack_open_bad_file():
	""" Test sur l'enregistrement d'une pile avec un fichier inexistant. """
	stack = Stack()
	with pytest.raises(OSError) as exception_info:
		stack.open("bad_filename.tif")
	assert exception_info.type == OSError, "L'erreur relevé n'est pas correcte."
