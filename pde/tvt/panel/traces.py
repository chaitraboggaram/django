import panel as pn
from .cytoscape import Cytoscape as Cyto
from .new_cyto import Cytoscape as NewCytoscape

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

		django_data = pn.pane.Markdown(
			f"Django Data: {documents}",
			sizing_mode="stretch_width",
			css_classes=["sub-title"]
		)

		cyto = Cyto.show_cytoscape()
		layout = pn.Column(cytoTitle, django_data, cyto, tableTitle)

		return layout