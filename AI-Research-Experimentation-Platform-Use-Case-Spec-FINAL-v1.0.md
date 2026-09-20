# Use Case Specification
## AI Research Experimentation Platform

**Document Type:** Use Case Specification  
**Project:** AI Research Experimentation Platform  
**Version:** 1.0 Final  
**Status:** Final / Aligned with BRD v1.2 and PRD v1.0  
**Date:** 2026-09-20  

---

# 1. Purpose

Tài liệu này mô tả các use case chính của **AI Research Experimentation Platform** theo góc nhìn:

```text
Actor
→ Goal
→ Preconditions
→ Trigger
→ Main Flow
→ Alternative / Exception Flows
→ Postconditions
→ Business Rules
→ Acceptance Criteria
```

Use Case Specification không mô tả chi tiết implementation nội bộ của LLM, sandbox hoặc decision provider. Các thành phần đó được xem là **internal system components**, không phải external UML actors.

Core research flow được use case layer hỗ trợ:

```text
Research Question + Dataset
        ↓
Initial H0 / H1
        ↓
Research State
        ↓
Candidate Hypotheses / Research Directions
        ↓
Structured Hypothesis Selection
        ↓
Selected Direction
        ↓
Deep Reasoning + Experiment Planning
        ↓
Method Selection + Assumption Checks
        ↓
Experiment Execution
        ↓
Deterministic Scientific Validation
        ↓
Evidence Sufficiency Decision
        ↓
Finding / Scientific Refinement / Human Review / Inconclusive
        ↓
Update Research State
        ↓
Stopping Criteria
        ↓
Next Iteration or Final Research Outputs
```

---

# 2. Use Case Modeling Rules

## 2.1. External Actors Only

Official UML Use Case Diagram chỉ sử dụng external actors:

- Researcher / Data Analyst;
- Project Manager;
- Reviewer / Stakeholder;
- System Administrator.

Các thành phần sau **không phải actors**:

- AI Research Agent;
- LLM;
- TypeSafe / Jev;
- Structured Decision Provider;
- Tool Router;
- Statistical Tools;
- Secure Sandbox;
- Scientific Validator.

Chúng là internal components và được mô tả ở Activity Diagram, Sequence Diagram và SDD.

## 2.2. Role Combination

Một user có thể có nhiều role. Ví dụ:

```text
Project Manager + Researcher
```

khi đó user nhận union của các permissions tương ứng.

Project Manager thuần quản trị project không mặc định được xem là người thực hiện scientific experiment nếu không có Researcher permission.

## 2.3. Scientific Decision Rule

Platform phải phân biệt:

```text
Technical Retry
≠
Scientific Refinement
```

- **Technical Retry:** execution thất bại do code/runtime/tool.
- **Scientific Refinement:** execution thành công nhưng evidence chưa đủ hoặc cần alternative/replication.

## 2.4. Structured Decision Rule

Structured decision provider có thể được triển khai bằng:

```text
TypeSafe / Jev
Structured LLM Provider
Other compatible provider
```

Use case không phụ thuộc một vendor cụ thể.

---

# 3. Actors

## ACT-01 — Researcher / Data Analyst

Primary actor của research workflow.

### Goals

- upload và hiểu dataset;
- review data-quality issues;
- định nghĩa research question;
- định nghĩa/confirm H0/H1;
- review Research State;
- review candidate hypotheses/research directions;
- review hypothesis-selection decision;
- review experiment plan;
- review method selection và assumptions;
- chạy experiment;
- review deterministic validation;
- review evidence-sufficiency decision;
- xử lý scientific refinement/human review;
- review findings;
- theo dõi dependency/conflicting evidence;
- quyết định continue/stop;
- tạo research outputs;
- xem provenance, trace và decision history;
- chạy benchmark/evaluation nếu có quyền.

---

## ACT-02 — Project Manager

Quản lý project và theo dõi research progress.

### Goals

- tạo/quản lý project;
- quản lý members;
- xem Research State và project progress;
- review findings;
- review dependency/conflicting evidence;
- review/generate project-level outputs nếu có quyền;
- xem provenance/trace;
- chạy benchmark/evaluation nếu có quyền.

---

## ACT-03 — Reviewer / Stakeholder

Read/review actor.

### Goals

- xem validated findings;
- xem report/figures/tables;
- xem evidence/provenance;
- xem experiment/decision trace;
- xem limitations/conflicting evidence;
- gửi feedback nếu được cấp quyền.

Reviewer không trực tiếp tạo experiment hoặc generate official report.

---

## ACT-04 — System Administrator

Quản trị hệ thống.

### Goals

- quản lý users/roles;
- quản lý model/provider configuration;
- quản lý decision-provider configuration;
- xem logs/system health;
- xem usage/cost;
- quản lý benchmark/evaluation configuration;
- audit provider fallback và system failures.

---

# 4. Internal System Components

Các thành phần sau tham gia use case nhưng không phải external actors:

| Component | Responsibility |
|---|---|
| Generative Reasoner / LLM | Generate, reason, plan, interpret, refine |
| Research State Builder | Build/version structured research context |
| Structured Decision Provider | Rank/select/verify/route bounded decisions |
| Analytical / Statistical Tools | Calculate scientific facts |
| Tool Router | Route tool requests |
| Secure Sandbox | Execute code/query with isolation/limits |
| Scientific Validator | Deterministic validation |
| Provenance Service | Link finding → evidence → execution → dataset |
| Evaluation Engine | Benchmark, scoring, ablation |
| Audit / Telemetry | Persist trace, decision, cost, latency, retry/refinement |

---

# 5. Use Case Summary

| ID | Use Case | Primary Actor | Priority |
|---|---|---|---|
| UC-01 | Authenticate | All users | P0 |
| UC-02 | Create / Manage Research Project | Researcher / Project Manager | P0 |
| UC-03 | Manage Project Members | Project Manager | P0 |
| UC-04 | Upload & Validate Dataset | Researcher | P0 |
| UC-05 | Review Profiling & Data Card | Researcher | P0 |
| UC-06 | Review Data Quality, Cleaning & Versioning | Researcher | P0 |
| UC-07 | Define Research Question & Context | Researcher | P0 |
| UC-08 | Define / Confirm Initial H0 & H1 | Researcher | P0 |
| UC-09 | Review Research State | Researcher | P0 |
| UC-10 | Generate & Review Candidate Hypotheses / Directions | Researcher | P1 |
| UC-11 | Review / Resolve Hypothesis Selection Decision | Researcher | P1 |
| UC-12 | Generate & Review Experiment Plan | Researcher | P0 |
| UC-13 | Review Method Selection & Assumption Checks | Researcher | P0 |
| UC-14 | Execute Experiment | Researcher | P0 |
| UC-15 | Review Deterministic Scientific Validation | Researcher | P0 |
| UC-16 | Review / Resolve Evidence Sufficiency Decision | Researcher | P1 |
| UC-17 | Resolve Scientific Refinement / Human Review | Researcher | P1 |
| UC-18 | Review Research Finding | Researcher / Reviewer | P0 |
| UC-19 | Review Dependency, Invalidation & Conflicting Evidence | Researcher | P1 |
| UC-20 | Continue or Stop Research Loop | Researcher | P1 |
| UC-21 | Generate Figures, Tables & Research Report | Researcher | P1 |
| UC-22 | View Research Outputs, Provenance, Evidence, Trace & Decision History | Researcher / Reviewer | P0 |
| UC-23 | Run Benchmark & Evaluation | Researcher / Project Manager / Admin | P1 |
| UC-24 | Manage Models, Decision Providers, Logs, Cost & System Configuration | Admin | P1 |

