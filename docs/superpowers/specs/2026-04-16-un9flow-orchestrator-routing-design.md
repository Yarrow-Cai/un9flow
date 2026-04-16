# un9flow orchestrator 路由与调度设计稿

日期：2026-04-16
主题：围绕 un9flow 的 orchestrator 总外壳，定义三场景并列的主路由、Phase 装配、specialist 分派、控制信号与 prompt 契约骨架

## 1. 设计结论摘要

本轮设计采用如下方向：

- 将 orchestrator 定义为三场景并列的总调度外壳，而不是某一场景的附属控制器
- 当前优先覆盖三个场景：
  - `incident-investigation`
  - `bringup-path`
  - `design-safety-review`
- 主路由判定采用 **证据特征优先**，不以用户措辞作为第一信号
- 调度粒度达到 **specialist 级**，而不是只停留在 Phase 级
- 后续文档落点采用：
  - `docs/ORCHESTRATION.md`：总调度文档
  - `docs/INCIDENT_WORKFLOW.md`：场景专属文档

一句话总结：

> un9flow 的下一阶段，不是继续扩 incident 场景细节，而是先定义一个面向三场景的 orchestrator 总外壳，用统一 case 视图、证据特征优先路由、场景化 Phase 骨架和 specialist 分派，把调度规则固化为可写成 prompt 契约的结构。

---

## 2. orchestrator 总外壳规则

建议将 orchestrator 作为总调度外壳（总 orchestrator）固定为一个承担五项职责的调度外壳：

- 与此一致，`incident-orchestrator` 仅作 `incident-investigation` 场景内调度器示例，不代表总层级唯一名字。

1. 输入归一化
2. 主路由判定
3. Phase 装配
4. specialist 分派
5. 回退 / 升级 / 换轨 / 收敛控制

### 2.1 输入归一化

orchestrator 不直接消费杂乱自然语言，而先将输入整理为统一 case 视图。

建议最小 case 结构：

```text
normalized_case = {
  stated_goal,
  observed_symptoms,
  evidence_inventory,
  current_risk_state,
  system_stage,
  explicit_constraints,
  missing_evidence
}
```

### 2.2 主路由判定

主路由判定采用证据特征优先，而不是先看用户自述标签。

建议输出：

```text
routing_result = {
  primary_scenario,
  secondary_candidates,
  routing_rationale
}
```

### 2.3 Phase 装配

主路由判定后，不直接进入 specialist，而是先装配场景化 Phase 骨架。

### 2.4 specialist 分派

specialist 分派达到 specialist 级，必须显式说明：

- 调用哪个 specialist
- 为什么调它
- 期望产出哪些 Artifact

### 2.5 控制层

控制层负责：

- 回退
- 升级
- 换轨
- 收敛 / 进入 review gate

orchestrator 不是线性推进器，而是调度控制器。

---

## 3. 三场景主路由判定规则

### 3.1 `incident-investigation`

以下证据特征优先判为 `incident-investigation`：

- 系统原本可运行，现在出现异常
- 当前问题更像解释现象、缩小故障半径、寻找根因
- 输入中出现：掉线、CRC 错误、偶发复位、状态卡死、watchdog 异常、采样异常、寄存器异常、failsafe 未收敛

它是 **退化排查型场景**。

### 3.2 `bringup-path`

以下证据特征优先判为 `bringup-path`：

- 系统 / 板卡 / 链路尚未建立稳定运行基线
- 当前目标是首次拉通、初始化、上电、建立确定性运行基线
- 输入中出现：新板、新链路、新模块、初始化失败、首次通信建立失败、配置序列未验证

它是 **系统建立型场景**。

### 3.3 `design-safety-review`

以下证据特征优先判为 `design-safety-review`：

- 当前没有活跃故障排查压力
- 当前目标是审查设计、验证安全边界和收敛路径
- 输入中出现：review、audit、safety、failsafe、limp-home、timeout strategy、watchdog strategy、state machine safety

它是 **方案复核型场景**。

### 3.4 裁决规则

主路由裁决遵循以下顺序：

1. 先看证据模式，不先看用户措辞
2. 区分系统当前处于“建立中”还是“退化中”
3. 区分当前任务是“解释现象”还是“复核方案”
4. 若存在交叉场景，优先选择下一步最可执行的主路由

