# Claude Code 最小 Setup 真源文档

本文档是 Claude Code 在该仓库中的最小 setup 唯一真源，定义了让 Claude Code 正确工作所需的最小配置和验证步骤。

## 目标

- 建立 Claude Code 的最小可用 setup，确保其能正确调用 skills、执行验证工具并生成预期输出。
- 作为 Claude Code 环境下的最小 setup 参考，保证本仓库在当前 host 语境中的接入边界清晰可追溯。

## setup 前提

- 已安装 Claude Code CLI（`claude` 命令可用）。
- 仓库已克隆到本地，且工作目录位于仓库根目录。
- Python 3 环境可用（用于运行验证工具）。

## 最小 setup 对象

### 必须关心的对象

1. **正式 skill 入口**：`skills/**/SKILL.md` — 所有正式 `SKILL.md` 文件必须存在且可读，这是 Claude Code 识别和调用 skill 的基础。
2. **host 真源文档**：`docs/CLAUDE_CODE_HOST.md` — 说明 Claude Code 如何理解并消费本仓库。
3. **入口规范文档**：`docs/SKILL_ARCHITECTURE.md` — 定义总入口 / 子入口 / 辅助 skill / Domain Specialist 的进入边界。
4. **调度协议文档**：`docs/ORCHESTRATOR_PROMPT_CONTRACT.md` — 定义 Routing Result / Phase Plan / Dispatch Plan / Control Result 的字段与约束。
5. **总调度文档**：`docs/ORCHESTRATION.md` — 定义总调度外壳规则。
6. **一致性验证工具**：`tools/validate_consistency.py` — 用于验证文档和代码之间的一致性。
7. **生成回归检查工具**：`tools/run_generation_regression.py --check` — 用于检查生成输出是否与预期一致。
8. **Skill 同步脚本**：`tools/sync_claude_code_skills.py` — 用于把正式 `skills/**/SKILL.md` 入口同步到 Claude Code 消费目录骨架。

### 可选关心的对象

- `docs/INCIDENT_WORKFLOW.md`
- `docs/BRINGUP_PATH.md`
- `docs/DESIGN_SAFETY_REVIEW.md`
- `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- `docs/REGISTER_STATE_AUDIT.md`
- `docs/templates/**`
- `docs/cases/**`

这些对象不是 setup 成立的第一步硬前提，但在真实消费仓库能力时具有很高价值。

### 当前明确不属于 setup 的对象

- 自动安装器
- 自动目录同步脚本
- 多 host setup
- 分发包 / 发布产物
- CI 平台配置自动注入
- 外部平台专用目录映射

## 最小 setup 步骤

1. 确认仓库结构完整，特别是 `skills/`、`docs/`、`tools/` 目录存在。
2. 确认所有 `skills/**/SKILL.md` 文件已提交到版本控制且未损坏。
3. 阅读 `docs/CLAUDE_CODE_HOST.md`，了解当前 host 的特定配置要求。
4. 运行验证工具确认 setup 正确：
   ```bash
   python tools/validate_consistency.py
   python tools/run_generation_regression.py --check
   ```

## setup 后验证

完成 setup 后，必须运行以下命令验证：

```bash
# 验证一致性
python tools/validate_consistency.py

# 验证生成回归
python tools/run_generation_regression.py --check

# 先盘点当前状态（inspect）
python tools/sync_claude_code_skills.py --target-root <path> --inspect

# 验证 skill 同步计划（dry-run）
python tools/sync_claude_code_skills.py --target-root <path> --dry-run

# 精确点名单个正式 skill 的预演同步
python tools/sync_claude_code_skills.py --target-root <path> --only <skill-name> --dry-run

# 识别目标目录中哪些 skill 仍受管、哪些已经 stale
python tools/sync_claude_code_skills.py --target-root <path> --stale-check

# 列出 stale 目标中可考虑清理的对象（prune advice）
python tools/sync_claude_code_skills.py --target-root <path> --prune-advice

# 显式触发下清理 stale 的 SKILL.md 目标文件
python tools/sync_claude_code_skills.py --target-root <path> --prune
```

上述命令均应返回成功（exit code 0），无报错信息。

- `--inspect`：先看当前状态。用于在执行同步前盘点 skill 来源、目标路径与当前目标状态，属于"先盘点再执行"的辅助动作。
- `--dry-run`：预演将执行的 copy 动作。输出稳定同步计划，且仅覆盖 `skills/**/SKILL.md`。
- `--only <skill-name>`：最小可控同步能力，按 skill 目录名精确过滤一个 skill，用于精确点名单个正式 skill 的预演同步。当前不支持多个 `--only`、按组过滤、路径模式过滤或 exclude。
- `--stale-check`：只做 stale 目标识别与报告，用于识别目标目录中哪些 skill 仍受管、哪些已经 stale。当前不提供 prune 建议，也不执行删除。
- `--prune-advice`：在 stale 目标识别的基础上，给出 `consider-cleanup` 最小建议，用于列出 stale 目标中可考虑清理的对象。当前不输出删除命令，也不执行删除。
- `--prune`：显式动作层，只删除 stale 的 `skills/**/SKILL.md` 目标文件。当前不删除空目录，也不删除非 `SKILL.md` 对象。

## 当前明确不做

- 不提供自动安装器；本轮只定义最小 setup 真源，不进入自动安装流程。
- 不支持多 host setup；当前 setup 文档只对 Claude Code 成立。
- 不配置 CI/CD 流水线自动化（超出最小 setup 范围）。
- 不修改或扩展 skill 的业务逻辑（setup 仅确保可读可用）。
- 不处理与 Claude Code 无关的通用开发环境配置。
- 不强制要求安装非 Python 依赖的第三方服务。

## 与其他文档的关系

- `docs/CLAUDE_CODE_HOST.md`：host 级配置与消费语义真源；本文档负责说明如何最小接起来。
- `docs/PLATFORMS.md`：平台战略、host 优先级与非承诺边界真源；setup 文档不重写平台战略。
- `docs/SKILL_ARCHITECTURE.md`：skill 入口边界与层级结构真源；setup 文档只引用其边界，不重写入口规范。
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`：调度协议与 prompt 字段真源；setup 文档只说明需要查阅，不重写协议本身。
- `docs/CONSISTENCY_VALIDATION.md`：详细说明一致性验证的原理和规则，本文档仅引用工具入口。
- `docs/ROADMAP.md`：项目长期规划，与 setup 无直接依赖，但可帮助理解后续扩展方向。
- `README.md`：项目总览，本文档聚焦于 Claude Code 的 setup 子集。
