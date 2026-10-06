# Research run event stream — contract giữa Platform BE và FE

Trạng thái: **DRAFT**, FE đang chạy bằng mock theo đúng contract này.
Hướng dẫn triển khai cho luồng topic → hypothesis: [Platform BE handoff](be-handoff-topic-to-hypothesis.md) (API cho FE, SSE, gate, pacer, lưu trữ) và [Engine handoff](engine-handoff-topic-to-hypothesis.md) (repo lõi chạy stage 1–8, danh mục event chi tiết).
Nguồn sự thật về kiểu dữ liệu: [`src/lib/run-stream/contract.ts`](../ai-research-platform-fe/src/lib/run-stream/contract.ts) trong repo FE.

## 1. Mục đích

Workspace của một research run hiển thị từng việc Popper đang làm: agent nào đang làm, ở stage và step nào, kết quả trung gian, và những điểm dừng chờ người dùng quyết định. FE dựng toàn bộ giao diện đó từ **một chuỗi event có thứ tự**. Reducer phía FE (`applyRunEvent`) gộp từng event vào state, nên:

- Mock và BE thật phải phát **cùng shape event**. Đổi nguồn không phải sửa UI.
- Mọi thứ hiển thị phải suy ra được từ event. FE không tự bịa tiến trình.
- Phát lại từ đầu, hoặc từ một `seq` bất kỳ, phải cho ra cùng state.

Hiện BE chỉ có `research_runs.status` (6 giá trị), một dòng message, `frame_reviews` và `run_artifacts`. Tài liệu này mô tả phần cần bổ sung.

## 2. Endpoint

| Method | Path | Mục đích |
|---|---|---|
| `GET` | `/api/v1/projects/{projectId}/runs/{runId}/events/stream` | Server-Sent Events. Mỗi SSE `id` = `seq`. Nối lại bằng header `Last-Event-ID` hoặc query `after`. |
| `GET` | `/api/v1/projects/{projectId}/runs/{runId}/events?after={seq}&limit=` | Lấy lại event đã lưu dạng JSON (phân trang), dùng khi mở lại workspace. |
| `POST` | `/api/v1/projects/{projectId}/runs/{runId}/gates/{gateId}` | Trả lời một điểm dừng. Body là `GateAnswer`. |
| `POST` | `/api/v1/projects/{projectId}/runs/{runId}/pause` | Tạm dừng. BE phát `run.status` = `paused`. |
| `POST` | `/api/v1/projects/{projectId}/runs/{runId}/resume` | Chạy tiếp. BE phát `run.status` = `running` hoặc `awaiting_review`. |
| `POST` | `/api/v1/projects/{projectId}/runs` | Đã có. Đề xuất body mới: `topic` (câu hỏi người dùng gõ, thay cho `research_context_version`), `domains[]` (lĩnh vực người dùng giữ lại, tương ứng `research.domains`), `dataset_version_id`, và `review_mode: "auto" \| "light" \| "copilot" \| "full"` thay cho `auto_review: boolean`. Sub-question không gửi lên: Popper tự sinh ở stage 2. |

Quy tắc SSE:

- Mỗi message SSE có `event: run-event`, `id: <seq>`, `data: <RunEvent JSON>`.
- Gửi comment `: keep-alive` khoảng mỗi 15 giây.
- Event phải được lưu bền (append-only) trước khi gửi, để `Last-Event-ID` phát lại được đúng.
- Lỗi xác thực và quyền dùng format lỗi hiện có của API (`success`, `message`, `error.code`).

## 3. Envelope

```ts
{
  seq: number;          // tăng nghiêm ngặt theo từng run, bắt đầu từ 1
  run_id: string;
  ts: string;           // ISO 8601, thời điểm BE ghi event
  type: string;         // xem mục 5
  stage_key?: string;   // stage mà event thuộc về; event nội dung bắt buộc có
  actor?: AgentRole;    // steward | strategist | librarian | theorist | methodologist | skeptic | pi | interpreter | reporter | code
  payload: object;
}
```

