# bringup-path

## 目标
- 面向新板 / 新链路 / 新模块的首次拉通与重复建立过程，先建立确定性基线，再验证链路拉通。

## 适用边界
- 系统尚未建立稳定运行基线。
- 不用于解释现网退化异常。

## 最小输入要求
- 系统阶段
- 板卡/模块信息
- 初始化状态
- 链路状态
- 当前约束与风险边界

## 默认 Phase 骨架
1. `hazard-analysis`
2. `deterministic-foundation`
3. `link-diagnostics`
4. `failsafe-validation`

## 默认 specialist 偏向
- `register-state-auditor`
- `state-machine-tracer`
- `timing-watchdog-auditor`
- `signal-path-tracer`
- `failsafe-convergence-reviewer`

## 主要 Artifact
- `bringup-baseline`
- `link-qualification-log`
- `initial-diagnosis-conclusion`

## 场景特化段
### 建立基线优先说明
- 在未确认确定性行为前不进行深层 root-cause 下推；优先建立可重复、可回归的 `bringup-baseline`。
- `hazard-analysis` 与 `deterministic-foundation` 先约束默认安全态和关键状态机不变量，再进入 `link-diagnostics` 做通路验证。
- 每次拉通动作都按相同收敛口径写入 `link-qualification-log`，以便对比不同版本与硬件批次。
- `initial-diagnosis-conclusion` 只在基线稳定后生成，避免在基线未建立时给出过度诊断。

## 不负责什么
- 不把所有运行期异常都当 incident 解释。
- 不在未建立基线前给过度诊断结论。

## 与总入口 / prompt 契约的关系
- 与总入口决策链路与输入字段约束遵循 `docs/ORCHESTRATION.md`。
- 与场景输入输出字段边界遵循 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`。

## Claude Code 宿主附录
- 新板/新链路/新模块的首次拉通、反复建立动作优先进入本 skill。