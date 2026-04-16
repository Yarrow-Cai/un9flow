# un9flow Roadmap

## v0 - 文档基线

目标：先把项目身份、哲学与边界钉死。

- [x] 项目命名为 `un9flow`
- [x] 建立 README / 哲学 / 工作流 / 平台说明
- [x] 形成文档基线
- [x] 初始化仓库

## v1 - incident-first 规格定义

目标：先把第一条可运行 incident workflow 的边界钉死。
- 范围说明：三场景总调度外壳已定义在 `docs/ORCHESTRATION.md`，当前优先落地顺序仍按 `incident-first` 推进；`bringup-path` 与 `design-safety-review` 先以总调度规则形式存在，后续再逐步细化为独立场景实现。

计划方向：

- [x] 落地 `incident-investigation` 场景规格基线
- [x] 落地 `incident-orchestrator` 职责边界基线
- [x] 落地 `docs/ORCHESTRATION.md` 作为总调度文档
- [ ] 定义 5 个 `Domain Specialist` 的输入 / 输出契约（含 `signal-path-tracer`）
- [x] 落地第一批 `Artifact` 模板基线（如 `incident-summary`、`evidence-package`、`incident-review-memo`）
- [ ] 固化 `Scenario / Phase / Domain Specialist / Artifact` 命名规则
- [ ] 固定第一条 incident pipeline 的输入输出边界，禁止混淆 skill 与 artifact 角色

## v2 - incident pipeline skill 化

目标：把第一条 embedded incident workflow 做成真正可接入的能力链。

计划方向：

- [ ] 落地 `incident-investigation`
- [ ] 落地 `evidence-pack`
- [ ] 落地 `incident-review`
- [ ] 落地 `incident-orchestrator` 调度规则
- [x] 以 `docs/ORCHESTRATION.md` 为总调度基线，以 scenario 文档（如 `docs/INCIDENT_WORKFLOW.md`）为下层场景基线
- [ ] 落地 5 个 `Domain Specialist`

## v3 - host 接入

目标：让 incident-first 能力链在 host 层可消费。

计划方向：

- [ ] 第一阶段仅对齐 workflow orchestration 思路、Claude Code / skill 入口习惯与后续目录组织方式
- [ ] `gstack-compatible first` 仅指以上对齐层，不承诺现阶段具备安装器、分发、目录映射或广泛 host 兼容能力
- [ ] OpenClaw 作为外层调度预留位

## v4 - 生成与校验体系

目标：围绕 incident-first 的 `incident pipeline`，补齐能力定义的可生成、可校验、可回归。

计划方向：

- [ ] 模板化能力文档（基于 `Artifact` 模板）
- [ ] 文档生成脚本（覆盖 incident workflow 主线）
- [x] 增加路由验证矩阵模板
- [x] 增加 orchestrator dispatch plan 模板
- [ ] `Scenario / Phase / Domain Specialist / Artifact` 一致性校验
- [ ] `incident workflow` 示例任务回归测试

## v5 - 嵌入式专用能力

目标：在 incident-first 跑稳后，沿 incident workflow 向外扩展 embedded 专用能力。

计划方向：

- [ ] 功能安全 review 能力（按 Domain Specialist 输出要求对齐 incident-first）
- [ ] 寄存器审计能力（对接 `incident workflow` 中对应 Artifact）
- [ ] ISR / 主循环职责冲突检查（沿 `Domain Specialist` 与 `Artifact` 主线延展）
- [ ] 看门狗与超时策略审计（以 incident pipeline 事件语义串联）
- [ ] 菊花链 / isoSPI / AFE bring-up 模板
- [ ] Keil Scatter / Linker Script 审核模板

## v6 - 示例与实战

目标：让仓库不仅有方法论，还有落地演示。

计划方向：

- [ ] 示例 BMS 方法论用法
- [ ] 示例功率板 bring-up 流程
- [ ] 示例故障注入报告
- [ ] 示例 limp-home 设计说明

## 长期目标

把 `un9flow` 做成：

> **安全关键嵌入式系统场景下，围绕确定性工程方法构建的专业能力仓库。**
