# un9flow Orchestration

## 目标
- 把 `incident-investigation`、`bringup-path`、`design-safety-review` 三场景的 orchestrator 规则统一为一套可复用、可审查、可继续写成 prompt 契约的文档基线。

## 适用场景
- `incident-investigation`
- `bringup-path`
- `design-safety-review`

## 执行结构（固定）
`Scenario -> Orchestrator -> Phase -> Domain Specialist -> Artifact / Review`

- `Scenario / Phase / Domain Specialist / Artifact` 是命名纪律；
- 当前文档定义的是**总调度外壳**（总 orchestrator）：统一 case、主路由、Phase 装配、specialist 分派与控制信号。
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 负责 prompt 的输入/输出协议与硬约束；`docs/ORCHESTRATION.md` 保持总调度规则主文档。
- `incident-orchestrator` 仅是 `incident-investigation` **场景内调度器示例**，不是三场景共用的总路由名。
- 未来若扩展为更通用名字，可由**总调度外壳**向各 scenario 内调度器下发 phase / dispatch 规则。

## 总调度外壳职责
- 输入归一化：统一 case 输入字段并明确缺口。
- 主路由判定：基于证据特征决定首选场景与可选场景。
- Phase 装配：生成有序的 Phase 骨架并允许在可控条件下重排。
- specialist 分派：按 Phase 分配对应 Domain Specialist。
- 回退/升级/换轨/收敛控制：输出控制信号并驱动下一步。

## 主路由判定
1. **证据特征优先**：以 evidence quality/profile 为首要依据。
2. **三场景主路由规则**：
   - `incident-investigation`
     - 适用表征：系统原本可运行或已达基线后出现异常，关注“现象解释 + 故障半径缩小 + 根因定位”。
     - 典型关键词：掉线、CRC 错误、偶发复位、状态卡死、watchdog 异常、采样异常、寄存器异常、failsafe 未收敛。
     - 目标：在既有运行行为基础上尽快形成主假设并收敛至可验证证据链。
   - `bringup-path`
     - 适用表征：系统/板卡/链路尚未建立稳定运行基线，处于首次拉通或重复建立阶段。
     - 典型场景：新板、新链路、新模块、初始化失败、首次通信建立失败、配置序列未验证。
     - 目标：先确认 deterministic 基线与控制面可重复建立，再逐步引入复杂诊断。
   - `design-safety-review`
     - 适用表征：当前无活跃故障排查压力，关注设计复核与安全边界评估。
     - 典型关键词：review、audit、safety、failsafe、limp-home、timeout strategy、watchdog strategy、state machine safety。
     - 目标：在不引入新故障前提下评估收敛路径、边界策略与交付风险。
3. **冲突时优先下一步最可执行场景**：在多场景信号同强时，优先选当前能直接推进且可闭环的场景。
4. **路由校准**：若下游证据推翻上一步主判定，可触发换轨（目标不变，场景纠偏）。

## 入口路由优先级

### 核心原则
- 显式总调度请求（如“先走总调度 / 先做统一编排 / 让 orchestrator 判定场景”）必须先走 `orchestration`。
- 显式主场景且证据一致时直进子入口。
- 模糊、交叉或跨场景请求时先走 `orchestration`。
- 辅助 skill 不参与全局首路由竞争，仅在 incident 语义上下文中受控进入。

### 优先级顺序
1. 显式总调度请求 -> `orchestration`。
2. 显式主场景且证据一致。
3. 模糊 / 交叉 / 跨场景 -> `orchestration`。
4. 显式辅助 skill 点名（仅在 incident 语义上下文中成立）。
5. 低置信度判断时，宁可走总入口，不误塞子入口。

> 路由判定记录建议使用 `docs/templates/skill-routing-matrix.md`，统一沉淀 case 证据与判定理由。

## 辅助 skill 受控进入规则

### `evidence-pack`
- 只允许：
  1. 用户显式要求先整理证据 / 补证据。
  2. incident 主链明确要求先补证据。
- 禁止：
  - 参与全局主路由竞争。
  - 单独充当 incident 主入口。
  - 在没有 incident 语义时被误当成通用证据整理器。
  - 直接输出根因结论。

### `incident-review`
- 只允许：
  1. 用户显式要求复核当前 incident 结论。
  2. incident 主链已经形成初步结论，准备进入 review gate。