- FE bỏ qua event có `seq` ≤ `seq` đã áp dụng, nên gửi trùng là an toàn.
- `actor: "code"` dùng cho các bước kiểm tra không có AI (copy kết quả, kiểm số, typeset).

## 4. Stage, round và review mode

Thứ tự stage: `data` → `scope` → `search` → `screen` → `read` → `synthesize` → [`hypothesize` → `experiment` → `interpret`] × số round → `report` → `write`.

- `stage_key` có dạng `data`, `scope`, `search`, `screen`, `read`, `synthesize`, `r{n}-hypothesize`, `r{n}-experiment`, `r{n}-interpret`, `report`, `write`.
- Ánh xạ với pipeline stage 1–9 của Popper (xem [`pipeline_stage_1_to_8_guide.md`](../ai-research-platform-fe/docs/pipeline_stage_1_to_8_guide.md)):

  | `stage` | Pipeline stage | Agent chính | File |
  |---|---|---|---|
  | `scope` | 1 TOPIC_INIT, 2 PROBLEM_DECOMPOSE | strategist, pi | `stage-01/goal.md`, `stage-02/problem_tree.md`, `stage-02/topic_evaluation.json` |
  | `search` | 3 SEARCH_STRATEGY, 4 LITERATURE_COLLECT | librarian | `stage-03/search_plan.yaml`, `stage-04/candidates.jsonl` |
  | `screen` | 5 LITERATURE_SCREEN (HITL) | librarian | `stage-05/shortlist.jsonl` |
  | `read` | 6 KNOWLEDGE_EXTRACT | librarian | `stage-06/cards/` |
  | `synthesize` | 7 SYNTHESIS | theorist | `stage-07/synthesis.md` |
  | `hypothesize` | 8 HYPOTHESIS_GEN | theorist, methodologist, skeptic, librarian, pi | `stage-08/perspectives/`, `hypotheses.md`, `novelty_report.json` |
  | `experiment` | 9 EXPERIMENT_DESIGN trở đi | methodologist, skeptic | `stage-09/exp_plan.yaml`, … |

  `PlannedStage.pipeline` (mảng số stage) và `StagePlanStep.pipeline_stage`, `StagePlanStep.artifact` là tuỳ chọn, để FE hiện "Stage 03–04" và thứ mỗi step viết ra. `artifact` là **tên cho người dùng đọc** ("Research goal", "Shortlist", "Gap map"), không phải đường dẫn file; đường dẫn trong run folder ở cột bên trên chỉ nằm ở BE.
- `StagePlan.reads` (tuỳ chọn, mảng tên cho người dùng đọc) liệt kê những gì stage dựa vào, từ stage trước hoặc từ input ("Your topic", "Sub-question tree", "Knowledge cards"). FE ghép `reads` với `artifact` của các step thành dải "Builds on → Writes" ở đầu mỗi stage.
- Round 2 kiểu `pivot` chỉ chạy lại `hypothesize` (stage 8) dựa trên gap đã có; không tìm tài liệu lại.
- Round có `round_kind`: `first`, `pivot` (đi hướng mới, có Hypothesize) hoặc `refine` (chạy lại cùng tập hypothesis, không có Hypothesize).
- Quyết định đi lại (`refine`, `pivot`) tối đa 2 lần mỗi run.
- Mỗi khi kế hoạch đổi (bắt đầu run, hoặc sau `decision.committed`), BE phát `run.plan` với **toàn bộ** danh sách stage, kể cả stage đã xong và chưa tới. FE dùng nó để vẽ thanh tiến trình và báo trước điểm dừng.

Điểm dừng theo review mode:

| Mode | Gate |
|---|---|
| `auto` | không có; PI tự quyết và quyết định vẫn được ghi lại |
| `light` | `publish` |
| `copilot` | `screen`, `hypotheses`, `decision`, `publish` |
| `full` | `scope`, `screen`, `hypotheses`, `decision`, `report`, `publish` |

