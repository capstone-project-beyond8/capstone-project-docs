#!/usr/bin/env python3
"""Build the source-backed Conceptual ERD.

The JSON model is declarative: entities sit on a fixed grid and every
relationship names its crow's-foot cardinality at both ends.  Straight
neighbours are routed automatically; longer relationships carry explicit
orthogonal waypoints so the rendered draw.io layout is deterministic.
``--check`` validates the routing geometry before anything is written.
"""

from __future__ import annotations

import argparse
import html
import json
from itertools import combinations
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


HERE = Path(__file__).resolve().parent
DEFAULT_MODEL = HERE / "platform_be_conceptual_erd.json"
DEFAULT_OUTPUT = HERE / "Platform-BE-Conceptual-ERD.drawio"

# Crow's-foot markers shipped with draw.io.
CARDINALITY = {
    "one": "ERmandOne",
    "zero_one": "ERzeroToOne",
    "many": "ERmany",
    "one_many": "ERoneToMany",
    "zero_many": "ERzeroToMany",
}
SIDE_FACTORS = {"left": (0, None), "right": (1, None), "top": (None, 0), "bottom": (None, 1)}

INK = "#111827"
MUTED = "#4b5563"
FONT = "fontFamily=Helvetica;"


def text_value(value: str, *, bold_first: bool = False) -> str:
    safe = html.escape(str(value), quote=False).replace("&lt;br&gt;", "<br>")
    if bold_first:
        first, separator, rest = safe.partition("<br>")
        return f"<b>{first}</b>{separator}{rest}"
    return safe


def fmt(number: float) -> str:
    return str(int(number)) if float(number).is_integer() else f"{number:g}"


# --------------------------------------------------------------------------
# Geometry
# --------------------------------------------------------------------------


def entity_boxes(model: dict) -> dict[str, dict]:
    grid = model["grid"]
    boxes = {}
    for entity in model["entities"]:
        boxes[entity["id"]] = {
            "x": grid["x0"] + entity["col"] * grid["dx"],
            "y": grid["y0"] + entity["row"] * grid["dy"],
            "w": grid["width"],
            "h": grid["height"],
        }
    return boxes


def default_ports(source: dict, target: dict, relation_id: str) -> tuple[list, list]:
    if source["y"] == target["y"]:
        return (["right", 0.5], ["left", 0.5]) if source["x"] < target["x"] else (["left", 0.5], ["right", 0.5])
    if source["x"] == target["x"]:
        return (["bottom", 0.5], ["top", 0.5]) if source["y"] < target["y"] else (["top", 0.5], ["bottom", 0.5])
    raise ValueError(f"{relation_id}: non-adjacent relationship needs explicit exit/entry/points")


def port_point(box: dict, side: str, position: float) -> tuple[float, float]:
    fx, fy = SIDE_FACTORS[side]
    fx = position if fx is None else fx
    fy = position if fy is None else fy
    return box["x"] + fx * box["w"], box["y"] + fy * box["h"]


def resolve(model: dict) -> list[dict]:
    """Attach ports and the full polyline (source port → waypoints → target port)."""

    boxes = entity_boxes(model)
    resolved = []
    for relation in model["relationships"]:
        source, target = boxes[relation["from"]], boxes[relation["to"]]
        if "exit" in relation:
            exit_port, entry_port = relation["exit"], relation["entry"]
        else:
            exit_port, entry_port = default_ports(source, target, relation["id"])
        polyline = [
            port_point(source, *exit_port),
            *[tuple(point) for point in relation.get("points", [])],
            port_point(target, *entry_port),
        ]
        resolved.append({**relation, "exit": exit_port, "entry": entry_port, "polyline": polyline})
    return resolved


def segments(polyline: list) -> list[tuple]:
    return list(zip(polyline, polyline[1:]))


def segment_hits_box(start: tuple, end: tuple, box: dict, pad: float = 0.5) -> bool:
    """True when an axis-aligned segment passes through a box interior."""

    x1, x2 = sorted((start[0], end[0]))
    y1, y2 = sorted((start[1], end[1]))
    left, right = box["x"] + pad, box["x"] + box["w"] - pad
    top, bottom = box["y"] + pad, box["y"] + box["h"] - pad
    return x1 < right and x2 > left and y1 < bottom and y2 > top


