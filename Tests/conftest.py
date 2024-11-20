import platform
import psutil
import cpuinfo

def cpu_infos() -> str:
	info = cpuinfo.get_cpu_info()
	res = info.get('processor', 'Unknown Processor')
	cpu_info = psutil.cpu_freq(percpu=False)  # Donne la fréquence actuelle du processeur
	res += f" ({cpu_info.current/1000} GHz - {psutil.cpu_count(logical=False)} Cores ({psutil.cpu_count(logical=True)} Logical))"
	return res

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

