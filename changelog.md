# Changelog

Lịch sử thay đổi và registry của toàn bộ tài liệu canonical trong
`capstone-project-docs`. Các đường dẫn bên dưới là đường dẫn tương đối từ
repository root.

## 2026-09-28 — Đồng bộ BRD v1.9 / PRD v1.8 với kiến trúc đích Popper

### Changed

- Cập nhật [BRD](AI-Research-Experimentation-Platform-BRD-v1.8-DRAFT.md) lên v1.9 và [PRD](AI-Research-Experimentation-Platform-PRD-v1.7-DRAFT.md) lên v1.8 theo mục "Proposed BRD/PRD changes" và bảng mapping §7.10 của [architecture.md](architecture.md). Tên file giữ nguyên để không làm hỏng link và builder hiện có.
- Research loop: thay luồng tuyến tính single-path bằng agent loop trong giới hạn budget và invariant, giữ state machine cũ làm workflow floor (BR-80, PRD Module AJ, Section 38).
- Thêm exploration/confirmation split, Analysis Ledger, look budget, Research Protocol và confirmation batch (BR-79, PRD Module AI).
- Evidence Sufficiency Gate trở thành deterministic: Finding / Negative Result / Inconclusive tính trên adjusted interval so với δ_F / δ_N (BR-59, PRD Module AE). `NEED_MORE_EVIDENCE`, `TRY_ALTERNATIVE_METHOD` và `REPLICATE` chuyển thành next move (BR-60, Module AF); `NEED_HUMAN_REVIEW` chuyển thành escalation.
- Escalation dùng deterministic trigger làm mức sàn; confidence của decision layer chỉ được thêm escalation (BR-61, BRule-28).
- BR-78: các candidate ngang điểm cùng vào một confirmation batch trong look budget, không mở nhánh song song; bỏ `co_selected_with` và các cap cho nhánh song song, thêm quan hệ `registered_in`.
- Bỏ `run_python`/`run_sql`: experiment chỉ chạy qua registered capabilities (BR-22/23, PRD Module L).
- BR-21 được đổi thành triangulation / bounded robustness. BR-65 được đổi thành Prior-Work Assessment giới hạn theo coverage, không có nhãn `novel`. BR-48 dùng origin do hệ thống gán. Thêm BR-81 cho Research Program branches (Should).
- [architecture.md](architecture.md): sửa link BRD/PRD đang trỏ tới file `-REQ-TOOL.md` không tồn tại thành link tương đối tới file DRAFT; đổi đoạn "Proposed BRD/PRD changes" thành đã áp dụng, vẫn chờ supervisor sign-off.
- **Chưa đồng bộ diagram:** các builder Activity/Sequence/Use Case/Context vẫn mô tả outcome cũ (`ENOUGH_EVIDENCE`…) và luồng tuyến tính, nên cần cập nhật và regenerate trong một đợt riêng trước khi commit theo [AGENTS.md](AGENTS.md).
- Use Case Specification không có file canonical trong inventory nên không có gì để sửa.
- Lượt verify sau đó sửa thêm những chỗ còn mâu thuẫn với kiến trúc:
  - BR-07 / FR-PROFILE-04: quan hệ giữa hai biến chỉ được tính trên exploration partition.
  - BR-12 / FR-CLEAN-04: cleaning sau khi split là protocol deviation.
  - BR-41 / Module W: report hiển thị Negative Result và Inconclusive ngang Finding.
  - BR-42: checklist có thêm confirmation batch, severity checks và claim level.
  - BR-59 / Module AE: ghi rõ trường hợp two-sided và directional.
  - BRule-27 / PP-11: bỏ "re-plan" khỏi technical retry.
  - FR-EVAL-04: danh sách ablation khớp với BR-46.
  - FR-VIZ-02: figure chỉ được vẽ bằng registered chart capability.
- Lượt kiểm tra thứ ba:
  - Chuyển BR-78 từ section 11 (Business Rules) về section 10 (Business Requirements). Lỗi đặt sai vị trí này có từ v1.7.
  - BR-25: tách stability check trên cùng dữ liệu khỏi replication trên dữ liệu mới.
  - BR-16 / FR-RQ-01/02: thêm các trường của Research Brief, gap và intake (proceed / restate / clarify) trước khi đọc dữ liệu.
  - BR-44/45 / FR-EVAL-02 và Benchmark Task Structure: thêm null / planted-signal ground truth, false-finding rate và power.
  - FR-ADMIN-04: thêm run / policy / evaluation settings có policy version.
