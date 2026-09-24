#!/usr/bin/env python3
"""Build the source-backed DFD Level 0 Context Diagram.

The JSON model is deliberately declarative.  This builder owns only the
shared draw.io XML vocabulary and deterministic placement; internal platform
modules are not represented as external entities in this view.
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import xml.etree.ElementTree as ET


HERE = Path(__file__).resolve().parent
DEFAULT_MODEL = HERE / "context_diagram.json"
DEFAULT_OUTPUT = HERE / "AI-Research-Experimentation-Platform-Context.drawio"


def text_value(value: str, *, bold_first: bool = False) -> str:
    """Escape text while allowing the model's explicit ``<br>`` line breaks."""

    safe = html.escape(str(value), quote=False).replace("&lt;br&gt;", "<br>")
    if bold_first:
        first, separator, rest = safe.partition("<br>")
        return f"<b>{first}</b>{separator}{rest}"
    return safe


def add_vertex(
    root: ET.Element,
    cell_id: str,
    value: str,
    style: str,
    *,
    x: float,
    y: float,
    width: float,
    height: float,
) -> None:
    cell = ET.SubElement(
        root,
        "mxCell",
        {
            "id": cell_id,
            "value": value,
            "style": style,
            "vertex": "1",
            "parent": "1",
        },
    )
    ET.SubElement(
        cell,
        "mxGeometry",
        {
            "x": str(x),
            "y": str(y),
            "width": str(width),
            "height": str(height),
            "as": "geometry",
        },
    )


def add_edge(root: ET.Element, relation: dict) -> None:
    ports = relation.get("ports", {})
    style = (
        "edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;"
        "rounded=0;html=1;whiteSpace=wrap;"
        "strokeColor=#111827;fontColor=#111827;fontFamily=Helvetica;fontSize=11;"
        "strokeWidth=1.2;endArrow=block;endFill=1;endSize=7;startArrow=none;"
    )
    for name in ("exitX", "exitY", "entryX", "entryY"):
        if name in ports:
            offset_name = name.replace("X", "Dx").replace("Y", "Dy")
            style += f"{name}={ports[name]};{offset_name}=0;"
    cell = ET.SubElement(
        root,
        "mxCell",
        {
            "id": relation["id"],
            "value": "",
            "style": style,
            "edge": "1",
            "parent": "1",
            "source": relation["from"],
            "target": relation["to"],
        },
    )
    geometry = ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
    points = relation.get("points", [])
    if points:
        array = ET.SubElement(geometry, "Array", {"as": "points"})
        for point in points:
            ET.SubElement(array, "mxPoint", {"x": str(point[0]), "y": str(point[1])})


def add_flow_label(root: ET.Element, relation: dict) -> None:
    box = relation["label_box"]
    label_style = (
        "text;html=1;whiteSpace=wrap;align=center;verticalAlign=middle;"
        "fontFamily=Helvetica;fontSize=11;fontColor=#111827;"
        "fillColor=#ffffff;strokeColor=none;opacity=100;spacing=3;"
    )
    add_vertex(
        root,
        f"{relation['id']}_label",
        text_value(relation["label"]),
        label_style,
        x=box["x"],
        y=box["y"],
        width=box["width"],
        height=box["height"],
    )


def build(model_path: Path, output_path: Path) -> None:
    model = json.loads(model_path.read_text(encoding="utf-8"))
    canvas = model["canvas"]
    system = model["system"]

    mxfile = ET.Element(
        "mxfile",
        {
            "host": "app.diagrams.net",
            "version": "31.4.5",
            "type": "device",
            "agent": "Codex drawio-skill",
        },
    )
    diagram = ET.SubElement(
        mxfile,
        "diagram",
        {
            "id": "ai-research-dfd-level-0",
            "name": model["page_name"],
            "data-source": "; ".join(model["source_documents"]),
            "data-model": model["scope_note"],
        },
    )
    graph_model = ET.SubElement(
        diagram,
        "mxGraphModel",
        {
            "grid": "1",
            "gridSize": "10",
            "page": "1",
            "pageScale": "1",
            "pageWidth": str(canvas["width"]),
            "pageHeight": str(canvas["height"]),
            "background": "#ffffff",
            "pageBackgroundColor": "#ffffff",
            "math": "0",
            "shadow": "0",
        },
    )
    root = ET.SubElement(graph_model, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    title_style = (
        "text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;"
        "fontFamily=Helvetica;fontSize=20;fontStyle=1;fontColor=#111827;"
    )
    source_style = (
        "text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;"
        "fontFamily=Helvetica;fontSize=9;fontColor=#6b7280;"
    )
    note_style = (
        "text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;"
        "fontFamily=Helvetica;fontSize=9;fontColor=#4b5563;"
    )
    add_vertex(
        root,
        "diagram_title",
        text_value(model["title"], bold_first=True),
        title_style,
        x=40,
        y=20,
        width=canvas["width"] - 80,
        height=35,
    )
    add_vertex(
        root,
        "diagram_source",
        text_value("Source: " + " • ".join(model["source_documents"])),
        source_style,
        x=40,
        y=62,
        width=canvas["width"] - 80,
        height=24,
    )

    process_style = (
        "ellipse;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
        "fillColor=#ffffff;strokeColor=#111827;strokeWidth=2.5;"
        "fontFamily=Helvetica;fontSize=18;fontColor=#111827;spacing=14;"
    )
    add_vertex(
        root,
        system["id"],
        text_value("<br>".join(system["label_lines"]), bold_first=True),
        process_style,
        x=system["x"],
        y=system["y"],
        width=system["width"],
        height=system["height"],
    )

    entity_style = (
        "rounded=0;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
        "fillColor=#ffffff;strokeColor=#111827;strokeWidth=1.5;"
        "fontFamily=Helvetica;fontSize=12;fontColor=#111827;spacing=8;"
    )
    for entity in model["external_entities"]:
        add_vertex(
            root,
            entity["id"],
            text_value("<br>".join(entity["label_lines"]), bold_first=True),
            entity_style,
            x=entity["x"],
            y=entity["y"],
            width=entity["width"],
            height=entity["height"],
        )

    for relation in model["relationships"]:
        add_edge(root, relation)
    for relation in model["relationships"]:
        add_flow_label(root, relation)

    add_vertex(
        root,
        "scope_note",
        text_value("Scope: " + model["scope_note"]),
        note_style,
        x=40,
        y=canvas["height"] - 80,
        width=canvas["width"] - 80,
        height=35,
    )
    add_vertex(
        root,
        "legend",
        text_value("Single-headed arrows = high-level data flow"),
        note_style,
        x=40,
        y=canvas["height"] - 40,
        width=canvas["width"] - 80,
        height=35,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space="  ")
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"wrote {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    build(args.model.resolve(), args.output.resolve())


if __name__ == "__main__":
    main()
