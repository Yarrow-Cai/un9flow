# bringup-path 场景真源

本文档是 `bringup-path` 场景的正式真源（single source of truth），定义进入边界、Phase 骨架、specialist 装配、主 Artifact 与输出对齐、canonical bring-up 子焦点，以及 Review Gate / Completion Gate。

## 进入边界与换轨

### 允许直进
- 系统 / 板卡 / 链路尚未建立稳定运行基线。
- 当前目标是首次拉通、初始化、建立确定性基线。

### 不该误进
- 当前问题属于既有系统的运行期退化异常（应走 `incident-investigation`）。
- 用户当前任务本质是设计审查（应走 `design-safety-review`）。

### 应回总入口
- 无法判断当前处于“建立中”还是“退化中”时，回总入口重新裁决。
- 总调度规则与入口路由优先级见 `docs/ORCHESTRATION.md`。

### 换轨信号
- `reroute-to-bringup-path`：目标未变（如恢复稳定运行），但主路由判定应纠正为 `bringup-path`（例如系统尚未有稳定基线）。
- `reroute-to-incident-investigation`：目标未变，但证据指向异常扩散与根因搜索。
- `upgrade-to-design-safety-review`：当 bring-up 调查持续触发设计安全边界反思（如 timeout、watchdog、failsafe 收敛策略偏移）时。

## 默认 Phase 骨架

1. `hazard-analysis`
2. `deterministic-foundation`
3. `link-diagnostics`
4. `failsafe-validation`

Phase 顺序体现了“先安全、再基线、后链路、最后收敛”的 bring-up 逻辑。与 `incident-investigation` 的区别在于：`deterministic-foundation` 优先于 `link-diagnostics`，确保在验证通路前先锁定可重复的安全态与寄存器基线。

## 默认 specialist 装配

| Phase | 默认 specialist |
|-------|-----------------|
| `hazard-analysis` | `state-machine-tracer`、`signal-path-tracer` |
| `deterministic-foundation` | `register-state-auditor`、`timing-watchdog-auditor` |
| `link-diagnostics` | `signal-path-tracer` |
| `failsafe-validation` | `failsafe-convergence-reviewer` |

- specialist 的输入 / 输出契约、禁止项与回交条件统一见 `docs/DOMAIN_SPECIALIST_CONTRACTS.md`。
- 与总入口的调度关系见 `docs/ORCHESTRATION.md`。

## 主 Artifact 与 specialist 输出对齐

| Artifact | 产出阶段 | 说明 |
|----------|----------|------|
| `bringup-baseline` | `deterministic-foundation` | 可重复、可回归的基线记录，包含安全态、寄存器默认值、时序基线。 |
| `link-qualification-log` | `link-diagnostics` | 每次拉通动作按相同收敛口径写入，以便对比不同版本与硬件批次。 |
| `initial-diagnosis-conclusion` | `link-diagnostics` / `failsafe-validation` | 仅在基线稳定后生成，避免在基线未建立时给出过度诊断。 |
| `bringup-path-summary` | 全 Phase 收敛后 | 汇总 bring-up 结论、已确认项、未确认项、下一步建议与风险边界。 |

- 在未确认确定性行为前不进行深层 root-cause 下推；优先建立 `bringup-baseline`。
- `hazard-analysis` 与 `deterministic-foundation` 先约束默认安全态和关键状态机不变量，再进入 `link-diagnostics` 做通路验证。

## canonical bring-up 子焦点

### isoSPI / AFE bring-up
- 对于菊花链 / isoSPI / AFE 的首次拉通，优先使用 `docs/templates/daisy-chain-isospi-afe-bringup-template.md` 固定 bring-up 步骤、观测点、基线判据与升级规则。
- 该模板覆盖：上电、唤醒、基本通信探测、链路寻址 / 枚举、AFE 基本寄存器读回、首次健康检查、基线判据、常见故障特征与升级规则。

### 功率板 bring-up
- 功率板首次上电后的早期 bring-up 示例见 `docs/cases/power-board-bringup-example.md`。
- 该案例演示了从 safety baseline 到 control establishment，再到 escalation decision 的完整串联。

## Review Gate / Completion Gate

### 进入 Review Gate 的条件
- 关键症状解释闭环、证据缺口可控且输出可被 cross-check。
- 主假设可解释主要症状，且未解释项已显式标记为 `pending`。
- 控制信号：`enter-review-gate`。

### Completion Gate 判据
- `bringup-baseline` 已建立且可复现。
- `link-qualification-log` 覆盖目标链路的最小可重复读写条件。
- `initial-diagnosis-conclusion` 已生成，且明确区分“已确认”“未确认”“不支持”三类结论。
- `bringup-path-summary` 已汇总，包含已确认项、未确认项、下一步建议与风险边界。
- 所有升级或换轨决策均有明确触发条件记录。

### 不负责什么
- 不把所有运行期异常都当 incident 解释。
- 不在未建立基线前给过度诊断结论。
- 不替代设计安全审查（`design-safety-review`）的根因闭环。
