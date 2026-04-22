# un9flow Register State Audit

## 目标
固定为 `register-state-auditor` 的方法真源，审查默认值、目标值、当前值、复位后值与关键位语义之间的配置偏移与确定性缺口。

## 定位与边界

### 它属于什么
- `register-state-auditor` 的专项方法真源。
- 面向寄存器快照、关键使能位、保护位与复位返回路径的审计方法。
- 用于回答“寄存器层是否存在配置偏移、位语义误判或复位残留风险”。

### 它不属于什么
- 不是新的 `Scenario`。
- 不是链路分段定位器。
- 不是完整状态机迁移分析器。
- 不是直接给出系统级根因定论的裁决器。

## 核心检查项
1. `reset-value baseline`
2. `enable and protection chain`
3. `sticky and latched semantics`
4. `config mismatch and init gap`
5. `reset-return risk`

## 输出结构
- `register-bitfield-map`
- `register-anomaly-list`
- `config-mismatch-note`

## 与 specialist / 模板 / 场景的关系
- specialist 契约真源：`docs/DOMAIN_SPECIALIST_CONTRACTS.md`
- incident 场景交接边界：`docs/INCIDENT_WORKFLOW.md`
- design-safety-review 主场景真源：`docs/DESIGN_SAFETY_REVIEW.md`
- 对应输出模板：`docs/templates/register-state-audit-pack.md`
