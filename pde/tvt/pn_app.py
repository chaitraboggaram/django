import panel as pn
from .panel.traces import Traces
from .panel.cytoscape import Cytoscape
pn.config.raw_css.append('@import url("/static/css/style.css");')
pn.extension()

def traces(doc):
	documents = doc.session_context.request.arguments['documents']  # Bokeh way
	generate_flag = doc.session_context.request.arguments['generate_flag']
	print("Flag in pn_app:", generate_flag)
	content = Traces.get_data(documents=documents, generate_flag=generate_flag)
	content.server_doc(doc)