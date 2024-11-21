import threading
import time
from dataclasses import dataclass, field
from typing import List

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import psutil


##################################################
@dataclass
class Monitoring:
	"""Classe de monitoring"""
	cpu: List[float] = field(init=False, default_factory=list)
	# gpu: List[float] = field(init=False, default_factory=list)
	memory: List[float] = field(init=False, default_factory=list)
	disk: List[float] = field(init=False, default_factory=list)
	timestamps: List[float] = field(init=False, default_factory=list)
	monitoring: bool = field(init=False, default=False)
	thread: threading.Thread = field(init=False, default_factory=threading.Thread)

	##################################################
	@property
	def n_entries(self)->int: return len(self.timestamps)

	# ==================================================
	# region Monitoring Manipulation
	# ==================================================
	##################################################
	def start(self, interval: float = 1):
		""" Autorise le monitoring """
		self.cpu = []
		# self.gpu = []
		self.memory = []
		self.disk = []
		self.timestamps = []
		self.monitoring = True
		self.thread = threading.Thread(target=self.monitor, args=(interval,))
		self.thread.start()

	##################################################
	def monitor(self, interval: float = 1):
		"""
		Monitoring qui doit se lancer dans un thread séparé, récupère l'utilisation système et non uniquement de python et ses tests.

		Voir dans un second plan si c'est possible avec Getpid.
		"""
		while self.monitoring:
			self.cpu.append(psutil.cpu_percent())
			# self.gpu.append(0)
			self.memory.append(psutil.virtual_memory().percent)
			self.disk.append(psutil.disk_usage('/').percent)
			self.timestamps.append(time.time())
			time.sleep(interval)

	##################################################
	def stop(self):
		""" Stoppe le monitoring """
		self.monitoring = False
		self.thread.join()

	# ==================================================
	# endregion Monitoring Manipulation
	# ==================================================

	# ==================================================
	# region Drawing
	# ==================================================
	##################################################
	def _plot_usage(self, ax: plt.axes, datas: List, resource: str):
		""" Trace les données sur l'axe donné. """
		ax.plot(self.timestamps, datas)
		ax.set_ylabel(f"{resource} Usage (%)")  # Ajout du label sur l'axe Y

	##################################################
	def draw_png(self, filename: str):
		""" Générer un graphique des ressources utilisées pendant l'exécution des tests """
		plt.close()  # Fermeture des précédentes figures
		_, axs = plt.subplots(3, 1, figsize=(16, 9), sharex=True)

		self._plot_usage(axs[0], self.cpu, "CPU")
		self._plot_usage(axs[1], self.memory, "Memory")
		self._plot_usage(axs[2], self.disk, "Disk")

		plt.xlabel('Time (s)')
		plt.savefig(filename, bbox_inches="tight")
		plt.close()

	##################################################
	def draw_html(self, filename: str):
		fig = go.Figure()
		fig.add_trace(go.Scatter(x=self.timestamps, y=self.cpu, mode='lines', name='CPU Usage'))
		fig.add_trace(go.Scatter(x=self.timestamps, y=self.memory, mode='lines', name='Memory Usage'))
		fig.add_trace(go.Scatter(x=self.timestamps, y=self.disk, mode='lines', name='Disk Usage'))
		fig.update_layout(title='Resource Usage Over Time', xaxis_title='Time (s)', yaxis_title='% Usage')
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
		return (f"{len(self.timestamps)} entrées.\n"
				f"Timestamps : {self.timestamps}\n"
				f"CPU Usage : {self.cpu}\n"
				#f"GPU Usage : {self.gpu}\n"
				f"Memory Usage : {self.memory}\n"
				f"Disk Usage : {self.disk}")

	##################################################
	def __str__(self) -> str: return self.tostring()

	# ==================================================
	# endregion IO
	# ==================================================
