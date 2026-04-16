# un9flow Skill Architecture

## 目标
将“总入口 skill + 三子入口 skill + 辅助 skill”的方法边界先固定为**可复用、可审查**，并沉淀为后续正式 `SKILL.md` 可直接继承的文档基线。

## skill 版图

- **总入口**：`orchestration`
- **场景入口（总共 3 个）**：
  - `incident-investigation`
  - `bringup-path`
  - `design-safety-review`
- **辅助 skill**：
  - `evidence-pack`
  - `incident-review`

## 总入口职责

总入口 skill 负责：

1. 接收不明确或跨场景请求，提取进入总调度所需的最小输入；
2. 按 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 的输入协议组织请求字段与缺口；
3. 将整理后的请求送入总调度外壳，由总调度外壳完成 case 归一化与主路由判定；
4. 以统一输出协议承接结果：`Routing Result`、`Phase Plan`、`Dispatch Plan`、`Control Result`。

主路由判定权属于 `docs/ORCHESTRATION.md` 中定义的总调度外壳，`总入口 skill 只负责进入与承接`，并对路由结果进行承接与回传。

## 子入口职责（场景入口）

每个场景入口 skill 在声明边界时需固定：

1. **场景边界**：该入口仅处理所属场景语义，拒绝扩散到其他场景；
2. **最小输入要求**：给定场景必须满足的关键输入（如目标系统、故障症状、上下文版本、限制条件）；
3. **场景内初始 Artifact 组织**：定义进入场景后第一轮应产出的 artifact 结构；
4. **默认运行约束**：限制场景内默认 `Phase / specialist / Artifact` 的初始值与允许范围（便于人工与自动检查）。

### 子入口清单

- `incident-investigation`：事故事件聚焦入口，面向现网或验收时异常闭环；
- `bringup-path`：开发早期 bringup 路径入口，强调快速收敛与最小副作用验证；
- `design-safety-review`：设计阶段审查入口，偏向前置约束性审查与风险界定。

## 辅助 skill 职责

- 不参与总路由竞争；
- 不直接承接未定向的自由请求；
- 仅在特定场景内被主入口显式调用，或被主入口显式引导调用；
- 输出应为可复用子产物（例如 evidence/diagnosis/review 片段），供主场景继续使用。

## 文档骨架建议（面向后续 `SKILL.md`）

- 总入口 `SKILL.md`
- 子入口 `SKILL.md`
- 辅助 skill `SKILL.md`

> 当前仓库为方法论文档仓库，以上为下一阶段 skill 化前的边界骨架，不代表已具备正式 host-level 绑定。
