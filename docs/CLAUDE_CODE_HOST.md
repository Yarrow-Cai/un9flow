# Claude Code Host 接入真源

本文档是 `un9flow` 面向 **Claude Code** 的最小 host 接入真源，定义目录映射、当前可消费能力与明确不承诺范围。

> Claude Code 的最小 setup 前提、setup 对象、setup 步骤与 setup 后验证详见 `docs/CLAUDE_CODE_SETUP.md`。本文档只负责说明“如何理解并消费”本仓库中的能力，不承担 setup 说明。

## 目标

为 Claude Code 提供一套可立即使用、不依赖安装器或分发脚本的 `un9flow` 消费路径：

- 通过 `skills/**/SKILL.md` 直接触发 skill 入口。
- 通过 `docs/` 下的真源文档理解方法边界与调度协议。
- 通过 `tools/validate_consistency.py` 与 `tools/run_generation_regression.py --check` 在本地验证文档与生成产物的一致性。
- 不引入额外配置层、不修改 Claude Code 核心行为、不承诺跨 host 兼容。

## 宿主定位

Claude Code 是当前 `un9flow` 的**第一优先级 host**，原因如下：

- 仓库内所有正式 `skills/**/SKILL.md` 均按 Claude Code skill 入口习惯编写。
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 的输入 / 输出协议与控制信号直接面向 Claude Code 的 prompt 绑定场景设计。
- 本地一致性校验 CLI（`tools/validate_consistency.py`）与回归脚本（`tools/run_generation_regression.py --check`）已在 Claude Code 工作流中验证可用。

其他 host（OpenAI Codex CLI、Cursor、OpenCode 等）的兼容能力当前**不在本文档承诺范围内**。

## 目录映射

### 直接消费层

- `skills/**/SKILL.md`

这是 Claude Code 的正式直接消费入口层。当前宿主真正直接消费的能力对象，以正式 `skills/**/SKILL.md` 为准。

### 真源支撑层

- `docs/CLAUDE_CODE_HOST.md`
- `docs/PLATFORMS.md`
- `docs/SKILL_ARCHITECTURE.md`
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
- `docs/ORCHESTRATION.md`
- `docs/INCIDENT_WORKFLOW.md`
- `docs/BRINGUP_PATH.md`
- `docs/DESIGN_SAFETY_REVIEW.md`
- `docs/DOMAIN_SPECIALIST_CONTRACTS.md`
- `docs/CONSISTENCY_VALIDATION.md`
- `docs/ROADMAP.md`

这层不是 Claude Code 的直接 skill 入口，但它们为宿主消费 skill 时提供规则解释、入口边界、调度协议与一致性约束。

### 模板 / 案例 / 回归支撑层

- `docs/templates/**`
- `docs/cases/**`
- `docs/golden-inputs/**`
- `docs/golden-outputs/**`
- `tools/validate_consistency.py`
- `tools/run_generation_regression.py --check`
- `.github/workflows/consistency-validation.yml`

这层用于支撑模板承载、案例演示与回归验证，不应被解释为 Claude Code 的直接入口层。

### 关键消费路径

- **触发 skill**：在 Claude Code 中直接引用 `skills/**/SKILL.md` 文件路径或内容，即可进入对应 skill 的入口规范与执行骨架。
- **理解架构**：先读 `docs/SKILL_ARCHITECTURE.md` 明确入口边界，再读 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 明确调度协议。
- **验证一致性**：运行 `python tools/validate_consistency.py` 检查 docs / skills / templates 的命名与结构一致性。
- **回归检查**：运行 `python tools/run_generation_regression.py --check` 对比当前生成产物与 golden outputs。

## 消费路径

完成 setup（详见 `docs/CLAUDE_CODE_SETUP.md`）后，按以下路径消费本仓库能力：

