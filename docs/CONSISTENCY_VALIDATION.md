# un9flow Consistency Validation

## 目标
建立 docs 为主真源的统一一致性校验体系，使 docs / skills / templates / routing cases / 过程文档可在同一套规则下被检查、分级与收口。

## 一致性校验对象分层

- **Level 1: docs 真源层**
  - `docs/ORCHESTRATION.md`
  - `docs/INCIDENT_WORKFLOW.md`
  - `docs/SKILL_ARCHITECTURE.md`
  - `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
  - 说明：`README.md`、`docs/WORKFLOW.md`、`docs/PLATFORMS.md`、`docs/ROADMAP.md` 等属于 docs 层中的入口/派生/辅助说明文档，受 docs 真源层约束，但不单独承担主真源职责。
- **Level 2: 正式 skills 映射层**
  - 以正式 `skills/**/SKILL.md` 为主，校验其是否严格映射 docs 真源规则。
- **Level 3: 模板层**
  - `docs/templates/consistency-review-checklist.md`：review 执行模板。
  - `docs/templates/validation-findings.md`：findings 记录模板。
  - 说明：模板层以 `docs/templates/**` 为主，校验模板结构是否可承载上层规则。
- **Level 4: 案例层**
  - `docs/templates/skill-routing-matrix.md`：案例层模板。
  - 说明：以 routing cases 与回归案例为主，校验路由解释链是否稳定。
- **Level 5: 过程文档层**
  - 以 spec/plan 等过程文档为主，校验其与真源规则是否历史一致。

## 主真源规则

1. 主真源只在 docs 层。
2. skills 层只能映射，不得反向定义规则。
3. 模板 / 案例 / 过程文档只允许继承或验证，不允许发明新规则。

## 每层校验职责

- **docs：规则完整性**
- **skills：真源映射正确性**
- **模板：结构可承载性**
- **案例：路由可解释性与回归稳定性**
- **过程文档：历史一致性**

## 失败等级

- **L1（阻断级）**：违反主真源规则、破坏层级关系或导致关键规则不可判定。
- **L2（重要级）**：映射偏差、覆盖不全或解释链缺口，影响一致性但可定位修复。
- **L3（整理级）**：命名、排版、引用等整理项，不改变规则语义。

## 处理动作

- **L1**：必须先修，未修不得继续。
- **L2**：原则上本轮修；若不修必须记录为 concern。
- **L3**：可顺手修，不阻断流程。

## 校验顺序

`docs -> skills -> templates -> cases -> 过程文档`

## 当前明确不做

- 自动校验脚本
- CI 校验器
- host-specific 校验流程
