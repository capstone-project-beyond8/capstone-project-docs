# Business Requirements Document (BRD)

## AI Research Experimentation Platform

**Document Type:** Business Requirements Document  
**Project:** AI Research Experimentation Platform  
**Version:** 1.8 Draft  
**Status:** Draft for supervisor review  

---

**Normalization target:** req-tool section-contract Markdown format.  The original DRAFT remains unchanged; source sections are preserved below and only their hierarchy is normalized.

---

## Executive Summary

<!-- Source sections: 1. Executive Summary; 2. Business Context; 24. High-Level Product Positioning; 25. Product Value Proposition -->

### Executive Summary

AI Research Experimentation Platform là nền tảng hỗ trợ researcher thực hiện quy trình nghiên cứu dựa trên dữ liệu thông qua AI Agent.

Người dùng có thể đưa dataset, research question, hypothesis và domain context vào hệ thống. AI Agent sau đó hỗ trợ hiểu dữ liệu, kiểm tra chất lượng, lựa chọn phương pháp phân tích, chạy experiment, kiểm tra giả định thống kê, đánh giá kết quả, sinh research finding và tiếp tục đề xuất hypothesis mới dựa trên evidence thu được.

Nền tảng không chỉ dừng ở việc "chat với dataset" hoặc chạy một phép kiểm thử thống kê đơn lẻ. Mục tiêu chính là hỗ trợ một vòng lặp nghiên cứu có cấu trúc:

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
Selected Hypothesis
    ↓
Deep Reasoning & Experiment Planning
    ↓
Deterministic Scientific Checks
    ↓
Experiment Execution
    ↓
Deterministic Scientific Validation
    ↓
Evidence Sufficiency Gate
    ↓
Enough Evidence?
   /              \
 No                Yes
 ↓                  ↓
Scientific          Research Finding
Refinement          ↓
Loop                Update Research State
 ↓                  ↓
Next Experiment     Stopping Criteria
 └───────────────↺
```

Mọi finding quan trọng phải có evidence, provenance và execution trace. Các giả thuyết mới do AI sinh ra phải được đánh dấu là chưa được xác minh cho đến khi được kiểm thử bởi experiment tiếp theo.

Kiến trúc nghiệp vụ tách ba loại trách nhiệm: **generative reasoning** để tạo và phân tích sâu candidate hypothesis/experiment, **deterministic analytical tools** để tính toán các facts khoa học, và **structured decision gates** để lựa chọn hướng nghiên cứu hoặc quyết định evidence đã đủ hay cần tiếp tục. Decision gate phải trả về quyết định có cấu trúc cùng confidence/uncertainty để hệ thống có thể tự động tiếp tục, yêu cầu phân tích sâu hơn hoặc chuyển sang human review.

Platform đồng thời cung cấp cơ chế benchmark và evaluation nhằm đo lường độ chính xác, reliability, traceability và hiệu quả của AI Research Agent cũng như chất lượng của các decision gates.

Ngoài execution correctness, platform phải kiểm soát scientific validity của vòng lặp nghiên cứu: data leakage, multiple testing, post-hoc hypothesis, effect size, confidence interval, experiment dependency, conflicting evidence và reproducibility drift.

Từ v1.3, platform bổ sung một số capability theo tinh thần AI Scientist mà không mở rộng sang tree-search: ideation có reflection và novelty assessment tham khảo, cùng bản thảo nghiên cứu có automated review và phê duyệt của researcher. Các capability này nằm dưới decision gate và deterministic tools của BRD, và không thay đổi triết lý linear, single-path execution của Decision-Gated Research Loop (BR-21).

---

### Business Context

Trong nghiên cứu dựa trên dữ liệu, researcher thường phải thực hiện nhiều bước:

```text
Research Question
    ↓
Form Hypothesis
    ↓
Understand Dataset
    ↓
Data Quality Check
    ↓
Cleaning
    ↓
Select Analysis Method
    ↓
Check Assumptions
    ↓
Run Experiment
    ↓
Interpret Result
    ↓
Refine Hypothesis
    ↓
Run Next Experiment
    ↓
Generate Finding
    ↓
Create Figure / Table
    ↓
Write Research Report
```

Quy trình này đòi hỏi kiến thức về:

- data analysis;
- statistical methods;
- research methodology;
- experiment design;
- interpretation;
- reproducibility;
- scientific reporting.

AI Research Experimentation Platform được đề xuất để hỗ trợ tự động hóa một phần đáng kể workflow trên nhưng vẫn giữ researcher trong vòng kiểm soát ở những quyết định quan trọng.

---

### High-Level Product Positioning

> AI Research Experimentation Platform là nền tảng AI Agent hỗ trợ researcher thực hiện vòng lặp nghiên cứu dựa trên dữ liệu với kiến trúc `Generate → Select → Reason → Execute → Validate → Verify → Refine`. Platform tách generative reasoning, deterministic scientific computation và structured decision gating để lựa chọn hypothesis, đánh giá evidence sufficiency và quyết định bước tiếp theo có kiểm soát. Mục tiêu là tạo evidence-backed findings có provenance, reproducibility, confidence-aware escalation và human control thay vì chỉ trả về câu trả lời dạng black-box.

---

### Product Value Proposition

```text
Research Question
        +
Research State
        +
Candidate Hypothesis Generation
        +
Structured Hypothesis Selection
        +
Hypothesis Management
        +
Unknown Dataset Understanding
        +
Automated Profiling
        +
Method Selection
        +
Assumption Checking
        +
Experiment Execution
        +
Experiment Branching
        +
Hypothesis Refinement
        +
Deterministic Scientific Validation
        +
Evidence Sufficiency Verification
        +
Scientific Refinement Loop
        +
Finding Validation
        +
Confidence-Based Human Escalation
        +
Decision Auditability
        +
Provenance
        +
Execution Trace
        +
Reproducibility
        +
Scientific Validity Guard
        +
Multiple-Testing Control
        +
Experiment Dependency Graph
        +
Conflicting Evidence Handling
        +
Reproducibility Snapshot
        +
Bounded Tied-Candidate Selection
        +
Systematic Evaluation
```

---

## Problem Statement

<!-- Source sections: 3. Business Problem Statement; 7. Current State — As-Is; 8.1. Gap Analysis -->

### Business Problem Statement

#### BP-01 — Research workflow có nhiều bước thủ công

Researcher thường phải chuyển đổi giữa nhiều công cụ để:

- kiểm tra dữ liệu;
- cleaning;
- viết code;
- chạy statistical test;
- tạo figure;
- lưu experiment result;
- viết report.

Điều này làm tăng thời gian xử lý và khó duy trì traceability.

---

#### BP-02 — Việc lựa chọn statistical method yêu cầu chuyên môn

Researcher không phải lúc nào cũng biết:

- phép kiểm thử nào phù hợp;
- assumption nào cần kiểm tra;
- khi nào nên dùng parametric hoặc non-parametric method;
- khi nào cần regression;
- khi nào cần interaction analysis;
- khi nào cần replication.

Platform cần hỗ trợ method selection dựa trên question, variable type và data characteristics.

---

#### BP-03 — Dataset nghiên cứu thường có ambiguity và data-quality issue

Dataset có thể khác nhau về:

- schema;
- định dạng;
- kiểu dữ liệu;
- missing values;
- duplicates;
- outliers;
- domain semantics;
- variable meaning.

AI phải hiểu dataset trước khi đưa ra experiment plan.

---

#### BP-04 — AI có thể biến assumption thành conclusion

Một AI Agent có thể suy luận:

```text
Observation
→ Assumption
→ Conclusion
```

mà không có đủ evidence.

Platform phải phân biệt rõ:

```text
Observation
Hypothesis
Finding
Conclusion
```

và không được coi hypothesis là fact khi chưa được experiment xác minh.

---

#### BP-05 — Research finding khó kiểm chứng nếu thiếu provenance

Một finding phải truy ngược được về:

```text
Finding
→ Hypothesis
→ Experiment
→ Dataset Version
→ Method
→ Assumptions
→ Code / Query
→ Raw Output
→ Statistical Result
```

Nếu không có provenance, researcher khó đánh giá tính hợp lệ và reproducibility.

---

#### BP-06 — Một experiment đơn lẻ có thể chưa đủ

Kết quả E1 có thể tạo ra một câu hỏi mới hoặc hypothesis mới.

Ví dụ:

```text
H1
↓
E1
↓
Finding F1
↓
Generate H2
↓
E2
↓
Finding F2
```

Platform cần hỗ trợ iterative research thay vì chỉ chạy một phép thử rồi dừng.

---

#### BP-07 — Khó đánh giá AI Research Agent một cách khách quan

Cần đo lường:

- task success;
- method selection quality;
- statistical correctness;
- retry;
- experiment count;
- latency;
- cost;
- human intervention;
- provenance coverage;
- unsupported claim rate;
- reproducibility.

---


#### BP-08 — Iterative hypothesis generation làm tăng nguy cơ false positive

Khi agent liên tục sinh H2, H3, H4... từ kết quả trước và thực hiện nhiều statistical tests, xác suất tìm thấy kết quả có vẻ "significant" do ngẫu nhiên tăng lên.

Platform cần theo dõi số lượng hypothesis/test và áp dụng multiple-testing control khi phù hợp.

---

#### BP-09 — Post-hoc hypothesis có thể bị trình bày như hypothesis ban đầu

Hypothesis được tạo sau khi quan sát E1 không tương đương hypothesis được xác định trước khi xem dữ liệu.

Platform phải phân biệt rõ:

```text
Initial / Confirmatory Hypothesis
Post-hoc / Exploratory Hypothesis
```

---

#### BP-10 — Experiment phụ thuộc lẫn nhau

E2 có thể được tạo từ finding của E1. Nếu E1 sau đó bị invalidate, downstream hypothesis/finding có thể không còn đáng tin cậy.

Platform cần lưu dependency graph và hỗ trợ invalidate downstream artifacts.

---

#### BP-11 — Evidence có thể xung đột

Một experiment có thể support một hypothesis trong khi experiment khác cho kết quả ngược lại.

Platform không được chỉ giữ result thuận lợi mà phải quản lý trạng thái conflicting evidence.

---

#### BP-12 — Data leakage và reproducibility drift

Khi sử dụng predictive/ML analysis, preprocessing hoặc model selection có thể vô tình sử dụng thông tin từ test data.

Ngoài ra, cùng một experiment có thể khó tái lập nếu model, prompt, library hoặc environment thay đổi.

Platform phải hỗ trợ data split policy, leakage guard và reproducibility snapshot.

---

#### BP-13 — LLM không nên tự quyết định mọi bước của research loop

LLM phù hợp cho việc sinh hypothesis, reasoning và lập kế hoạch nhưng các quyết định như:

- hypothesis nào đáng theo đuổi;
- evidence đã đủ hay chưa;
- có cần replicate;
- có cần alternative method;
- có cần human review;

nếu chỉ dựa vào free-form reasoning có thể khó kiểm soát, khó đo lường và thiếu confidence rõ ràng.

Platform cần một cơ chế **structured decision gate** tách biệt với generative reasoning để lựa chọn, verify và route bước tiếp theo của research loop.

---

#### BP-14 — Experiment chạy thành công về kỹ thuật nhưng evidence vẫn có thể chưa đủ

Một experiment không lỗi code và trả ra statistic hợp lệ không đồng nghĩa research question đã có đủ evidence.

Platform phải phân biệt:

```text
Technical Failure
≠
Scientific Insufficiency
```

Scientific insufficiency phải có thể dẫn tới:

```text
Need More Evidence
Try Alternative Method
Replicate
Human Review
Inconclusive
```

thay vì chỉ trả về finding hoặc cố retry cùng một execution.

---

#### BP-16 — Ý tưởng do AI sinh có thể không mới hoặc đã được nghiên cứu

Agent có thể đề xuất hypothesis đã có trong tài liệu và xem đó là mới. Platform cần hỗ trợ đánh giá novelty ở mức tham khảo, không bảo đảm novelty.

---

#### BP-17 — Bản thảo do AI viết dễ có số liệu, hình và trích dẫn sai

Các đánh giá độc lập của hệ thống AI Scientist đời đầu ghi nhận lỗi thí nghiệm, hình thiếu, placeholder và trích dẫn ít hoặc cũ. Bản thảo phải truy được về experiment log và được review trước khi sử dụng.

---

### Current State — As-Is

```text
Researcher
    ↓
