# un9flow Claude Code prune advice design

## 背景

当前仓库已经完成：

- Claude Code host 接入真源：`docs/CLAUDE_CODE_HOST.md`
- Claude Code setup 真源：`docs/CLAUDE_CODE_SETUP.md`
- skills-only 最小同步脚本：`tools/sync_claude_code_skills.py`
- inspect / dry-run / sync 三段能力分离
- 第一轮 selective sync：`--only <skill-name>`
- stale target detect：`--stale-check`

当前同步器已经能够识别目标目录中的 stale skill，但还不能把这种识别结果推进到下一层“最小可操作建议”：使用者仍然需要自己从 `status: stale` 推断“这些对象值得关注，并可考虑清理”。

## 目标

在 `tools/sync_claude_code_skills.py` 上新增一个只读建议层模式：

- `--prune-advice`

目标是让脚本在不删除任何文件、不输出删除命令的前提下，明确指出：

- 哪些 stale 目标值得用户关注
- 哪些 stale 目标可考虑清理

## 非目标

本轮明确不做：

- 不执行删除
- 不输出删除命令
- 不输出长理由模板
- 不输出 risk level
- 不输出 JSON / YAML manifest
- 不与 `--only` 叠加
- 不扩展到 docs / templates / cases 的 prune advice

## 总体方案

采用“独立 prune-advice 建议层模式”的方案：

1. 新增 `--prune-advice`
2. 它与 `--stale-check`、`--inspect`、`--dry-run`、`--force`、`--only` 互斥
3. 它复用 stale 目标识别逻辑，但只聚焦 stale 对象
4. 对每个 stale 对象只给出最小建议：`advice: consider-cleanup`

## 核心分工

- `--stale-check`
  - 识别目标目录中哪些是 `managed`、哪些是 `stale`
- `--prune-advice`
  - 只聚焦 stale 对象
  - 给出最小清理建议：`consider-cleanup`

这样可以保持：

- stale-check = 识别层
- prune-advice = 建议层
- future prune = 动作层

## CLI 设计

新增：

- `--prune-advice`

并固定以下互斥关系：

- `--prune-advice` 与 `--stale-check` 互斥
- `--prune-advice` 与 `--inspect` 互斥
- `--prune-advice` 与 `--dry-run` 互斥
- `--prune-advice` 与 `--force` 互斥
- `--prune-advice` 与 `--only` 互斥

第一轮推荐保持 prune-advice 只对整个目标目录做整体 stale 建议，不叠加 selective 语义。

## prune-advice 模式职责

prune-advice 只承担以下职责：

1. 基于目标目录中的 `skills/**/SKILL.md` 做 stale 对象识别
2. 只列出 stale 对象，不重复输出 managed 对象清单
3. 对每个 stale 对象输出：
   - `status: stale`
   - `advice: consider-cleanup`
4. 输出统一 summary

## 输出结构

推荐采用文本优先的三段结构：

### 1. 头部摘要

至少包含：

- `PRUNE-ADVICE`
- `TARGET ROOT: <path>`
- `TOTAL TARGET SKILLS: <n>`
- `STALE TARGETS: <n>`

### 2. 逐项清单

每个 stale 目标至少输出：

- `skill name`
- `target`
- `status: stale`
- `advice: consider-cleanup`

### 3. 尾部 summary

至少包含：

- `SUMMARY`
- `total: <n>`
- `stale: <n>`
- `consider-cleanup: <n>`

## 推荐文本形态

```text
PRUNE-ADVICE
TARGET ROOT: .claude-sync-preview
TOTAL TARGET SKILLS: 14
STALE TARGETS: 2

- old-skill
  target: .claude-sync-preview/skills/old-skill/SKILL.md
  status: stale
  advice: consider-cleanup

SUMMARY
- total: 14
- stale: 2
- consider-cleanup: 2
```

## 行为边界

### prune-advice

- 不写文件
- 不创建目录
- 不执行复制
- 不执行删除
- 不输出删除命令
- 只针对 stale 对象给建议

### stale-check / inspect / dry-run / sync

- 现有语义保持不变
- prune-advice 不改变它们的输出格式与决策逻辑

## 错误边界

本轮只做最小错误边界处理：

- 缺少 `--target-root` → 报错
- `--prune-advice` 与 `--stale-check` / `--inspect` / `--dry-run` / `--force` / `--only` 同时出现 → 报错
- 目标目录不存在时，不报错为失败；可输出 `STALE TARGETS: 0`
- 若目标目录中不存在任何 stale 对象，也不报错；summary 直接显示 `stale: 0`

## 与现有文档的关系

- `docs/CLAUDE_CODE_SETUP.md`
  - 可把 prune-advice 记为“先识别 stale target，再考虑是否手动清理”的辅助动作
- `docs/CONSISTENCY_VALIDATION.md`
  - 若后续纳管，应只校验 prune-advice 的只读边界与最小建议输出，不扩展到删除动作
- `docs/ROADMAP.md`
  - 可作为下一阶段从 stale target detect 推进到 prune advice 的落点

## 建议的后续实施范围

若基于本设计推进实现，建议最小触达这些文件：

- 修改：`tools/sync_claude_code_skills.py`
- 修改：`docs/CLAUDE_CODE_SETUP.md`
- 视需要修改：`docs/CONSISTENCY_VALIDATION.md`
- 视需要修改：`docs/ROADMAP.md`

## 验收标准

当以下条件同时满足时，可认为 Claude Code prune advice 基线完成：

- `tools/sync_claude_code_skills.py` 支持 `--prune-advice`
- `--prune-advice` 与 `--stale-check`、`--inspect`、`--dry-run`、`--force`、`--only` 正确互斥
- prune-advice 只输出 stale 对象，不重复列出 managed 对象
- 每个 stale 对象至少输出 `status: stale` 与 `advice: consider-cleanup`
- prune-advice 不写文件、不创建目录、不执行复制、不执行删除
- stale-check / inspect / dry-run / sync / selective sync 的既有行为不被破坏