Gate nằm ở step cuối của stage tương ứng: `scope` ở `scope`, `screen` ở `screen`, `hypotheses` ở `hypothesize`, `decision` ở `interpret`, `report` ở `report`, `publish` ở `write`.

## 5. Danh mục event

### 5.1 Khung chạy

| `type` | Payload | Khi nào |
|---|---|---|
| `run.started` | `mode`, `topic`, `domains[]`, `dataset? {name, version, rows, columns}` | Event đầu tiên; `topic` là đầu vào của stage 1; không có `dataset` khi run chỉ đi từ topic |
| `run.plan` | `stages: PlannedStage[]` (`key`, `stage`, `round?`, `round_kind?`, `title`, `has_gate`) | Đầu run và mỗi khi kế hoạch đổi |
| `run.status` | `status: running \| paused \| awaiting_review \| completed \| failed`, `reason?` | Khi trạng thái đổi |
| `run.completed` | `paper_title?` | Sau khi paper được duyệt publish; nếu run kết thúc ở stage 8 (sau khi chọn hypothesis) thì không có `paper_title` |
| `stage.started` | `plan: StagePlan` (thêm `purpose`, `cast`, `steps[]`) | Mở stage; `steps` đã gồm step gate theo mode |
| `stage.completed` | `summary` (một câu) | Đóng stage |
| `step.started` / `step.completed` | `step_id` | Mỗi step trong `plan.steps` |
| `agent.message` | `message_id`, `delta`, `done?` | Lời agent tường thuật, stream theo đoạn; các `delta` cùng `message_id` được nối lại |
| `rule.checked` | `rule: 1..6`, `state: pass \| hit`, `detail?` | Khi một luật được kiểm tra hoặc chặn một việc |
| `skills.loaded` | `skills[{id, name, category: domain \| experiment \| tooling \| writing, matched[]}]` | Ngay sau `stage.started`, khi SkillMatcher đã chọn skill cho stage; `matched` là từ khoá khớp |

Sáu luật: 1 mọi con số trong paper lấy từ `results.json`; 2 mọi phân tích báo đúng con số plan đã hứa; 3 data version và record không bao giờ bị ghi đè; 4 test plan được khoá trước khi chạy code; 5 mọi hypothesis phải nói rõ kết quả nào sẽ bác bỏ nó; 6 con số agent nhớ ra (ước tính SOTA) giữ trạng thái chưa kiểm chứng cho tới khi có bài báo xác nhận.

### 5.2 Check the data

| `type` | Payload |
|---|---|
| `data.sample` | `file`, `columns[{name, type, unit}]`, `rows: string[][]` (mẫu, ~40 dòng), `total_rows` |
| `data.column_profiled` | `column`, `clean_share` (0–100) |
| `data.issue_found` | `issue {id, title, detail, column, affected_rows, tone: error \| warning, share, cells[{row, column}], rows[]}`; `row` là chỉ số dòng trong mẫu |
| `data.issue_fixed` | `issue_id`, `fix`, `method`, `replacements[{row, column, value}]`, `removed_rows[]` |
| `data.version_created` | `version`, `rows`, `removed`, `fixes`, `sha256` |

### 5.3 Scope (stage 1–2)

| `type` | Payload |
|---|---|
| `scope.profile` | `domains[]`, `compute {label, detail}` (kết quả `detect_hardware`) |
| `scope.goal` | `field: title \| problem \| objective \| scope \| success`, `label`, `value`; gửi lại cùng `field` sẽ thay giá trị |
| `scope.estimate` | `estimate {id, text}`: con số nhớ ra, mặc định chưa kiểm chứng (luật 6) |
| `scope.adjusted` | `field`, `from`, `to`, `reason`: thu hẹp phạm vi theo dữ liệu hoặc phần cứng |
| `scope.approved` | `at` (ISO 8601 UTC), `note`: PI duyệt goal và lưu lại; phải đến trước `problem.subquestion` đầu tiên (decision của stage 1) |
| `problem.subquestion` | `sub_question {id, text, tests, priority, covers[]}`; `covers` là cụm từ trích nguyên văn từ câu hỏi, để FE đánh dấu phần đã được bao phủ (MECE) |
| `problem.risk` | `risk {id, sq_id, text, level: low \| medium \| high}` |
| `topic.evaluated` | `scores {novelty, specificity, feasibility}` (0–10), `overall`, `threshold` (5), `advice` |

