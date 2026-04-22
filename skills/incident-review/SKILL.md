---
name: incident-review
description: Provide a second-opinion review of the current incident evidence chain before closure or escalation.
---

# incident-review

## 目标
- 作为 incident 辅助 skill，对当前 incident 诊断链路执行 second opinion 与收口前复核，重点检查 evidence 到结论链的一致性与可复核性。

## 仅适用于哪个场景
- 主要服务场景：`incident-investigation`。
- 不作为总 review skill，不替代 incident 场景内调度与总调度职责。

## 进入限制
### 只允许
1. 用户显式要求复核 incident 结论。
2. `incident` 主链进入 review gate 前触发。

### 不允许
- 参与全局主路由竞争。
- 充当通用 review / audit skill。
- 替代 `design-safety-review`。

## 何时应使用
- 用户显式要求复核 incident 结论。
- `incident` 主链进入 review gate 前触发。
- 以上两类情形之外，即使需要 second opinion，也应先由主场景判断是否进入本 skill。

## 输入要求
- `incident-diagnosis-pack`
- 各 specialist 输出
- 当前未解释项
- 当前风险判断

## 输出 Artifact
- `incident-review-memo`
- `confidence-gap-summary`
- `recommended-next-action`

## 何时返回主场景
- 若复核发现缺口、逻辑断裂或风险被低估，退回 `incident-investigation`。
- 若复核通过，允许进入收口（例如 `incident` 收束与对外交付）。

## 不负责什么
- 不替代总调度，不替代 `design-safety-review`。
- 不在证据明显不足时直接给出“审批通过”结论。

## Claude Code 宿主附录
- 仅在用户显式要求复核 incident 结论，或 incident 主链进入 review gate 前触发时进入本 skill。
