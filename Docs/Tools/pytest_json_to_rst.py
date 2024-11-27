""" Fichier permettant de transformer un rapport pytest json en reStructuredText pour sphinx """

import datetime
import json
import os
import sys
import re

from ansi2html import Ansi2HTMLConverter

# Convertisseur ANSI vers HTML
conv = Ansi2HTMLConverter(inline=True)  # Utiliser des styles en ligne pour éviter les dépendances CSS


##################################################
def to_title_case(name: str) -> str:
	return name.replace("_", " ").title()


##################################################
def format_duration(duration: float) -> str:
	"""
	Formate une durée en une unité lisible avec la précision adéquate.

	:param duration: Durée en secondes (float).
	:return: Chaîne formatée avec la meilleure unité.
	"""
	if duration < 1:  # Moins d'une seconde : millisecondes
		return f"{round(duration * 1000)}ms"
	elif duration < 60:  # Moins d'une minute : secondes
		return f"{duration:.2f}s"
	elif duration < 3600:  # Moins d'une heure : minutes et secondes
		minutes = int(duration // 60)
		seconds = round(duration % 60, 2)
		return f"{minutes}min {seconds:.0f}s"
	else:  # Une heure ou plus : heures, minutes et secondes
		hours = int(duration // 3600)
		minutes = int((duration % 3600) // 60)
		seconds = round(duration % 60, 2)
		return f"{hours}h {minutes}min {seconds:.0f}s"


# ==================================================
# region Generation
# ==================================================
##################################################
def generate_rst_from_json(src: str, dst: str):
	try:
		with open(src, 'r') as f:
			data = json.load(f)  # Read json
	except FileNotFoundError:
		print("Json File not found.")

	title, monitoring = get_files_info(dst)

	with open(dst, 'w', encoding="utf-8") as f:
		f.write(f"{title}\n{"=" * len(title)}\n\n")
		f.write(get_metadata(data["metadata"]))
		f.write(get_summary(data))
		f.write(get_monitoring(monitoring))
		f.write(get_tests(data["tests"]))


##################################################
def get_files_info(src, monitoring_ext="html") -> list[str]:
	file_basename = os.path.splitext(os.path.basename(src))[0]
	title = to_title_case(file_basename)
	monitoring_file = file_basename.replace("Test_Report", "Monitoring") + f".{monitoring_ext}"
	return [title, monitoring_file]


##################################################
def get_metadata(metadata: dict) -> str:
	res = ("Environnement\n"
		   "-------------\n\n"
		   ".. list-table::\n\n")

	for key, value in metadata.items():
		if key != "Packages" and key != "Plugins":
			res += f"   * - {key}\n     - {value}\n"

	return res + "\n"


##################################################
def get_summary(data: dict) -> str:
	res = ("Summary\n"
		   "-------\n\n")
	timestamp = datetime.datetime.fromtimestamp(data["created"])
	time = timestamp.strftime("%H:%M:%S")
	date = timestamp.strftime("%d/%m/%Y")
	duration = str(datetime.timedelta(seconds=data["duration"])).split(".")[0]
	sum = data["summary"]

	res += (f"{sum.get("collected", 0)} tests collected, {sum.get("passed", 0)} passed, {sum.get("failed", 0)} failed "
			f"in {duration}s on {date} at {time}\n")
	return res + "\n"


##################################################
def get_monitoring(file: str) -> str:
	res = ("Monitoring\n"
		   "----------\n\n")

	#Le Json pourrait etre bien mais ne marche pas
	#res += f".. chart:: Reports/{file}\n\n    Resources Monitoring\n\n"
	#Le Iframe fait le travail
	res += (f".. raw:: html\n\n"
			f"   <div style=\"position: relative; width: 100%; height: 620px; max-width: 100%; margin: 0 0 1em 0; padding:0;\">\n"
			f"     <iframe src=\"{file}\"\n"
			f"             style=\"position: absolute; margin: 0; padding:0; width: 100%; height: 100%; border: none;\">\n"
			f"     </iframe>\n"
			f"   </div>\n\n")

	return res


##################################################
def get_tests(tests: list) -> str:
	"""
	Génère une section RST formatée pour afficher les résultats des tests.

	:param tests: Liste des résultats de tests sous forme de dictionnaires.
	:return: Chaîne RST formatée.
	"""
	res = ("Test Cases\n"
		   f"----------\n\n"
		   ".. raw:: html\n\n   <div class=\"test-page\">\n\n")

	# Grouper les tests par fichier
	tests_by_file = {}
	for test in tests:
		filename = test["nodeid"].split("::")[0]  # Extraire le fichier
		if filename not in tests_by_file:
			tests_by_file[filename] = []
		tests_by_file[filename].append(test)

	for filename, file_tests in tests_by_file.items():
		# Titre du fichier
		title = to_title_case(filename.split("/")[-1][5:-3])  # Nom du fichier sans chemin, sans "test_" et sans ".py"
		underline = "^" * len(title)
		res += f"{title}\n{underline}\n\n"

		# Ajouter le tableau avec `.. list-table::`
		res += (".. list-table:: \n"
				"   :header-rows: 1\n\n"
				"   * - Test Name\n"
				"     - Status\n"
				"     - Duration\n")
		# "     - Setup Duration\n"
		# "     - Call Duration\n"
		# "     - Teardown Duration\n\n")

		for test in file_tests:
			test_name = to_title_case(test["nodeid"].split("::")[1][5:])  # Nom du test sans "test_"
			outcome = test["outcome"]
			durations = [test["setup"].get("duration", 0),
						 test["call"].get("duration", 0),
						 test["teardown"].get("duration", 0)]

			res += (f"   * - {test_name}\n"
					f"     - {get_outcome_icon(outcome)}\n"
					f"     - {format_duration(sum(durations))}\n")
		# f"     - {format_duration(durations[0])}\n"
		# f"     - {format_duration(durations[1])}\n"
		# f"     - {format_duration(durations[2])}\n\n")

		res += "\n"

		# Ajouter un lien vers le stdout
		for test in file_tests:
			test_name = to_title_case(test["nodeid"].split("::")[1][5:])  # Nom du test sans "test_"
			stdout = test["call"].get("stdout", "")
			stdout = conv.convert(stdout, full=False)  # Convertir ANSI en HTML
			stdout = stdout.replace("\n", "<br>")  # Remplacer les sauts de ligne par <br> pour un bon affichage en HTML
			stdout = re.sub(r"^(<br>)+", "", stdout)  # Supprime les <br> initiaux
			stdout = re.sub(r"(<br>)+$", "", stdout)  # Supprime les <br> finaux
			if stdout:  # Si le stdout existe, l'afficher dans un bloc repliable
				res += f".. raw:: html\n\n"
				res += f"   <details>\n"
				res += f"      <summary>Log Test : {test_name}</summary>\n"
				res += f"      <pre>{stdout}</pre>\n"
				res += f"   </details>\n\n"

	res += ".. raw:: html\n\n   </div>\n\n"
	return res


##################################################
def get_outcome_icon(outcome: str) -> str:
	"""
	Retourne une icône/emoji correspondant à un résultat de test.

	:param outcome: Résultat du test ("passed", "failed", "xpassed", "xfailed", "skipped").
	:return: Emoji correspondant au résultat.
	"""
	icons = {
			"passed":  "✅",  # Test réussi
			"failed":  "❌",  # Test échoué
			"xpassed": "⚠️",  # Test attendu comme échoué mais a réussi
			"xfailed": "✔️",  # Test attendu comme échoué et a échoué
			"skipped": "⏭️",  # Test sauté
			}
	return icons.get(outcome, "❓")  # Par défaut, une icône d'interrogation pour les résultats inconnus


# ==================================================
# endregion Generation
# ==================================================
##################################################
def usage():
	print("Usage:\n"
		  "  python gtest2md.py <REPORT_FILE> <OUTPUT_FILE>\n"
		  "  Args:\n"
		  "    REPORT_FILE: Pytest json report.\n"
		  "    OUTPUT_FILE: Path to the output reStructuredText file.")


##################################################
if __name__ == "__main__":
	if len(sys.argv) < 2:
		usage()
		exit(0)

	# Get the source and destination directories.
	src, dst = sys.argv[1], sys.argv[2]

	if not os.path.exists(src):
		print(f"ERROR: The report file \"{src}\" does not exists.")
		usage()
		exit(1)

	print(f"Start generation: input ({src}), output ({dst})")
	generate_rst_from_json(src, dst)
	print('reStructuredText report was generated successfully.')