---

# 6. Actor–Use Case Access Matrix

Legend:

```text
P = Primary / performs use case
R = Review / read access
C = Conditional when role/permission is granted
- = Not normally associated
```

| Use Case | Researcher | Project Manager | Reviewer | Admin |
|---|---:|---:|---:|---:|
| UC-01 Authenticate | P | P | P | P |
| UC-02 Manage Project | P | P | - | C |
| UC-03 Manage Members | - | P | - | C |
| UC-04 Upload Dataset | P | C | - | C |
| UC-05 Review Profiling | P | R | - | C |
| UC-06 Cleaning & Versioning | P | C | - | C |
| UC-07 Research Question | P | R | - | C |
| UC-08 Initial H0/H1 | P | R | - | C |
| UC-09 Review Research State | P | R | R | C |
| UC-10 Candidate Hypotheses | P | R | - | C |
| UC-11 Hypothesis Selection Decision | P | R | - | C |
| UC-12 Experiment Plan | P | R | - | C |
| UC-13 Method & Assumptions | P | R | R | C |
| UC-14 Execute Experiment | P | C | - | C |
| UC-15 Scientific Validation | P | R | R | C |
| UC-16 Evidence Sufficiency | P | R | R | C |
| UC-17 Scientific Refinement / Human Review | P | C | - | C |
| UC-18 Review Finding | P | R | P/R | C |
| UC-19 Dependency / Conflict | P | R | R | C |
| UC-20 Continue / Stop | P | C | - | C |
| UC-21 Generate Outputs | P | C | - | C |
| UC-22 View Outputs / Evidence / Trace | P | R | P/R | C |
| UC-23 Benchmark / Evaluation | P | P | R | P |
| UC-24 Administration | - | - | - | P |

---

# 7. UC-01 — Authenticate

## Goal

Cho phép user đăng nhập và truy cập đúng phạm vi quyền.

## Primary Actor

All users.

## Preconditions

- account tồn tại;
- account không bị disabled.

## Trigger

User mở platform và chọn đăng nhập.

## Main Flow

1. User nhập credential.
2. System xác thực credential.
3. System tạo authenticated session/token.
4. System tải global role và project memberships.
5. System áp dụng authorization policy.
6. User được chuyển tới workspace phù hợp.

## Alternative / Exception Flows

### A1 — Invalid Credential

1. Authentication thất bại.
2. System hiển thị lỗi không tiết lộ sensitive information.
3. Không tạo session.

### A2 — Account Disabled

System từ chối truy cập dù credential đúng.

### A3 — Session Expired

System yêu cầu user authenticate lại.

## Postconditions

- valid user có authenticated session;
- permissions được enforce server-side.

## Acceptance Criteria

- invalid/expired session không truy cập protected resources;
- project scope được enforce;
- privileged actions có audit record.

---

# 8. UC-02 — Create / Manage Research Project

## Goal

Tạo và quản lý workspace chứa toàn bộ research lifecycle.

## Primary Actor

Researcher / Project Manager.

## Preconditions

- actor đã authenticate;
- actor có quyền create/manage project.

## Trigger

Actor chọn `Create Project` hoặc mở project hiện có.

## Main Flow

1. Actor nhập/sửa:
   - project name;
   - description;
   - research domain;
   - objective;
   - tags.
2. System validate input.
3. System tạo/cập nhật Project.
4. System gán owner khi tạo mới.
5. Project dashboard hiển thị:
   - active research question;
   - Research State;
   - dataset;
   - current hypothesis;
   - latest experiment;
   - latest finding;
   - warnings;
   - loop status;
   - report status.

## Alternative Flows

### A1 — Missing Required Field

System không lưu và highlight field lỗi.

### A2 — Archived Project

Project mặc định read-only trừ user có quyền restore.

## Postconditions

Project tồn tại với state hợp lệ và audit metadata.

---

# 9. UC-03 — Manage Project Members

## Goal

Quản lý membership và project-level roles.

## Primary Actor

Project Manager.

## Preconditions

- project tồn tại;
- actor có `Manage Members`.

## Trigger

Actor mở `Project Settings → Members`.

## Main Flow

1. Actor xem member list.
2. Actor chọn add member hoặc edit role.
3. System kiểm tra user.
4. Actor chọn project role.
5. System lưu membership/role.
6. Permission có hiệu lực.
7. System ghi audit record.

## Alternative Flows

### A1 — Member Already Exists

System chuyển sang update role.

### A2 — Actor Lacks Permission

System trả access denied.

### A3 — Removing Last Owner/Manager

System block nếu vi phạm ownership policy.

## Postconditions

Membership và permission state được cập nhật.

---

# 10. UC-04 — Upload & Validate Dataset

## Goal

Đưa structured dataset vào project và đảm bảo đủ điều kiện xử lý.

## Primary Actor

Researcher.

## Preconditions

- project tồn tại;
- actor có quyền upload.

## Trigger

Actor chọn `Upload Dataset`.

## Main Flow

1. Actor chọn supported file.
2. System upload file.
3. System lưu immutable original.
4. System tính checksum.
5. System tạo Dataset entity.
6. System tạo raw `Dataset Version v1`.
7. System validate:
   - readability;
   - encoding;
   - empty file;
   - schema/header;
   - duplicate column names;
   - unsupported types;
   - row/column count;
   - file-size limits.
8. Nếu validation pass, system enqueue profiling.
9. Dataset chuyển sang trạng thái phù hợp.

## Alternative Flows

### A1 — Unsupported Format

System reject và hiển thị supported formats.

### A2 — Invalid Dataset

Dataset không được dùng cho research planning.

### A3 — Upload Interrupted

Không tạo usable dataset version.

## Postconditions

- raw dataset immutable;
- usable dataset gắn version cụ thể;
- validation record tồn tại.

