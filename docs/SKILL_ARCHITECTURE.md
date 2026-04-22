# un9flow Skill Architecture

## 目标
将“总入口 skill + 三子入口 skill + 辅助 skill + Domain Specialist”的方法边界固定为**可复用、可审查、已落地的架构基线**，供后续 skill 扩展与审查继续沿用。

## 入口规范定位

- `docs/SKILL_ARCHITECTURE.md` 只负责**入口规范**：定义总入口 / 三子入口 / 辅助 skill / Domain Specialist 的进入边界与分工。
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 只负责**调度协议**：定义 Routing Result、Phase Plan、Dispatch Plan、Control Result 的字段与硬约束。
- 正式 `skills/*/SKILL.md` 只能继承入口规范，不重写总调度协议，也不越权发明新的 control signal。

## skill 版图

- **总入口**：`orchestration`
- **场景入口（总共 3 个）**：
  - `incident-investigation`
  - `bringup-path`
  - `design-safety-review`
- **辅助 skill**：
  - `evidence-pack`
  - `incident-review`
- **Domain Specialist**：
  - `signal-path-tracer`
  - `register-state-auditor`
  - `state-machine-tracer`
  - `timing-watchdog-auditor`
  - `failsafe-convergence-reviewer`

## 首批正式 skill 落点

- `skills/orchestration/SKILL.md`
- `skills/incident-investigation/SKILL.md`
- `skills/bringup-path/SKILL.md`
- `skills/design-safety-review/SKILL.md`
- `skills/evidence-pack/SKILL.md`
- `skills/incident-review/SKILL.md`
- `skills/signal-path-tracer/SKILL.md`
- `skills/register-state-auditor/SKILL.md`
- `skills/state-machine-tracer/SKILL.md`
- `skills/timing-watchdog-auditor/SKILL.md`
- `skills/failsafe-convergence-reviewer/SKILL.md`

这 11 个正式文件已经构成当前 skill 架构的首批可用基线：
- 总入口 `orchestration` 负责进入与承接总调度
- 三个主场景入口采用统一主骨架
- 两个 incident 辅助 skill 负责主动找证据与证据链复核
- 五个 `Domain Specialist` 负责各自证据域的结构化分析与 Artifact 产出
- 默认运行约束以各自正式 `SKILL.md` 中的 `Phase / specialist / Artifact` 配置为准
- 三者差异通过各自场景特化段表达

## 总入口职责

总入口 skill 负责：

1. 接收不明确或跨场景请求，提取进入总调度所需的最小输入；
2. 按 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 的输入协议组织请求字段与缺口；
3. 将整理后的请求送入总调度外壳，由总调度外壳完成 case 归一化与主路由判定；
4. 以统一输出协议承接结果：`Routing Result`、`Phase Plan`、`Dispatch Plan`、`Control Result`。

主路由判定权属于 `docs/ORCHESTRATION.md` 中定义的总调度外壳，`总入口 skill 只负责进入与承接`，并对路由结果进行承接与回传。

## 入口边界矩阵

- `总入口 / orchestration`
  - 允许直接承接自由请求：是
  - 是否参与总路由竞争：是
  - 负责内容：主路由承接、输入归一化、结果回传
  - 不负责内容：场景内 specialist 细化与 Artifact 细节填写
- `三子入口 / 场景入口`
  - 允许直接承接自由请求：仅在场景明确且证据一致时
  - 是否参与总路由竞争：是
  - 负责内容：场景骨架执行、场景特化约束、Artifact 主线收敛
  - 不负责内容：重写总入口规则或总控制信号协议
- `辅助 skill`
  - 允许直接承接自由请求：否，必须受控进入
  - 是否参与总路由竞争：否
  - 负责内容：证据整理、review gate 前复核等子任务
  - 不负责内容：充当主场景入口或替代总路由裁决
- `Domain Specialist`
  - 允许直接承接自由请求：否，必须由场景内调度明确分派
  - 是否参与总路由竞争：否
  - 负责内容：单一证据域分析与结构化 Artifact 产出
  - 不负责内容：冒充主场景 skill、辅助 skill 或 review gate

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

## Domain Specialist 职责

- 只在场景内调度明确分派后进入，不参与总路由竞争；
- 只消费 `incident-orchestrator` 或其他场景内调度器交付的 phase objective、dispatch reason、`evidence-package` 与相关上游 Artifact；
- 只产出本证据域的结构化 Artifact，不直接冒充主场景 skill、辅助 skill 或 review gate；
- 输入 / 输出契约、禁止项与回交条件统一继承 `docs/DOMAIN_SPECIALIST_CONTRACTS.md`。

## 与调度协议的分工

- 入口规范先回答“谁可以进、何时能进、进来后属于哪一层”。
- 调度协议再回答“进来以后按什么字段组织输入 / 输出，以及 control signal 如何回传”。
- 若出现冲突，入口边界问题先回 `docs/SKILL_ARCHITECTURE.md`，字段协议与控制信号问题先回 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`。

## 已落地的文档骨架约束

- 总入口 `SKILL.md`
- 子入口 `SKILL.md`
- 辅助 skill `SKILL.md`
- Domain Specialist `SKILL.md`

当前仓库已落第一批正式 skill 文件，但仍保持文档基线阶段：已定义正式文件与边界，不代表已具备自动安装、生成脚本或多 host 绑定能力。
