import panel as pn
from .cytoscape import Cytoscape as Cyto
from .new_cyto import Cytoscape as NewCytoscape

pn.extension()
pn.config.raw_css.append('@import url("/static/css/style.css");')

class Traces:
	@staticmethod
	def get_data(session_key):
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

		newCytoscapeTitle = pn.pane.Markdown(
			f"### New Cytoscape - Session ID: {session_key}",
			sizing_mode="stretch_width",
			css_classes=["sub-title"]
		)

		cyto = Cyto.show_cytoscape()
		new_cyto = NewCytoscape.show_cytoscape()
		layout = pn.Column(newCytoscapeTitle, new_cyto, tableTitle)

		return layout