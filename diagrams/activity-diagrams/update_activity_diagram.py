"""Apply source-backed semantic fixes to the Activity Main Flow package.

The existing XML is intentionally preserved as the layout source of truth.
This updater changes only the affected nodes/edges, keeps stable cell IDs, and
adds explicit corridors for every newly introduced cross-lane hand-off.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
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
    existing = root.find(f"mxCell[@id='{cell_id}']")
    if existing is not None:
        existing.set("value", value)
        existing.set("style", style)
        existing.set("parent", parent)
        _set_geometry(existing, x=x, y=y, width=width, height=height)
        return
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
        _set_edge(page, edge_id, source, target, value=value, points=points, ports=ports)
        return
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


def _update_research_setup(page: ET.Element) -> None:
    _set_value(page, "p01_section", "BRD §12 — Research Setup; PRD Modules B–G, AC, AH")
    _set_value(page, "p01_upload_dataset", "3. Upload & validate dataset")
    _set_value(page, "p01_review_quality", "6. Review data quality, cleaning & versioning")
    _set_value(page, "p01_candidate_hypotheses", "10. Generate candidate hypotheses + Structured Idea Records")


def _update_decision_gated_loop(page: ET.Element) -> None:
    decision_style = _cell(page, "p02_stopping").get("style", "")
    action_style = _cell(page, "p02_update_state").get("style", "")
    merge_style = "rhombus;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor=#ffffff;strokeColor=#d6b656;strokeWidth=1.4;fontColor=#111827;fontFamily=Helvetica;fontSize=12;spacing=4;"

    _set_lane_height(page, 2600)
    _set_page_height(page, 2750)
    _set_value(page, "p02_section", "BRD §13 — Decision-Gated Research Loop; BR-64/78; PRD Modules AC–AF, AH")
    _set_value(page, "p02_note", "Tied candidates use immutable branch snapshots; shared Research State updates only after all sibling branches join.")
    _set_value(page, "p02_generate_candidates", "2. Generate candidate hypotheses / directions")
    _add_vertex(
        page,
        "p02_idea_reflection",
        "p02_lane_0",
        "3. Create Structured Idea Records + perform Reflection",
        action_style,
        40,
        315,
    )
    _set_value(page, "p02_apply_hypothesis_gate", "4. Apply Hypothesis Selection Gate (1..N candidates)")
    _add_vertex(
        page,
        "p02_tied_selection",
        "p02_lane_1",
        "Tied within tie_threshold?",
        decision_style,
        40,
        415,
        height=80,
    )
    _set_value(page, "p02_activate_hypothesis", "5. Activate single selected hypothesis")
    _set_geometry(_cell(page, "p02_activate_hypothesis"), y=535)
    _add_vertex(
        page,
        "p02_snapshot_branches",
        "p02_lane_2",
        "5. Snapshot Research State + assign branch IDs (bounded K)",
        action_style,
        40,
        535,
    )
    _add_vertex(
        page,
        "p02_selection_join",
        "p02_lane_2",
        "",
        merge_style,
        40,
        655,
        height=80,
    )
    _set_value(page, "p02_selection_join", "Join single / tied selection")
    _set_value(page, "p02_deep_reasoning", "6. Plan each selected hypothesis branch")
    _set_geometry(_cell(page, "p02_deep_reasoning"), y=775)
    _set_value(page, "p02_candidate_methods", "7. Generate candidate methods per branch")
    _set_geometry(_cell(page, "p02_candidate_methods"), y=875)
    _set_value(page, "p02_check_assumptions", "8. Check assumptions + dependencies")
    _set_geometry(_cell(page, "p02_check_assumptions"), y=975)
    _set_value(page, "p02_select_method", "9. Select valid method(s) + enforce max_total_concurrent_branches")
    _cell(page, "p02_select_method").set("parent", "p02_lane_2")
    _set_geometry(_cell(page, "p02_select_method"), y=1075)
    _set_value(page, "p02_execute_experiment", "10. Execute bounded branches in secure sandbox")
    _set_geometry(_cell(page, "p02_execute_experiment"), y=1175)
    _set_value(page, "p02_deterministic_validation", "11. Validate branch results + shared testing-family ID")
    _set_geometry(_cell(page, "p02_deterministic_validation"), y=1275)
    _set_value(page, "p02_evidence_gate", "12. Evaluate Evidence Sufficiency per branch")
    _set_geometry(_cell(page, "p02_evidence_gate"), y=1375)
    _set_value(page, "p02_route_outcome", "Evidence sufficient for this branch?")
    _set_style(page, "p02_route_outcome", decision_style)
    _set_geometry(_cell(page, "p02_route_outcome"), y=1495, height=80)

    _add_vertex(page, "p02_enough_outcome", "p02_lane_0", "ENOUGH_EVIDENCE for branch → Generate finding", action_style, 40, 1655)
    _add_vertex(page, "p02_refinement_decision", "p02_lane_1", "Refinement / human review?", decision_style, 40, 1655, height=80)
    _add_vertex(page, "p02_refinement_outcome", "p02_lane_2", "Refinement / review outcome for branch", action_style, 40, 1795)
    _add_vertex(page, "p02_inconclusive_outcome", "p02_lane_3", "INCONCLUSIVE branch → Record limitations", action_style, 40, 1795)
    _add_vertex(page, "p02_outcome_merge", "p02_lane_1", "Join all selected sibling branches", merge_style, 40, 1945, height=80)

    _set_value(page, "p02_update_state", "14. Update shared Research State + lineage after join")
    _set_geometry(_cell(page, "p02_update_state"), y=2085)
    _set_value(page, "p02_stopping", "Stopping criteria met across cumulative branch budgets?")
    _set_geometry(_cell(page, "p02_stopping"), y=2205)
    _set_value(page, "p02_next_candidates", "15. Generate next candidate set")
    _set_geometry(_cell(page, "p02_next_candidates"), y=2345)
    _set_value(page, "p02_final_report", "16. Generate final research report / output handoff")
    _set_geometry(_cell(page, "p02_final_report"), y=2345)
    _set_geometry(_cell(page, "p02_finish"), y=2455)

    _set_edge(page, "p02_edge_02", "p02_generate_candidates", "p02_idea_reflection")
    _add_edge(page, "p02_edge_24", "p02_edge_02", "p02_idea_reflection", "p02_apply_hypothesis_gate", points=[(247.5, 545), (485, 545)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_03", "p02_apply_hypothesis_gate", "p02_tied_selection")
    _add_edge(page, "p02_edge_25", "p02_edge_03", "p02_tied_selection", "p02_snapshot_branches", value="[Yes]", points=[(537.5, 660), (775, 660)], ports=(0.75, 1.0, 0.5, 0.0))
    _add_edge(page, "p02_edge_26", "p02_edge_03", "p02_tied_selection", "p02_activate_hypothesis", value="[No]")
    _add_edge(page, "p02_edge_27", "p02_edge_25", "p02_snapshot_branches", "p02_selection_join")
    _add_edge(page, "p02_edge_28", "p02_edge_25", "p02_activate_hypothesis", "p02_selection_join", points=[(537.5, 770), (775, 770)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_04", "p02_selection_join", "p02_deep_reasoning")
    _set_edge(page, "p02_edge_05", "p02_deep_reasoning", "p02_candidate_methods")
    _set_edge(page, "p02_edge_06", "p02_candidate_methods", "p02_check_assumptions", points=[(827.5, 1100), (1065, 1100)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_07", "p02_check_assumptions", "p02_select_method", points=[(1065, 1205), (775, 1205)], ports=(0.5, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_08", "p02_select_method", "p02_execute_experiment", points=[(827.5, 1300), (1065, 1300)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_09", "p02_execute_experiment", "p02_deterministic_validation")
    _set_edge(page, "p02_edge_10", "p02_deterministic_validation", "p02_evidence_gate", points=[(1065, 1505), (485, 1505)], ports=(0.5, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_11", "p02_evidence_gate", "p02_route_outcome")
    _set_edge(page, "p02_edge_12", "p02_route_outcome", "p02_enough_outcome", value="[Yes]", points=[(432.5, 1760), (195, 1760)], ports=(0.25, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_18", "p02_route_outcome", "p02_refinement_decision", value="[No]")
    _set_edge(page, "p02_edge_19", "p02_refinement_decision", "p02_refinement_outcome", value="[Yes]", points=[(537.5, 1910), (775, 1910)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_20", "p02_refinement_decision", "p02_inconclusive_outcome", value="[No]", points=[(537.5, 1910), (1065, 1910)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_21", "p02_enough_outcome", "p02_outcome_merge", points=[(195, 1920), (485, 1920)], ports=(0.5, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_22", "p02_refinement_outcome", "p02_outcome_merge", points=[(775, 2050), (485, 2050)], ports=(0.5, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_23", "p02_inconclusive_outcome", "p02_outcome_merge", points=[(1065, 2050), (485, 2050)], ports=(0.5, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_13", "p02_outcome_merge", "p02_update_state", points=[(432.5, 2200), (195, 2200)], ports=(0.25, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_14", "p02_stopping", "p02_next_candidates", value="[No]")
    _set_edge(page, "p02_edge_15", "p02_next_candidates", "p02_generate_candidates", points=[(195, 2600), (24, 2600), (24, 420), (195, 420)], ports=(0.5, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_16", "p02_stopping", "p02_final_report", value="[Yes]", points=[(247.5, 2460), (1065, 2460)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p02_edge_17", "p02_final_report", "p02_finish")


def _update_hypothesis_gate(page: ET.Element) -> None:
    decision_style = _cell(page, "p03_candidate_selected").get("style", "")
    action_style = _cell(page, "p03_record_decision").get("style", "")
    merge_style = "rhombus;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor=#ffffff;strokeColor=#d6b656;strokeWidth=1.4;fontColor=#111827;fontFamily=Helvetica;fontSize=12;spacing=4;"

    _set_lane_height(page, 2200)
    _set_page_height(page, 2350)
    _set_value(page, "p03_section", "BRD §14 — Hypothesis Generation & Selection; BR-64/65/78; PRD Modules AD, AH")
    _set_value(page, "p03_load_state", "1. Load active Research State")
    _set_value(page, "p03_generate_set", "2. Generate candidate hypotheses / directions")
    _add_vertex(
        page,
        "p03_idea_record",
        "p03_lane_0",
        "3. Create Structured Idea Record",
        action_style,
        40,
        315,
    )
    _add_vertex(
        page,
        "p03_reflection",
        "p03_lane_0",
        "4. Perform Reflection Round",
        action_style,
        40,
        415,
    )
    _add_vertex(
        page,
        "p03_novelty",
        "p03_lane_0",
        "5. Assess Novelty (source/context available; else Not Assessed)",
        action_style,
        40,
        515,
    )
    _set_value(page, "p03_receive_candidates", "6. Send Research State + Candidate Set to Structured Decision Gate")
    _set_geometry(_cell(page, "p03_receive_candidates"), y=615)
    _set_value(
        page,
        "p03_evaluate_candidates",
        "7. Evaluate candidates<br>Relevance • Testability • Evidence support<br>Feasibility • Confidence / uncertainty",
    )
    _set_geometry(_cell(page, "p03_evaluate_candidates"), y=715, height=80)
    _set_value(page, "p03_rank_select", "8. Evaluate numeric decision score + confidence separately")
    _set_geometry(_cell(page, "p03_rank_select"), y=815)
    _add_vertex(page, "p03_tied_selection", "p03_lane_1", "Tied within tie_threshold?", decision_style, 40, 915, height=80)
    _add_vertex(
        page,
        "p03_single_candidate",
        "p03_lane_1",
        "9. Select one clear winner",
        action_style,
        0,
        1035,
        width=140,
        height=80,
    )
    _add_vertex(
        page,
        "p03_bounded_candidates",
        "p03_lane_1",
        "9. Select bounded tied candidates (1..max_parallel_candidates)",
        action_style,
        150,
        1035,
        width=140,
        height=100,
    )
    _add_vertex(page, "p03_selection_merge", "p03_lane_1", "Join selected candidate set", merge_style, 40, 1155, height=80)
    _set_value(page, "p03_record_decision", "10. Record score, confidence, tie threshold, tied candidates + audit metadata")
    _set_geometry(_cell(page, "p03_record_decision"), y=1275)
    _set_value(page, "p03_candidate_selected", "Candidate selection viable?")
    _set_geometry(_cell(page, "p03_candidate_selected"), y=1395)
    _add_vertex(page, "p03_human_review_required", "p03_lane_1", "Human review required?", decision_style, 40, 1515, height=80)
    _set_value(page, "p03_more_candidates", "11. Generate more candidates / adjust context")
    _set_geometry(_cell(page, "p03_more_candidates"), y=1515)
    _set_value(page, "p03_researcher_review", "12. Researcher review / override when policy requires")
    _set_geometry(_cell(page, "p03_researcher_review"), y=1635)
    _set_value(page, "p03_activate_direction", "13. Activate selected hypothesis branch(es) + immutable snapshots")
    _set_geometry(_cell(page, "p03_activate_direction"), y=1755)
    _set_geometry(_cell(page, "p03_finish"), y=1885)

    _set_edge(page, "p03_edge_01", "p03_load_state", "p03_generate_set")
    _set_edge(page, "p03_edge_02", "p03_generate_set", "p03_idea_record")
    _set_edge(page, "p03_edge_03", "p03_novelty", "p03_receive_candidates", points=[(247.5, 745), (485, 745)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p03_edge_04", "p03_receive_candidates", "p03_evaluate_candidates")
    _set_edge(page, "p03_edge_05", "p03_evaluate_candidates", "p03_rank_select")
    _set_edge(page, "p03_edge_14", "p03_idea_record", "p03_reflection")
    _set_edge(page, "p03_edge_15", "p03_reflection", "p03_novelty")
    _set_edge(page, "p03_edge_16", "p03_tied_selection", "p03_bounded_candidates", value="[Yes]", points=[(537.5, 1160), (560, 1160)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p03_edge_17", "p03_tied_selection", "p03_single_candidate", value="[No]", points=[(432.5, 1160), (410, 1160)], ports=(0.25, 1.0, 0.5, 0.0))
    _set_edge(page, "p03_edge_18", "p03_bounded_candidates", "p03_selection_merge")
    _set_edge(page, "p03_edge_19", "p03_single_candidate", "p03_selection_merge")
    _set_edge(page, "p03_edge_06", "p03_selection_merge", "p03_record_decision")
    _set_edge(page, "p03_edge_07", "p03_record_decision", "p03_candidate_selected")
    _add_edge(page, "p03_edge_20", "p03_edge_07", "p03_candidate_selected", "p03_human_review_required", value="[Yes]")
    _set_edge(page, "p03_edge_09", "p03_candidate_selected", "p03_more_candidates", value="[No]", points=[(432.5, 1640), (195, 1640)], ports=(0.25, 1.0, 0.5, 0.0))
    _set_edge(page, "p03_edge_10", "p03_more_candidates", "p03_generate_set", points=[(195, 1740), (24, 1740), (24, 420), (195, 420)], ports=(0.5, 1.0, 0.5, 0.0))
    _set_edge(page, "p03_edge_12", "p03_human_review_required", "p03_researcher_review", value="[Yes]", points=[(537.5, 1760), (775, 1760)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p03_edge_13", "p03_human_review_required", "p03_activate_direction", value="[No]", points=[(537.5, 1760), (1140, 1760), (1140, 1870), (1065, 1870)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p03_edge_08", "p03_researcher_review", "p03_activate_direction", points=[(827.5, 1880), (1065, 1880)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p03_edge_11", "p03_activate_direction", "p03_finish")


def _update_execution_validation(page: ET.Element) -> None:
    action_style = _cell(page, "p04_result_package").get("style", "")
    _set_value(page, "p04_section", "BRD §13 / §16.1 — Execution and Scientific Validation; PRD Modules J–M, K, BR-78")
    _set_value(page, "p04_receive_plan", "1. Receive approved plan for selected hypothesis branch")
    _set_value(page, "p04_check_assumptions", "2. Load immutable Research State snapshot + branch ID")
    _set_value(page, "p04_assumptions_valid", "3. Assumptions valid?")
    _set_value(page, "p04_revise_plan", "Revise branch plan (adjust method / parameters)")
    _set_value(page, "p04_select_method", "4. Select method + enforce total branch cap")
    _set_value(page, "p04_prepare_environment", "5. Prepare branch execution environment<br>(secure sandbox + dependencies)")
    _set_value(page, "p04_run_experiment", "6. Run branch experiment")
    _set_value(page, "p04_collect_results", "7. Collect branch output + artifacts")
    _set_value(page, "p04_scientific_validation", "8. Validate branch results + shared testing-family ID")
    _set_value(page, "p04_result_package", "9. Create structured result package + branch metadata")
    _set_lane_height(page, 1500)
    _set_page_height(page, 1750)
    _add_vertex(
        page,
        "p04_return_branch",
        "p04_lane_3",
        "10. Return branch outcome to sibling join / Research State updater",
        action_style,
        40,
        1105,
    )
    _set_geometry(_cell(page, "p04_finish"), y=1235)
    _add_edge(page, "p04_edge_12", "p04_edge_11", "p04_result_package", "p04_return_branch")
    _add_edge(page, "p04_edge_13", "p04_edge_11", "p04_return_branch", "p04_finish")


def _update_method_selection(page: ET.Element) -> None:
    action_style = _cell(page, "p05_check_assumptions").get("style", "")
    _set_value(page, "p05_section", "BRD §15 — Method Selection; PRD Modules H–J, K; BRule-36")
    _set_value(page, "p05_capture_question", "1. Receive selected branch plan(s) + method context")
    _set_value(page, "p05_generate_methods", "4. Generate candidate methods per branch")
    _set_value(page, "p05_check_assumptions", "5. Check assumptions for each branch")
    _add_vertex(
        page,
        "p05_check_branch_cap",
        "p05_lane_2",
        "6. Enforce max_total_concurrent_branches (hypothesis × method)",
        action_style,
        40,
        615,
    )
    _set_geometry(_cell(page, "p05_suitable"), y=715)
    _set_geometry(_cell(page, "p05_selected"), y=835)
    _set_geometry(_cell(page, "p05_alternative"), y=835)
    _set_geometry(_cell(page, "p05_recheck"), y=935)
    _set_geometry(_cell(page, "p05_finish"), y=1055)
    _set_lane_height(page, 1500)
    _set_page_height(page, 1750)
    _set_edge(page, "p05_edge_05", "p05_check_assumptions", "p05_check_branch_cap")
    _add_edge(page, "p05_edge_11", "p05_edge_05", "p05_check_branch_cap", "p05_suitable")
    _set_edge(page, "p05_edge_06", "p05_suitable", "p05_selected", value="[Yes]", points=[(827.5, 960), (1065, 960)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p05_edge_07", "p05_suitable", "p05_alternative", value="[No]", points=[(722.5, 960), (485, 960)], ports=(0.25, 1.0, 0.5, 0.0))
    _set_edge(page, "p05_edge_08", "p05_alternative", "p05_recheck", points=[(537.5, 1060), (775, 1060)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p05_edge_09", "p05_recheck", "p05_suitable")
    _set_edge(page, "p05_edge_10", "p05_selected", "p05_finish")


def _update_provenance(page: ET.Element) -> None:
    _set_value(page, "p06_section", "BRD §16 — Research Finding Verification; PRD Modules Q, X, Y, Z, BR-78")
    _set_value(page, "p06_retrieve_hypothesis", "3. Retrieve hypothesis + selection decision")
    _set_value(page, "p06_retrieve_experiment", "4. Retrieve branch snapshot + experiment plan")
    _set_value(page, "p06_retrieve_dataset", "5. Retrieve dataset version + Research State lineage")
    _set_value(page, "p06_retrieve_method", "6. Retrieve method + assumptions + testing-family ID")
    _set_value(page, "p06_retrieve_code", "7. Retrieve code / query + branch metadata")
    _set_value(page, "p06_retrieve_raw", "8. Retrieve raw output + artifacts")
    _set_value(page, "p06_retrieve_statistical", "9. Retrieve statistical result + tied-selection metadata")
    _set_value(page, "p06_retrieve_snapshot", "10. Retrieve reproducibility snapshot + co-selected siblings")


def _update_scientific_validity(page: ET.Element) -> None:
    _set_value(page, "p07_section", "BRD §16.1 — Scientific Validity Guard; PRD Modules M–P, BR-49/78")
    _set_value(page, "p07_record_issue", "Record assumption issue; flag human review")
    _set_value(page, "p07_multiple_tests", "Multiple tests or tied sibling branches?")
    _set_value(page, "p07_apply_correction", "Apply Holm / FDR across shared testing-family ID")
    _set_value(page, "p07_effect_ci", "Calculate effect size + confidence interval per branch")
    _set_value(page, "p07_validation_record", "Create Scientific Validation Record + testing-family membership")
    _set_edge(page, "p07_edge_04", "p07_multiple_tests", "p07_apply_correction", points=[(247.5, 590), (300, 590), (300, 620), (485, 620)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p07_edge_11", "p07_record_issue", "p07_multiple_tests", points=[(1065, 460), (320, 460), (320, 480), (195, 480)], ports=(0.5, 0.0, 0.5, 0.0))


def _update_evidence_gate(page: ET.Element) -> None:
    decision_style = "rhombus;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor=#fff2cc;strokeColor=#d6b656;strokeWidth=1.4;fontColor=#111827;fontFamily=Helvetica;fontSize=12;spacing=4;"
    _set_value(page, "p08_lane_2", "Researcher")
    _set_value(page, "p08_human", "NEED_HUMAN_REVIEW / Create review task")
    _set_value(page, "p08_note", "Per-branch decisions wait for all siblings; incompatible outcomes route to researcher review.")
    _set_value(page, "p08_section", "BRD §16.1.1 — Evidence Sufficiency Gate; PRD Module AE, BR-61/78")
    _set_value(page, "p08_receive_facts", "1. Receive per-branch validation facts + active Research State")
    _set_value(page, "p08_evaluate_evidence", "2. Evaluate evidence per branch<br>Statistical evidence • assumptions • consistency<br>Strength • uncertainty • replication • conflicts")
    _set_value(page, "p08_make_decision", "3. Make structured per-branch evidence decision")
    _set_value(page, "p08_enough", "ENOUGH_EVIDENCE per branch<br>Generate finding")
    _set_value(page, "p08_need_more", "NEED_MORE_EVIDENCE<br>Plan next experiment")
    _set_value(page, "p08_alternative", "TRY_ALTERNATIVE_METHOD<br>Re-plan with different method")
    _set_value(page, "p08_replicate", "REPLICATE<br>Run replication experiment")
    _set_value(page, "p08_inconclusive", "INCONCLUSIVE<br>Record as inconclusive")
    _add_vertex(page, "p08_sibling_compatible", "p08_lane_1", "Sibling outcomes compatible?", decision_style, 40, 785, height=80)
    _set_value(page, "p08_review_override", "Researcher reviews / resolves incompatible sibling outcomes")
    _set_geometry(_cell(page, "p08_human"), y=905)
    _set_geometry(_cell(page, "p08_review_override"), y=1105)
    _set_value(page, "p08_return_outcome", "5. Record per-branch decisions + sibling compatibility; update shared state after join")
    _set_geometry(_cell(page, "p08_return_outcome"), y=1235)
    _set_geometry(_cell(page, "p08_finish"), y=1365)
    _set_lane_height(page, 1650)
    _set_page_height(page, 1900)
    action_style = _cell(page, "p08_human").get("style", "")
    _set_style(page, "p08_review_override", action_style)
    _set_edge(page, "p08_edge_09", "p08_enough", "p08_sibling_compatible", points=[(247.5, 720), (700, 720), (700, 930), (485, 930)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p08_edge_10", "p08_need_more", "p08_sibling_compatible", points=[(432.5, 720), (720, 720), (720, 930), (485, 930)], ports=(0.25, 1.0, 0.5, 0.0))
    _set_edge(page, "p08_edge_11", "p08_alternative", "p08_sibling_compatible", points=[(827.5, 720), (740, 720), (740, 930), (485, 930)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p08_edge_12", "p08_replicate", "p08_sibling_compatible", points=[(1065, 720), (760, 720), (760, 930), (485, 930)], ports=(0.5, 1.0, 0.5, 0.0))
    _set_edge(page, "p08_edge_14", "p08_inconclusive", "p08_sibling_compatible")
    _set_edge(page, "p08_edge_07", "p08_make_decision", "p08_human", points=[(380, 516), (30, 516), (30, 1030), (195, 1030)], ports=(0.0, 0.5, 0.5, 0.0))
    _set_edge(page, "p08_edge_08", "p08_make_decision", "p08_inconclusive", points=[(380, 516), (80, 516), (80, 790), (485, 790)], ports=(0.0, 0.5, 0.5, 0.0))
    _set_edge(page, "p08_edge_13", "p08_human", "p08_review_override", points=[(247.5, 1190), (775, 1190)], ports=(0.75, 1.0, 0.5, 0.0))
    _add_edge(page, "p08_edge_17", "p08_edge_09", "p08_sibling_compatible", "p08_return_outcome", value="[Yes]", points=[(537.5, 1160), (1065, 1160)], ports=(0.75, 1.0, 0.5, 0.0))
    _add_edge(page, "p08_edge_18", "p08_edge_09", "p08_sibling_compatible", "p08_review_override", value="[No]", points=[(537.5, 1160), (775, 1160)], ports=(0.75, 1.0, 0.5, 0.0))
    _set_edge(page, "p08_edge_15", "p08_return_outcome", "p08_finish")
    _set_edge(page, "p08_edge_16", "p08_review_override", "p08_return_outcome", points=[(880, 1340), (1065, 1340)], ports=(0.5, 1.0, 0.5, 0.0))


def _update_dependency_conflict(page: ET.Element) -> None:
    _set_value(page, "p09_section", "BRD §16.2 — Dependency & Conflict Handling; PRD Modules S–T, BR-51/53/78")
    _set_value(page, "p09_load_f1", "1. Load finding F1 + sibling / co-selection state")
    _set_value(page, "p09_generate_h2", "2. Generate candidate H2 / inspect sibling findings")
    _set_value(page, "p09_record_f2", "4. Record all valid findings F2…Fn")
    _set_value(page, "p09_conflict", "Conflict on the same hypothesis?")
    _set_value(page, "p09_mark_conflict", "Preserve valid sibling findings + create co_selected_with edges")
    _set_value(page, "p09_review_conflict", "Researcher / reviewer examines same-hypothesis conflict")
    _set_value(page, "p09_update_state", "Update dependency state without merging valid sibling findings")
    _set_value(page, "p09_mark_downstream", "Mark only affected descendants as Needs re-validation")
    _set_edge(
        page,
        "p09_edge_05",
        "p09_conflict",
        "p09_update_state",
        value="[No]",
        points=[(380, 780), (30, 780), (30, 1400), (195, 1400)],
        ports=(0.0, 1.0, 0.5, 0.0),
    )
    _set_edge(
        page,
        "p09_edge_09",
        "p09_invalidated",
        "p09_update_state",
        value="[No]",
        points=[(380, 1120), (330, 1120), (330, 1400), (195, 1400)],
        ports=(0.0, 0.5, 0.5, 0.0),
    )


def _update_evaluation(page: ET.Element) -> None:
    _set_value(page, "p10_lane_0", "Researcher / Project Manager / System Administrator")
    _set_value(page, "p10_section", "BRD §17 — Evaluation; PRD Modules AA/AG, BR-63/78")
    _set_value(page, "p10_select_task", "1. Select benchmark task + single/tied-selection configuration")
    _set_value(page, "p10_load_context", "3. Load research question / hypothesis + tied-selection config")
    _set_value(page, "p10_collect_decisions", "6. Collect decision scores, confidence, thresholds + overrides")
    _set_value(page, "p10_collect_findings", "7. Collect findings incl. valid sibling findings")
    _set_value(page, "p10_score_run", "9. Score gate quality + numeric decision-score calibration")
    _set_value(page, "p10_aggregate", "10. Aggregate tied-selection frequency / bounded correctness / cost")
    _set_value(page, "p10_compare", "11. Compare single-candidate vs tied-selection + ablation")
    _set_value(page, "p10_report", "12. Generate evaluation report")


def _new_final_outputs_page(template: ET.Element) -> ET.Element:
    page = deepcopy(template)
    page.set("id", "activity-page-11-final-outputs")
    page.set("name", "Final Outputs & Manuscript — Main Flow")
    page.set("data-source", "BRD §17.1 / BR-73–75; PRD Module AH")
    model = page.find("mxGraphModel")
    if model is None:
        raise ValueError("activity template has no mxGraphModel")
    model.set("pageHeight", "1850")
    graph_root = model.find("root")
    if graph_root is None:
        raise ValueError("activity template has no graph root")
    for child in list(graph_root):
        if child.tag == "mxCell" and child.get("id") not in {"0", "1"}:
            graph_root.remove(child)

    title_style = _cell(template, "p10_title").get("style", "")
    section_style = _cell(template, "p10_section").get("style", "")
    scope_style = _cell(template, "p10_scope").get("style", "")
    lane_style = _cell(template, "p10_lane_0").get("style", "")
    action_style = _cell(template, "p10_select_task").get("style", "")
    decision_style = _cell(template, "p10_runs_completed").get("style", "")
    start_style = _cell(template, "p10_start").get("style", "")
    finish_style = _cell(template, "p10_finish").get("style", "")
    finish_inner_style = _cell(template, "p10_finish_inner").get("style", "")
    edge_style = _cell(template, "p10_edge_00").get("style", "")
    edge_template = "p11_edge_template"
    template_edge = ET.Element(
        "mxCell",
        {"id": edge_template, "style": edge_style, "edge": "1", "parent": "1"},
    )
    ET.SubElement(template_edge, "mxGeometry", {"relative": "1", "as": "geometry"})
    graph_root.append(template_edge)
    merge_style = "rhombus;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor=#ffffff;strokeColor=#d6b656;strokeWidth=1.4;fontColor=#111827;fontFamily=Helvetica;fontSize=12;spacing=4;"

    _add_vertex(page, "p11_title", "1", "Final Outputs & Manuscript — Main Flow", title_style, 50, 18, 1160, 28)
    _add_vertex(page, "p11_section", "1", "BRD §17.1 / BR-73–75; PRD Module AH", section_style, 50, 48, 1160, 22)
    _add_vertex(page, "p11_scope", "1", "Primary flow with core decisions/loops; exception flows excluded. Approval rejection returns to revision and automated review.", scope_style, 50, 78, 1160, 20)
    lanes = [
        ("p11_lane_0", "Researcher", 50),
        ("p11_lane_1", "Output & Manuscript Agent", 340),
        ("p11_lane_2", "Figure / Report Services", 630),
        ("p11_lane_3", "Approval & Reproducibility Store", 920),
    ]
    for lane_id, label, x in lanes:
        _add_vertex(page, lane_id, "1", label, lane_style, x, 145, 290, 1650)

    _add_vertex(page, "p11_start", "p11_lane_0", "", start_style, 133, 45, 24, 24)
    actions = [
        ("p11_receive_findings", "p11_lane_0", "1. Receive validated final findings", 40, 115, 210, 72),
        ("p11_generate_figures", "p11_lane_2", "2. Generate figures + tables", 40, 215, 210, 72),
        ("p11_aggregate_figures", "p11_lane_2", "3. Aggregate figures + visual feedback", 40, 315, 210, 72),
        ("p11_generate_report", "p11_lane_1", "4. Generate research report", 40, 415, 210, 72),
        ("p11_manuscript_requested", "p11_lane_1", "Manuscript requested?", 40, 515, 210, 80),
        ("p11_generate_manuscript", "p11_lane_1", "5. Generate manuscript draft + verify numbers / citations", 40, 655, 210, 80),
        ("p11_automated_review", "p11_lane_1", "6. Run automated manuscript review", 40, 795, 210, 72),
        ("p11_external_use", "p11_lane_1", "External use / export requested?", 40, 905, 210, 80),
        ("p11_researcher_approval", "p11_lane_0", "Researcher review: approved?", 40, 1045, 210, 80),
        ("p11_revise_draft", "p11_lane_1", "Revise manuscript draft / request changes", 40, 1045, 210, 80),
        ("p11_package_merge", "p11_lane_3", "Join report-only / approved manuscript paths", 40, 1215, 210, 80),
        ("p11_repro_package", "p11_lane_3", "7. Generate reproducibility package", 40, 1335, 210, 72),
    ]
    for cell_id, parent, value, x, y, width, height in actions:
        style = decision_style if cell_id in {"p11_manuscript_requested", "p11_external_use", "p11_researcher_approval"} else merge_style if cell_id == "p11_package_merge" else action_style
        _add_vertex(page, cell_id, parent, value, style, x, y, width, height)
    _add_vertex(page, "p11_finish", "p11_lane_3", "", finish_style, 130, 1470, 30, 30)
    _add_vertex(page, "p11_finish_inner", "p11_finish", "", finish_inner_style, 6, 6, 18, 18)

    _add_edge(page, "p11_edge_00", edge_template, "p11_start", "p11_receive_findings")
    _add_edge(page, "p11_edge_01", edge_template, "p11_receive_findings", "p11_generate_figures", points=[(247.5, 332), (775, 332)], ports=(0.75, 1.0, 0.5, 0.0))
    _add_edge(page, "p11_edge_02", edge_template, "p11_generate_figures", "p11_aggregate_figures")
    _add_edge(page, "p11_edge_03", edge_template, "p11_aggregate_figures", "p11_generate_report", points=[(827.5, 532), (485, 532)], ports=(0.75, 1.0, 0.5, 0.0))
    _add_edge(page, "p11_edge_04", edge_template, "p11_generate_report", "p11_manuscript_requested")
    _add_edge(page, "p11_edge_05", edge_template, "p11_manuscript_requested", "p11_package_merge", value="[No]", points=[(537.5, 760), (1195, 760), (1195, 1360), (1065, 1360)], ports=(0.75, 1.0, 0.5, 0.0))
    _add_edge(page, "p11_edge_06", edge_template, "p11_manuscript_requested", "p11_generate_manuscript", value="[Yes]")
    _add_edge(page, "p11_edge_07", edge_template, "p11_generate_manuscript", "p11_automated_review")
    _add_edge(page, "p11_edge_08", edge_template, "p11_automated_review", "p11_external_use")
    _add_edge(page, "p11_edge_09", edge_template, "p11_external_use", "p11_package_merge", value="[No]", points=[(537.5, 1150), (1195, 1150), (1195, 1360), (1065, 1360)], ports=(0.75, 1.0, 0.5, 0.0))
    _add_edge(page, "p11_edge_10", edge_template, "p11_external_use", "p11_researcher_approval", value="[Yes]", points=[(380, 1150), (195, 1150)], ports=(0.0, 1.0, 0.5, 0.0))
    _add_edge(page, "p11_edge_11", edge_template, "p11_researcher_approval", "p11_package_merge", value="[Yes]", points=[(247.5, 1270), (330, 1270), (1195, 1270), (1195, 1360), (1065, 1360)], ports=(0.75, 1.0, 0.5, 0.0))
    _add_edge(page, "p11_edge_14", edge_template, "p11_researcher_approval", "p11_revise_draft", value="[No]", points=[(195, 1290), (485, 1290)], ports=(0.5, 1.0, 0.5, 1.0))
    _add_edge(page, "p11_edge_15", edge_template, "p11_revise_draft", "p11_automated_review", value="[Revision submitted]", ports=(0.5, 1.0, 0.5, 1.0))
    _add_edge(page, "p11_edge_12", edge_template, "p11_package_merge", "p11_repro_package")
    _add_edge(page, "p11_edge_13", edge_template, "p11_repro_package", "p11_finish")
    graph_root.remove(template_edge)
    return page


def _append_final_outputs_page(root: ET.Element, template: ET.Element) -> None:
    for page in list(root.findall("diagram")):
        if page.get("name") == "Final Outputs & Manuscript — Main Flow":
            root.remove(page)
    root.append(_new_final_outputs_page(template))


def update(input_path: Path = DEFAULT_INPUT, output_path: Path = DEFAULT_INPUT) -> None:
    tree = ET.parse(input_path)
    root = tree.getroot()
    _update_research_setup(_diagram(root, 1))
    _update_decision_gated_loop(_diagram(root, 2))
    _update_hypothesis_gate(_diagram(root, 3))
    _update_execution_validation(_diagram(root, 4))
    _update_method_selection(_diagram(root, 5))
    _update_provenance(_diagram(root, 6))
    _update_scientific_validity(_diagram(root, 7))
    _update_evidence_gate(_diagram(root, 8))
    _update_dependency_conflict(_diagram(root, 9))
    _update_evaluation(_diagram(root, 10))
    _append_final_outputs_page(root, _diagram(root, 10))
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
