---
name: evidence-pack
description: Organize incident evidence, identify evidence gaps, and produce a structured evidence package for the incident workflow.
---

# evidence-pack

## 目标
- 作为 incident 辅助 skill，`主动识别证据缺口`，推动下一轮取证，最终形成可供 incident 主链后续诊断步骤消费的 `evidence-package`。
- 强调 `主动找证据 / 补证据`，而不是被动整理已有材料。

## 仅适用于哪个场景
- 主要服务场景：`incident-investigation`。
- 不作为全局主路由入口，不参与总路由竞争（不做场景级调度裁决）。

## 进入限制
### 只允许
1. 用户显式要求先整理证据或补证据。
2. `incident` 主链明确要求先补证据后再继续。

### 不允许
- 参与全局主路由竞争。
- 充当通用证据整理器（脱离 incident 上下文独立接单）。
- 直接给出根因结论。

## 何时应使用
- 用户显式要求先整理证据或补证据。
- `incident` 主链已明确要求先补证据后再继续。
- 以上两类情形之外，即使材料混乱，也应先由主场景或总入口决定是否切入本 skill。

## 输入要求
- 当前已有症状与触发背景。
- 日志、快照、波形、寄存器信息（或其摘要）。
- 当前约束（时间窗、采样条件、复现实验条件）。
- 当前风险边界（安全态、影响范围、可接受停机/降级条件）。

## 核心动作
1. 盘点已有证据，按时间窗、来源、可靠性和可复核性进行结构化梳理。
2. 标记缺失证据与关键缺口，明确每项缺口对假设验证的影响。
3. 生成按优先级排序的取证建议（High / Medium / Low），给出建议动作、验证入口和必要前置条件。
4. 形成 `evidence-package`：统一字段、统一时间粒度、统一证据引用关系，保留待补项与执行边界。

## 输出 Artifact
- `evidence-package`
- `evidence-gap-note`
- `evidence-acquisition-plan`

## 何时返回主场景
- 当证据结构可被 incident 主链直接消费，且缺口不再阻断下一步诊断时，返回 `incident-investigation`。

## 不负责什么
- 不给出根因结论（RC / RC hypothesis）。
- 不替代总路由与场景裁决。
- 不替代 `incident-investigation` 下的 specialist 深度分析。

## Claude Code 宿主附录
- 仅在用户显式要求先整理证据或补证据，或 incident 主链明确要求先补证据后再继续时进入本 skill。
