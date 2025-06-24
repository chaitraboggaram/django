import panel as pn

pn.extension()
pn.config.raw_css.append('@import url("/static/css/style.css");')

class Traces:
	@staticmethod
	def get_message():
		tableTitle = pn.pane.Markdown(
			"### Traces Table",
			sizing_mode="stretch_width",
			css_classes=["sub-title"]
		)

		panelTitle = pn.pane.Markdown(
			"### Panel Page",
			sizing_mode="stretch_width",
			css_classes=["sub-title"]
		)

		return pn.Column(
			panelTitle,
			tableTitle,
		)