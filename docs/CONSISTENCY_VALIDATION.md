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

### bringup-path 场景真源规则

1. `docs/BRINGUP_PATH.md` 是 `bringup-path` 的正式场景真源文档。
2. `docs/BRINGUP_PATH.md` 必须回指：
   - `docs/ORCHESTRATION.md`
   - `docs/DOMAIN_SPECIALIST_CONTRACTS.md`
   - `docs/templates/daisy-chain-isospi-afe-bringup-template.md`
   - `docs/cases/power-board-bringup-example.md`
3. `skills/bringup-path/SKILL.md` 必须回指 `docs/BRINGUP_PATH.md`。
4. `docs/templates/daisy-chain-isospi-afe-bringup-template.md` 与 `docs/cases/power-board-bringup-example.md` 只能作为模板 / 示例承接 bring-up 规则，不得反向承担 `bringup-path` 的场景真源职责。

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

### Claude Code host 接入真源规则

1. `docs/CLAUDE_CODE_HOST.md` 是 Claude Code 的最小 host 接入真源文档。
2. `docs/CLAUDE_CODE_HOST.md` 必须回指：
   - `docs/PLATFORMS.md`
   - `docs/SKILL_ARCHITECTURE.md`
   - `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
3. `docs/CLAUDE_CODE_HOST.md` 必须把 Claude Code 视角下的目录映射固定为以下三层：
   - 直接消费层
   - 真源支撑层
   - 模板 / 案例 / 回归支撑层
4. `docs/CLAUDE_CODE_HOST.md` 必须明确：
   - 当前可消费能力
   - 当前明确不承诺
5. `docs/PLATFORMS.md` 与 `README.md` 必须将 `docs/CLAUDE_CODE_HOST.md` 暴露为 Claude Code host 入口之一。

### Claude Code setup 真源规则

1. `docs/CLAUDE_CODE_SETUP.md` 是 Claude Code 的最小 setup 真源文档。
2. `docs/CLAUDE_CODE_SETUP.md` 必须回指：
   - `docs/CLAUDE_CODE_HOST.md`
   - `docs/PLATFORMS.md`
   - `docs/SKILL_ARCHITECTURE.md`
   - `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
3. `docs/CLAUDE_CODE_SETUP.md` 必须明确：
   - setup 前提
   - 最小 setup 对象
   - 最小 setup 步骤
   - setup 后验证
   - 当前明确不做

### Claude Code skills-only 同步脚本边界规则

1. `tools/sync_claude_code_skills.py` 只允许处理正式 `skills/**/SKILL.md`。
2. `tools/sync_claude_code_skills.py` 不得同步 `docs/**`、`docs/templates/**`、`docs/cases/**`、`docs/golden-outputs/**`、`docs/golden-inputs/**`、`regression` 相关文件或其他非 `SKILL.md` 对象。
3. `tools/sync_claude_code_skills.py` 必须支持以下最小参数：
   - `--target-root`
   - `--inspect`
   - `--dry-run`
   - `--force`
4. `tools/sync_claude_code_skills.py --inspect` 只允许执行静态盘点，不得写文件、不得创建目录、不得执行复制等实际同步动作。
5. `--inspect` 必须与 `--dry-run`、`--force` 互斥，不允许组合使用。
6. 目标路径必须按来源相对路径稳定镜像；同一来源 `skills/**/SKILL.md` 在同一 `--target-root` 下必须得到稳定且可预测的目标路径。
7. `--dry-run` 必须输出稳定同步计划，`--force` 必须覆盖已存在目标文件，且脚本必须显式输出最小 summary 行为，便于 host 侧验证同步结果。
8. `tools/sync_claude_code_skills.py --only <skill-name>` 只允许按 skill 目录名精确匹配一个正式 skill；`<skill-name>` 必须与某个正式 `skills/<skill-name>/SKILL.md` 的目录名完全一致。
9. `--only` 不得支持多个值、按组过滤、路径模式过滤或 exclude；该参数的语义边界固定为“只精确点名一个正式 skill”。
10. 当 `--only` 未命中任何正式 skill 时，脚本必须硬失败，并显式输出当前可用 formal skill 列表，禁止静默跳过、自动回退为全量同步或仅给出模糊错误。
11. `tools/sync_claude_code_skills.py --stale-check` 只允许扫描目标目录中的 `skills/**/SKILL.md`，不得把目标目录下的其他文件或非 `SKILL.md` 对象纳入 stale 判定范围。
12. `--stale-check` 只允许输出 `managed` / `stale` 两类状态，并提供最小 summary；不得扩展为 repair、sync、diff、warning 分类或其他处置建议。
13. `--stale-check` 不得提供 prune 建议、不得执行删除，也不得以任何形式修改目标目录内容。
14. `--stale-check` 必须与 `--inspect`、`--dry-run`、`--force`、`--only` 互斥，不允许组合使用。
15. `tools/sync_claude_code_skills.py --prune-advice` 只允许针对 `stale` 对象输出最小建议；不得重复列出 `managed` 清单，也不得把 `managed` 对象混入 prune advice 输出。
16. `--prune-advice` 只允许输出 `advice: consider-cleanup` 这一种最小建议，不得扩展为其他 advice 类型、不得附带 repair / sync / delete 类动作建议。
17. `--prune-advice` 不得输出删除命令、不得执行删除，也不得以任何形式修改目标目录内容。
18. `--prune-advice` 必须与 `--stale-check`、`--inspect`、`--dry-run`、`--force`、`--only` 互斥，不允许组合使用。

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
