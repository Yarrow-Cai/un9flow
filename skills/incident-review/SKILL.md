# incident-review

## 目标
- 作为 incident 辅助 skill，对当前 incident 诊断链路执行 second opinion 与收口前复核，重点检查 evidence 到结论链的一致性与可复核性。

## 仅适用于哪个场景
- 主要服务场景：`incident-investigation`。
- 不作为总 review skill，不替代 `incident-orchestrator` 的全局调度职责。

## 何时应使用
- 根因已初步形成，准备进入 review gate。
- 需要 second opinion 来复核证据链与风险判断。
- 主链或 specialist 结论存在待解释项、交叉不一致、置信度不足。

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
- 当 incident 已形成初步结论，但需要证据链复核和 second opinion 时，可进入本 skill。
