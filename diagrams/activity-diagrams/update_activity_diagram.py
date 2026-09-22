"""Apply source-backed semantic fixes to the Activity Main Flow package.

The existing XML is intentionally preserved as the layout source of truth.
This updater changes only the affected nodes/edges, keeps stable cell IDs, and
adds explicit corridors for every newly introduced cross-lane hand-off.
"""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = ROOT / "AI-Research-Experimentation-Platform-Activity-Main-Flows.drawio"


def _diagram(root: ET.Element, page_number: int) -> ET.Element:
    pages = root.findall("diagram")
    try:
        return pages[page_number - 1]
    except IndexError as exc:
        raise ValueError(f"missing activity page {page_number}") from exc


def _root(page: ET.Element) -> ET.Element:
    graph_root = page.find("./mxGraphModel/root")
    if graph_root is None:
        raise ValueError(f"page {page.get('name', '?')} has no graph root")
    return graph_root


def _cell(page: ET.Element, cell_id: str) -> ET.Element:
    cell = _root(page).find(f"mxCell[@id='{cell_id}']")
    if cell is None:
        raise ValueError(f"page {page.get('name', '?')} is missing cell {cell_id}")
    return cell


def _geometry(cell: ET.Element) -> ET.Element:
    geometry = cell.find("mxGeometry")
    if geometry is None:
        geometry = ET.SubElement(cell, "mxGeometry", {"as": "geometry"})
    return geometry


def _set_geometry(cell: ET.Element, *, x: int | None = None, y: int | None = None,
                  width: int | None = None, height: int | None = None) -> None:
    geometry = _geometry(cell)
    for key, value in (("x", x), ("y", y), ("width", width), ("height", height)):
        if value is not None:
            geometry.set(key, str(value))


def _set_value(page: ET.Element, cell_id: str, value: str) -> None:
    _cell(page, cell_id).set("value", value)


def _set_style(page: ET.Element, cell_id: str, style: str) -> None:
    _cell(page, cell_id).set("style", style)


def _add_vertex(page: ET.Element, cell_id: str, parent: str, value: str,
                style: str, x: int, y: int, width: int = 210, height: int = 72) -> None:
    root = _root(page)
    if root.find(f"mxCell[@id='{cell_id}']") is not None:
        raise ValueError(f"cell {cell_id} already exists")
    vertex = ET.Element(
        "mxCell",
        {
            "id": cell_id,
            "value": value,
            "style": style,
            "vertex": "1",
            "parent": parent,
        },
    )
    ET.SubElement(
        vertex,
        "mxGeometry",
        {"x": str(x), "y": str(y), "width": str(width), "height": str(height), "as": "geometry"},
    )
    first_edge = next((index for index, item in enumerate(root) if item.get("edge") == "1"), len(root))
    root.insert(first_edge, vertex)


def _with_ports(style: str, *, exit_x: float, exit_y: float,
                entry_x: float, entry_y: float) -> str:
    stripped = re.sub(
        r"(?:exitX|exitY|exitDx|exitDy|entryX|entryY|entryDx|entryDy)=[^;]*;",
        "",
        style,
    )
    return (
        f"{stripped}exitX={exit_x};exitY={exit_y};exitDx=0;exitDy=0;"
        f"entryX={entry_x};entryY={entry_y};entryDx=0;entryDy=0;"
    )


def _set_points(edge: ET.Element, points: list[tuple[float, float]]) -> None:
    geometry = _geometry(edge)
    for child in list(geometry):
        if child.tag == "Array":
            geometry.remove(child)
    if points:
        array = ET.SubElement(geometry, "Array", {"as": "points"})
        for x, y in points:
            ET.SubElement(array, "mxPoint", {"x": str(x), "y": str(y)})


def _set_edge(page: ET.Element, edge_id: str, source: str, target: str, *,
              value: str | None = None, points: list[tuple[float, float]] | None = None,
              ports: tuple[float, float, float, float] | None = None) -> None:
    edge = _cell(page, edge_id)
    if edge.get("edge") != "1":
        raise ValueError(f"cell {edge_id} is not an edge")
    edge.set("source", source)
    edge.set("target", target)
    if value is not None:
        edge.set("value", value)
    if ports is not None:
        edge.set("style", _with_ports(edge.get("style", ""), exit_x=ports[0], exit_y=ports[1], entry_x=ports[2], entry_y=ports[3]))
    _set_points(edge, points or [])


