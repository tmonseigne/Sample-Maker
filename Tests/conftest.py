import platform

import cpuinfo
import psutil
from pytest import hookimpl

from SampleMaker.Tools.Monitoring import Monitoring

all_tests_monitoring = Monitoring()

##################################################
def cpu_infos() -> str:
	info = cpuinfo.get_cpu_info()
	res = info.get('processor', 'Unknown Processor')
	try:  # En cas e problème notamment sur mac
		cpu_info = psutil.cpu_freq(percpu=False)
		res += f" ({cpu_info.current / 1000} GHz - {psutil.cpu_count(logical=False)} Cores ({psutil.cpu_count(logical=True)} Logical))"
	except RuntimeError: cpu_info = None
	return res


##################################################
# Fonction pour configurer les métadonnées du rapport
def pytest_metadata(metadata):
	metadata['System'] = platform.system()
	metadata['Platform'] = platform.platform()
	metadata['CPU'] = cpu_infos()
	metadata['RAM'] = f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB"

	## Ajout de la carte graphique si disponible
	try:
		import GPUtil
		gpus = GPUtil.getGPUs()
		if gpus: metadata['GPU'] = f"{gpus[0].name} (Memory: {gpus[0].memoryTotal}MB)"
		else: metadata['GPU'] = 'No GPU found'
	except ImportError:
		metadata['GPU'] = 'GPUtil not installed'


##################################################
@hookimpl(tryfirst=True)
def pytest_sessionstart(session):
	global all_tests_monitoring
	all_tests_monitoring.start(0.1)

##################################################
@hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
	global all_tests_monitoring
	all_tests_monitoring.stop()
	all_tests_monitoring.draw_png("Reports/Monitoring.png")
	all_tests_monitoring.draw_html("Reports/Monitoring.html")
	all_tests_monitoring.save("Reports/test_info.txt")

##################################################
@hookimpl(tryfirst=True)
def pytest_runtest_protocol(item, nextitem):
	""" Capture les informations sur chaque test """
	global all_tests_monitoring
	all_tests_monitoring.add_test_info(item.nodeid)
	return None