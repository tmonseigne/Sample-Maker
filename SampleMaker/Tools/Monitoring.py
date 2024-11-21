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

	# ==================================================
	# region Monitoring Manipulation
	# ==================================================
	##################################################
	@property
	def n_entries(self)->int: return len(self.timestamps)

	##################################################
	def _reset(self):
		"""Réinitialise les tableaux"""
		self.cpu = []
		# self.gpu = []
		self.memory = []
		self.disk = []
		self.timestamps = []
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
	def _plot_usage(self, ax: plt.axes, times: List, datas: List, resource: str):
		""" Trace les données sur l'axe donné. """
		ax.plot(times, datas)
		ax.set_ylabel(f"{resource} Usage (%)")  # Ajout du label sur l'axe Y
		ax.set_xlim([times[0], times[-1]])

	##################################################
	def draw_png(self, filename: str):
		""" Générer un graphique des ressources utilisées pendant l'exécution des tests """
		plt.close()  # Fermeture des précédentes figures
		_, axs = plt.subplots(3, 1, figsize=(16, 9), sharex=True)

		new_times = [t - self.timestamps[0] for t in self.timestamps]
		self._plot_usage(axs[0], new_times, self.cpu, "CPU")
		self._plot_usage(axs[1], new_times, self.memory, "Memory")
		self._plot_usage(axs[2], new_times, self.disk, "Disk")

		plt.xlabel('Time (s)')
		plt.savefig(filename, bbox_inches="tight")
		plt.close()

	##################################################
	def draw_html(self, filename: str):
		fig = go.Figure()
		new_times = [t - self.timestamps[0] for t in self.timestamps]
		fig.add_trace(go.Scatter(x=new_times, y=self.cpu, mode='lines', name='CPU Usage'))
		fig.add_trace(go.Scatter(x=new_times, y=self.memory, mode='lines', name='Memory Usage'))
		fig.add_trace(go.Scatter(x=new_times, y=self.disk, mode='lines', name='Disk Usage'))
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
		return (f"{self.n_entries} entrées.\n"
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
