# Business Requirements Document (BRD)
## AI Research Experimentation Platform

**Document Type:** Business Requirements Document  
**Project:** AI Research Experimentation Platform  
**Version:** 1.0 Final  
**Status:** Final  

---

# 1. Executive Summary

AI Research Experimentation Platform là nền tảng hỗ trợ researcher thực hiện quy trình nghiên cứu dựa trên dữ liệu thông qua AI Agent.

Người dùng có thể đưa dataset, research question, hypothesis và domain context vào hệ thống. AI Agent sau đó hỗ trợ hiểu dữ liệu, kiểm tra chất lượng, lựa chọn phương pháp phân tích, chạy experiment, kiểm tra giả định thống kê, đánh giá kết quả, sinh research finding và tiếp tục đề xuất hypothesis mới dựa trên evidence thu được.

Nền tảng không chỉ dừng ở việc "chat với dataset" hoặc chạy một phép kiểm thử thống kê đơn lẻ. Mục tiêu chính là hỗ trợ một vòng lặp nghiên cứu có cấu trúc:

```text
Research Question
    ↓
Initial Hypothesis
    ↓
Experiment
    ↓
Evidence
    ↓
Finding
    ↓
Hypothesis Refinement
    ↓
New Hypothesis (Post-hoc / Unverified)
    ↓
Next Experiment
    ↓
Scientific Validity Guard
    ↓
Stopping Criteria
```

Mọi finding quan trọng phải có evidence, provenance và execution trace. Các giả thuyết mới do AI sinh ra phải được đánh dấu là chưa được xác minh cho đến khi được kiểm thử bởi experiment tiếp theo.

Platform đồng thời cung cấp cơ chế benchmark và evaluation nhằm đo lường độ chính xác, reliability, traceability và hiệu quả của AI Research Agent.

Ngoài execution correctness, platform phải kiểm soát scientific validity của vòng lặp nghiên cứu: data leakage, multiple testing, post-hoc hypothesis, effect size, confidence interval, experiment dependency, conflicting evidence và reproducibility drift.

---

# 2. Business Context

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

# 3. Business Problem Statement

## BP-01 — Research workflow có nhiều bước thủ công

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

## BP-02 — Việc lựa chọn statistical method yêu cầu chuyên môn

Researcher không phải lúc nào cũng biết:

- phép kiểm thử nào phù hợp;
- assumption nào cần kiểm tra;
- khi nào nên dùng parametric hoặc non-parametric method;
- khi nào cần regression;
- khi nào cần interaction analysis;
- khi nào cần replication.

Platform cần hỗ trợ method selection dựa trên question, variable type và data characteristics.

---

## BP-03 — Dataset nghiên cứu thường có ambiguity và data-quality issue

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

## BP-04 — AI có thể biến assumption thành conclusion

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

## BP-05 — Research finding khó kiểm chứng nếu thiếu provenance

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

## BP-06 — Một experiment đơn lẻ có thể chưa đủ

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

## BP-07 — Khó đánh giá AI Research Agent một cách khách quan

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


## BP-08 — Iterative hypothesis generation làm tăng nguy cơ false positive

Khi agent liên tục sinh H2, H3, H4... từ kết quả trước và thực hiện nhiều statistical tests, xác suất tìm thấy kết quả có vẻ "significant" do ngẫu nhiên tăng lên.

Platform cần theo dõi số lượng hypothesis/test và áp dụng multiple-testing control khi phù hợp.

---

## BP-09 — Post-hoc hypothesis có thể bị trình bày như hypothesis ban đầu

Hypothesis được tạo sau khi quan sát E1 không tương đương hypothesis được xác định trước khi xem dữ liệu.

Platform phải phân biệt rõ:

```text
Initial / Confirmatory Hypothesis
Post-hoc / Exploratory Hypothesis
```

---

## BP-10 — Experiment phụ thuộc lẫn nhau

E2 có thể được tạo từ finding của E1. Nếu E1 sau đó bị invalidate, downstream hypothesis/finding có thể không còn đáng tin cậy.

Platform cần lưu dependency graph và hỗ trợ invalidate downstream artifacts.

---

## BP-11 — Evidence có thể xung đột

Một experiment có thể support một hypothesis trong khi experiment khác cho kết quả ngược lại.

Platform không được chỉ giữ result thuận lợi mà phải quản lý trạng thái conflicting evidence.

---

## BP-12 — Data leakage và reproducibility drift

Khi sử dụng predictive/ML analysis, preprocessing hoặc model selection có thể vô tình sử dụng thông tin từ test data.