Define Research Question
    ↓
Write Hypothesis
    ↓
Open Dataset
    ↓
Inspect Variables
    ↓
Clean Data
    ↓
Choose Statistical Method
    ↓
Write Code
    ↓
Run Analysis
    ↓
Check Result
    ↓
Interpret
    ↓
Create Figure
    ↓
Generate New Question
    ↓
Repeat Manually
    ↓
Write Report
```

#### Pain Points

##### P1 — Nhiều thao tác lặp lại

Profiling, cleaning, assumption checking và reporting lặp lại giữa nhiều experiment.

##### P2 — Method selection phụ thuộc chuyên môn

Chọn sai test có thể dẫn đến kết luận không hợp lệ.

##### P3 — Research iteration khó quản lý

H1 → E1 → H2 → E2 thường bị lưu rời rạc giữa notebook, file và document.

##### P4 — Khó phân biệt hypothesis và confirmed finding

AI hoặc researcher có thể diễn giải quá mức một result chưa đủ evidence.

##### P5 — Khó truy vết finding

Một finding có thể không rõ được tạo từ experiment nào.

##### P6 — Khó tái lập

Thiếu code, dataset version, assumptions hoặc environment làm experiment khó reproduce.

##### P7 — Khó đánh giá AI

Không có benchmark thì khó chứng minh agent thực sự chọn method và reason tốt.

---

### Gap Analysis

Gap Analysis liên kết trực tiếp giữa pain point hiện tại, khoảng trống cần giải quyết, target state và Business Requirement tương ứng.

| ID | Pain Point / Current State | Gap | Target State | Related BR |
|---|---|---|---|---|
| GA-01 | Research workflow gồm nhiều bước rời rạc và lặp lại | Không có một workflow thống nhất từ question đến finding | Một research lifecycle thống nhất có planning, execution, validation và iteration | BR-13 → BR-30 |
| GA-02 | Method selection phụ thuộc nhiều vào kinh nghiệm cá nhân | Khó đảm bảo phương pháp phù hợp và assumptions được kiểm tra | Agent sinh candidate methods, kiểm tra assumptions và ghi rationale | BR-18, BR-19, BR-20, BR-24 |
| GA-03 | Dataset mới thường có ambiguity, missing values hoặc quality issues | Dễ xử lý sai dữ liệu trước khi analysis | Dataset được validate, profile, review và version trước khi experiment | BR-04 → BR-12 |
| GA-04 | Hypothesis, assumption và finding có thể bị trộn lẫn | Dễ biến hypothesis hoặc association thành fact/causal claim | Hypothesis có status/origin rõ; finding chỉ được chấp nhận sau validation | BR-14, BR-15, BR-27, BR-42, BR-48 |
| GA-05 | Finding khó kiểm chứng hoặc tái lập | Thiếu provenance, execution trace và reproducibility metadata | Official finding truy vết được về experiment, dataset, code và snapshot | BR-34 → BR-37, BR-55 |
| GA-06 | Một experiment chạy thành công có thể vẫn chưa đủ evidence | Không có cơ chế quyết định tiếp tục nghiên cứu hay dừng | Evidence Sufficiency Gate quyết định finding, re-plan, replicate, review hoặc inconclusive | BR-59, BR-60, BR-61 |
| GA-07 | Nhiều hypothesis/tests có thể làm tăng false-positive risk | Thiếu phân biệt initial/post-hoc và multiple-testing control | Hypothesis origin, correction, effect size và CI được quản lý rõ | BR-48, BR-49, BR-50 |
| GA-08 | Experiment phụ thuộc nhau và có thể tạo evidence xung đột | Không theo dõi downstream impact khi evidence thay đổi | Dependency graph, invalidation và conflict preservation | BR-51, BR-52, BR-53 |
| GA-09 | LLM free-form reasoning có thể tự quyết định quá nhiều | Bounded decisions khó audit và thiếu confidence rõ ràng | Tách generative reasoning khỏi structured decision gates | BR-56 → BR-63 |
| GA-10 | Khó chứng minh kiến trúc agentic tốt hơn baseline | Demo thành công đơn lẻ không đủ bằng chứng | Benchmark, quantitative metrics, ablation và gate evaluation | BR-43 → BR-46, BR-63 |
| GA-12 | Ý tưởng do AI sinh có thể đã được nghiên cứu | Không có novelty assessment | Idea record có reflection và novelty assessment tham khảo | BR-64, BR-65 |
| GA-13 | Bản thảo do AI viết khó kiểm chứng | Số liệu, hình và trích dẫn không truy vết được; thiếu review | Manuscript draft liên kết log, automated review và human approval | BR-73, BR-74, BR-75 |
| GA-14 | Selection Gate phải ép chọn 1 candidate dù điểm/confidence giữa các candidate top gần như ngang nhau | Ép chọn cứng khi chênh lệch điểm nằm trong sai số đo lường của chính decision model có thể loại bỏ oan một hướng nghiên cứu tốt | Bounded tied-candidate selection với ngưỡng/số lượng cấu hình được, gộp đúng testing family và giới hạn tổng branching | BR-78, BRule-35, BRule-36 |

**Kết luận Gap Analysis:** mọi capability chính trong scope đều phải giải quyết một gap cụ thể; capability không truy vết được về pain point/objective không nên được đưa vào core scope.

---

## Vision and Objectives

<!-- Source sections: 4. Business Objectives; 5. Success Metrics; 8. Future State — To-Be; 21. Business Benefits -->

### Business Objectives

#### BO-01 — Hỗ trợ researcher từ research question đến research finding

Platform cần hỗ trợ một workflow thống nhất:

```text
Research Question
→ Hypothesis
→ Experiment Planning
→ Analysis
→ Validation
→ Finding
```

---

#### BO-02 — Hỗ trợ tự động chọn phương pháp phân tích phù hợp

AI Agent phải có khả năng:

- hiểu research question;
- xác định variable type;
- sinh candidate methods;
- kiểm tra assumptions;
- chọn method phù hợp;
- fallback sang method khác nếu assumption không đạt.

---

#### BO-03 — Hỗ trợ iterative hypothesis refinement

Sau một experiment, agent có thể:

- giữ hypothesis hiện tại;
- reject hypothesis;
- đánh dấu inconclusive;
- sinh hypothesis mới;
- đề xuất experiment tiếp theo.

---

#### BO-04 — Tăng khả năng kiểm chứng research finding

Finding quan trọng phải có evidence và provenance.

---

#### BO-05 — Bảo vệ dữ liệu nghiên cứu gốc

Dataset gốc không được ghi đè.

Mọi transformation phải tạo version mới.

---

#### BO-06 — Giữ human control ở các điểm rủi ro

AI phải yêu cầu researcher xác nhận khi:

- data ambiguity;
- destructive cleaning;
- uncertain business/scientific meaning;
- unclear variable semantics;
- experiment có nhiều lựa chọn có ý nghĩa khác nhau.

---

#### BO-07 — Tăng reproducibility

Một experiment phải có đủ metadata để người khác có thể hiểu cách kết quả được tạo ra.

---

#### BO-08 — Đánh giá AI Research Agent bằng benchmark và metric định lượng

Platform cần hỗ trợ systematic evaluation và ablation study.

---


#### BO-09 — Kiểm soát multiple testing và exploratory research

Platform phải phân biệt confirmatory và exploratory hypothesis, đồng thời theo dõi số lượng phép kiểm thử được thực hiện.

---

#### BO-10 — Quản lý dependency và conflicting evidence

Platform phải biểu diễn quan hệ phụ thuộc giữa hypothesis, experiment và finding; đồng thời giữ được evidence trái chiều thay vì loại bỏ.

---

#### BO-11 — Đánh giá practical significance thay vì chỉ p-value

Khi phù hợp, platform phải xem xét effect size, confidence interval và uncertainty bên cạnh statistical significance.

---

#### BO-12 — Ngăn data leakage và tăng reproducibility

Experiment phải có data split policy khi cần và lưu execution snapshot đủ để tái lập.

---

#### BO-13 — Tách generative reasoning khỏi structured decision making

Platform phải cho phép generative model tập trung vào:

- tạo candidate hypothesis;
- reasoning chuyên sâu;
- thiết kế experiment;
- giải thích và refinement;

trong khi các decision gate chịu trách nhiệm chọn/routing các quyết định có tập output xác định.

---

#### BO-14 — Tự động kiểm tra evidence sufficiency trước khi chấp nhận finding

Sau deterministic scientific validation, platform phải đánh giá xem evidence đã đủ để:

- tạo finding;
- chạy thêm experiment;
- thử alternative method;
- replicate;
- yêu cầu human review;
- hoặc kết luận inconclusive.

---

#### BO-15 — Hỗ trợ confidence-based human escalation

Khi decision confidence thấp hoặc uncertainty/risk cao, platform phải ưu tiên chuyển decision cho researcher thay vì tự động tiếp tục.

---

#### BO-17 — Ideation có cấu trúc và nhận thức về novelty

Candidate hypothesis phải có idea record, được reflection trước khi vào selection gate, và có novelty assessment tham khảo khi có nguồn tài liệu.

---

#### BO-19 — Bản thảo nghiên cứu có thể review

Platform hỗ trợ tạo bản thảo từ validated findings với số liệu và trích dẫn kiểm chứng được, có review tự động và phê duyệt của researcher.

---

#### BO-20 — Xử lý candidate hypothesis ngang điểm một cách có kiểm soát

Khi Structured Hypothesis Selection Gate không thể phân biệt rõ candidate tốt nhất do điểm/confidence quá sát nhau, platform phải cho phép chọn đồng thời một số lượng candidate giới hạn (bounded tied-candidate selection) thay vì ép chọn một candidate duy nhất dựa trên khác biệt điểm số không đáng tin cậy, đồng thời giữ nguyên kiểm soát về chi phí, multiple-testing và audit.

---

### Success Metrics

Các target dưới đây là đề xuất ban đầu và cần được supervisor xác nhận.

| ID | Objective | Metric | Target đề xuất |
|---|---|---|---:|
| KPI-01 | Dataset understanding | Profiling completion rate | ≥ 95% dataset hợp lệ |
| KPI-02 | Method selection | Appropriate-method selection rate | ≥ 80% trên benchmark |
| KPI-03 | Research execution | Experiment success rate | ≥ 75% |
| KPI-04 | Trustworthiness | Important findings with evidence | 100% |
| KPI-05 | Human control | Destructive changes without approval | 0 |
| KPI-06 | Traceability | Experiments with execution trace | 100% |
| KPI-07 | Reproducibility | Experiments with reproducibility metadata | 100% |
| KPI-08 | Data safety | Original dataset preserved | 100% |
| KPI-09 | Hypothesis discipline | New hypotheses clearly marked unverified | 100% |
| KPI-10 | Evaluation | Benchmark tasks with measurable score | 100% |
| KPI-11 | Scientific validity | Hypotheses with origin classification | 100% |
| KPI-12 | Multiple testing | Eligible multi-test workflows with correction/justification | 100% |
| KPI-13 | Dependency | Downstream artifacts linked to parent evidence | 100% |
| KPI-14 | Reproducibility | Official experiments with execution snapshot | 100% |
| KPI-15 | Hypothesis gate | Selected hypothesis/direction has structured decision record | 100% |
| KPI-16 | Evidence gate | Validated experiment result receives explicit sufficiency decision | 100% |
| KPI-17 | Decision safety | Low-confidence/high-risk gate decisions escalated according to policy | 100% |
| KPI-18 | Decision evaluation | Decision-gate quality measured on benchmark tasks | 100% |
| KPI-21 | Ideation quality | Candidate hypotheses có idea record và reflection trước selection gate | 100% |
| KPI-22 | Manuscript integrity | Số liệu trong bản thảo truy được về experiment log | 100% |
| KPI-23 | Manuscript integrity | Trích dẫn trong bản thảo được xác minh là tồn tại | 100% |
| KPI-26 | Gate accuracy | Decision accuracy của structured gate so với baseline rule-based | Không thấp hơn baseline; ngưỡng do supervisor xác nhận |

---

### Future State — To-Be

```text
Researcher
    ↓