## Includes

`<<include>> Validate Dataset`

---

# 11. UC-05 — Review Profiling & Data Card

## Goal

Giúp researcher hiểu dataset trước khi research planning.

## Primary Actor

Researcher.

## Preconditions

- dataset validation pass;
- profiling hoàn tất.

## Trigger

Actor mở Dataset Detail.

## Main Flow

1. System hiển thị:
   - row/column count;
   - variable types;
   - missing ratio;
   - duplicates;
   - cardinality;
   - descriptive statistics;
   - distribution hints;
   - candidate outliers;
   - sample values;
   - potential identifiers/relationships;
   - quality warnings.
2. System hiển thị Data Card của exact dataset version.
3. Actor review warnings.
4. Actor bổ sung variable/domain meaning nếu cần.
5. System lưu context update.

## Alternative Flows

### A1 — Profiling Failed

System hiển thị reason và cho phép retry.

### A2 — Ambiguous Variable Type / Meaning

System yêu cầu actor override hoặc clarify.

## Postconditions

- Data Card tồn tại;
- agent/research workflow có compact dataset context.

---

# 12. UC-06 — Review Data Quality, Cleaning & Versioning

## Goal

Xử lý data-quality issue mà không phá raw research data.

## Primary Actor

Researcher.

## Preconditions

- Data Card tồn tại.

## Trigger

System phát hiện issue hoặc actor mở Data Quality.

## Main Flow

1. System classify issue:
   - Confirmed Data Issue;
   - Potential Anomaly;
   - Needs User Confirmation;
   - Needs Domain Clarification.
2. System hiển thị cleaning proposal:
   - transformation;
   - rationale;
   - affected rows/columns;
   - potential information loss;
   - risk;
   - reversibility.
3. Actor chọn:
   - Approve;
   - Reject;
   - Modify;
   - Ask Agent.
4. Nếu approved, transformation chạy trên derived version.
5. System tạo new Dataset Version.
6. System regenerate Data Card.
7. Transformation lineage được lưu.

## Alternative Flows

### A1 — Risky Transformation

Human approval bắt buộc.

### A2 — Actor Rejects

Dataset giữ nguyên và decision được log.

### A3 — Transformation Fails

Không tạo completed derived version.

## Postconditions

- original dataset không bị ghi đè;
- lineage được lưu.

## Extends

`Human Approval <<extend>> UC-06 [risky/destructive transformation]`

---

# 13. UC-07 — Define Research Question & Context

## Goal

Xác định scientific/research problem và domain context.

## Primary Actor

Researcher.

## Preconditions

- project tồn tại;
- có ít nhất một dataset ready.

## Trigger

Actor chọn `Create Research Question`.

## Main Flow

1. Actor nhập:
   - question text;
   - research goal;
   - domain context;
   - relevant variables;
   - constraints;
   - optional prior assumptions/notes.
2. System validate.
3. Research Question trở thành active.
4. Context được version/timestamp.
5. System sử dụng context cho hypothesis/research planning.

## Alternative Flows

### A1 — Variable Meaning Ambiguous

System yêu cầu clarification.

### A2 — Unsupported Causal Question

System warning rằng current design/data có thể chỉ hỗ trợ association.

## Postconditions

Active Research Question tồn tại.

---

# 14. UC-08 — Define / Confirm Initial H0 & H1

## Goal

Tạo initial/confirmatory hypothesis cho research loop.

## Primary Actor

Researcher.

## Preconditions

- active Research Question tồn tại.

## Trigger

Actor mở Hypothesis Setup.

## Main Flow

1. Actor nhập H0/H1 hoặc yêu cầu AI draft.
2. Nếu AI draft, actor review.
3. Actor confirm.
4. System lưu:
   - `Origin = Initial / Confirmatory`;
   - `Status = Unverified`;
   - parent Research Question;
   - created-by metadata.
5. System chuẩn bị Research State.

## Alternative Flows

### A1 — Hypothesis Not Testable

System giải thích và đề xuất rewrite.

### A2 — Missing Required Variables

System mark insufficient data / needs clarification.

### A3 — AI Draft Not Confirmed

Hypothesis giữ ở `Proposed`, không trở thành active initial hypothesis.

## Postconditions

Initial H0/H1 sẵn sàng cho research iteration.

---

# 15. UC-09 — Review Research State

## Goal

Cho researcher xem structured state dùng làm context chính thức cho research iteration.

## Primary Actor

Researcher.

## Secondary Actors

Project Manager / Reviewer có read access nếu được cấp quyền.

## Preconditions

- Research Question tồn tại;
- dataset version tồn tại;
- initial hypothesis hoặc prior iteration tồn tại.

## Trigger

- actor mở `Research State`; hoặc
- system tạo/update state trước research iteration.

## Main Flow

1. System build/version Research State từ:
   - Research Question;
   - current hypothesis;
   - previous hypotheses;
   - experiment history;
   - validated findings;
   - conflicting evidence;
   - uncertainty/warnings;
   - dataset version;
   - remaining experiment/time/cost constraints;
   - iteration number.
2. System gắn unique Research State version.
3. Actor review state summary.
4. Actor có thể navigate tới source artifacts.
5. Nếu context sai/thiếu, actor sửa domain context hoặc dataset/hypothesis selection.
6. System tạo updated Research State version.

## Alternative Flows

### A1 — Missing Required Context

State = `Needs Review`; candidate generation bị block.

### A2 — Referenced Dataset Version Superseded

System warning và yêu cầu chọn version hợp lệ.

## Postconditions

Active Research State version tồn tại.

## Includes

`<<include>> Build Research State`

---

# 16. UC-10 — Generate & Review Candidate Hypotheses / Research Directions

## Goal

Sinh một hoặc nhiều testable candidate hypotheses/research directions từ active Research State.

## Primary Actor

Researcher.

## Preconditions

- active Research State hợp lệ.

## Trigger

Actor chọn `Generate Candidates` hoặc research loop yêu cầu iteration tiếp theo.

## Main Flow

1. System cung cấp Research State cho Generative Reasoner.
2. Reasoner tạo candidate set.
3. Mỗi candidate tối thiểu có:
   - statement;
   - rationale;
   - parent evidence;
   - testability;
   - relevant variables;
   - risk/uncertainty notes;
   - origin.
4. System đánh dấu candidate sau prior findings là:
   - `Post-hoc / Exploratory`;
   - `Unverified`.
5. System hiển thị candidate list.
6. Actor có thể:
   - inspect;
   - request more candidates;
   - edit candidate;
   - discard obvious invalid candidate;
   - continue to selection gate.

## Alternative Flows

### A1 — Candidate Not Testable