def crossing(a: tuple, b: tuple) -> bool:
    """Proper crossing of one horizontal and one vertical segment."""

    (ax1, ay1), (ax2, ay2) = a
    (bx1, by1), (bx2, by2) = b
    a_horizontal, b_horizontal = ay1 == ay2, by1 == by2
    if a_horizontal == b_horizontal:
        return False
    (hx1, hy), (hx2, _) = a if a_horizontal else b
    (vx, vy1), (_, vy2) = b if a_horizontal else a
    return min(hx1, hx2) < vx < max(hx1, hx2) and min(vy1, vy2) < hy < max(vy1, vy2)


def collinear_overlap(a: tuple, b: tuple) -> bool:
    (ax1, ay1), (ax2, ay2) = a
    (bx1, by1), (bx2, by2) = b
    if ay1 == ay2 == by1 == by2:
        return min(max(ax1, ax2), max(bx1, bx2)) - max(min(ax1, ax2), min(bx1, bx2)) > 0
    if ax1 == ax2 == bx1 == bx2:
        return min(max(ay1, ay2), max(by1, by2)) - max(min(ay1, ay2), min(by1, by2)) > 0
    return False


def check(model: dict, relations: list[dict]) -> tuple[list[str], list[str]]:
    boxes = entity_boxes(model)
    errors, crossings = [], []
    known = set(boxes)
    for relation in relations:
        for end in ("from", "to"):
            if relation[end] not in known:
                errors.append(f"{relation['id']}: unknown entity {relation[end]}")
        for card in ("from_card", "to_card"):
            if relation[card] not in CARDINALITY:
                errors.append(f"{relation['id']}: unknown cardinality {relation[card]}")
        for start, end in segments(relation["polyline"]):
            if start[0] != end[0] and start[1] != end[1]:
                errors.append(f"{relation['id']}: diagonal segment {start}->{end}")
            for entity_id, box in boxes.items():
                if segment_hits_box(start, end, box):
                    errors.append(f"{relation['id']}: passes through {entity_id}")
    errors += readability_errors(boxes, relations)
    for first, second in combinations(relations, 2):
        for a in segments(first["polyline"]):
            for b in segments(second["polyline"]):
                if collinear_overlap(a, b):
                    errors.append(f"{first['id']} overlaps {second['id']}")
                elif crossing(a, b):
                    crossings.append(f"{first['id']} x {second['id']}")
    return errors, crossings


# A crow's-foot marker reaches about 26px out from its entity and 12px across the line.
MARKER_ZONE = 28
PORT_GAP = 24
LANE_GAP = 16


def readability_errors(boxes: dict, relations: list[dict]) -> list[str]:
    """Markers must not touch each other, foreign lines, or run in near-parallel lanes."""

    errors = []
    ports: dict[tuple, list] = {}
    for relation in relations:
        for end, port in (("from", relation["exit"]), ("to", relation["entry"])):
            box = boxes[relation[end]]
            point = port_point(box, *port)
            ports.setdefault((relation[end], port[0]), []).append((relation["id"], point))
    for (entity_id, side), items in ports.items():
        for (first, p), (second, q) in combinations(items, 2):
            if abs(p[0] - q[0]) + abs(p[1] - q[1]) < PORT_GAP:
                errors.append(f"{first} and {second}: markers crowd {entity_id} {side}")
    for relation in relations:
        parts = segments(relation["polyline"])
        for index, (start, end) in enumerate(parts):
            for entity_id, box in boxes.items():
                own = (index == 0 and entity_id == relation["from"]) or (
                    index == len(parts) - 1 and entity_id == relation["to"]
                )
                if own:
                    continue
                zone = {"x": box["x"] - MARKER_ZONE, "y": box["y"] - MARKER_ZONE,
                        "w": box["w"] + 2 * MARKER_ZONE, "h": box["h"] + 2 * MARKER_ZONE}
                if segment_hits_box(start, end, zone):
                    errors.append(f"{relation['id']}: runs through the marker zone of {entity_id}")
    for first, second in combinations(relations, 2):
        for a in segments(first["polyline"]):
            for b in segments(second["polyline"]):
                if too_close(a, b):
                    errors.append(f"{first['id']} runs too close to {second['id']}")
    return errors


def too_close(a: tuple, b: tuple) -> bool:
    (ax1, ay1), (ax2, ay2) = a
    (bx1, by1), (bx2, by2) = b
    if ay1 == ay2 and by1 == by2 and 0 < abs(ay1 - by1) < LANE_GAP:
        return min(max(ax1, ax2), max(bx1, bx2)) - max(min(ax1, ax2), min(bx1, bx2)) > 0
    if ax1 == ax2 and bx1 == bx2 and 0 < abs(ax1 - bx1) < LANE_GAP:
        return min(max(ay1, ay2), max(by1, by2)) - max(min(ay1, ay2), min(by1, by2)) > 0
    return False