Ngoài ra, cùng một experiment có thể khó tái lập nếu model, prompt, library hoặc environment thay đổi.

Platform phải hỗ trợ data split policy, leakage guard và reproducibility snapshot.

---

# 4. Business Objectives

## BO-01 — Hỗ trợ researcher từ research question đến research finding

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

## BO-02 — Hỗ trợ tự động chọn phương pháp phân tích phù hợp

AI Agent phải có khả năng:

- hiểu research question;
- xác định variable type;
- sinh candidate methods;
- kiểm tra assumptions;
- chọn method phù hợp;
- fallback sang method khác nếu assumption không đạt.

---

## BO-03 — Hỗ trợ iterative hypothesis refinement

Sau một experiment, agent có thể:

- giữ hypothesis hiện tại;
- reject hypothesis;
- đánh dấu inconclusive;
- sinh hypothesis mới;
- đề xuất experiment tiếp theo.

---

## BO-04 — Tăng khả năng kiểm chứng research finding

Finding quan trọng phải có evidence và provenance.

---

## BO-05 — Bảo vệ dữ liệu nghiên cứu gốc

Dataset gốc không được ghi đè.

Mọi transformation phải tạo version mới.

---

## BO-06 — Giữ human control ở các điểm rủi ro

AI phải yêu cầu researcher xác nhận khi:

- data ambiguity;
- destructive cleaning;
- uncertain business/scientific meaning;
- unclear variable semantics;
- experiment có nhiều lựa chọn có ý nghĩa khác nhau.

---

## BO-07 — Tăng reproducibility

Một experiment phải có đủ metadata để người khác có thể hiểu cách kết quả được tạo ra.

---

## BO-08 — Đánh giá AI Research Agent bằng benchmark và metric định lượng

Platform cần hỗ trợ systematic evaluation và ablation study.

---


## BO-09 — Kiểm soát multiple testing và exploratory research

Platform phải phân biệt confirmatory và exploratory hypothesis, đồng thời theo dõi số lượng phép kiểm thử được thực hiện.

---

## BO-10 — Quản lý dependency và conflicting evidence

Platform phải biểu diễn quan hệ phụ thuộc giữa hypothesis, experiment và finding; đồng thời giữ được evidence trái chiều thay vì loại bỏ.

---

## BO-11 — Đánh giá practical significance thay vì chỉ p-value

Khi phù hợp, platform phải xem xét effect size, confidence interval và uncertainty bên cạnh statistical significance.

---

## BO-12 — Ngăn data leakage và tăng reproducibility

Experiment phải có data split policy khi cần và lưu execution snapshot đủ để tái lập.

---

# 5. Success Metrics

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

---

# 6. Stakeholders

## 6.1. System Administrator

### Mục tiêu

Quản lý hệ thống, user, model và operational monitoring.

### Nhu cầu

- quản lý tài khoản;
- quản lý role và quyền;
- cấu hình AI model;
- xem logs;
- xem usage;
- xem token/cost;
- theo dõi agent failures;
- theo dõi system performance.

---

## 6.2. Research Project Manager

### Mục tiêu

Quản lý research project, dataset, member, experiment history và output.

### Nhu cầu

- tạo research project;
- quản lý member;
- quản lý dataset;
- theo dõi experiment;
- theo dõi finding;
- xem research report;
- xem project summary.

---

## 6.3. Researcher / Data Analyst

### Mục tiêu

Thực hiện nghiên cứu dựa trên dữ liệu với sự hỗ trợ của AI.

### Nhu cầu

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

## 6.4. Reviewer / Stakeholder

### Mục tiêu

Đánh giá output nghiên cứu mà không cần trực tiếp chạy experiment.

### Nhu cầu

- xem research finding;
- xem figure/table;
- xem evidence;
- xem report;
- xem experiment trace;
- gửi feedback.

---

# 7. Current State — As-Is

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

## Pain Points

### P1 — Nhiều thao tác lặp lại

Profiling, cleaning, assumption checking và reporting lặp lại giữa nhiều experiment.

### P2 — Method selection phụ thuộc chuyên môn

Chọn sai test có thể dẫn đến kết luận không hợp lệ.

### P3 — Research iteration khó quản lý

H1 → E1 → H2 → E2 thường bị lưu rời rạc giữa notebook, file và document.

### P4 — Khó phân biệt hypothesis và confirmed finding

AI hoặc researcher có thể diễn giải quá mức một result chưa đủ evidence.

