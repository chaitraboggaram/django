import panel as pn
from .panel.traces import Traces

pn.extension()

def traces(doc):
	content = Traces.get_message()
	content.server_doc(doc)