# --------------------------------------------------------------------------
# draw.io XML
# --------------------------------------------------------------------------


def add_vertex(root: ET.Element, cell_id: str, value: str, style: str, x, y, width, height) -> None:
    cell = ET.SubElement(
        root, "mxCell", {"id": cell_id, "value": value, "style": style, "vertex": "1", "parent": "1"}
    )
    ET.SubElement(
        cell,
        "mxGeometry",
        {"x": fmt(x), "y": fmt(y), "width": fmt(width), "height": fmt(height), "as": "geometry"},
    )


def edge_style(start_card: str, end_card: str) -> str:
    return (
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
        f"strokeColor={INK};strokeWidth=1.2;fontColor={INK};{FONT}fontSize=11;"
        "labelBackgroundColor=#ffffff;jumpStyle=arc;jumpSize=8;"
        f"startArrow={CARDINALITY[start_card]};startFill=0;startSize=12;"
        f"endArrow={CARDINALITY[end_card]};endFill=0;endSize=12;"
    )


def add_relationship(root: ET.Element, relation: dict) -> None:
    style = edge_style(relation["from_card"], relation["to_card"])
    for prefix, (side, position) in (("exit", relation["exit"]), ("entry", relation["entry"])):
        fx, fy = SIDE_FACTORS[side]
        style += f"{prefix}X={fmt(position if fx is None else fx)};{prefix}Y={fmt(position if fy is None else fy)};"
        style += f"{prefix}Dx=0;{prefix}Dy=0;"
    cell = ET.SubElement(
        root,
        "mxCell",
        {
            "id": relation["id"],
            # A conceptual ERD names every relationship; read the verb from `from` to `to`.
            "value": text_value(relation.get("label", "")),
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
        for x, y in points:
            ET.SubElement(array, "mxPoint", {"x": fmt(x), "y": fmt(y)})


def add_legend(root: ET.Element, legend: dict, groups: dict) -> None:
    x, y, width = legend["x"], legend["y"], legend["width"]
    add_vertex(
        root,
        "legend_frame",
        "",
        f"rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor={INK};strokeWidth=1;",
        x,
        y,
        width,
        legend["height"],
    )
    heading = f"text;html=1;align=left;verticalAlign=middle;{FONT}fontSize=12;fontStyle=1;fontColor={INK};"
    item = f"text;html=1;align=left;verticalAlign=middle;{FONT}fontSize=11;fontColor={INK};"
    add_vertex(root, "legend_title", "Crow's-foot notation (marker at an entity = how many of that entity)", heading, x + 16, y + 8, width - 32, 26)
    samples = [
        ("one", "Exactly one (1)"),
        ("zero_one", "Zero or one (0..1)"),
        ("one_many", "One or many (1..*)"),
        ("zero_many", "Zero or many (0..*)"),
    ]
    for index, (card, text) in enumerate(samples):
        column, row = divmod(index, 2)
        sx = x + 24 + column * (width / 2)
        sy = y + 62 + row * 44
        cell = ET.SubElement(
            root,
            "mxCell",
            {
                "id": f"legend_{card}",
                "value": "",
                "style": (
                    f"endArrow={CARDINALITY[card]};endFill=0;endSize=12;startArrow=none;html=1;"
                    f"strokeColor={INK};strokeWidth=1.2;"
                ),
                "edge": "1",
                "parent": "1",
            },
        )
        geometry = ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
        ET.SubElement(geometry, "mxPoint", {"x": fmt(sx), "y": fmt(sy), "as": "sourcePoint"})
        ET.SubElement(geometry, "mxPoint", {"x": fmt(sx + 90), "y": fmt(sy), "as": "targetPoint"})
        add_vertex(root, f"legend_{card}_text", text, item, sx + 104, sy - 13, width / 2 - 140, 26)
    add_vertex(
        root,
        "legend_reading",
        "Read each line from both ends: the marker next to an entity says how many of that entity "
        "relate to one instance at the other end, e.g. Project ||——o< Dataset: each Dataset belongs "
        "to exactly one Project; a Project has zero or many Datasets.",
        f"text;html=1;align=left;verticalAlign=middle;whiteSpace=wrap;{FONT}fontSize=10;fontColor={MUTED};",
        x + 16,
        y + 150,
        width - 32,
        56,
    )
    for index, (group_id, group) in enumerate(groups.items()):
        sy = y + 214 + index * 34
        add_vertex(
            root,
            f"legend_group_{group_id}",
            "",
            f"rounded=0;html=1;fillColor={group['fill']};strokeColor={INK};strokeWidth=1.2;",
            x + 24,
            sy,
            90,
            24,
        )
        add_vertex(root, f"legend_group_{group_id}_text", text_value(group["label"]), item, x + 128, sy - 1, width - 150, 26)


def add_frame(root: ET.Element, frame: dict) -> None:
    """A labelled boundary drawn behind the entities it encloses."""

    dashed = "dashed=1;dashPattern=8 4;" if frame.get("dashed") else ""
    add_vertex(
        root,
        frame["id"],
        "",
        f"rounded=0;html=1;fillColor={frame['fill']};strokeColor={INK};strokeWidth=1.6;{dashed}",
        frame["x"],
        frame["y"],
        frame["width"],
        frame["height"],
    )
    add_vertex(
        root,
        f"{frame['id']}_title",
        text_value(frame["label"], bold_first=True),
        f"text;html=1;align=left;verticalAlign=middle;whiteSpace=wrap;{FONT}fontSize=14;fontColor={INK};",
        frame.get("title_x", frame["x"] + 14),
        frame["y"] + 6,
        frame["title_width"],
        frame.get("title_height", 26),
    )


def add_note(root: ET.Element, note: dict) -> None:
    add_vertex(
        root,
        note["id"],
        text_value(note["text"], bold_first=True),
        f"text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;{FONT}fontSize=11;fontColor={INK};",
        note["x"],
        note["y"],
        note["width"],
        note["height"],
    )


def build(model: dict, relations: list[dict], output_path: Path) -> None:
    canvas = model["canvas"]
    grid = model["grid"]

    mxfile = ET.Element(
        "mxfile", {"host": "app.diagrams.net", "version": "31.4.5", "type": "device", "agent": "Codex drawio-skill"}
    )
    diagram = ET.SubElement(
        mxfile,
        "diagram",
        {
            "id": "ai-research-conceptual-erd",
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

    title_style = f"text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;{FONT}fontSize=20;fontStyle=1;fontColor={INK};"
    small_style = f"text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;{FONT}fontSize=9;fontColor={MUTED};"
    add_vertex(root, "diagram_title", text_value(model["title"], bold_first=True), title_style, 40, 18, canvas["width"] - 80, 34)
    add_vertex(
        root,
        "diagram_source",
        text_value("Source: " + " • ".join(model["source_documents"])),
        small_style,
        40,
        56,
        canvas["width"] - 80,
        22,
    )

    groups = model.get("groups", {})
    for frame in model.get("frames", []):
        add_frame(root, frame)
    for note in model.get("notes", []):
        add_note(root, note)

    for entity, box in zip(model["entities"], entity_boxes(model).values()):
        fill = groups.get(entity.get("group"), {}).get("fill", "#ffffff")
        entity_style = (
            "rounded=0;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
            f"fillColor={fill};strokeColor={INK};strokeWidth=1.5;{FONT}fontSize=13;fontStyle=1;fontColor={INK};"
        )
        add_vertex(root, entity["id"], text_value(entity["label"]), entity_style, box["x"], box["y"], grid["width"], grid["height"])

    for relation in relations:
        add_relationship(root, relation)

    add_legend(root, model["legend"], groups)
    add_vertex(
        root,
        "scope_note",
        text_value("Scope: " + model["scope_note"]),
        f"text;html=1;align=left;verticalAlign=middle;whiteSpace=wrap;{FONT}fontSize=10;fontColor={MUTED};",
        40,
        canvas["height"] - 90,
        canvas["width"] - 80,
        50,
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
    parser.add_argument("--check", action="store_true", help="validate routing only; do not write")
    args = parser.parse_args()

    model = json.loads(args.model.resolve().read_text(encoding="utf-8"))
    relations = resolve(model)
    errors, crossings = check(model, relations)
    print(f"entities={len(model['entities'])} relationships={len(relations)} crossings={len(crossings)}")
    for item in crossings:
        print(f"  crossing: {item}")
    for item in errors:
        print(f"  ERROR: {item}")
    if errors:
        sys.exit(1)
    if not args.check:
        build(model, relations, args.output.resolve())


if __name__ == "__main__":
    main()
