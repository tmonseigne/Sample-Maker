""" Fichier des tests pour le monitoring """

import os
import time
from pathlib import Path

from SampleMaker.Tools.Monitoring import Monitoring

OUTPUT_DIR = Path(__file__).parent / "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)

##################################################
def simulate_memory_usage(size:int, duration:float=10, pause: float=2):
	"""
	Simule une utilisation importante de mémoire en allouant un tableau de bytes.

	:param size: Taille totale de mémoire à allouer (en mégaoctets).
	:param duration: Temps pendant lequel la mémoire reste allouée (en secondes).
	"""
	print(f"Allocating {size} MB of memory...")
	allocated_memory = bytearray(size * 1024 * 1024)  # Alloue un tableau de bytes
	print(f"Memory allocated. Holding for {duration} seconds...")
	time.sleep(duration)  # Garde la mémoire allouée pour observer l'impact
	print("Releasing memory.")
	del allocated_memory  # Libère la mémoire
	time.sleep(pause)  # Ajoute une petite pause pour observer la libération de la mémoire

##################################################
def test_monitoring():
	""" Test basique sur la classe. """
	monitoring = Monitoring()
	monitoring.start(0.1)
	time.sleep(1)
	monitoring.stop()
	print(f"\n{monitoring}")
	assert 5 <= monitoring.n_entries <= 15, (f"On a monitoré {monitoring.n_entries} entrées. "
											 f"Il devrait y en avoir autour de 10 (approximation du au threading).")


##################################################
def test_monitoring_save():
	""" Test d'enregistrement des graphiques. """
	monitoring = Monitoring()
	monitoring.start(0.1)
	simulate_memory_usage(50, 2, 1)
	monitoring.stop()
	monitoring.draw_png(f"{OUTPUT_DIR}/test_monitoring.png")
	monitoring.draw_html(f"{OUTPUT_DIR}/test_monitoring.html")
	monitoring.save(f"{OUTPUT_DIR}/test_monitoring.txt")
