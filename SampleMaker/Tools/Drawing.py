""" Quelques fonctions de dessin utiles """

import matplotlib.pyplot as plt
import plotly.express as px  # Pour accéder aux couleurs qualitatives
import plotly.graph_objects as go
import psutil
from plotly.subplots import make_subplots


##################################################
def add_color_map_legend_to_go(fig: go.Figure, color_map: dict):
	# Configuration de la légende
	x_start = 0.05  # Position de départ sur l'axe x (en proportion de la largeur)
	y_pos = -0.2  # Position sous le graphique
	spacing = 0.15  # Espacement horizontal entre les entrées de la légende

	annotations = []
	shapes = []
	for i, (item, color) in enumerate(color_map.items()):
		# Calcul des positions
		x_rect_start = x_start + i * spacing
		x_rect_end = x_rect_start + 0.05

		# Ajouter un carré coloré
		shapes.append(dict(type="rect", xref="paper", yref="paper",
						   x0=x_rect_start, y0=y_pos, x1=x_rect_end, y1=y_pos + 0.05, fillcolor=color, line=dict(width=0), ))

		# Ajouter un texte à côté
		annotations.append(dict(x=x_rect_end + 0.02, y=y_pos + 0.025, xref="paper", yref="paper",
								text=item, showarrow=False, font=dict(size=10), align="left", ))

	# Appliquer les annotations et les formes au graphique
	fig.update_layout(annotations=annotations, shapes=shapes, )