### 5.4 Search (stage 3–4)

| `type` | Payload |
|---|---|
| `search.strategy` | `strategy {id, title, why}` |
| `search.query` | `query {id, strategy_id, text}` (3–6 từ) |
| `search.sources` | `sources[{id, name}]`, `delay_ms` (khoảng cách giữa các request) |
| `literature.request` | `query_id`, `source_id`: request vừa gửi |
| `literature.batch` | `query_id`, `source_id`, `hits` |
| `literature.merged` | `title`, `records[{source, record_id, citations, has_doi}]`, `kept`: một bài tìm thấy ở nhiều nguồn; `kept` là nguồn có bản ghi được giữ, ưu tiên có DOI rồi nhiều trích dẫn nhất |
| `literature.collected` | `raw`, `unique`, `duplicates`, `files[{name, detail}]`, `collected_at` (ISO 8601 UTC) |

### 5.5 Screen (stage 5)

| `type` | Payload |
|---|---|
| `screen.criteria` | `rules[]`, `relevance_min`, `quality_min` |
| `screen.scored` | `points[{id, relevance, quality}]` (0–1), gửi theo lô |
| `screen.rejected` | `paper {id, title, venue, false_friend, reason}`: trùng từ khoá nhưng sai lĩnh vực |
| `screen.kept` | `paper {id, citation, title, venue, year, relevance, quality, reason, doi?, seminal?, source, citations}`; `source` và `citations` là nguồn gốc của bản ghi được giữ ở stage 4 |

Gate `screen` có `droppable` là id các bài trong shortlist; `answer.dropped` là id bài bị bỏ. Bài bị bỏ không được đọc ở stage 6 và không được trích dẫn.

### 5.6 Read (stage 6)

`card.extracted` (`card {id, paper_id, citation, problem, method, data, metrics, findings, limitations}`), `estimate.checked` (`check {estimate_id, status: verified | unsupported, source?, note}`; sau đó `rule.checked` luật 6 `pass`).

### 5.7 Synthesize (stage 7)

`synthesis.cluster` (`cluster {id, title, claim, card_ids[]}`), `synthesis.tension` (`tension {between: [clusterId, clusterId], text}`), `synthesis.gap` (`gap {id, text, from: card_ids[]}`), `synthesis.overview` (`text`: một đoạn tổng quan toàn cảnh, gửi sau khi gom cụm), `synthesis.ranked` (`ranking[{gap_id, priority, text}]`: gap xếp thành cơ hội nghiên cứu, `priority` 1 làm trước).

### 5.8 Hypothesize (stage 8)

| `type` | Payload |
|---|---|
| `debate.turn` | `turn {id, actor, stance: propose \| test \| challenge \| refine \| concede, text, reply_to?, about?}`; `actor` của envelope trùng `turn.actor` |
| `hypothesis.drafted` | `hypothesis` đủ 4 phần (xem dưới) |
| `hypothesis.checked` | `hypothesis_id`, `novelty {novel, closest, similarity}`, `feasibility {ok, note}` |
| `hypothesis.selected` | `hypothesis_id`, `override_note?` |
| `idea.set_aside` | `idea_id`, `statement`, `reason` |

`Hypothesis`: `id`, `statement`, `short`, `prediction`, `outcome`, `exposure`, `estimand`, `method`, `report_key`, `sub_question`, `gap`, `novelty`, `rationale`, `falsify {text, zone: [lo | null, hi | null], unit}`. `zone` là vùng mà khoảng tin cậy 95% không được chạm vào; `null` là đầu mở, hai đầu bằng nhau là một giá trị (ví dụ 0). Sau khi drafted đủ, BE phát `rule.checked` luật 5 `pass`.

