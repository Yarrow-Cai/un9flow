---
name: failsafe-convergence-reviewer
description: Review whether the current fault path converges to the intended safety state and identify unsafe persistence risks.
---

# failsafe-convergence-reviewer

## 目标
- 聚焦异常收敛、安全态与降级行为，判断当前故障链是否按预期进入可接受的安全边界。

## 适用边界
- 只作为 `Domain Specialist` 使用，由场景内调度器或主场景 skill 明确分派。
- 默认首先服务 `incident-investigation`，也可被 `bringup-path` 与 `design-safety-review` 复用。
- 不作为总路由入口，不替代主场景 skill。

## 默认落点 Phase
- `failsafe-validation`
- `hazard-analysis`（用于校验默认安全态假设）

## 输入契约
- 当前故障链假设
- 当前安全态信息
- 降级 / 停机 / limp-home 行为
- 当前风险边界与不可突破约束
- 恢复条件、保持条件与收敛预期

## 输出 Artifact
- `failsafe-convergence-note`
- `unsafe-persistence-risk`
- `convergence-expectation-check`

## 不负责什么
- 不替代前置 specialist 的证据采样与定位工作。
- 不把安全审查意见包装成主路由裁决。
- 不在证据不足时宣告系统“安全通过”。
- 不替代 `design-safety-review`。

## 回交条件
- 已明确当前异常是否收敛到安全态，或已明确阻断收敛判断的缺口。

## 与真源文档的关系
- specialist 契约真源见 `docs/DOMAIN_SPECIALIST_CONTRACTS.md`
- 场景内交接边界见 `docs/INCIDENT_WORKFLOW.md`
- 总调度与 phase / dispatch 规则见 `docs/ORCHESTRATION.md`

## Claude Code 宿主附录
- 仅在场景内调度明确分派后进入本 skill。
