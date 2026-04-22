---
name: signal-path-tracer
description: Trace communication, sampling, and control paths to segment failure propagation and prioritize the most suspicious links.
---

# signal-path-tracer

## 目标
- 聚焦通信 / 采样 / 控制路径的分段定位，缩小故障半径并给出下一轮观测点。

## 适用边界
- 只作为 `Domain Specialist` 使用，由场景内调度器或主场景 skill 明确分派。
- 默认首先服务 `incident-investigation`，也可被 `bringup-path` 与 `design-safety-review` 复用。
- 不作为总路由入口，不替代主场景 skill。

## 默认落点 Phase
- `hazard-analysis`
- `link-diagnostics`
- `deterministic-foundation`（支撑定位）

## 输入契约
- `incident-summary` 中的症状描述
- `evidence-package` 中与通信 / 采样 / 控制路径相关的证据
- 路径拓扑、器件分段、板级连接关系
- 波形观测点、链路状态、收发错误或掉线证据
- 当前风险边界与安全态假设

## 输出 Artifact
- `segmented-failure-path`
- `observability-point-list`
- `path-suspicion-ranking`

## 不负责什么
- 不替代寄存器配置审计。
- 不替代状态迁移追踪。
- 不直接给出最终根因定论。
- 不修改 Scenario 路由、Phase 次序或 review 结论。

## 回交条件
- 已明确主要可疑路径段，或已明确下一轮必须补的观测点与链路证据。

## 与真源文档的关系
- specialist 契约真源见 `docs/DOMAIN_SPECIALIST_CONTRACTS.md`
- 场景内交接边界见 `docs/INCIDENT_WORKFLOW.md`
- 总调度与 phase / dispatch 规则见 `docs/ORCHESTRATION.md`

## Claude Code 宿主附录
- 仅在场景内调度明确分派后进入本 skill。
