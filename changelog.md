# Changelog

Lịch sử thay đổi và registry của toàn bộ tài liệu canonical trong
`capstone-project-docs`. Các đường dẫn bên dưới là đường dẫn tương đối từ
repository root.

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