### P5 — Khó truy vết finding

Một finding có thể không rõ được tạo từ experiment nào.

### P6 — Khó tái lập

Thiếu code, dataset version, assumptions hoặc environment làm experiment khó reproduce.

### P7 — Khó đánh giá AI

Không có benchmark thì khó chứng minh agent thực sự chọn method và reason tốt.

---

# 8. Future State — To-Be

```text
Researcher
    ↓
Create/Open Research Project
    ↓
Upload Dataset
    ↓
Automatic Profiling
    ↓
Enter Research Question
    ↓
Define H0 / H1
    ↓
Experiment Planner
    ↓
Generate Candidate Methods
    ↓
Check Assumptions
    ↓
Select / Branch Method
    ↓
Execute Experiment
    ↓
Validate Result
    ↓
Research Finding
    ↓
Generate / Refine Next Hypothesis
    ↓
Next Experiment
    ↓
Stopping Criteria
    ↓
Final Research Findings
    ↓
Figures / Tables
    ↓
Research Report
```

---

# 9. Scope

## 9.1. Core / Must Have

### User & Research Project

- Authentication
- RBAC
- Research project management
- Member management

### Dataset

- Dataset upload
- Dataset validation
- Data profiling
- Data Card
- Data-quality review
- Cleaning proposal
- Human approval
- Dataset versioning

### Research Context

- Research question
- H0 / H1 definition
- Domain context
- Analysis goal
- Optional literature/context notes

### Experimentation

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

### Research Output

- Research finding
- Statistical result
- Figure/table
- Methodology summary
- Limitations
- Research report

### Trust & Reproducibility

- Provenance
- Execution trace
- Experiment history
- Dataset lineage
- Reproducibility metadata
- Reproducibility snapshot
- Downstream invalidation
- Evidence conflict tracking

### Evaluation

- Telemetry
- Benchmark execution
- Method-selection evaluation
- Quantitative metrics
- Ablation study

---

## 9.2. Supporting / Should Have

- Project summary dashboard
- Reviewer view
- Cost monitoring
- Multi-dataset analysis
- Figure reviewer
- Finding validator
- Model configuration
- Research report customization

---

## 9.3. Nice to Have

- Literature connector
- Database connector
- Scheduled experiment
- Collaborative report editing
- Advanced statistical models
- Automatic citation assistance
- More advanced experiment search

---

## 9.4. Out of Scope

- Fully autonomous literature discovery
- Fully autonomous paper publication
- Automatic novelty guarantee
- Training custom foundation models
- Large-scale distributed big data
- Real-time streaming analytics
- Image/audio/video scientific analysis
- Mobile application

---

# 10. Business Requirements

## BR-01 — Authentication

Hệ thống phải cho phép người dùng đăng nhập và truy cập theo danh tính hợp lệ.

---

## BR-02 — Role-Based Access Control

Hệ thống phải phân quyền theo role và project scope.

---

## BR-03 — Research Project Workspace

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

## BR-04 — Dataset Upload

Researcher phải có khả năng upload structured dataset.

Target format:

- CSV;
- XLSX;
- JSON;
- Parquet;
- TSV.

---

## BR-05 — Dataset Validation

Hệ thống phải kiểm tra dataset trước khi sử dụng.

---

## BR-06 — Automatic Dataset Understanding

Hệ thống phải tự hiểu schema, variable type và basic data characteristics.

---

## BR-07 — Data Profiling

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

## BR-08 — Data Quality Review

Researcher phải có khả năng review issue trước experiment.

---

## BR-09 — Cleaning Recommendation

AI phải đề xuất cleaning plan và nêu risk/information loss.

---

## BR-10 — Human Approval

Destructive hoặc semantically risky change phải được user approve.

---

## BR-11 — Original Dataset Preservation

Raw dataset không được ghi đè.

---

## BR-12 — Dataset Versioning

Mỗi transformation phải tạo dataset version mới.

---

## BR-13 — Research Question Definition

Researcher phải có khả năng nhập research question.

---

## BR-14 — Hypothesis Definition

Researcher phải có khả năng định nghĩa:

```text
H0
H1
```

hoặc để agent đề xuất hypothesis draft cần researcher review.

---

## BR-15 — Hypothesis Status

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

## BR-16 — Research Context

Hệ thống phải cho phép lưu:

- domain context;
- variable meaning;
- research goal;
- important assumptions;
- optional prior knowledge.

---

## BR-17 — Experiment Planning

Agent phải tạo experiment plan dựa trên:

- research question;
- hypothesis;
- dataset;
- variable types;
- data quality;
- domain context.

---

## BR-18 — Candidate Method Generation

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

## BR-19 — Assumption Checking

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

## BR-20 — Method Selection

Agent phải chọn method phù hợp dựa trên assumption và research goal.

Nếu assumption không đạt, agent phải:

- chọn alternative method;
- hoặc yêu cầu user clarification;
- hoặc đánh dấu experiment không phù hợp.

---

## BR-21 — Limited Experiment Branching

Khi nhiều method hợp lệ, hệ thống có thể chạy nhiều experiment branch để so sánh.

```text
Experiment
├── Method A
├── Method B
└── Method C
```

---

## BR-22 — Experiment Execution

Agent phải có khả năng thực hiện experiment bằng tool/code được hệ thống kiểm soát.

---

## BR-23 — Self-Correction

Nếu execution lỗi, agent có thể:

```text
Observe Error
→ Revise Code / Plan
→ Retry
```

trong giới hạn cho phép.

---

## BR-24 — Experiment Validation

Sau khi execution thành công, hệ thống phải validate:

- statistical result;
- assumptions;
- output consistency;
- possible data leakage;
- unsupported interpretation.

---

## BR-25 — Replication

Khi cần, experiment có thể chạy nhiều lần hoặc qua nhiều sampling/run để đánh giá stability.

---

## BR-26 — Research Finding Generation

Agent phải chuyển raw experiment result thành research finding dễ hiểu.

---

## BR-27 — Finding Status

Finding phải có status:

```text
Preliminary
Validated
Inconclusive
Rejected
Needs Review
```

---

## BR-28 — Hypothesis Refinement

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

## BR-29 — Experiment-Finding-Hypothesis Linkage

Hệ thống phải lưu quan hệ:

```text
Hypothesis
→ Experiment
→ Finding
→ Next Hypothesis
```

---

## BR-30 — Stopping Criteria

Research loop phải dừng khi:

- research question đã được trả lời đủ mức;
- không còn meaningful hypothesis;
- hết experiment budget;
- hết step/time limit;
- researcher dừng;
- result vẫn inconclusive sau giới hạn cho phép.

---

## BR-31 — Statistical Analysis

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

## BR-32 — Visualization

Agent phải có khả năng tạo figure phù hợp với research question và statistical result.

---

## BR-33 — Figure Review

Hệ thống nên kiểm tra:

- chart type;
- axis labels;
- units;
- legend;
- misleading scale;
- caption consistency;
- figure supports finding.

---

## BR-34 — Research Finding Provenance

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

## BR-35 — Execution Trace

Researcher phải có khả năng xem từng step agent đã thực hiện.

---

## BR-36 — Experiment History

Hệ thống phải lưu experiment history.

---

## BR-37 — Reproducibility Metadata

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

## BR-38 — Research Figure/Table Output

Hệ thống phải hỗ trợ tạo figure/table phục vụ report.

---

## BR-39 — Methodology Summary

Agent phải có khả năng sinh summary mô tả:

- dataset;
- cleaning;
- variables;
- method;
- assumptions;
- experiment procedure.

---

## BR-40 — Limitations

Agent phải hỗ trợ ghi rõ limitations của analysis.

---

## BR-41 — Research Report Generation

Platform phải tạo research report từ validated findings.

---

## BR-42 — Finding Validation

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

## BR-43 — Evaluation Framework

Hệ thống phải có benchmark runner để đánh giá agent.

---

## BR-44 — Benchmark Task Structure

Mỗi task có thể gồm:

- dataset;
- research question;
- hypothesis;
- expected method;
- expected output/ground truth;
- required skills;
- scoring function.

---

## BR-45 — Evaluation Metrics

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