1. **验证文件存在**
   确认以下文件已就位：
   - `skills/**/SKILL.md`
   - `docs/PLATFORMS.md`
   - `docs/SKILL_ARCHITECTURE.md`
   - `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
   - `tools/validate_consistency.py`
   - `tools/run_generation_regression.py`

2. **运行一致性校验**
   ```bash
   python tools/validate_consistency.py
   ```
   预期：无 L1 / L2 级别 finding，或 finding 已在 `docs/CONSISTENCY_VALIDATION.md` 中说明。

3. **运行生成回归检查**
   ```bash
   python tools/run_generation_regression.py --check
   ```
   预期：各回归对象输出 `PASS <object>/<case>`，且命令退出码为 0。

4. **在 Claude Code 中消费 skill**
   - 直接引用 `skills/orchestration/SKILL.md` 进入总入口。
   - 或引用具体场景入口，如 `skills/incident-investigation/SKILL.md`、`skills/bringup-path/SKILL.md`、`skills/design-safety-review/SKILL.md`。
   - Domain Specialist 由场景内调度器分派，不直接作为自由请求入口。

5. **查阅协议与约束**
   - 路由与调度字段定义见 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`。
   - 总入口 / 子入口 / 辅助 skill / Domain Specialist 的边界见 `docs/SKILL_ARCHITECTURE.md`。
   - 平台方向与 host 优先级见 `docs/PLATFORMS.md`。

## 当前可消费能力

以下能力在当前基线中**已可用**：

- **正式 skill 入口**：正式 `skills/**/SKILL.md` 入口已落地，可直接在 Claude Code 中引用。
- **总调度规则**：`docs/ORCHESTRATION.md` 定义三场景统一总调度外壳。
- **调度协议**：`docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 固定输入 / 输出字段、控制信号与硬约束。
- **场景真源**：
  - `docs/INCIDENT_WORKFLOW.md`（incident 闭环）
  - `docs/BRINGUP_PATH.md`（bringup 路径）
  - `docs/DESIGN_SAFETY_REVIEW.md`（设计安全审查）
- **Domain Specialist 契约**：`docs/DOMAIN_SPECIALIST_CONTRACTS.md` 固定 5 个 specialist 的输入 / 输出与禁止项。
- **一致性校验**：`tools/validate_consistency.py` 支持本地 CLI 校验与 CI 门禁。
- **生成回归**：`tools/run_generation_regression.py --check` 支持生成产物与 golden outputs 的对比。
- **模板与样例**：`docs/templates/` 与 `docs/cases/` 提供可复用模板与端到端示例。

## 当前明确不承诺

以下能力在当前基线中**明确不提供**：

- **自动安装器**：不提供 `setup.py`、`install.sh` 或 Claude Code 自动 skill 安装脚本。
- **多 host 兼容**：除 Claude Code 外，不承诺 Codex CLI、Cursor、OpenCode 等 host 的直接可用性。
- **动态 skill 发现**：不支持运行时自动扫描或注册 skill，所有入口以静态 `SKILL.md` 为准。
- **跨仓库引用**：`skills/**/SKILL.md` 的调度协议仅保证在本仓库内一致，不保证被外部仓库直接继承。
- **分发与版本化**：当前无 pip / npm / brew 等包管理器分发计划，版本以 git tag 为准。
- **GUI / Web 界面**：无可视化界面，所有交互通过 Claude Code CLI 与 markdown 文档完成。

## 与其他文档的关系

| 文档 | 职责 | 与本文档的关系 |
|---|---|---|
| `docs/PLATFORMS.md` | 定义目标平台列表与 host 优先级 | 本文档是 `PLATFORMS.md` 中 Claude Code 优先级的具体落地 |
| `docs/SKILL_ARCHITECTURE.md` | 定义入口规范与 skill 边界 | host 消费 skill 前必须先理解的架构基线 |
| `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` | 定义调度协议字段与控制信号 | host 侧 prompt 绑定的唯一协议真源 |
| `docs/ORCHESTRATION.md` | 定义总调度外壳规则 | 提供本文档中“总入口”行为的真源 |
| `docs/CONSISTENCY_VALIDATION.md` | 一致性校验总文档 | 说明 `tools/validate_consistency.py` 的校验范围与规则 |
| `docs/ROADMAP.md` | 版本路线图 | 本文档所列“不承诺”项的后续推进计划见路线图 |
| `skills/**/SKILL.md` | 正式 skill 入口文件 | Claude Code 的直接消费对象 |
| `tools/validate_consistency.py` | 本地一致性校验 CLI | host 侧验证文档与代码一致性的工具 |
| `tools/run_generation_regression.py --check` | 生成回归检查 | host 侧验证生成产物未退化的工具 |
