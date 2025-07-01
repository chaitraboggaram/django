import param
import panel as pn
from panel.custom import JSComponent
import ast

pn.extension(sizing_mode="stretch_width")
pn.config.raw_css.append(
	"""
	.cytoscape-container {
		border: 2px solid #444;
		border-radius: 8px;
		padding: 5px;
		overflow: hidden;
	}
"""
)


class Cytoscape(JSComponent):
	object = param.List()
	layout = param.Selector(
		default="cose",
		objects=[
			"breadthfirst",
			"circle",
			"concentric",
			"cose",
			"grid",
			"preset",
			"random",
		],
	)
	style = param.List(default=[], doc="Use to set the styles of the nodes/edges")
	pan = param.Dict(default={"x": 0, "y": 0})
	selected_nodes = param.List()
	selected_edges = param.List()
	root_node = param.String(default="")

	_esm = """
import { default as cytoscape } from "https://esm.sh/cytoscape"
let cy = null;
function removeCy() {
	if (cy) { cy.destroy() }
}
export function render({ model }) {
	removeCy();
	const div = document.createElement('div');
	div.style.width = "100%";
	div.style.height = "100%";
	div.style.position = "relative";
	model.on('after_render', () => {
		cy = cytoscape({
			container: div,
			layout: {
				name: model.layout,
				roots: model.root_node || undefined
			},
			elements: model.object,
			pan: model.pan
		});
		cy.style().resetToDefault().fromJson([
		{
			selector: 'node',
			style: {
				'background-color': 'data(color)',
				'label': 'data(label)',
				'color': '#fff',
				'text-valign': 'center',
				'text-halign': 'center',
				'shape': 'ellipse',
				'text-wrap': 'wrap',
				'text-max-width': '80%',
				'font-size': '10px',
				'text-overflow': 'ellipsis',
				'width': 50,
				'height': 50
			}
		},
		{
			selector: 'edge',
			style: {
				'width': 2,
				'line-color': '#bbb',
				'target-arrow-color': '#bbb',
				'target-arrow-shape': 'triangle',
				'curve-style': 'bezier'
			}
		}
		]).update();

		const tooltip = document.createElement('div');
		tooltip.style.position = 'absolute';
		tooltip.style.background = 'rgba(0,0,0,0.7)';
		tooltip.style.color = 'white';
		tooltip.style.padding = '2px 6px';
		tooltip.style.borderRadius = '4px';
		tooltip.style.pointerEvents = 'none';
		tooltip.style.fontSize = '12px';
		tooltip.style.zIndex = '9999';
		tooltip.style.display = 'none';
		document.body.appendChild(tooltip);

		cy.on('mouseover', 'node', (evt) => {
			const node = evt.target;
			tooltip.textContent = node.data('label') || node.id();
			const pos = evt.renderedPosition;
			const containerRect = cy.container().getBoundingClientRect();
			tooltip.style.left = (containerRect.left + pos.x + 10) + 'px';
			tooltip.style.top = (containerRect.top + pos.y + 10) + 'px';
			tooltip.style.display = 'block';
		});
		cy.on('mouseout', 'node', () => {
			tooltip.style.display = 'none';
		});

		cy.on('select unselect', function (evt) {
			model.selected_nodes = cy.elements('node:selected').map(el => el.id());
			model.selected_edges = cy.elements('edge:selected').map(el => el.id());
		});

		model.on('object', () => { cy.json({ elements: model.object }); });
		model.on('layout', () => { cy.layout({ name: model.layout, roots: model.root_node || undefined }).run() });
		model.on('pan', () => { cy.pan(model.pan) });
		model.on('style', () => { cy.style().resetToDefault().append(model.style).update() });
		model.on('select_node', (node_id) => {
			cy.elements().unselect();
			const node = cy.$id(node_id);
			if (node) {
				node.select();
				cy.center(node);
			}
		});

		window.addEventListener('resize', function (event) {
			cy.center();
		});

		model.on('remove', removeCy);
	});
	return div;
}
"""

	TYPE_COLOR_MAP = {
		"Requirement": "#1f77b4",
		"Design": "#ff7f0e",
		"Test": "#2ca02c",
		"Specification": "#d62728",
		"Task": "#9467bd",
		"Development": "#8c564b",
		"Risk": "#e377c2",
		"Unknown": "gray",
	}


	DEFAULT_STYLE = [
		{
			"selector": "node",
			"style": {
				"background-color": "data(color)",
				"label": "data(label)",
				"color": "#fff",
				"text-valign": "center",
				"text-halign": "center",
				"shape": "ellipse",
				"text-wrap": "wrap",
				"text-max-width": "80%",
				"font-size": "10px",
				"text-overflow": "ellipsis",
				"width": 80,
				"height": 50,
			},
		},
		{
			"selector": "edge",
			"style": {
				"width": 2,
				"line-color": "#bbb",
				"target-arrow-color": "#bbb",
				"target-arrow-shape": "triangle",
				"curve-style": "bezier",
			},
		},
	]

	cytoscape_graph_cache = None

	@staticmethod
	def ensure_node_exists(node_id, nodes, doc_type, label):
		if node_id in nodes:
			return
		color = Cytoscape.TYPE_COLOR_MAP.get(doc_type, "gray")
		nodes[node_id] = {
			"data": {
				"id": node_id,
				"label": label,
				"color": color,
			},
			"classes": doc_type.lower() if doc_type else "",
		}

	@staticmethod
	def recurse(node_dict, nodes, edges, all_nodes, has_parents):
		node_id = node_dict["id"]
		doc_type = node_dict.get("doc_type", "")
		label = node_dict.get("title", str(node_id))[:50]
		Cytoscape.ensure_node_exists(node_id, nodes, doc_type, label)
		all_nodes.add(node_id)

		for child_id, child_obj in node_dict.get("children", {}).items():
			Cytoscape.recurse(child_obj, nodes, edges, all_nodes, has_parents)
			edges.append(
				{
					"data": {
						"id": f"{node_id}-{child_id}",
						"source": node_id,
						"target": child_id,
					}
				}
			)
			has_parents.add(child_id)

	@staticmethod
	def build_layout(graph):
		return pn.Column(
			pn.Row(
				pn.Param(
					graph,
					parameters=["layout", "pan", "selected_nodes", "selected_edges"],
					sizing_mode="fixed",
					width=300,
				),
				graph,
			),
			pn.Spacer(height=30),
		)

	@staticmethod
	def show_cytoscape(documents, generate_flag):
		Cytoscape.cytoscape_graph_cache

		if generate_flag != "true" and Cytoscape.cytoscape_graph_cache:
			print("Returning cached Cytoscape graph")
			return Cytoscape.build_layout(Cytoscape.cytoscape_graph_cache)

		if not documents:
			print("No documents found, returning empty graph.")
			empty_graph = Cytoscape(
				object=[],
				style=Cytoscape.DEFAULT_STYLE,
				root_node="",
				sizing_mode="stretch_width",
				height=600,
				css_classes=["cytoscape-container"],
			)
			Cytoscape.cytoscape_graph_cache = empty_graph
			return Cytoscape.build_layout(empty_graph)

		documents_list = ast.literal_eval(documents)
		if isinstance(documents_list, dict):
			documents_list = [documents_list]

		document_data = {
			doc["id"]: {**doc, "children": doc.get("children", {})}
			for doc in documents_list
		}

		nodes, edges = {}, []
		all_nodes, has_parents = set(), set()

		for top in document_data.values():
			Cytoscape.recurse(top, nodes, edges, all_nodes, has_parents)

		root_nodes = list(all_nodes - has_parents)
		roots_selector = ", ".join(f"#{r}" for r in root_nodes) if root_nodes else None
		elements = list(nodes.values()) + edges

		graph = Cytoscape(
			object=elements,
			style=Cytoscape.DEFAULT_STYLE,
			root_node=roots_selector,
			sizing_mode="stretch_width",
			height=600,
			css_classes=["cytoscape-container"],
		)

		Cytoscape.cytoscape_graph_cache = graph
		return Cytoscape.build_layout(graph)