- 禁止：
  - 参与全局主路由竞争。
  - 充当通用 review / audit skill。
  - 替代 `design-safety-review`。
  - 在证据链明显不足时给“通过”结论。

## 默认场景骨架与 specialist 装配

- 5 个 `Domain Specialist` 的输入 / 输出契约、禁止项与回交条件统一见 `docs/DOMAIN_SPECIALIST_CONTRACTS.md`；本文件只定义“何时分派谁”，不重写 specialist 内部协议。

- `incident-investigation`
  - 默认 Phase：`hazard-analysis -> link-diagnostics -> deterministic-foundation -> failsafe-validation`
  - 默认 specialist：
    - `hazard-analysis`：`signal-path-tracer`、`state-machine-tracer`
    - `link-diagnostics`：`signal-path-tracer`
    - `deterministic-foundation`：`register-state-auditor`、`signal-path-tracer`
    - `failsafe-validation`：`timing-watchdog-auditor`、`failsafe-convergence-reviewer`
- `bringup-path`
  - 默认 Phase：`hazard-analysis -> deterministic-foundation -> link-diagnostics -> failsafe-validation`
  - 默认 specialist：
    - `hazard-analysis`：`state-machine-tracer`、`signal-path-tracer`
    - `deterministic-foundation`：`register-state-auditor`、`timing-watchdog-auditor`
    - `link-diagnostics`：`signal-path-tracer`
    - `failsafe-validation`：`failsafe-convergence-reviewer`
- `design-safety-review`
  - 默认 Phase：`hazard-analysis -> deterministic-foundation -> failsafe-validation -> link-diagnostics（按需补）`
  - 默认 specialist：
    - `hazard-analysis`：`signal-path-tracer`、`state-machine-tracer`
    - `deterministic-foundation`：`register-state-auditor`
    - `failsafe-validation`：`failsafe-convergence-reviewer`、`timing-watchdog-auditor`
    - `link-diagnostics（按需）`：`signal-path-tracer`

## 回退 / 升级 / 换轨 / 收敛规则

- 回退（fallback）
  - `fallback-for-more-evidence`：证据不足以支持继续推进时，优先补齐当前场景所需的关键 Artifact / 证据包后再继续。
  - `fallback-route-assumption-invalid`：主路由假设被新证据否定，需要回退并按最新假设重判。
  - `fallback-specialist-explanation-failed`：出现 specialist 解释失败（无可验证假设或证据缺口未闭环）时，回退至更保守诊断步次。
  - `fallback-reorder-specialists`：路由成立但 specialist 输出解释不足，需重排 specialist 执行顺序与问题拆分。
- 升级（upgrade）
  - `upgrade-to-design-safety-review`：当 incident/bringup 调查持续触发设计安全边界反思（如 timeout、watchdog、failsafe 收敛策略偏移）时。
  - `upgrade-to-incident-investigation`：当 design-safety-review 复核未发现新结构性缺陷，但新增故障现象和回归迹象出现时。
  - 规则：`incident-investigation -> design-safety-review`、`bringup-path -> design-safety-review`、`design-safety-review -> incident-investigation`。
- 换轨（reroute）
  - `reroute-to-bringup-path`：目标未变（如恢复稳定运行），但主路由判定应纠正为 `bringup-path`（例如系统尚未有稳定基线）。
  - `reroute-to-incident-investigation`：目标未变（修复可用性/稳定性），但证据指向异常扩散与根因搜索。
- 收敛（convergence）
  - `continue-current-route`：主假设可解释主要症状，且未解释项已显式标记为 `pending`。
  - `artifact` 产出需可支撑 review、复测与复盘。特别是主路径解释、缺口清单与风险边界可追溯。
  - `enter-review-gate`：在关键症状解释闭环、证据缺口可控且输出可被 cross-check 时触发。

## 控制信号
- `continue-current-route`
- `fallback-for-more-evidence`
- `fallback-route-assumption-invalid`
- `fallback-specialist-explanation-failed`
- `fallback-reorder-specialists`
- `reroute-to-bringup-path`
- `reroute-to-incident-investigation`
- `upgrade-to-design-safety-review`
- `upgrade-to-incident-investigation`
- `enter-review-gate`

## prompt 协议锚点

- `prompt` 的输入/输出协议、硬约束与扩展点统一见 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`。
- 本文仅保留总调度外壳规则，不再在本节重复细化协议字段，避免与 contract 成为双重真源。
