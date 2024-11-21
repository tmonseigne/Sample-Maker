""" Fichier des tests pour le monitoring """

import os
import time
from pathlib import Path

from SampleMaker.Tools.Monitoring import Monitoring

OUTPUT_DIR = Path(__file__).parent / "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Créer le dossier de sorties (la première fois, il n'existe pas)


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
	time.sleep(1)
	monitoring.stop()
	monitoring.draw_png(f"{OUTPUT_DIR}/test_monitoring.png")
	monitoring.draw_html(f"{OUTPUT_DIR}/test_monitoring.html")
