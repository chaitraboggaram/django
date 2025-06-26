import panel as pn
from .cytoscape import Cytoscape as Cyto
import json

pn.extension()
pn.config.raw_css.append('@import url("/static/css/style.css");')

class Traces:
	@staticmethod
	def get_data(documents):
		tableTitle = pn.pane.Markdown(
			"### Traces Table",
			sizing_mode="stretch_width",
			css_classes=["sub-title"]
		)

		cytoTitle = pn.pane.Markdown(
			"### Cytoscape",
			sizing_mode="stretch_width",
			css_classes=["sub-title"]
		)

		documents = documents[1:-1]
		cyto = Cyto.show_cytoscape(documents)
		layout = pn.Column(cytoTitle, cyto, tableTitle)

		return layout