Create/Open Research Project
    ↓
Upload Dataset
    ↓
Automatic Profiling + Data Card
    ↓
Enter Research Question
    ↓
Define Initial H0 / H1
    ↓
Build Research State
    ↓
Generate Candidate Hypotheses / Directions
    ↓
Hypothesis Selection Gate
    ↓
Selected Hypothesis
    ↓
Deep Reasoning + Experiment Planner
    ↓
Generate Candidate Methods
    ↓
Check Assumptions
    ↓
Select / Branch Method
    ↓
Execute Experiment
    ↓
Deterministic Scientific Validation
    ↓
Evidence Sufficiency Gate
    ↓
Decision
├── ENOUGH_EVIDENCE → Research Finding
├── NEED_MORE_EVIDENCE → Re-plan
├── TRY_ALTERNATIVE_METHOD → Re-plan
├── REPLICATE → New Experiment
├── NEED_HUMAN_REVIEW → Researcher
└── INCONCLUSIVE → Record Outcome
    ↓
Update Research State
    ↓
Stopping Criteria
├── Continue → Generate Next Candidate Hypotheses
└── Stop → Final Research Findings
                  ↓
            Figures / Tables
                  ↓
            Research Report
```

---

### Business Benefits

#### Cho Researcher

- giảm thao tác lặp;
- hỗ trợ chọn method;
- hỗ trợ assumption checking;
- quản lý experiment loop;
- hỗ trợ hypothesis refinement;
- tạo figure/table nhanh;
- giữ trace và evidence.

#### Cho Research Project Manager

- theo dõi research progress;
- quản lý experiment history;
- quản lý dataset version;
- xem findings và report.

#### Cho Reviewer

- kiểm tra evidence;
- xem experiment trace;
- review methodology và result dễ hơn.

#### Cho Research Evaluation

- benchmark được agent;
- so sánh architecture;
- đo method selection;
- đo hypothesis-selection quality;
- đo evidence-sufficiency decision;
- đo confidence/calibration;
- so sánh structured decision gate với LLM-only decision baseline;
- đo reproducibility;
- đo provenance.

---

## Stakeholder Register

<!-- Source sections: 6. Stakeholders -->

### Stakeholders

#### 6.1. System Administrator

##### Mục tiêu

Quản lý hệ thống, user, model và operational monitoring.

##### Nhu cầu

- quản lý tài khoản;
- quản lý role và quyền;
- cấu hình AI model;
- xem logs;
- xem usage;
- xem token/cost;
- theo dõi agent failures;
- theo dõi system performance.

---

#### 6.2. Research Project Manager

##### Mục tiêu

Quản lý research project, dataset, member, experiment history và output.

##### Nhu cầu

- tạo research project;
- quản lý member;
- quản lý dataset;
- theo dõi experiment;
- theo dõi finding;
- xem research report;
- xem project summary.

---

#### 6.3. Researcher / Data Analyst

##### Mục tiêu

Thực hiện nghiên cứu dựa trên dữ liệu với sự hỗ trợ của AI.

##### Nhu cầu

- upload dataset;
- nhập research question;
- nhập hypothesis;
- xem profiling;
- cleaning;
- chạy experiment;
- xem statistical result;
- kiểm tra assumption;
- xem evidence;
- xem execution trace;
- tạo figure/table;
- tạo research report.

---

#### 6.4. Reviewer / Stakeholder

##### Mục tiêu

Đánh giá output nghiên cứu mà không cần trực tiếp chạy experiment.

##### Nhu cầu

- xem research finding;
- xem figure/table;
- xem evidence;
- xem report;
- xem experiment trace;
- gửi feedback.

---

## Scope and Capabilities

<!-- Source sections: 9. Scope; 10. Business Requirements; 10.1. Business Requirement Prioritization — MoSCoW; 12. Business Process — Research Setup; 13. Business Process — Decision-Gated Research Loop; 14. Business Process — Hypothesis Generation & Selection; 15. Business Process — Method Selection; 16. Business Process — Research Finding Verification; 16.1. Business Process — Scientific Validity Guard; 16.1.1. Business Process — Evidence Sufficiency Gate; 16.2. Business Process — Dependency & Conflict Handling; 17. Business Process — Evaluation; 17.1. Business Process — Manuscript Draft & Review; 22. Business Acceptance Criteria -->

### Scope

#### 9.1. Core / Must Have

##### User & Research Project

- Authentication
- RBAC
- Research project management
- Member management

##### Dataset

- Dataset upload
- Dataset validation
- Data profiling
- Data Card
- Data-quality review
- Cleaning proposal
- Human approval
- Dataset versioning

##### Research Context

- Research question
- H0 / H1 definition
- Domain context
- Analysis goal
- Optional literature/context notes
- Research State built from previous hypotheses, experiments, findings, conflicts and uncertainty

##### Decision & Verification Gates

- Candidate hypothesis/direction generation
- Structured hypothesis ranking / selection / rejection
- Decision confidence / uncertainty
- Evidence sufficiency verification
- Decision outcomes for continue / re-plan / replicate / human review / inconclusive
- Human escalation policy for low-confidence or high-risk decisions
- Decision audit trail

##### Experimentation

- Experiment planner
- Candidate method generation
- Assumption checking
- Method selection
- Statistical analysis
- Limited experiment branching
- Retry / self-correction
- Hypothesis refinement
- Hypothesis origin classification: initial / post-hoc
- Multiple-testing control
- Effect size & confidence interval
- Data leakage guard where applicable
- Experiment dependency graph
- Conflicting evidence handling
- Uncertainty/confidence recording
- Stopping criteria
- Replication where appropriate

##### Research Output

- Research finding
- Statistical result
- Figure/table
- Methodology summary
- Limitations
- Research report

##### Trust & Reproducibility

- Provenance
- Execution trace
- Experiment history
- Dataset lineage
- Reproducibility metadata
- Reproducibility snapshot
- Downstream invalidation
- Evidence conflict tracking

##### Evaluation

- Telemetry
- Benchmark execution
- Method-selection evaluation
- Hypothesis-gate evaluation
- Evidence-gate evaluation
- Confidence/calibration evaluation
- Quantitative metrics
- Ablation study

##### Ideation Quality

- Structured idea record & reflection

> **Implementation note:** TypeSafe/Jev là một candidate cho structured decision model. BRD chỉ yêu cầu capability `Structured Decision Gate`; vendor/model cụ thể được quyết định ở PRD/SDD để tránh khóa kiến trúc vào một provider.

---

#### 9.2. Supporting / Should Have

- Project summary dashboard
- Reviewer view
- Cost monitoring
- Multi-dataset analysis
- Figure reviewer
- Finding validator
- Model configuration
- Research report customization
- Novelty assessment (tham khảo)
- Figure aggregation & visual feedback
- Manuscript draft generation
- Automated manuscript review

---

#### 9.3. Nice to Have

- Literature connector
- Database connector
- Scheduled experiment
- Collaborative report editing
- Advanced statistical models
- Automatic citation assistance
- More advanced experiment search

---

#### 9.4. Out of Scope

- Fully autonomous literature discovery
- Fully autonomous paper publication
- Automatic novelty guarantee
- Training custom foundation models
- Large-scale distributed big data
- Real-time streaming analytics
- Image/audio/video scientific analysis
- Mobile application

---

### Business Requirements

#### BR-01 — Authentication

Hệ thống phải cho phép người dùng đăng nhập và truy cập theo danh tính hợp lệ.

---

#### BR-02 — Role-Based Access Control

Hệ thống phải phân quyền theo role và project scope.

---

#### BR-03 — Research Project Workspace

Hệ thống phải cho phép tạo một research project chứa:

- members;
- datasets;
- research questions;
- hypotheses;
- experiments;
- findings;
- figures/tables;
- reports.

---

#### BR-04 — Dataset Upload

Researcher phải có khả năng upload structured dataset.

Target format:

- CSV;
- XLSX;
- JSON;
- Parquet;
- TSV.

---

#### BR-05 — Dataset Validation

Hệ thống phải kiểm tra dataset trước khi sử dụng.

---

#### BR-06 — Automatic Dataset Understanding

Hệ thống phải tự hiểu schema, variable type và basic data characteristics.

---

#### BR-07 — Data Profiling

Hệ thống phải cung cấp:

- row/column count;
- data type;
- missing values;
- duplicates;
- distribution;
- cardinality;
- outliers;
- sample values;
- potential relationships.

---

#### BR-08 — Data Quality Review

Researcher phải có khả năng review issue trước experiment.

---

#### BR-09 — Cleaning Recommendation

AI phải đề xuất cleaning plan và nêu risk/information loss.

---

#### BR-10 — Human Approval

Destructive hoặc semantically risky change phải được user approve.

---

#### BR-11 — Original Dataset Preservation

Raw dataset không được ghi đè.

---

#### BR-12 — Dataset Versioning

Mỗi transformation phải tạo dataset version mới.

---

#### BR-13 — Research Question Definition

Researcher phải có khả năng nhập research question.

---

#### BR-14 — Hypothesis Definition

Researcher phải có khả năng định nghĩa:

```text
H0
H1
```

hoặc để agent đề xuất hypothesis draft cần researcher review.

---

#### BR-15 — Hypothesis Status

Mỗi hypothesis phải có status:

```text
Proposed
Unverified
Supported
Rejected
Inconclusive
Superseded
```

---

#### BR-16 — Research Context

Hệ thống phải cho phép lưu:

- domain context;
- variable meaning;
- research goal;
- important assumptions;
- optional prior knowledge.

---

#### BR-17 — Experiment Planning

Agent phải tạo experiment plan dựa trên:

- research question;
- hypothesis;
- dataset;
- variable types;
- data quality;
- domain context.

---

#### BR-18 — Candidate Method Generation

Agent phải có khả năng sinh một hoặc nhiều candidate analytical methods.

Ví dụ:

```text
Pearson
Spearman
T-test
Mann–Whitney
ANOVA
Kruskal–Wallis
Chi-square
Regression
Interaction Analysis
```

---

#### BR-19 — Assumption Checking

Trước khi chạy một statistical method, agent phải kiểm tra các assumption liên quan.

Ví dụ:

- variable type;
- normality;
- independence;
- linearity;
- homoscedasticity;
- expected frequency;
- sample size;
- outliers.

---

#### BR-20 — Method Selection

Agent phải chọn method phù hợp dựa trên assumption và research goal.

Nếu assumption không đạt, agent phải:

- chọn alternative method;
- hoặc yêu cầu user clarification;
- hoặc đánh dấu experiment không phù hợp.

---

#### BR-21 — Limited Experiment Branching

Khi nhiều method hợp lệ, hệ thống có thể chạy nhiều experiment branch để so sánh.

```text
Experiment
├── Method A
├── Method B
└── Method C
```

---

#### BR-22 — Experiment Execution

Agent phải có khả năng thực hiện experiment bằng tool/code được hệ thống kiểm soát.

---

#### BR-23 — Self-Correction

Nếu execution lỗi, agent có thể:

```text
Observe Error
→ Revise Code / Plan
→ Retry
```

trong giới hạn cho phép.

---

#### BR-24 — Experiment Validation

Sau khi execution thành công, hệ thống phải validate:

- statistical result;
- assumptions;
- output consistency;
- possible data leakage;
- unsupported interpretation.

---

#### BR-25 — Replication

Khi cần, experiment có thể chạy nhiều lần hoặc qua nhiều sampling/run để đánh giá stability.

---

#### BR-26 — Research Finding Generation

Agent phải chuyển raw experiment result thành research finding dễ hiểu.

---

#### BR-27 — Finding Status

Finding phải có status:

```text
Preliminary
Validated
Inconclusive
Rejected
Needs Review
```

---

#### BR-28 — Hypothesis Refinement

Dựa trên finding, agent có thể đề xuất hypothesis mới.

Ví dụ:

```text
H1
↓
E1
↓
F1
↓
H2
```

Hypothesis mới phải được đánh dấu `Unverified`.

---

#### BR-29 — Experiment-Finding-Hypothesis Linkage

Hệ thống phải lưu quan hệ:

```text
Hypothesis
→ Experiment
→ Finding
→ Next Hypothesis
```

---

#### BR-30 — Stopping Criteria

Research loop phải dừng khi:

- research question đã được trả lời đủ mức;
- không còn meaningful hypothesis;
- hết experiment budget;
- hết step/time limit;
- researcher dừng;
- result vẫn inconclusive sau giới hạn cho phép.

Khi bounded tied-candidate selection (BR-78) chạy K nhánh song song, experiment/time/cost budget phải được tính tổng hợp trên toàn bộ nhánh đang chạy trong vòng lặp đó, không tính riêng lẻ theo từng nhánh.

---

#### BR-31 — Statistical Analysis

Platform phải hỗ trợ các method cơ bản:

- correlation;
- t-test;
- Mann–Whitney;
- chi-square;
- ANOVA;
- Kruskal–Wallis;
- linear regression;
- logistic regression;
- interaction analysis;
- basic time-series analysis.

---

#### BR-32 — Visualization

Agent phải có khả năng tạo figure phù hợp với research question và statistical result.

---

#### BR-33 — Figure Review

Hệ thống nên kiểm tra:

- chart type;
- axis labels;
- units;
- legend;
- misleading scale;
- caption consistency;
- figure supports finding.

---

#### BR-34 — Research Finding Provenance

Mọi finding quan trọng phải truy vết được về:

- research question;
- hypothesis;
- experiment;
- dataset version;
- selected method;
- assumptions;
- generated code/query;
- raw output;
- statistical result.

---

#### BR-35 — Execution Trace

Researcher phải có khả năng xem từng step agent đã thực hiện.

---

#### BR-36 — Experiment History

Hệ thống phải lưu experiment history.

---

#### BR-37 — Reproducibility Metadata

Mỗi experiment phải lưu tối thiểu:

- dataset version;
- method;
- parameters;
- code/query;
- execution time;
- environment info;
- output;
- random seed nếu có;
- agent/model configuration.

---

#### BR-38 — Research Figure/Table Output

Hệ thống phải hỗ trợ tạo figure/table phục vụ report.

---

#### BR-39 — Methodology Summary

Agent phải có khả năng sinh summary mô tả:

- dataset;
- cleaning;
- variables;
- method;
- assumptions;
- experiment procedure.

---

#### BR-40 — Limitations

Agent phải hỗ trợ ghi rõ limitations của analysis.

---

#### BR-41 — Research Report Generation

Platform phải tạo research report từ validated findings.

---

#### BR-42 — Finding Validation

Trước khi finding xuất hiện trong report chính thức, hệ thống phải kiểm tra:

```text
Has Evidence?
Method Valid?
Assumptions Documented?
Dataset Version Known?
Execution Trace Exists?
Interpretation Supported?
```

---

#### BR-43 — Evaluation Framework

Hệ thống phải có benchmark runner để đánh giá agent.

---

#### BR-44 — Benchmark Task Structure

Mỗi task có thể gồm:

- dataset;
- research question;
- hypothesis;
- expected method;
- expected output/ground truth;
- required skills;
- scoring function.

---

#### BR-45 — Evaluation Metrics

Hệ thống phải đo:

- task success;
- correctness;
- method-selection accuracy;
- assumption-check quality;
- retry count;
- experiment count;
- latency;
- token usage;
- cost;
- human intervention;
- provenance coverage;
- unsupported claim rate;
- reproducibility coverage.

---

#### BR-46 — Agent Configuration Comparison

Hệ thống phải hỗ trợ ablation study.

Ví dụ:

```text
Full Agent
No Planner
No Assumption Checking
No Retry
No Profiling
No Validator
No Hypothesis Refinement
No Hypothesis Selection Gate
No Evidence Sufficiency Gate
No Tied-Candidate Selection (single-select baseline)
LLM-only Decision Baseline
Single Agent
Text-to-Code Baseline
```

---


#### BR-47 — Data Split & Leakage Guard

Khi experiment sử dụng predictive/ML workflow, hệ thống phải cho phép hoặc yêu cầu xác định:

- training split;
- validation split;
- test split;
- preprocessing scope;
- feature-selection scope.

Agent không được sử dụng test data để fit preprocessing, select features hoặc tune model nếu research design không cho phép.

---

#### BR-48 — Hypothesis Origin Classification

Mỗi hypothesis phải lưu origin:

```text
Initial / Confirmatory
Post-hoc / Exploratory
User-defined
Agent-generated
```

Hypothesis sinh sau khi xem result phải được đánh dấu rõ là post-hoc/exploratory.

---

#### BR-49 — Multiple-Testing Control

Khi một workflow thực hiện nhiều hypothesis tests có liên quan, hệ thống phải:

- ghi nhận số lượng tests;
- xác định testing family khi phù hợp;
- đề xuất hoặc áp dụng correction phù hợp;
- lưu correction method;
- lưu cả raw và adjusted significance values khi có.

Các experiment phát sinh từ bounded tied-candidate selection (BR-78) phải được tính là cùng một testing family khi áp dụng correction, không được xử lý như các test độc lập riêng biệt.

Ví dụ:

```text
Bonferroni
Holm
Benjamini-Hochberg / FDR
```

---

#### BR-50 — Effect Size & Confidence Interval

Khi statistical method hỗ trợ, agent phải báo cáo:

- effect size;
- confidence interval;
- p-value hoặc equivalent evidence measure;
- practical interpretation.

Agent không được dựa duy nhất vào p-value để đưa ra finding mạnh.

---

#### BR-51 — Experiment Dependency Graph

Hệ thống phải lưu dependency:

```text
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

