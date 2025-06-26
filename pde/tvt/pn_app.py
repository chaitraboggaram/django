import panel as pn
from .panel.traces import Traces
from .panel.cytoscape import Cytoscape
pn.config.raw_css.append('@import url("/static/css/style.css");')
pn.extension()

def traces(doc):
	session_key = doc.session_context.request.arguments['session_key']  # Bokeh way
	content = Traces.get_data(session_key=session_key)
	content.server_doc(doc)