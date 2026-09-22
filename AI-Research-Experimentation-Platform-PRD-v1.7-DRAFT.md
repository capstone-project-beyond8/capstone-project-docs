# Product Requirements Document (PRD)
## AI Research Experimentation Platform

**Document Type:** Product Requirements Document  
**Project:** AI Research Experimentation Platform  
**Version:** 1.7 Draft  
**Status:** Draft / Aligned with BRD v1.8 (Draft)  
**Source:** Business Requirements Document v1.8 (Draft)  
**Date:** 2026-09-22  

---

# 1. Product Summary

AI Research Experimentation Platform là nền tảng web sử dụng AI Agent để hỗ trợ researcher thực hiện quy trình nghiên cứu dựa trên structured/tabular datasets.

Sản phẩm không chỉ thực hiện một lần phân tích dữ liệu, mà quản lý một research loop có cấu trúc:

```text
Research Question + Dataset
        ↓
Dataset Understanding / Data Card
        ↓
Initial H0 / H1
        ↓
Build Research State
        ↓
Generate Candidate Hypotheses / Research Directions
        ↓
Structured Hypothesis Selection Gate
        ↓
Selected Hypothesis / Direction
        ↓
LLM Deep Reasoning
        ↓
Experiment Planning
        ↓
Candidate Method Generation
        ↓
Deterministic Assumption Checks
        ↓
Experiment Execution
        ↓
Deterministic Scientific Validation
        ↓
Evidence Sufficiency Gate
        ↓
Decision
├── ENOUGH_EVIDENCE → Research Finding
├── NEED_MORE_EVIDENCE → Scientific Refinement
├── TRY_ALTERNATIVE_METHOD → Scientific Refinement
├── REPLICATE → New Experiment
├── NEED_HUMAN_REVIEW → Researcher Review
└── INCONCLUSIVE → Record Outcome
        ↓
Update Research State
        ↓
Stopping Criteria?
├── Continue → Next Candidate Hypotheses
└── Stop → Final Findings → Figures/Tables → Research Report
```

Mọi finding quan trọng phải có khả năng truy ngược về:

```text
Finding
→ Hypothesis
→ Experiment
→ Dataset Version
→ Selected Method
→ Assumption Checks
→ Code / Query
→ Raw Output
→ Statistical Result
```

Platform tập trung vào sáu giá trị sản phẩm:

1. **Scientific Validity** — method phù hợp, assumptions rõ ràng, multiple-testing control, effect size và uncertainty.
2. **Structured Decision Safety** — bounded decisions như hypothesis selection và evidence sufficiency có output cấu trúc, confidence và escalation policy.
3. **Separation of Responsibilities** — LLM dùng cho generate/reason/refine; deterministic tools dùng để tính scientific facts; decision gates dùng để select/verify/route.
4. **Traceability** — mọi finding và structured decision quan trọng có provenance, decision record và execution trace.
5. **Reproducibility** — experiment có metadata/snapshot đủ để tái lập.
6. **Human Control** — researcher giữ quyền quyết định tại các bước có uncertainty/risk cao.

---

# 2. Product Vision

> Cho phép researcher biến một research question và dataset thành một chuỗi experiment có kiểm soát, tạo ra evidence-backed findings có thể kiểm chứng và tái lập, thay vì chỉ nhận một câu trả lời dạng black-box từ AI.

---

# 3. Product Goals

| ID | Product Goal |
|---|---|
| PG-01 | Cho phép researcher bắt đầu từ research question, hypothesis và dataset |
| PG-02 | Tự động profiling và hiểu dataset mà không yêu cầu khai báo schema thủ công |
| PG-03 | Tự động đề xuất candidate analytical/statistical methods |
| PG-04 | Kiểm tra assumptions trước khi thực thi method |
| PG-05 | Thực thi experiment an toàn trong sandbox và hỗ trợ retry/re-plan |
| PG-06 | Chuyển raw output thành evidence-backed finding |
| PG-07 | Sinh/refine hypothesis mới từ validated finding |
| PG-08 | Quản lý vòng lặp H → E → F → H(n+1) có stopping criteria |
| PG-09 | Quản lý provenance, dependency, conflicting evidence và downstream invalidation |
| PG-10 | Tạo figure/table/report có thể truy vết |
| PG-11 | Lưu reproducibility snapshot cho official experiments |
| PG-12 | Đánh giá agent bằng benchmark, metrics và ablation study |
| PG-13 | Xây dựng Research State có cấu trúc cho từng research iteration |
| PG-14 | Sinh và đánh giá candidate hypotheses/research directions trước deep experiment planning |
| PG-15 | Sử dụng structured hypothesis-selection gate để rank/select/reject/escalate candidate directions |
| PG-16 | Sử dụng evidence-sufficiency gate để quyết định finding, refinement, replication, review hoặc inconclusive |
| PG-17 | Đánh giá chất lượng decision gates và so sánh structured decision với LLM-only baseline |
| PG-18 | Khi candidate hypothesis ngang điểm trong ngưỡng cấu hình, chọn đồng thời một số lượng giới hạn thay vì ép chọn 1, có kiểm soát chi phí và multiple-testing |

---

# 4. Non-Goals

Phiên bản capstone không nhằm xây dựng:

- fully autonomous AI Scientist;
- autonomous literature discovery trên toàn Internet;
- automatic novelty guarantee;
- autonomous paper submission/publication;
- foundation model training;
- distributed big-data platform;
- real-time streaming analytics;
- scientific image/audio/video analysis;
- full causal-inference engine;
- Agentic Tree Search (kiểu Sakana AI Scientist-v2, kể cả một bản bounded/scoped cho một hypothesis) — platform không tổ chức experiment thành cây node cha-con với expand/select/prune; mỗi hypothesis được chọn thực thi theo một luồng tuyến tính duy nhất (Decision-Gated Research Loop, BR-21), có thể thử nhiều candidate method trong giới hạn branching hiện có nhưng không có staged multi-phase exploration hay Experiment Manager riêng.

Platform có thể tham khảo một số ý tưởng rời rạc từ các agentic research systems (ví dụ: idea reflection trước khi chọn hypothesis, novelty assessment tham khảo, automated manuscript review) mà không áp dụng kiến trúc tree-search của các hệ thống đó. Scope chính vẫn là **scientific analysis trên user-provided structured datasets** theo một luồng quyết định tuyến tính, có audit, dễ kiểm soát chi phí.

---

# 5. Target Users & Roles

## 5.1. Researcher / Data Analyst — Primary Persona

### Jobs to Be Done

- upload và hiểu dataset;
- định nghĩa research question và H0/H1;
- yêu cầu AI lập experiment plan;
- xem lý do chọn statistical method;
- review assumption checks;
- chạy experiment;
- xem result và evidence;
- review hypothesis mới;
- tạo figure/table/report;
- kiểm tra provenance và reproducibility.

### Success Definition

Researcher có thể đi từ dataset + hypothesis đến validated finding mà không phải tự viết toàn bộ workflow thủ công.

---

## 5.2. Project Manager

### Jobs to Be Done

- tạo project;
- quản lý members;
- theo dõi research progress;
- theo dõi experiment/finding history;
- review final research outputs.

---

## 5.3. Reviewer / Stakeholder

### Jobs to Be Done

- xem findings;
- xem figures/tables;
- xem methodology;
- kiểm tra evidence/provenance;
- review report;
- để lại feedback nếu được cấp quyền.

---

## 5.4. System Administrator

### Jobs to Be Done

- quản lý users/roles;
- quản lý AI model configuration;
- xem logs;
- theo dõi system health;
- theo dõi usage/cost;
- quản lý benchmark/evaluation configurations.

---

# 6. Product Principles

## PP-01 — Evidence Before Conclusion

Finding quan trọng không được xuất hiện trong official report nếu không có supporting evidence.

## PP-02 — Hypothesis Is Not Fact

Hypothesis mới do agent sinh ra luôn bắt đầu ở trạng thái `Unverified`.

## PP-03 — Unusual Does Not Mean Incorrect

Outlier/anomaly không tự động được sửa hoặc loại bỏ.

## PP-04 — Association Does Not Imply Causation

Agent không được dùng language causal khi research design chỉ hỗ trợ association/correlation.

## PP-05 — Preserve the Original

Raw dataset không bao giờ bị ghi đè.

## PP-06 — Method Selection Must Be Explainable

Agent phải lưu lý do chọn method và lý do loại candidate khác khi cần.

## PP-07 — Human Controls High-Risk Decisions

Risky cleaning, ambiguous variable meaning, conflicting evidence hoặc strong causal interpretation phải có human review.

## PP-08 — Reproducibility by Default

Official experiment phải có reproducibility snapshot.

## PP-09 — Tools Establish Scientific Facts

Statistical values, diagnostics và deterministic checks phải đến từ analytical/statistical tools khi có thể. LLM hoặc decision model không được tự phát minh scientific facts.

## PP-10 — Structured Decisions Before Automation

Các bounded decision quan trọng phải dùng structured output có decision type, confidence/uncertainty và downstream action.

## PP-11 — Technical Retry Is Not Scientific Refinement

Execution failure được xử lý bằng technical retry/re-plan; valid execution nhưng evidence chưa đủ phải đi vào scientific refinement.

## PP-12 — Confidence Does Not Replace Evidence

Confidence của decision gate chỉ dùng cho routing/escalation, không thay thế p-value, effect size, confidence interval, diagnostics hoặc evidence thực tế.

---

# 7. Product Scope & Priority

## 7.1. P0 — Core MVP

- authentication;
- RBAC cơ bản;
- research project;
- dataset upload;
- dataset validation;
- profiling;
- Data Card;
- research question;
- H0/H1;
- Research State;
- candidate hypothesis / research-direction generation;
- idea record & reflection (Module AH, BR-64, Must);
- structured decision-provider interface;
- experiment planner;
- candidate method generation;
- assumption checking;
- method selection;
- secure experiment execution;
- retry/re-plan;
- statistical result;
- finding generation;
- provenance;
- execution trace;
- dataset versioning.

## 7.2. P1 — Research Loop & Scientific Validity

- hypothesis refinement;
- hypothesis origin/status;
- structured Hypothesis Selection Gate;
- Evidence Sufficiency Gate;
- scientific refinement loop;
- confidence-based human escalation;
- decision audit trail;
- decision-gate evaluation;
- stopping criteria;
- limited experiment branching (Must for final capstone per BRD BR-21; grouped here because it depends on P1 method-selection scope);
- multiple-testing control;
- effect size;
- confidence interval;
- data leakage guard;
- experiment dependency graph;
- conflicting evidence;
- downstream invalidation;
- uncertainty/confidence metadata;
- figure/table generation;
- research report;
- reproducibility snapshot;
- evaluation center;
- benchmark;
- ablation;
- novelty assessment (tham khảo, Module AH, BR-65);
- figure aggregation & visual feedback (Module AH, BR-73);
- manuscript draft generation (Module AH, BR-74);
- automated manuscript review (Module AH, BR-75).

## 7.3. P2 — Extension

- figure/VLM reviewer;
- literature connectors;
- advanced ML;
- collaborative editing;
- scheduled experiments;
- external database connectors;
- advanced research templates.

---

# 8. Information Architecture

Primary project navigation:

```text
Project Overview
├── Research
│   ├── Research Questions
│   ├── Research State
│   ├── Candidate Hypotheses
│   ├── Active Hypothesis
│   ├── Decision History
│   └── Research Loop
├── Datasets
│   ├── Dataset List
│   ├── Data Card
│   ├── Data Quality
│   └── Versions
├── Experiments
│   ├── Plans
│   ├── Runs
│   ├── Dependency Graph
│   └── Execution Trace
├── Findings
│   ├── Validated Findings
│   ├── Conflicting Evidence
│   ├── Evidence Sufficiency Decisions
│   └── Evidence View
├── Outputs
│   ├── Figures
│   ├── Tables
│   └── Reports
├── Evaluation
│   ├── Benchmarks
│   ├── Runs
│   ├── Metrics
│   └── Ablations
└── Project Settings
```

Admin navigation:

```text
Users
Roles
Model Configuration
System Logs
Usage / Cost
Evaluation Configuration
System Health
```

---

# 9. Primary End-to-End User Flow

```text
Login
↓
Create/Open Project
↓
Upload Dataset
↓
Dataset Validation
↓
Automatic Profiling + Data Card
↓
Review Data Quality
↓
Apply Approved Cleaning if needed
↓
Enter Research Question
↓
Define / Confirm Initial H0/H1
↓
Build Research State
↓
Generate Candidate Hypotheses / Research Directions
↓
Structured Hypothesis Selection Gate
├── Select → Continue
├── Reject → Remove Candidate
└── Low Confidence / High Risk → Researcher Review
↓
Selected Hypothesis / Direction
↓
LLM Deep Reasoning
↓
Generate Experiment Plan
↓
Generate Candidate Methods
↓
Deterministic Assumption Checks
↓
Select Method / Limited Branch
↓
Execute in Secure Sandbox
↓
Execution Successful?
├── No → Technical Retry / Re-plan
└── Yes
     ↓
Deterministic Scientific Validation
↓
Evidence Sufficiency Gate
├── ENOUGH_EVIDENCE → Generate Finding
├── NEED_MORE_EVIDENCE → LLM Re-plan
├── TRY_ALTERNATIVE_METHOD → LLM Re-plan
├── REPLICATE → New Experiment
├── NEED_HUMAN_REVIEW → Researcher Review
└── INCONCLUSIVE → Record Outcome
↓
Update Research State
↓
Stopping Criteria?
├── No → Generate Next Candidate Hypotheses → Selection Gate → Next Iteration
└── Yes → Final Findings → Figures/Tables → Research Report → Reproducibility Package
```

### Product Rule

The product must visibly distinguish:

```text
Technical Retry
= execution failed

Scientific Refinement
= execution succeeded, but evidence is insufficient
```

These paths must have different states, trace entries and evaluation metrics.

---

# 10. Feature Module A — Authentication & Access Control

## Objective

Đảm bảo user chỉ truy cập project và action được cấp quyền.

## User Stories

**US-AUTH-01**  
As a user, I want to sign in securely so that I can access my research projects.

**US-AUTH-02**  
As a project manager, I want to assign project roles so that members have appropriate permissions.

**US-AUTH-03**  
As an admin, I want to manage global roles and access so that the platform remains controlled.

## Functional Requirements

### FR-AUTH-01 — Login

System shall support authenticated login.

### FR-AUTH-02 — Session / Token

System shall maintain authenticated session/token and reject expired/invalid sessions.

### FR-AUTH-03 — Project Membership

A user must be a project member or privileged admin to access project resources.

### FR-AUTH-04 — Role Enforcement

Actions must be checked server-side, not only hidden in frontend.

## Minimum Permission Model

| Capability | Admin | Project Manager | Researcher | Reviewer |
|---|---:|---:|---:|---:|
| Manage system users | ✓ |  |  |  |
| Create project | ✓ | ✓ | ✓ |  |
| Manage project members | ✓ | ✓ |  |  |
| Upload dataset | ✓ | ✓ | ✓ |  |
| Apply cleaning | ✓ | ✓ | ✓ |  |
| Create hypothesis | ✓ | ✓ | ✓ |  |
| Run experiment | ✓ | ✓ | ✓ |  |
| Review finding | ✓ | ✓ | ✓ | ✓ |
| Generate report | ✓ | ✓ | ✓ |  |
| Run benchmark | ✓ | ✓ | ✓ |  |
| View system logs | ✓ |  |  |  |

## Acceptance Criteria

- unauthorized users receive access denied;
- role changes take effect without editing frontend code;
- project data is isolated by project membership;
- all privileged actions are auditable.

**Priority:** P0

---

# 11. Feature Module B — Research Project Workspace

## Objective

Cung cấp một workspace tập trung chứa toàn bộ research lifecycle.

## User Stories

**US-PROJ-01**  
As a researcher, I want to create a research project so that datasets, hypotheses, experiments and findings are organized together.

**US-PROJ-02**  
As a project manager, I want an overview of project progress so that I know the current research state.

## Functional Requirements

### FR-PROJ-01 — Create Project

Fields:

- project name;
- description;
- research domain;
- owner;
- optional objective;
- optional tags.

### FR-PROJ-02 — Project Overview

Overview shall show:

- active research question;
- current hypothesis;
- datasets;
- latest experiment;
- latest finding;
- loop status;
- unresolved warnings;
- report status.

### FR-PROJ-03 — Project State

Suggested states:

```text
Draft
Data Ready
Researching
Needs Review
Completed
Archived
```

## Acceptance Criteria

- project owner can create and edit metadata;
- project page loads key research state without opening multiple screens;
- archived projects become read-only by default.

**Priority:** P0

---

# 12. Feature Module C — Dataset Upload & Validation

## Objective

Cho phép user đưa structured dataset vào platform một cách an toàn.

## Supported Formats

P0:

- CSV;
- XLSX.

P1:

- JSON;
- TSV;
- Parquet.

## User Stories

**US-DATA-01**  
As a researcher, I want to upload my dataset so that the agent can analyze it.

**US-DATA-02**  
As a researcher, I want validation errors before analysis starts so that invalid input does not silently affect findings.

## Functional Requirements

### FR-DATA-01 — Upload

System shall:

1. accept supported file;
2. store immutable original;
3. calculate checksum;
4. create dataset entity;
5. create `v1` raw version;
6. start validation/profiling job.

### FR-DATA-02 — Validation

Validate:

- file readability;
- empty file;
- header/schema;
- duplicate column names;
- unsupported types;
- encoding;
- row/column count;
- file size limit.

### FR-DATA-03 — Error Handling

Upload failures must show actionable error message and must not create a usable dataset version.

## Acceptance Criteria

- original file remains immutable;
- validation result is visible;
- invalid file cannot be used by experiment planner;
- every uploaded dataset has unique ID/version.

**Priority:** P0

---

# 13. Feature Module D — Automatic Profiling & Data Card

## Objective

Tạo machine-readable và human-readable representation của dataset để agent không cần đưa toàn bộ raw data vào LLM context.

## User Stories

**US-PROFILE-01**  
As a researcher, I want to understand my dataset quickly without manually inspecting every column.

**US-PROFILE-02**  
As the agent, I need a compact Data Card so that I can plan experiments without loading the entire dataset into the prompt.

## Functional Requirements

### FR-PROFILE-01 — Profiling

Generate:

- row count;
- column count;
- inferred type;
- missing count/ratio;
- unique count;
- duplicate rows;
- numeric summary;
- categorical frequency summary;
- distribution hints;
- candidate outliers;
- example values;
- possible identifiers;
- possible target/feature hints;
- quality warnings.

### FR-PROFILE-02 — Data Card

Data Card shall include:

```text
Dataset Identity
Version
Schema
Variable Types
Quality Summary
Statistical Summary
Sample Values
Potential Relationships
Warnings
Known Domain Notes
```

### FR-PROFILE-03 — Agent Context

Planner receives Data Card and selected samples/statistics, not unrestricted full raw dataset text.

## Acceptance Criteria

- profiling runs after successful upload;
- Data Card references exact dataset version;
- Data Card is regenerated when version changes;
- researcher can inspect profiling result before experiment.

**Priority:** P0

---

# 14. Feature Module E — Data Quality, Cleaning & Versioning

## Objective

Hỗ trợ data preparation nhưng không tự biến anomaly thành data error.

## Issue Types

```text
Confirmed Data Issue
Potential Anomaly
Needs User Confirmation
Needs Domain Clarification
```

## User Stories

**US-CLEAN-01**  
As a researcher, I want the agent to identify possible data-quality issues so that I can review them before analysis.

**US-CLEAN-02**  
As a researcher, I want risky cleaning to require my approval so that valid scientific data is not silently changed.

## Functional Requirements

### FR-CLEAN-01 — Issue Detection

Each issue must store:

- issue type;
- affected columns/rows;
- severity;
- reason;
- evidence;
- recommended action;
- confidence.

### FR-CLEAN-02 — Cleaning Proposal

Proposal shall show:

- transformation;
- rationale;
- rows/columns affected;
- potential information loss;
- risk;
- reversibility.

### FR-CLEAN-03 — Approval

Actions:

```text
Approve
Reject
Modify
Ask Agent
```

### FR-CLEAN-04 — Version Creation

Approved transformation creates:

```text
Dataset vN
→ Transformation Record
→ Dataset vN+1
```

### FR-CLEAN-05 — Lineage

User shall be able to see dataset version lineage.

## Acceptance Criteria

- original version is never overwritten;
- risky transformation cannot execute without required approval;
- every version records parent version and transformations;
- experiments reference a specific dataset version.

**Priority:** P0

---

# 15. Feature Module F — Research Question & Research Context

## Objective

Cho agent đủ scientific/domain context trước experiment planning.

## User Stories

**US-RQ-01**  
As a researcher, I want to enter a research question so that the agent knows what evidence to seek.

**US-RQ-02**  
As a researcher, I want to provide variable/domain meaning so that the agent does not invent business/scientific semantics.

## Functional Requirements

### FR-RQ-01 — Research Question

Required:

- question text.

Optional:

- research goal;
- domain;
- expected variables;
- constraints;
- notes;
- prior assumptions.

### FR-RQ-02 — Context Clarification

If key variable meaning is ambiguous, agent may call `ask_user` before finalizing experiment plan.

### FR-RQ-03 — Multiple Questions

P1: one project may contain multiple research questions, but only one active loop per research question unless parallel runs are intentionally enabled.

## Acceptance Criteria

- experiment cannot start without active research question;
- context is versioned or timestamped;
- user can edit context with history retained.

**Priority:** P0

---

# 16. Feature Module G — Hypothesis Management

## Objective

Quản lý hypothesis như first-class product object.

## Hypothesis Fields

```text
Hypothesis ID
Statement
Null / Alternative Type
Origin
Research Question
Parent Finding
Status
Created By
Created At
Approval Status
Evidence Summary
Notes
```

## Origin Values

```text
Initial / Confirmatory
Post-hoc / Exploratory
User-defined
Agent-generated
```

## Status Values

```text
Proposed
Unverified
Supported
Rejected
Inconclusive
Superseded
Needs Review
```

## User Stories

**US-HYP-01**  
As a researcher, I want to define H0/H1 so that the initial experiment has a clear hypothesis.

**US-HYP-02**  
As a researcher, I want agent-generated hypotheses labeled post-hoc so that exploratory and initial hypotheses are not mixed.

**US-HYP-03**  
As a reviewer, I want to see which experiment supports or rejects a hypothesis.

## Functional Requirements

### FR-HYP-01 — Initial H0/H1

Researcher may manually define or request an AI draft.

AI-generated initial hypothesis requires researcher confirmation before becoming active.

### FR-HYP-02 — Hypothesis Origin

System must never silently label a post-result hypothesis as initial/confirmatory.