- Audit coverage toàn bộ architecture.md, đối chiếu từng section §4–§25 với BRD/PRD:
  - BRD thêm các BR mới:
    - BR-82 Research Knowledge Layer
    - BR-83 Research Artifacts & Visibility (Must)
    - BR-84 Publication Views & Integrity Audit (Must)
    - BR-85 Simulation Lab
    - BR-86 Theory & Observable Implications
    - BR-87 Research Campaign
  - BRD thêm BRule-39 (policy settings có version, không được làm yếu bảo đảm), GA-17/18, R-33→36 và acceptance criteria 59–63.
  - BRD mở rộng các BR đang có:
    - BR-27: yêu cầu cho từng claim type / evidential status
    - BR-34: reverse provenance
    - BR-40: limitation theo validity type
    - BR-49: dataset-scope looks
    - BR-55: replay vs re-derivation, tombstone
    - BR-56: tách các loại state
    - BR-58: screens, admission gate, circuit breaker
    - BR-63: champion/challenger
    - BR-80: role profiles, context
    - BRule-07: causal endorsement
    - NFR-02/07
  - PRD thêm Module AK (Artifacts & Publication Views), Module AL (Knowledge Layer), Module AM (Simulation Lab).
  - PRD thêm các FR: FR-STATE-06, FR-REFLOOP-06, FR-LOOP-09, FR-VALID-05/06, FR-PROV-04, FR-REPRO-04/05, FR-EVAL-06, FR-RQ-04.
  - PRD mở rộng NFR-02/03, acceptance criteria 61–66, entities, release plan và traceability.
