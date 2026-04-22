# un9flow embedded specialist extension 设计稿

日期：2026-04-22
主题：围绕 `timing-watchdog-auditor`、`register-state-auditor` 与 ISR / main loop 职责冲突检查，定义 v5 第一批 embedded specialist 扩展的统一骨架与 3 个子计划拆分方式。

## 1. 设计结论摘要

本轮设计固定采用 **统一骨架 + 3 个子计划** 的推进方式，而不是把 3 条子线各自独立长成不同体系。

设计结论如下：

- docs 继续作为唯一主真源，skills / templates / validation / CI 只做映射、承载与检查。
- `timing-watchdog-auditor` 作为 v5 第一条完整闭环能力线推进：补齐 formal skill 映射、专项方法、模板承接、一致性校验与最小 CI 纳管关系。
- `register-state-auditor` 作为第二条 embedded specialist 能力线推进：在现有 specialist 契约与 pack 模板基础上，补齐寄存器审计方法真源与更强的证据约束。
- ISR / main loop 职责冲突检查 **不新开独立 specialist**，而是作为 `timing-watchdog-auditor` 线内的专项扩展能力推进，避免与 timing / watchdog 线重叠。
- 本轮交付物固定为：**1 份总设计 + 3 个子计划**。本轮不直接要求把 3 条子线全部实现完。

一句话总结：

> 先把 v5 的 embedded specialist 扩展做成一套同源、同命名、同校验骨架，再按 watchdog 闭环、register audit 补齐、ISR 冲突专项扩展这 3 条子线分计划推进。

---

## 2. 当前状态与问题

仓库当前已经具备以下基础：

- `docs/DOMAIN_SPECIALIST_CONTRACTS.md` 已定义第一批 5 个 `Domain Specialist` 的输入 / 输出契约。
- `skills/timing-watchdog-auditor/SKILL.md` 与 `skills/register-state-auditor/SKILL.md` 已存在。
- `docs/templates/timing-watchdog-audit-pack.md` 与 `docs/templates/register-state-audit-pack.md` 已存在。
- `docs/WATCHDOG_TIMEOUT_AUDIT.md` 已作为 watchdog / timeout 专项方法真源落地。
- `tools/validate_consistency.py` 与 `.github/workflows/consistency-validation.yml` 已提供最小一致性门禁骨架。

但 v5 仍存在 3 个明显缺口：

1. `timing-watchdog-auditor` 现有内容更接近“已命名 specialist + 已有模板”，还没有被明确收束成一条可复用、可校验、可纳管的专项能力闭环。
2. `register-state-auditor` 虽有契约与 pack 模板，但仍缺少与 watchdog 对应级别的专项方法真源，导致“如何审计、如何回交、如何被 consistency 检查”还不够硬。
3. ISR / main loop 职责冲突检查已经在 watchdog specialist 的输出中出现，但还没有被固定为该能力线内的专项扩展规则，后续容易漂成单独能力或与 timing / state-machine 边界打架。

因此，本轮设计的核心不是再发明新的入口，而是把已有 v5 扩展方向收敛成一套稳定骨架。

---

## 3. 设计目标

本轮总设计只解决以下问题：

1. **统一骨架**：定义这 3 条子线如何在 docs / skills / templates / consistency / CI 层保持同一套边界与命名纪律。
2. **子线拆分**：把 Top 3 优先项拆成 3 个可执行子计划，避免一次性做成范围失控的大杂烩。
3. **边界收敛**：明确 ISR / main loop 冲突检查挂在哪条线下，避免重复定义 specialist。
4. **最小纳管**：保证后续实施完成后，新增或补强内容可以被当前 consistency CLI 和 GitHub workflow 纳入检查。

本轮不解决安装分发、多 host 扩展、artifact 自动语义判定或示例实战案例。

---

## 4. 明确不做

为了避免 v5 扩展变成第二套体系，本轮明确不做以下事项：

- 不新增新的 `Scenario` 入口。
- 不新增独立 `incident` 之外的总调度器。
- 不把 ISR / main loop 职责冲突检查做成新的独立 `Domain Specialist`。
- 不把 consistency validation 扩成自动判定 artifact 内容正确性的语义引擎。
- 不在本轮引入安装器、分发器或 host-specific prompt 绑定实现。
- 不引入 RTOS 依赖、动态内存假设或与当前 deterministic 方针相冲突的设计前提。

---

## 5. 统一骨架设计

### 5.1 层级关系

本轮继续保持现有 5 层执行结构与 4 层命名纪律：

- 执行结构：`Scenario / Orchestrator / Phase / Domain Specialist / Artifact`
- 命名纪律：`Scenario / Phase / Domain Specialist / Artifact`

新增或补强内容必须遵守：

- docs 负责定义规则；
- `skills/**/SKILL.md` 只负责把规则映射成宿主可消费入口；
- `docs/templates/**` 只负责承接 Artifact 结构；
- `tools/validate_consistency.py` 与 CI 只负责检查规则映射，不负责发明规则。

