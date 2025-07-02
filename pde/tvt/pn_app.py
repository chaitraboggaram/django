import panel as pn
from .panel.traces import Traces
from .panel.cytoscape import Cytoscape
pn.config.raw_css.append('@import url("/static/css/style.css");')
pn.extension()

def traces(doc):
	documents = doc.session_context.request.arguments['documents']  # Bokeh way
	generate_cytoscape = doc.session_context.request.arguments['generate_cytoscape']
	content = Traces.get_data(documents=documents, generate_cytoscape=generate_cytoscape)
	content.server_doc(doc)