### 5.9 Experiment (stage 9 trở đi)

| `type` | Payload |
|---|---|
| `plan.locked` | `plan_id`, `hypotheses[]`, `design {independent[], dependent[], controls[]}`; step đầu tiên của stage, trước mọi `node.created`, kèm `rule.checked` luật 4 |
| `experiment.hypotheses` | `hypotheses[]` được test trong round này |
| `node.created` | `node {id, hypothesis_id, version, parent_id, kind: draft \| debug \| improve, title}` |
| `node.code` | `node_id`, `lines[{text, added}]`; `added` đánh dấu dòng mới so với node cha |
| `node.run_started` | `node_id` |
| `node.log` | `node_id`, `level: command \| info \| error \| success`, `text` |
| `node.finished` | `node_id`, `outcome: works \| crashed \| out_of_attempts \| discarded`, `error?` |
| `node.scored` | `node_id`, `score` (0–1) |
| `result.recorded` | `result {key, hypothesis_id, round, node_id, estimate, ci_low, ci_high}` (null khi không chạy được), `best_node_id` |

`discarded` là version bị luật 2 loại; BE phát kèm `rule.checked` với `state: hit`.

### 5.10 Interpret

`evidence.row` (`hypothesis`, `result`), `verdict.written` (`hypothesis_id`, `verdict: supported | not_supported | insufficient`, `reason`), `verdict.checked` (`hypothesis_id`, `objection?`), `decision.recommended` (`recommendation: proceed | refine | pivot`, `rationale`, `go_backs_used`, `go_backs_allowed`), `decision.committed` (`decision`, `by: pi | you`, `note?`).

### 5.11 Report

`report.row` (`row {hypothesis_id, statement, status: result | crashed | dropped, result_key?, round?, estimate?, ci_low?, ci_high?, verdict?}`), `report.figure` (`figure {id, title, caption, data}`; `data.kind` là `bars`, `forest` hoặc `paths`), `report.note` (`hypothesis_id`, `note`, `objection?`), `report.repro` (`items[{label, value}]`).

Hình được vẽ ở FE từ `data`. BE gửi số liệu, không gửi ảnh, để hình không thể lệch với `results.json`. File ảnh/PDF cuối vẫn đi qua `run_artifacts` như hiện tại.

### 5.12 Write the paper

| `type` | Payload |
|---|---|
| `paper.outline` | `title`, `authors`, `sections[{id, title, numbered, uses}]`, `sources[{id, label, detail}]` |
| `paper.section_started` / `paper.section_done` | `section_id` |
| `paper.block` | `section_id`, `block`: `paragraph`, `figure {figure}`, `table {title, caption, header, rows}`, `references {items}` hoặc `appendix {rows}` |
| `paper.delta` | `block_id`, `piece` (xem dưới) |
| `paper.checked` | `numbers`, `figures` |
| `paper.blocked` | `span_id`, `text`: số gõ tay, kèm `rule.checked` luật 1 `hit` |
| `paper.number_fixed` | `span_id`, `value`, `source` |
| `review.comment` | `comment_id`, `span_id`, `text` |
| `review.revision` | `comment_id`, `span_id`, `from`, `to` |
| `review.accepted` | `{}` |
| `draft.scored` | `draft`, `score` (0–10), `note`, `best` |
| `paper.typeset` | `{}` |

`piece` của `paper.delta`:

- `{kind: "text", text}`: chữ thường; nhiều delta liên tiếp được nối lại.
- `{kind: "number", value, source}`: **mọi con số phải đi theo dạng này**. `source` trỏ tới một `sources[].id`, ví dụ `result:h1_sleep7_diff_r1` hoặc `data:rows_v2`.
- `{kind: "cite", refs}`, `{kind: "figure_ref", figure}`.
- `{kind: "typed_number", span_id, text}`: số Reporter gõ tay, không có nguồn. Luật 1 phải chặn publish cho tới khi có `paper.number_fixed`.
- `{kind: "span", span_id, text}`: đoạn chữ Skeptic có thể comment hoặc Reporter có thể sửa.