### 5.2 共用约束

3 条子线统一遵守以下约束：

1. 每条 specialist 能力线都必须显式说明：
   - 输入证据基线
   - primary artifacts
   - confidence
   - unresolved gaps
   - evidence backlinks
   - next suggestion for orchestrator
2. 每个在 specialist 中声明的 primary artifact，都必须有稳定承载方式：
   - 要么在对应 `*-pack.md` 中有明确章节；
   - 要么在方法真源文档中被明确锚定，并由 pack 模板引用。
3. specialist 不得越权升级为 `Scenario`、`Phase` 或主路由入口。
4. 证据不足时必须输出保守判断与缺口，不得伪装成高置信结论。

### 5.3 文档真源策略

本轮统一采用以下真源策略：

- specialist 契约真源继续由 `docs/DOMAIN_SPECIALIST_CONTRACTS.md` 承担。
- 若某条子线需要“如何审计”的专项方法真源，则新增或扩展对应 docs 文档；方法真源负责定义检查维度、失败态与回交原则。
- `SKILL.md` 不负责定义新规则，只负责把真源中的边界、输入输出和适用范围映射出来。

### 5.4 consistency / CI 统一纳管规则

后续实施阶段必须让 3 条子线都能落入统一纳管规则：

- consistency 需要能检查 specialist 契约、skill、template、方法真源之间的名称与角色映射是否一致；
- consistency 需要能发现新增专项能力是否越权变成新的 `Scenario` 或新 specialist；
- CI 继续沿用现有最小门禁模式，只扩覆盖范围，不扩成复杂多 job 流程。

本轮总设计不要求直接实现这些检查，但子计划必须明确这些检查点会落到哪里。

---

## 6. 子计划 A：`timing-watchdog-auditor` 正式闭环

### 6.1 定位

这一子计划的目标，是把 `timing-watchdog-auditor` 从“已有 contract + skill + pack + watchdog 方法文档”推进成 v5 第一条完整闭环能力线。

### 6.2 现有基础

当前已存在：

