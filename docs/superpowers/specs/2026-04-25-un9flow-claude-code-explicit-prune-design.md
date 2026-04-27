# un9flow Claude Code explicit prune design

## 背景

当前仓库已经完成：

- Claude Code host 接入真源：`docs/CLAUDE_CODE_HOST.md`
- Claude Code setup 真源：`docs/CLAUDE_CODE_SETUP.md`
- skills-only 最小同步脚本：`tools/sync_claude_code_skills.py`
- inspect / dry-run / sync 三段能力分离
- selective sync：`--only <skill-name>`
- stale target detect：`--stale-check`
- prune advice：`--prune-advice`

当前同步器已经具备完整的识别层与建议层能力，但还没有一个真正的动作层模式，能够在强约束下删除 stale target skill 文件。

## 目标

在 `tools/sync_claude_code_skills.py` 上新增一个显式动作层模式：

- `--prune`

目标是在显式触发、受控边界和完整可见输出下，删除 stale target 中的 `skills/**/SKILL.md` 文件。

## 非目标

本轮明确不做：

- 不做二次交互确认 prompt
- 不做回收站 / trash
- 不做 undo / restore
- 不删除空目录
- 不删除 docs / templates / cases / golden / regression 文件
- 不和 `--only` 叠加做 selective prune
- 不做自动 prune
- 不做批量删除上限或策略分级

## 总体方案

采用“显式 prune 动作层”方案：

1. 新增 `--prune`
2. 该模式与 `--inspect`、`--dry-run`、`--stale-check`、`--prune-advice`、`--force`、`--only` 互斥
3. 只删除已判定为 stale 的目标 `skills/**/SKILL.md` 文件
4. 逐项输出 `PRUNED / SKIPPED / FAILED` 结果，并给出 summary

## 核心分工

- `--stale-check`
  - 识别层：告诉用户哪些目标是 `managed`、哪些是 `stale`
- `--prune-advice`
  - 建议层：告诉用户哪些 stale 目标 `consider-cleanup`
- `--prune`
  - 动作层：真正删除 stale 的 `SKILL.md` 目标文件

## 安全边界

第一轮 `--prune` 必须同时满足以下条件：

1. 必须显式传入 `--prune`
2. 只能删除已判定为 stale 的目标
3. 只能删除目标目录里的 `skills/**/SKILL.md`
4. 删除过程必须逐项打印并可审查

## 拒绝删除的情况

第一轮一律拒绝：

- 非 `skills/**/SKILL.md` 目标
- 当前仍属于 managed 的目标
- 与其他模式组合的调用

## CLI 设计

新增：

- `--prune`

并固定以下互斥关系：

- `--prune` 与 `--inspect` 互斥
- `--prune` 与 `--dry-run` 互斥
- `--prune` 与 `--stale-check` 互斥
- `--prune` 与 `--prune-advice` 互斥
- `--prune` 与 `--force` 互斥
- `--prune` 与 `--only` 互斥

## 输出结构

### 逐项动作输出

- `PRUNED <target>`
- `SKIPPED <target>: <reason>`
- `FAILED <target>: <reason>`

### summary

至少包含：

- `SUMMARY: pruned <n>, skipped <n>, failed <n>`

## 推荐文本形态

```text
PRUNED .claude-sync-preview/skills/old-skill/SKILL.md
SUMMARY: pruned 1, skipped 0, failed 0
```

## 删除范围

第一轮只删除：

- stale 的 `SKILL.md` 文件本身

不删除：

- 对应空目录
- 目录中的其他文件
- 任何非 `SKILL.md` 对象

## 错误边界

本轮只做最小错误边界处理：

- 缺少 `--target-root` → 报错
- 与互斥模式组合 → 报错
- 目标目录不存在时，不报错，summary 直接为 0
- 没有 stale 目标时，不报错，summary 直接为 0
- 目标文件删除失败时，输出 `FAILED ...` 并进入 summary 失败计数

## 与现有文档的关系

- `docs/CLAUDE_CODE_SETUP.md`
  - 可把 prune 记为“显式手动清理 stale target”的下一层动作
- `docs/CONSISTENCY_VALIDATION.md`
  - 若后续纳管，应只校验 prune 的受控边界，不扩展到自动清理系统
- `docs/ROADMAP.md`
  - 可作为下一阶段从 prune advice 推进到动作层 prune 的落点

## 建议的后续实施范围

若基于本设计推进实现，建议最小触达这些文件：

- 修改：`tools/sync_claude_code_skills.py`
- 修改：`tools/test_sync_claude_code_skills.py`
- 修改：`docs/CLAUDE_CODE_SETUP.md`
- 视需要修改：`docs/CONSISTENCY_VALIDATION.md`
- 视需要修改：`docs/ROADMAP.md`

## 验收标准

当以下条件同时满足时，可认为 Claude Code explicit prune 基线完成：

- `tools/sync_claude_code_skills.py` 支持 `--prune`
- `--prune` 与 `--inspect`、`--dry-run`、`--stale-check`、`--prune-advice`、`--force`、`--only` 正确互斥
- `--prune` 只删除 stale 的 `skills/**/SKILL.md`
- 删除过程逐项输出 `PRUNED / SKIPPED / FAILED`
- summary 至少包含 `pruned / skipped / failed`
- `--prune` 不删除空目录，不删除非 `SKILL.md` 对象
- stale-check / prune-advice / inspect / dry-run / sync / selective sync 的既有行为不被破坏
