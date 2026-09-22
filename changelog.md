# Changelog

Lịch sử thay đổi và registry của toàn bộ tài liệu canonical trong
`capstone-project-docs`. Các đường dẫn bên dưới là đường dẫn tương đối từ
repository root.

## 2026-09-22 — Refresh editable diagram package

### Changed

- Cập nhật các diagram editable Activity, Sequence và Use Case cùng các builder
  source-backed tương ứng.
- Thêm reference package GreenLens và các backup kỹ thuật đang nằm trong phạm
  vi staged; loại bỏ hai sequence artifact superseded.
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
- `greenlenslint.py --package --strict` — pass: 80 pages đúng family.
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

- [Business Requirements Document — BRD v1.2](AI-Research-Experimentation-Platform-BRD-FINAL-v1.2.md)
- [Product Requirements Document — PRD v1.0](AI-Research-Experimentation-Platform-PRD-FINAL-v1.0.md)
- [Use Case Specification — v1.0](AI-Research-Experimentation-Platform-Use-Case-Spec-FINAL-v1.0.md)

#### Flow và diagram reference

- [AI Research Experimentation Flows](AI-Research-Experimentation-Flows.png)
- [Activity — Main Flows](diagrams/activity-diagrams/AI-Research-Experimentation-Platform-Activity-Main-Flows.drawio)
- [Use Case — Platform](diagrams/usecase-diagrams/AI-Research-Experimentation-Platform-Use-Case.drawio)
- [Sequence — Main Flows](diagrams/sequence-diagrams/AI-Research-Experimentation-Platform-Main-Flows-Sequence.drawio)
- [GreenLens ERD reference](<diagrams/references/SEP492 GreenLens - ERD.drawio.xml>)

#### Source builder và project entry point

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
- Hai file builder là source-backed generator; khi flow hoặc quan hệ thay đổi,
  phải cập nhật builder và regenerate artifact tương ứng.
- Metadata nội bộ của Git và các file tạm của môi trường không thuộc
  documentation package canonical này.
