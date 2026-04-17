# un9flow Skill Architecture

## 目标
将“总入口 skill + 三子入口 skill + 辅助 skill”的方法边界固定为**可复用、可审查、已落地的架构基线**，供后续 skill 扩展与审查继续沿用。

## skill 版图

- **总入口**：`orchestration`
- **场景入口（总共 3 个）**：
  - `incident-investigation`
  - `bringup-path`
  - `design-safety-review`
- **辅助 skill**：
  - `evidence-pack`
  - `incident-review`

## 首批正式 skill 落点

- `skills/orchestration/SKILL.md`
- `skills/incident-investigation/SKILL.md`
- `skills/bringup-path/SKILL.md`
- `skills/design-safety-review/SKILL.md`
- `skills/evidence-pack/SKILL.md`
- `skills/incident-review/SKILL.md`

这六个正式文件已经构成当前 skill 架构的首批可用基线：
- 总入口 `orchestration` 负责进入与承接总调度
- 三个主场景入口采用统一主骨架
- 两个 incident 辅助 skill 负责主动找证据与证据链复核
- 默认运行约束以各自正式 `SKILL.md` 中的 `Phase / specialist / Artifact` 配置为准
- 三者差异通过各自场景特化段表达

## 总入口职责

总入口 skill 负责：

1. 接收不明确或跨场景请求，提取进入总调度所需的最小输入；
2. 按 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 的输入协议组织请求字段与缺口；
3. 将整理后的请求送入总调度外壳，由总调度外壳完成 case 归一化与主路由判定；
4. 以统一输出协议承接结果：`Routing Result`、`Phase Plan`、`Dispatch Plan`、`Control Result`。

主路由判定权属于 `docs/ORCHESTRATION.md` 中定义的总调度外壳，`总入口 skill 只负责进入与承接`，并对路由结果进行承接与回传。

## 子入口职责（场景入口）

每个场景入口 skill 在正式文件中固定同一主骨架：

1. **目标**
2. **适用边界**
3. **最小输入要求**
4. **默认 Phase 骨架**
5. **默认 specialist 偏向**
6. **主要 Artifact**
7. **场景特化段**
8. **不负责什么**
9. **与总入口 / prompt 契约的关系**
10. **Claude Code 宿主附录**

其中真正允许随场景变化的是两层：
- 场景特化段
- 默认运行约束（`Phase / specialist / Artifact` 的场景内初始值与允许范围）

### 子入口清单

- `incident-investigation`：事故事件聚焦入口，面向现网或验收时异常闭环；
- `bringup-path`：开发早期 bringup 路径入口，强调快速收敛与最小副作用验证；
- `design-safety-review`：设计阶段审查入口，偏向前置约束性审查与风险界定。

## 辅助 skill 职责

- 不参与总路由竞争；
- 不直接承接未定向的自由请求；
- 仅在特定场景内被主入口显式调用，或被主入口显式引导调用；
- 输出应为可复用子产物（例如 evidence/diagnosis/review 片段），供主场景继续使用。

## 已落地的文档骨架约束

- 总入口 `SKILL.md`
- 子入口 `SKILL.md`
- 辅助 skill `SKILL.md`

当前仓库已落第一批正式 skill 文件，但仍保持文档基线阶段：已定义正式文件与边界，不代表已具备自动安装、生成脚本或多 host 绑定能力。
