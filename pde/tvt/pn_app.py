import panel as pn
from .panel.traces import Test

pn.extension()

def traces(doc):
	content = Test.get_message()
	content.server_doc(doc)