## BR-46 — Agent Configuration Comparison

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
Single Agent
Text-to-Code Baseline
```

---


## BR-47 — Data Split & Leakage Guard

Khi experiment sử dụng predictive/ML workflow, hệ thống phải cho phép hoặc yêu cầu xác định:

- training split;
- validation split;
- test split;
- preprocessing scope;
- feature-selection scope.

Agent không được sử dụng test data để fit preprocessing, select features hoặc tune model nếu research design không cho phép.

---

## BR-48 — Hypothesis Origin Classification

Mỗi hypothesis phải lưu origin:

```text
Initial / Confirmatory
Post-hoc / Exploratory
User-defined
Agent-generated
```

Hypothesis sinh sau khi xem result phải được đánh dấu rõ là post-hoc/exploratory.

---

## BR-49 — Multiple-Testing Control

Khi một workflow thực hiện nhiều hypothesis tests có liên quan, hệ thống phải:

- ghi nhận số lượng tests;
- xác định testing family khi phù hợp;
- đề xuất hoặc áp dụng correction phù hợp;
- lưu correction method;
- lưu cả raw và adjusted significance values khi có.

Ví dụ:

```text
Bonferroni
Holm
Benjamini-Hochberg / FDR
```

---

## BR-50 — Effect Size & Confidence Interval

Khi statistical method hỗ trợ, agent phải báo cáo:

- effect size;
- confidence interval;
- p-value hoặc equivalent evidence measure;
- practical interpretation.

Agent không được dựa duy nhất vào p-value để đưa ra finding mạnh.

---

## BR-51 — Experiment Dependency Graph

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

---

## BR-52 — Downstream Invalidation

Nếu experiment/finding upstream bị:

```text
Rejected
Invalidated
Recomputed
Replaced
```

hệ thống phải đánh dấu các downstream hypothesis/finding bị ảnh hưởng và yêu cầu re-validation khi cần.

---

## BR-53 — Conflicting Evidence Management

Nếu nhiều experiment cho evidence trái chiều, hệ thống phải:

- giữ tất cả result;
- không cherry-pick result thuận lợi;
- đánh dấu trạng thái `Conflicting Evidence`;
- yêu cầu thêm analysis hoặc human review khi cần.

---

## BR-54 — Confidence & Uncertainty Recording

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

## BR-55 — Reproducibility Snapshot

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

# 11. Business Rules

## BRule-01 — Project Isolation

Research project chỉ được truy cập bởi user có quyền.

---

## BRule-02 — Original Dataset Preservation

Raw dataset không được ghi đè.

---

## BRule-03 — Version on Change

Mọi transformation tạo version mới.

---

## BRule-04 — Approval Before Risky Change

Risky cleaning phải được approve.

---

## BRule-05 — Unusual Does Not Mean Incorrect

Anomaly không tự động được coi là lỗi.

---

## BRule-06 — Hypothesis Is Not Fact

Hypothesis mới chưa được experiment xác minh phải được đánh dấu `Unverified`.

---

## BRule-07 — Association Does Not Imply Causation

Agent không được kết luận causation chỉ từ correlation/association nếu design không hỗ trợ causal inference.

---

## BRule-08 — Assumptions Must Be Explicit

Statistical assumptions phải được ghi lại.

---

## BRule-09 — Method Selection Must Be Justified

Agent phải lưu lý do chọn method.

---

## BRule-10 — Finding Must Have Evidence

Validated finding phải có evidence.

---

## BRule-11 — Finding Must Reference Experiment

Mỗi finding phải link về experiment tạo ra nó.

---

## BRule-12 — Experiment Must Reference Dataset Version

Mỗi experiment phải ghi rõ dataset version.

---

## BRule-13 — Interpretation Must Match Statistical Evidence

Agent không được diễn giải mạnh hơn evidence cho phép.

---

## BRule-14 — Human Decision Ownership

Researcher giữ quyền quyết định với các bước có uncertainty cao.

---

## BRule-15 — Reproducibility

Experiment chính thức phải có đủ metadata để tái lập.

---


## BRule-16 — Initial and Post-hoc Hypotheses Must Be Distinguishable

Hypothesis được tạo sau khi quan sát result không được trình bày như hypothesis ban đầu.

---

## BRule-17 — Multiple Testing Must Be Accounted For

Agent không được coi nhiều p-values độc lập như một single-test workflow nếu chúng thuộc cùng testing family.

---

## BRule-18 — Statistical Significance Is Not Practical Significance

Agent phải xem xét effect size và confidence interval khi phù hợp.

---

## BRule-19 — No Data Leakage

Test data không được dùng để fit/tune workflow khi research design yêu cầu holdout evaluation.

---

## BRule-20 — Dependency Must Be Preserved

Downstream hypothesis/finding phải giữ link đến upstream evidence.

---

## BRule-21 — Invalidated Evidence Propagates

Khi upstream evidence bị invalidate, downstream artifacts phải được đánh dấu cần re-validation.

---

## BRule-22 — Conflicting Evidence Must Be Preserved

Agent không được xóa hoặc bỏ qua result trái chiều chỉ vì không phù hợp với hypothesis đang theo đuổi.

---

## BRule-23 — Official Findings Require Reproducibility Snapshot

Finding được đưa vào final research report phải tham chiếu experiment có reproducibility snapshot đầy đủ.

---

# 12. Business Process — Research Setup

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

# 13. Business Process — Experiment Loop

```text
Hypothesis
    ↓