建议主路由输出不止包含 `primary_scenario`，还要包含次级候选与裁决依据。

---

## 4. 三条 scenario 的 Phase 装配与 specialist 默认分派

### 4.1 `incident-investigation`

默认 Phase 骨架：

```text
hazard-analysis
-> link-diagnostics
-> deterministic-foundation
-> failsafe-validation
```

默认 specialist 集合：

- `signal-path-tracer`
- `register-state-auditor`
- `state-machine-tracer`
- `timing-watchdog-auditor`
- `failsafe-convergence-reviewer`

默认分派偏向：

- 链路 / 采样 / 传播异常显著 -> `signal-path-tracer`
- 配置 / 寄存器异常显著 -> `register-state-auditor`
- 卡态 / 迁移异常显著 -> `state-machine-tracer`
- 超时 / 复位 / watchdog 症状显著 -> `timing-watchdog-auditor`
- 安全收敛异常 -> 强制追加 `failsafe-convergence-reviewer`

### 4.2 `bringup-path`

默认 Phase 骨架：

```text
hazard-analysis
-> deterministic-foundation
-> link-diagnostics
-> failsafe-validation
```

默认 specialist 集合：

- `register-state-auditor`
- `state-machine-tracer`
- `timing-watchdog-auditor`
- `signal-path-tracer`
- `failsafe-convergence-reviewer`

默认分派偏向：

- 初始化序列未稳 -> `register-state-auditor`
- 状态流未拉通 -> `state-machine-tracer`
- 节拍 / timeout / watchdog 基线未建立 -> `timing-watchdog-auditor`
- 通信 / 采样链路不通 -> `signal-path-tracer`
- 准备进入异常验证 -> `failsafe-convergence-reviewer`

### 4.3 `design-safety-review`

默认 Phase 骨架：

```text
hazard-analysis
-> deterministic-foundation
-> failsafe-validation
-> link-diagnostics（按需补）
```

默认 specialist 集合：

- `state-machine-tracer`
- `timing-watchdog-auditor`
- `failsafe-convergence-reviewer`
- `register-state-auditor`
- `signal-path-tracer`（按需）

默认分派偏向：

- 安全态定义不清 -> `state-machine-tracer`
- timeout / watchdog / reset 策略可疑 -> `timing-watchdog-auditor`
- failsafe / limp-home / degrade 定义不完整 -> `failsafe-convergence-reviewer`
- 寄存器配置直接承载安全约束 -> `register-state-auditor`
- 链路健康是安全关键前提 -> 按需加 `signal-path-tracer`

### 4.4 三场景差异的总括

- `incident-investigation`：先缩小故障半径，再解释确定性缺口
- `bringup-path`：先建立确定性基线，再验证链路拉通
- `design-safety-review`：先审风险与收敛结构，再按需补链路诊断

---

## 5. 回退、升级、换轨规则

### 5.1 回退

建议至少存在三类回退：

1. **证据不足回退**
   - 当前 specialist 输出无法支撑进一步判断
   - 需要补观测点、补快照、补状态条件、补时序证据

2. **路由假设失效回退**
   - 新证据推翻了当前主路由判断
   - 例如从 `incident-investigation` 回退并改判为 `bringup-path`

3. **specialist 解释失败回退**
   - 当前 specialist 只能解释局部现象，无法覆盖主要 observed symptoms

### 5.2 升级

建议至少存在三类升级：

1. `incident-investigation` -> `design-safety-review`
2. `bringup-path` -> `design-safety-review`
3. `design-safety-review` -> `incident-investigation`

升级表示问题级别发生变化，不等于简单换轨。

### 5.3 换轨

换轨表示当前目标未变，但主路由判定需要纠正。

例如：
- 初始判为 `incident-investigation`
- 后续确认系统从未建立稳定运行基线
- 换轨到 `bringup-path`

### 5.4 收敛

建议至少满足以下条件才能进入 review gate：

1. 当前主假设能解释主要 observed symptoms
2. 当前未解释项已显式标记
3. 当前 Artifact 已足以支撑 review / 复测 / 复盘

### 5.5 控制信号

建议 orchestrator 显式输出控制信号：

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