def _add_edge(page: ET.Element, edge_id: str, template_id: str, source: str, target: str,
              *, value: str = "", points: list[tuple[float, float]] | None = None,
              ports: tuple[float, float, float, float] | None = None) -> None:
    root = _root(page)
    if root.find(f"mxCell[@id='{edge_id}']") is not None:
        raise ValueError(f"cell {edge_id} already exists")
    template = _cell(page, template_id)
    edge = ET.Element(
        "mxCell",
        {
            "id": edge_id,
            "value": value,
            "style": template.get("style", ""),
            "edge": "1",
            "parent": template.get("parent", "1"),
            "source": source,
            "target": target,
        },
    )
    if ports is not None:
        edge.set("style", _with_ports(edge.get("style", ""), exit_x=ports[0], exit_y=ports[1], entry_x=ports[2], entry_y=ports[3]))
    ET.SubElement(edge, "mxGeometry", {"relative": "1", "as": "geometry"})
    root.append(edge)
    _set_points(edge, points or [])


def _set_lane_height(page: ET.Element, height: int) -> None:
    lane_zero = next(
        (cell.get("id", "") for cell in _root(page).findall("mxCell") if re.fullmatch(r"p\d+_lane_0", cell.get("id", ""))),
        "",
    )
    prefix = lane_zero.removesuffix("_lane_0")
    if not prefix:
        raise ValueError(f"page {page.get('name', '?')} has no numbered lanes")
    for lane_id in (f"{prefix}_lane_{lane_index}" for lane_index in range(4)):
        lane = _root(page).find(f"mxCell[@id='{lane_id}']")
        if lane is not None:
            _set_geometry(lane, height=height)


def _set_page_height(page: ET.Element, height: int) -> None:
    model = page.find("mxGraphModel")
    if model is not None:
        model.set("pageHeight", str(height))


