import os
import platform
import re
import threading
import time
from dataclasses import dataclass, field
from typing import List

import matplotlib.pyplot as plt
import plotly.express as px  # Pour accéder aux couleurs qualitatives
import plotly.graph_objects as go
import psutil
from plotly.subplots import make_subplots

from SampleMaker.Tools.Drawing import draw_test_section, get_color_map_by_name

MEMORY_RATIO = 1.0 / (1024 * 1024)


##################################################
@dataclass
class Monitoring:
	"""
	Classe de monitoring qui suit l'utilisation des ressources (CPU, mémoire, disque) pendant l'exécution des tests.

	Cette classe collecte les informations sur l'utilisation des ressources du système durant l'exécution des tests.
	Elle fournit des fonctionnalités pour démarrer et arrêter la surveillance, mettre à jour les valeurs des ressources,
	et générer des graphiques ou des fichiers texte avec ces données.

	Attributs :
		- **cpu (List[float])** : Liste des valeurs d'utilisation du CPU.
		- **memory (List[float])** : Liste des valeurs d'utilisation de la mémoire.
		- **disk (List[float])** : Liste des valeurs d'utilisation du disque.
		- **times (List[float])** : Liste des timestamps correspondant aux valeurs des ressources.
		- **monitoring (bool)** : Indique si la surveillance est en cours ou non.
		- **thread (threading.Thread)** : Le thread qui exécute le monitoring.
		- **tests_info (List[dict])** : Liste des informations relatives aux tests exécutés.
		- **interval (float)** : Intervalle de temps entre chaque mise à jour des données en secondes.

	"""
	cpu: List[float] = field(init=False, default_factory=list)
	# gpu: List[float] = field(init=False, default_factory=list)
	memory: List[float] = field(init=False, default_factory=list)
	disk: List[float] = field(init=False, default_factory=list)
	times: List[float] = field(init=False, default_factory=list)
	monitoring: bool = field(init=False, default=False)
	thread: threading.Thread = field(init=False, default_factory=threading.Thread)
	tests_info: List[dict] = field(init=False, default_factory=list)  # Liste des informations des tests
	interval: float = 1.0

	# ==================================================
	# region Monitoring Manipulation
	# ==================================================
	##################################################
	@property
	def n_entries(self) -> int:
		"""
		Retourne le nombre d'entrées (mesures) dans le monitoring.

		:return: Nombre d'entrées dans les listes de données.
		"""
		return len(self.times)

	##################################################
	def _reset(self):
		"""
		Réinitialise toutes les données de monitoring (CPU, mémoire, disque, etc.).
		"""
		self.cpu = []
		# self.gpu = []
		self.memory = []
		self.disk = []
		self.times = []
		self.tests_info = []
		self.monitoring = False
		self.thread = threading.Thread()

	##################################################
	def _update(self):
		"""
		Met à jour les valeurs d'utilisation du CPU, de la mémoire et du disque en fonction des processus en cours.
		"""
		# Sélection de processus
		pytest_pid = os.getpid()						 # PID de pytest
		pytest_proc = psutil.Process(pytest_pid)		 # Récupère le processus parent
		children = pytest_proc.children(recursive=True)  # Cible les processus enfants
		processes = [pytest_proc] + children			 # Inclut le processus principal et ses enfants

		self.cpu.append(sum(proc.cpu_percent(interval=self.interval) for proc in processes))
		self.memory.append(sum(proc.memory_info().rss for proc in processes))
		# "Darwin" est le nom de macOS dans platform.system()
		if platform.system() != "Darwin": self.disk.append(sum(proc.io_counters().write_bytes for proc in processes))
		else: self.disk.append(0)  # pragma: no cover
		self.times.append(time.time())

	##################################################
	def start(self, interval: float = 1.0):
		"""
		Démarre la surveillance des ressources.

		:param interval: Intervalle de mise à jour des données (en secondes).
		"""
		self._reset()
		self.interval = interval
		self.monitoring = True
		self.thread = threading.Thread(target=self.monitor)
		self.thread.start()

	##################################################
	def monitor(self):
		"""
		Surveille les ressources en continu dans un thread séparé.
		"""
		while self.monitoring:
			self._update()
			time.sleep(self.interval)

	##################################################
	def stop(self):
		"""
		Arrête la surveillance et effectue une dernière mise à jour des valeurs.
		"""
		self.monitoring = False
		self.thread.join()
		self._update()  # Dernière entrée
		self._update_array_for_readability()

	##################################################
	def add_test_info(self, name: str):
		"""
		Ajoute des informations sur un test dans la liste des tests.

		:param name: Le nom complet du test, au format "Tests/test_<file>.py::test_<test_name>".
		"""
		match = re.match(r"Tests/test_(.*)\.py::test_(.*)", name)
		if match:
			file = match.group(1).replace('_', ' ').title()  # Récupère le nom du fichier et change la casse
			test = match.group(2).replace('_', ' ').title()  # Récupère le nom du test et change la casse
			self.tests_info.append({"File": file, "Test": test, "Timestamp": time.time()})

	##################################################
	def _update_array_for_readability(self, round_time: int = 2):
		"""
		Met à jour les tableaux pour faciliter la lecture (ajustement des timestamps et normalisation).

		:param round_time: Le nombre de décimales pour arrondir les timestamps.
		"""
		first_time = self.times[0]

		for test_info in self.tests_info: test_info["Timestamp"] = round(test_info["Timestamp"] - first_time, round_time)
		self.times = [round(t - first_time, round_time) for t in self.times]

		num_cores = psutil.cpu_count(logical=True)
		self.cpu = [c / num_cores for c in self.cpu]													  # Division par le nombre de CPU
		self.memory = [m * MEMORY_RATIO for m in self.memory]											  # Passage en Mo
		self.disk = [(self.disk[i] - self.disk[i - 1]) * MEMORY_RATIO for i in range(1, len(self.disk))]  # Passage en Mo et en delta d'utilisation
		self.disk.insert(0, 0)												  							  # Ajouter 0 au début pour avoir une taille correcte

	# ==================================================
	# endregion Monitoring Manipulation
	# ==================================================

	# ==================================================
	# region Drawing
	# ==================================================
	##################################################
	@staticmethod
	def get_y_range(data, padding_ratio: float = 0.0):
		"""
		Calcule la plage de valeurs de l'axe Y avec un espacement supplémentaire autour des valeurs.

		:param data: Liste des données pour lesquelles la plage doit être calculée.
		:param padding_ratio: Rapport d'espacement ajouté à la plage des données.
		:return: La plage calculée [min, max] avec l'espacement ajouté.
		"""
		min_val, max_val = min(data), max(data)
		padding = (max_val - min_val) * padding_ratio  # Calcul de la marge en haut et en bas
		return [min_val - padding, max_val + padding]

	##################################################
	@staticmethod
	def _plot(ax: plt.axes, times: List, datas: List, label: str):
		"""
		Trace les données de `datas` contre les `times` sur l'axe spécifié.

		:param ax: L'axe matplotlib sur lequel les données doivent être tracées.
		:param times: Liste des temps pour l'axe des x.
		:param datas: Liste des données pour l'axe des y.
		:param label: Label à afficher pour l'axe des y.
		"""
		ax.plot(times, datas)
		ax.set_ylabel(label)  # Ajout du label sur l'axe Y
		ax.set_xlim([times[0], times[-1]])

	##################################################
	def draw_png(self, filename: str):
		"""
		Génère un graphique PNG des ressources utilisées (CPU, mémoire, disque) pendant l'exécution des tests.

		:param filename: Le chemin et nom du fichier PNG à enregistrer.
		"""
		plt.close()  # Fermeture des précédentes figures
		_, axs = plt.subplots(3, 1, figsize=(16, 9), sharex=True)

		self._plot(axs[0], self.times, self.cpu, "CPU Usage (%)")
		self._plot(axs[1], self.times, self.memory, "Memory Usage (Mo)")
		self._plot(axs[2], self.times, self.disk, "Disk Usage (IO Mo)")

		plt.xlabel("Time (s)")
		plt.savefig(filename, bbox_inches="tight")
		plt.close()

	##################################################
	def draw_html(self, filename: str):
		"""
		Génère un graphique interactif HTML des ressources utilisées pendant les tests et l'enregistre.

		:param filename: Le chemin et nom du fichier HTML à enregistrer.
		"""
		fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05,
							subplot_titles=("CPU Usage (%)", "Memory Usage (Mo)", "Disk Usage (IO Mo)"))
		color_map = get_color_map_by_name([test["File"] for test in self.tests_info], px.colors.qualitative.Plotly)

		params = [{"y": self.cpu, "name": "CPU Usage (%)", "line": dict(color="blue")},
				  {"y": self.memory, "name": "Memory Usage (Mo)", "line": dict(color="green")},
				  {"y": self.disk, "name": "Disk Usage (IO Mo)", "line": dict(color="red")}]

		for i in range(len(params)):
			fig.add_trace(go.Scatter(x=self.times, y=params[i]["y"], mode="lines",
									 name=params[i]["name"], line=params[i]["line"]), row=i + 1, col=1)
			draw_test_section(fig, self.get_y_range(params[i]["y"]), self.tests_info, color_map, self.times[-1], i + 1)

		# add_color_map_legend
		fig.update_layout(height=900, title_text="Resource Usage Over Time", showlegend=False)
		for i in range(3):
			fig.update_yaxes(showgrid=False, row=i + 1, col=1)  # Supprimer la grille verticale
			fig.update_xaxes(showgrid=False, row=i + 1, col=1)  # Supprimer la grille horizontale
		fig.update_xaxes(title_text="Time (s)", row=3, col=1)   # Place le titre X uniquement sur le graphique du bas

		fig.write_html(filename)

	# ==================================================
	# endregion Drawing
	# ==================================================

	# ==================================================
	# endregion IO
	# ==================================================
	##################################################
	def save(self, filename: str):
		"""
		Sauvegarde les données de monitoring dans un fichier texte.

		:param filename: Le chemin et nom du fichier texte à enregistrer.
		"""
		with open(filename, "w") as f:
			f.write(f"Timestamps : {self.times}\n")
			f.write(f"CPU Usage : {self.cpu}\n")
			# f.write(f"GPU Usage : {self.gpu}\n")
			f.write(f"Memory Usage : {self.memory}\n")
			f.write(f"Disk Usage : {self.disk}\n")
			f.write(f"Liste des tests : \n")
			for test in self.tests_info: f.write(f"{test["File"]}, {test["Test"]}, {test["Timestamp"]}\n")

	##################################################
	def tostring(self) -> str:
		"""
		Retourne une représentation textuelle des données de monitoring.

		:return: Chaîne décrivant les données de monitoring.
		"""
		return (f"{self.n_entries} entrées.\nTimestamps : {self.times}\n"
				f"CPU Usage : {self.cpu}\n"  # GPU Usage : {self.gpu}\n"
				f"Memory Usage : {self.memory}\nDisk Usage : {self.disk}")

	##################################################
	def __str__(self) -> str: return self.tostring()

# ==================================================
# endregion IO
# ==================================================