Mỗi downstream hypothesis/finding phải biết evidence upstream mà nó phụ thuộc.

Khi bounded tied-candidate selection (BR-78) chọn nhiều hypothesis cùng lúc, graph phải biểu diễn thêm một loại quan hệ `co_selected_with` giữa các nhánh anh em (sibling branches) được chọn trong cùng một lần tied-selection, tách biệt với các quan hệ tests/produces/motivates/depends_on/uses_dataset/supersedes/contradicts đã có.

---

#### BR-52 — Downstream Invalidation

Nếu experiment/finding upstream bị:

```text
Rejected
Invalidated
Recomputed
Replaced
```

hệ thống phải đánh dấu các downstream hypothesis/finding bị ảnh hưởng và yêu cầu re-validation khi cần.

---

#### BR-53 — Conflicting Evidence Management

Nếu nhiều experiment cho evidence trái chiều, hệ thống phải:

- giữ tất cả result;
- không cherry-pick result thuận lợi;
- đánh dấu trạng thái `Conflicting Evidence`;
- yêu cầu thêm analysis hoặc human review khi cần.

Phạm vi này cũng áp dụng khi các nhánh song song từ bounded tied-candidate selection (BR-78) cùng được validate thành finding: hệ thống phải giữ lại tất cả finding hợp lệ từ các nhánh anh em, không được tự ý gộp hoặc chỉ báo cáo một finding, và phải phân biệt trường hợp này (nhiều finding độc lập từ hypothesis khác nhau) với `Conflicting Evidence` (nhiều experiment mâu thuẫn trên cùng một hypothesis).

---

#### BR-54 — Confidence & Uncertainty Recording

Finding và hypothesis evaluation phải có uncertainty metadata khi phù hợp.

Ví dụ:

```text
Confidence: Low / Medium / High
Reason:
- small sample
- wide confidence interval
- conflicting evidence
- violated assumption
- unstable replication
```

Confidence không được thay thế statistical evidence mà chỉ là metadata hỗ trợ review.

---

#### BR-55 — Reproducibility Snapshot

Mỗi official experiment phải lưu snapshot tối thiểu:

- dataset version;
- data split;
- code/query;
- parameters;
- random seed;
- statistical method;
- model name/version;
- agent configuration;
- prompt/template version khi relevant;
- tool/library versions;
- runtime/environment;
- execution timestamp;
- raw outputs;
- generated figures/tables.

---

#### BR-56 — Research State Construction

Trước mỗi research iteration, hệ thống phải xây dựng một Research State có cấu trúc từ:

- research question;
- current hypothesis;
- previous hypotheses;
- experiment history;
- validated findings;
- conflicting evidence;
- uncertainty/warnings;
- dataset version;
- remaining constraints/budget.

Research State là input dùng để sinh và đánh giá hướng nghiên cứu tiếp theo.

Khi bounded tied-candidate selection (BR-78) tạo nhiều nhánh song song, mỗi nhánh phải giữ một snapshot Research State bất biến (immutable) tại thời điểm được chọn; Research State chung chỉ được cập nhật sau khi tất cả nhánh trong cùng vòng lặp hoàn tất, để tránh xung đột cập nhật giữa các nhánh chạy song song.

---

#### BR-57 — Candidate Hypothesis / Direction Generation

Hệ thống phải có khả năng tạo một hoặc nhiều candidate hypotheses/research directions từ Research State.

Mỗi candidate phải có:

- statement;
- rationale;
- parent evidence;
- testability;
- relevant variables;
- risk/uncertainty notes.

---

#### BR-58 — Structured Hypothesis Selection Gate

Trước khi đầu tư vào deep reasoning/experiment planning cho research iteration tiếp theo, hệ thống phải có khả năng:

```text
Rank
Select
Reject
Escalate
```

candidate hypotheses/directions bằng một structured decision.

Decision record tối thiểu phải có:

- selected candidate hoặc outcome;
- confidence/uncertainty;
- reason codes hoặc decision metadata;
- Research State version được sử dụng.

Khi nhiều candidate ngang điểm trong ngưỡng cấu hình được, xem cơ chế bounded tied-candidate selection ở BR-78.

---

#### BR-59 — Evidence Sufficiency Gate

Sau deterministic scientific validation, mỗi experiment result phải được đánh giá bằng một structured evidence decision.

Các outcome tối thiểu:

```text
ENOUGH_EVIDENCE
NEED_MORE_EVIDENCE
TRY_ALTERNATIVE_METHOD
REPLICATE
NEED_HUMAN_REVIEW
INCONCLUSIVE
```

Outcome phải điều khiển bước tiếp theo của research loop thay vì mặc định tạo finding.

---

#### BR-60 — Scientific Refinement Loop

Khi Evidence Sufficiency Gate trả về:

```text
NEED_MORE_EVIDENCE
TRY_ALTERNATIVE_METHOD
REPLICATE
```

hệ thống phải chuyển state về reasoning/planning để tạo experiment tiếp theo.

Đây là scientific refinement, khác với technical retry do execution error.

---

#### BR-61 — Confidence-Based Human Escalation