Candidate được mark unsupported/deferred.

### A2 — No Candidate Generated

System yêu cầu clarification hoặc đề xuất stopping review.

### A3 — Candidate Requires Missing Data

Candidate được mark `Needs Data`.

## Postconditions

Candidate set sẵn sàng cho structured selection.

---

# 17. UC-11 — Review / Resolve Hypothesis Selection Decision

## Goal

Chọn, reject hoặc escalate candidate research direction trước deep experiment planning.

## Primary Actor

Researcher.

## Preconditions

- candidate set tồn tại;
- active Research State tồn tại.

## Trigger

Candidate generation hoàn tất.

## Main Flow

1. System gửi Research State + candidate set tới configured Structured Decision Provider.
2. Provider evaluate candidates theo policy, ví dụ:
   - relevance;
   - testability;
   - evidence support;
   - feasibility;
   - confidence/uncertainty.
3. Provider trả structured decision:
   - `SELECT`;
   - `REJECT`;
   - `ESCALATE_TO_RESEARCHER`;
   - `NO_SUITABLE_CANDIDATE`.
4. System lưu Decision Record:
   - Research State version;
   - candidate set;
   - selected candidate/outcome;
   - confidence/uncertainty;
   - reason codes;
   - provider/model/configuration;
   - downstream action.
5. System hiển thị decision.
6. Nếu policy cho phép auto-continue và decision high-confidence/low-risk:
   - selected candidate trở thành active direction.
7. Nếu human review required:
   - actor chọn Approve / Modify / Override / Reject.
8. System lưu human override nếu có.
9. Active hypothesis/direction được xác định.

## Alternative Flows

### A1 — Low Confidence / High Risk

System tạo review task; không auto-activate.

### A2 — No Suitable Candidate

Actor có thể:
- generate more candidates;
- modify research context;
- stop research.

### A3 — Decision Provider Unavailable

System áp dụng configured fallback:
- structured LLM provider;
- human review;
- fail-closed.

### A4 — Malformed Decision

System reject decision và không activate candidate.

## Postconditions

- selected hypothesis/direction có decision record;
- không candidate nào silently trở thành active.

## Includes

`<<include>> Evaluate Candidate Hypotheses`

## Extends

`Human Review <<extend>> UC-11 [low confidence / high risk / provider disagreement]`

---

# 18. UC-12 — Generate & Review Experiment Plan

## Goal

Chuyển selected hypothesis/direction thành structured executable experiment plan.

## Primary Actor

Researcher.

## Preconditions

- active dataset version;
- active Research Question;
- active selected hypothesis/direction;
- active Research State.

## Trigger

Actor chọn `Generate Experiment Plan` hoặc loop auto-continues by policy.

## Main Flow

1. System build planning context.
2. Generative Reasoner tạo structured plan:
   - objective;
   - variables;
   - candidate methods;
   - assumptions to check;
   - data requirements;
   - proposed steps;
   - expected outputs;
   - risks;
   - testing family;
   - success/stopping conditions.
3. System hiển thị plan.
4. Actor review.
5. Actor chọn:
   - Accept;
   - Request Revision;
   - Cancel.
6. Accepted plan chuyển `Ready`.

## Alternative Flows

### A1 — Insufficient Context

System yêu cầu clarification.

### A2 — Not Feasible

Plan = `Needs Review / Not Feasible`.

### A3 — Suspected Leakage / Unsupported Causality

System flag trước execution.

## Postconditions

Experiment Plan ở trạng thái `Ready` hoặc `Needs Review`.

---

# 19. UC-13 — Review Method Selection & Assumption Checks

## Goal

Chọn analytical/statistical method phù hợp dựa trên deterministic checks.

## Primary Actor

Researcher.

## Preconditions

Experiment Plan tồn tại.

## Trigger

Plan bước vào method-selection stage.

## Main Flow

1. System tạo candidate methods.
2. System xác định required assumptions cho từng method.
3. Analytical tools chạy deterministic assumption checks.
4. Mỗi check trả:
   - Pass;
   - Fail;
   - Warning;
   - Not Applicable.
5. System/agent so sánh candidate methods.
6. Selected method được lưu cùng rationale.
7. System hiển thị:
   - selected method;
   - why selected;
   - rejected alternatives;
   - assumption results;
   - risk/warnings.
8. Actor review.

## Alternative Flows

### A1 — Preferred Method Fails Assumption

System chọn/recommend alternative method.

### A2 — Multiple Valid Methods

System có thể đề xuất limited branching theo policy.

### A3 — No Valid Method

System yêu cầu re-plan hoặc clarification.

## Postconditions

Method Selection record tồn tại.

## Includes

`<<include>> Check Assumptions`

---

# 20. UC-14 — Execute Experiment

## Goal

Thực thi experiment trong isolated environment và tạo raw result.

## Primary Actor

Researcher.

## Preconditions

- Experiment Plan ready;
- method selected;
- required approvals complete.

## Trigger

Actor chọn `Run Experiment` hoặc approved auto-run policy bắt đầu execution.

## Main Flow

1. System tạo Execution Run.
2. Tool Router chọn required tool.
3. Code/query chạy trong Secure Sandbox.
4. Sandbox enforce:
   - isolation;
   - CPU/RAM/time limits;
   - network policy;
   - filesystem restrictions.
5. Sandbox trả:
   - raw output;
   - error;
   - artifacts;
   - resource/runtime metadata.
6. System lưu Execution Trace.
7. Nếu success, experiment chuyển `Validating`.

## Alternative Flows

### A1 — Syntax / Runtime Error

1. System classify `TECHNICAL_RETRY`.
2. Agent diagnose.
3. Retry/re-plan trong configured limit.
4. Trace giữ cả failed run và retry.

### A2 — Timeout

Sandbox terminate run.

### A3 — User Cancels

Experiment = `Cancelled`.

### A4 — Security Violation

Execution bị block và audit.

### A5 — Maximum Retry Reached

Experiment = `Failed / Needs Review`.

## Postconditions

Experiment có explicit success hoặc failure record.

## Includes

`<<include>> Secure Execution`  
`<<include>> Execution Trace`

## Extends

`Technical Retry / Re-plan <<extend>> UC-14 [execution failure]`

---

# 21. UC-15 — Review Deterministic Scientific Validation

## Goal

Xác minh scientific facts và validity checks trước evidence-sufficiency decision.

## Primary Actor

Researcher.

## Preconditions

Execution thành công.

## Trigger

Experiment chuyển `Validating`.

## Main Flow

