# skill-boundary-checklist

该模板用于在 skill 边界定稿阶段形成统一表述。

- `skill name`: `incident-investigation` / `bringup-path` / `design-safety-review` / `evidence-pack` / `incident-review` / ...
- `skill type`: `总入口` / `场景入口` / `辅助 skill`
- `goal`: 本 skill 的一句话目标
- `in-scope`: 本 skill 负责的范围
- `out-of-scope`: 明确排除、不得覆盖的范围
- `minimum inputs`: 触发该 skill 所需的最小输入项
- `main artifacts`: 场景内关键产物与命名
- `default runtime constraints`: `default Phase` / `default specialist bias` / `main Artifacts`
- `relation to orchestrator`: 与总调度/路由约束的关系
- `relation to other skills`: 与其他 skill 的调用顺序、并列关系、边界交接

## skill type 约束

`skill type` 必须仅使用以下之一：

- 总入口
- 场景入口
- 辅助 skill

## 示例（待填）

```yaml
skill name:
skill type:
goal:
in-scope:
out-of-scope:
minimum inputs:
main artifacts:
default runtime constraints:
  default Phase:
  default specialist bias:
  main Artifacts:
relation to orchestrator:
relation to other skills:
```