Decision gate phải có thể chuyển quyết định cho researcher khi:

- confidence dưới policy threshold;
- evidence conflict nghiêm trọng;
- ambiguity ảnh hưởng interpretation;
- methodological choice có high impact;
- decision outcome là `NEED_HUMAN_REVIEW`;
- các nhánh song song từ bounded tied-candidate selection (BR-78) cho Evidence Sufficiency outcome mâu thuẫn nhau (ví dụ một nhánh ENOUGH_EVIDENCE trong khi nhánh anh em INCONCLUSIVE hoặc NEED_HUMAN_REVIEW).

---

#### BR-62 — Decision Auditability

Mọi decision gate phải lưu:

- input Research State/reference;
- candidate choices;
- selected outcome;
- confidence/uncertainty;
- timestamp;
- model/provider/configuration identifier;
- downstream action.

Khi bounded tied-candidate selection (BR-78) được kích hoạt, decision record phải lưu thêm: ngưỡng tied-selection đã dùng (tie threshold) và danh sách candidate được coi là ngang điểm.

---

#### BR-63 — Decision Gate Evaluation

Evaluation framework phải đo được quality của structured decision gates, bao gồm tối thiểu:

- decision accuracy/correctness;
- selection quality;
- false acceptance of insufficient evidence;
- unnecessary continuation rate;
- human escalation rate;
- confidence/calibration quality;
- latency;
- cost.

System phải hỗ trợ so sánh:

```text
Structured Decision Gate
vs
LLM-only Decision
```

trên cùng benchmark tasks khi khả thi.

---


#### BR-64 — Structured Idea Record & Reflection

Mỗi candidate hypothesis phải có idea record gồm statement, experiment đề xuất, context liên quan và risk, và phải qua ít nhất một reflection round trước khi vào Hypothesis Selection Gate.

---

#### BR-65 — Novelty Assessment

Hệ thống nên đánh giá mức độ mới của idea dựa trên nguồn literature/context được cung cấp, ở mức tham khảo và không bảo đảm novelty (theo Scope 9.4). Khi không có nguồn, idea được ghi nhận là chưa đánh giá.

---

#### BR-73 — Figure Aggregation & Visual Feedback

Hệ thống nên gom figure từ các phương pháp/thử nghiệm đã chạy cho một hypothesis (BR-21) và kiểm tra bằng visual reviewer về độ rõ, khớp caption và trùng lặp (mở rộng BR-33).

---

#### BR-74 — Manuscript Draft Generation

Hệ thống nên tạo bản thảo từ validated findings với số liệu lấy trực tiếp từ experiment log, trích dẫn được xác minh và nội dung do AI tạo được ghi rõ. Đây chỉ là draft, hệ thống không tự nộp hoặc xuất bản (Scope 9.4).

---

#### BR-75 — Automated Manuscript Review

Hệ thống nên review bản thảo theo rubric (soundness, novelty, clarity) và kiểm tra chất lượng: placeholder, hình thiếu, trích dẫn chưa xác minh, số không khớp log. Bản thảo cần researcher phê duyệt trước khi dùng bên ngoài.

---

### Business Requirement Prioritization — MoSCoW

Priority được hiểu theo **cam kết cho bản capstone cuối**, không phải thứ tự sprint.

- **Must:** bắt buộc để platform đáp ứng research scope và acceptance criteria.
- **Should:** giá trị cao và nên hoàn thành, nhưng có thể defer nếu ảnh hưởng tiến độ core.
- **Could:** chỉ thực hiện khi còn capacity; hiện được quản lý ở Scope 9.3 và chưa cấp BR ID.
- **Won't:** chủ động loại khỏi phiên bản capstone hiện tại; được liệt kê tại Scope 9.4.
- **Must\*:** Must có điều kiện khi loại workflow tương ứng được sử dụng.

| BR | Requirement | Priority | Rationale |
|---|---|---|---|
| BR-01 | Authentication | Must | Thuộc core/final submission scope. |
| BR-02 | Role-Based Access Control | Must | Thuộc core/final submission scope. |
| BR-03 | Research Project Workspace | Must | Thuộc core/final submission scope. |
| BR-04 | Dataset Upload | Must | Thuộc core/final submission scope. |
| BR-05 | Dataset Validation | Must | Thuộc core/final submission scope. |
| BR-06 | Automatic Dataset Understanding | Must | Thuộc core/final submission scope. |
| BR-07 | Data Profiling | Must | Thuộc core/final submission scope. |
| BR-08 | Data Quality Review | Must | Thuộc core/final submission scope. |
| BR-09 | Cleaning Recommendation | Must | Thuộc core/final submission scope. |
| BR-10 | Human Approval | Must | Thuộc core/final submission scope. |
| BR-11 | Original Dataset Preservation | Must | Thuộc core/final submission scope. |
| BR-12 | Dataset Versioning | Must | Thuộc core/final submission scope. |
| BR-13 | Research Question Definition | Must | Thuộc core/final submission scope. |
| BR-14 | Hypothesis Definition | Must | Thuộc core/final submission scope. |
| BR-15 | Hypothesis Status | Must | Thuộc core/final submission scope. |
| BR-16 | Research Context | Must | Thuộc core/final submission scope. |
| BR-17 | Experiment Planning | Must | Thuộc core/final submission scope. |
| BR-18 | Candidate Method Generation | Must | Thuộc core/final submission scope. |
| BR-19 | Assumption Checking | Must | Thuộc core/final submission scope. |
| BR-20 | Method Selection | Must | Thuộc core/final submission scope. |
| BR-21 | Limited Experiment Branching | Must | Thuộc core/final submission scope. |
| BR-22 | Experiment Execution | Must | Thuộc core/final submission scope. |
| BR-23 | Self-Correction | Must | Thuộc core/final submission scope. |
| BR-24 | Experiment Validation | Must | Thuộc core/final submission scope. |
| BR-25 | Replication | Should | Tăng độ mạnh evidence; core loop vẫn hoạt động khi chưa cần replication. |
| BR-26 | Research Finding Generation | Must | Thuộc core/final submission scope. |
| BR-27 | Finding Status | Must | Thuộc core/final submission scope. |
| BR-28 | Hypothesis Refinement | Must | Thuộc core/final submission scope. |
| BR-29 | Experiment-Finding-Hypothesis Linkage | Must | Thuộc core/final submission scope. |
| BR-30 | Stopping Criteria | Must | Thuộc core/final submission scope. |
| BR-31 | Statistical Analysis | Must | Thuộc core/final submission scope. |
| BR-32 | Visualization | Must | Thuộc core/final submission scope. |
| BR-33 | Figure Review | Should | Nâng chất lượng figure; không chặn core research loop. |
| BR-34 | Research Finding Provenance | Must | Thuộc core/final submission scope. |
| BR-35 | Execution Trace | Must | Thuộc core/final submission scope. |
| BR-36 | Experiment History | Must | Thuộc core/final submission scope. |
| BR-37 | Reproducibility Metadata | Must | Thuộc core/final submission scope. |
| BR-38 | Research Figure/Table Output | Must | Thuộc core/final submission scope. |
| BR-39 | Methodology Summary | Must | Thuộc core/final submission scope. |
| BR-40 | Limitations | Must | Thuộc core/final submission scope. |
| BR-41 | Research Report Generation | Must | Thuộc core/final submission scope. |
| BR-42 | Finding Validation | Must | Thuộc core/final submission scope. |
| BR-43 | Evaluation Framework | Must | Thuộc core/final submission scope. |
| BR-44 | Benchmark Task Structure | Must | Thuộc core/final submission scope. |
| BR-45 | Evaluation Metrics | Must | Thuộc core/final submission scope. |
| BR-46 | Agent Configuration Comparison | Must | Thuộc core/final submission scope. |
| BR-47 | Data Split & Leakage Guard | Must* | Bắt buộc khi workflow predictive/ML có data split. |
| BR-48 | Hypothesis Origin Classification | Must | Thuộc core/final submission scope. |
| BR-49 | Multiple-Testing Control | Must | Thuộc core/final submission scope. |
| BR-50 | Effect Size & Confidence Interval | Must | Thuộc core/final submission scope. |
| BR-51 | Experiment Dependency Graph | Should | Quan trọng cho research nhiều vòng; có thể triển khai sau core lineage. |
| BR-52 | Downstream Invalidation | Should | Phụ thuộc dependency graph; triển khai sau khi BR-51 ổn định. |
| BR-53 | Conflicting Evidence Management | Should | Tăng scientific robustness; có thể triển khai sau core finding flow. |
| BR-54 | Confidence & Uncertainty Recording | Must | Thuộc core/final submission scope. |
| BR-55 | Reproducibility Snapshot | Must | Thuộc core/final submission scope. |
| BR-56 | Research State Construction | Must | Thuộc core/final submission scope. |
| BR-57 | Candidate Hypothesis / Direction Generation | Must | Thuộc core/final submission scope. |
| BR-58 | Structured Hypothesis Selection Gate | Must | Thuộc core/final submission scope. |
| BR-59 | Evidence Sufficiency Gate | Must | Thuộc core/final submission scope. |
| BR-60 | Scientific Refinement Loop | Must | Thuộc core/final submission scope. |
| BR-61 | Confidence-Based Human Escalation | Must | Thuộc core/final submission scope. |
| BR-62 | Decision Auditability | Must | Thuộc core/final submission scope. |
| BR-63 | Decision Gate Evaluation | Must | Thuộc core/final submission scope. |
| BR-64 | Structured Idea Record & Reflection | Must | Thuộc core ideation scope (BO-17). |
| BR-65 | Novelty Assessment | Should | Hỗ trợ ideation; không bảo đảm novelty nên không chặn core loop. |
| BR-73 | Figure Aggregation & Visual Feedback | Should | Nâng chất lượng figure; không chặn core loop. |
| BR-74 | Manuscript Draft Generation | Should | Mở rộng Research Report; có thể defer nếu ảnh hưởng core. |
| BR-75 | Automated Manuscript Review | Should | Phụ thuộc BR-74; có thể defer. |
| BR-78 | Bounded Tied-Candidate Selection | Must | Bảo vệ Hypothesis Selection Gate (BR-58, Must) khỏi ép chọn sai khi candidate ngang điểm; thuộc core decision-gate scope. |

**Scope control rule:** một requirement mới chỉ được thêm vào nhóm Must khi chứng minh được liên kết tới Business Problem, Business Objective và Research/Evaluation need. Nếu không, requirement phải được xếp Should/Could hoặc Out of Scope.

---

### Business Process — Research Setup

```text
Researcher
    ↓
Create Project
    ↓
Upload Dataset
    ↓
Enter Research Question
    ↓
Define H0 / H1
    ↓
Add Domain Context
    ↓
Start Research Loop
```

---

### Business Process — Decision-Gated Research Loop

```text
Research State
    ↓
Generate Candidate Hypotheses / Directions
    ↓
Structured Hypothesis Selection Gate
    ↓
Selected Hypothesis
    ↓
LLM Deep Reasoning / Experiment Planner
    ↓
Generate Candidate Methods
    ↓
Check Assumptions
    ↓
Select Method
    ↓
Execute Experiment
    ↓
Deterministic Scientific Validation
    ↓
Evidence Sufficiency Gate
    ↓
Decision
├── ENOUGH_EVIDENCE
│       ↓
│   Generate Finding
│       ↓
│   Update Research State
│
├── NEED_MORE_EVIDENCE
│       ↓
│   LLM Re-plan
│
├── TRY_ALTERNATIVE_METHOD
│       ↓
│   LLM Re-plan
│
├── REPLICATE
│       ↓
│   New Experiment
│
├── NEED_HUMAN_REVIEW
│       ↓
│   Researcher Decision
│
└── INCONCLUSIVE
        ↓
    Record Outcome
        ↓
Update Research State
    ↓
Stopping Criteria
├── Continue → Next Candidate Hypotheses
└── Stop → Final Research Findings
```