def _update_decision_gated_loop(page: ET.Element) -> None:
    decision_style = _cell(page, "p02_stopping").get("style", "")
    action_style = _cell(page, "p02_update_state").get("style", "")
    merge_style = "rhombus;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor=#ffffff;strokeColor=#d6b656;strokeWidth=1.4;fontColor=#111827;fontFamily=Helvetica;fontSize=12;spacing=4;"

    _set_lane_height(page, 2300)
    _set_page_height(page, 2450)
    _set_value(page, "p02_note", "Evidence outcomes branch to finding, refinement / human review, or an inconclusive record.")
    _set_value(page, "p02_route_outcome", "Enough evidence?")
    _set_style(page, "p02_route_outcome", decision_style)
    _set_geometry(_cell(page, "p02_route_outcome"), y=1235, height=80)

    _add_vertex(page, "p02_enough_outcome", "p02_lane_0", "ENOUGH_EVIDENCE → Generate finding", action_style, 40, 1395)
    _add_vertex(page, "p02_refinement_decision", "p02_lane_1", "Refinement / human review?", decision_style, 40, 1395, height=80)
    _add_vertex(page, "p02_refinement_outcome", "p02_lane_2", "Refinement outcomes → Resolve scientific refinement / review", action_style, 40, 1535)
    _add_vertex(page, "p02_inconclusive_outcome", "p02_lane_3", "INCONCLUSIVE → Record outcome + limitations", action_style, 40, 1535)
    _add_vertex(page, "p02_outcome_merge", "p02_lane_1", "", merge_style, 40, 1685, height=80)

    _set_value(page, "p02_update_state", "13. Update Research State + lineage")
    _set_geometry(_cell(page, "p02_update_state"), y=1825)
    _set_geometry(_cell(page, "p02_stopping"), y=1945)
    _set_geometry(_cell(page, "p02_next_candidates"), y=2085)
    _set_geometry(_cell(page, "p02_final_report"), y=2085)
    _set_geometry(_cell(page, "p02_finish"), y=2195)

    _set_edge(page, "p02_edge_12", "p02_route_outcome", "p02_enough_outcome", value="[Yes]", points=[(485, 1500), (195, 1500)], ports=(0.25, 1.0, 0.5, 0.0))
    _add_edge(page, "p02_edge_18", "p02_edge_12", "p02_route_outcome", "p02_refinement_decision", value="[No]")
    _add_edge(page, "p02_edge_19", "p02_edge_12", "p02_refinement_decision", "p02_refinement_outcome", value="[Yes]", points=[(537.5, 1650), (775, 1650)], ports=(0.75, 1.0, 0.5, 0.0))
    _add_edge(page, "p02_edge_20", "p02_edge_12", "p02_refinement_decision", "p02_inconclusive_outcome", value="[No]", points=[(537.5, 1650), (1065, 1650)], ports=(0.75, 1.0, 0.5, 0.0))
    _add_edge(page, "p02_edge_21", "p02_edge_12", "p02_enough_outcome", "p02_outcome_merge", points=[(195, 1720), (485, 1720)], ports=(0.5, 1.0, 0.5, 0.0))
    _add_edge(page, "p02_edge_22", "p02_edge_12", "p02_refinement_outcome", "p02_outcome_merge", points=[(775, 1790), (485, 1790)], ports=(0.5, 1.0, 0.5, 0.0))
    _add_edge(page, "p02_edge_23", "p02_edge_12", "p02_inconclusive_outcome", "p02_outcome_merge", points=[(1065, 1790), (485, 1790)], ports=(0.5, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_13", "p02_outcome_merge", "p02_update_state", points=[(485, 1940), (195, 1940)], ports=(0.5, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_14", "p02_stopping", "p02_next_candidates", value="[No]")
    _set_edge(page, "p02_edge_15", "p02_next_candidates", "p02_generate_candidates", points=[(195, 2320), (24, 2320), (24, 420), (195, 420)], ports=(0.5, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_16", "p02_stopping", "p02_final_report", value="[Yes]", points=[(247.5, 2200), (1065, 2200)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_17", "p02_final_report", "p02_finish")


def _update_hypothesis_gate(page: ET.Element) -> None:
    decision_style = _cell(page, "p03_candidate_selected").get("style", "")
    _set_lane_height(page, 1500)
    _set_page_height(page, 1700)
    _set_value(page, "p03_record_decision", "6. Record original selection decision + audit metadata")
    _set_value(page, "p03_researcher_review", "7. Researcher review / override when policy requires")
    _set_geometry(_cell(page, "p03_researcher_review"), y=855)
    _add_vertex(page, "p03_human_review_required", "p03_lane_1", "Human review required?", decision_style, 40, 735, height=80)
    _set_geometry(_cell(page, "p03_candidate_selected"), y=1005)
    _set_geometry(_cell(page, "p03_activate_direction"), y=1125)
    _set_geometry(_cell(page, "p03_more_candidates"), y=1125)
    _set_geometry(_cell(page, "p03_finish"), y=1255)

    _set_edge(page, "p03_edge_06", "p03_record_decision", "p03_human_review_required")
    _set_edge(page, "p03_edge_07", "p03_researcher_review", "p03_candidate_selected", points=[(775, 1110), (485, 1110)], ports=(0.5, 1.0, 0.5, 0.0))
    _add_edge(page, "p03_edge_12", "p03_edge_07", "p03_human_review_required", "p03_researcher_review", value="[Yes]", points=[(537.5, 980), (775, 980)], ports=(0.75, 1.0, 0.5, 0.0))
    _add_edge(page, "p03_edge_13", "p03_edge_07", "p03_human_review_required", "p03_candidate_selected", value="[No]")
    _set_edge(page, "p03_edge_08", "p03_candidate_selected", "p03_activate_direction", value="[Yes]", points=[(537.5, 1250), (1065, 1250)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p03_edge_09", "p03_candidate_selected", "p03_more_candidates", value="[No]", points=[(432.5, 1250), (195, 1250)], ports=(0.25, 1.0, 0.5, 0.0))
    _set_edge(page, "p03_edge_10", "p03_more_candidates", "p03_generate_set", points=[(195, 1360), (24, 1360), (24, 420), (195, 420)], ports=(0.5, 1.0, 0.5, 0.0))
    _set_edge(page, "p03_edge_11", "p03_activate_direction", "p03_finish")


def _update_scientific_validity(page: ET.Element) -> None:
    _set_value(page, "p07_record_issue", "Record assumption issue; flag human review")
    _set_edge(page, "p07_edge_04", "p07_multiple_tests", "p07_apply_correction", points=[(432.5, 620), (485, 620)], ports=(0.25, 1.0, 0.5, 0.0))
    _set_edge(page, "p07_edge_11", "p07_record_issue", "p07_multiple_tests", points=[(1065, 570), (485, 570)], ports=(0.5, 1.0, 0.5, 1.0))


def _update_evidence_gate(page: ET.Element) -> None:
    _set_value(page, "p08_human", "NEED_HUMAN_REVIEW / Create review task")
    _set_value(page, "p08_return_outcome", "4. Record original decision + override; return resolved structured outcome")
    action_style = _cell(page, "p08_human").get("style", "")
    _add_vertex(page, "p08_review_override", "p08_lane_2", "Researcher reviews / overrides decision", action_style, 40, 845)
    _set_edge(page, "p08_edge_13", "p08_human", "p08_review_override", points=[(195, 936), (775, 936)], ports=(0.5, 1.0, 0.5, 0.0))
    _add_edge(page, "p08_edge_16", "p08_edge_13", "p08_review_override", "p08_return_outcome", points=[(775, 1075), (1065, 1075)], ports=(0.5, 1.0, 0.5, 1.0))


def update(input_path: Path = DEFAULT_INPUT, output_path: Path = DEFAULT_INPUT) -> None:
    tree = ET.parse(input_path)
    root = tree.getroot()
    _update_decision_gated_loop(_diagram(root, 2))
    _update_hypothesis_gate(_diagram(root, 3))
    _update_scientific_validity(_diagram(root, 7))
    _update_evidence_gate(_diagram(root, 8))
    ET.indent(tree, space="  ")
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"updated {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_INPUT)
    args = parser.parse_args()
    update(args.input, args.output)


if __name__ == "__main__":
    main()