1. Scientific Validator kiểm tra result integrity.
2. Re-check relevant assumptions.
3. Validate statistical result/test statistic khi applicable.
4. Calculate/report effect size khi applicable.
5. Calculate/report confidence interval khi applicable.
6. Check multiple-testing context/correction.
7. Check data leakage nếu predictive/ML workflow.
8. Check diagnostics/stability/reproducibility conditions.
9. Check unsupported causal language.
10. System tạo Scientific Validation Record.
11. Status:
    - Passed;
    - Passed with Warnings;
    - Needs Review;
    - Failed.
12. Actor xem validation summary.

## Alternative Flows

### A1 — Validation Failed but Recoverable

System route về experiment re-plan.

### A2 — Validation Failed and Not Recoverable

Result có thể được mark `Inconclusive`.

### A3 — Severe Assumption Violation

Human review required.

### A4 — Multiple Related Tests

Apply/justify correction.

### A5 — Possible Leakage

Result không được dùng làm official finding cho tới khi resolved.

## Postconditions

Deterministic scientific facts/checks tồn tại.

## Includes

`<<include>> Deterministic Scientific Validation`

## Extends

`Multiple-Testing Control <<extend>> UC-15 [multiple related tests]`  
`Data Leakage Check <<extend>> UC-15 [predictive / ML workflow]`

---

# 22. UC-16 — Review / Resolve Evidence Sufficiency Decision

## Goal

Quyết định validated experiment evidence đã đủ để tạo official finding hay cần scientific follow-up.

## Primary Actor

Researcher.

## Preconditions

- Scientific Validation Record tồn tại;
- required validation facts đã được tạo.

## Trigger

Deterministic validation hoàn tất.

## Main Flow

1. System gửi structured evidence + active Research State vào Evidence Sufficiency Gate.
2. Gate evaluate:
   - statistical evidence;
   - effect size / confidence interval;
   - assumptions;
   - consistency with prior findings;
   - evidence strength;
   - uncertainty;
   - replication history;
   - conflict state.
3. Gate trả một outcome:
   - `ENOUGH_EVIDENCE`;
   - `NEED_MORE_EVIDENCE`;
   - `TRY_ALTERNATIVE_METHOD`;
   - `REPLICATE`;
   - `NEED_HUMAN_REVIEW`;
   - `INCONCLUSIVE`.
4. System lưu Decision Record:
   - evidence references;
   - Research State version;
   - outcome;
   - confidence/uncertainty;
   - reason codes;
   - provider/model/configuration;
   - downstream action.
5. System hiển thị decision.
6. Nếu low-confidence/high-risk:
   - actor review/override.
7. System route:
   - `ENOUGH_EVIDENCE` → UC-18;
   - refinement outcomes → UC-17;
   - `NEED_HUMAN_REVIEW` → UC-17;
   - `INCONCLUSIVE` → record outcome and UC-20.

## Alternative Flows

### A1 — Provider Unavailable

Fallback/human review theo policy.

### A2 — Malformed Decision

Fail-safe; không tạo official finding.

### A3 — Human Override

Original decision + override reason đều được giữ.

## Postconditions

Mỗi validated experiment có explicit evidence-sufficiency decision.

## Includes

`<<include>> Evaluate Evidence Sufficiency`

## Extends

`Human Review <<extend>> UC-16 [low confidence / high risk / NEED_HUMAN_REVIEW]`

---

# 23. UC-17 — Resolve Scientific Refinement / Human Review

## Goal

Xử lý non-ENOUGH evidence outcomes mà không nhầm với technical retry.

## Primary Actor

Researcher.

## Preconditions

UC-16 trả một outcome khác `ENOUGH_EVIDENCE`.

## Trigger

Evidence Sufficiency Decision yêu cầu next action.

## Main Flow

1. System classify follow-up:
   - `SCIENTIFIC_REFINEMENT`;
   - `HUMAN_REVIEW`;
   - `INCONCLUSIVE`.
2. Với `NEED_MORE_EVIDENCE`:
   - LLM re-plan additional experiment.
3. Với `TRY_ALTERNATIVE_METHOD`:
   - LLM re-plan bằng valid alternative method.
4. Với `REPLICATE`:
   - system tạo replication experiment.
5. Với `NEED_HUMAN_REVIEW`:
   - system tạo review task.
6. Actor review proposed next action.
7. Actor chọn:
   - Approve;
   - Modify;
   - Reject;
   - Request Alternative;
   - Stop Research.
8. System kiểm tra experiment/time/cost budget.
9. Nếu continue:
   - quay lại UC-12/UC-13/UC-14 tùy outcome.
10. System lưu refinement lineage.

## Alternative Flows

### A1 — Budget Exceeded

System block auto-continue và yêu cầu explicit decision.

### A2 — Repeated Inconclusive

System đề xuất stopping review.

### A3 — Actor Rejects Refinement

Current evidence được giữ; research may stop.

## Postconditions

Scientific refinement có parent evidence rõ ràng hoặc research loop chuyển sang stop review.

---

# 24. UC-18 — Review Research Finding

## Goal

Chuyển evidence đủ điều kiện thành evidence-backed research finding.

## Primary Actors

Researcher / Reviewer.

## Preconditions

- Evidence Sufficiency Decision = `ENOUGH_EVIDENCE`; hoặc
- human-approved equivalent policy outcome.

## Trigger

System tạo Finding Candidate.

## Main Flow

1. System/agent tạo finding statement.
2. Finding chứa:
   - statement;
   - hypothesis;
   - experiment;
   - dataset version;
   - selected method;
   - deterministic validation;
   - evidence-sufficiency decision;
   - statistical result;
   - effect size/CI;
   - uncertainty;
   - warnings.
3. System check provenance completeness.
4. Actor review finding.
5. Finding status được đặt:
   - Validated;
   - Needs Review;
   - Rejected;
   - Conflicting Evidence;
   - Invalidated.
6. Validated finding được đưa vào updated Research State.

## Alternative Flows

### A1 — Missing Evidence / Broken Provenance

Finding không thể `Validated`.

### A2 — Unsupported Interpretation

System yêu cầu sửa statement.

### A3 — Causal Overclaim

System flag/rewrite language.

### A4 — Conflict with Prior Evidence

System giữ cả evidence và route tới UC-19.

## Postconditions

Finding link tới complete scientific/provenance chain.

## Includes

`<<include>> Check Provenance`

---

# 25. UC-19 — Review Dependency, Invalidation & Conflicting Evidence

## Goal

Đảm bảo research chain không che giấu dependency hoặc contradictory evidence.

## Primary Actor

Researcher.

## Secondary Actors

Project Manager / Reviewer có read access.

## Preconditions

Có multiple experiments/findings hoặc downstream hypothesis.

## Trigger

Actor mở Dependency Graph hoặc system phát hiện conflict/invalidation.

## Main Flow

1. System hiển thị graph:

```text
Research Question
↓
Research State
↓
Hypothesis
↓
Experiment
↓
Finding
↓
Next Hypothesis / Experiment
```

2. Actor inspect dependency edges.
3. Nếu upstream artifact bị invalidated/recomputed/replaced:
   - system identify descendants.
4. Downstream artifacts được mark `Needs Re-validation` khi cần.
5. Nếu evidence conflict:
   - system giữ tất cả results;
   - tạo Conflict Record;
   - không cherry-pick result thuận lợi.
6. Actor review recommended next action.
7. Actor có thể re-run/refine hoặc giữ conflict như limitation.

## Alternative Flows

### A1 — Re-run

New experiment/run được tạo; old history preserved.

### A2 — Conflict Cannot Be Resolved

Final report phải disclose conflict/limitation.

## Postconditions

Dependency/conflict/invalidation state được cập nhật.

## Extends

`Conflict Handling <<extend>> UC-18 [contradictory evidence]`

---

# 26. UC-20 — Continue or Stop Research Loop

## Goal

Quyết định có tiếp tục research iteration hay finalize.

## Primary Actor

Researcher.

## Preconditions

Có updated Research State sau finding, inconclusive outcome hoặc refinement review.

## Trigger

System đánh giá stopping criteria.

## Main Flow

1. System evaluate:
   - research question sufficiently answered;
   - meaningful new candidate còn tồn tại;
   - evidence convergence;
   - unresolved conflict;
   - repeated inconclusive outcomes;
   - max experiment count;
   - time/cost/step budget.
2. System đề xuất:
   - Continue;
   - Stop.
3. System hiển thị reason.
4. Actor confirm hoặc override nếu policy cho phép.
5. Nếu Continue:
   - system sang UC-10.
6. Nếu Stop:
   - loop status = `Completed`;
   - system cho phép UC-21.

## Alternative Flows

### A1 — Manual Stop

Actor dừng bất kỳ lúc nào; artifacts được giữ.

### A2 — Budget Exceeded

System stop/fail-safe theo policy.

### A3 — No Suitable Candidate

System đề xuất Stop hoặc ask-user.

## Postconditions

Research loop có explicit next action hoặc stop reason.

---

# 27. UC-21 — Generate Figures, Tables & Research Report

## Goal

Tạo official research outputs từ validated findings.

## Primary Actor

Researcher.

## Secondary Actor

Project Manager nếu được cấp generate-output permission.

## Preconditions

- có ít nhất một validated finding;
- output generation permission hợp lệ.

## Trigger

Actor chọn `Generate Output`.

## Main Flow

1. Actor chọn:
   - Figure;
   - Table;
   - Methodology Summary;
   - Research Report;
   - Reproducibility Package.
2. System chỉ lấy eligible/validated findings.
3. System lấy exact experiment/provenance/reproducibility metadata.
4. Agent/tool tạo output.
5. System lưu source linkage.
6. Actor review.
7. Actor save/export.

## Suggested Research Report Sections

```text
Research Question
Initial / Post-hoc Hypotheses
Dataset & Data Preparation
Research State / Iteration Summary
Methodology
Experiments
Scientific Validation
Evidence Sufficiency Decisions
Statistical Results
Research Findings
Conflicting Evidence
Figures / Tables
Limitations
Conclusion
Reproducibility Information
```

## Alternative Flows

### A1 — Preliminary / Inconclusive Result

Không được trình bày như validated finding; chỉ include nếu clearly labeled.

### A2 — Known Conflict

Conflict phải được disclose.

### A3 — Invalidated Finding

System exclude khỏi official conclusion.

## Postconditions

Output có provenance và links tới validated sources.

## Includes

`<<include>> Select Validated Findings`

---

# 28. UC-22 — View Research Outputs, Provenance, Evidence, Trace & Decision History

## Goal

Cho user audit research outputs và toàn bộ decision/execution chain.

## Primary Actors

Researcher / Reviewer.

## Secondary Actor

Project Manager.

## Preconditions

Có project artifacts.

## Trigger

Actor chọn `View Evidence`, `Trace`, `Decision History` hoặc mở report/finding.

## Main Flow

1. System hiển thị output/finding.
2. Actor mở provenance chain:

```text
Finding
↓
Evidence Sufficiency Decision
↓
Scientific Validation
↓
Statistical Result
↓
Experiment
↓
Method / Assumptions
↓
Execution
↓
Code / Query
↓
Dataset Version
↓
Dataset Lineage
```

3. Actor mở Decision History:
   - decision type;
   - Research State version;
   - candidates/evidence input;
   - outcome;
   - confidence/uncertainty;
   - reason codes;
   - provider/model/config;
   - downstream action;
   - human override.
4. Actor mở Execution Trace:
   - step;
   - tool;
   - input refs;
   - code/query;
   - raw output;
   - error;
   - technical retry;
   - scientific refinement;
   - latency;
   - usage/cost.
5. Actor navigate giữa linked artifacts.

## Alternative Flows

### A1 — Broken Provenance

Artifact/finding bị flag.

### A2 — Restricted Artifact

System enforce permission and redact if policy requires.

## Postconditions

Read-only audit; research state không bị thay đổi.

---

# 29. UC-23 — Run Benchmark & Evaluation

## Goal

Đánh giá AI Research Agent và decision-gated architecture bằng quantitative metrics.

## Primary Actors

Researcher / Project Manager / System Administrator.

## Preconditions

- benchmark tasks tồn tại;
- agent configuration tồn tại;
- scoring/rubric tồn tại.

## Trigger

Actor chọn `Run Evaluation`.

## Main Flow

1. Actor chọn benchmark/task set.
2. Actor chọn configuration(s).
3. Actor chọn repetitions N.
4. System execute benchmark.
5. Mỗi run lưu:
   - outputs;
   - execution trace;
   - decision records;
   - latency;
   - cost;
   - human escalation;
   - retry/refinement.
6. Evaluation Engine score:
   - task success;
   - result correctness;
   - method-selection accuracy;
   - assumption-check quality;
   - hypothesis-selection quality;
   - evidence-gate correctness;
   - false acceptance of insufficient evidence;
   - unnecessary continuation;
   - confidence/calibration quality;
   - provenance coverage;
   - reproducibility coverage.
7. System aggregate.
8. Actor compare configurations.

## Required / Recommended Ablations

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

## Alternative Flows

### A1 — Missing Ground Truth / Rubric

Metric requiring labels is marked unavailable rather than fabricated.

### A2 — Run Failure

Failure retained as evaluation result, not silently discarded.

## Postconditions

Evaluation result có raw run references và configuration metadata.

---

# 30. UC-24 — Manage Models, Decision Providers, Logs, Cost & System Configuration