---

### Business Process — Hypothesis Generation & Selection

```text
Initial H1 / Previous Finding Fn
        ↓
Build / Update Research State
        ↓
Generate Candidates
├── H(n+1)-A
├── H(n+1)-B
└── H(n+1)-C
        ↓
Structured Hypothesis Selection Gate
        ↓
Rank / Select / Reject / Escalate
        ↓
Selected H(n+1)
        ↓
Type: Post-hoc / Exploratory
Status: Unverified
        ↓
Deep Reasoning + Experiment Planning
        ↓
Experiment E(n+1)
```

Candidate hypothesis chỉ trở thành active research direction sau khi được selection gate và policy/human review xử lý.

---

### Business Process — Method Selection

```text
Research Question
      ↓
Identify Variables
      ↓
Determine Variable Types
      ↓
Generate Candidate Methods
      ↓
Check Assumptions
      ↓
Suitable?
  ┌────┴────┐
 Yes        No
  │          │
  ▼          ▼
Execute   Alternative Method
             ↓
          Re-check
```

---

### Business Process — Research Finding Verification

```text
Research Finding
      ↓
View Evidence
      ↓
Hypothesis
      ↓
Experiment
      ↓
Dataset Version
      ↓
Method + Assumptions
      ↓
Code / Query
      ↓
Raw Output
      ↓
Statistical Result
```

---

### Business Process — Scientific Validity Guard

```text
Experiment Result
      ↓
Assumptions Valid?
      ↓
Multiple Tests?
      ↓
Apply / Justify Correction
      ↓
Effect Size + Confidence Interval
      ↓
Leakage Check (if applicable)
      ↓
Evidence Quality Facts
```

Deterministic scientific validation tạo facts/evidence; nó không tự động quyết định rằng research evidence đã đủ để dừng.

---

### Business Process — Evidence Sufficiency Gate

```text
Validated Scientific Facts
      +
Current Research State
      ↓
Structured Evidence Gate
      ↓
Decision
├── ENOUGH_EVIDENCE → Finding
├── NEED_MORE_EVIDENCE → LLM Re-plan
├── TRY_ALTERNATIVE_METHOD → LLM Re-plan
├── REPLICATE → New Experiment
├── NEED_HUMAN_REVIEW → Researcher
└── INCONCLUSIVE → Record Outcome
```

---

### Business Process — Dependency & Conflict Handling

```text
Finding F1
   ↓
Generates H2
   ↓
Experiment E2
   ↓
Finding F2
   ↓
Conflict with F1?
 ┌────┴────┐
 No       Yes
 │         │
 ▼         ▼
Continue   Mark Conflicting Evidence
              ↓
          Human / Agent Review
```

Nếu F1 bị invalidate:

```text
F1 Invalidated
      ↓
H2 flagged
      ↓
E2/F2 marked "Needs Re-validation"
```

---

### Business Process — Evaluation

```text
Benchmark Task
      ↓
Load Dataset
      ↓
Load Research Question / Hypothesis
      ↓
Run Agent
      ↓
Collect Experiments
      ↓
Collect Decision-Gate Outputs
      ↓
Collect Findings
      ↓
Collect Trace
      ↓
Score
      ↓
Repeat N Times
      ↓
Aggregate Metrics
      ↓
Compare Configurations
      ↓
Evaluation Report
```

---

### Business Process — Manuscript Draft & Review

```text
Validated Findings + Experiment Logs
      ↓
Figure Aggregation + Visual Feedback
      ↓
Manuscript Draft (số liệu từ log, trích dẫn xác minh)
      ↓
Automated Review (rubric + quality checks)
      ↓
Cần sửa?
 ┌───┴───┐
Yes      No
 │        │
 ▼        ▼
Revise   Researcher Approval
            ↓
      Final Manuscript Draft
```

---

### Business Acceptance Criteria

Platform được xem là đạt mục tiêu business khi:

*Lưu ý: các tiêu chí 27–29 tương ứng với BR-51, BR-52, BR-53 (priority Should theo mục 10.1). Nếu các BR này chưa được triển khai trong phạm vi capstone do giới hạn thời gian, ba tiêu chí này được coi là extended acceptance (mục tiêu mở rộng), không phải điều kiện bắt buộc để platform đạt business acceptance tối thiểu.*

1. User có thể upload dataset mà không cần khai báo schema trước.
2. Platform tự profiling dataset.
3. Researcher nhập được research question và H0/H1.
4. Agent sinh được experiment plan.
5. Agent sinh candidate methods.
6. Agent kiểm tra assumptions trước khi chọn method.
7. Agent chọn hoặc fallback method phù hợp.
8. Experiment được chạy và lưu trace.
9. Agent có thể retry khi execution lỗi.
10. Raw dataset luôn được giữ nguyên.
11. Finding có link về experiment.
12. Finding quan trọng có evidence.
13. Agent có thể đề xuất hypothesis mới từ finding.
14. Hypothesis mới được đánh dấu unverified.
15. Experiment tiếp theo có thể kiểm thử hypothesis mới.
16. Agent có stopping criteria.
17. Researcher có thể tạo figure/table.
18. Researcher có thể tạo research report.
19. Experiment có reproducibility metadata.
20. Agent có thể được benchmark bằng metric định lượng.
21. Có thể chạy ablation study giữa nhiều configuration.
22. Mỗi hypothesis có origin classification.
23. Post-hoc hypothesis không được trình bày như initial hypothesis.
24. Multi-test workflow có correction hoặc justification rõ ràng khi phù hợp.
25. Statistical finding có effect size/confidence interval khi method hỗ trợ.
26. Predictive workflow có leakage guard.
27. Experiment/finding có dependency graph.
28. Upstream invalidation được propagate xuống downstream artifacts.
29. Conflicting evidence được giữ lại và hiển thị.
30. Official experiment có reproducibility snapshot.
31. Hệ thống xây dựng Research State trước mỗi iteration.
32. Agent có thể tạo nhiều candidate hypotheses/research directions.
33. Candidate hypothesis được rank/select/reject bằng structured decision gate trước deep experiment planning.
34. Hypothesis selection decision có confidence/uncertainty và audit record.
35. Deterministic scientific validation hoàn tất trước Evidence Sufficiency Gate.
36. Experiment chạy thành công không tự động trở thành validated finding.
37. Evidence Sufficiency Gate trả một outcome có cấu trúc.
38. `NEED_MORE_EVIDENCE`, `TRY_ALTERNATIVE_METHOD` và `REPLICATE` kích hoạt scientific refinement loop.
39. `NEED_HUMAN_REVIEW` chuyển decision cho researcher.
40. Low-confidence/high-risk decisions tuân thủ escalation policy.
41. Technical retry và scientific refinement được trace riêng.
42. Evaluation framework đo được quality của hypothesis gate và evidence gate.
43. Có thể so sánh structured decision gate với LLM-only decision baseline.
50. Candidate hypothesis có idea record và reflection; novelty assessment (nếu bật) có nguồn.
51. Bản thảo (nếu tạo) có số liệu truy được về log, trích dẫn xác minh, review và phê duyệt của researcher.
53. Khi candidate hypothesis ngang điểm trong ngưỡng cấu hình, hệ thống chọn được nhiều candidate có giới hạn (bounded tied-selection) thay vì chỉ 1, và quyết định này được ghi audit.

---

## Business Rules

<!-- Source sections: 11. Business Rules -->

### Business Rules

#### BRule-01 — Project Isolation

Research project chỉ được truy cập bởi user có quyền.

---

#### BRule-02 — Original Dataset Preservation

Raw dataset không được ghi đè.

---

#### BRule-03 — Version on Change

Mọi transformation tạo version mới.

---

#### BRule-04 — Approval Before Risky Change

Risky cleaning phải được approve.

---

#### BRule-05 — Unusual Does Not Mean Incorrect

Anomaly không tự động được coi là lỗi.

---

#### BRule-06 — Hypothesis Is Not Fact

Hypothesis mới chưa được experiment xác minh phải được đánh dấu `Unverified`.

---

#### BRule-07 — Association Does Not Imply Causation

Agent không được kết luận causation chỉ từ correlation/association nếu design không hỗ trợ causal inference.

---

#### BRule-08 — Assumptions Must Be Explicit

Statistical assumptions phải được ghi lại.

---

#### BRule-09 — Method Selection Must Be Justified

Agent phải lưu lý do chọn method.

---

#### BRule-10 — Finding Must Have Evidence

Validated finding phải có evidence.

---

#### BRule-11 — Finding Must Reference Experiment

Mỗi finding phải link về experiment tạo ra nó.

---

#### BRule-12 — Experiment Must Reference Dataset Version

Mỗi experiment phải ghi rõ dataset version.

---

#### BRule-13 — Interpretation Must Match Statistical Evidence

Agent không được diễn giải mạnh hơn evidence cho phép.

---

#### BRule-14 — Human Decision Ownership

Researcher giữ quyền quyết định với các bước có uncertainty cao.

---

#### BRule-15 — Reproducibility

Experiment chính thức phải có đủ metadata để tái lập.

---


#### BRule-16 — Initial and Post-hoc Hypotheses Must Be Distinguishable

Hypothesis được tạo sau khi quan sát result không được trình bày như hypothesis ban đầu.

---

#### BRule-17 — Multiple Testing Must Be Accounted For

Agent không được coi nhiều p-values độc lập như một single-test workflow nếu chúng thuộc cùng testing family.

---

#### BRule-18 — Statistical Significance Is Not Practical Significance

Agent phải xem xét effect size và confidence interval khi phù hợp.

---

#### BRule-19 — No Data Leakage

Test data không được dùng để fit/tune workflow khi research design yêu cầu holdout evaluation.

---

#### BRule-20 — Dependency Must Be Preserved

Downstream hypothesis/finding phải giữ link đến upstream evidence.

---

#### BRule-21 — Invalidated Evidence Propagates

Khi upstream evidence bị invalidate, downstream artifacts phải được đánh dấu cần re-validation.

---

#### BRule-22 — Conflicting Evidence Must Be Preserved

Agent không được xóa hoặc bỏ qua result trái chiều chỉ vì không phù hợp với hypothesis đang theo đuổi.

---

#### BRule-23 — Official Findings Require Reproducibility Snapshot

Finding được đưa vào final research report phải tham chiếu experiment có reproducibility snapshot đầy đủ.

---

#### BRule-24 — Generative Reasoning and Decision Gating Are Separate Responsibilities

Free-form LLM reasoning không được là nguồn duy nhất cho các bounded decisions quan trọng nếu hệ thống đã định nghĩa structured gate cho decision đó.

---

#### BRule-25 — Tools Establish Scientific Facts

Statistical values, diagnostics và deterministic checks phải được tạo bởi analytical/statistical tools khi có thể; decision model không được tự phát minh scientific facts.

---

#### BRule-26 — Evidence Gate Precedes Official Finding

Experiment chạy thành công không tự động tạo validated finding. Evidence Sufficiency Gate phải xác định evidence đủ hoặc yêu cầu next action.

---

#### BRule-27 — Technical Retry Is Not Scientific Refinement

```text
Execution Error → Technical Retry / Re-plan
```

khác với:

```text
Valid Execution + Insufficient Evidence → Scientific Refinement
```

Hai loại loop phải được ghi nhận và đánh giá riêng.

---

#### BRule-28 — Low Confidence Requires Policy-Based Escalation

Decision có confidence thấp hoặc risk cao phải tuân theo escalation policy thay vì tự động tiếp tục.

---

#### BRule-29 — Structured Decision History Must Be Preserved

Mọi selection/verification decision phải được giữ trong audit history và liên kết với Research State đã tạo ra decision đó.

---

#### BR-78 — Bounded Tied-Candidate Selection