### FR-HYP-03 — Status Update

Hypothesis evaluation is updated from validated findings only.

### FR-HYP-04 — Parent Link

Post-hoc hypothesis must link to the finding that motivated it.

## Acceptance Criteria

- all hypotheses have explicit origin;
- agent-generated post-hoc hypothesis starts `Unverified`;
- hypothesis history is retained;
- a finding cannot silently overwrite hypothesis statement.

**Priority:** P0 for initial hypothesis; P1 for full lifecycle/refinement.

---

# 17. Feature Module H — Experiment Planner

## Objective

Chuyển hypothesis + Data Card + context thành executable scientific plan.

## Planner Inputs

```text
Research Question
Active Hypothesis
Data Card
Dataset Version
Domain Context
Previous Findings
Previous Experiments
Constraints
```

## Planner Output

```text
Experiment Objective
Variables
Candidate Methods
Assumptions to Check
Data Requirements
Proposed Steps
Expected Outputs
Possible Risks
Testing Family
Stopping / Success Conditions
```

## User Stories

**US-PLAN-01**  
As a researcher, I want the agent to explain the experiment plan before execution so that I understand what it intends to do.

## Functional Requirements

### FR-PLAN-01 — Plan Generation

Planner shall generate structured plan, not only free text.

### FR-PLAN-02 — Plan Revision

Plan may be revised after:

- failed assumption;
- execution error;
- user clarification;
- conflicting evidence;
- invalid dataset version.

### FR-PLAN-03 — Risk Flag

Planner must flag:

- ambiguous variable meaning;
- suspected leakage;
- insufficient sample;
- unsupported causal question;
- destructive preprocessing.

### FR-PLAN-04 — Parallel Plans Under Bounded Tied-Candidate Selection

When the Hypothesis Selection Gate (Module AD) activates bounded tied-candidate selection, Planner shall generate one independent Experiment Plan per selected candidate, each referencing its own hypothesis and its own immutable Research State snapshot. Two project-level configuration parameters govern this behavior: `tie_threshold` (score-closeness margin) and `max_parallel_candidates` (upper bound on simultaneously selected hypotheses); a further `max_total_concurrent_branches` bounds the combined total when hypothesis-level and method-level (Module K) branching are both active in the same iteration.

## Acceptance Criteria

- plan references exact hypothesis and dataset version;
- plan lists candidate methods;
- user can inspect plan before execution;
- reason for re-plan is logged;
- when multiple candidates are tied-selected, each resulting plan is independently inspectable and references its own hypothesis and Research State snapshot;
- combined hypothesis-level x method-level branching never exceeds `max_total_concurrent_branches`.

**Priority:** P0

---

# 18. Feature Module I — Candidate Method Generation & Selection

## Objective

Cho agent lựa chọn statistical/analytical method phù hợp thay vì hard-code một test duy nhất.

## Initial Supported Methods

P0 / Must for final capstone (BR-31 Statistical Analysis is Must in BRD MoSCoW and explicitly lists every method below):

- descriptive statistics;
- Pearson correlation;
- Spearman correlation;
- independent t-test;
- paired t-test;
- Mann–Whitney U;
- chi-square test;
- one-way ANOVA;
- Kruskal–Wallis;
- linear regression;
- logistic regression;
- interaction analysis;
- basic time-series analysis.

P1 (extension beyond BR-31 — not required for Must compliance):

- simple repeated-measure support;
- selected ML prediction workflows.

## User Stories

**US-METHOD-01**  
As a researcher, I want to know why a method was selected so that I can review its scientific appropriateness.

## Functional Requirements

### FR-METHOD-01 — Candidate Generation

Agent shall generate one or more candidates based on:

- research goal;
- variable types;
- sample structure;
- distribution;
- expected relationship;
- prior findings.

### FR-METHOD-02 — Assumption Definition

Each candidate shall declare required assumptions.

### FR-METHOD-03 — Selection

System shall store:

- selected method;
- selection reason;
- rejected alternatives;
- failed/passed assumptions.

### FR-METHOD-04 — Alternative Method

If assumptions fail, agent should:

1. choose valid alternative; or
2. ask user; or
3. mark experiment not currently feasible.

## Acceptance Criteria

- selected method is explainable;
- assumption failures are visible;
- method cannot silently switch without trace;
- unsupported method must not be executed as if supported.

**Priority:** P0

---

# 19. Feature Module J — Assumption Checking

## Objective

Kiểm tra điều kiện sử dụng method trước và sau execution khi cần.

## Example Checks

- variable type;
- independence;
- normality where relevant;
- linearity;
- homoscedasticity;
- expected cell count;
- sample size;
- influential outliers;
- multicollinearity where relevant;
- model-specific diagnostics.

## Functional Requirements

### FR-ASSUME-01

Each assumption check produces:

```text
Assumption
Status: Pass / Fail / Warning / Not Applicable
Evidence
Method Used
Impact
Recommended Action
```

### FR-ASSUME-02

Warning/failure must propagate into experiment plan and finding interpretation.

## Acceptance Criteria

- checks are stored with experiment;
- finding cannot hide failed assumption;
- alternative method may be triggered automatically if safe.

**Priority:** P0

---

# 20. Feature Module K — Limited Experiment Branching

## Objective

Cho phép nhiều candidate analyses khi có scientific value mà không triển khai full tree-search system.

## Example

```text
Parent Plan
├── E1A: Pearson
├── E1B: Spearman
└── E1C: Linear Regression
```

## Functional Requirements

### FR-BRANCH-01

Planner may create max configurable branch count.

### FR-BRANCH-02

Each branch has separate:

- method;
- assumptions;
- execution;
- result;
- validation.

### FR-BRANCH-03

Branch comparison must not automatically choose the most statistically significant result.

## Acceptance Criteria

- branches are visible as alternatives;
- evidence from all executed branches is retained;
- agent explains why one result is more appropriate/reliable.

**Priority:** P1 / Must for final capstone (BR-21 is Must in BRD MoSCoW; kept as P1 here because it depends on Module I/J being in place first, not because it is optional for final submission)

---

# 21. Feature Module L — Secure Experiment Execution

## Objective

Thực thi agent-generated code/tools an toàn.

## Execution Flow

```text
Plan
↓
Tool Router
↓
Sandbox
↓
Execute
↓
Capture stdout/result/error
↓
Observer
↓
Validator
```

## Tool Categories

```text
inspect_schema
profile_dataset
run_python
run_sql
clean_dataset
statistical_test
create_chart
generate_table
generate_report
ask_user
```

## Sandbox Requirements

- project/session isolation;
- no unrestricted host filesystem;
- network disabled by default;
- CPU limit;
- RAM limit;
- execution timeout;
- library whitelist;
- temporary working directory;
- output size limit;
- concurrent-execution quota per project, sized to accommodate parallel branches from bounded tied-candidate selection (Module AD) and limited experiment branching (Module K) without exceeding `max_total_concurrent_branches`.

## User Stories

**US-EXEC-01**  
As a researcher, I want experiments to execute without risking my system or unrelated project data.

## Functional Requirements

### FR-EXEC-01 — Execution Record

Every execution stores:

- execution ID;
- experiment ID;
- tool;
- code/query;
- input references;
- output;
- error;
- latency;
- resource usage;
- retry number.

### FR-EXEC-02 — Retry / Re-plan

On error:

```text
Observe
→ Diagnose
→ Retry same approach OR Re-plan
```

Retry count is limited.

### FR-EXEC-03 — Cancellation

User can cancel long-running experiment.

## Acceptance Criteria

- code cannot access other project data;
- timeout terminates process;
- every retry is traceable;
- failed execution does not create validated finding.

**Priority:** P0

---

# 22. Feature Module M — Statistical & Scientific Validation

## Objective

Không cho raw output đi thẳng thành scientific conclusion.

## Validation Pipeline

```text
Raw Result
↓
Execution Success
↓
Assumption Validation
↓
Multiple-Testing Check
↓
Effect Size
↓
Confidence Interval
↓
Leakage Check
↓
Stability / Replication Check
↓
Interpretation Check
↓
Evidence Quality
↓
Finding Candidate
```

## Functional Requirements

### FR-VALID-01 — Result Validation

Validate numerical/statistical output consistency.

### FR-VALID-02 — Unsupported Interpretation Guard

Agent must reject or soften statements not supported by result.

### FR-VALID-03 — Causal Language Guard

If design is observational/non-causal, output must use association language.

### FR-VALID-04 — Validation Status

```text
Passed
Passed with Warnings
Needs Review
Failed
```

## Acceptance Criteria

- failed validation blocks official finding;
- warning appears in finding/report;
- causal overclaim is prevented or flagged;
- validation record remains inspectable.

**Priority:** P0/P1

---

# 23. Feature Module N — Multiple-Testing Control

## Objective

Giảm false-positive risk trong iterative/multi-test workflow.

## Functional Requirements

### FR-MTEST-01 — Testing Family Tracking

Experiments may be grouped into a testing family. Experiments produced by bounded tied-candidate selection (Module AD) within the same iteration shall be assigned the same testing-family ID, so correction (Holm/FDR) is applied across the tied set rather than per branch independently.

### FR-MTEST-02 — Correction

When applicable, support:

- Bonferroni;
- Holm;
- Benjamini-Hochberg / FDR.

### FR-MTEST-03 — Values

Store:

- raw p-value;
- adjusted p-value;
- correction method;
- family size;
- rationale.

## Acceptance Criteria

- system does not silently apply correction without showing method;
- system does not claim correction is necessary when not applicable;
- report distinguishes raw/adjusted result.

**Priority:** P1 / Must for final capstone (BR-49 Multiple-Testing Control is Must in BRD MoSCoW)

---

# 24. Feature Module O — Effect Size, Confidence Interval & Uncertainty

## Objective

Không phụ thuộc duy nhất vào p-value.

## Functional Requirements

### FR-EFFECT-01

When supported, output:

- point estimate;
- effect size;
- confidence interval;
- significance/evidence measure.

### FR-UNCERT-01

Finding may contain:

```text
Confidence: Low / Medium / High
Reasons:
- small sample
- wide CI
- unstable result
- assumption warning
- conflicting evidence
```

This confidence label is explanatory metadata and does not replace formal statistical evidence.

## Acceptance Criteria

- finding UI shows practical magnitude when available;
- p-value alone cannot be used as sole explanation for strong finding;
- uncertainty reasons are inspectable.

**Priority:** P1 / Must for final capstone (BR-50 Effect Size & Confidence Interval and BR-54 Confidence & Uncertainty Recording are Must in BRD MoSCoW)

---

# 25. Feature Module P — Data Leakage Guard

## Objective

Ngăn contamination trong predictive/ML workflows.

## Functional Requirements

### FR-LEAK-01 — Split Definition

Support:

```text
Train
Validation
Test
```

where applicable.

### FR-LEAK-02 — Fit Scope

Preprocessing/feature selection/tuning must not fit on held-out test data unless research design explicitly allows it.

### FR-LEAK-03 — Leakage Warning

Agent flags suspicious target leakage or inappropriate data access.

## Acceptance Criteria

- split strategy is stored in experiment;
- official predictive evaluation identifies held-out data;
- leakage warning blocks or requires review for high-risk case.

**Priority:** P1

---

# 26. Feature Module Q — Finding Management

## Objective

Biến validated experiment results thành first-class research findings.

## Finding Fields

```text
Finding ID
Statement
Research Question
Hypothesis
Experiment
Dataset Version
Evidence
Statistical Result
Effect Size
Confidence Interval
Uncertainty
Causality Level
Status
Created By
Created At
```

