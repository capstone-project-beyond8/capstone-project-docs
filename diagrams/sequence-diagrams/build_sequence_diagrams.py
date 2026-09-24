"""Build the editable sequence-diagram package from source-backed page specs.

The page model follows the current BRD/PRD/Use Case Specification and the
three-panel activity flow reference. Geometry is delegated to drawio-skill's
seqlayout.py so lifelines, activation bars, returns and UML fragments stay
consistent across all pages.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LAYOUT_SCRIPT = Path(r"C:\Users\ADMIN\.agents\skills\drawio-skill\scripts\seqlayout.py")


def _wrap_participant_label(label: str, max_width: int = 14) -> str:
    """Keep lifeline headers inside their cells without widening the canvas."""
    text = str(label).strip()
    text = re.sub(r"\s*\n\s*", " ", text)
    lines: list[str] = []
    # Split CamelCase only at a line boundary, so the displayed class or
    # interface name remains exact (ConfigurationController, not two words).
    camel_lines = re.sub(
        r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])",
        "\n",
        text,
    ).splitlines()
    for camel_line in camel_lines:
        words = camel_line.replace("/", " / ").split()
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if current and len(candidate) > max_width:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
    return "\n".join(lines) or text


def participant(identifier: str, label: str, actor: bool = False) -> dict:
    value = {"id": identifier, "label": _wrap_participant_label(label)}
    if actor:
        value["actor"] = True
    return value


def call(source: str, target: str, label: str, **flags: object) -> dict:
    value = {"from": source, "to": target, "label": label}
    value.update(flags)
    return value


def returning(source: str, target: str, label: str) -> dict:
    return call(source, target, label, **{"return": True})


def page(
    title: str,
    source: str,
    participants: list[dict],
    messages: list[dict],
    fragments: list[dict] | None = None,
) -> dict:
    return {
        "title": title,
        "source": source,
        "profile": "greenlens",
        "participants": participants,
        "messages": messages,
        "fragments": fragments or [],
    }


def alt_fragment(
    identifier: str,
    start: int,
    end: int,
    split_after: int,
    top: str,
    bottom: str,
) -> dict:
    return {
        "id": identifier,
        "kind": "alt",
        "start_message": start,
        "end_message": end,
        "split_after": split_after,
        "branches": [
            {"label": top, "position": "top"},
            {"label": bottom, "position": "bottom"},
        ],
    }


def opt_fragment(identifier: str, start: int, end: int, label: str) -> dict:
    return {
        "id": identifier,
        "kind": "opt",
        "label": label,
        "start_message": start,
        "end_message": end,
    }


def loop_fragment(identifier: str, start: int, end: int, label: str) -> dict:
    return {
        "id": identifier,
        "kind": "loop",
        "label": label,
        "start_message": start,
        "end_message": end,
    }


# The detailed source flows intentionally describe business capabilities rather
# than framework classes.  This profile adds the implementation boundary that
# the reference package uses, without duplicating that boundary in every page
# definition.  The original domain participants remain after the controller so
# their business interactions are still visible and traceable to the source.
ARCHITECTURE_RULES = (
    ("authenticate", "User", "LoginPage", "AuthenticateController"),
    ("project members", "Membership", "MemberManagementPage", "MembershipController"),
    ("manage research definition", "ResearchContext", "ResearchDefinitionPage", "ResearchDefinitionController"),
    ("manage hypotheses", "Hypothesis", "HypothesisManagementPage", "HypothesisManagementController"),
    ("manage experiments", "Experiment", "ExperimentManagementPage", "ExperimentManagementController"),
    ("manage research findings", "Finding", "FindingManagementPage", "FindingManagementController"),
    ("manage research outputs", "ResearchOutput", "OutputManagementPage", "OutputManagementController"),
    ("manage system administration", "Configuration", "AdminConsole", "ConfigurationController"),
    ("project", "Project", "ProjectPage", "ProjectController"),
    ("dataset", "Dataset", "DatasetPage", "DatasetController"),
    ("profiling", "Dataset", "ProfilingPage", "DatasetController"),
    ("data quality", "Dataset", "DataQualityPage", "DatasetController"),
    ("research question", "ResearchContext", "ResearchContextPage", "ResearchContextController"),
    ("hypothesis", "Hypothesis", "HypothesisPage", "HypothesisController"),
    ("research state", "ResearchState", "ResearchStatePage", "ResearchStateController"),
    ("experiment plan", "Experiment", "ExperimentPlanPage", "ExperimentPlanController"),
    ("method selection", "Method", "MethodReviewPage", "MethodController"),
    ("execute experiment", "Execution", "ExperimentRunPage", "ExecutionController"),
    ("scientific validation", "Validation", "ValidationReviewPage", "ValidationController"),
    ("evidence sufficiency", "Evidence", "EvidenceGatePage", "EvidenceController"),
    ("scientific refinement", "Experiment", "RefinementPage", "RefinementController"),
    ("research finding", "Finding", "FindingReviewPage", "FindingController"),
    ("dependency", "Dependency", "DependencyPage", "DependencyController"),
    ("continue or stop", "ResearchState", "ResearchLoopPage", "ResearchLoopController"),
    ("figures", "ResearchOutput", "ReportPage", "ReportController"),
    ("research outputs", "Provenance", "ProvenancePage", "ProvenanceController"),
    ("benchmark", "Evaluation", "BenchmarkPage", "BenchmarkController"),
    ("configuration", "Configuration", "AdminConsole", "ConfigurationController"),
    ("research setup", "ResearchState", "ResearchSetupPage", "ResearchSetupController"),
    ("research loop", "ResearchState", "ResearchWorkspacePage", "ResearchLoopController"),
)


def _architecture_profile(title: str) -> tuple[str, str, str]:
    """Return repository stem, UI object and controller for a page title."""
    normalized = title.lower()
    for keyword, stem, ui, controller in ARCHITECTURE_RULES:
        if keyword in normalized:
            return stem, ui, controller
    return "Research", "ResearchWorkspacePage", "ResearchController"


def _plain_label(value: object) -> str:
    """Remove source-flow numbering before the final page is renumbered."""
    return re.sub(r"^\s*\d+\.\s*", "", str(value))


def _number_messages(messages: list[dict]) -> None:
    """Apply stable display numbering after all architectural calls are added."""
    for number, message in enumerate(messages, start=1):
        if "label" in message:
            message["label"] = f"{number:02d}. {_plain_label(message['label'])}"


def _mapped_message(message: dict, source: str, target: str) -> dict:
    mapped = dict(message)
    mapped["from"] = source
    mapped["to"] = target
    return mapped


def _remap_fragments(fragments: list[dict], message_indexes: dict[int, int]) -> list[dict]:
    """Keep fragment ranges valid after the architectural calls are inserted."""
    remapped: list[dict] = []
    for fragment in fragments:
        start = int(fragment["start_message"])
        end = int(fragment["end_message"])
        indexes = [
            message_indexes[index]
            for index in range(start, end + 1)
            if index in message_indexes
        ]
        if not indexes:
            continue
        current = dict(fragment)
        current["start_message"] = min(indexes)
        current["end_message"] = max(indexes)
        if "split_after" in current:
            split_after = int(current["split_after"])
            current["split_after"] = message_indexes.get(split_after, min(indexes))
        remapped.append(current)
    return remapped


def layered_page(spec: dict) -> dict:
    """Add the shared UI/Auth/Controller/Service/Repository/DB pipeline.

    The existing page specs are the business-flow source of truth.  This
    adapter keeps those interactions and projects them through one application
    service, then persists through one repository implementation.  The
    repository interface is a dependency contract, not a second runtime
    lifeline, so the generated sequence is readable as:

        Controller -> Service -> Repository -> Database

    Self-calls are promoted to a normal hand-off to the next responsible
    participant; the generated package deliberately contains no edge from a
    participant to itself.
    """
    source_participants = spec["participants"]
    actor = next((item for item in source_participants if item.get("actor")), None)
    if actor is None:
        raise ValueError(f"Sequence page has no actor: {spec['title']}")

    # UC-01 is a credential-authentication flow, not an already-authenticated
    # application request.  Keep it explicit instead of forcing it through the
    # shared session/authorization preamble used by UC-02..UC-24.
    if spec["title"].startswith("UC-01 "):
        return authentication_page(spec)

    ui_source = next(
        (
            item
            for item in source_participants
            if item is not actor
            and (
                item["id"] in {"web", "web_app", "console"}
                or re.search(r"web app|console|page", item.get("label", ""), re.I)
            )
        ),
        next(item for item in source_participants if item is not actor),
    )
    stem, ui_name, controller_name = _architecture_profile(spec["title"])

    actor_id = actor["id"]
    ui_source_id = ui_source["id"]
    ui_id = "ui_layer"
    auth_id = "auth_layer"
    controller_id = "controller_layer"
    service_id = "service_layer"
    repository_id = "repository_layer"
    database_id = "database_layer"

    original_messages = spec.get("messages", [])
    primary_original_id = next(
        (
            str(message.get("to"))
            for message in original_messages
            if message.get("from") == ui_source_id
            and message.get("to") not in {actor_id, ui_source_id}
            and "note" not in message
        ),
        None,
    )
    if primary_original_id is None:
        primary_original_id = next(
            item["id"]
            for item in source_participants
            if item is not actor and item is not ui_source
        )

    domain_ids: dict[str, str] = {}
    domain_participants: list[dict] = []
    for item in source_participants:
        if item is actor or item is ui_source:
            continue
        domain_id = service_id if item["id"] == primary_original_id else f"domain_{item['id']}"
        while domain_id in domain_ids.values():
            domain_id += "_service"
        domain_ids[item["id"]] = domain_id
        label = str(item.get("label", item["id"]))
        domain_participants.append(participant(domain_id, f":{label.lstrip(':')}"))

    participants = [
        participant(actor_id, actor.get("label", actor_id), True),
        participant(ui_id, f":{ui_name}"),
        participant(auth_id, ":Auth / Authorization"),
        participant(controller_id, f":{controller_name}"),
        *domain_participants,
        participant(repository_id, f":{stem}Repository"),
        participant(database_id, "Database"),
    ]

    def remap(identifier: str) -> str:
        if identifier == ui_source_id:
            return ui_id
        if identifier == actor_id:
            return actor_id
        return domain_ids.get(identifier, identifier)

    participant_order = [item["id"] for item in participants]

    def next_responsible_participant(identifier: str) -> str:
        """Return the next lifeline for an internal step, never itself."""
        try:
            position = participant_order.index(identifier)
        except ValueError:
            return repository_id
        if position + 1 < len(participant_order):
            return participant_order[position + 1]
        return repository_id

    first_trigger = next(
        (
            index
            for index, message in enumerate(original_messages)
            if message.get("from") == actor_id and message.get("to") == ui_source_id
        ),
        None,
    )
    trigger_message = (
        _mapped_message(original_messages[first_trigger], actor_id, ui_id)
        if first_trigger is not None
        else call(actor_id, ui_id, f"Open {ui_name.lstrip(':')}")
    )

    messages: list[dict] = [trigger_message]
    messages.extend(
        [
            call(ui_id, auth_id, "Authenticate existing session / token + request context"),
            call(auth_id, controller_id, f"Authorize scope + dispatch {controller_name}"),
        ]
    )

    message_indexes: dict[int, int] = {}
    if first_trigger is not None:
        message_indexes[first_trigger] = 0
    pending_final_responses: list[int] = []
    final_response_label = f"{_plain_label(spec['title'])} completed"

    service_call_added = False
    for index, original in enumerate(original_messages):
        if index == first_trigger:
            continue
        if "note" in original:
            mapped_note = dict(original)
            mapped_note["over"] = remap(str(original.get("over", ui_source_id)))
            message_indexes[index] = len(messages)
            messages.append(mapped_note)
            continue

        original_source = str(original.get("from", ""))
        original_target = str(original.get("to", ""))
        mapped_source = remap(original_source)
        mapped_target = remap(original_target)

        # Final UI -> actor responses are emitted after the controller/auth
        # return chain, so they do not bypass the boundary in the middle.
        if original_source == ui_source_id and original_target == actor_id:
            final_response_label = _plain_label(original.get("label", final_response_label))
            pending_final_responses.append(index)
            continue

        if original_source == actor_id and original_target == ui_source_id:
            message_indexes[index] = len(messages)
            messages.append(_mapped_message(original, actor_id, ui_id))
            messages.extend(
                [
                    call(ui_id, auth_id, "Validate session / role for follow-up action"),
                    call(auth_id, controller_id, f"Forward authorized {controller_name} request"),
                ]
            )
            continue

        # The Web App is a boundary only.  Once a request is inside the
        # application, the controller owns calls to domain collaborators.
        if original_source == ui_source_id:
            mapped_source = controller_id
        if original_target == ui_source_id:
            mapped_target = controller_id

        # Do not render UML self-call loops.  Internal processing is shown as
        # a regular hand-off to the next responsible lifeline instead.
        if mapped_source == mapped_target:
            mapped_target = next_responsible_participant(mapped_source)

        message_indexes[index] = len(messages)
        messages.append(_mapped_message(original, mapped_source, mapped_target))
        if mapped_source == controller_id and mapped_target == service_id:
            service_call_added = True

    if not service_call_added:
        messages.append(call(controller_id, service_id, f"Handle {_plain_label(spec['title'])} request"))

    messages.extend(
        [
            call(service_id, repository_id, f"Load / persist {stem} aggregate"),
            call(repository_id, database_id, f"SELECT / INSERT / UPDATE {stem} data"),
            returning(database_id, repository_id, "Rows / transaction result"),
            returning(repository_id, service_id, f"{stem} aggregate ready"),
            returning(service_id, controller_id, f"{stem} service result + audit context"),
            returning(controller_id, auth_id, f"{controller_name} response + audit context"),
            returning(auth_id, ui_id, "Authenticated response envelope"),
            returning(ui_id, actor_id, final_response_label),
        ]
    )
    final_response_index = len(messages) - 1
    for index in pending_final_responses:
        message_indexes[index] = final_response_index

    _number_messages(messages)

    return page(
        spec["title"],
        spec["source"],
        participants,
        messages,
        _remap_fragments(spec.get("fragments", []), message_indexes),
    )


def authentication_page(spec: dict) -> dict:
    """Build the pre-session login flow without an invalid authorization step."""
    actor = next((item for item in spec["participants"] if item.get("actor")), None)
    if actor is None:
        raise ValueError(f"Authentication page has no actor: {spec['title']}")

    actor_id = actor["id"]
    participants = [
        participant(actor_id, actor.get("label", actor_id), True),
        participant("login_page", ":LoginPage"),
        participant("auth_controller", ":AuthenticateController"),
        participant("auth_service", ":AuthService"),
        participant("user_repository", ":UserRepository"),
        participant("database", "Database"),
        participant("workspace_policy", ":Workspace / Policy"),
    ]
    messages = [
        call(actor_id, "login_page", "Submit credential"),
        call("login_page", "auth_controller", "Start credential authentication"),
        call("auth_controller", "auth_service", "Authenticate credential"),
        call("auth_service", "user_repository", "Load user / credential record"),
        call("user_repository", "database", "SELECT user + credential data"),
        returning("database", "user_repository", "User / credential row"),
        returning("user_repository", "auth_service", "User / credential record"),
        call("auth_service", "auth_service", "Verify credential + create session / token"),
        call("auth_service", "workspace_policy", "Load roles + project memberships"),
        returning("workspace_policy", "auth_service", "Roles + project scope"),
        call("auth_service", "workspace_policy", "Apply workspace / authorization policy"),
        returning("workspace_policy", "auth_service", "Authorization policy applied"),
        call("auth_service", "auth_controller", "Authenticated session + authorized scope"),
        returning("auth_controller", "login_page", "Authenticated session / token"),
        returning("login_page", actor_id, "Open authorized workspace"),
    ]
    _number_messages(messages)
    return page(spec["title"], spec["source"], participants, messages)


def core_page() -> dict:
    return page(
        "Core Research Loop - UML Sequence",
        "BRD §13 · PRD §9/§37.4 · Use Case Spec §35",
        [
            participant("researcher", "Researcher", True),
            participant("web_app", "Web App"),
            participant("state", "Research State"),
            participant("agent", "AI Research Agent"),
            participant("gate", "Structured Decision Gate"),
            participant("tools", "Analytical Tools"),
            participant("sandbox", "Secure Sandbox"),
            participant("validator", "Scientific Validator"),
        ],
        [
            call("researcher", "web_app", "01. Open project + dataset; define RQ"),
            call("web_app", "state", "02. Build Research State (dataset vN, H0/H1)"),
            returning("state", "web_app", "03. Research State v1 ready"),
            call("web_app", "agent", "04. Generate candidate hypotheses / directions"),
            returning("agent", "web_app", "05. Candidate set + rationale + testability"),
            call("web_app", "gate", "06. Evaluate candidates (policy criteria)"),
            returning("gate", "web_app", "07. SELECT / REJECT / ESCALATE + confidence"),
            returning("web_app", "researcher", "08. Decision / review task"),
            call("researcher", "web_app", "09. Confirm active research direction"),
            call("web_app", "agent", "10. Deep reasoning + experiment plan"),
            returning("agent", "web_app", "11. Plan + methods + assumptions"),
            call("web_app", "tools", "12. Run deterministic assumption checks"),
            returning("tools", "web_app", "13. Pass / Fail / Warning / N/A"),
            call("web_app", "sandbox", "14. Execute approved experiment"),
            returning("sandbox", "web_app", "15. Raw results + artifacts + trace"),
            call("web_app", "validator", "16. Deterministic scientific validation"),
            returning("validator", "web_app", "17. Scientific facts + effect size / CI"),
            call("web_app", "gate", "18. Evaluate evidence sufficiency"),
            returning("gate", "web_app", "19. Evidence outcome + confidence / reasons"),
            returning("web_app", "researcher", "20. Finding or next-action review"),
            call("researcher", "web_app", "21. Approve / modify / continue / stop"),
            call("web_app", "state", "22. Update state + decision audit"),
            returning("state", "web_app", "23. Research State updated"),
            call("web_app", "agent", "24. Next candidates / scientific refinement"),
            returning("agent", "web_app", "25. Next plan / direction"),
            returning("web_app", "researcher", "26. Final findings / report when stopped"),
        ],
        [
            alt_fragment(
                "hypothesis-selection",
                5,
                7,
                6,
                "[SELECT / auto-continue]",
                "else [REJECT / ESCALATE / no candidate]",
            ),
            alt_fragment(
                "evidence-gate",
                17,
                20,
                18,
                "[ENOUGH_EVIDENCE]",
                "else [REFINE / REPLICATE / HUMAN / INCONCLUSIVE]",
            ),
            alt_fragment(
                "stopping",
                20,
                25,
                23,
                "[Continue → UC-10]",
                "else [Stop → final outputs]",
            ),
        ],
    )


def business_pages() -> list[dict]:
    return [
        page(
            "Research Setup - Main Flow",
            "BRD §12 · PRD §9 · Use Case Spec §32",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("workspace", "Project Workspace"),
                participant("dataset", "Dataset Services"),
                participant("state", "Research State / Context"),
            ],
            [
                call("researcher", "web", "01. Authenticate + open project"),
                call("web", "workspace", "02. Load memberships + project scope"),
                returning("workspace", "web", "03. Authorized workspace"),
                returning("web", "researcher", "04. Project workspace ready"),
                call("researcher", "web", "05. Upload / select dataset"),
                call("web", "dataset", "06. Store original + create Dataset v1"),
                returning("dataset", "web", "07. Validated dataset + Data Card"),
                returning("web", "researcher", "08. Review profile + quality warnings"),
                call("researcher", "web", "09. Review quality / approve cleaning if needed"),
                call("web", "dataset", "10. Create derived version + lineage"),
                returning("dataset", "web", "11. Updated Data Card / version state"),
                returning("web", "researcher", "12. Dataset ready for research"),
                call("researcher", "web", "13. Enter research question + domain context"),
                call("web", "state", "14. Version active RQ and context"),
                returning("state", "web", "15. Context ready"),
                returning("web", "researcher", "16. Active research question"),
                call("researcher", "web", "17. Define / confirm H0 + H1"),
                call("web", "state", "18. Initialize Research State"),
                returning("state", "web", "19. State tracks hypotheses + constraints"),
                returning("web", "researcher", "20. Research setup complete / start loop"),
            ],
            [opt_fragment("approved-cleaning", 8, 11, "[If quality issue requires a derived version]")],
        ),
        page(
            "Decision-Gated Research Loop - Main Flow",
            "BRD §13 · PRD §9/§37.3-37.4 · Use Case Spec §32",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("state", "Research State"),
                participant("agent", "AI Research Agent"),
                participant("gate", "Evidence Sufficiency Gate"),
                participant("tools", "Analytical Tools"),
                participant("sandbox", "Secure Sandbox"),
                participant("validator", "Scientific Validator"),
            ],
            [
                call("researcher", "web", "01. Start iteration with active Research State"),
                call("web", "state", "02. Load hypothesis, history, budget, conflicts"),
                returning("state", "web", "03. Current research context"),
                call("web", "agent", "04. Deep reasoning + generate experiment plan"),
                returning("agent", "web", "05. Plan + candidate methods + risks"),
                call("web", "tools", "06. Check assumptions deterministically"),
                returning("tools", "web", "07. Assumption results"),
                returning("web", "researcher", "08. Plan / method review"),
                call("researcher", "web", "09. Approve execution"),
                call("web", "sandbox", "10. Execute experiment"),
                returning("sandbox", "web", "11. Raw outputs + trace"),
                call("web", "validator", "12. Validate scientific result"),
                returning("validator", "web", "13. Deterministic facts + validation status"),
                call("web", "gate", "14. Evaluate evidence sufficiency"),
                returning("gate", "web", "15. ENOUGH / refine / replicate / human / inconclusive"),
                call("web", "agent", "16. Generate finding or scientific refinement"),
                returning("agent", "web", "17. Finding candidate / next experiment plan"),
                call("web", "state", "18. Update Research State + decision history"),
                returning("state", "web", "19. State version saved"),
                returning("web", "researcher", "20. Continue / stop recommendation"),
            ],
            [
                alt_fragment(
                    "evidence-outcome",
                    15,
                    17,
                    16,
                    "[ENOUGH_EVIDENCE → finding]",
                    "else [scientific refinement / human review / inconclusive]",
                )
            ],
        ),
        page(
            "Hypothesis Selection Gate - Main Flow",
            "BRD §14 · PRD §37.1-37.2 · Use Case Spec UC-09–UC-11",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("state", "Research State"),
                participant("agent", "Generative Reasoner"),
                participant("gate", "Hypothesis Selection Gate"),
            ],
            [
                call("researcher", "web", "01. Open current state / previous finding"),
                call("web", "state", "02. Build / update versioned Research State"),
                returning("state", "web", "03. State + parent evidence ready"),
                call("web", "agent", "04. Generate candidate hypotheses / directions"),
                returning("agent", "web", "05. Candidates + rationale + testability"),
                call("web", "researcher", "06. Inspect / edit / discard candidates"),
                call("researcher", "web", "07. Continue to selection gate / request more"),
                call("web", "gate", "08. Rank candidates by policy criteria"),
                returning("gate", "web", "09. SELECT / REJECT / ESCALATE / NO_SUITABLE"),
                call("web", "state", "10. Save decision record + confidence / reasons"),
                returning("state", "web", "11. Decision history persisted"),
                returning("web", "researcher", "12. Decision + human review task"),
                call("researcher", "web", "13. Approve / modify / override / reject"),
                call("web", "state", "14. Set active direction (Post-hoc / Unverified)"),
                returning("state", "web", "15. Active direction saved"),
                returning("web", "researcher", "16. Direction ready for experiment planning"),
            ],
            [
                loop_fragment("candidate-set", 3, 6, "[more candidates needed]"),
                alt_fragment(
                    "selection-resolution",
                    11,
                    14,
                    12,
                    "[SELECT + high confidence]",
                    "else [ESCALATE / REJECT / NO_SUITABLE]",
                ),
            ],
        ),
        page(
            "Experiment Execution & Validation - Main Flow",
            "BRD §16 · PRD Modules L–M · Use Case Spec UC-14/UC-15",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("plan", "Experiment Plan"),
                participant("sandbox", "Secure Sandbox"),
                participant("trace", "Execution Trace"),
                participant("validator", "Scientific Validator"),
                participant("store", "Experiment / Result Store"),
            ],
            [
                call("researcher", "web", "01. Open approved experiment plan"),
                call("web", "plan", "02. Load plan, method and assumptions"),
                returning("plan", "web", "03. Execution-ready plan + risk flags"),
                returning("web", "researcher", "04. Review execution plan"),
                call("researcher", "web", "05. Approve execution"),
                call("web", "sandbox", "06. Execute experiment in secure sandbox"),
                call("sandbox", "trace", "07. Persist execution trace + artifacts"),
                returning("trace", "sandbox", "08. Trace id + artifacts recorded"),
                returning("sandbox", "web", "09. Raw outputs + execution status"),
                call("web", "validator", "10. Validate scientific result"),
                returning("validator", "web", "11. Deterministic facts + validation status"),
                call("web", "store", "12. Save result + validation record"),
                returning("store", "web", "13. Reproducibility snapshot saved"),
                returning("web", "researcher", "14. Execution and validation summary"),
            ],
        ),
        page(
            "Method Selection - Main Flow",
            "BRD §15 · PRD Modules I/J · Use Case Spec UC-13",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("agent", "AI Research Agent"),
                participant("tools", "Analytical Tools"),
                participant("method", "Method Store"),
            ],
            [
                call("researcher", "web", "01. Open method selection review"),
                call("web", "agent", "02. Generate candidate methods + assumptions"),
                returning("agent", "web", "03. Candidate methods + required checks"),
                call("web", "tools", "04. Run deterministic assumption checks"),
                returning("tools", "web", "05. Pass / Fail / Warning / N/A"),
                call("web", "agent", "06. Compare candidates + select suitable method"),
                returning("agent", "web", "07. Selected method + rationale + alternatives"),
                returning("web", "researcher", "08. Display method and assumption results"),
                call("researcher", "web", "09. Confirm method / request alternative"),
                call("web", "agent", "10. Select alternative or keep selected method"),
                returning("agent", "web", "11. Method decision ready"),
                call("web", "method", "12. Persist method + rationale"),
                returning("method", "web", "13. Method ready for execution"),
                returning("web", "researcher", "14. Execution handoff"),
            ],
            [
                alt_fragment(
                    "method-suitability",
                    3,
                    6,
                    4,
                    "[Suitable method]",
                    "else [Alternative method / re-check]",
                )
            ],
        ),
        page(
            "Research Finding Provenance - Main Flow",
            "BRD §16 · PRD Modules Q/X · Use Case Spec UC-18/UC-22",
            [
                participant("researcher", "Researcher / Reviewer", True),
                participant("web", "Web App"),
                participant("provenance", "Provenance Service"),
                participant("experiment", "Experiment Store"),
                participant("evidence", "Execution / Data Evidence"),
            ],
            [
                call("researcher", "web", "01. Open research finding"),
                call("web", "provenance", "02. Load evidence chain"),
                call("provenance", "experiment", "03. Load hypothesis + experiment links"),
                call("experiment", "evidence", "04. Load dataset version, method, code / query"),
                returning("evidence", "experiment", "05. Raw output + statistical result"),
                returning("experiment", "provenance", "06. Experiment and evidence references"),
                returning("provenance", "web", "07. Provenance + finding evidence"),
                returning("web", "researcher", "08. Display evidence chain"),
                call("researcher", "web", "09. Review finding / validation status"),
                call("web", "provenance", "10. Check and save review decision"),
                returning("provenance", "web", "11. Finding state + trace saved"),
                returning("web", "researcher", "12. Verified finding / limitations available"),
            ],
        ),
        page(
            "Scientific Validity Guard - Main Flow",
            "BRD §16.1/§16.1.1 · PRD Modules M–P · Use Case Spec UC-15/UC-16",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("validator", "Scientific Validator"),
                participant("checks", "Sandbox / Data Checks"),
                participant("stats", "Statistical Service"),
                participant("store", "Validation Store"),
            ],
            [
                call("researcher", "web", "01. Open experiment validation review"),
                call("web", "validator", "02. Start deterministic validation"),
                call("validator", "store", "03. Load execution result + artifacts"),
                returning("store", "validator", "04. Result metadata + outputs"),
                call("validator", "checks", "05. Check assumptions, leakage, diagnostics"),
                returning("checks", "validator", "06. Validity + reproducibility facts"),
                call("validator", "stats", "07. Validate statistic, correction, effect size / CI"),
                returning("stats", "validator", "08. Statistical result + uncertainty"),
                call("validator", "validator", "09. Check interpretation / causal language"),
                call("validator", "store", "10. Save Scientific Validation Record"),
                returning("store", "validator", "11. Validation record persisted"),
                returning("validator", "web", "12. Passed / Warnings / Review / Failed"),
                returning("web", "researcher", "13. Deterministic validation summary"),
            ],
        ),
        page(
            "Evidence Sufficiency Gate - Main Flow",
            "BRD §16.1.2 · BR-59 · PRD Modules Q/R · Use Case Spec UC-16/UC-17",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("evidence", "Evidence & Provenance"),
                participant("gate", "Evidence Sufficiency Gate"),
                participant("state", "Research State"),
            ],
            [
                call("researcher", "web", "01. Open validated result / finding"),
                call("web", "evidence", "02. Load result, provenance and validation facts"),
                returning("evidence", "web", "03. Evidence chain + uncertainty"),
                call("web", "gate", "04. Evaluate evidence sufficiency"),
                returning("gate", "web", "05. ENOUGH_EVIDENCE / REFINE / REPLICATE / HUMAN / INCONCLUSIVE"),
                call("web", "state", "06. Persist gate outcome + confidence"),
                returning("state", "web", "07. Outcome + reasons saved"),
                returning("web", "researcher", "08. Finding or next action for review"),
            ],
            [
                alt_fragment(
                    "evidence-outcome",
                    4,
                    7,
                    5,
                    "[ENOUGH_EVIDENCE → finding]",
                    "else [REFINE / REPLICATE / HUMAN / INCONCLUSIVE]",
                )
            ],
        ),
        page(
            "Dependency & Conflict Handling - Main Flow",
            "BRD §16.2 · PRD Modules S/T · Use Case Spec UC-19",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("dependency", "Dependency Service"),
                participant("store", "Experiment Store"),
                participant("agent", "AI Research Agent"),
            ],
            [
                call("researcher", "web", "01. Open dependency / conflict view"),
                call("web", "dependency", "02. Load dependency graph"),
                call("dependency", "store", "03. Fetch RQ → State → H → E → F lineage"),
                returning("store", "dependency", "04. Upstream / downstream artifacts"),
                returning("dependency", "web", "05. Graph + invalidation / conflict impact"),
                returning("web", "researcher", "06. Display dependency state"),
                call("researcher", "web", "07. Inspect edge / review conflict"),
                call("web", "dependency", "08. Detect descendants + create Conflict Record"),
                call("dependency", "agent", "09. Propose re-run / refine / preserve action"),
                returning("agent", "dependency", "10. Recommended next action"),
                call("dependency", "store", "11. Preserve results; mark descendants re-validation"),
                returning("store", "dependency", "12. Updated H / E / F states"),
                returning("dependency", "web", "13. Conflict and lineage state saved"),
                returning("web", "researcher", "14. Limitation / next action available"),
            ],
            [
                opt_fragment(
                    "conflict-impact",
                    7,
                    12,
                    "[When invalidation or conflicting evidence is detected]",
                )
            ],
        ),
        page(
            "Evaluation - Main Flow",
            "BRD §17 · PRD Module AA/AG · Use Case Spec UC-23",
            [
                participant("evaluator", "Researcher / Project Manager / System Administrator", True),
                participant("web", "Web App"),
                participant("config", "Agent / Gate Config"),
                participant("runner", "Benchmark Runner"),
                participant("store", "Evaluation Store"),
            ],
            [
                call("evaluator", "web", "01. Select benchmark task + configurations"),
                call("web", "config", "02. Load dataset, RQ, hypothesis, gate policy"),
                returning("config", "web", "03. Benchmark context + configuration"),
                call("web", "runner", "04. Run agent benchmark"),
                call("runner", "store", "05. Collect experiments, decisions, findings, trace"),
                returning("store", "runner", "06. Run records + cost / latency"),
                returning("runner", "web", "07. Benchmark result"),
                call("web", "store", "08. Score gate quality + correctness + reproducibility"),
                returning("store", "web", "09. Aggregated metrics"),
                returning("web", "evaluator", "10. Evaluation dashboard / report"),
                call("evaluator", "web", "11. Compare configurations"),
                call("web", "store", "12. Save comparison + audit record"),
                returning("store", "web", "13. Evaluation output persisted"),
                returning("web", "evaluator", "14. Export evaluation report"),
            ],
            [loop_fragment("benchmark-runs", 3, 6, "[i = 1..N]")],
        ),
    ]


def detailed_pages() -> list[dict]:
    return [
        page(
            "UC-01 Authenticate - Main Flow",
            "Use Case Spec §7 · PRD Module A",
            [
                participant("user", "User", True),
                participant("web", "Web App"),
                participant("auth", "Auth Service"),
                participant("workspace", "Workspace / Policy"),
            ],
            [
                call("user", "web", "01. Submit credential"),
                call("web", "auth", "02. Authenticate credential"),
                returning("auth", "web", "03. Authenticated session / token"),
                call("web", "workspace", "04. Load roles + project memberships"),
                returning("workspace", "web", "05. Roles + project scope"),
                call("web", "auth", "06. Apply authorization policy"),
                returning("web", "user", "07. Open authorized workspace"),
            ],
        ),
        page(
            "UC-02 Create / Manage Research Project - Main Flow",
            "Use Case Spec §8 · PRD Module B",
            [
                participant("actor", "Researcher / PM", True),
                participant("web", "Web App"),
                participant("project", "Project Service"),
                participant("membership", "Membership Service"),
            ],
            [
                call("actor", "web", "01. Submit project details"),
                call("web", "project", "02. Validate + create / update Project"),
                returning("project", "web", "03. Project saved"),
                call("web", "membership", "04. Assign owner / project scope"),
                returning("membership", "web", "05. Membership saved"),
                returning("web", "actor", "06. Dashboard: state, dataset, hypothesis, findings"),
            ],
        ),
        page(
            "UC-03 Manage Project Members - Main Flow",
            "Use Case Spec §9 · PRD Modules A/B",
            [
                participant("pm", "Project Manager", True),
                participant("web", "Web App"),
                participant("membership", "Membership Service"),
                participant("permission", "Permission Service"),
                participant("audit", "Audit Service"),
            ],
            [
                call("pm", "web", "01. Open member list"),
                call("pm", "web", "02. Add member / edit project role"),
                call("web", "membership", "03. Check user + save membership"),
                call("membership", "permission", "04. Apply effective permission"),
                returning("permission", "membership", "05. Permission active"),
                returning("membership", "web", "06. Member + role saved"),
                call("web", "audit", "07. Record membership audit event"),
                returning("audit", "web", "08. Audit record saved"),
                returning("web", "pm", "09. Refresh member list"),
            ],
        ),
        page(
            "UC-04 Upload & Validate Dataset - Main Flow",
            "Use Case Spec §10 · PRD Module C",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("dataset", "Dataset Service"),
                participant("validator", "Dataset Validator"),
                participant("profiler", "Profiler / Queue"),
            ],
            [
                call("researcher", "web", "01. Select supported file"),
                call("web", "dataset", "02. Store immutable original + checksum"),
                returning("dataset", "web", "03. Dataset + raw Dataset Version v1"),
                call("web", "validator", "04. Validate readability, schema, types, limits"),
                returning("validator", "web", "05. Validation pass"),
                call("web", "profiler", "06. Enqueue profiling"),
                returning("profiler", "web", "07. Profiling queued / complete"),
                returning("web", "researcher", "08. Dataset status = Valid / Profiled"),
            ],
        ),
        page(
            "UC-05 Review Profiling & Data Card - Main Flow",
            "Use Case Spec §11 · PRD Module D",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("dataset", "Dataset Service"),
                participant("profiler", "Profiler"),
            ],
            [
                call("researcher", "web", "01. Open exact dataset version"),
                call("web", "dataset", "02. Load profile + Data Card"),
                call("dataset", "profiler", "03. Read profiling outputs"),
                returning("profiler", "dataset", "04. Counts, types, missingness, warnings"),
                returning("dataset", "web", "05. Data Card for vN"),
                returning("web", "researcher", "06. Display statistics + quality warnings"),
                call("researcher", "web", "07. Review warnings + add variable meaning"),
                call("web", "dataset", "08. Persist domain meaning / context"),
                returning("dataset", "web", "09. Updated Data Card"),
                returning("web", "researcher", "10. Context update saved"),
            ],
        ),
        page(
            "UC-06 Review Data Quality, Cleaning & Versioning - Main Flow",
            "Use Case Spec §12 · PRD Module E",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("agent", "AI Research Agent"),
                participant("quality", "Data Quality Service"),
                participant("dataset", "Dataset Service"),
            ],
            [
                call("researcher", "web", "01. Open data-quality review"),
                call("web", "agent", "02. Classify issue + draft cleaning proposal"),
                call("agent", "quality", "03. Assess issue, risk, affected rows / columns"),
                returning("quality", "agent", "04. Issue classification + impact"),
                returning("agent", "web", "05. Proposal + rationale + reversibility"),
                returning("web", "researcher", "06. Show proposal and information-loss risk"),
                call("researcher", "web", "07. Approve / modify / reject / ask agent"),
                call("web", "dataset", "08. Apply approved transformation as derived version"),
                returning("dataset", "web", "09. New Dataset Version + lineage"),
                call("web", "agent", "10. Regenerate Data Card"),
                returning("agent", "web", "11. Updated Data Card"),
                returning("web", "researcher", "12. Versioned quality state"),
            ],
            [opt_fragment("approved-transformation", 7, 10, "[If cleaning is approved or modified]")],
        ),
        page(
            "UC-07 Define Research Question & Context - Main Flow",
            "Use Case Spec §13 · PRD Module F",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("rq", "Research Question Service"),
                participant("context", "Research Context Store"),
            ],
            [
                call("researcher", "web", "01. Submit question, goal, variables, constraints"),
                call("web", "rq", "02. Validate and activate Research Question"),
                returning("rq", "web", "03. Active Research Question"),
                call("web", "context", "04. Version domain context + notes"),
                returning("context", "web", "05. Context version saved"),
                returning("web", "researcher", "06. RQ + context ready for planning"),
            ],
        ),
        page(
            "UC-08 Define / Confirm Initial H0 & H1 - Main Flow",
            "Use Case Spec §14 · PRD Module G",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("agent", "AI Research Agent"),
                participant("hypothesis", "Hypothesis Service"),
                participant("state", "Research State"),
            ],
            [
                call("researcher", "web", "01. Enter H0 + H1 or request AI draft"),
                call("web", "agent", "02. Draft initial hypotheses (optional)"),
                returning("agent", "web", "03. Draft H0 / H1"),
                returning("web", "researcher", "04. Review AI draft"),
                call("researcher", "web", "05. Confirm H0 + H1"),
                call("web", "hypothesis", "06. Save Initial / Confirmatory, Unverified"),
                returning("hypothesis", "web", "07. Hypotheses linked to RQ"),
                call("web", "state", "08. Initialize Research State"),
                returning("state", "web", "09. Initial state ready"),
                returning("web", "researcher", "10. H0/H1 + state confirmed"),
            ],
            [opt_fragment("ai-initial-draft", 1, 3, "[If researcher requests an AI draft]")],
        ),
        page(
            "UC-09 Review Research State - Main Flow",
            "Use Case Spec §15 · PRD Module AC",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("state", "Research State Service"),
                participant("artifacts", "Research Artifacts"),
            ],
            [
                call("researcher", "web", "01. Open Research State review"),
                call("web", "state", "02. Build / version Research State"),
                call("state", "artifacts", "03. Load RQ, hypotheses, history, findings, budget"),
                returning("artifacts", "state", "04. Source artifacts + warnings"),
                returning("state", "web", "05. State vN + constraints"),
                returning("web", "researcher", "06. Show state summary + source links"),
                call("researcher", "web", "07. Correct context / dataset / hypothesis selection"),
                call("web", "state", "08. Create updated Research State version"),
                returning("state", "web", "09. Updated state persisted"),
                returning("web", "researcher", "10. Research State ready for candidates"),
            ],
            [opt_fragment("state-correction", 6, 8, "[If context or source selection needs correction]")],
        ),
        page(
            "UC-10 Generate & Review Candidate Hypotheses - Main Flow",
            "Use Case Spec §16 · PRD Modules AC/AH · BR-64/65",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("state", "Research State"),
                participant("agent", "Generative Reasoner"),
            ],
            [
                call("researcher", "web", "01. Open candidate generation"),
                call("web", "state", "02. Load active Research State"),
                returning("state", "web", "03. State + parent evidence"),
                call("web", "agent", "04. Generate candidate set / directions"),
                returning("agent", "web", "05. Statement, rationale, testability, risks"),
                call("web", "agent", "06. Create Structured Idea Record (statement, proposed experiment, context, risks)"),
                returning("agent", "web", "07. Idea record draft"),
                call("web", "agent", "08. Perform Reflection Round (statement, risk, testability)"),
                returning("agent", "web", "09. Reflection record + open questions"),
                call("web", "agent", "10. Assess novelty from provided literature / context"),
                returning("agent", "web", "11. Novelty result + references, or Not Assessed"),
                call("web", "state", "12. Mark origin + Unverified and persist candidate"),
                returning("state", "web", "13. Candidate idea / reflection metadata saved"),
                returning("web", "researcher", "14. Display candidate list + provenance"),
                call("researcher", "web", "15. Inspect / edit / discard / request more"),
                call("web", "agent", "16. Generate more candidates if requested"),
                returning("agent", "web", "17. Additional candidate set"),
                returning("web", "researcher", "18. Candidate set ready for selection gate"),
            ],
            [
                loop_fragment("candidate-generation", 3, 16, "[more candidates needed]"),
                opt_fragment("novelty-assessment", 9, 10, "[Novelty feature enabled]"),
                alt_fragment(
                    "novelty-input",
                    9,
                    10,
                    9,
                    "[Source / context available → assess novelty]",
                    "else [No source / context → record Not Assessed]",
                ),
            ],
        ),
        page(
            "UC-11 Review / Resolve Hypothesis Selection Decision - Main Flow",
            "Use Case Spec §17 · PRD Module AD · BR-78",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("gate", "Structured Decision Provider"),
                participant("state", "Decision / Research State Store"),
            ],
            [
                call("researcher", "web", "01. Open hypothesis selection gate"),
                call("web", "state", "02. Load Research State + candidate set"),
                returning("state", "web", "03. Candidate context + State version"),
                call("web", "gate", "04. Evaluate relevance, testability, evidence, feasibility"),
                returning("gate", "web", "05. Numeric decision score + confidence / reasons"),
                call("web", "gate", "06. Apply tie_threshold + max_parallel_candidates"),
                returning("gate", "web", "07. Single candidate or bounded tied candidates (1..N)"),
                call("web", "state", "08. Save Decision Record + score, confidence, tie_threshold_used, tied_candidates"),
                returning("state", "web", "09. Decision history persisted"),
                returning("web", "researcher", "10. Decision + review task"),
                call("researcher", "web", "11. Human review: approve / modify / override / reject"),
                call("web", "state", "12. Set active direction(s) or record outcome after review / auto-continue"),
                returning("state", "web", "13. Active direction(s) / outcome saved"),
                returning("web", "researcher", "14. Direction(s) ready for planning"),
            ],
            [
                alt_fragment(
                    "selection-outcome",
                    5,
                    6,
                    5,
                    "[score gap > tie_threshold → one candidate]",
                    "else [score gap ≤ tie_threshold → 1..N candidates]",
                ),
                opt_fragment("human-review", 10, 11, "[Human review required; otherwise auto-continue on high confidence]"),
            ],
        ),
        page(
            "UC-12 Generate & Review Experiment Plan - Main Flow",
            "Use Case Spec §18 · PRD Module H · FR-PLAN-04 / BR-78",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("state", "Planning Context Store"),
                participant("agent", "Generative Reasoner"),
            ],
            [
                call("researcher", "web", "01. Open experiment planning"),
                call("web", "state", "02. Build planning context"),
                returning("state", "web", "03. RQ, Data Card, State, history"),
                call("web", "state", "04. Resolve selected hypotheses + immutable Research State snapshots"),
                returning("state", "web", "05. Branch context + tie_threshold / max_parallel_candidates"),
                call("web", "state", "06. Check max_total_concurrent_branches"),
                returning("state", "web", "07. Branch quota available"),
                call("web", "agent", "08. Generate one independent Experiment Plan per selected branch"),
                returning("agent", "web", "09. Branch plans + methods, checks, risks"),
                returning("web", "researcher", "10. Display branch plans for review"),
                call("researcher", "web", "11. Accept / request revision / cancel"),
                call("web", "agent", "12. Revise branch plans if requested"),
                returning("agent", "web", "13. Revised branch plans"),
                call("web", "state", "14. Persist accepted plans = Ready"),
                returning("state", "web", "15. Plan states saved"),
                returning("web", "researcher", "16. Plans ready for method review"),
            ],
            [
                loop_fragment("selected-branches", 7, 8, "[for each selected hypothesis branch]"),
                opt_fragment("plan-revision", 11, 12, "[Request Revision]"),
            ],
        ),
        page(
            "UC-13 Review Method Selection & Assumption Checks - Main Flow",
            "Use Case Spec §19 · PRD Modules I/J · BR-21 / BRule-36",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("agent", "AI Research Agent"),
                participant("tools", "Analytical Tools"),
                participant("method", "Method Store"),
            ],
            [
                call("researcher", "web", "01. Open method selection review"),
                call("web", "agent", "02. Generate candidate methods + assumptions"),
                returning("agent", "web", "03. Candidate methods + required checks"),
                call("web", "tools", "04. Run deterministic assumption checks"),
                returning("tools", "web", "05. Pass / Fail / Warning / N/A"),
                call("web", "agent", "06. Check single method vs limited method branching + combined branch cap"),
                returning("agent", "web", "07. Method candidates + branch quota"),
                call("web", "agent", "08. Compare candidates + select suitable method"),
                returning("agent", "web", "09. Selected method + rationale + alternatives"),
                returning("web", "researcher", "10. Display method + assumption results"),
                call("researcher", "web", "11. Review / confirm method"),
                call("web", "method", "12. Persist selected method + rationale"),
                returning("method", "web", "13. Method decision saved"),
                returning("web", "researcher", "14. Method ready for execution"),
            ],
            [
                alt_fragment(
                    "method-result",
                    3,
                    8,
                    5,
                    "[Single / suitable method]",
                    "else [Limited method branching / re-check]",
                )
            ],
        ),
        page(
            "UC-14 Execute Experiment - Main Flow",
            "Use Case Spec §20 · PRD Module L / Execution Trace · BR-78",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("agent", "AI Research Agent"),
                participant("router", "Tool Router"),
                participant("sandbox", "Secure Sandbox"),
                participant("trace", "Execution Trace Store"),
            ],
            [
                call("researcher", "web", "01. Run approved experiment"),
                call("web", "agent", "02. Create Execution Run with branch ID / immutable snapshot"),
                call("agent", "router", "03. Select required tool within concurrency quota"),
                call("router", "sandbox", "04. Execute code / query in isolation"),
                returning("sandbox", "router", "05. Raw output / error / artifacts / metadata"),
                returning("router", "agent", "06. Execution result + tool metadata"),
                call("agent", "router", "07. Observe + classify technical error"),
                call("agent", "router", "08. Retry same approach or re-plan"),
                call("router", "sandbox", "09. Re-execute bounded run"),
                returning("sandbox", "router", "10. Retry result"),
                returning("router", "agent", "11. Retry result + trace metadata"),
                call("agent", "trace", "12. Save Execution Trace"),
                returning("trace", "agent", "13. Trace persisted"),
                returning("agent", "web", "14. Success → Experiment = Validating"),
                returning("web", "researcher", "15. Execution result / status"),
            ],
            [opt_fragment("technical-retry", 6, 10, "[Technical retry only if execution fails]")],
        ),
        page(
            "UC-15 Review Deterministic Scientific Validation - Main Flow",
            "Use Case Spec §21 · PRD Modules M/N/O/P · BR-49/78",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("validator", "Scientific Validator"),
                participant("checks", "Data / Leakage Checks"),
                participant("stats", "Statistical Service"),
                participant("store", "Validation Store"),
            ],
            [
                call("researcher", "web", "01. Open validation review"),
                call("web", "validator", "02. Start deterministic validation"),
                call("validator", "store", "03. Load execution result + artifacts"),
                returning("store", "validator", "04. Result metadata + outputs"),
                call("validator", "checks", "05. Re-check assumptions, leakage, stability"),
                returning("checks", "validator", "06. Scientific check results"),
                call("validator", "stats", "07. Load testing_family_id + tied sibling experiment set"),
                returning("stats", "validator", "08. Apply Holm / FDR across tied set + effect size / CI"),
                call("validator", "validator", "09. Check unsupported causal language + integrity"),
                call("validator", "store", "10. Save Scientific Validation Record"),
                returning("store", "validator", "11. Record persisted"),
                returning("validator", "web", "12. Passed / Warnings / Review / Failed"),
                returning("web", "researcher", "13. Validation summary"),
            ],
        ),
        page(
            "UC-16 Review / Resolve Evidence Sufficiency Decision - Main Flow",
            "Use Case Spec §22 · PRD Module AE · BR-61/78",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("state", "Research State"),
                participant("gate", "Evidence Sufficiency Gate"),
            ],
            [
                call("researcher", "web", "01. Open evidence-sufficiency review"),
                call("web", "state", "02. Load validated facts + active Research State"),
                returning("state", "web", "03. Facts, conflicts, replication, State version"),
                call("web", "gate", "04. Evaluate stats, CI, assumptions, consistency, uncertainty per branch"),
                returning("gate", "web", "05. Per-branch ENOUGH / NEED_MORE / ALTERNATIVE / REPLICATE / HUMAN / INCONCLUSIVE"),
                call("web", "state", "06. Save per-branch Evidence Decision Records + reasons"),
                returning("state", "web", "07. Decision history persisted"),
                returning("web", "researcher", "08. Sibling outcomes + review task"),
                call("researcher", "web", "09. Confirm / override if required"),
                call("web", "state", "10. Wait for all sibling branch decisions"),
                call("web", "state", "11. Check sibling outcomes compatible"),
                returning("state", "web", "12. Route compatible outcomes or human review"),
                returning("web", "researcher", "13. Next action available"),
            ],
            [
                alt_fragment(
                    "evidence-outcome",
                    10,
                    12,
                    11,
                    "[Sibling outcomes compatible → route]",
                    "else [Researcher review / resolve conflict]",
                )
            ],
        ),
        page(
            "UC-17 Resolve Scientific Refinement / Human Review - Main Flow",
            "Use Case Spec §23 · PRD Module AF",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("agent", "AI Research Agent"),
                participant("budget", "Budget / Policy Service"),
            ],
            [
                call("researcher", "web", "01. Open refinement / human-review task"),
                call("web", "agent", "02. Classify refinement / human review / inconclusive"),
                call("web", "agent", "03. Re-plan additional / alternative / replication experiment"),
                returning("agent", "web", "04. Proposed next action + lineage"),
                returning("web", "researcher", "05. Show action + budget impact"),
                call("researcher", "web", "06. Approve / modify / reject / alternative / stop"),
                call("web", "budget", "07. Check experiment, time and cost budget"),
                returning("budget", "web", "08. Budget decision"),
                call("web", "agent", "09. Create next plan / replication run if continue"),
                returning("agent", "web", "10. Next experiment queued"),
                returning("web", "researcher", "11. Refinement lineage saved"),
            ],
            [
                alt_fragment(
                    "refinement-route",
                    1,
                    9,
                    3,
                    "[SCIENTIFIC_REFINEMENT]",
                    "else [HUMAN_REVIEW / INCONCLUSIVE]",
                )
            ],
        ),
        page(
            "UC-18 Review Research Finding - Main Flow",
            "Use Case Spec §24 · PRD Modules Q/X · BR-53/78",
            [
                participant("researcher", "Researcher / Reviewer", True),
                participant("web", "Web App"),
                participant("agent", "AI Research Agent"),
                participant("provenance", "Provenance Service"),
                participant("state", "Research State"),
            ],
            [
                call("researcher", "web", "01. Open finding review"),
                call("web", "agent", "02. Generate finding statement from validated evidence"),
                call("agent", "provenance", "03. Assemble H / E / branch snapshot / testing family / validation / gate"),
                returning("provenance", "agent", "04. Provenance completeness"),
                returning("agent", "web", "05. Finding candidate + evidence links"),
                returning("web", "researcher", "06. Display finding for review"),
                call("researcher", "web", "07. Set Validated / Review / Rejected / Conflict / Invalidated; retain all valid siblings"),
                call("web", "provenance", "08. Check + save finding status"),
                returning("provenance", "web", "09. Finding state saved"),
                call("web", "state", "10. Update shared Research State after sibling join if validated"),
                returning("state", "web", "11. State version updated"),
                returning("web", "researcher", "12. Finding + lineage ready for loop"),
            ],
        ),
        page(
            "UC-19 Review Dependency, Invalidation & Conflicting Evidence - Main Flow",
            "Use Case Spec §25 · PRD Modules S/T · BR-51/53/78",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("dependency", "Dependency Service"),
                participant("store", "Experiment Store"),
                participant("agent", "AI Research Agent"),
            ],
            [
                call("researcher", "web", "01. Open dependency / conflict view"),
                call("web", "dependency", "02. Load RQ → State → H → E → Finding graph + co_selected_with"),
                call("dependency", "store", "03. Fetch linked artifacts + statuses"),
                returning("store", "dependency", "04. Lineage and evidence state"),
                returning("dependency", "web", "05. Graph + impact summary"),
                returning("web", "researcher", "06. Display dependency edges"),
                call("researcher", "web", "07. Inspect edge / review conflict"),
                call("web", "dependency", "08. Record co_selected_with siblings; distinguish valid siblings from same-H conflicts"),
                call("dependency", "agent", "09. Recommend re-run / refine / preserve action"),
                returning("agent", "dependency", "10. Recommended next action"),
                call("dependency", "store", "11. Preserve all valid sibling findings; mark affected descendants Needs Re-validation"),
                returning("store", "dependency", "12. Updated downstream states"),
                returning("dependency", "web", "13. Conflict / invalidation saved"),
                returning("web", "researcher", "14. Re-run / refine / limitation available"),
            ],
            [
                opt_fragment("dependency-impact", 7, 12, "[If upstream invalidation or conflict is detected]"),
            ],
        ),
        page(
            "UC-20 Continue or Stop Research Loop - Main Flow",
            "Use Case Spec §26 · PRD Module U · BR-30/78",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("state", "Research State"),
            ],
            [
                call("researcher", "web", "01. Open loop decision"),
                call("web", "state", "02. Load evidence, candidates, sibling branches, conflicts, budgets"),
                returning("state", "web", "03. Current research state"),
                call("web", "state", "04. Evaluate cumulative experiment / time / cost budget across all K branches"),
                returning("web", "researcher", "05. Continue / Stop recommendation + reason"),
                call("researcher", "web", "06. Confirm or override"),
                call("web", "state", "07. Persist loop decision"),
                returning("state", "web", "08. Decision saved"),
                call("web", "state", "09. Route [Continue] → UC-10 or [Stop] → Completed after branch join"),
                returning("web", "researcher", "10. Next candidates or final-output handoff"),
            ],
            [alt_fragment("continue-stop", 8, 9, 8, "[Continue → UC-10]", "else [Stop → Completed]")],
        ),
        page(
            "UC-21 Generate Figures, Tables & Research Report - Main Flow",
            "Use Case Spec §27 · PRD Module AH · BR-73/74/75",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("findings", "Findings Store"),
                participant("agent", "AI Research Agent"),
                participant("output", "Output Tool"),
            ],
            [
                call("researcher", "web", "01. Choose figure / table / report / manuscript / package"),
                call("web", "findings", "02. Load eligible validated findings + metadata"),
                returning("findings", "web", "03. Findings + provenance context"),
                call("web", "agent", "04. Generate evidence-backed figures / tables"),
                call("agent", "output", "05. Create figure / table artifacts"),
                returning("output", "agent", "06. Artifact + reproducibility metadata"),
                call("web", "output", "07. Persist figure / table candidates"),
                returning("output", "web", "08. Candidate outputs + source linkage"),
                call("web", "output", "09. Aggregate figures + visual feedback / duplicate / caption checks"),
                returning("output", "web", "10. Aggregated visual feedback"),
                call("web", "agent", "11. Generate research report from validated findings"),
                returning("agent", "web", "12. Report + source linkage"),
                returning("web", "researcher", "13. Review report / request manuscript"),
                call("web", "agent", "14. Generate manuscript draft; verify numbers / citations; mark AI content"),
                returning("agent", "web", "15. Manuscript draft + integrity checks"),
                call("web", "agent", "16. Run automated manuscript review (soundness / novelty / clarity)"),
                returning("agent", "web", "17. Manuscript review result"),
                call("researcher", "web", "18. Approve manuscript for external use / export"),
                returning("web", "researcher", "19. Approval status + export decision"),
                call("web", "output", "20. Generate reproducibility package"),
                returning("output", "web", "21. Package + export record"),
                returning("web", "researcher", "22. Final output confirmation"),
            ],
            [
                opt_fragment("figure-aggregation", 8, 9, "[Figure aggregation enabled]"),
                opt_fragment("manuscript-pipeline", 13, 18, "[Manuscript requested]"),
                opt_fragment("automated-manuscript-review", 15, 16, "[Automated review enabled]"),
                alt_fragment(
                    "external-approval",
                    17,
                    18,
                    17,
                    "[External export/share → researcher approval]",
                    "else [Internal review only]",
                ),
            ],
        ),
        page(
            "UC-22 View Research Outputs, Provenance, Evidence, Trace & Decision History - Main Flow",
            "Use Case Spec §28 · PRD Modules X/Y/AG/AH · BR-64/65/73-75/78",
            [
                participant("researcher", "Researcher / Reviewer", True),
                participant("web", "Web App"),
                participant("provenance", "Provenance Service"),
                participant("history", "Decision History"),
                participant("trace", "Execution Trace Store"),
            ],
            [
                call("researcher", "web", "01. Open finding / research output"),
                call("web", "provenance", "02. Load provenance chain incl. Idea Record + Reflection"),
                call("provenance", "history", "03. Load selection Decision Record + tie_threshold_used + tied_candidates"),
                returning("history", "provenance", "04. Decisions, confidence, overrides, co-selection metadata"),
                call("provenance", "trace", "05. Load execution trace + branch snapshots + testing family"),
                returning("trace", "provenance", "06. Steps, tools, inputs, outputs, errors, cost"),
                returning("provenance", "web", "07. Linked evidence + provenance + decisions"),
                returning("web", "researcher", "08. Display lineage / output"),
                call("researcher", "web", "09. Open trace / decision detail"),
                call("web", "trace", "10. Load detailed execution trace"),
                returning("trace", "web", "11. Trace + retry / refinement categories"),
                returning("web", "researcher", "12. Trace detail / linked artifacts"),
            ],
        ),
        page(
            "UC-23 Run Benchmark & Evaluation - Main Flow",
            "Use Case Spec §29 · PRD Modules AA/AG · BR-63/78",
            [
                participant("researcher", "Researcher / Project Manager / System Administrator", True),
                participant("web", "Web App"),
                participant("config", "Agent / Gate Config"),
                participant("runner", "Benchmark Runner"),
                participant("sandbox", "Secure Sandbox"),
                participant("evaluation", "Evaluation Store"),
            ],
            [
                call("researcher", "web", "01. Choose benchmark, config(s), N, single/tied-selection arm"),
                call("web", "config", "02. Load model, decision-provider, tie threshold and branch-cap configuration"),
                returning("config", "web", "03. Benchmark configuration"),
                call("web", "runner", "04. Start benchmark"),
                call("runner", "sandbox", "05. Execute one benchmark run"),
                returning("sandbox", "runner", "06. Output + trace + runtime metadata"),
                call("runner", "evaluation", "07. Save decisions, scores, confidence, branch/testing-family metadata, cost"),
                returning("evaluation", "runner", "08. Run record saved"),
                returning("runner", "web", "09. Run score + quality metrics"),
                call("web", "evaluation", "10. Aggregate score calibration, tied-selection frequency/correctness, reproducibility and cost metrics"),
                returning("evaluation", "web", "11. Evaluation dashboard data"),
                returning("web", "researcher", "12. Display evaluation dashboard"),
                call("researcher", "web", "13. Compare configurations: single-candidate vs tied-selection + ablation"),
                call("web", "evaluation", "14. Save comparison result"),
                returning("evaluation", "web", "15. Comparison persisted"),
                returning("web", "researcher", "16. Export evaluation report"),
            ],
            [loop_fragment("benchmark-runs", 4, 8, "[i = 1..N]")],
        ),
        page(
            "UC-24 Manage Models, Decision Providers, Logs, Cost & System Configuration - Main Flow",
            "Use Case Spec §30 · PRD Module AG / Admin · BR-78",
            [
                participant("admin", "Admin", True),
                participant("console", "Admin Console"),
                participant("config", "Configuration Service"),
                participant("provider", "Decision Provider Registry"),
                participant("audit", "Audit / Monitoring"),
            ],
            [
                call("admin", "console", "01. Open admin console"),
                call("console", "config", "02. Load models, providers, tie thresholds, branch caps, logs, cost"),
                returning("config", "console", "03. Operational configuration + health"),
                returning("console", "admin", "04. Display management controls"),
                call("admin", "console", "05. Submit configuration changes"),
                call("console", "config", "06. Validate + version configuration"),
                call("config", "provider", "07. Apply rollout / fallback policy"),
                returning("provider", "config", "08. Provider configuration ready"),
                call("config", "audit", "09. Record audit event"),
                returning("audit", "config", "10. Audit record saved"),
                returning("config", "console", "11. Configuration saved"),
                returning("console", "admin", "12. Updated system state"),
            ],
        ),
        page(
            "UC-25 Manage Research Definition - Main Flow",
            "Use Case group Manage Research Definition · BRD §§12–15 · PRD Modules B–G, AC",
            [
                participant("actor", "Researcher / Project Manager", True),
                participant("web", "Web App"),
                participant("definition", "Research Definition Service"),
                participant("state", "Research State Service"),
            ],
            [
                call("actor", "web", "01. Open research definition workspace"),
                call("web", "definition", "02. Load project scope, dataset, question and current definition"),
                returning("definition", "web", "03. Current research definition + validation status"),
                call("actor", "web", "04. Submit / revise project members, dataset, research question and context"),
                call("web", "definition", "05. Validate definition completeness and source references"),
                returning("definition", "web", "06. Validation result + missing-field guidance"),
                call("web", "state", "07. Build and version active Research State"),
                returning("state", "web", "08. Research State version + constraints"),
                call("web", "definition", "09. Persist approved research definition and audit metadata"),
                returning("definition", "web", "10. Definition saved"),
                returning("web", "actor", "11. Research definition ready for hypothesis generation"),
            ],
            [
                alt_fragment(
                    "definition-validity",
                    4,
                    5,
                    4,
                    "[Valid → version Research State]",
                    "else [Return validation errors for revision]",
                )
            ],
        ),
        page(
            "UC-26 Manage Hypotheses - Main Flow",
            "Use Case group Manage Hypotheses · BRD §§14–15 · PRD Modules AD, AH · BR-64/65/78",
            [
                participant("researcher", "Researcher", True),
                participant("web", "Web App"),
                participant("hypothesis", "Hypothesis Service"),
                participant("gate", "Structured Decision Gate"),
                participant("state", "Research State / Decision Store"),
            ],
            [
                call("researcher", "web", "01. Open hypothesis management"),
                call("web", "state", "02. Load active Research State and candidate set"),
                returning("state", "web", "03. Candidate context + current directions"),
                call("web", "hypothesis", "04. Create / update Structured Idea Record"),
                returning("hypothesis", "web", "05. Idea record draft"),
                call("web", "hypothesis", "06. Perform Reflection Round and record open questions"),
                returning("hypothesis", "web", "07. Reflection record + testability risks"),
                call("web", "hypothesis", "08. Assess novelty from available source / context"),
                returning("hypothesis", "web", "09. Novelty result + references, or Not Assessed"),
                call("web", "gate", "10. Evaluate relevance, testability, evidence and feasibility"),
                returning("gate", "web", "11. Numeric score, confidence and decision reasons"),
                call("web", "state", "12. Persist candidate set, Decision Record and active direction metadata"),
                returning("state", "web", "13. Hypothesis management state saved"),
                returning("web", "researcher", "14. Candidates and selection outcome ready"),
            ],
            [
                opt_fragment("hypothesis-novelty", 7, 8, "[Novelty feature enabled]"),
                alt_fragment(
                    "hypothesis-novelty-input",
                    7,
                    8,
                    7,
                    "[Source / context available → assess novelty]",
                    "else [Record Not Assessed]",
                ),
            ],
        ),
        page(
            "UC-27 Manage Experiments - Main Flow",
            "Use Case group Manage Experiments · BRD §§13, 15–16 · PRD Modules H–P, U · BR-21/49/78",
            [
                participant("actor", "Researcher / Project Manager", True),
                participant("web", "Web App"),
                participant("planner", "Experiment Planner / AI Agent"),
                participant("method", "Method & Assumption Service"),
                participant("execution", "Experiment Execution Service"),
                participant("state", "Research State / Experiment Store"),
            ],
            [
                call("actor", "web", "01. Open experiment management"),
                call("web", "state", "02. Load selected directions, immutable snapshots and branch budget"),
                returning("state", "web", "03. Branch context + concurrency constraints"),
                call("web", "planner", "04. Generate / revise one Experiment Plan per selected branch"),
                returning("planner", "web", "05. Branch plans, methods, risks and expected outputs"),
                call("web", "method", "06. Validate methods, assumptions and total branch cap"),
                returning("method", "web", "07. Method suitability + quota result"),
                returning("web", "actor", "08. Plans ready for approval"),
                call("actor", "web", "09. Approve plan and start bounded execution"),
                call("web", "execution", "10. Execute approved branch in secure sandbox"),
                returning("execution", "web", "11. Branch result, artifacts, trace and runtime metadata"),
                call("web", "state", "12. Persist plan / run status and branch lineage"),
                returning("state", "web", "13. Experiment state updated"),
                returning("web", "actor", "14. Experiment management result"),
            ],
            [
                loop_fragment("experiment-branches", 3, 6, "[for each selected hypothesis branch]"),
                opt_fragment("start-execution", 8, 9, "[Approved plan is executed]"),
            ],
        ),
        page(
            "UC-28 Manage Research Findings - Main Flow",
            "Use Case group Manage Research Findings · BRD §§16–16.2 · PRD Modules Q–T, X–Z · BR-49/51/53/61/78",
            [
                participant("actor", "Researcher / Reviewer", True),
                participant("web", "Web App"),
                participant("finding", "Finding Service"),
                participant("validation", "Scientific Validation / Evidence Gate"),
                participant("provenance", "Provenance Service"),
                participant("state", "Research State / Finding Store"),
            ],
            [
                call("actor", "web", "01. Open research findings workspace"),
                call("web", "finding", "02. Load validated branch results and existing findings"),
                returning("finding", "web", "03. Findings + branch status"),
                call("web", "validation", "04. Evaluate evidence sufficiency and sibling compatibility"),
                returning("validation", "web", "05. Evidence decision, uncertainty and next-action route"),
                call("web", "provenance", "06. Resolve hypothesis, dataset, method and execution lineage"),
                returning("provenance", "web", "07. Provenance chain + trace references"),
                call("web", "finding", "08. Create / update Finding with limitations and confidence"),
                call("web", "state", "09. Persist finding status, dependency links and decision history"),
                returning("state", "web", "10. Finding state saved"),
                returning("web", "actor", "11. Finding review result + next action"),
            ],
            [
                alt_fragment(
                    "finding-route",
                    3,
                    4,
                    3,
                    "[Enough evidence → eligible finding]",
                    "else [Refine / replicate / human review / inconclusive]",
                )
            ],
        ),
        page(
            "UC-29 Manage Research Outputs - Main Flow",
            "Use Case group Manage Research Outputs · BRD §17.1 · PRD Module AH · BR-73–75",
            [
                participant("actor", "Researcher / Reviewer", True),
                participant("web", "Web App"),
                participant("findings", "Validated Findings Store"),
                participant("report", "Output & Manuscript Agent"),
                participant("output", "Figure / Report / Export Store"),
            ],
            [
                call("actor", "web", "01. Open research outputs workspace"),
                call("web", "findings", "02. Load eligible findings, provenance and review status"),
                returning("findings", "web", "03. Findings and source linkage"),
                call("web", "report", "04. Generate figures, tables and research report"),
                returning("report", "web", "05. Report artifacts + integrity metadata"),
                call("web", "report", "06. Generate manuscript draft and run automated review"),
                returning("report", "web", "07. Draft, review findings and requested revisions"),
                returning("web", "actor", "08. Review output package and manuscript"),
                call("actor", "web", "09. Approve internal output or request revision / export"),
                call("web", "output", "10. Persist approved output, reproducibility package and export record"),
                returning("output", "web", "11. Output package saved"),
                returning("web", "actor", "12. Final output confirmation"),
            ],
            [
                opt_fragment("manuscript-output", 5, 6, "[Manuscript requested]"),
                alt_fragment(
                    "output-approval",
                    8,
                    9,
                    8,
                    "[Approved → persist output / export record]",
                    "else [Revise draft and repeat automated review]",
                ),
            ],
        ),
        page(
            "UC-30 Manage System Administration - Main Flow",
            "Use Case group Manage System Administration · BRD §17 · PRD Module AG / Admin · BR-63/78",
            [
                participant("admin", "System Administrator", True),
                participant("console", "Admin Console"),
                participant("config", "Configuration Service"),
                participant("provider", "Decision Provider Registry"),
                participant("audit", "Audit / Monitoring Service"),
            ],
            [
                call("admin", "console", "01. Open system administration console"),
                call("console", "config", "02. Load models, providers, thresholds, branch caps, logs and cost"),
                returning("config", "console", "03. Current configuration + health status"),
                returning("console", "admin", "04. Display administration controls"),
                call("admin", "console", "05. Submit model / provider / policy configuration changes"),
                call("console", "config", "06. Validate, version and stage configuration"),
                returning("config", "console", "07. Configuration validation result"),
                call("config", "provider", "08. Apply rollout, fallback and decision-provider policy"),
                returning("provider", "config", "09. Provider configuration ready"),
                call("config", "audit", "10. Record audit, usage, cost and operational events"),
                returning("audit", "config", "11. Audit record + monitoring status"),
                returning("config", "console", "12. Configuration saved and active"),
                returning("console", "admin", "13. Updated system administration state"),
            ],
            [
                alt_fragment(
                    "admin-configuration",
                    5,
                    8,
                    6,
                    "[Valid configuration → apply rollout]",
                    "else [Reject and retain previous version]",
                )
            ],
        ),
    ]


TITLE_STYLE = (
    "text;html=1;align=center;verticalAlign=middle;fontFamily=Times New Roman;"
    "fontSize=18;fontStyle=1;fontColor=#000000;"
)
NOTATION_STYLE = (
    "text;html=1;align=center;verticalAlign=middle;fontFamily=Times New Roman;"
    "fontSize=10;fontColor=#666666;"
)


def load_layout():
    if not LAYOUT_SCRIPT.exists():
        raise FileNotFoundError(f"Missing drawio-skill layout script: {LAYOUT_SCRIPT}")
    spec = importlib.util.spec_from_file_location("drawio_seqlayout", LAYOUT_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {LAYOUT_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.layout


COMPACT_ALT_HEADERS = {
    "hypothesis-selection": "alt [SELECT / else review]",
    "selection-resolution": "alt [SELECT / else review]",
    "selection-outcome": "alt [single / tied]",
    "evidence-gate": "alt [ENOUGH / else refine]",
    "evidence-outcome": "alt [ENOUGH / else refine]",
    "stopping": "alt [CONTINUE / STOP]",
    "continue-stop": "alt [CONTINUE / STOP]",
    "method-suitability": "alt [SUITABLE / else alternative]",
    "method-result": "alt [SUITABLE / else alternative]",
    "refinement-route": "alt [REFINE / else human]",
    "definition-validity": "alt [VALID / else INVALID]",
    "hypothesis-novelty-input": "alt [SOURCE / else NOT ASSESSED]",
    "finding-route": "alt [ENOUGH / else REFINE]",
    "output-approval": "alt [APPROVED / else REVISE]",
    "admin-configuration": "alt [VALID / else REJECT]",
}


def add_page_header(diagram: ET.Element, source_index: int) -> None:
    model = diagram.find("mxGraphModel")
    if model is None:
        raise ValueError("Generated page has no mxGraphModel")
    graph_root = model.find("root")
    if graph_root is None:
        raise ValueError("Generated page has no graph root")

    offset = 30
    page_width = int(float(model.get("pageWidth", "1200")))
    for cell in graph_root.findall("mxCell"):
        if cell.get("vertex") != "1" or cell.get("parent") != "1":
            continue
        geometry = cell.find("mxGeometry")
        if geometry is None or geometry.get("y") is None:
            continue
        geometry.set("y", str(float(geometry.get("y", "0")) + offset).rstrip("0").rstrip("."))

    # Put alt branch conditions into the frame header. The default seqlayout
    # branch cells are positioned on message rows and can cover their labels
    # on compact pages, so a single explicit frame header is more readable.
    remove_ids: set[str] = set()
    for frame in graph_root.findall("mxCell"):
        frame_id = frame.get("id", "")
        if not frame_id.startswith("fragment_") or frame_id.endswith("_divider") or "_label_" in frame_id:
            continue
        frame_style = frame.get("style", "")
        frame_style = frame_style.replace("spacingLeft=130;", "spacingLeft=8;")
        frame_style = frame_style.replace("whiteSpace=wrap;", "whiteSpace=nowrap;fontSize=11;")
        frame_style = frame_style.replace("fontSize=12;", "fontSize=11;")
        frame.set("style", frame_style)
        frame_geometry = frame.find("mxGeometry")
        if frame_geometry is not None and frame_geometry.get("y") is not None and frame_geometry.get("height") is not None:
            frame_geometry.set("y", str(float(frame_geometry.get("y", "0")) - 38).rstrip("0").rstrip("."))
            frame_geometry.set("height", str(float(frame_geometry.get("height", "0")) + 38).rstrip("0").rstrip("."))
        top_label = graph_root.find(f"mxCell[@id='{frame_id}_label_0']")
        bottom_label = graph_root.find(f"mxCell[@id='{frame_id}_label_1']")
        if top_label is not None or bottom_label is not None:
            fragment_key = frame_id.removeprefix("fragment_")
            frame.set("value", COMPACT_ALT_HEADERS.get(fragment_key, "alt"))
            if top_label is not None:
                remove_ids.add(frame_id + "_label_0")
            if bottom_label is not None:
                remove_ids.add(frame_id + "_label_1")
    for cell in list(graph_root.findall("mxCell")):
        if cell.get("id") in remove_ids:
            graph_root.remove(cell)

    page_height = int(float(model.get("pageHeight", "1200"))) + offset
    model.set("pageHeight", str(page_height))

    name = diagram.get("name", "Sequence")
    source = diagram.get("data-source", "")
    title = ET.Element(
        "mxCell",
        {
            "id": "page_title",
            "value": name,
            "style": TITLE_STYLE,
            "vertex": "1",
            "parent": "1",
        },
    )
    ET.SubElement(
        title,
        "mxGeometry",
        {"x": "20", "y": "0", "width": str(max(400, page_width - 40)), "height": "26", "as": "geometry"},
    )
    notation = ET.Element(
        "mxCell",
        {
            "id": "page_notation",
            "value": (
                f"{source} · Solid = call / request · grey dashed filled arrow = return "
                "to immediate caller · internal work = regular hand-off · time flows top → bottom"
            ),
            "style": NOTATION_STYLE,
            "vertex": "1",
            "parent": "1",
        },
    )
    ET.SubElement(
        notation,
        "mxGeometry",
        {"x": "20", "y": "27", "width": str(max(400, page_width - 40)), "height": "20", "as": "geometry"},
    )
    graph_root.insert(0, notation)
    graph_root.insert(0, title)
    diagram.set("id", f"sequence-page-{source_index + 1}")
    diagram.set("data-source", source)


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def apply_reference_arrow_styles(diagram: ET.Element, spec: dict) -> None:
    """Make generated arrows match the supplied reference package.

    The layout engine emits semantic return edges with an open arrowhead.  The
    GreenLens reference uses a filled arrowhead at the caller end, so the final
    XML is adjusted here without forking the shared skill renderer.  Self-call
    edges are intentionally not styled or generated.
    """
    model = diagram.find("mxGraphModel")
    if model is None:
        raise ValueError("Generated page has no mxGraphModel")
    graph_root = model.find("root")
    if graph_root is None:
        raise ValueError("Generated page has no graph root")

    # seqlayout keeps lifeline bodies compact at 80 px.  Keep that width, but
    # give wrapped two-line headers enough vertical room for the full label.
    for lifeline in graph_root.findall("mxCell"):
        if lifeline.get("vertex") != "1" or lifeline.get("parent") != "1":
            continue
        style = lifeline.get("style", "")
        if "shape=umlLifeline" in style:
            lifeline.set("style", style.replace("size=40;", "size=56;"))

    for index, message in enumerate(spec.get("messages", [])):
        cell = graph_root.find(f"mxCell[@id='m{index}']")
        if cell is None:
            continue
        style = cell.get("style", "")
        if message.get("return"):
            style = style.replace("endArrow=open", "endArrow=block;endFill=1")
            cell.set("style", style)


def compose(pages: list[dict], output: Path, layout) -> None:
    root = ET.Element("mxfile")
    for index, source_spec in enumerate(pages):
        spec = layered_page(source_spec)
        raw_xml = layout(spec)
        generated = ET.fromstring(raw_xml)
        diagram = generated.find("diagram")
        if diagram is None:
            raise ValueError(f"No diagram generated for {spec['title']}")
        apply_reference_arrow_styles(diagram, spec)
        diagram.set("name", spec["title"])
        diagram.set("id", f"sequence-page-{index + 1}-{slug(spec['title'])}")
        diagram.set("data-source", spec["source"])
        add_page_header(diagram, index)
        root.append(diagram)
    output.write_text(ET.tostring(root, encoding="unicode"), encoding="utf-8")
    print(f"wrote {output} ({len(pages)} pages)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--view",
        choices=("all", "core", "business", "detailed"),
        default="all",
        help="generate one view or the complete sequence package (default: all)",
    )
    args = parser.parse_args()
    layout = load_layout()
    if args.view in {"all", "core"}:
        compose([core_page()], ROOT / "AI-Research-Experimentation-Platform-Sequence.drawio", layout)
    if args.view in {"all", "business"}:
        compose(
            business_pages(),
            ROOT / "AI-Research-Experimentation-Platform-Business-Main-Flows-Sequence.drawio",
            layout,
        )
    if args.view in {"all", "detailed"}:
        compose(
            detailed_pages(),
            ROOT / "AI-Research-Experimentation-Platform-Main-Flows-Sequence.drawio",
            layout,
        )


if __name__ == "__main__":
    main()
