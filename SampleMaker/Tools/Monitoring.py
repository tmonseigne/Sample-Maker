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
	def start(self, interval: float = 1):
		""" Autorise le monitoring """
		self._reset()
		self.monitoring = True
		self.thread = threading.Thread(target=self.monitor, args=(interval,))
		self.thread.start()

	##################################################
	def monitor(self, interval: float = 1):
		"""
		Monitoring qui doit se lancer dans un thread séparé, récupère l'utilisation système et non uniquement de python et ses tests.

		Voir dans un second plan si c'est possible avec Getpid.
		"""
		pytest_pid = os.getpid()  # PID de pytest
		pytest_proc = psutil.Process(pytest_pid)
		while self.monitoring:
			# Cibler les processus enfants
			children = pytest_proc.children(recursive=True)
			processes = [pytest_proc] + children  # Inclut le processus principal et ses enfants
			cpu = sum(proc.cpu_percent(interval=0) for proc in processes)
			memory = sum(proc.memory_info().rss for proc in processes)
			disk = sum(proc.io_counters().write_bytes for proc in processes)

			self.cpu.append(cpu)
			self.memory.append(memory)
			self.disk.append(disk)
			self.times.append(time.time())
			time.sleep(interval)

	##################################################
	def stop(self):
		""" Stoppe le monitoring """
		self.monitoring = False
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
	def get_y_range(data):
		min_val, max_val = min(data), max(data)
		padding = (max_val - min_val) * 0.1  # Ajouter 10% de marge en haut et en bas
		return [min_val - padding, max_val + padding]

	##################################################
	def _get_file_color_map(self) -> dict:
		# Récupérer les noms de fichiers uniques
		file_names = set(test_info["File"] for test_info in self.tests_info)

		# Générer une couleur unique pour chaque fichier
		color_palette = px.colors.qualitative.Plotly  # Choisir une palette de couleurs
		file_color_map = {}  # Dictionnaire pour associer chaque fichier à une couleur

		# Associer une couleur unique à chaque fichier
		color_index = 0
		for file_name in file_names:
			file_color_map[file_name] = color_palette[color_index % len(color_palette)]
			color_index += 1  # Passer à la couleur suivante

		return file_color_map

	##################################################
	def _draw_tests(self, fig: go.Figure, file_color_map: dict):
		# Ajouter les barres verticales pour chaque test
		for test in self.tests_info:
			timestamp = test["Timestamp"]
			file = test["File"]
			name = test["Test"]

			# Récupérer la couleur associée au fichier
			color = file_color_map[file]

			# Ajouter une ligne verticale pointillée
			fig.add_trace(go.Scatter(x=[timestamp, timestamp], y=self.get_y_range(self.cpu),
									 mode='lines', line=dict(color=color, width=0.5, dash='dash'),
									 name=f"{file} - {name}", hoverinfo='text', text=f"{file} - {name}"), row=1, col=1)
			fig.add_trace(go.Scatter(x=[timestamp, timestamp], y=self.get_y_range(self.memory),
									 mode='lines', line=dict(color=color, width=0.5, dash='dash'),
									 name=f"{file} - {name}", hoverinfo='text', text=f"{file} - {name}"), row=2, col=1)
			fig.add_trace(go.Scatter(x=[timestamp, timestamp], y=self.get_y_range(self.disk),
									 mode='lines', line=dict(color=color, width=0.5, dash='dash'),
									 name=f"{file} - {name}", hoverinfo='text', text=f"{file} - {name}"), row=3, col=1)

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

		fig.add_trace(go.Scatter(x=self.times, y=self.cpu, mode="lines+markers", name="CPU Usage (%)", line=dict(color="blue")), row=1, col=1)
		fig.add_trace(go.Scatter(x=self.times, y=self.memory, mode="lines+markers", name="Memory Usage (Mo)", line=dict(color="green")), row=2, col=1)
		fig.add_trace(go.Scatter(x=self.times, y=self.disk, mode="lines+markers", name="Disk Usage (IO Mo)", line=dict(color="red")), row=3, col=1)

		self._draw_tests(fig, self._get_file_color_map())

		fig.update_layout(height=900, title_text="Resource Usage Over Time", showlegend=False)
		for i in range(3): fig.update_yaxes(showgrid=False, row=i + 1, col=1)  # SUpprimer la grille verticale
		fig.update_xaxes(title_text="Time (s)", row=3, col=1)  # Place le titre X uniquement sur le graphique du bas

		fig.write_html(filename)

	# ==================================================
	# endregion Drawing
	# ==================================================

	# ==================================================
	# endregion IO
	# ==================================================
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