---

## 6. orchestrator 的伪代码式决策流骨架

建议总流程：

```text
normalize_input
-> detect_evidence_pattern
-> choose_primary_scenario
-> assemble_phase_backbone
-> dispatch_specialists
-> evaluate_outputs
-> control_decision
-> repeat_or_exit
```

### 6.1 主流程伪代码

```text
function orchestrate(case_input):
    normalized_case = normalize_case(case_input)

    evidence_profile = detect_evidence_pattern(normalized_case)

    routing_result = choose_primary_scenario(
        normalized_case,
        evidence_profile
    )

    phase_plan = assemble_phase_backbone(
        routing_result.primary_scenario,
        normalized_case,
        evidence_profile
    )

    dispatch_plan = dispatch_specialists(
        routing_result.primary_scenario,
        phase_plan,
        evidence_profile,
        normalized_case
    )

    specialist_outputs = run_dispatch_plan(dispatch_plan)

    control_result = evaluate_and_control(
        normalized_case,
        routing_result,
        phase_plan,
        specialist_outputs
    )

    return control_result
```

### 6.2 `normalize_case`

建议输出：

```text
normalized_case = {
  stated_goal,
  observed_symptoms,
  evidence_inventory,
  current_risk_state,
  system_stage,
  explicit_constraints,
  missing_evidence
}
```

### 6.3 `detect_evidence_pattern`

建议输出：

```text
evidence_profile = {
  incident_like_signals,
  bringup_like_signals,
  review_like_signals,
  link_related_signals,
  register_related_signals,
  state_machine_related_signals,
  timing_related_signals,
  failsafe_related_signals
}
```

### 6.4 `choose_primary_scenario`

建议输出：

```text
routing_result = {
  primary_scenario,
  secondary_candidates,
  routing_rationale
}
```

### 6.5 `assemble_phase_backbone`

建议按主场景输出 Phase 骨架，并允许按证据做增删或重排。

### 6.6 `dispatch_specialists`

建议输出：

```text
dispatch_plan = [
  {
    phase,
    specialist,
    dispatch_reason,
    expected_artifacts
  }
]
```

### 6.7 `evaluate_and_control`

建议输出：

```text
control_result = {
  control_signal,
  rationale,
  next_actions,
  unresolved_gaps
}
```

### 6.8 `repeat_or_exit`

根据控制信号决定：

- 继续当前路径
- 补证据
- 重排 specialist
- 换轨
- 升级
- 进入 review gate

---

## 7. prompt 契约骨架与文档落点

### 7.1 prompt 契约骨架

建议 future orchestrator prompt 固定为 4 段输入、4 段输出。

#### 输入段
1. case input
2. normalized case
3. routing context
4. control context

#### 输出段
1. routing result
2. phase plan
3. dispatch plan
4. control result

### 7.2 prompt 的硬约束

建议未来 prompt 固定以下规则：

1. 不允许把用户措辞直接当主路由
2. 不允许跳过 risk framing
3. 不允许把 scenario / phase / specialist / artifact 混成一层
4. 不允许在证据不足时给高置信根因
5. 不允许跳过 review gate 直接收口

### 7.3 文档落点

建议新增：

- `docs/ORCHESTRATION.md`

职责：
- 总调度规则
- 三场景主路由
- Phase 装配
- specialist 分派
- 回退 / 升级 / 换轨
- 伪代码骨架
- prompt 契约骨架

同时保持：

- `docs/INCIDENT_WORKFLOW.md` 作为 incident 场景专属文档

### 7.4 后续验证方式

建议后续配一组路由验证矩阵，至少覆盖：

1. 典型 incident case
2. 典型 bring-up case
3. 典型 review case
4. 交叉 case
5. 换轨 case
6. 升级 case

---

## 8. 最终结论

本轮 orchestrator 设计的推荐方向是：

> 先定义一个面向 `incident-investigation`、`bringup-path`、`design-safety-review` 三场景的 orchestrator 总外壳，再在 `docs/ORCHESTRATION.md` 中固化主路由、Phase 装配、specialist 分派、控制信号和 prompt 契约骨架；其中主路由以证据特征优先，调度粒度达到 specialist 级，并保留回退、换轨、升级与收敛控制。