## Goal

Vận hành platform và quản lý AI/decision infrastructure.

## Primary Actor

System Administrator.

## Preconditions

Admin authenticated.

## Trigger

Admin mở Admin Console.

## Main Flow

1. Admin quản lý:
   - users;
   - roles;
   - LLM/model configuration;
   - Structured Decision Provider configuration;
   - TypeSafe/Jev provider credentials/config nếu được sử dụng;
   - fallback provider/policy;
   - confidence thresholds;
   - system logs;
   - sandbox/tool failures;
   - usage;
   - token/cost;
   - benchmark config;
   - system health.
2. System validate config.
3. System version configuration khi cần reproducibility.
4. Changes được audit.
5. New configuration áp dụng theo rollout policy.

## Alternative Flows

### A1 — Invalid Model / Provider Configuration

System reject và giữ stable config.

### A2 — Provider Health Failure

System alert và áp dụng configured fallback policy.

### A3 — Unsafe Threshold

System warning hoặc block nếu vi phạm system safety policy.

## Postconditions

Operational configuration được cập nhật và auditable.

---

# 31. Key Include / Extend Relationships

## 31.1. `<<include>>`

```text
UC-04 Upload & Validate Dataset
    <<include>> Validate Dataset

UC-09 Review Research State
    <<include>> Build Research State

UC-11 Hypothesis Selection Decision
    <<include>> Evaluate Candidate Hypotheses

UC-13 Method Selection
    <<include>> Check Assumptions

UC-14 Execute Experiment
    <<include>> Secure Execution
    <<include>> Execution Trace

UC-15 Scientific Validation
    <<include>> Deterministic Scientific Validation

UC-16 Evidence Sufficiency
    <<include>> Evaluate Evidence Sufficiency

UC-18 Review Finding
    <<include>> Check Provenance

UC-21 Generate Research Outputs
    <<include>> Select Validated Findings
```

## 31.2. `<<extend>>`

```text
Human Approval
    <<extend>> UC-06
    [risky/destructive cleaning]

Human Review
    <<extend>> UC-11
    [low-confidence/high-risk hypothesis decision]

Technical Retry / Re-plan
    <<extend>> UC-14
    [execution failure]

Multiple-Testing Control
    <<extend>> UC-15
    [multiple related tests]

Data Leakage Check
    <<extend>> UC-15
    [predictive/ML workflow]

Human Review
    <<extend>> UC-16
    [low-confidence/high-risk evidence decision]

Scientific Refinement
    <<extend>> UC-16
    [NEED_MORE_EVIDENCE / TRY_ALTERNATIVE_METHOD / REPLICATE]

Conflict Handling
    <<extend>> UC-18
    [contradictory evidence]
```

---

# 32. Use Case Interaction Map

Đây là interaction map để đọc spec, **không phải UML Use Case flow arrow**:

```text
UC-01 Authenticate
    ↓
UC-02 Project
    ↓
UC-04 Upload Dataset
    ↓
UC-05 Profiling / Data Card
    ↓
UC-06 Cleaning / Versioning (optional)
    ↓
UC-07 Research Question
    ↓
UC-08 Initial H0/H1
    ↓
UC-09 Research State
    ↓
UC-10 Candidate Hypotheses
    ↓
UC-11 Hypothesis Selection Decision
    ↓
UC-12 Experiment Plan
    ↓
UC-13 Method + Assumptions
    ↓
UC-14 Execute Experiment
    ↓
UC-15 Deterministic Validation
    ↓
UC-16 Evidence Sufficiency Decision
    ├── ENOUGH_EVIDENCE → UC-18 Finding
    ├── NEED_MORE_EVIDENCE ─┐
    ├── ALTERNATIVE_METHOD  ├→ UC-17 Scientific Refinement
    ├── REPLICATE ──────────┘
    ├── NEED_HUMAN_REVIEW → UC-17
    └── INCONCLUSIVE → UC-20
                         ↓
                  UC-20 Continue / Stop
                    ├── Continue → UC-10
                    └── Stop → UC-21 Outputs
```

Supporting/audit use cases:

```text
UC-19 Dependency / Conflict
UC-22 Provenance / Trace / Decision History
UC-23 Evaluation
UC-24 Administration
```

---

# 33. Business Rules Affecting Use Cases

| Rule | Affected Use Cases |
|---|---|
| Raw dataset cannot be overwritten | UC-04, UC-06 |
| Risky cleaning requires human approval | UC-06 |
| Anomaly ≠ error | UC-05, UC-06 |
| Hypothesis ≠ fact | UC-08, UC-10, UC-18 |
| Post-hoc hypothesis must be labeled | UC-10, UC-11 |
| Candidate cannot silently become active | UC-11 |
| Association ≠ causation | UC-07, UC-15, UC-18, UC-21 |
| Method selection must be justified | UC-13 |
| Tools establish scientific facts | UC-13, UC-15 |
| Decision confidence ≠ scientific evidence | UC-11, UC-16 |
| Technical retry ≠ scientific refinement | UC-14, UC-17 |
| Official finding requires Evidence Sufficiency Decision | UC-16, UC-18 |
| Finding must have provenance/evidence | UC-18, UC-21, UC-22 |
| Multiple testing must be accounted for | UC-15 |
| Leakage guard required when applicable | UC-15 |
| Conflicting evidence must be preserved | UC-19, UC-21 |
| Upstream invalidation propagates | UC-19 |
| Official experiment requires reproducibility snapshot | UC-14, UC-15, UC-21 |
| Research loop has stopping criteria | UC-20 |
| Low-confidence/high-risk gate decisions follow escalation policy | UC-11, UC-16, UC-17 |
| Structured decision history must be retained | UC-11, UC-16, UC-22 |
| Provider fallback must fail safely | UC-11, UC-16, UC-24 |

---

# 34. BRD / PRD Traceability