Khi nhiều candidate hypothesis có điểm/confidence chênh nhau dưới một ngưỡng cấu hình được (tie threshold), Structured Hypothesis Selection Gate (BR-58) được phép chọn đồng thời tối đa một số lượng candidate giới hạn (bounded tied-selection) thay vì bắt buộc chọn duy nhất một candidate. Ngưỡng và số lượng tối đa phải cấu hình được ở cấp project, không hard-code. Decision gate phải xuất ra một điểm số dạng numeric có thể so sánh được (dùng để xác định tied-selection) tách biệt với nhãn confidence định tính ở BR-54 (dùng cho giải thích/escalation); chất lượng calibration của điểm số này phải nằm trong phạm vi đánh giá của BR-63.

---

#### BRule-33 — Manuscript Claims Must Be Verifiable

Số liệu và figure trong bản thảo phải truy được về experiment log; trích dẫn phải được xác minh là tồn tại.

---

#### BRule-34 — AI-Generated Manuscripts Must Be Disclosed and Approved

Bản thảo do AI tạo phải được ghi rõ, cần researcher phê duyệt trước khi dùng bên ngoài và không được tự động nộp.

---

#### BRule-35 — Tied Candidates Require Bounded Exploration, Not Unlimited Branching

Khi Structured Hypothesis Selection Gate (BR-58) xác định nhiều candidate có điểm gần bằng nhau, hệ thống chỉ được mở rộng song song trong giới hạn số lượng và ngưỡng đã cấu hình trước (BR-78); đây không phải cơ chế tìm kiếm mở rộng không giới hạn, và mọi candidate được chọn theo cơ chế này phải được tính vào cùng một testing family theo BR-49.

---

#### BRule-36 — Combined Branching Must Stay Within a Configured Total Cap

Khi bounded tied-candidate selection (BR-78, tầng hypothesis) và limited experiment branching (BR-21, tầng method) cùng được áp dụng trong một vòng lặp, tổng số nhánh thực thi đồng thời (số hypothesis song song nhân số method mỗi hypothesis) phải nằm trong một giới hạn tổng cấu hình được ở cấp project; hệ thống không được để hai lớp branching cộng dồn vượt ngân sách experiment/cost mà không cảnh báo hoặc chặn lại.

---

## Constraints, Assumptions, and Risks

<!-- Source sections: 10.2. High-Level Non-Functional Requirements; 18. Assumptions; 19. Constraints; 20. Risks & Mitigation -->

### High-Level Non-Functional Requirements

Các NFR dưới đây mô tả **quality expectations ở mức BRD**. Threshold kỹ thuật chi tiết sẽ được chốt ở PRD/SDD và Test Plan.

| ID | Quality Attribute | Business Requirement |
|---|---|---|
| NFR-01 | Security & Access Control | Dataset, experiment, findings và project artifacts chỉ được truy cập bởi user có quyền phù hợp; không được có cross-project data exposure. |
| NFR-02 | Reliability & Recovery | Execution failure không được làm mất raw dataset, experiment history hoặc project state; user phải có khả năng tiếp tục/re-run từ trạng thái an toàn. |
| NFR-03 | Auditability & Traceability | Mọi official experiment, finding, approval và structured decision quan trọng phải có audit trail/execution reference. |
| NFR-04 | Explainability | Method selection, validation outcome và bounded decision quan trọng phải có rationale hoặc structured metadata đủ để researcher review. |
| NFR-05 | Reproducibility | Official experiments/findings phải có reproducibility metadata/snapshot đủ để tái lập trong phạm vi environment được hỗ trợ. |
| NFR-06 | Performance & Responsiveness | Tác vụ tương tác thông thường phải phản hồi trong thời gian chấp nhận được; long-running experiment phải có status/progress, timeout và failure state rõ ràng. |
| NFR-07 | Privacy & Data Governance | Dữ liệu nghiên cứu chỉ được sử dụng trong scope được user/project cho phép; raw data và sensitive context không được expose ngoài luồng được kiểm soát. |
| NFR-08 | Maintainability & Modularity | Planner, analytical tools, validators và structured decision providers phải có thể thay đổi độc lập ở mức thiết kế; platform không được phụ thuộc bắt buộc vào một AI/decision vendor duy nhất. |
| NFR-09 | Usability | Core research workflow phải có thể được thực hiện mà researcher không cần trực tiếp viết code; system phải hiển thị state, warning và required human action rõ ràng. |
| NFR-10 | Observability & Cost Awareness | System phải ghi nhận execution status, error, latency, usage và cost-related telemetry đủ để vận hành và đánh giá research agent. |
| NFR-11 | Scientific Integrity | System không được tự động biến hypothesis thành fact, association thành causation hoặc statistically significant result thành practical significance nếu thiếu evidence phù hợp. |
| NFR-12 | Decision Safety | Low-confidence/high-risk structured decisions phải tuân theo escalation policy; confidence không được dùng để thay thế deterministic scientific evidence. |

##### NFR Acceptance Direction

Các tiêu chí sau phải được thể hiện trong PRD/Test Plan:

```text
Security
→ authorization / project-isolation tests

Reliability
→ failure / retry / recovery tests

Auditability
→ trace completeness tests

Explainability
→ rationale / decision-record checks

Reproducibility
→ re-run / snapshot verification

Performance
→ response-time / long-running job tests

Decision Safety
→ low-confidence escalation tests

Scientific Integrity
→ unsupported-claim / evidence checks
```

---

### Assumptions

- Dataset chủ yếu là structured/tabular data.
- User có quyền sử dụng dataset.
- Researcher chịu trách nhiệm cuối cùng cho interpretation.
- AI-generated hypothesis cần được xem là proposal cho đến khi được experiment kiểm thử.
- Không phải mọi correlation đều có causal meaning.
- Statistical method phải phù hợp với data characteristics.
- Một research question có thể cần nhiều experiment.
- Post-hoc hypothesis phải được phân biệt với initial hypothesis.
- Multiple testing có thể yêu cầu correction.
- Predictive workflows phải kiểm soát data leakage.
- Downstream findings có thể phụ thuộc evidence upstream.
- Ground truth hoặc expert rubric cần thiết cho benchmark.
- Structured decision capability có thể được triển khai bằng TypeSafe/Jev hoặc provider/model tương đương; business requirements không phụ thuộc một vendor cụ thể.
- Decision confidence chỉ hỗ trợ routing/escalation, không thay thế deterministic statistical evidence.

---

### Constraints

- Scope phải phù hợp với capstone.
- Không xây full autonomous AI Scientist.
- Không đảm bảo novelty research tự động.
- Không train foundation model.
- Phải kiểm soát cost.
- Agent output có tính bất định.
- Tool/code execution phải được kiểm soát.
- Research data phải được isolate.
- Experiment history phải được lưu để audit.
- Experiment exploration được giới hạn bởi budget và không thay thế human control.
- Bản thảo do AI tạo chỉ là draft cần researcher phê duyệt.

---

### Risks & Mitigation

| ID | Risk | Impact | Mitigation |
|---|---|---|---|
| R-01 | Chọn sai statistical method | High | Candidate methods + assumption checking |
| R-02 | AI over-interpret result | High | Finding validator + evidence |
| R-03 | Correlation bị diễn giải thành causation | High | Explicit business/scientific rule |
| R-04 | Hypothesis mới bị coi là fact | High | Hypothesis status |
| R-05 | Data cleaning làm sai result | High | Human approval + versioning |
| R-06 | Experiment không reproducible | High | Reproducibility metadata |
| R-07 | Agent loop chạy quá lâu | Medium | Stopping criteria |
| R-08 | Dataset ambiguity | High | Human clarification |
| R-09 | AI cost cao | Medium | Budget monitoring |
| R-10 | Figure gây hiểu nhầm | Medium | Figure reviewer |
| R-11 | Benchmark không đủ tốt | Medium | Diverse task design |
| R-12 | Unsupported finding | High | Provenance + finding validation |
| R-13 | Multiple testing tạo false positive | High | Testing-family tracking + correction |
| R-14 | Post-hoc hypothesis bị trình bày như confirmatory | High | Hypothesis origin classification |
| R-15 | Data leakage | High | Split policy + leakage guard |
| R-16 | Upstream experiment sai làm lệch downstream | High | Dependency graph + invalidation propagation |
| R-17 | Cherry-picking evidence | High | Conflicting-evidence preservation |
| R-18 | Re-run cho kết quả khác | Medium | Reproducibility snapshot |
| R-19 | Decision gate chọn hypothesis kém | High | Benchmark selection quality + human review |
| R-20 | Evidence gate chấp nhận evidence chưa đủ | High | Deterministic validation + gate evaluation + escalation |
| R-21 | Confidence không được calibration tốt | Medium | Calibration evaluation + conservative threshold |
| R-22 | Quá phụ thuộc một decision-model provider | Medium | Provider abstraction + fallback strategy |
| R-23 | LLM và decision gate tạo feedback loop quá dài | Medium | Stopping criteria + experiment/time/cost budgets |
| R-25 | Novelty assessment phân loại sai | Medium | Ghi rõ mức tham khảo + benchmark misclassification |
| R-26 | Trích dẫn sai hoặc cũ, bản thảo chất lượng thấp | High | Xác minh trích dẫn + automated review + human approval |
| R-29 | Bounded tied-candidate selection cộng dồn với method-level branching làm bùng nổ chi phí hoặc tăng false-positive nếu không gộp đúng testing family | High | Giới hạn tổng branching (BRule-36) + bắt buộc gộp testing family (BR-49) + audit ngưỡng tied-selection (BR-62) |

---

## Research Basis

<!-- Source sections: 23. Business & Research Traceability Matrix; 26. Glossary; 27. Approval & Sign-off; 28. Document Change Log -->

### Business & Research Traceability Matrix

#### 23.1. Research Questions Used for Traceability

Để giữ liên kết với mục tiêu nghiên cứu ban đầu của capstone, BRD operationalize ba Research Questions như sau:

- **RQ1 — End-to-End Effectiveness:** AI Research Agent thực hiện end-to-end research experimentation trên user-provided datasets hiệu quả đến mức nào?
- **RQ2 — Architecture Effectiveness:** Kiến trúc `Generate → Select → Reason → Execute → Validate → Verify → Refine`, kết hợp generative reasoning, deterministic scientific tools và structured decision gates, cải thiện reliability/quality của research workflow đến mức nào?
- **RQ3 — Task/Skill Performance:** AI Research Agent hoạt động như thế nào theo từng nhóm research task và skill khi được đánh giá bằng benchmark và quantitative metrics?

Các RQ này giữ nguyên ý định cốt lõi của proposal: đánh giá end-to-end capability, giá trị của agentic architecture và performance theo task category.

#### 23.2. BO → BR → KPI → RQ Matrix

