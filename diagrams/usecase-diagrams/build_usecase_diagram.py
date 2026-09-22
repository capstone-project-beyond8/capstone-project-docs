"""Build the consolidated Use Case diagram in a clean, editable layout.

The page is one white UML canvas with a single system boundary, lightweight
domain cards, external actors on both sides, readable oval use cases, solid
actor associations, and dashed include/extend relations. Mermaid snippets are
used only as relationship input; the delivered artifact remains editable
draw.io XML.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "AI-Research-Experimentation-Platform-Use-Case.drawio"

OUTER = {"x": 300.0, "y": 90.0, "w": 2300.0, "h": 2550.0}
PRIMARY_W = 300.0
PRIMARY_H = 78.0
HELPER_H = 54.0

def fmt(number: float) -> str:
    return str(int(number)) if number.is_integer() else f"{number:g}"


def cell(
    root: ET.Element,
    cell_id: str,
    parent: str,
    *,
    value: str = "",
    style: str = "",
    vertex: bool = False,
    edge: bool = False,
    x: float | None = None,
    y: float | None = None,
    width: float | None = None,
    height: float | None = None,
    source: str | None = None,
    target: str | None = None,
) -> ET.Element:
    attrs = {"id": cell_id, "parent": parent, "style": style, "value": value}
    if vertex:
        attrs["vertex"] = "1"
    if edge:
        attrs["edge"] = "1"
    if source:
        attrs["source"] = source
    if target:
        attrs["target"] = target
    node = ET.SubElement(root, "mxCell", attrs)
    if x is not None or y is not None or width is not None or height is not None:
        geometry = ET.SubElement(node, "mxGeometry", {"as": "geometry"})
        if x is not None:
            geometry.set("x", fmt(x))
        if y is not None:
            geometry.set("y", fmt(y))
        if width is not None:
            geometry.set("width", fmt(width))
        if height is not None:
            geometry.set("height", fmt(height))
    return node


def text_style(size: int, *, align: str = "left", color: str = "#111827") -> str:
    return (
        "text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;"
        f"align={align};verticalAlign=middle;rounded=0;"
        f"fontColor={color};fontFamily=Helvetica;fontSize={size};"
        "labelBackgroundColor=#ffffff;"
    )


def primary_style() -> str:
    return (
        "shape=ellipse;perimeter=ellipsePerimeter;whiteSpace=wrap;html=1;"
        "align=center;verticalAlign=middle;fillColor=#ffffff;"
        "strokeColor=#334155;strokeWidth=1.3;fontColor=#111827;"
        "fontFamily=Helvetica;fontSize=13;"
    )


def helper_style(kind: str) -> str:
    # The Mermaid class colors are relationship hints only. The delivered
    # diagram follows the supplied GreenLens visual: white ovals and neutral
    # grey strokes for both include and extend helper use cases.
    fill = "#ffffff"
    stroke = "#94a3b8"
    return (
        "shape=ellipse;perimeter=ellipsePerimeter;whiteSpace=wrap;html=1;"
        f"align=center;verticalAlign=middle;fillColor={fill};"
        f"strokeColor={stroke};strokeWidth=1.1;fontColor=#111827;"
        "fontFamily=Helvetica;fontSize=12;"
    )


def actor_style() -> str:
    return (
        "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;"
        "html=1;whiteSpace=wrap;align=center;fillColor=#ffffff;"
        "strokeColor=#334155;strokeWidth=1.5;fontColor=#111827;"
        "fontFamily=Helvetica;fontSize=14;"
    )


def association_style(side: str) -> str:
    exit_x = "1.0" if side == "left" else "0.0"
    entry_x = "0.0" if side == "left" else "1.0"
    return (
        "edgeStyle=none;rounded=0;html=1;endArrow=none;endSize=0;"
        "strokeColor=#94a3b8;strokeWidth=1;fontColor=#475569;opacity=70;"
        "fontFamily=Helvetica;fontSize=10;labelBackgroundColor=#ffffff;"
        f"exitX={exit_x};exitY=0.5;entryX={entry_x};entryY=0.5;"
    )


def relation_style() -> str:
    return (
        "edgeStyle=none;rounded=0;html=1;dashed=1;startArrow=none;"
        "endArrow=open;endFill=0;endSize=10;strokeColor=#64748b;strokeWidth=1.1;"
        "fontColor=#111827;fontFamily=Helvetica;fontSize=10;"
        "labelBackgroundColor=#ffffff;exitX=0.5;exitY=0.5;"
        "entryX=0.5;entryY=0.5;"
    )


def add_edge(
    root: ET.Element,
    edge_id: str,
    source_id: str,
    target_id: str,
    style: str,
    *,
    value: str = "",
    points: list[tuple[float, float]] | None = None,
) -> None:
    node = cell(root, edge_id, "1", value=value, style=style, edge=True, source=source_id, target=target_id)
    geometry = ET.SubElement(node, "mxGeometry", {"relative": "1", "as": "geometry"})
    if points:
        array = ET.SubElement(geometry, "Array", {"as": "points"})
        for x, y in points:
            ET.SubElement(array, "mxPoint", {"x": fmt(x), "y": fmt(y)})


def add_inside(
    root: ET.Element,
    cell_id: str,
    *,
    x: float,
    y: float,
    width: float,
    height: float,
    value: str,
    style: str,
    parent: str = "system_boundary",
    parent_origin: tuple[float, float] = (0.0, 0.0),
) -> tuple[float, float, float, float]:
    origin_x, origin_y = parent_origin
    cell(
        root,
        cell_id,
        parent,
        value=value,
        style=style,
        vertex=True,
        x=x - origin_x,
        y=y - origin_y,
        width=width,
        height=height,
    )
    return (OUTER["x"] + x, OUTER["y"] + y, width, height)


def add_domain_card(
    root: ET.Element,
    card_id: str,
    title: str,
    *,
    x: float,
    y: float,
    width: float,
    height: float,
) -> None:
    style = (
        "rounded=1;arcSize=12;html=1;whiteSpace=wrap;align=left;"
        "verticalAlign=top;spacingTop=12;spacingLeft=16;"
        "fillColor=#f8fafc;strokeColor=#e2e8f0;strokeWidth=1;"
        "container=1;pointerEvents=0;connectable=0;collapsible=0;"
        "fontColor=#475569;fontFamily=Helvetica;fontSize=15;fontStyle=1;"
    )
    cell(
        root,
        card_id,
        "system_boundary",
        value=title,
        style=style,
        vertex=True,
        x=x,
        y=y,
        width=width,
        height=height,
    )


def add_primary(
    root: ET.Element,
    number: int,
    x: float,
    y: float,
    label: str,
    *,
    parent: str = "system_boundary",
    parent_origin: tuple[float, float] = (0.0, 0.0),
) -> tuple[float, float, float, float]:
    return add_inside(
        root,
        f"uc{number:02d}",
        x=x,
        y=y,
        width=PRIMARY_W,
        height=PRIMARY_H,
        value=f"<b>UC-{number:02d}</b><br>{label}",
        style=primary_style(),
        parent=parent,
        parent_origin=parent_origin,
    )


def add_helper(
    root: ET.Element,
    helper_id: str,
    x: float,
    y: float,
    label: str,
    *,
    kind: str,
    width: float = 245.0,
    parent: str = "system_boundary",
    parent_origin: tuple[float, float] = (0.0, 0.0),
) -> tuple[float, float, float, float]:
    return add_inside(
        root,
        helper_id,
        x=x,
        y=y,
        width=width,
        height=HELPER_H,
        value=label,
        style=helper_style(kind),
        parent=parent,
        parent_origin=parent_origin,
    )


def add_actor(root: ET.Element, actor_id: str, label: str, x: float, y: float) -> tuple[float, float, float, float]:
    width, height = 190.0, 130.0
    cell(root, actor_id, "1", value=label, style=actor_style(), vertex=True, x=x, y=y, width=width, height=height)
    return (x, y, width, height)


def add_association(
    root: ET.Element,
    edge_id: str,
    actor_id: str,
    target_id: str,
    *,
    side: str,
) -> None:
    """Draw a direct sample-style fan-out association from an external actor."""

    add_edge(root, edge_id, actor_id, target_id, association_style(side))


def build() -> None:
    root = ET.Element(
        "mxfile",
        {
            "host": "app.diagrams.net",
            "modified": "2026-09-21T00:00:00.000Z",
            "agent": "Codex drawio-skill",
            "version": "24.7.17",
            "type": "device",
        },
    )
    diagram = ET.SubElement(
        root,
        "diagram",
        {
            "id": "use-case-sample-style",
            "name": "Use Case Diagram",
            "data-source": "BRD v1.2; PRD v1.0; Use-Case Spec v1.0; AI Research Experimentation Flows v1.0",
        },
    )
    model = ET.SubElement(
        diagram,
        "mxGraphModel",
        {
            "grid": "1",
            "page": "1",
            "gridSize": "10",
            "guides": "1",
            "tooltips": "1",
            "connect": "1",
            "arrows": "1",
            "fold": "1",
            "pageScale": "1",
            "pageWidth": "3000",
            "pageHeight": "2900",
            "background": "#ffffff",
            "pageBackgroundColor": "#ffffff",
            "math": "0",
            "shadow": "0",
        },
    )
    graph = ET.SubElement(model, "root")
    ET.SubElement(graph, "mxCell", {"id": "0"})
    ET.SubElement(graph, "mxCell", {"id": "1", "parent": "0"})

    boundary_style = (
        "rounded=0;html=1;whiteSpace=wrap;align=center;verticalAlign=top;"
        "spacingTop=16;fillColor=#ffffff;strokeColor=#6b7280;strokeWidth=1.5;"
        "container=1;pointerEvents=0;collapsible=0;fontColor=#111827;"
        "fontFamily=Helvetica;fontSize=20;fontStyle=1;"
    )
    cell(graph, "system_boundary", "1", value="", style=boundary_style, vertex=True, x=OUTER["x"], y=OUTER["y"], width=OUTER["w"], height=OUTER["h"])
    cell(
        graph,
        "header",
        "1",
        value="<b>AI Research Experimentation Platform Use Case Diagram</b>",
        style=text_style(28, align="center"),
        vertex=True,
        x=OUTER["x"] + 40,
        y=OUTER["y"] + 24,
        width=OUTER["w"] - 80,
        height=62,
    )
    cell(
        graph,
        "source",
        "1",
        value="Source: BRD v1.2 • PRD v1.0 • Use-Case Spec v1.0 • AI Research Experimentation Flows v1.0",
        style=text_style(10, align="center", color="#4b5563"),
        vertex=True,
        x=OUTER["x"] + 100,
        y=OUTER["y"] + 88,
        width=OUTER["w"] - 200,
        height=28,
    )

    domain_cards = [
        ("card_access_data", "01  Access & Dataset", 60, 150, 1040, 620),
        ("card_research", "02  Research Definition & Hypothesis", 1140, 150, 1100, 620),
        ("card_experiment", "03  Experiment & Scientific Validation", 60, 850, 1040, 930),
        ("card_findings", "04  Findings, Evidence & Outputs", 1140, 850, 1100, 930),
        ("card_ops", "05  Evaluation & Administration", 60, 1880, 2180, 300),
    ]
    for card_id, title, x, y, width, height in domain_cards:
        add_domain_card(graph, card_id, title, x=x, y=y, width=width, height=height)
    card_origins = {card_id: (x, y) for card_id, _title, x, y, _width, _height in domain_cards}

    labels = {
        1: "Authenticate",
        2: "Create / Manage Research Project",
        3: "Manage Project Members",
        4: "Upload & Validate Dataset",
        5: "Review Profiling & Data Card",
        6: "Review Data Quality,<br>Cleaning & Versioning",
        7: "Define Research Question<br>& Context",
        8: "Define / Confirm Initial H0 & H1",
        9: "Review Research State",
        10: "Generate & Review Candidate<br>Hypotheses",
        11: "Review / Resolve<br>Hypothesis Selection",
        12: "Generate & Review Experiment Plan",
        13: "Review Method Selection<br>& Assumption Checks",
        14: "Execute Experiment",
        15: "Review Deterministic<br>Scientific Validation",
        16: "Review / Resolve<br>Evidence Sufficiency",
        17: "Resolve Scientific Refinement<br>/ Human Review",
        18: "Review Research Finding",
        19: "Review Dependency, Invalidation<br>& Conflicting Evidence",
        20: "Continue or Stop Research Loop",
        21: "Generate Figures, Tables<br>& Research Report",
        22: "View Outputs, Provenance,<br>Evidence, Trace & Decision History",
        23: "Run Benchmark & Evaluation",
        24: "Manage Models, Decision Providers,<br>Logs, Cost & System Configuration",
    }
    positions = {
        1: (90, 230), 2: (420, 230), 3: (750, 230),
        4: (90, 420), 5: (420, 420), 6: (750, 420),
        7: (1170, 230), 8: (1510, 230), 9: (1850, 230),
        10: (1170, 420), 11: (1510, 420),
        12: (90, 930), 13: (420, 930), 14: (750, 930),
        15: (90, 1130), 16: (420, 1130), 17: (750, 1130),
        18: (1170, 930), 19: (1510, 930), 20: (1850, 930),
        21: (1170, 1130), 22: (1510, 1130),
        23: (500, 2020), 24: (1450, 2020),
    }
    primary_cards = {
        **{number: "card_access_data" for number in range(1, 7)},
        **{number: "card_research" for number in range(7, 12)},
        **{number: "card_experiment" for number in range(12, 18)},
        **{number: "card_findings" for number in range(18, 23)},
        23: "card_ops",
        24: "card_ops",
    }
    for number, (x, y) in positions.items():
        card_id = primary_cards[number]
        add_primary(
            graph,
            number,
            x,
            y,
            labels[number],
            parent=card_id,
            parent_origin=card_origins[card_id],
        )

    helper_specs = [
        ("validate_dataset", 90, 560, "Validate Dataset", "include"),
        ("human_approval", 750, 560, "Human Approval", "extend"),
        ("build_research_state", 1850, 420, "Build Research State", "include"),
        ("evaluate_candidate_hypotheses", 1170, 560, "Evaluate Candidate<br>Hypotheses", "include"),
        ("human_hypothesis_review", 1510, 560, "Human Review", "extend"),
        ("check_assumptions", 420, 1260, "Check Assumptions", "include", 200),
        ("secure_execution", 750, 1260, "Secure Execution", "include", 200),
        ("execution_trace", 750, 1340, "Execution Trace", "include", 200),
        ("deterministic_scientific_validation", 90, 1260, "Deterministic Scientific<br>Validation", "include"),
        ("evaluate_evidence_sufficiency", 420, 1340, "Evaluate Evidence<br>Sufficiency", "include"),
        ("technical_retry", 750, 1450, "Technical Retry / Re-plan", "extend", 200),
        ("multiple_testing_control", 90, 1410, "Multiple-Testing Control", "extend"),
        ("data_leakage_check", 90, 1530, "Data Leakage Check", "extend"),
        ("human_evidence_review", 420, 1410, "Human Review", "extend"),
        ("scientific_refinement", 420, 1530, "Scientific Refinement", "extend"),
        ("check_provenance", 1170, 1260, "Check Provenance", "include"),
        ("select_validated_findings", 1510, 1260, "Select Validated Findings", "include"),
        ("conflict_handling", 1850, 1260, "Conflict Handling", "extend"),
    ]
    helper_cards = {
        "validate_dataset": "card_access_data",
        "human_approval": "card_access_data",
        "build_research_state": "card_research",
        "evaluate_candidate_hypotheses": "card_research",
        "human_hypothesis_review": "card_research",
        "check_assumptions": "card_experiment",
        "secure_execution": "card_experiment",
        "execution_trace": "card_experiment",
        "deterministic_scientific_validation": "card_experiment",
        "evaluate_evidence_sufficiency": "card_experiment",
        "technical_retry": "card_experiment",
        "multiple_testing_control": "card_experiment",
        "data_leakage_check": "card_experiment",
        "human_evidence_review": "card_experiment",
        "scientific_refinement": "card_experiment",
        "check_provenance": "card_findings",
        "select_validated_findings": "card_findings",
        "conflict_handling": "card_findings",
    }
    for helper_spec in helper_specs:
        helper_id, x, y, label, kind, *width = helper_spec
        card_id = helper_cards[helper_id]
        add_helper(
            graph,
            helper_id,
            x,
            y,
            label,
            kind=kind,
            width=width[0] if width else 245.0,
            parent=card_id,
            parent_origin=card_origins[card_id],
        )

    add_actor(graph, "researcher", "Researcher /<br>Data Analyst", 40, 360)
    add_actor(graph, "project_manager", "Project Manager", 40, 1130)
    add_actor(graph, "reviewer", "Reviewer /<br>Stakeholder", 2630, 1160)
    add_actor(graph, "administrator", "System<br>Administrator", 2630, 1980)
    actor_access = {
        "researcher": [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
        "project_manager": [1, 2, 3, 23],
        "reviewer": [1, 18, 22],
        "administrator": [1, 23, 24],
    }
    for actor_id, numbers in actor_access.items():
        side = "left" if actor_id in {"researcher", "project_manager"} else "right"
        for index, number in enumerate(numbers, start=1):
            target_id = f"uc{number:02d}"
            add_association(
                graph,
                f"assoc_{actor_id}_{index:02d}",
                actor_id,
                target_id,
                side=side,
            )

    relations = [
        ("include_04_validate", "uc04", "validate_dataset", "<<include>>"),
        ("include_09_state", "uc09", "build_research_state", "<<include>>"),
        ("include_11_candidates", "uc11", "evaluate_candidate_hypotheses", "<<include>>"),
        ("include_13_assumptions", "uc13", "check_assumptions", "<<include>>"),
        ("include_14_secure", "uc14", "secure_execution", "<<include>>"),
        ("include_14_trace", "uc14", "execution_trace", "<<include>>"),
        ("include_15_validation", "uc15", "deterministic_scientific_validation", "<<include>>"),
        ("include_16_evidence", "uc16", "evaluate_evidence_sufficiency", "<<include>>"),
        ("include_18_provenance", "uc18", "check_provenance", "<<include>>"),
        ("include_21_validated", "uc21", "select_validated_findings", "<<include>>"),
        ("extend_06_approval", "human_approval", "uc06", "<<extend>><br>risky / destructive cleaning"),
        ("extend_11_human_review", "human_hypothesis_review", "uc11", "<<extend>><br>low confidence / high risk"),
        ("extend_14_retry", "technical_retry", "uc14", "<<extend>><br>execution failure"),
        ("extend_15_multiple", "multiple_testing_control", "uc15", "<<extend>><br>multiple related tests"),
        ("extend_15_leakage", "data_leakage_check", "uc15", "<<extend>><br>predictive / ML workflow"),
        ("extend_16_review", "human_evidence_review", "uc16", "<<extend>><br>low confidence / high risk"),
        ("extend_16_refinement", "scientific_refinement", "uc16", "<<extend>><br>insufficient evidence"),
        ("extend_18_conflict", "conflict_handling", "uc18", "<<extend>><br>contradictory evidence"),
    ]
    for relation_id, source_id, target_id, label in relations:
        add_edge(graph, relation_id, source_id, target_id, relation_style(), value=label)

    note = (
        "<b>Scope:</b> One consolidated overview in the supplied sample style. "
        "Solid lines show actor access from the Use-Case Spec matrix; dashed arrows show reusable behavior and extension points."
    )
    cell(graph, "overview_note", "1", value=note, style=text_style(10, color="#4b5563"), vertex=True, x=OUTER["x"] + 100, y=OUTER["y"] + 2300, width=OUTER["w"] - 200, height=60)
    legend = "Solid = actor association • dashed open arrow = <<include>> / <<extend>> • internal services remain inside the system boundary"
    cell(graph, "legend", "1", value=legend, style=text_style(10, align="center", color="#4b5563"), vertex=True, x=OUTER["x"] + 100, y=OUTER["y"] + 2370, width=OUTER["w"] - 200, height=35)

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(OUTPUT, encoding="utf-8", xml_declaration=True)
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    build()
