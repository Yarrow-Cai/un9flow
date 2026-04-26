# un9flow Claude Code stale target detect design

## 背景

当前仓库已经完成：

- Claude Code host 接入真源：`docs/CLAUDE_CODE_HOST.md`
- Claude Code setup 真源：`docs/CLAUDE_CODE_SETUP.md`
- skills-only 最小同步脚本：`tools/sync_claude_code_skills.py`
- inspect / dry-run / sync 三段能力分离
- 第一轮 selective sync：`--only <skill-name>`

当前同步器已经具备“看 source → target 映射”“预演将执行动作”“真实同步正式 skill”的能力，但仍缺少一条 target-centric 的安全控制能力：目标目录里哪些 `skills/<name>/SKILL.md` 已经不再受当前仓库管理、哪些属于 stale target，目前还无法被只读识别出来。

## 目标

在 `tools/sync_claude_code_skills.py` 上新增一个只读 stale target detect / report 模式。

目标是让脚本在不删除任何文件的前提下，能够明确指出：

- 目标目录里哪些 skill 仍受当前仓库管理
- 哪些目标 skill 已经 stale
- 当前整体 stale 风险分布是什么

## 非目标

本轮明确不做：

- 不输出 prune 建议
- 不执行删除
- 不做 docs / templates / cases 的 stale 检测
- 不做 hash / diff / mtime 比较
- 不做 JSON / YAML manifest 文件
- 不与 `--only` 叠加计算 selective stale 结果
- 不把 stale detect 扩展成通用垃圾扫描器

## 总体方案

采用“独立 stale-check 只读模式”的方案：

1. 新增 `--stale-check`
2. 它与 `--inspect`、`--dry-run`、`--force`、`--only` 互斥
3. 只扫描目标目录中的 `skills/**/SKILL.md`
4. 用当前仓库正式 `skills/**/SKILL.md` 集合作为受管集合
5. 逐项输出 `managed` / `stale`

## 核心分工

- `--inspect`
  - source-centric
  - 看 source → target 的映射与目标存在状态
- `--dry-run`
  - action-centric
  - 看如果执行同步会做什么动作
- `sync`
  - execution-centric
  - 真正写入目标目录
- `--stale-check`
  - target-centric
  - 看目标目录里哪些 skill 仍受管、哪些已 stale

## CLI 设计

新增：

- `--stale-check`

并固定以下关系：

- `--stale-check` 与 `--inspect` 互斥
- `--stale-check` 与 `--dry-run` 互斥
- `--stale-check` 与 `--force` 互斥
- `--stale-check` 与 `--only` 互斥

第一轮推荐保持 stale-check 只检查目标目录整体 stale 状态，不叠加 selective sync 语义。

## stale-check 模式职责

stale-check 只承担以下职责：

1. 扫描目标目录中的 `skills/**/SKILL.md`
2. 与当前仓库正式 `skills/**/SKILL.md` 集合对比
3. 对每个目标 skill 给出状态：
   - `managed`
   - `stale`
4. 输出统一 summary

## 输出结构

推荐采用文本优先的三段结构：

### 1. 头部摘要

至少包含：

- `STALE-CHECK`
- `TARGET ROOT: <path>`
- `FOUND TARGET SKILLS: <n>`
- `CURRENT SOURCE SKILLS: <n>`

### 2. 逐项清单

每个目标 skill 至少输出：

- `skill name`
- `target`
- `status`

第一轮状态只保留：

- `managed`
- `stale`

### 3. 尾部 summary

至少包含：

- `SUMMARY`
- `total: <n>`
- `managed: <n>`
- `stale: <n>`

## 推荐文本形态

```text
STALE-CHECK
TARGET ROOT: .claude-sync-preview
FOUND TARGET SKILLS: 14
CURRENT SOURCE SKILLS: 12

- orchestration
  target: .claude-sync-preview/skills/orchestration/SKILL.md
  status: managed

- old-skill
  target: .claude-sync-preview/skills/old-skill/SKILL.md
  status: stale

SUMMARY
- total: 14
- managed: 12
- stale: 2
```

## 行为边界

### stale-check

- 不写文件
- 不创建目录
- 不执行复制
- 不执行删除
- 只观察目标目录中的 `skills/**/SKILL.md`

### selective sync / inspect / dry-run / sync

- 现有语义保持不变
- stale-check 不改变它们的输出格式与决策逻辑

## 错误边界

本轮只做最小错误边界处理：

- 缺少 `--target-root` → 报错
- `--stale-check` 与 `--inspect` / `--dry-run` / `--force` / `--only` 同时出现 → 报错
- 目标目录不存在时，不报错为失败；可输出 `FOUND TARGET SKILLS: 0` 与 `stale: 0`
- 当前仓库没有任何正式 `skills/**/SKILL.md` 时，沿用脚本既有错误处理策略

## 与现有文档的关系

- `docs/CLAUDE_CODE_SETUP.md`
  - 可把 stale-check 记为“先识别 stale target 再决定后续动作”的安全辅助能力
- `docs/CONSISTENCY_VALIDATION.md`
  - 若后续纳管，应只校验 stale-check 的只读边界与状态分类，不扩展到 prune 建议或删除动作
- `docs/ROADMAP.md`
  - 可作为下一阶段从 selective sync 推进到 stale target detect 的落点

## 建议的后续实施范围

若基于本设计推进实现，建议最小触达这些文件：

- 修改：`tools/sync_claude_code_skills.py`
- 修改：`docs/CLAUDE_CODE_SETUP.md`
- 视需要修改：`docs/CONSISTENCY_VALIDATION.md`
- 视需要修改：`docs/ROADMAP.md`

## 验收标准

当以下条件同时满足时，可认为 Claude Code stale target detect 基线完成：

- `tools/sync_claude_code_skills.py` 支持 `--stale-check`
- `--stale-check` 与 `--inspect`、`--dry-run`、`--force`、`--only` 正确互斥
- stale-check 只扫描目标目录中的 `skills/**/SKILL.md`
- stale-check 输出包含头部摘要、逐项清单与尾部 summary
- 状态值至少稳定区分 `managed` 与 `stale`
- stale-check 不写文件、不创建目录、不执行复制、不执行删除
- inspect / dry-run / sync / selective sync 的既有行为不被破坏