## Finding Status

```text
Preliminary
Validated
Inconclusive
Rejected
Needs Review
Conflicting Evidence
Invalidated
```

## User Stories

**US-FIND-01**  
As a researcher, I want every finding to show its evidence so that I can verify it.

## Functional Requirements

### FR-FIND-01 — Candidate Finding

Only generated after experiment output exists.

### FR-FIND-02 — Validated Finding

Requires:

- valid experiment;
- known dataset version;
- method record;
- assumption record;
- execution trace;
- supporting evidence.

### FR-FIND-03 — Evidence View

User can open finding and navigate to all supporting artifacts.

## Acceptance Criteria

- finding without evidence cannot be marked validated;
- finding preserves warnings;
- invalidated finding is not used as official final finding.

**Priority:** P0

---

# 27. Feature Module R — Hypothesis Refinement

## Objective

Cho agent tạo research continuation dựa trên evidence nhưng vẫn phân biệt exploratory hypothesis.

## Flow

```text
Validated Finding F1
↓
Agent proposes H2
↓
H2 = Post-hoc / Agent-generated / Unverified
↓
Researcher Review when required
↓
Experiment Plan E2
```

## Functional Requirements

### FR-REFINE-01 — Generate New Hypothesis

New hypothesis must include:

- statement;
- rationale;
- parent finding;
- proposed variables;
- why it is testable;
- suggested experiment direction.

### FR-REFINE-02 — No Circular Claim

Agent may not treat its own generated H2 as evidence.

### FR-REFINE-03 — Researcher Control

Configurable policy:

```text
Auto-continue low-risk
Require approval for every new hypothesis
Require approval only for high-impact/ambiguous hypothesis
```

For capstone MVP, default should favor explicit researcher review.

## Acceptance Criteria

- H2 cannot exist without origin;
- H2 links to F1;
- H2 remains unverified until E2 validates it;
- user can reject hypothesis and stop branch.

**Priority:** P1 / Must for final capstone (BR-28 Hypothesis Refinement is Must in BRD MoSCoW)

---

# 28. Feature Module S — Experiment Dependency Graph

## Objective

Biểu diễn full research lineage.

## Example

```text
RQ-01
↓
H1
↓
E1
↓
F1
↓
H2
↓
E2
↓
F2
```

## Functional Requirements

### FR-DEP-01

Graph nodes:

- research question;
- hypothesis;
- experiment;
- finding;
- dataset version where useful.

### FR-DEP-02

Graph edges include:

```text
tests
produces
motivates
depends_on
uses_dataset
supersedes
contradicts
co_selected_with
```

`co_selected_with` links sibling hypothesis branches chosen together by a single bounded tied-candidate selection decision (Module AD); it is distinct from the other edge types, which represent sequential/causal research relationships.

### FR-DEP-03 — Downstream Invalidation

If upstream evidence is invalidated/recomputed:

```text
Upstream artifact
↓
Affected descendants
↓
Needs Re-validation
```

## Acceptance Criteria

- user can trace H2 back to F1/E1;
- affected downstream artifacts are identified;
- invalidation never silently deletes history.

**Priority:** P1

---

# 29. Feature Module T — Conflicting Evidence

## Objective

Ngăn cherry-picking.

## Functional Requirements

### FR-CONFLICT-01

When experiments produce incompatible evidence, system shall preserve all results. This also covers the case where sibling branches from bounded tied-candidate selection (Module AD) each produce a validated finding: all such findings must be retained and shown, and this multi-finding case must be distinguished from `Conflicting Evidence` (which applies to incompatible evidence about the same hypothesis).

### FR-CONFLICT-02

Hypothesis/finding may receive `Conflicting Evidence`.

### FR-CONFLICT-03

Agent may recommend:

- replication;
- subgroup analysis;
- alternative method;
- data-quality investigation;
- researcher review.

## Acceptance Criteria

- contradicting result remains visible;
- final report cannot hide known high-impact conflict;
- resolution action is traceable.

**Priority:** P1

---

# 30. Feature Module U — Stopping Criteria

## Objective

Ngăn infinite experiment loop và xác định khi nào research question đã đủ evidence.

## Default Criteria

Any configured combination of:

- research question sufficiently answered;
- no meaningful/testable new hypothesis;
- evidence converged;
- max experiment count reached;
- max agent steps reached;
- time budget reached;
- cost/token budget reached;
- repeated inconclusive results;
- researcher stops manually.

## Functional Requirements

### FR-STOP-01

After each validated finding, agent evaluates stopping criteria. When bounded tied-candidate selection (Module AD) runs K branches in parallel, experiment/time/cost budget consumption is evaluated cumulatively across all K branches in that iteration, not per branch.

### FR-STOP-02

Agent explains:

```text
Continue / Stop
Reason
Criteria Triggered
Suggested Next Step
```

### FR-STOP-03

Human can override agent stop/continue decision within permission policy.

## Acceptance Criteria

- loop has bounded execution;
- stop reason is stored;
- manual stop preserves current artifacts.

**Priority:** P1 / Must for final capstone (BR-30 Stopping Criteria is Must in BRD MoSCoW)

---

# 31. Feature Module V — Visualization & Figure Review

## Objective

Tạo figure/table hỗ trợ scientific finding, không chỉ decorative charts.

## Functional Requirements

### FR-VIZ-01 — Generate Chart

Chart must reference source experiment/finding.

### FR-VIZ-02 — Figure Metadata

Store:

- chart type;
- variables;
- filters;
- dataset version;
- code;
- caption;
- source finding.

### FR-VIZ-03 — Figure Review

P1/P2 check:

- chart type appropriateness;
- axes labels;
- units;
- legend;
- misleading scale;
- caption consistency;
- whether figure supports stated finding.

## Acceptance Criteria

- chart can be regenerated from stored metadata;
- figure has source linkage;
- misleading or invalid figure receives warning.

**Priority:** P1 / Must for final capstone (BR-32 Visualization and BR-38 Research Figure/Table Output are Must in BRD MoSCoW); advanced visual/VLM reviewer remains P2

---

# 32. Feature Module W — Research Outputs & Report

## Objective

Tổng hợp only validated/reviewed research artifacts.

## Report Sections

Suggested:

```text
Research Question
Hypotheses
Dataset & Data Preparation
Methodology
Experiments
Statistical Results
Research Findings
Figures / Tables
Conflicting Evidence
Limitations
Conclusion
Reproducibility Information
```

## Functional Requirements

### FR-REPORT-01

Only validated findings are included by default.

### FR-REPORT-02

Preliminary/inconclusive/conflicting result can be included only with explicit label.

### FR-REPORT-03

Methodology summary must reference actual executed workflow, not invented text.

### FR-REPORT-04

Report content must link back to provenance where UI supports it.

## Acceptance Criteria

- report never silently converts exploratory hypothesis into initial hypothesis;
- known limitations/warnings are preserved;
- report can identify dataset version/method behind finding.

**Priority:** P1 / Must for final capstone (BR-41 Research Report Generation and BR-42 Finding Validation are Must in BRD MoSCoW)

---

# 33. Feature Module X — Provenance & Evidence

## Objective

Cho researcher verify every important analytical claim.

## Provenance Chain

```text
Claim / Finding
↓
Statistical Result
↓
Experiment
↓
Execution
↓
Code / Query
↓
Dataset Version
↓
Dataset Lineage
```

## Functional Requirements

### FR-PROV-01

Each validated finding stores provenance IDs.

### FR-PROV-02

UI supports "View Evidence".

### FR-PROV-03

Evidence cannot be overwritten; new execution creates new record.

## Acceptance Criteria

- 100% validated findings have provenance;
- broken provenance blocks final validation;
- user can navigate from finding to raw output.

**Priority:** P0

---

# 34. Feature Module Y — Execution Trace

## Objective

Hiển thị agent đã làm gì và tại sao.

## Trace Item

```text
Step Number
Timestamp
Agent Stage
Tool
Input References
Plan / Reason Summary
Code / Query
Raw Output
Error
Retry
Latency
Token Usage if applicable
```

## Functional Requirements

### FR-TRACE-01

Trace is append-only for completed execution record.

### FR-TRACE-02

Sensitive/internal secrets must not be exposed to normal user.

### FR-TRACE-03

Trace UI supports filtering by experiment/run.

## Acceptance Criteria

- every experiment has visible trace;
- retries appear as separate steps;
- trace distinguishes plan, tool action and validation.

**Priority:** P0

---

# 35. Feature Module Z — Reproducibility Snapshot

## Objective

Đảm bảo official experiment có đủ context để reproduce.

## Snapshot Fields

```text
Dataset Version
Dataset Checksum
Data Split
Code / Query
Parameters
Random Seed
Selected Method
Model Name / Version
Agent Configuration
Prompt / Template Version if applicable
Tool Versions
Library Versions
Runtime / Environment
Execution Timestamp
Raw Output References
Figure/Table References
```

## Functional Requirements

### FR-REPRO-01

Snapshot created when experiment is marked official/validated.

### FR-REPRO-02

Snapshot is immutable; rerun creates new run/snapshot.

### FR-REPRO-03

Reproduction attempt can reference prior snapshot.

## Acceptance Criteria

- validated official experiment has snapshot;
- changing code/config creates new run;
- environment metadata is visible to authorized users.

**Priority:** P1 / Must for final capstone (BR-55 Reproducibility Snapshot is Must in BRD MoSCoW)

---

# 36. Feature Module AA — Evaluation Center

## Objective

Đánh giá agent architecture có hệ thống cho capstone research questions.

## Benchmark Task Structure

```text
Task ID
Dataset
Research Question
Hypothesis
Expected Method / Allowed Methods
Expected Result / Ground Truth
Required Skills
Scoring Function
Difficulty
Tags
```

## User Stories

**US-EVAL-01**  
As a researcher, I want to run benchmark tasks repeatedly so that I can measure agent performance objectively.

**US-EVAL-02**  
As a project team, we want ablation comparisons so that we can measure which architecture components matter.

## Functional Requirements

### FR-EVAL-01 — Benchmark Run

Run selected task/configuration N times.

### FR-EVAL-02 — Metrics

Minimum metrics:

- task success;
- result correctness;
- method-selection accuracy;
- assumption-check accuracy;
- experiment count;
- retry count;
- latency;
- token usage;
- cost;
- human intervention;
- provenance coverage;
- unsupported claim rate;
- reproducibility coverage.

### FR-EVAL-03 — Skill-Level Evaluation

Suggested skills:

```text
dataset_understanding
method_selection
assumption_checking
execution
result_validation
hypothesis_refinement
evidence_grounding
```

### FR-EVAL-04 — Ablation

Configurations may include:

```text
Full Agent
No Planner
No Profiling
No Assumption Checking
No Retry
No Validator
No Hypothesis Refinement
No Tied-Candidate Selection (single-select baseline)
Single-Pass Agent
Text-to-Code Baseline
```

### FR-EVAL-05 — Aggregation

Show:

- mean;
- standard deviation where meaningful;
- success rate;
- per-task;
- per-skill;
- per-configuration.

## Acceptance Criteria

- benchmark run is reproducible/configurable;
- metrics retain raw run references;
- comparison does not mix configurations silently.

**Priority:** P1 / Must for final capstone (BR-43 Evaluation Framework and BR-63 Decision Gate Evaluation are Must in BRD MoSCoW)

---

# 37. Feature Module AB — Admin, Telemetry & Cost

## Objective