- Thêm [PRD §53.1 Proposed Defaults](AI-Research-Experimentation-Platform-PRD-v1.7-DRAFT.md): bảng giá trị đề xuất cho các open decision 5–7 và 14–24, gồm α = 0.05, deciding interval Bonferroni 1 − α/L (Holm chỉ để báo cáo, FDR chỉ cho exploration), margin theo từng summary measure, bảng cỡ mẫu, δ_F/δ_N cho pack `general` và software engineering, split 50/50, look budget 5, mode và threshold của từng decision point ở A1, margin evaluation và danh sách capability MVP. BRD KPI-28 giờ trỏ tới α đề xuất. Tất cả đều đang chờ nhóm và supervisor duyệt.
- Kiểm tra lại phần định lượng của §53.1 (tính lại bằng power calculation):
  - Sửa Holm thành simultaneous interval Bonferroni cho quyết định sufficiency, vì Holm không cho ra simultaneous CI. BRD BR-49 và PRD FR-MTEST-02 được làm rõ theo.
  - Sửa số run evaluation từ 200 thành khoảng 655 mỗi arm cho margin 0.03; với margin 0.02 thì cần khoảng 1.470.
  - Thêm margin theo từng summary measure (d, r, β, OR, Cramér's V, η²) và bảng hướng dẫn cỡ mẫu.
- Kiểm tra tự động sau audit — pass:
  - BR/BRule đúng thứ tự và đúng section;
  - MoSCoW và traceability đầy đủ;
  - không có tham chiếu BR/BRule/BO/BP/GA/KPI/R/NFR/FR/Module tới ID không tồn tại;
  - không có FR trùng;
  - acceptance criteria PRD liên tục 1–66;
  - code fence cân bằng;
  - `git diff --check` sạch.

### Validation

- `git diff --check` — pass.
- Kiểm tra local link trong BRD, PRD, architecture.md và entry này — pass. Riêng [architecture.md](architecture.md) còn tham chiếu `research-methodology.md` và `roadmap.md`, hai file chưa có trong repository; lỗi này có sẵn từ trước và nằm ngoài phạm vi lần sửa này. Entry ngày 2026-09-24 bên dưới cũng đang link tới hai file `-REQ-TOOL.md`, vốn đã bị xoá khỏi working tree trước khi task này bắt đầu.
- Chưa chạy diagram generator/validator vì chưa sửa diagram.

### References

- [Target architecture](architecture.md)
- [BRD v1.9 Draft](AI-Research-Experimentation-Platform-BRD-v1.8-DRAFT.md)
- [PRD v1.8 Draft](AI-Research-Experimentation-Platform-PRD-v1.7-DRAFT.md)

## 2026-09-24 — Chuẩn hóa tài liệu REQ-TOOL và cập nhật package diagram

### Changed

- Thêm bản chuẩn hóa BRD v1.8 và PRD v1.7 theo định dạng REQ-TOOL; giữ nguyên hai file DRAFT nguồn.
- Cập nhật Use Case diagram editable cùng Activity và Sequence artifacts/builders theo các entry đồng bộ BRD/PRD ở dưới; trạng thái cuối có thay đổi Use Case diagram.
- Backup Context draw.io là artifact kỹ thuật, không phải nguồn nội dung.
- Giữ Context model và builder là nguồn cho Context DFD Level 0.

### Validation

- Chưa chạy validation diagram trong lượt cập nhật changelog này; kết quả validation của từng diagram được ghi tại entry tương ứng bên dưới.
- `git diff --check` — pass.

### References

- [BRD v1.8 Draft](AI-Research-Experimentation-Platform-BRD-v1.8-DRAFT.md) và [bản REQ-TOOL](AI-Research-Experimentation-Platform-BRD-v1.8-REQ-TOOL.md)
- [PRD v1.7 Draft](AI-Research-Experimentation-Platform-PRD-v1.7-DRAFT.md) và [bản REQ-TOOL](AI-Research-Experimentation-Platform-PRD-v1.7-REQ-TOOL.md)
- [Context — DFD Level 0](diagrams/context-diagrams/AI-Research-Experimentation-Platform-Context.drawio)
- [Activity — Main Flows](diagrams/activity-diagrams/AI-Research-Experimentation-Platform-Activity-Main-Flows.drawio)
- [Sequence — Main Flows](diagrams/sequence-diagrams/AI-Research-Experimentation-Platform-Main-Flows-Sequence.drawio)
- [Use Case — Platform](diagrams/usecase-diagrams/AI-Research-Experimentation-Platform-Use-Case.drawio)

## 2026-09-22 — Hoàn thiện 30 Sequence UC và chỉnh Activity theo BRD/PRD mới

### Changed

- Cập nhật [Activity — Main Flows](diagrams/activity-diagrams/AI-Research-Experimentation-Platform-Activity-Main-Flows.drawio) và [Activity builder](diagrams/activity-diagrams/update_activity_diagram.py): sửa thứ tự Hypothesis Selection Gate, đưa novelty về đúng lane, chuyển method-cap sang Experiment Planner / AI Agent, giới hạn reviewer override ở Researcher, cập nhật ownership của Evaluation và thêm nhánh Approved / Rejected–Revise–Automated Review cho Final Outputs & Manuscript.
- Cập nhật [Sequence — Main Flows](diagrams/sequence-diagrams/AI-Research-Experimentation-Platform-Main-Flows-Sequence.drawio) và [Sequence builder](diagrams/sequence-diagrams/build_sequence_diagrams.py) từ 24 lên đủ 30 trang UC. UC-25–UC-30 là các capability group đang có trong Use Case package: Research Definition, Hypotheses, Experiments, Research Findings, Research Outputs và System Administration.
- Sửa UC-10 để novelty có outer `opt [Novelty feature enabled]` và nhánh `SOURCE / NOT ASSESSED`; sửa UC-11 để human review là optional, cho phép high-confidence auto-continue.
- Không sửa Use Case diagram đang có trong worktree; không thay đổi nội dung BRD/PRD vì các requirement đã là source input của lần đồng bộ này.

### Validation

- `python -B -m py_compile` cho hai builder — pass.
- Sequence builder — pass: sinh đúng 30 pages, UC-01..UC-30 liên tục và unique.
- `activitylint.py --strict` — pass: 0 error, 0 warning.
- Activity `validate.py --strict --score` — pass: 0 error, 0 warning, score 0.
- Sequence `validate.py --strict --score` — pass: 0 error, 0 warning, score 0.
- Sequence semantic QA — pass: 30 pages; 0 actor-to-non-boundary message, 0 actor return source lỗi, 0 fragment parent reference lỗi.
- Draw.io 31.4.5 render check — pass trên các trang Activity 3/8/10/11 và Sequence 1/10/11/21/25–30.
- `git diff --check` — pass.

### References

- [BRD v1.8 Draft](AI-Research-Experimentation-Platform-BRD-v1.8-DRAFT.md)
- [PRD v1.7 Draft](AI-Research-Experimentation-Platform-PRD-v1.7-DRAFT.md)

## 2026-09-23 — Hoàn thiện System Context theo DFD Level 0

### Added

- Thêm [Context — DFD Level 0](diagrams/context-diagrams/AI-Research-Experimentation-Platform-Context.drawio) dạng `.drawio` editable cho AI Research Experimentation Platform.
- Thêm [context model](diagrams/context-diagrams/context_diagram.json) và [context builder](diagrams/context-diagrams/build_context_diagram.py), mô tả sáu external entity, một process trung tâm và 25 labeled data flow cấp cao theo BRD/PRD.
- Sắp xếp lại layout theo reference: Researcher ở trên, Project Manager/System Administrator bên trái, provider bên phải và Reviewer bên dưới; nới corridor để 25 connector không chồng nhau.
- Đặt từng flow label sát đúng làn mũi tên, rút gọn nhãn dài và tăng cỡ chữ để đọc được ở bản render.
- Loại các module nội bộ và Secure Sandbox khỏi external boundary; giữ AI/LLM Provider và Structured Decision Provider ở mức abstraction, không khóa vào vendor cụ thể.
- Không chỉnh sửa Use Case, Activity hoặc Sequence trong task này; các thay đổi sẵn có khác trong worktree được giữ nguyên.

### Validation

- Context builder — pass; builder dùng deterministic DFD Level 0 layout từ cùng model nguồn, không phụ thuộc Graphviz.
- Context `validate.py --strict --score` — pass: 0 error, 0 warning, score 0.
- Draw.io 31.4.5 render check — pass; artifact đã render thành PNG draft và được kiểm tra trực quan.
- `git diff --check` — pass.

### References

- [BRD v1.8 Draft](AI-Research-Experimentation-Platform-BRD-v1.8-DRAFT.md)
- [PRD v1.7 Draft](AI-Research-Experimentation-Platform-PRD-v1.7-DRAFT.md)

## 2026-09-22 — Đồng bộ Activity và Sequence với BRD v1.8 / PRD v1.7

### Changed

- Đồng bộ [Activity — Main Flows](diagrams/activity-diagrams/AI-Research-Experimentation-Platform-Activity-Main-Flows.drawio) và [Activity builder](diagrams/activity-diagrams/update_activity_diagram.py) với BR-64/65/73-75/78: Structured Idea Record/Reflection, optional novelty assessment, bounded tied candidates, immutable branch snapshots, sibling join, shared testing family, provenance/evaluation metadata và Final Outputs & Manuscript page.
- Đồng bộ [Sequence — Main Flows](diagrams/sequence-diagrams/AI-Research-Experimentation-Platform-Main-Flows-Sequence.drawio) và [Sequence builder](diagrams/sequence-diagrams/build_sequence_diagrams.py) cho UC-10–UC-16, UC-18–UC-24; giữ 24 pages và không thêm tree-search flow.
- Giữ nguyên [Use Case — Platform](diagrams/usecase-diagrams/AI-Research-Experimentation-Platform-Use-Case.drawio) theo đúng scope yêu cầu; BRD/PRD không cần sửa vì đã là source input của lần đồng bộ này.

### Validation

- `activitylint.py --strict` — pass: 0 error, 0 warning.
- Activity `validate.py --strict --score` — pass: 0 error, 0 warning, score 0.
- Sequence `validate.py --strict --score` — pass: 0 error, 0 warning, score 0.
- Sequence semantic QA — pass: 24 pages; không có actor-to-non-boundary message, actor return source lỗi hoặc fragment parent reference lỗi.
- Draw.io 31.4.5 render check — pass: 11 Activity pages và 24 Sequence pages đã render thành công để kiểm tra layout.
- Use Case SHA256 giữ nguyên so với trước khi thực hiện task.
- `git diff --check` — pass.

### References

- [BRD v1.8 Draft](AI-Research-Experimentation-Platform-BRD-v1.8-DRAFT.md)
- [PRD v1.7 Draft](AI-Research-Experimentation-Platform-PRD-v1.7-DRAFT.md)

## 2026-09-22 — Refresh editable diagram package

### Changed

- Cập nhật các diagram editable Activity, Sequence và Use Case cùng các builder
  source-backed tương ứng.
- Thêm các backup kỹ thuật đang nằm trong phạm vi staged; loại bỏ hai sequence artifact superseded.
- Không thay đổi BRD, PRD hoặc Use Case Spec vì đợt này không thay đổi
  requirement nghiệp vụ.

### Validation

- `activitylint.py --strict` — pass: 0 error, 0 warning.
- Activity `validate.py --strict --score` — 0 error, 1 cảnh báo crossing,
  score 10.
- Main Sequence `validate.py --strict --score` — pass: 0 error, 0 warning,
  score 0.
- Use Case `validate.py --strict --score` — 0 error, 56 cảnh báo geometry của
  system boundary/nested layout, score 355; giữ nguyên theo phạm vi yêu cầu.
- `git diff --cached --check` — pass trước khi commit.

## 2026-09-22 — Local tooling cleanup

### Removed

- Xoá metadata và worktree local của các công cụ agent không còn dùng.
- Loại bỏ các rule/reference tương ứng khỏi `AGENTS.md` và registry này.

### Validation

- Không có tài liệu canonical hoặc diagram editable nào bị xoá.
- Local links và cross-references được kiểm tra lại sau khi cleanup.

## 2026-09-22 — Documentation governance

### Added

- Thêm [`AGENTS.md`](AGENTS.md) với documentation-first gate: agent phải cập
  nhật tài liệu và changelog trước khi bắt đầu commit hoặc PR.
- Thêm registry này để liên kết tập trung tới toàn bộ tài liệu, flow reference,
  diagram editable và source builder.

### Validation

- Kiểm tra toàn bộ local link trong `changelog.md` và `AGENTS.md` — pass.
- `git diff --check` — clean.

### Scope note

- Task này chỉ thêm documentation governance và registry; không regenerate hoặc
  chỉnh sửa nội dung diagram.
- Các thay đổi diagram/source đang được stage từ trước được giữ nguyên, không
  gộp thêm thay đổi không liên quan.

### Current documentation package

#### Tài liệu nguồn

- [Business Requirements Document — BRD v1.8 Draft](AI-Research-Experimentation-Platform-BRD-v1.8-DRAFT.md)
- [Product Requirements Document — PRD v1.7 Draft](AI-Research-Experimentation-Platform-PRD-v1.7-DRAFT.md)
- Use Case Specification không có file canonical trong inventory hiện tại; Use Case diagram được giữ nguyên theo scope task.

#### Flow và diagram reference

- [Context — DFD Level 0](diagrams/context-diagrams/AI-Research-Experimentation-Platform-Context.drawio)
- [Activity — Main Flows](diagrams/activity-diagrams/AI-Research-Experimentation-Platform-Activity-Main-Flows.drawio)
- [Use Case — Platform](diagrams/usecase-diagrams/AI-Research-Experimentation-Platform-Use-Case.drawio)
- [Sequence — Main Flows](diagrams/sequence-diagrams/AI-Research-Experimentation-Platform-Main-Flows-Sequence.drawio)

#### Source builder và project entry point

- [Context model](diagrams/context-diagrams/context_diagram.json)
- [Context diagram builder](diagrams/context-diagrams/build_context_diagram.py)
- [Use Case diagram builder](diagrams/usecase-diagrams/build_usecase_diagram.py)
- [Sequence diagram builder](diagrams/sequence-diagrams/build_sequence_diagrams.py)
- [Repository README](README.md)
- [Agent rules](AGENTS.md)

#### Auxiliary artifact

- [Use Case diagram backup](<diagrams/usecase-diagrams/.$AI-Research-Experimentation-Platform-Use-Case.drawio.bkp>) — bản backup kỹ thuật, không phải source of truth.

## Quy ước registry

- BRD, PRD và Use Case Spec là nguồn nội dung nghiệp vụ/chức năng.
- PNG là flow reference trực quan; các file `.drawio`/`.xml` là artifact
  editable cần được giữ nguyên khả năng chỉnh sửa.
- Các file builder là source-backed generator; khi flow hoặc quan hệ thay đổi,
  phải cập nhật builder và regenerate artifact tương ứng.
- Metadata nội bộ của Git và các file tạm của môi trường không thuộc
  documentation package canonical này.
