# Product Requirements Document (PRD)
## AI Research Experimentation Platform

**Document Type:** Product Requirements Document  
**Project:** AI Research Experimentation Platform  
**Version:** 0.1 Draft  
**Status:** Draft for Product / Technical Review  
**Source:** Business Requirements Document Final v1.0  
**Date:** 2026-09-19  

---

# 1. Product Summary

AI Research Experimentation Platform là nền tảng web sử dụng AI Agent để hỗ trợ researcher thực hiện quy trình nghiên cứu dựa trên structured/tabular datasets.

Sản phẩm không chỉ thực hiện một lần phân tích dữ liệu, mà quản lý một research loop có cấu trúc:

```text
Research Question
    ↓
Initial Hypothesis H0 / H1
    ↓
Dataset Understanding
    ↓
Experiment Planning
    ↓
Candidate Method Selection
    ↓
Assumption Checking
    ↓
Experiment Execution
    ↓
Scientific Validation
    ↓
Research Finding
    ↓
Stopping Criteria?
   / \
 No   Yes
 │     │
 ▼     ▼
Generate H(n+1)      Final Research Findings
Post-hoc/Unverified          ↓
 │                    Figures / Tables
 ▼                           ↓
Next Experiment       Research Report
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

Platform tập trung vào bốn giá trị sản phẩm:

1. **Scientific Validity** — method phù hợp, assumptions rõ ràng, multiple-testing control, effect size và uncertainty.
2. **Traceability** — mọi finding quan trọng có provenance và execution trace.
3. **Reproducibility** — experiment có metadata/snapshot đủ để tái lập.
4. **Human Control** — researcher giữ quyền quyết định tại các bước có uncertainty/risk cao.

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
- full Agentic Tree Search như một research-search system tổng quát.

Platform có thể tham khảo iterative experimentation từ các agentic research systems, nhưng scope chính vẫn là **scientific analysis trên user-provided structured datasets**.

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
- stopping criteria;
- limited experiment branching;
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
- ablation.

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
│   ├── Hypotheses
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
Automatic Profiling
↓
Review Data Card
↓
Review Data Quality
↓
Apply Approved Cleaning if needed
↓
Enter Research Question
↓
Define Initial H0/H1
↓
Start Research Loop
↓
Generate Experiment Plan
↓
Generate Candidate Methods
↓
Check Assumptions
↓
Select Method / Branch
↓
Execute in Sandbox
↓
Observe / Retry / Re-plan
↓
Scientific Validation
↓
Generate Finding
↓
Evaluate Hypothesis
↓
Stopping Criteria?
├── No → Generate/Review H(n+1) → Next Experiment
└── Yes → Final Findings → Figures/Tables → Report
```

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

## Acceptance Criteria

- plan references exact hypothesis and dataset version;
- plan lists candidate methods;
- user can inspect plan before execution;
- reason for re-plan is logged.

**Priority:** P0

---

# 18. Feature Module I — Candidate Method Generation & Selection

## Objective

Cho agent lựa chọn statistical/analytical method phù hợp thay vì hard-code một test duy nhất.

## Initial Supported Methods

P0:

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
- logistic regression.

P1:

- interaction analysis;
- simple repeated-measure support;
- basic time-series analysis;
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

**Priority:** P1

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
- output size limit.

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

Experiments may be grouped into a testing family.

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

**Priority:** P1

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

**Priority:** P1

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

**Priority:** P1

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
```

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

When experiments produce incompatible evidence, system shall preserve all results.

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

After each validated finding, agent evaluates stopping criteria.

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

**Priority:** P1

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

**Priority:** P1; advanced visual/VLM reviewer P2

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

**Priority:** P1

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

**Priority:** P1

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

**Priority:** P1

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

# 38. Agent Runtime Product Behavior

High-level agent state machine:

```text
IDLE
↓
BUILD_CONTEXT
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
├── Error → RETRY / REPLAN
└── Success
      ↓
VALIDATE
├── Invalid → REPLAN / ASK_USER / STOP
└── Valid
      ↓
GENERATE_FINDING
      ↓
EVALUATE_STOPPING
├── Continue → REFINE_HYPOTHESIS → PLAN
└── Stop → FINALIZE
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
- explicit publication/final report approval.

## Optional Auto-Continue

Low-risk cases may continue automatically:

- profiling;
- descriptive stats;
- safe schema inspection;
- read-only diagnostics;
- retry of syntax/runtime error within limit.

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
Active Hypothesis
Agent Plan
Experiment Timeline
Current Finding
Next Action
```

## 41.4. Experiment Detail

Tabs:

```text
Plan
Method & Assumptions
Execution
Result
Validation
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
- cost;
- ablation comparison.

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
- unsupported causal claim.

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
- benchmark complete.

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
Hypothesis
ExperimentPlan
Experiment
ExperimentBranch
AssumptionCheck
MethodSelection
ExecutionRun
ExecutionStep
StatisticalResult
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
│   └── Hypothesis
│       └── Experiment
│           ├── AssumptionCheck
│           ├── MethodSelection
│           ├── ExecutionRun
│           ├── StatisticalResult
│           └── Finding
│               └── Next Hypothesis
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
- retry rate;
- unsupported claim rate;
- human intervention rate.

## Trust

- provenance coverage;
- validated findings with evidence;
- reproducibility snapshot coverage;
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

Product MVP is accepted when:

1. User can authenticate and create a project.
2. User can upload supported dataset.
3. Platform preserves immutable original dataset.
4. Platform automatically profiles dataset.
5. Data Card is generated for exact dataset version.
6. User can enter research question.
7. User can define/confirm H0/H1.
8. Agent can generate structured experiment plan.
9. Agent can generate candidate methods.
10. Agent can execute assumption checks.
11. Agent records selected method and reason.
12. Agent can execute experiment in isolated sandbox.
13. Execution error can trigger bounded retry/re-plan.
14. Experiment creates inspectable raw/statistical result.
15. Validation can block unsupported finding.
16. Validated finding links to hypothesis and experiment.
17. Validated finding links to dataset version and execution trace.
18. Dataset transformations create new versions.
19. User can inspect experiment trace.
20. User can inspect provenance/evidence.
21. P1: Agent can propose post-hoc H2 from F1.
22. P1: H2 is marked `Post-hoc / Unverified`.
23. P1: System can run E2 and preserve H1→E1→F1→H2→E2 linkage.
24. P1: Stopping criteria can end loop.
25. P1: Multiple-testing warning/correction works when applicable.
26. P1: Effect size/CI is shown when supported.
27. P1: Conflicting evidence is preserved.
28. P1: Upstream invalidation flags affected downstream artifacts.
29. P1: Validated official experiment has reproducibility snapshot.
30. P1: Benchmark/evaluation can compare at least two agent configurations.

---

# 49. Release Plan

## Release 0 — Technical Spike

Goal: prove tool execution.

Deliver:

```text
CSV
→ Data Profile
→ Planner
→ run_python/statistical_test
→ Result
```

No full UI required.

---

## Release 1 — Core Data Agent MVP

Deliver:

- auth/project;
- upload;
- profiling/Data Card;
- research question/H0/H1;
- experiment planner;
- method selection;
- assumption check;
- secure execution;
- finding;
- trace/provenance.

Success demo:

```text
Dataset + H1
→ E1
→ Validated F1
```

---

## Release 2 — Iterative Research Agent

Deliver:

- hypothesis refinement;
- H2 generation;
- dependency graph;
- stopping criteria;
- limited branching;
- conflict handling.

Success demo:

```text
H1 → E1 → F1 → H2 → E2 → F2 → Stop
```

---

## Release 3 — Scientific Validity & Reproducibility

Deliver:

- multiple testing;
- effect size/CI;
- leakage guard;
- downstream invalidation;
- reproducibility snapshot;
- figure/table/report.

---

## Release 4 — Evaluation

Deliver:

- benchmark tasks;
- repeated runs;
- quantitative metrics;
- skill evaluation;
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

---

# 51. Research Evaluation Alignment

The product must expose enough telemetry to evaluate three broad research areas:

## RQ-A — End-to-End Effectiveness

Can the agent successfully move from user-provided dataset + research question to a scientifically defensible result?

Relevant metrics:

- task success;
- correctness;
- experiment completion;
- evidence coverage.

## RQ-B — Architecture Effectiveness

Do planning, profiling, validation, retry and hypothesis refinement improve performance compared with simpler baselines?

Relevant method:

- ablation study.

## RQ-C — Task/Skill Performance

How does the agent perform across:

- dataset understanding;
- method selection;
- assumption checking;
- execution;
- validation;
- hypothesis refinement;
- evidence grounding?

Relevant output:

- per-skill scores.

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
E1:
Agent selects appropriate association test after checking assumptions.

↓
F1:
Association result + effect size + CI + limitations.

↓
H2:
Does the association remain after controlling for study_hours?
Type: Post-hoc / Exploratory / Unverified

↓
E2:
Regression / appropriate multivariable method.

↓
F2:
Adjusted result.

↓
Stopping Criteria
↓
Final Research Findings
```

The demo should visibly show:

- why the method was chosen;
- assumption results;
- experiment trace;
- evidence;
- hypothesis origin;
- H1→E1→F1→H2→E2 dependency;
- no unsupported causal conclusion;
- reproducibility metadata.

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
10. documentation is updated.

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