Cho admin/team theo dõi operational behavior.

## Functional Requirements

### FR-ADMIN-01

Admin can configure available models.

### FR-ADMIN-02

System records:

- agent runs;
- failed runs;
- latency;
- token usage;
- cost estimates;
- sandbox failures;
- tool failures.

### FR-ADMIN-03

Logs must not expose sensitive dataset contents unnecessarily.

## Acceptance Criteria

- admin can identify failing component;
- usage metrics can be filtered by project/model/date;
- project isolation applies to user-facing logs.

**Priority:** P1

---


# 37.1. Feature Module AC — Research State & Candidate Hypothesis Generation

## Objective

Tạo một structured Research State làm source-of-context chính thức cho mỗi research iteration và sinh candidate hypotheses/research directions có thể đánh giá được.

## Research State Fields

Tối thiểu:

```text
research_question
current_hypothesis
previous_hypotheses
experiment_history
validated_findings
conflicting_evidence
uncertainty_warnings
dataset_version
remaining_experiment_budget
remaining_cost_budget
iteration_number
```

## Candidate Hypothesis Fields

```text
candidate_id
statement
rationale
parent_evidence
testability
relevant_variables
risk_notes
uncertainty_notes
origin
status
```

## Functional Requirements

### FR-STATE-01 — Build Research State

System shall build a versioned Research State before each research iteration.

### FR-STATE-02 — State Versioning

Any meaningful update to findings, hypothesis status, dataset version or evidence must create/update the active Research State version.

### FR-STATE-03 — Candidate Generation

Agent shall be able to generate one or more candidate hypotheses/research directions from the active Research State.

### FR-STATE-04 — Candidate Testability

Candidate that cannot be operationalized/tested using available data/tools must be marked unsupported, deferred or require clarification.

### FR-STATE-05 — Initial vs Post-hoc Origin

Candidate generated after observing experiment findings must be marked `Post-hoc / Exploratory` by default.

## Acceptance Criteria

- each iteration has an inspectable Research State reference;
- candidates show parent evidence and rationale;
- generated candidates cannot silently become active hypotheses;
- candidate origin and testability are visible;
- Research State references exact dataset version.

**Priority:** P1 / Must for final capstone

---

# 37.2. Feature Module AD — Structured Hypothesis Selection Gate

## Objective

Rank/select/reject/escalate candidate hypotheses or research directions before deep reasoning and experiment planning.

## Decision Outcomes

```text
SELECT
REJECT
ESCALATE_TO_RESEARCHER
NO_SUITABLE_CANDIDATE
```

A selection decision shall include:

```text
decision_id
research_state_version
candidate_scores_or_probabilities
selected_candidate
decision_outcome
confidence
uncertainty
reason_codes
provider
provider_model_version
configuration_version
timestamp
downstream_action
```

## Functional Requirements

### FR-HGATE-01 — Candidate Evaluation

Gate shall receive the active Research State plus candidate hypotheses/directions.

### FR-HGATE-02 — Rank / Select / Reject

Gate shall return a bounded decision and preserve the evaluated candidate set.

### FR-HGATE-03 — Confidence

Decision shall include confidence/uncertainty metadata when supported.

### FR-HGATE-04 — Human Escalation

If confidence is below configured threshold, evidence conflict is severe or risk is high, system shall create a researcher review task.

### FR-HGATE-05 — Provider Abstraction

Product shall use a `DecisionProvider` abstraction rather than bind business behavior to one vendor.

Conceptual interface:

```text
DecisionProvider
├── TypeSafe / Jev Provider       # candidate implementation
└── Structured LLM Provider       # fallback / baseline
```

### FR-HGATE-06 — No Silent Activation

A candidate may only become the active hypothesis/research direction after a valid selection decision or explicit researcher choice.

### FR-HGATE-07 — Bounded Tied-Candidate Selection

If the score gap between top-ranked candidates falls below a configured `tie_threshold`, Gate shall select up to `max_parallel_candidates` candidates instead of exactly one. Gate output shall separate two values: a numeric, comparable decision score (used for tie detection) and the categorical confidence label (Low/Medium/High, per the Effect Size & Uncertainty module) used for human-facing explanation and escalation — the two are not interchangeable. Calibration quality of the numeric decision score shall be covered by Module AG's gate-evaluation metrics. When triggered, the decision record shall additionally store the `tie_threshold` used and the full list of tied candidates.

## Acceptance Criteria

- candidate set and selected outcome are inspectable;
- low-confidence decision can be escalated;
- provider can be switched without changing research-domain behavior;
- decision record links to the exact Research State version;
- LLM free-form text alone is not treated as the structured selection record;
- bounded tied-candidate selection never exceeds `max_parallel_candidates`;
- when tied-candidate selection is used, the decision record includes the tie threshold and the tied-candidate list.

**Priority:** P1 / Must for final capstone

---

# 37.3. Feature Module AE — Evidence Sufficiency Gate

## Objective

Quyết định một validated experiment result đã có đủ evidence để tạo official finding hay cần thêm scientific work.

## Inputs

```text
active_research_state
hypothesis
experiment_result
assumption_results
effect_size
confidence_interval
multiple_testing_status
leakage_status
diagnostics
conflicting_evidence
replication_history
```

## Required Outcomes

```text
ENOUGH_EVIDENCE
NEED_MORE_EVIDENCE
TRY_ALTERNATIVE_METHOD
REPLICATE
NEED_HUMAN_REVIEW
INCONCLUSIVE
```

## Functional Requirements

### FR-EGATE-01 — Gate After Deterministic Validation

Evidence gate shall run only after deterministic scientific validation has produced the required facts/checks.

### FR-EGATE-02 — Structured Decision

Gate shall produce one required outcome plus confidence/uncertainty and reason codes.

### FR-EGATE-03 — Finding Protection

`ENOUGH_EVIDENCE` is the only automatic gate outcome that may proceed directly to validated finding generation.

### FR-EGATE-04 — Inconclusive Is Valid

`INCONCLUSIVE` must be treated as a legitimate research outcome and must not trigger forced significance-seeking.

### FR-EGATE-05 — No Fact Generation

Gate may evaluate the structured scientific evidence but must not fabricate statistical values or replace deterministic validation.

## Acceptance Criteria

- every completed validated experiment has an explicit evidence-sufficiency decision before official finding;
- non-ENOUGH outcomes do not silently become findings;
- `INCONCLUSIVE` can terminate or continue according to stopping policy;
- decision links to validation outputs and Research State.

**Priority:** P1 / Must for final capstone

---

# 37.4. Feature Module AF — Scientific Refinement & Confidence-Based Escalation

## Objective

Xử lý các trường hợp experiment chạy đúng nhưng evidence chưa đủ, và phân biệt rõ chúng với technical retry.

## Refinement Routing

```text
NEED_MORE_EVIDENCE
        ↓
LLM Re-plan
        ↓
Design Additional Experiment

TRY_ALTERNATIVE_METHOD
        ↓
LLM Re-plan
        ↓
Select Alternative Valid Method

REPLICATE
        ↓
Create Replication Experiment

NEED_HUMAN_REVIEW
        ↓
Researcher Review Task
```

## Functional Requirements

### FR-REFLOOP-01 — Scientific Refinement

System shall create a new/revised experiment plan when evidence decision requests more scientific work.

### FR-REFLOOP-02 — Technical vs Scientific Classification

Every retry/re-plan event shall be classified at minimum as:

```text
TECHNICAL_RETRY
SCIENTIFIC_REFINEMENT
```

### FR-REFLOOP-03 — Budget Guard

Scientific refinement must respect configured experiment, time and cost budgets.

### FR-REFLOOP-04 — Escalation Policy

Escalation rules may use:

- confidence threshold;
- methodological risk;
- conflicting evidence;
- ambiguity severity;
- experiment budget;
- explicit gate outcome.

### FR-REFLOOP-05 — Researcher Actions

Researcher can:

```text
Approve
Modify
Reject
Stop Research
Request Alternative
```

## Acceptance Criteria

- scientific refinement is visible separately from technical retry;
- refinement preserves parent hypothesis/experiment/evidence links;
- low-confidence or high-risk decisions can be routed to researcher;
- loop stops when budget or stopping criteria require it.

**Priority:** P1 / Must for final capstone

---

# 37.5. Feature Module AG — Decision Audit, Configuration & Gate Evaluation

## Objective

Lưu lịch sử structured decisions, cho phép review/debug và đánh giá decision gates như một thành phần riêng của architecture.

## Decision Record

```text
decision_id
decision_type
research_state_version
input_references
candidate_choices
outcome
confidence
uncertainty
reason_codes
provider
model_version
configuration_version
latency
estimated_cost
timestamp
downstream_action
human_override
override_reason
tie_threshold_used
tied_candidates
```

## Functional Requirements

### FR-DEC-01 — Audit History

All hypothesis-selection and evidence-sufficiency decisions must be persisted and inspectable.

### FR-DEC-02 — Configuration Version

Decision record shall identify provider/model/configuration used for reproducibility and evaluation.

### FR-DEC-03 — Human Override

When researcher overrides a decision, system shall retain both original decision and override.

### FR-DEC-04 — Gate Metrics

Evaluation center shall support:

- decision accuracy/correctness;
- hypothesis-selection quality;
- false acceptance of insufficient evidence;
- unnecessary continuation rate;
- human escalation rate;
- confidence/calibration quality;
- latency;
- cost.

### FR-DEC-05 — Baseline Comparison

When benchmark labels/rubrics support it, evaluation shall compare:

```text
Structured Decision Gate
vs
LLM-only Decision Baseline
```

## Acceptance Criteria

- decision history is filterable by type/provider/outcome;
- benchmark run can collect gate-specific metrics;
- decision-provider changes remain reproducible through configuration versioning;
- human override is auditable.

**Priority:** P1 / Must for final capstone

---

# 37.6. Feature Module AH — Ideation Quality & Manuscript Reporting

## Objective

Nâng chất lượng ideation trước Hypothesis Selection Gate (Module AD) và cung cấp bản thảo nghiên cứu có thể review từ validated findings, mà không đưa vào bất kỳ cơ chế tree-search/branching nào (xem Non-Goals, mục 4).

## Functional Requirements

### FR-IDEA-01 — Idea Record

Mỗi candidate hypothesis phải có idea record gồm tối thiểu: statement, experiment đề xuất, context liên quan, risk notes, trước khi được đưa vào Module AD.

### FR-IDEA-02 — Reflection Round

Candidate hypothesis phải qua ít nhất một reflection round (agent tự rà lại statement/risk/testability) trước khi vào Hypothesis Selection Gate.

### FR-IDEA-03 — Novelty Assessment (tham khảo)

Hệ thống nên đánh giá mức độ mới của idea dựa trên nguồn literature/context do researcher cung cấp, ở mức tham khảo — không bảo đảm novelty. Khi không có nguồn, idea được ghi nhận trạng thái "chưa đánh giá" thay vì bị chặn hoặc suy diễn.

### FR-MANU-01 — Figure Aggregation & Visual Feedback

Hệ thống nên gom các figure sinh ra từ các candidate method/thử nghiệm đã chạy cho một hypothesis (Module K) và kiểm tra bằng visual reviewer về độ rõ, khớp caption và trùng lặp; đây là phần mở rộng của figure review ở Module V, không tạo cấu trúc node/cây riêng.

### FR-MANU-02 — Manuscript Draft Generation

