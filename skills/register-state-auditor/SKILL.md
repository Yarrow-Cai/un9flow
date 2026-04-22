---
name: register-state-auditor
description: Audit register snapshots and configuration state to identify mismatches, anomalous bitfields, and deterministic gaps.
---

# register-state-auditor

## 目标
- 聚焦寄存器快照、配置位与使能链，识别异常位域、配置偏移与确定性缺口。

## 适用边界
- 只作为 `Domain Specialist` 使用，由场景内调度器或主场景 skill 明确分派。
- 默认首先服务 `incident-investigation`，也可被 `bringup-path` 与 `design-safety-review` 复用。
- 不作为总路由入口，不替代主场景 skill。

## 默认落点 Phase
- `deterministic-foundation`
- `hazard-analysis`（支撑配置风险判断）

## 输入契约
- 寄存器快照
- 关键配置项与使能位
- 默认值 / 目标值 / 当前值
- 异常现象与保护触发背景
- 与寄存器行为直接相关的时序或复位证据

## 输出 Artifact
- `register-bitfield-map`
- `register-anomaly-list`
- `config-mismatch-note`

## 不负责什么
- 不替代路径分段定位。
- 不替代完整状态机迁移分析。
- 不把配置异常直接包装成最终根因结论。
- 不越权定义新的保护策略。

## 回交条件
- 已明确寄存器层异常、配置偏移或当前快照无法解释的位域缺口。

## 与真源文档的关系
- specialist 契约真源见 `docs/DOMAIN_SPECIALIST_CONTRACTS.md`
- 场景内交接边界见 `docs/INCIDENT_WORKFLOW.md`
- 总调度与 phase / dispatch 规则见 `docs/ORCHESTRATION.md`
- 专项方法真源见 `docs/REGISTER_STATE_AUDIT.md`
- 对应输出模板见 `docs/templates/register-state-audit-pack.md`

## Claude Code 宿主附录
- 仅在场景内调度明确分派后进入本 skill。
