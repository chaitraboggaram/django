import panel as pn
from .panel.traces import Traces
from .panel.cytoscape import Cytoscape
pn.config.raw_css.append('@import url("/static/css/style.css");')
pn.extension()

def traces(doc):
	content = Traces.get_data()
	content.server_doc(doc)