Hệ thống nên tạo bản thảo nghiên cứu (manuscript draft) từ validated findings, với số liệu lấy trực tiếp từ experiment log và trích dẫn được xác minh tồn tại. Nội dung do AI tạo phải được ghi rõ là AI-generated. Đây chỉ là bản nháp — hệ thống không tự nộp hoặc xuất bản (Non-Goals, mục 4).

### FR-MANU-03 — Automated Manuscript Review

Hệ thống nên review bản thảo theo rubric (soundness, novelty, clarity) và kiểm tra chất lượng: placeholder còn sót, hình thiếu, trích dẫn chưa xác minh, số liệu không khớp experiment log.

### FR-MANU-04 — Human Approval Gate

Bản thảo phải được researcher phê duyệt trước khi dùng bên ngoài hệ thống; hệ thống không được tự động coi bản thảo là final hoặc gửi đi thay researcher.

## Acceptance Criteria

- candidate hypothesis có idea record và ít nhất một reflection round trước Module AD;
- khi bật, novelty assessment hiển thị nguồn tham khảo hoặc trạng thái "chưa đánh giá";
- figure trong bản thảo (nếu có) truy được về experiment log tương ứng;
- bản thảo (nếu tạo) có số liệu truy được về log, trích dẫn xác minh, kết quả automated review, và trạng thái phê duyệt của researcher trước khi export/chia sẻ.

**Priority:** P1 / Must for final capstone (FR-IDEA-01, FR-IDEA-02 — tương ứng BR-64, Must trong BRD); Should cho phần còn lại (FR-IDEA-03, FR-MANU-01→04 — tương ứng BR-65/73/74/75, Should trong BRD) — có thể defer nếu ảnh hưởng core loop.

---

# 38. Agent Runtime Product Behavior

High-level agent state machine:

```text
IDLE
↓
BUILD_RESEARCH_STATE
↓
GENERATE_CANDIDATES
↓
HYPOTHESIS_GATE
├── Escalate → WAIT_HUMAN
├── No Suitable Candidate → ASK_USER / STOP
└── Selected
      ↓
DEEP_REASON
↓
PLAN
↓
CHECK_ASSUMPTIONS
↓
SELECT_METHOD
↓
EXECUTE
↓
OBSERVE
├── Error → TECHNICAL_RETRY / REPLAN
└── Success
      ↓
DETERMINISTIC_VALIDATE
├── Invalid / Recoverable → REPLAN
├── Invalid / Not Recoverable → INCONCLUSIVE
└── Valid
      ↓
EVIDENCE_GATE
├── ENOUGH_EVIDENCE → GENERATE_FINDING
├── NEED_MORE_EVIDENCE → SCIENTIFIC_REFINEMENT
├── TRY_ALTERNATIVE_METHOD → SCIENTIFIC_REFINEMENT
├── REPLICATE → SCIENTIFIC_REFINEMENT
├── NEED_HUMAN_REVIEW → WAIT_HUMAN
└── INCONCLUSIVE → RECORD_OUTCOME
      ↓
UPDATE_RESEARCH_STATE
      ↓
EVALUATE_STOPPING
├── Continue → GENERATE_CANDIDATES
└── Stop → FINALIZE
```

## Agent Responsibility Model

```text
LLM / Generative Reasoner
= generate + reason + plan + interpret + refine

Analytical / Statistical Tools
= calculate + execute + deterministic scientific checks

Structured Decision Gate
= select + verify + route + confidence-based escalation
```

## Agent Rules

1. Never claim access to data/tool result that was not actually available.
2. Never mark hypothesis supported from planning/reasoning alone.
3. Never silently change dataset version.
4. Never hide failed assumptions.
5. Never select the "best" branch solely because p-value is lowest.
6. Never state causal conclusion without supported design.
7. Ask user when domain ambiguity materially changes interpretation.
8. Preserve conflicting evidence.
9. Respect step/time/cost limits.
10. Store reason summary for method selection/re-plan.
11. Never treat decision-model confidence as scientific evidence.
12. Never allow a candidate hypothesis to become active without a selection record or explicit researcher choice.
13. Never create an official finding before evidence-sufficiency decision.
14. Keep technical retry and scientific refinement as separate trace categories.
15. Preserve all structured decision records and human overrides.
16. If a structured decision provider is unavailable, apply configured fallback or require human review; do not silently skip the gate.

---

# 39. Human-in-the-Loop Decision Policy

## Mandatory Review

- destructive/risky cleaning;
- unresolved variable semantics;
- agent-generated initial hypothesis before activation;
- high-impact post-hoc hypothesis if configured;
- severe assumption violation;
- potential causal interpretation;
- conflicting evidence before final conclusion;
- downstream invalidation affecting report;
- explicit publication/final report approval;
- hypothesis-selection gate below configured confidence threshold;
- evidence gate below configured confidence threshold;
- `NEED_HUMAN_REVIEW` outcome;
- provider disagreement when configured as a high-risk policy;
- sibling branches from bounded tied-candidate selection produce conflicting Evidence Sufficiency outcomes (e.g. one branch `ENOUGH_EVIDENCE` while a sibling is `INCONCLUSIVE` or `NEED_HUMAN_REVIEW`).

## Optional Auto-Continue

Low-risk cases may continue automatically:

- profiling;
- descriptive stats;
- safe schema inspection;
- read-only diagnostics;
- retry of syntax/runtime error within limit;
- high-confidence structured decision when policy allows auto-continue and no high-risk flag exists.

---

# 40. Product State Models

## 40.1. Dataset

```text
Uploaded
→ Validating
→ Valid
→ Profiled
→ Ready
→ Superseded
```

Failure:

```text
Uploaded
→ Validation Failed
```

---

## 40.2. Experiment

```text
Draft
→ Planned
→ Ready
→ Running
→ Validating
→ Completed
```

Alternative outcomes:

```text
Failed
Cancelled
Needs Review
Invalidated
```

---

## 40.3. Hypothesis

```text
Proposed
→ Unverified
→ Supported / Rejected / Inconclusive
→ Superseded
```

---

## 40.4. Finding

```text
Preliminary
→ Validating
→ Validated
```

Alternative:

```text
Needs Review
Conflicting Evidence
Rejected
Invalidated
```

## 40.5. Research State

```text
Building
→ Active
→ Updated
→ Superseded
```

Each experiment/finding/decision must reference the Research State version used at the time.

## 40.6. Structured Decision

```text
Pending
→ Evaluating
→ Decided
```

Alternative:

```text
Needs Human Review
Overridden
Failed
Fallback Used
```

## 40.7. Scientific Refinement

```text
Requested
→ Planning
→ Ready
→ Executing
→ Re-verified
```

---

# 41. Core UI Screens

## 41.1. Project Dashboard

Show:

- research objective;
- current question;
- active hypothesis;
- latest experiment;
- latest finding;
- warnings;
- loop progress;
- dataset version;
- quick actions.

## 41.2. Dataset Detail

Tabs:

```text
Overview
Data Card
Quality
Versions
Transformations
```

## 41.3. Research Workspace

Primary workspace should show:

```text
Research Question
Research State Summary
Candidate Hypotheses / Directions
Hypothesis Selection Decision
Active Hypothesis
Agent Deep-Reasoning / Plan Summary
Experiment Timeline
Current Finding
Evidence Sufficiency Decision
Next Action
```

## 41.4. Experiment Detail

Tabs:

```text
Plan
Method & Assumptions
Execution
Result
Deterministic Validation
Evidence Decision
Refinement History
Trace
Reproducibility
```

## 41.5. Finding Detail

Show:

- finding statement;
- status;
- effect/CI;
- hypothesis;
- evidence;
- warnings;
- provenance;
- evidence-sufficiency decision;
- decision confidence/uncertainty;
- next hypothesis.

## 41.6. Dependency Graph

Visual graph of:

```text
RQ → H → E → F → H → E → F
```

## 41.7. Evaluation Dashboard

Show:

- benchmark runs;
- success rate;
- method accuracy;
- skill scores;
- hypothesis-selection quality;
- evidence-gate correctness;
- false evidence acceptance rate;
- escalation rate;
- confidence/calibration quality;
- cost;
- ablation comparison.

## 41.8. Decision History

Show:

```text
Decision Type
Research State Version
Candidates / Evidence Input
Outcome
Confidence
Reason Codes
Provider / Model
Downstream Action
Human Override
Timestamp
```

User must be able to open a decision and navigate to the related hypothesis, experiment, validation result and Research State.

---

# 42. Error & Empty States

## Dataset

- unsupported format;
- unreadable file;
- empty dataset;
- duplicate column names;
- too-large file;
- profiling failed.

## Research

- no active dataset;
- no research question;
- hypothesis not approved;
- insufficient sample;
- ambiguous variable.

## Experiment

- unsupported method;
- assumption failed;
- sandbox timeout;
- code error;
- dependency unavailable;
- max retry reached;
- user cancelled.

## Validation

- result invalid;
- conflicting evidence;
- multiple-testing warning;
- possible leakage;
- unsupported causal claim;
- evidence gate returned inconclusive;
- evidence insufficient for official finding;
- low-confidence structured decision.

## Decision Gate

- no suitable candidate hypothesis;
- decision provider unavailable;
- decision timeout;
- malformed structured decision;
- low confidence requiring review;
- provider fallback activated.

Every error state must include:

```text
What happened
Why it matters
What the user can do next
```

---

# 43. Notifications & Review Tasks

P1 notification types:

- dataset profiling complete;
- approval required;
- experiment complete;
- experiment failed;
- conflicting evidence detected;
- downstream findings invalidated;
- report ready;
- benchmark complete;
- hypothesis selection needs review;
- evidence sufficiency needs review;
- decision provider fallback used;
- scientific refinement requested.

Notifications should deep-link to the relevant object.

---

# 44. High-Level Data Entities

This PRD does not define the physical database schema, but product behavior requires at least:

```text
User
Role
Project
ProjectMember
Dataset
DatasetVersion
Transformation
DataProfile
DataCard
ResearchQuestion
ResearchContext
ResearchState
CandidateHypothesis
Hypothesis
HypothesisSelectionDecision
ExperimentPlan
Experiment
ExperimentBranch
AssumptionCheck
MethodSelection
ExecutionRun
ExecutionStep
StatisticalResult
ScientificValidation
EvidenceSufficiencyDecision
DecisionRecord
Finding
Evidence
DependencyEdge
ConflictRecord
Figure
ResearchTable
Report
ReproducibilitySnapshot
BenchmarkTask
BenchmarkRun
EvaluationMetric
AgentConfiguration
DecisionGateConfiguration
AuditLog
```

---

# 45. High-Level Relationship Model

```text
Project
├── Dataset
│   └── DatasetVersion
│       ├── DataProfile
│       └── Transformation
│
├── ResearchQuestion
│   └── ResearchState
│       ├── CandidateHypothesis
│       │   └── HypothesisSelectionDecision
│       │       └── Active Hypothesis
│       └── Hypothesis
│           └── Experiment
│               ├── AssumptionCheck
│               ├── MethodSelection
│               ├── ExecutionRun
│               ├── StatisticalResult
│               ├── ScientificValidation
│               ├── EvidenceSufficiencyDecision
│               └── Finding
│                   └── Updated ResearchState
│
├── Figure / Table
├── Report
└── Evaluation
```

---

# 46. Non-Functional Requirements

## NFR-01 — Security

- authentication required;
- server-side authorization;
- project data isolation;
- secure sandbox;
- encryption in transit;
- secret management;
- audit log for privileged actions.

## NFR-02 — Privacy

- user dataset is not exposed across projects;
- logs avoid storing raw sensitive data unless required;
- configurable retention where practical.

