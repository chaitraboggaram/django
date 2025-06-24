import panel as pn

pn.extension()

class Test:
	@staticmethod
	def get_message():
		return pn.pane.Markdown(
			"#### Panel Page",
			sizing_mode="stretch_width",
			css_classes=["my-title"]
		)