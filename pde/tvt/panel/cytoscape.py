import param
import panel as pn
from panel.custom import JSComponent
import json
import os

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
import { default as cytoscape} from "https://esm.sh/cytoscape"
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
        model.on('object', () => {cy.json({elements: model.object});});
        model.on('layout', () => {cy.layout({name: model.layout, roots: model.root_node || undefined}).run()});
        model.on('pan', () => {cy.pan(model.pan)});
        model.on('style', () => {cy.style().resetToDefault().append(model.style).update()});
        model.on('select_node', (node_id) => {
            cy.elements().unselect();
            const node = cy.$id(node_id);
            if(node) {
                node.select();
                cy.center(node);
            }
        });
        window.addEventListener('resize', function(event){
            cy.center();
        });
        model.on('remove', removeCy);
    });
    return div;
}
"""

    @staticmethod
    def show_cytoscape():
        pn.extension("cytoscape", sizing_mode="stretch_width")

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_path = os.path.join(base_dir, "input.json")

        with open(json_path, "r") as f:
            nodes_data = json.load(f)

        type_color_map = {
            "Requirement": "#1f77b4",
            "Design": "#ff7f0e",
            "Test": "#2ca02c",
            "Specification": "#d62728",
            "Task": "#9467bd",
            "Development": "#8c564b",
        }

        nodes = {}
        edges = []
        all_nodes = set()
        has_parents = set()

        def ensure_node_exists(node_id, data=None):
            if node_id in nodes:
                return
            node_info = {"id": node_id}
            if data:
                node_info.update(data)

            doc_type = node_info.get("Document Type", "")
            color = type_color_map.get(doc_type, "gray")

            nodes[node_id] = {
                "data": {
                    "id": node_id,
                    "label": node_id,
                    "color": color,
                },
                **({"classes": doc_type.lower()} if doc_type else {}),
            }

        def recurse(node_dict):
            node_id = node_dict["id"]
            meta = {k: v for k, v in node_dict.items() if k not in ("id", "children")}
            ensure_node_exists(node_id, meta)
            all_nodes.add(node_id)

            for child_id, child_obj in node_dict.get("children", {}).items():
                recurse(child_obj)
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

        for top in nodes_data.values():
            recurse(top)

        root_nodes = list(all_nodes - has_parents)
        roots_selector = ", ".join(f"#{r}" for r in root_nodes) if root_nodes else None

        elements = list(nodes.values()) + edges

        default_style = [
            {
                "selector": "node",
                "style": {
                    "background-color": "data(color)",
                    "label": "data(label)",
                    "color": "#fff",
                    "text-valign": "center",
                    "text-halign": "center",
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

        graph = Cytoscape(
            object=elements,
            style=default_style,
            root_node=roots_selector,
            sizing_mode="stretch_width",
            height=600,
            css_classes=["cytoscape-container"],
        )

        load_btn = pn.widgets.Button(name="Load Table", button_type="primary", width=50, height=50)

        layout = pn.Column(
            pn.Row(
                pn.Param(
                    graph,
                    parameters=["layout", "pan", "selected_nodes", "selected_edges"],
                    sizing_mode="fixed",
                    width=300,
                ),
                graph,
            ),
            pn.Row(pn.layout.HSpacer(), load_btn, pn.layout.HSpacer()),
        )
        return layout