## NFR-03 — Reliability

- failed experiment does not corrupt project data;
- dataset versions immutable after creation;
- asynchronous jobs are retry-safe/idempotent where possible.

## NFR-04 — Performance

Initial targets for capstone:

- common page response target: ≤ 2 seconds excluding long-running jobs;
- upload/profiling can be asynchronous;
- experiment UI must show progress for long-running task;
- cancellation should be supported.

## NFR-05 — Explainability

User must be able to inspect:

- selected method;
- assumption result;
- experiment plan;
- supporting evidence;
- warnings.

## NFR-06 — Auditability

Important user/agent actions must have timestamp + actor + object.

## NFR-07 — Reproducibility

Official experiment must retain reproducibility snapshot.

## NFR-08 — Scalability

Architecture should allow workers/sandbox execution to scale separately from frontend/API, without requiring microservices for MVP.

## NFR-09 — Maintainability

Agent tools, validators and scorers should be modular and independently testable.

## NFR-10 — Accessibility

Primary web flows should support keyboard navigation, readable status labels and non-color-only error indication.

## NFR-11 — Scientific Integrity

Product must enforce:

- hypothesis ≠ fact;
- anomaly ≠ error;
- association ≠ causation;
- statistically significant ≠ practically important;
- decision confidence ≠ scientific evidence.

## NFR-12 — Decision Safety

- low-confidence/high-risk gate decisions must follow escalation policy;
- decision outcome must be typed/structured;
- malformed or missing decision must fail safely;
- official finding cannot bypass evidence gate.

## NFR-13 — Provider Portability

Hypothesis/evidence decision capability must be isolated behind a provider interface so that TypeSafe/Jev, structured LLM baseline or another compatible provider can be evaluated without rewriting research-domain workflows.

## NFR-14 — Observability

Telemetry must distinguish:

```text
technical retry
scientific refinement
gate decision
human escalation
provider fallback
human override
```

---

# 47. Product Metrics

## Adoption / Usage

- projects created;
- datasets uploaded;
- research loops started;
- experiments executed;
- reports generated.

## Agent Quality

- experiment success rate;
- method-selection acceptance rate;
- assumption warning rate;
- technical retry rate;
- scientific refinement rate;
- unsupported claim rate;
- human intervention rate;
- hypothesis-selection quality;
- evidence-gate correctness;
- false acceptance of insufficient evidence;
- unnecessary continuation rate.

## Trust

- provenance coverage;
- validated findings with evidence;
- reproducibility snapshot coverage;
- structured decision record coverage;
- low-confidence escalation compliance;
- decision calibration quality;
- number of downstream invalidations;
- number of conflicting evidence cases surfaced.

## Performance / Cost

- median experiment latency;
- average tool calls;
- tokens/run;
- estimated cost/run;
- sandbox failure rate.

---

# 48. Product Acceptance Criteria

Product is accepted when:

1. User can authenticate and create a project.
2. User can upload supported dataset.
3. Platform preserves immutable original dataset.
4. Platform automatically profiles dataset.
5. Data Card is generated for exact dataset version.
6. User can enter research question.
7. User can define/confirm H0/H1.
8. System builds a versioned Research State before research iteration.
9. Agent can generate candidate hypotheses/research directions from Research State.
10. Candidate hypotheses contain rationale, parent evidence and testability metadata.
11. Candidate cannot silently become active hypothesis.
12. Structured Hypothesis Selection Gate can rank/select/reject/escalate candidates.
13. Hypothesis-selection decision links to exact Research State version.
14. Selection decision stores confidence/uncertainty and provider/configuration reference.
15. Low-confidence/high-risk selection can create researcher review task.
16. Agent can generate structured experiment plan for selected hypothesis/direction.
17. Agent can generate candidate methods.
18. Agent can execute deterministic assumption checks.
19. Agent records selected method and rationale.
20. Agent can execute experiment in isolated sandbox.
21. Execution error can trigger bounded technical retry/re-plan.
22. Technical retry is recorded separately from scientific refinement.
23. Experiment creates inspectable raw/statistical result.
24. Deterministic validation can block unsupported result/interpretation.
25. Multiple-testing control is applied/justified when applicable.
26. Effect size/CI is shown when supported.
27. Leakage guard is applied for predictive/ML workflow when applicable.
28. Every completed validated experiment receives an Evidence Sufficiency decision before official finding.
29. Evidence gate supports `ENOUGH_EVIDENCE`.
30. Evidence gate supports `NEED_MORE_EVIDENCE`.
31. Evidence gate supports `TRY_ALTERNATIVE_METHOD`.
32. Evidence gate supports `REPLICATE`.
33. Evidence gate supports `NEED_HUMAN_REVIEW`.
34. Evidence gate supports `INCONCLUSIVE`.
35. Only `ENOUGH_EVIDENCE` may automatically proceed to validated finding.
36. `NEED_MORE_EVIDENCE`, `TRY_ALTERNATIVE_METHOD`, and `REPLICATE` can create a scientific refinement path.
37. `NEED_HUMAN_REVIEW` creates a researcher review task.
38. Validated finding links to hypothesis, experiment, dataset version, validation, evidence decision and execution trace.
39. Dataset transformations create new versions.
40. User can inspect experiment trace and provenance/evidence.
41. System preserves H1→E1→F1→H2→E2 lineage for iterative research.
42. Post-hoc hypotheses are marked `Post-hoc / Exploratory / Unverified` until tested.
43. Conflicting evidence is preserved.
44. Upstream invalidation flags affected downstream artifacts.
45. Stopping criteria can terminate research loop.
46. Official experiment has reproducibility snapshot.
47. Decision records preserve provider/model/configuration and downstream action.
48. Human override preserves original decision and override reason.
49. Evaluation center can measure hypothesis-gate quality.
50. Evaluation center can measure evidence-gate quality.
51. Evaluation center can compare Structured Decision Gate vs LLM-only decision baseline when benchmark labels/rubrics allow.
52. Benchmark/evaluation can compare at least two agent configurations.
53. System supports safe fallback/human review if structured decision provider is unavailable.
54. Final report uses validated findings only.

---

# 49. Release Plan

## Release 0 — Technical & Decision Spike

Goal: prove the riskiest execution and structured-decision interfaces.

Deliver:

```text
CSV
→ Data Profile
→ Research State
→ Mock / Structured DecisionProvider
→ Planner
→ run_python / statistical_test
→ Deterministic Validation
→ Evidence Decision
```

Must prove:

- sandbox execution;
- structured decision schema;
- provider abstraction;
- trace persistence.

---

## Release 1 — Core Research MVP

Deliver:

- auth/project;
- upload;
- profiling/Data Card;
- research question/H0/H1;
- Research State;
- experiment planner;
- method selection;
- assumption check;
- secure execution;
- deterministic validation;
- basic evidence gate;
- finding;
- trace/provenance.

Success demo:

```text
Dataset + H1
→ Research State
→ E1
→ Validation
→ Evidence Decision
→ Validated F1 or Inconclusive
```

---

## Release 2 — Decision-Gated Iterative Research Agent

Deliver:

- candidate hypothesis generation;
- Hypothesis Selection Gate;
- confidence-based escalation;
- hypothesis refinement;
- scientific refinement loop;
- H2 generation;
- stopping criteria;
- decision history;
- limited branching;
- conflict handling.

Success demo:

```text
F1
→ Candidate H2-A / H2-B / H2-C
→ Selection Gate
→ Selected H2
→ E2
→ Validation
→ Evidence Gate
→ F2 / Refine / Replicate
→ Stop
```

---

## Release 3 — Scientific Validity & Reproducibility

Deliver:

- multiple testing;
- effect size/CI;
- leakage guard;
- dependency graph;
- downstream invalidation;
- reproducibility snapshot;
- figure/table/report.

---

## Release 4 — Evaluation & Ablation

Deliver:

- benchmark tasks;
- repeated runs;
- quantitative metrics;
- skill evaluation;
- hypothesis-gate metrics;
- evidence-gate metrics;
- calibration metrics;
- `Structured Decision Gate vs LLM-only Decision`;
- ablation comparison.

---

# 50. BRD → PRD Traceability

| BRD Requirement | PRD Module |
|---|---|
| BR-01 Authentication | Module A |
| BR-02 RBAC | Module A |
| BR-03 Research Project Workspace | Module B |
| BR-04–07 Dataset Upload/Validation/Profiling | Modules C–D |
| BR-08–12 Data Quality/Cleaning/Versioning | Module E |
| BR-13 Research Question | Module F |
| BR-14–16 Hypothesis/Context | Modules F–G |
| BR-17 Experiment Planning | Module H |
| BR-18–20 Candidate Method/Assumption/Selection | Modules I–J |
| BR-21 Limited Branching | Module K |
| BR-22–23 Execution/Self-Correction | Module L |
| BR-24–25 Validation/Replication | Modules M, O |
| BR-26–30 Finding/Refinement/Stopping | Modules Q, R, U |
| BR-31 Statistical Analysis | Module I |
| BR-32–33 Visualization/Figure Review | Module V |
| BR-34–37 Provenance/Trace/Reproducibility | Modules X, Y, Z |
| BR-38–42 Research Output/Validation | Modules V, W, M |
| BR-43–46 Evaluation/Ablation | Module AA |
| BR-47 Leakage Guard | Module P |
| BR-48 Hypothesis Origin | Module G |
| BR-49 Multiple Testing | Module N |
| BR-50 Effect Size/CI | Module O |
| BR-51 Dependency Graph | Module S |
| BR-52 Downstream Invalidation | Module S |
| BR-53 Conflicting Evidence | Module T |
| BR-54 Confidence/Uncertainty | Module O |
| BR-55 Reproducibility Snapshot | Module Z |
| BR-56 Research State Construction | Module AC |
| BR-57 Candidate Hypothesis / Direction Generation | Module AC |
| BR-58 Structured Hypothesis Selection Gate | Module AD |
| BR-59 Evidence Sufficiency Gate | Module AE |
| BR-60 Scientific Refinement Loop | Module AF |
| BR-61 Confidence-Based Human Escalation | Modules AD, AF |
| BR-62 Decision Auditability | Module AG |
| BR-63 Decision Gate Evaluation | Modules AG, AA |
| BR-64 Structured Idea Record & Reflection | Module AH |
| BR-65 Novelty Assessment | Module AH |
| BR-73 Figure Aggregation & Visual Feedback | Module AH |
| BR-74 Manuscript Draft Generation | Module AH |
| BR-75 Automated Manuscript Review | Module AH |
| BR-78 Bounded Tied-Candidate Selection | Modules AD, H |

---

# 51. Research Evaluation Alignment

The product must expose telemetry required to answer the three research questions carried forward from BRD v1.2.

## RQ1 — End-to-End Effectiveness

How effectively can the AI Research Agent perform end-to-end research experimentation on user-provided datasets?

Relevant metrics:

- task success;
- result correctness;
- experiment completion;
- method-selection accuracy;
- evidence coverage;
- provenance coverage;
- reproducibility coverage;
- unsupported claim rate.

## RQ2 — Architecture Effectiveness

How effective is the architecture:

```text
GENERATE
→ SELECT
→ REASON
→ EXECUTE
→ VALIDATE
→ VERIFY
→ REFINE
```

compared with simpler architectures?

Required comparisons/ablations should include when feasible:

```text
Full Agent
No Planner
No Profiling
No Assumption Checking
No Retry
No Validator
No Hypothesis Refinement
No Hypothesis Selection Gate
No Evidence Sufficiency Gate
LLM-only Decision Baseline
Single-Pass / Text-to-Code Baseline
```