| Use Case | Key BRD Requirements | PRD Module / Area |
|---|---|---|
| UC-01 | BR-01, BR-02 | Module A |
| UC-02 | BR-03 | Module B |
| UC-03 | BR-02, BR-03 | Module A/B |
| UC-04 | BR-04–BR-06 | Module C |
| UC-05 | BR-07 | Module D |
| UC-06 | BR-08–BR-12 | Module E |
| UC-07 | BR-13, BR-16 | Module F |
| UC-08 | BR-14, BR-15, BR-48 | Module G |
| UC-09 | BR-56 | Module AC |
| UC-10 | BR-57, BR-48 | Module AC |
| UC-11 | BR-58, BR-61, BR-62 | Module AD |
| UC-12 | BR-17 | Module H |
| UC-13 | BR-18–BR-20, BR-31 | Modules I/J |
| UC-14 | BR-22, BR-23, BR-35 | Module L / Trace |
| UC-15 | BR-24, BR-47, BR-49, BR-50, BR-54 | Modules M/N/O/P |
| UC-16 | BR-59, BR-61, BR-62 | Module AE |
| UC-17 | BR-60, BR-61 | Module AF |
| UC-18 | BR-26, BR-27, BR-34, BR-42 | Modules Q/X |
| UC-19 | BR-51, BR-52, BR-53 | Modules S/T |
| UC-20 | BR-30 | Module U |
| UC-21 | BR-32, BR-38–BR-41, BR-55 | Modules V/W/Z |
| UC-22 | BR-34–BR-37, BR-62 | Modules X/Y/AG |
| UC-23 | BR-43–BR-46, BR-63 | Modules AA/AG |
| UC-24 | BR-61–BR-63 + Administration | Module AG / Admin |

---

# 35. Canonical End-to-End Use Case Scenario

## Dataset

```text
student_id
score
ai_usage_rate
study_hours
attendance
major
...
```

## Research Question

> Is AI usage associated with student academic performance?

## Initial Hypotheses

```text
H0:
No statistically meaningful association exists
between AI usage rate and student score.

H1:
A statistically meaningful association exists.
```

## Scenario

```text
UC-04 Upload Dataset
↓
UC-05 Review Data Card
↓
UC-07 Define Research Question
↓
UC-08 Confirm H0/H1
↓
UC-09 Build / Review Research State
↓
UC-10 Generate Candidates

Candidate A:
Overall AI usage ↔ score association

Candidate B:
Association differs by major

Candidate C:
Adjusted association controlling study_hours

↓
UC-11 Hypothesis Selection Gate
SELECT Candidate A
↓
UC-12 Deep Experiment Plan
↓
UC-13 Assumptions + Method
↓
UC-14 Execute E1
↓
UC-15 Deterministic Validation
↓
UC-16 Evidence Gate

Example:
NEED_MORE_EVIDENCE
↓
UC-17 Scientific Refinement

Generate candidate H2 directions
↓
UC-10 / UC-11

Selected H2:
Association remains after controlling study_hours
Origin = Post-hoc / Exploratory
Status = Unverified

↓
UC-12 → UC-15
↓
UC-16

Example:
ENOUGH_EVIDENCE
↓
UC-18 Finding F2
↓
UC-20 Stopping Criteria
↓
UC-21 Final Research Outputs
```

Scenario phải chứng minh:

- exact Research State;
- candidate set;
- structured selection decision;
- confidence/uncertainty;
- deterministic method/assumption checks;
- technical retry vs scientific refinement;
- evidence-sufficiency decision;
- no unsupported causal claim;
- hypothesis origin;
- H→E→F lineage;
- provenance;
- reproducibility;
- human escalation khi cần.

---

# 36. Suggested Implementation Order

## Phase 1 — Core Research MVP

```text
UC-01
→ UC-02
→ UC-04
→ UC-05
→ UC-07
→ UC-08
→ UC-09
→ UC-12
→ UC-13
→ UC-14
→ UC-15
→ UC-16 (basic)
→ UC-18
→ UC-22
```

## Phase 2 — Decision-Gated Research Loop

```text
UC-10
→ UC-11
→ UC-17
→ UC-19
→ UC-20
```

## Phase 3 — Outputs & Reproducibility

```text
UC-21
```

## Phase 4 — Evaluation & Administration

```text
UC-23
→ UC-24
```

---

# 37. Use Case Acceptance at System Level

Use-case layer được xem là complete khi:

1. Mọi P0 use case có actor, trigger, preconditions, main flow, alternatives và postconditions.
2. External UML actors chỉ gồm Researcher, Project Manager, Reviewer và Administrator.
3. AI Agent, TypeSafe/Jev và Sandbox không được model như external actors.
4. Research State được version và có thể audit.
5. Candidate hypothesis không tự động trở thành active mà thiếu selection record/human choice.
6. Low-confidence/high-risk selection có human escalation.
7. Experiment execution có explicit technical retry path.
8. Deterministic validation hoàn tất trước Evidence Sufficiency Gate.
9. Official finding không bypass Evidence Sufficiency Decision.
10. `NEED_MORE_EVIDENCE`, `TRY_ALTERNATIVE_METHOD`, `REPLICATE` đi vào scientific refinement.
11. Technical retry và scientific refinement có trace category khác nhau.
12. `INCONCLUSIVE` được hỗ trợ như valid scientific outcome.
13. Every official finding có provenance đầy đủ.
14. Post-hoc hypothesis có origin/status rõ.
15. Conflicting evidence không bị silent discard.
16. Upstream invalidation ảnh hưởng downstream artifacts.
17. Research loop có explicit stopping criteria.
18. Official outputs chỉ dùng validated findings hoặc clearly labeled non-validated material.
19. Structured decision provider failure có safe fallback/fail-closed path.
20. Decision history giữ provider/configuration + human override.
21. Benchmark có thể đánh giá decision gates.
22. Structured Decision Gate có thể so sánh với LLM-only baseline khi benchmark cho phép.
23. Reviewer chỉ review/view, không được model là actor tạo experiment/report.
24. Use Case Specification trace được về BRD/PRD.

---

# 38. Relationship to Other Diagrams

```text
Use Case Specification
= Who wants to achieve what?

Use Case Diagram
= Which external actor is associated with which use case?

Overall Activity Diagram
= End-to-end research process runs how?

Experiment Activity Diagram
= One experiment is executed/validated how?

Hypothesis & Evidence Activity Diagram
= Structured gates route decisions how?

Sequence Diagram
= Components interact over time how?

SDD / Architecture
= Internal components implement the behavior how?
```

Use Case Diagram không nên dùng workflow arrows giữa numbered use cases.

---

# 39. Next Artifacts

```text
BRD Final v1.2
        ↓
PRD Final v1.0
        ↓
Use Case Specification Final v1.0
        ↓
Use Case Diagram Final
        ↓
Activity Diagrams Final
        ↓
Sequence Diagrams
        ↓
SDD / Architecture
        ↓
Database ERD
        ↓
API Contract
        ↓
UI Wireframes
        ↓
Test Cases
```

---

# 40. Document Change Log

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-09-19 | Initial use case specification based on BRD v1.0 / PRD v0.1 |
| 1.0 | 2026-09-20 | Rewritten and finalized for BRD v1.2 / PRD v1.0; added Research State, candidate hypotheses, structured Hypothesis Selection Gate, Evidence Sufficiency Gate, scientific refinement, confidence-based escalation, decision audit/provider fallback, TypeSafe/Jev as internal candidate provider, updated evaluation, traceability and actor modeling |