- `docs/DOMAIN_SPECIALIST_CONTRACTS.md` 中的 `timing-watchdog-auditor` 契约
- `skills/timing-watchdog-auditor/SKILL.md`
- `docs/templates/timing-watchdog-audit-pack.md`
- `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- `docs/templates/watchdog-timeout-audit-checklist.md`

### 6.3 这条线要补齐什么

子计划 A 需要补齐以下内容：

1. 把 `docs/WATCHDOG_TIMEOUT_AUDIT.md` 与 specialist 契约、pack 模板的关系写硬，而不是只并列存在。
2. 明确 watchdog / timeout 专项方法与 `timing-watchdog-auditor` 的角色分工：
   - 方法真源回答“审什么、为什么审、失败态是什么”；
   - specialist pack 回答“这次 dispatch 实际产出了什么、证据链是什么、下一步建议是什么”。
3. 把 ISR / main loop 职责冲突检查正式收编进这条线，而不是额外新开能力入口。
4. 为后续 consistency 校验提供可检查锚点：技能名、artifact 名、模板章节名、方法真源引用关系必须可定位。

### 6.4 完成后的目标状态

完成后，这条线应达到：

- 用户可以在 `timing-watchdog-auditor` 上看到明确 specialist 边界；
- 维护者可以在 `docs/WATCHDOG_TIMEOUT_AUDIT.md` 中看到方法真源；
- reviewer 可以通过 pack 模板复核具体输出物；
- consistency / CI 可以检查命名、映射与边界是否漂移。

---

## 7. 子计划 B：`register-state-auditor` 能力补齐

### 7.1 定位

这一子计划的目标，是把 `register-state-auditor` 从“已有契约与 pack 模板”推进到具备专项方法真源、强证据约束与稳定纳管边界的 embedded specialist 能力线。

### 7.2 现有基础

当前已存在：

- `docs/DOMAIN_SPECIALIST_CONTRACTS.md` 中的 `register-state-auditor` 契约
- `skills/register-state-auditor/SKILL.md`
- `docs/templates/register-state-audit-pack.md`

### 7.3 推荐方法真源落点

本轮设计建议为寄存器审计新增独立方法真源文档：

- `docs/REGISTER_STATE_AUDIT.md`

原因是：

- 当前 contract 只说明输入 / 输出与禁止项，但没有把“寄存器审计到底如何展开”写成可 review 的方法骨架；
- register audit 在 embedded 场景中是高频专项，不应长期只靠 contract 段落隐式承载；
- 单独方法真源更利于与 `timing-watchdog-auditor` 对齐，而不是让两条能力线的文档成熟度失衡。

### 7.4 这条线要补齐什么

子计划 B 需要补齐以下内容：

1. 固定寄存器审计的专项检查维度，至少覆盖：
   - 默认值 / 目标值 / 当前值 / 复位后值
   - 关键使能位与保护位
   - sticky flag / latch / write-clear / shadow register 等容易误判的位语义
   - 配置偏移、初始化缺口与复位回返风险
2. 明确方法真源、specialist contract 与 pack 模板之间的映射关系。
3. 为后续 consistency 校验提供硬锚点，避免 `register-bitfield-map`、`register-anomaly-list`、`config-mismatch-note` 只停留在模板命名层。
4. 明确该能力线在 `incident-investigation`、`bringup-path`、`design-safety-review` 三类场景中的复用边界。

### 7.5 完成后的目标状态

完成后，这条线应达到：

- 寄存器审计不再只是“有一个 specialist 名称和 pack 模板”；
- reviewer 可以依据方法真源判断产物是否缺项；
- consistency / CI 可以检查寄存器审计线的命名与映射是否稳定。

---

## 8. 子计划 C：ISR / main loop 职责冲突检查专项扩展

### 8.1 定位

这一子计划不是新 specialist，也不是新场景，而是 `timing-watchdog-auditor` 线内的专项扩展。

### 8.2 为什么不单独成线

本轮明确不把 ISR / main loop 职责冲突检查做成独立 specialist，原因有 3 个：

1. 当前 `timing-watchdog-auditor` 的输入已经包含节拍信息、ISR / main loop 责任划分、timeout / watchdog 行为。
2. 当前 `timing-watchdog-auditor` 的输出已经包含 `isr-mainloop-conflict-note`。
3. 若再新开独立 specialist，极易与 timing / watchdog 分析、状态机追踪和 design review 发生职责重叠。

### 8.3 这条子计划要补齐什么

子计划 C 需要把以下判断固定为 watchdog 线内专项检查：

- ISR 是否承担了本不应在中断上下文完成的状态推进或耗时动作；
- main loop 是否承担了本应由固定节拍或硬约束触发的关键动作；
- 是否存在无超时保护等待、错误的喂狗责任划分或“系统失活但仍能喂狗”的路径；
- 这些冲突如何映射到 reset、timeout、调度抖动或 failsafe 失效风险。

### 8.4 文档落点策略

本轮默认不新增独立 `docs/ISR_MAINLOOP_CONFLICT_CHECK.md`。

推荐做法是：

- 在 `docs/WATCHDOG_TIMEOUT_AUDIT.md` 中补足 ISR / main loop 冲突检查的专项小节；
- 在 `docs/templates/timing-watchdog-audit-pack.md` 中把 `isr-mainloop-conflict-note` 的证据要求写得更硬；
- 在 consistency 校验中把该 artifact 与 `timing-watchdog-auditor` 绑定。

只有当后续证明该专项已经稳定脱离 watchdog / timeout 边界时，才考虑独立拆文档或单独扩能力名。

### 8.5 完成后的目标状态

完成后，这条子计划应达到：

- ISR / main loop 冲突检查有稳定归属；
- 不会和 `state-machine-tracer`、`register-state-auditor`、`design-safety-review` 发生命名和职责重叠；
- reviewer 能明确知道这项检查应由 watchdog 线承担，而不是额外发明新 specialist。

---

## 9. 3 个子计划的拆分关系

本轮固定采用以下拆分方式：

### 子计划 1：watchdog / timeout 正式闭环
聚焦：先做出 v5 第一条“方法真源 + specialist + template + consistency + CI 接点”完整路径。

### 子计划 2：register audit 能力补齐
聚焦：补齐与 watchdog 对齐级别的方法真源和强证据约束，让第二条能力线成形。

### 子计划 3：ISR / main loop 冲突检查专项扩展
聚焦：把 ISR / main loop 冲突检查正式收编进 watchdog 线，并固定其证据要求与边界。

拆分原则是：

- 子计划 1 优先，因为它是最短闭环路径；
- 子计划 2 其次，因为它是第二条硬能力线；
- 子计划 3 虽然排第 3，但结构上挂在子计划 1 下面，实施时可以与子计划 1 紧耦合推进。

---

## 10. 验证策略

本轮总设计要求后续子计划在实施时至少满足以下验证策略：

1. docs 真源、specialist contract、skill、template 之间的名称与角色映射可以被 `tools/validate_consistency.py` 检查。
2. 现有 `.github/workflows/consistency-validation.yml` 不需要大改架构，只需要覆盖新增或补强的映射检查点。
3. 任一子计划完成后，都应能够通过本地 consistency validation，而不是只在文档文字上“看起来合理”。
4. ISR / main loop 冲突检查的归属必须可验证地落在 `timing-watchdog-auditor` 线内，而不是靠口头约定。

---

## 11. 最终结论

本轮推荐方向固定为：

> 先用一份总设计把 v5 的 embedded specialist 扩展骨架钉稳，再拆成 3 个子计划推进：`timing-watchdog-auditor` 正式闭环、`register-state-auditor` 能力补齐，以及挂在 watchdog 线内的 ISR / main loop 职责冲突检查专项扩展。

这个方向的核心价值不在于一次性把所有能力都铺开，而在于先保证新增能力继续服从 `un9flow` 已经建立的 deterministic、incident-first、docs-as-source 纪律。