Relevant metrics:

- task success delta;
- false evidence acceptance;
- unnecessary continuation;
- human escalation;
- latency;
- cost;
- retry/refinement counts.

## RQ3 — Task / Skill Performance

How does the agent perform across:

- dataset understanding;
- candidate-hypothesis generation;
- hypothesis selection;
- deep experiment planning;
- method selection;
- assumption checking;
- execution;
- deterministic validation;
- evidence sufficiency verification;
- scientific refinement;
- evidence grounding;
- reproducibility.

Decision-gate evaluation should include:

- decision correctness;
- selection quality;
- confidence/calibration quality;
- false acceptance of insufficient evidence;
- unnecessary continuation rate;
- human escalation rate;
- latency;
- cost.

---

# 52. Key Product Risks

| Risk | Product Response |
|---|---|
| Agent chooses wrong method | Candidate methods + assumption checks + explain selection |
| Agent hallucinates business meaning | Research context + ask-user |
| Agent overclaims causality | Causal-language guard |
| Agent p-hacks through many tests | Testing-family tracking + correction |
| Agent cherry-picks results | Preserve branches/conflicts |
| Experiment chain depends on invalid result | Dependency graph + downstream invalidation |
| Dataset is damaged by cleaning | Immutable raw + versioning + approval |
| Generated code is unsafe | Sandbox + limits + no network by default |
| Result cannot be reproduced | Reproducibility snapshot |
| Loop runs forever | Stopping criteria + budgets |
| Too much scope for capstone | P0/P1/P2 prioritization |
| Hypothesis gate selects weak/irrelevant direction | Candidate set preserved + benchmark + human escalation |
| Evidence gate accepts insufficient evidence | Deterministic validation + conservative policy + gate evaluation |
| Decision confidence is poorly calibrated | Calibration metrics + conservative threshold + human review |
| TypeSafe/decision provider unavailable | Provider abstraction + structured-LLM fallback + human review |
| LLM and gate create long feedback loop | Stopping criteria + experiment/time/cost budgets |
| Gate provider fabricates scientific facts | Gate receives validated structured facts only; no fact-generation authority |

---

# 53. Open Product Decisions

These decisions should be finalized before implementation freeze:

1. Which file formats are P0: recommend CSV + XLSX.
2. Maximum dataset size for capstone deployment.
3. Which statistical methods are officially supported/tested in P0.
4. Whether every agent-generated post-hoc hypothesis requires manual approval.
5. Default max experiment count.
6. Default retry count per execution.
7. Default branch count for limited branching.
8. Which LLM/model provider(s) are supported.
9. Whether report export is Markdown/PDF/DOCX in MVP.
10. Whether evaluation datasets are internal, public benchmark, or both.
11. Exact benchmark scoring rubric.
12. Retention policy for uploaded datasets and raw execution output.
13. Which structured decision provider is primary for evaluation: TypeSafe/Jev, structured LLM, or both.
14. Default confidence threshold for automatic hypothesis selection.
15. Default confidence threshold for automatic evidence decision.
16. Whether first iteration uses gate-selected sub-hypothesis/direction or researcher-confirmed H1 directly.
17. Fallback policy when decision provider fails: structured LLM, human review, or fail-closed.
18. Which benchmark tasks have gold/rubric labels suitable for decision-gate calibration.
19. Whether candidate hypothesis count is fixed or budget-driven.
20. Whether human override should feed future evaluation only or also adaptive policy tuning.

---

# 54. Recommended MVP Demo Scenario

A canonical capstone demo should use a student dataset containing variables such as:

```text
student_id
score
ai_usage_rate
study_hours
attendance
major
other contextual variables
```

Example research flow:

```text
RQ:
Is AI usage associated with student academic performance?

Initial H0:
No statistically meaningful association exists.

Initial H1:
An association exists.

↓
Build Research State
- dataset/Data Card
- H0/H1
- current evidence = none
- available variables
- warnings / budget

↓
Generate Candidate Research Directions
A. Test overall association between AI usage and score
B. Test whether association differs by major
C. Test adjusted association controlling study_hours

↓
Hypothesis Selection Gate
SELECT A
confidence = ...
reason_codes = ...

↓
LLM Deep Reasoning
- choose variables
- design E1
- propose candidate methods

↓
Deterministic Assumption Checks

↓
E1:
Run appropriate association test.

↓
Deterministic Validation
- statistic / p-value
- effect size
- confidence interval
- assumptions
- multiple-testing state
- evidence quality

↓
Evidence Sufficiency Gate
Example outcome:
NEED_MORE_EVIDENCE

↓
Scientific Refinement
LLM proposes adjusted analysis because study_hours may confound interpretation.

↓
Generate Candidate H2 Directions
H2-A:
Association remains after controlling for study_hours.

H2-B:
Association differs by major.

↓
Hypothesis Selection Gate
SELECT H2-A
Type: Post-hoc / Exploratory / Unverified

↓
E2:
Regression / appropriate multivariable method.

↓
Deterministic Validation

↓
Evidence Sufficiency Gate
Example outcome:
ENOUGH_EVIDENCE

↓
F2:
Adjusted evidence-backed finding.

↓
Update Research State
↓
Stopping Criteria
↓
Final Research Findings
```

The demo should visibly show:

- exact Research State used;
- candidate hypotheses/directions;
- structured selection decision;
- confidence/uncertainty and reason codes;
- why statistical method was chosen;
- assumption results;
- technical retry vs scientific refinement if triggered;
- deterministic validation facts;
- evidence-sufficiency decision;
- experiment trace;
- evidence/provenance;
- hypothesis origin;
- H1→E1→F1→H2→E2 lineage;
- no unsupported causal conclusion;
- reproducibility metadata;
- decision-provider/configuration metadata.

### Demo Comparison for RQ2

If time permits, run the same benchmark/demo under:

```text
Configuration A
LLM handles reasoning + bounded decisions

vs

Configuration B
LLM handles deep reasoning
+
Structured Decision Gate handles selection / evidence routing
```

Compare:

```text
correctness
selection quality
false evidence acceptance
latency
cost
human intervention
confidence calibration
```

---

# 55. Definition of Done — Product Level

A feature is considered complete only when:

1. functional behavior is implemented;
2. authorization is enforced;
3. success/error/empty state exists;
4. audit/trace requirement is satisfied where relevant;
5. data object is linked to correct project/dataset version;
6. unit/integration tests cover critical logic;
7. acceptance criteria pass;
8. agent-related output is evaluated against at least one known test case;
9. UI communicates uncertainty/warnings clearly;
10. documentation is updated;
11. if the feature participates in structured decision flow, decision schema and audit record are tested;
12. technical retry and scientific refinement are classified correctly where applicable;
13. low-confidence/high-risk cases have a defined safe escalation path.

---

# 56. Next Documents

After PRD review, recommended next artifacts:

```text
PRD
↓
Use Case Specification
↓
System Architecture
↓
Agent Workflow / State Machine
↓
Decision Gate Contract / Provider Interface
↓
Activity Diagrams (Overall / Execution & Validation / Hypothesis & Evidence Loop)
↓
Database ERD
↓
API Contract
↓
UI Wireframe
↓
Test Strategy
↓
Benchmark & Evaluation Protocol
```

---

# 57. Document Change Log

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-09-19 | Initial full PRD derived from BRD Final v1.0 |
| 1.0 | 2026-09-20 | Finalized PRD aligned with BRD v1.2; added Research State, candidate-hypothesis generation, Structured Hypothesis Selection Gate, Evidence Sufficiency Gate, scientific refinement, confidence-based escalation, decision audit/provider abstraction, TypeSafe/Jev as candidate provider, decision-gate evaluation, updated state machine, UI, entities, NFRs, release plan, acceptance criteria, risks and RQ alignment |
| 1.1 | 2026-09-22 | Added support for bounded tied-candidate selection at the Hypothesis Selection Gate (BR-58/BR-78): new FR-PLAN-04, concurrency-quota bullet in the concurrent-execution module, extended multiple-testing FR, new `co_selected_with` dependency-graph edge, extended conflicting-evidence and stopping-criteria FRs, new ablation arm, new FR-HGATE-07, and new Decision Record fields `tie_threshold_used`/`tied_candidates`, plus a new human-escalation trigger |
| 1.2 | 2026-09-22 | Added PG-18 (Product Goal for bounded tied-candidate selection) |
| 1.3 | 2026-09-22 | Fixed a direct contradiction in Non-Goals: the original wording excluded "full Agentic Tree Search" while BRD v1.7 mandated a bounded Experiment Tree (BR-66→BR-71) as Must — reworded Non-Goals to distinguish unbounded/general-purpose tree search (excluded) from the bounded, single-hypothesis Experiment Tree (then in scope) |
| 1.4 | 2026-09-22 | BRD v1.8 removed the entire bounded tree-search layer (BR-66→BR-72, BR-76, BR-77 and dependents) to restore the platform's original linear Decision-Gated Research Loop; reworded Non-Goals again to plainly exclude Agentic Tree Search (bounded or unbounded) and note that idea reflection, novelty assessment and automated manuscript review are still referenced from agentic-research systems without adopting their tree-search architecture; updated header Status/Source to BRD v1.8 |
| 1.5 | 2026-09-22 | Closed three remaining coverage/consistency gaps found by cross-audit: (1) added new Feature Module AH — Ideation Quality & Manuscript Reporting, covering BR-64 (Idea Record & Reflection, Must), BR-65 (Novelty Assessment), BR-73 (Figure Aggregation & Visual Feedback), BR-74 (Manuscript Draft Generation) and BR-75 (Automated Manuscript Review), none of which had any PRD module/FR before this version despite being defined in BRD since v1.3; (2) added BR-64/65/73/74/75/78 rows to the BRD → PRD Traceability table (mục 50), which previously stopped at BR-63 and also omitted BR-78 even though BR-78 was already functionally implemented in Modules AD/H; (3) annotated Module K (Limited Experiment Branching, BR-21) as "Must for final capstone" to match the BRD MoSCoW (Must) and the annotation convention used by Modules AC-AH, resolving a priority-signal mismatch flagged earlier but not previously fixed |
| 1.6 | 2026-09-22 | A follow-up cross-audit (comparing every BRD Must-priority BR against its PRD module's Priority line) found the same priority-signal mismatch fixed for Module K in v1.5 was still present in 8 more modules; annotated all of them with "Must for final capstone" plus the specific Must BR(s) driving it: Module N (BR-49), Module O (BR-50, BR-54), Module R (BR-28), Module U (BR-30), Module V (BR-32, BR-38; advanced visual/VLM reviewer sub-item stays P2), Module W (BR-41, BR-42), Module Z (BR-55), Module AA (BR-43, BR-63) — every PRD module that contains at least one BRD Must requirement is now annotated consistently; no functional/FR changes |
| 1.7 | 2026-09-22 | Fixed a different kind of priority mismatch in Module I: BR-31 (Statistical Analysis, Must in BRD, flat list with no internal split) had been silently split by the PRD into P0 and P1 sub-lists, demoting "interaction analysis" and "basic time-series analysis" to P1 despite both being explicitly named in the Must-priority BR-31; moved both into the P0/Must list so it now matches BR-31 exactly, and kept "simple repeated-measure support" and "selected ML prediction workflows" (which are PRD-only additions not present in BR-31 at all) at P1 with a note that they are extensions beyond BR-31 and not required for Must compliance |