### 5.13 Điểm dừng

| `type` | Payload |
|---|---|
| `gate.opened` | `gate {id, kind, title, why, summary[], options[{id, label, description, leads_to, confirm_label, recommended?, disabled?}], stop_index, stop_total, droppable?}` |
| `gate.resolved` | `gate_id`, `answer {option_id, note?, dropped?}`, `summary` (một câu để ghi vào timeline) |

Trình tự bắt buộc: `run.status = awaiting_review` → `gate.opened` → (người dùng trả lời) → `gate.resolved` → `run.status = running`. Trong lúc chờ không có event nội dung nào khác.

`option_id` đã dùng:

| Gate | Options |
|---|---|
| `scope`, `report` | `ok`, `note` |
| `screen` | `approve`, `drop` (kèm `dropped` là id bài) |
| `hypotheses` | `approve`, `drop` (kèm `dropped` là id hypothesis) |
| `decision` | `proceed`, `refine`, `pivot` |
| `publish` | `publish`, `revise`; `revise` mở lại gate sau một bản nháp mới |

## 6. Ví dụ

```text
event: run-event
id: 42
data: {"seq":42,"run_id":"…","ts":"2026-10-06T09:12:03Z","type":"node.finished","stage_key":"r1-experiment","actor":"methodologist","payload":{"node_id":"H2-r1-v1","outcome":"crashed","error":"KeyError: 'stress_score'"}}

event: run-event
id: 43
data: {"seq":43,"run_id":"…","ts":"2026-10-06T09:12:04Z","type":"agent.message","stage_key":"r1-experiment","actor":"methodologist","payload":{"message_id":"m31","delta":"Two versions crashed. "}}
```

## 7. Ánh xạ với BE hiện tại

| Hiện có | Trong contract |
|---|---|
| `research_runs.status` | Vẫn giữ. `run.status` là luồng chi tiết; `queued` tương ứng chưa có `run.started`. `budget_exceeded` phát thành `run.status = failed` với `reason`. |
| `auto_review` | Thay bằng `review_mode`. `auto_review = true` ≈ `auto`; `false` ≈ chỉ dừng ở scope, tương đương một mode riêng nếu cần giữ. |
| `frame_reviews` | Trở thành một trường hợp của gate (`kind: scope`). Có thể giữ bảng cũ, thêm bảng gate tổng quát. |
| HITL gate stage 5 của pipeline | Gate `kind: screen`; `decision.json` của stage 5 tương ứng `gate.resolved`. |
| `run_artifacts` | Giữ nguyên cho file cuối (PDF, TeX, hình, `results.json`). |
| `POST /runs/{id}/sync` | Không cần cho workspace khi đã có SSE; vẫn giữ cho màn hình danh sách. |

## 8. Cài đặt tham chiếu phía FE

- Contract: `ai-research-platform-fe/src/lib/run-stream/contract.ts`
- Reducer và state: `src/lib/run-stream/reducer.ts`, `run-state.ts`; test ở `reducer.test.ts` (phát trọn một run Auto, một run Copilot có bỏ một bài ở shortlist và một hypothesis, và một run Full kiểm tra thứ tự stage 1–9).
- Dữ liệu mẫu stage 1–8: `src/lib/run-stream/mock/discovery.ts`.
- Mock: `src/lib/run-stream/mock/mock-run.ts` phát đúng chuỗi event trên, chờ ở gate và rẽ nhánh theo câu trả lời. Đây là bản mẫu tốt nhất để BE đối chiếu thứ tự và payload.
- Biến `NEXT_PUBLIC_RUN_STREAM_SOURCE=api` đưa tab Research runs về bảng cũ cho tới khi có stream thật.
