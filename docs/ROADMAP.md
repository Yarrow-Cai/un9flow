# un9flow Roadmap

## v0 - 文档基线

目标：先把项目身份、哲学与边界钉死。

- [x] 项目命名为 `un9flow`
- [x] 建立 README / 哲学 / 工作流 / 平台说明
- [x] 形成文档基线（含 `docs/SKILL_ARCHITECTURE.md` 与 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 入口规范/调度协议基线，先于后续 `SKILL.md`）
- [x] 初始化仓库

## v1 - incident-first 规格定义

目标：先把第一条可运行 incident workflow 的边界钉死。
- 范围说明：三场景总调度外壳已定义在 `docs/ORCHESTRATION.md`，当前优先落地顺序仍按 `incident-first` 推进；`bringup-path` 与 `design-safety-review` 先以总调度规则形式存在，后续再逐步细化为独立场景实现。

计划方向：

- [x] 落地 `incident-investigation` 场景规格基线
- [x] 落地 `incident-orchestrator` 职责边界基线
- [x] 落地 `docs/ORCHESTRATION.md` 作为总调度文档
- [x] 先固化 `docs/SKILL_ARCHITECTURE.md` 中的总入口 / 三子入口 / 辅助 skill 边界（作为正式 `SKILL.md` 前置**入口规范**，见 `## 入口规范定位` / `## 入口边界矩阵` / `## 与调度协议的分工`）
- [x] 先固化 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 的调度协议，再落地 host 侧 prompt 绑定文件（见 `## 调度协议定位` 与 `## host 侧 prompt 绑定前置约束`）。
- [x] 定义 5 个 `Domain Specialist` 的输入 / 输出契约（含 `signal-path-tracer`，见 `docs/DOMAIN_SPECIALIST_CONTRACTS.md`）
- [x] 落地第一批 `Artifact` 模板基线（如 `incident-summary`、`evidence-package`、`incident-review-memo`）
- [x] 固化 `Scenario / Phase / Domain Specialist / Artifact` 命名规则（见 `docs/ORCHESTRATION.md`、`docs/ORCHESTRATOR_PROMPT_CONTRACT.md`、`docs/DOMAIN_SPECIALIST_CONTRACTS.md`）
- [x] 固定第一条 incident pipeline 的输入输出边界，禁止混淆 skill 与 artifact 角色（见 `docs/INCIDENT_WORKFLOW.md`）

## v2 - incident pipeline skill 化

目标：把第一条 embedded incident workflow 做成真正可接入的能力链。

计划方向：

- [x] 落地 `incident-investigation`
- [x] 落地 `evidence-pack`
- [x] 落地 `incident-review`
- [x] 落地 `incident-orchestrator` 调度规则
- [x] 以 `docs/ORCHESTRATION.md` 为总调度基线，以 scenario 文档（如 `docs/INCIDENT_WORKFLOW.md`）为下层场景基线
- [x] 落地 5 个 `Domain Specialist`

## v3 - host 接入

目标：让 incident-first 能力链在 host 层可消费。

计划方向：

- [x] 第一阶段仅对齐 workflow orchestration 思路、Claude Code / skill 入口习惯与后续目录组织方式（见 `docs/PLATFORMS.md`）
- [x] `gstack-compatible first` 仅指以上对齐层，不承诺现阶段具备安装器、分发、目录映射或广泛 host 兼容能力（见 `docs/PLATFORMS.md`）
- [x] OpenClaw 作为外层调度预留位（见 `docs/PLATFORMS.md`）

## v4 - 生成与校验体系

目标：围绕 incident-first 的 `incident pipeline`，补齐能力定义的可生成、可校验、可回归。

计划方向：

- [x] 模板化能力文档（基于 `Artifact` 模板，见 `docs/templates/*-pack.md`）
- [x] 文档生成脚本（覆盖 incident workflow 主线，见 `tools/generate_incident_case_bundle.py`）
- [x] 落地 `docs/CONSISTENCY_VALIDATION.md` 统一校验基线
- [x] 增加 `consistency-review-checklist.md`
- [x] 增加 `validation-findings.md`
- [x] `docs/templates/skill-routing-matrix.md` 作为案例层模板继续复用
- [x] 增加 orchestrator dispatch plan 模板
- [x] 当前本地一致性校验 CLI 已接入最小 GitHub 门禁 workflow（PR / main）
- [x] 第一版仅做严格阻断，不含 artifact / summary / matrix 增强
- [x] `Scenario / Phase / Domain Specialist / Artifact` 一致性校验
- [x] `incident workflow` 示例任务回归测试（见 `docs/cases/incident-workflow-routing-regression.md` 与 `docs/cases/incident-workflow-dispatch-regression.md`）

## v5 - 嵌入式专用能力

目标：在 incident-first 跑稳后，沿 incident workflow 向外扩展 embedded 专用能力。

计划方向：

- [x] 功能安全 review 能力（按 Domain Specialist 输出要求对齐 incident-first，见 `docs/DESIGN_SAFETY_REVIEW.md`）
- [x] 寄存器审计能力基线已落地：`docs/REGISTER_STATE_AUDIT.md` 作为方法真源，`docs/templates/register-state-audit-pack.md` 作为 specialist pack 模板
- [x] ISR / 主循环职责冲突检查已作为 `timing-watchdog-auditor` 线内专项扩展固化，沿 `Domain Specialist` 与 `Artifact` 主线延展
- [x] 看门狗与超时策略审计专项基线已落地：`docs/WATCHDOG_TIMEOUT_AUDIT.md` 作为方法真源，`docs/templates/watchdog-timeout-audit-checklist.md` 作为 checklist 模板
- [x] 看门狗与超时策略 formal skill / findings 基线已落地：`skills/watchdog-timeout-audit/SKILL.md` 与 `docs/templates/watchdog-timeout-audit-findings.md` 已纳入现有 consistency / CI 门禁
- [x] watchdog 自动报告模板基线已落地：`docs/templates/watchdog-timeout-audit-report.md` 已纳入现有 consistency / CI 门禁
- [x] watchdog 自动报告生成器基线已落地：`tools/generate_watchdog_timeout_audit_report.py` 已接入现有对象体系并受 consistency / CI 门禁约束
- [x] 更重型 watchdog 专项 workflow 已落地：docs/WATCHDOG_TIMEOUT_WORKFLOW.md 已把 checklist → pack → findings → report 固定为专项执行骨架
- [x] 菊花链 / isoSPI / AFE bring-up 模板已落地：docs/templates/daisy-chain-isospi-afe-bringup-template.md 作为 bringup-path 下的专项模板
- [x] Keil Scatter / Linker Script 审核模板已落地：docs/templates/keil-scatter-linker-review-template.md 作为 design-safety-review 下的专项模板

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
