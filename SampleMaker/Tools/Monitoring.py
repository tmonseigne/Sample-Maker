import os
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

from SampleMaker.Tools.Drawing import add_color_map_legend_to_go

MEMORY_RATIO = 1.0 / (1024 * 1024)


##################################################
@dataclass
class Monitoring:
	"""Classe de monitoring"""
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
	def n_entries(self) -> int: return len(self.times)

	##################################################
	def _reset(self):
		"""Réinitialise les tableaux"""
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
		# Sélection de processus
		pytest_pid = os.getpid()  # PID de pytest
		pytest_proc = psutil.Process(pytest_pid)  # Récupère le processus parent
		children = pytest_proc.children(recursive=True)  # Cible les processus enfants
		processes = [pytest_proc] + children  # Inclut le processus principal et ses enfants
		cpu = sum(proc.cpu_percent(interval=self.interval) for proc in processes)
		memory = sum(proc.memory_info().rss for proc in processes)
		disk = sum(proc.io_counters().write_bytes for proc in processes)
		self.cpu.append(cpu)
		self.memory.append(memory)
		self.disk.append(disk)
		self.times.append(time.time())

	##################################################
	def start(self, interval: float = 1.0):
		""" Autorise le monitoring """
		self._reset()
		self.interval = interval
		self.monitoring = True
		self.thread = threading.Thread(target=self.monitor)
		self.thread.start()

	##################################################
	def monitor(self):
		"""
		Monitoring qui doit se lancer dans un thread séparé, récupère l'utilisation système et non uniquement de python et ses tests.

		Voir dans un second plan si c'est possible avec Getpid.
		"""
		while self.monitoring:
			self._update()
			time.sleep(self.interval)

	##################################################
	def stop(self):
		""" Stoppe le monitoring """
		self.monitoring = False
		self._update() # Dernière entrée
		self._update_array_for_readability()
		self.thread.join()

	##################################################
	def add_test_info(self, name: str):
		"""Ajoute des informations sur le test dans la liste"""
		# example avec name = Tests/test_FileIO.py::test_save_boolean_mask_as_png
		# Je veux file = FileIO et test = Save Boolean Mask As PNG
		match = re.match(r"Tests/test_(.*)\.py::test_(.*)", name)
		if match:
			file = match.group(1).replace('_', ' ').title()  # Récupère le nom du fichier et change la casse
			test = match.group(2).replace('_', ' ').title()  # Récupère le nom du test et change la casse
			self.tests_info.append({"File": file, "Test": test, "Timestamp": time.time()})

	##################################################
	def _update_array_for_readability(self, round_time: int = 2):
		first_time = self.times[0]

		for test_info in self.tests_info: test_info["Timestamp"] = round(test_info["Timestamp"] - first_time, round_time)
		self.times = [round(t - first_time, round_time) for t in self.times]

		num_cores = psutil.cpu_count(logical=True)
		self.cpu = [c / num_cores for c in self.cpu]
		self.memory = [m * MEMORY_RATIO for m in self.memory]
		self.disk = [(self.disk[i] - self.disk[i - 1]) * MEMORY_RATIO for i in range(1, len(self.disk))]
		self.disk.insert(0, 0)  # Ajouter 0 au début pour correspondre à la longueur de `timestamps`

	# ==================================================
	# endregion Monitoring Manipulation
	# ==================================================

	# ==================================================
	# region Drawing
	# ==================================================
	##################################################
	@staticmethod
	def get_y_range(data, padding_ratio: float = 0.0):
		min_val, max_val = min(data), max(data)
		padding = (max_val - min_val) * padding_ratio  # Ajouter une marge en haut et en bas
		return [min_val - padding, max_val + padding]

	##################################################
	def _get_file_color_map(self) -> dict:
		# Récupérer les noms de fichiers uniques
		filenames = set(test_info["File"] for test_info in self.tests_info)

		# Générer une couleur unique pour chaque fichier
		palette = px.colors.qualitative.Plotly  # Choisir une palette de couleurs
		color_map = {}  # Dictionnaire pour associer chaque fichier à une couleur

		# Associer une couleur unique à chaque fichier
		color_index = 0
		for file in filenames:
			color_map[file] = palette[color_index % len(palette)]
			color_index += 1  # Passer à la couleur suivante

		return color_map

	##################################################
	def _draw_tests(self, fig: go.Figure, color_map: dict):
		y_ranges = [self.get_y_range(self.cpu), self.get_y_range(self.memory), self.get_y_range(self.disk)]
		print(y_ranges)
		# Ajouter les barres verticales pour chaque test et des zones colorées en fonction du fichier
		for i, test in enumerate(self.tests_info):
			timestamp = test["Timestamp"]
			file = test["File"]
			name = test["Test"]

			# Récupérer la couleur associée au fichier
			color = color_map[file]

			# Déterminer la plage pour la zone colorée
			# Si ce n'est pas le dernier test, la fin de la zone est le timestamp du test suivant sinon le dernier timestamp
			if i < len(self.tests_info) - 1: next_timestamp = self.tests_info[i + 1]["Timestamp"]
			else: next_timestamp = self.times[-1]

			for j in range(len(y_ranges)):
				# Ajouter une zone colorée
				fig.add_shape(type="rect", x0=timestamp, x1=next_timestamp, y0=y_ranges[j][0], y1=y_ranges[j][1],
							  fillcolor=color, opacity=0.2, line=dict(width=0), row=j + 1, col=1)
				# Ajouter une ligne verticale pointillée
				fig.add_trace(go.Scatter(x=[timestamp, timestamp], y=y_ranges[j],
										 mode='lines', line=dict(color=color, width=0.5, dash='dash'),
										 name=f"{file} - {name}", hoverinfo='text', text=f"{file} - {name}"), row=j + 1, col=1)



	##################################################
	@staticmethod
	def _plot(ax: plt.axes, times: List, datas: List, label: str):
		""" Trace les données sur l'axe donné. """
		ax.plot(times, datas)
		ax.set_ylabel(label)  # Ajout du label sur l'axe Y
		ax.set_xlim([times[0], times[-1]])

	##################################################
	def draw_png(self, filename: str):
		""" Générer un graphique des ressources utilisées pendant l'exécution des tests """
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
		fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05,
							subplot_titles=("CPU Usage (%)", "Memory Usage (Mo)", "Disk Usage (IO Mo)"))

		params = [
				{"y": self.cpu, "name": "CPU Usage (%)", "line": dict(color="blue")},
				{"y": self.memory, "name": "Memory Usage (Mo)", "line": dict(color="green")},
				{"y": self.disk, "name": "Disk Usage (IO Mo)", "line": dict(color="red")},
				]
		for i in range(len(params)):
			fig.add_trace(go.Scatter(x=self.times, y=params[i]["y"], mode="lines",
									 name=params[i]["name"], line=params[i]["line"]), row=i + 1, col=1)

		color_map = self._get_file_color_map()
		self._draw_tests(fig, color_map)
		#add_color_map_legend_to_go(fig, color_map)

		fig.update_layout(height=900, title_text="Resource Usage Over Time", showlegend=False)
		for i in range(3):
			fig.update_yaxes(showgrid=False, row=i + 1, col=1)  # Supprimer la grille verticale
			fig.update_xaxes(showgrid=False, row=i + 1, col=1)  # Supprimer la grille horizontale
		fig.update_xaxes(title_text="Time (s)", row=3, col=1)  # Place le titre X uniquement sur le graphique du bas

		fig.write_html(filename)

	# ==================================================
	# endregion Drawing
	# ==================================================

	# ==================================================
	# endregion IO
	# ==================================================

	##################################################
	def save(self, filename: str):
		with open(filename, "w") as f:
			f.write(f"Timestamps : {self.times}\n")
			f.write(f"CPU Usage : {self.cpu}\n")
			#f.write(f"GPU Usage : {self.gpu}\n")
			f.write(f"Memory Usage : {self.memory}\n")
			f.write(f"Disk Usage : {self.disk}\n")
			f.write(f"Liste des tests : \n")
			for test in self.tests_info:
				f.write(f"{test["File"]}, {test["Test"]}, {test["Timestamp"]}\n")


	##################################################
	def tostring(self) -> str:
		"""
		Retourne une représentation textuelle du monitoring.

		:return: Chaîne décrivant le monitoring.
		"""
		return (f"{self.n_entries} entrées.\n"
				f"Timestamps : {self.times}\n"
				f"CPU Usage : {self.cpu}\n"
				# f"GPU Usage : {self.gpu}\n"
				f"Memory Usage : {self.memory}\n"
				f"Disk Usage : {self.disk}")

	##################################################
	def __str__(self) -> str: return self.tostring()

	# ==================================================
	# endregion IO
	# ==================================================