| Business Objective | Key Business Requirements | KPI / Evidence | Research Question |
|---|---|---|---|
| BO-01 — Hỗ trợ researcher từ question đến finding | BR-13 → BR-30 | KPI-03 Agent reliability, task completion, experiment success | RQ1 |
| BO-02 — Chọn phương pháp phù hợp | BR-18, BR-19, BR-20, BR-24 | Method-selection accuracy, assumption-check quality | RQ1, RQ3 |
| BO-03 — Iterative hypothesis refinement | BR-28, BR-29, BR-30, BR-57, BR-60 | Experiment count, valid refinement rate, successful continuation | RQ1, RQ2 |
| BO-04 — Tăng khả năng kiểm chứng finding | BR-34, BR-35, BR-42, BR-55 | KPI-04 evidence coverage, KPI-06 traceability | RQ1, RQ2 |
| BO-05 — Bảo vệ dữ liệu gốc | BR-10, BR-11, BR-12 | KPI-05 destructive changes without approval = 0; KPI-08 raw preservation | RQ1 |
| BO-06 — Human control | BR-10, BR-61 | Human intervention rate, escalation correctness | RQ2, RQ3 |
| BO-07 / BO-12 — Reproducibility & leakage control | BR-37, BR-47, BR-55 | KPI-14 reproducibility coverage, leakage violations | RQ1, RQ3 |
| BO-08 — Quantitative evaluation | BR-43 → BR-46, BR-63 | KPI-10 benchmark score coverage; task success; ablation deltas | RQ1, RQ2, RQ3 |
| BO-09 — Multiple-testing & exploratory control | BR-48, BR-49 | Hypothesis-origin coverage, correction compliance | RQ1, RQ3 |
| BO-10 — Dependency & conflicting evidence | BR-51, BR-52, BR-53 | Dependency coverage, invalidation propagation, conflict preservation | RQ1, RQ2 |
| BO-11 — Practical significance | BR-50 | Effect-size/CI coverage | RQ1, RQ3 |
| BO-13 — Tách reasoning khỏi bounded decision | BR-56, BR-57, BR-58, BR-62 | KPI-15 selection records; decision correctness | RQ2 |
| BO-14 — Evidence sufficiency verification | BR-59, BR-60 | KPI-16 evidence-gate coverage; false acceptance rate | RQ2, RQ3 |
| BO-15 — Confidence-based escalation | BR-54, BR-61, BR-63 | KPI-17 safe escalation; calibration quality | RQ2, RQ3 |
| BO-17 — Ideation & novelty | BR-64, BR-65 | KPI-21 | RQ2 |
| BO-19 — Bản thảo review được | BR-73, BR-74, BR-75 | KPI-22, KPI-23 | RQ1, RQ3 |
| BO-20 — Bounded tied-candidate selection | BR-78, BRule-35, BRule-36, BR-49, BR-56, BR-51, BR-53, BR-61, BR-62 | Acceptance Criteria 53; tied-selection audit coverage; R-29 mitigation coverage | RQ2, RQ3 |

#### 23.3. Product Traceability Chain

Ở cấp artifact, traceability phải duy trì theo chuỗi:

```text
Business Problem
      ↓
Business Objective
      ↓
Business Requirement
      ↓
Product Feature / User Story
      ↓
Acceptance Criteria
      ↓
Test Case
      ↓
Telemetry / Evaluation Metric
      ↓
Research Question
```

Ở cấp research execution:

```text
Research Question
      ↓
Research State
      ↓
Candidate Hypotheses
      ↓
Hypothesis Selection Decision
      ↓
Selected Hypothesis
      ↓
Experiment
      ↓
Method
      ↓
Execution
      ↓
Deterministic Scientific Evidence
      ↓
Evidence Sufficiency Decision
      ↓
Finding / Refinement / Human Review / Inconclusive
      ↓
Updated Research State
      ↓
Next Hypothesis or Research Conclusion
```

**Traceability rule:** một official conclusion phải truy ngược được về evidence và experiment; một core feature phải truy ngược được về BR/BO/RQ hoặc một NFR đã được phê duyệt.

---

### Glossary

| Term | Definition |
|---|---|
| Research Question | Câu hỏi nghiên cứu cần được trả lời bằng evidence |
| Hypothesis | Giả thuyết cần được kiểm thử |
| H0 | Null hypothesis |
| H1 | Alternative hypothesis |
| Experiment | Một quy trình phân tích/kiểm thử nhằm đánh giá hypothesis |
| Candidate Method | Phương pháp phân tích được agent xem xét |
| Assumption Checking | Kiểm tra điều kiện áp dụng statistical method |
| Finding | Kết quả nghiên cứu được suy ra từ experiment |
| Hypothesis Refinement | Sinh/chỉnh hypothesis mới dựa trên finding |
| Provenance | Thông tin truy vết finding về experiment và dữ liệu |
| Execution Trace | Lịch sử step/tool/code/output của agent |
| Reproducibility | Khả năng tái lập experiment từ metadata đã lưu |
| Replication | Lặp experiment để kiểm tra stability |
| Ablation Study | Loại bỏ một thành phần để đo ảnh hưởng |
| Benchmark | Tập task dùng để đánh giá agent |
| Ground Truth | Expected result hoặc tiêu chí chuẩn để chấm |
| Initial Hypothesis | Hypothesis xác định trước khi xem kết quả liên quan |
| Post-hoc Hypothesis | Hypothesis được tạo sau khi quan sát evidence/result |
| Multiple Testing | Thực hiện nhiều statistical tests trong cùng một research family |
| Effect Size | Mức độ lớn của effect/association, không chỉ mức significance |
| Confidence Interval | Khoảng bất định của estimate |
| Data Leakage | Thông tin từ evaluation/test data ảnh hưởng vào training/tuning |
| Experiment Dependency Graph | Graph liên kết hypothesis, experiment, finding và downstream research steps |
| Conflicting Evidence | Nhiều experiment tạo evidence trái chiều |
| Reproducibility Snapshot | Snapshot dataset/code/config/model/tool/environment để tái lập experiment |
| Research State | Structured state tổng hợp question, hypothesis, experiment history, findings, conflicts, uncertainty và constraints tại một iteration |
| Candidate Hypothesis | Hypothesis/research direction được sinh ra để selection gate đánh giá trước khi active |
| Structured Decision Gate | Thành phần trả bounded decision có cấu trúc thay vì free-form text |
| Hypothesis Selection Gate | Decision gate dùng để rank/select/reject/escalate candidate hypotheses |
| Evidence Sufficiency Gate | Decision gate xác định evidence đủ để tạo finding hay cần thêm analysis/replication/review |
| Scientific Refinement | Vòng lặp bổ sung experiment vì evidence chưa đủ, khác technical retry do lỗi execution |
| Decision Confidence | Confidence/uncertainty metadata dùng cho routing và human escalation |
| TypeSafe / Jev | Candidate implementation cho structured decision capability; không phải dependency bắt buộc của BRD |
| Novelty Assessment | Đánh giá tham khảo mức độ mới của idea dựa trên nguồn tài liệu, không bảo đảm novelty |
| Manuscript Draft | Bản thảo do AI tạo từ validated findings, cần review và phê duyệt của researcher |
| Bounded Tied-Candidate Selection | Cơ chế cho phép Hypothesis Selection Gate chọn đồng thời tối đa một số lượng candidate giới hạn khi điểm/confidence của chúng chênh nhau dưới một ngưỡng cấu hình được, thay vì ép chọn một candidate duy nhất |
| Tie Threshold | Ngưỡng chênh lệch điểm/confidence cấu hình được, dùng để xác định các candidate được coi là "ngang điểm" trong bounded tied-candidate selection |
| co_selected_with | Loại quan hệ trong Experiment Dependency Graph, liên kết các nhánh hypothesis anh em được chọn cùng lúc bởi một quyết định bounded tied-candidate selection |

---

### Approval & Sign-off

| Role | Name | Status | Date |
|---|---|---|---|
| Project Leader |  | Pending |  |
| Project Members |  | Pending |  |
| Supervisor |  | Pending |  |

---

### Document Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 |  |  | Initial AI Data Analytics BRD |
| 0.2 |  |  | Reframed toward AI Research Experimentation with iterative hypothesis-experiment loops |
| 0.3 | 2026-09-19 |  | Added scientific-validity controls: multiple testing, post-hoc hypothesis classification, effect size/CI, data leakage guard, dependency graph, conflicting evidence, uncertainty and reproducibility snapshot |
| 1.0 | 2026-09-19 |  | Finalized BRD and aligned with final architecture diagram and iterative research loop |
| 1.1 | 2026-09-20 |  | Added decision-gated research architecture: Research State, candidate-hypothesis selection, structured decision confidence, evidence sufficiency verification, scientific refinement loop, human escalation, and decision-gate evaluation; TypeSafe/Jev recorded as an implementation candidate rather than a required vendor |
| 1.2 | 2026-09-20 |  | Submission-ready BRD: added Gap Analysis, explicit MoSCoW prioritization for BR-01→BR-63, high-level NFR summary, and BO→BR→KPI→RQ traceability matrix; scope remains unchanged from v1.1 |
| 1.3 | 2026-09-21 |  | Added AI-Scientist-style experiment exploration (BP-15→17, BO-16→19, BR-64→77, KPI-19→26, BRule-30→34, NFR-13, R-24→28, GA-11→13, acceptance criteria 44→52): structured idea record and reflection, novelty assessment, experiment tree with Experiment Manager and staged exploration, debug nodes, search budget and selection-bias control, manuscript draft and review, exploration ablation with rule-based gate baseline and benchmark seed set; existing requirements unchanged |
| 1.4 | 2026-09-22 |  | Added bounded tied-candidate selection at Hypothesis Selection Gate (BR-58.1, BRule-35, BRule-36) and its cross-cutting impact on multiple-testing family (BR-49), Research State versioning under parallel branches (BR-56), dependency-graph sibling edges (BR-51), multi-finding handling (BR-53), cumulative stopping-criteria budget (BR-30), escalation on disagreeing parallel branches (BR-61), decision audit fields (BR-62) and a new ablation arm (BR-46); acceptance criterion 53 added; fixed KPI mislabeling in section 23.2 (BO-05: KPI-07→KPI-08; BO-08: KPI-08→KPI-10) and added a conditional-scope note for acceptance criteria 27–29 relative to the Should-priority of BR-51/52/53; existing requirements otherwise unchanged |
| 1.7 | 2026-09-22 |  | Renumbered the bounded tied-candidate selection requirement from the sub-clause BR-58.1 to a standalone BR-78, for consistency with the document's convention that every BR is a top-level, independently prioritized requirement; added BR-78 to the MoSCoW table (Must); updated all cross-references (GA-14, traceability matrix, BRule-35/36, BR-30/49/51/53/56/61/62 cross-references) accordingly; BR-58 now carries a short pointer to BR-78; no semantic change to the requirement itself |
| 1.8 | 2026-09-22 |  | Removed the Sakana-style bounded tree-search layer added in v1.3 (BR-66 Experiment Tree, BR-67 Staged Exploration, BR-68 Experiment Manager, BR-69 Debug Node & Bounded Retry, BR-70 Search Budget Control, BR-71 Search Selection-Bias Control, BR-72 Replication & Aggregation Nodes, BR-76 Search Trace View, BR-77 Exploration Evaluation & Ablation) and their dependent BRule-30/31/32, BP-15, BO-16, BO-18, GA-11, R-24/27/28, KPI-19/20/24/25, NFR-13, acceptance criteria 44–49 and 52, Business Process 13.1, and related MoSCoW/traceability/glossary entries — restoring the platform's original linear, single-path Decision-Gated Research Loop (BR-21) as the sole execution architecture, since the tree-search layer conflicted with that original design choice and its Sakana-comparable value was judged not to justify the added scope/engineering risk for a capstone deliverable; retained the tree-independent parts of the same v1.3 addition (BR-64 Structured Idea Record & Reflection, BR-65 Novelty Assessment, BR-73 Figure Aggregation & Visual Feedback — reworded to reference BR-21 method-level results instead of experiment-tree nodes, BR-74 Manuscript Draft Generation, BR-75 Automated Manuscript Review) and the bounded tied-candidate selection capability (BR-78, BRule-35/36, BO-20, GA-14, R-29) which operates at the Hypothesis Selection Gate and is independent of tree search; existing requirements otherwise unchanged |
| 1.5 | 2026-09-22 |  | Closed internal-consistency gaps left by v1.4: added BO-20 as a proper Business Objective for bounded tied-candidate selection (replacing the ad-hoc "BO-13 (mở rộng)" traceability label), added GA-14 (Gap Analysis) and R-29 (Risks & Mitigation) so the new capability is traceable end-to-end per BRD's own rule that every core capability must resolve a gap; existing requirements otherwise unchanged |
