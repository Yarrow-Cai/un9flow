# un9flow Consistency Validation

## 目标
建立 docs 为主真源的统一一致性校验体系，使 docs / skills / templates / routing cases / 过程文档可在同一套规则下被检查、分级与收口。

## 一致性校验对象分层

- **Level 1: docs 真源层**
  - `docs/ORCHESTRATION.md`
  - `docs/INCIDENT_WORKFLOW.md`
  - `docs/SKILL_ARCHITECTURE.md`
  - `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
  - `docs/TEMPLATE_GENERATION.md`
  - 说明：`README.md`、`docs/WORKFLOW.md`、`docs/PLATFORMS.md`、`docs/ROADMAP.md` 等属于 docs 层中的入口/派生/辅助说明文档，受 docs 真源层约束，但不单独承担主真源职责。
  - 说明：模板生成体系不单独拆出新的校验分层；`docs/TEMPLATE_GENERATION.md` 仍属于 docs 真源层，`tools/generation_core.py` 与接入生成脚本属于受该真源约束的实现对象，CLI 只按现有分层口径校验，不新增 `generation_system` 层。
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

## Domain Specialist 方法真源规则

1. Domain Specialist 的独立方法真源文档（例如 `docs/WATCHDOG_TIMEOUT_AUDIT.md`、`docs/REGISTER_STATE_AUDIT.md`）属于 docs 层受控对象。
2. 若某个 Domain Specialist 存在独立方法真源，该方法真源文档必须回指：
   - `docs/DOMAIN_SPECIALIST_CONTRACTS.md`
   - 至少一个复用该方法的主场景文档
   - 对应的 `docs/templates/*-pack.md`
3. 对应的 `skills/**/SKILL.md` 必须回指该方法真源文档。
4. 对应的 `docs/templates/*-pack.md` 必须回指该方法真源文档。

### Register 方法真源规则（register-state-auditor）

1. `docs/REGISTER_STATE_AUDIT.md` 是 `register-state-auditor` 的方法真源文档。
2. `docs/REGISTER_STATE_AUDIT.md` 必须回指：
   - `docs/DOMAIN_SPECIALIST_CONTRACTS.md`
   - `docs/INCIDENT_WORKFLOW.md`
   - `docs/DESIGN_SAFETY_REVIEW.md`
   - `docs/templates/register-state-audit-pack.md`
3. `skills/register-state-auditor/SKILL.md` 必须回指 `docs/REGISTER_STATE_AUDIT.md`。
4. `docs/templates/register-state-audit-pack.md` 必须回指 `docs/REGISTER_STATE_AUDIT.md`。
5. `README.md` 必须将 `docs/REGISTER_STATE_AUDIT.md` 暴露为仓库文档入口之一。

### ISR / main loop 冲突归属规则（timing-watchdog-auditor）

1. `isr-mainloop-conflict-note` 是 `timing-watchdog-auditor` 的 canonical Artifact，不单独派生新的 `Domain Specialist`。
2. `docs/WATCHDOG_TIMEOUT_AUDIT.md` 必须显式包含 `ISR / main loop 职责冲突` 专项说明。
3. `skills/timing-watchdog-auditor/SKILL.md` 必须显式声明 ISR / main loop 冲突检查属于该能力线内的 `线内专项扩展`。
4. `docs/templates/timing-watchdog-audit-pack.md` 必须为 `isr-mainloop-conflict-note` 提供专属证据字段，至少包含：
   - `- ISR 侧职责:`
   - `- main loop 侧职责:`
   - `- 被破坏的确定性约束:`
   - `- 可能导致的 reset / timeout / 饥饿风险:`
   - `- 仍缺的证据:`
5. `docs/DOMAIN_SPECIALIST_CONTRACTS.md` 必须说明该 Artifact 归属 `timing-watchdog-auditor`，并声明 `不得拆成新的 specialist`。

### Watchdog formal skill / findings / report / generator 归属规则

1. `skills/watchdog-timeout-audit/SKILL.md` 是 watchdog / timeout 的正式专项 skill 入口，不作为新的主场景，也不作为新的 `Domain Specialist`。
2. `skills/watchdog-timeout-audit/SKILL.md` 必须回指：
   - `docs/WATCHDOG_TIMEOUT_AUDIT.md`
   - `docs/templates/timing-watchdog-audit-pack.md`
   - `docs/templates/watchdog-timeout-audit-findings.md`
3. `docs/templates/watchdog-timeout-audit-findings.md` 是 watchdog / timeout 的轻量 findings 模板。
4. `docs/templates/watchdog-timeout-audit-findings.md` 必须回指：
   - `docs/WATCHDOG_TIMEOUT_AUDIT.md`
   - `skills/watchdog-timeout-audit/SKILL.md`
5. `docs/templates/watchdog-timeout-audit-report.md` 是 watchdog / timeout 的最终专项报告模板。
6. `docs/templates/watchdog-timeout-audit-report.md` 必须回指：
   - `docs/WATCHDOG_TIMEOUT_AUDIT.md`
   - `docs/templates/watchdog-timeout-audit-findings.md`
   - `docs/templates/timing-watchdog-audit-pack.md`
7. `docs/templates/watchdog-timeout-audit-report.md` 必须包含以下二级标题锚点（精确匹配 `## <小写段名>`）：
   - `## audit summary`
   - `## key findings`
   - `## evidence highlights`
   - `## risk assessment`
   - `## recommended actions`
   - `## verification gaps`
8. `tools/generate_watchdog_timeout_audit_report.py` 是 watchdog 自动报告生成器脚本。
9. `tools/generate_watchdog_timeout_audit_report.py` 必须显式依赖：
   - `docs/templates/watchdog-timeout-audit-findings.md`
   - `docs/templates/timing-watchdog-audit-pack.md`
   - `docs/templates/watchdog-timeout-audit-report.md`
10. `tools/generate_watchdog_timeout_audit_report.py` 必须体现：
   - findings 为主输入
   - pack 为补充输入
   - 输出为 markdown 报告文件
11. `docs/WATCHDOG_TIMEOUT_AUDIT.md` 必须补充对 watchdog formal skill、findings 模板、report 模板与报告生成器脚本的回指。

### Watchdog workflow 真源规则

1. `docs/WATCHDOG_TIMEOUT_WORKFLOW.md` 是 watchdog / timeout 的流程真源文档。
2. `docs/WATCHDOG_TIMEOUT_WORKFLOW.md` 必须回指：
   - `docs/WATCHDOG_TIMEOUT_AUDIT.md`
   - `skills/watchdog-timeout-audit/SKILL.md`
   - `docs/templates/watchdog-timeout-audit-checklist.md`
   - `docs/templates/timing-watchdog-audit-pack.md`
   - `docs/templates/watchdog-timeout-audit-findings.md`
   - `docs/templates/watchdog-timeout-audit-report.md`
   - `tools/generate_watchdog_timeout_audit_report.py`
3. `docs/WATCHDOG_TIMEOUT_WORKFLOW.md` 必须显式声明：
   - 不是新的主场景
   - 不是新的 `Domain Specialist`
   - 默认服务 `design-safety-review`
   - 可被 `incident-investigation` / `bringup-path` 复用
   - 固定顺序：`checklist → pack → findings → report`

### 模板生成体系真源规则

1. `docs/TEMPLATE_GENERATION.md` 是模板生成体系的约定真源，归属 docs 真源层。
2. `tools/generation_core.py` 是模板生成体系的共享生成内核，属于受 docs 真源层约束的实现对象。
3. `docs/TEMPLATE_GENERATION.md` 至少必须明确：
   - 允许被生成的对象
   - 输入最小集合
   - 输出文件命名规则
   - 生成器输入/输出责任
   - 缺字段时的处理原则
   - 单文件 / bundle 输出约定
4. `tools/generation_core.py` 至少必须包含或体现：
   - `read_text`
   - `write_text`
   - `replace_fields`
5. 被纳入模板生成体系的脚本必须显式回指：
   - `docs/TEMPLATE_GENERATION.md`
   - `tools/generation_core.py`
   - 自己服务的模板或对象
6. 首批接入对象至少包括：
   - `tools/generate_incident_case_bundle.py`
   - `tools/generate_watchdog_timeout_audit_report.py`
7. 首批接入对象必须能说明：
   - 输入是什么
   - 输出是什么
   - 输出是单文件还是 bundle
8. 对 `tools/generate_incident_case_bundle.py` 与 `tools/generate_watchdog_timeout_audit_report.py` 的校验，除对象锚点外，还必须检查：
   - 是否显式回指 `docs/TEMPLATE_GENERATION.md`
   - 是否显式回指 `tools/generation_core.py`
   - 是否显式说明“输入是什么 / 输出是什么 / 输出是单文件还是 bundle"

## 每层校验职责

- **docs：规则完整性**
- **skills：真源映射正确性**
- **模板：结构可承载性**
- **案例：路由可解释性与回归稳定性**
- **过程文档：历史一致性**

## Generation regression 定位

1. generation regression 用于校验“给定输入 → 生成输出”是否稳定，确保 docs 真源约束下的生成结果不会无意漂移。
2. 首批仅覆盖以下生成对象：
   - `watchdog-timeout-audit-report`
   - `incident case bundle`
3. golden files 允许在本地通过显式刷新方式更新，用于开发者确认预期输出已按新规则收敛；CI 中只允许 `check-only` 模式，不允许在门禁中直接刷新 golden files。
4. generation regression 不替代 consistency validation；前者负责输出稳定性回归，后者负责 docs / skills / templates / cases / 过程文档的一致性校验，两者并列服务 docs 真源。

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

- host-specific 校验流程
- 独立于现有 consistency / generation regression 门禁之外的新校验平台层
- 自动批准或自动刷新 golden 变更的 CI 流程