Experiment Planner
    ↓
Generate Candidate Methods
    ↓
Check Assumptions
    ↓
Select Method
    ↓
Execute Experiment
    ↓
Validate Result
    ↓
Generate Finding
    ↓
Finding Conclusive?
   / \
 No   Yes
 │     │
 ▼     ▼
Refine  Generate Next Hypothesis
Method      ↓
 │       New Experiment
 └───────────────┐
                 ↓
           Stopping Criteria
```

---

# 14. Business Process — Hypothesis Refinement

```text
Initial Hypothesis H1
        ↓
Experiment E1
        ↓
Finding F1
        ↓
Generate H2
        ↓
Status: Unverified
        ↓
Experiment E2
        ↓
Finding F2
        ↓
H2:
Supported / Rejected / Inconclusive
```

---

# 15. Business Process — Method Selection

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

# 16. Business Process — Research Finding Verification

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


# 16.1. Business Process — Scientific Validity Guard

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
Evidence Quality Check
      ↓
Finding Status
```

---

# 16.2. Business Process — Dependency & Conflict Handling

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

# 17. Business Process — Evaluation

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

# 18. Assumptions

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

---

# 19. Constraints

- Scope phải phù hợp với capstone.
- Không xây full autonomous AI Scientist.
- Không đảm bảo novelty research tự động.
- Không train foundation model.
- Phải kiểm soát cost.
- Agent output có tính bất định.
- Tool/code execution phải được kiểm soát.
- Research data phải được isolate.
- Experiment history phải được lưu để audit.

---

# 20. Risks & Mitigation

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

---

# 21. Business Benefits

## Cho Researcher

- giảm thao tác lặp;
- hỗ trợ chọn method;
- hỗ trợ assumption checking;
- quản lý experiment loop;
- hỗ trợ hypothesis refinement;
- tạo figure/table nhanh;
- giữ trace và evidence.

## Cho Research Project Manager

- theo dõi research progress;
- quản lý experiment history;
- quản lý dataset version;
- xem findings và report.

## Cho Reviewer

- kiểm tra evidence;
- xem experiment trace;
- review methodology và result dễ hơn.

## Cho Research Evaluation

- benchmark được agent;
- so sánh architecture;
- đo method selection;
- đo reproducibility;
- đo provenance.

---

# 22. Business Acceptance Criteria

Platform được xem là đạt mục tiêu business khi:

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

---

# 23. Traceability Structure

```text
Research Question
      ↓
Hypothesis
      ↓
Experiment
      ↓
Method
      ↓
Execution
      ↓
Finding
      ↓
Evidence Quality
      ↓
Next Hypothesis
      ↓
Dependency / Conflict Check
      ↓
Research Conclusion
```

Và ở cấp requirement:

```text
Business Objective
      ↓
Business Requirement
      ↓
Product Feature
      ↓
User Story
      ↓
Acceptance Criteria
      ↓
Test Case
      ↓
Research Metric / RQ
```

---

# 24. High-Level Product Positioning

> AI Research Experimentation Platform là nền tảng AI Agent hỗ trợ researcher thực hiện vòng lặp nghiên cứu dựa trên dữ liệu: từ research question, hypothesis, method selection và experiment execution đến finding validation, hypothesis refinement và research reporting. Platform tập trung vào evidence, provenance, reproducibility và human control thay vì chỉ trả về câu trả lời dạng black-box.

---

# 25. Product Value Proposition

```text
Research Question
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
Finding Validation
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
Systematic Evaluation
```

---

# 26. Glossary

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

---

# 27. Approval & Sign-off

| Role | Name | Status | Date |
|---|---|---|---|
| Project Leader |  | Pending |  |
| Project Members |  | Pending |  |
| Supervisor |  | Pending |  |

---

# 28. Document Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 |  |  | Initial AI Data Analytics BRD |
| 0.2 |  |  | Reframed toward AI Research Experimentation with iterative hypothesis-experiment loops |
| 0.3 | 2026-09-19 |  | Added scientific-validity controls: multiple testing, post-hoc hypothesis classification, effect size/CI, data leakage guard, dependency graph, conflicting evidence, uncertainty and reproducibility snapshot |
| 1.0 | 2026-09-19 |  | Finalized BRD and aligned with final architecture diagram and iterative research loop |
