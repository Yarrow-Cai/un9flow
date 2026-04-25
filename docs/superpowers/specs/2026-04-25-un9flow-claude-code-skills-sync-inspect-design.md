# un9flow Claude Code skills sync inspect design

## 背景

当前仓库已经完成：

- Claude Code host 接入真源：`docs/CLAUDE_CODE_HOST.md`
- Claude Code setup 真源：`docs/CLAUDE_CODE_SETUP.md`
- skills-only 最小同步脚本：`tools/sync_claude_code_skills.py`

当前同步脚本已经能：

- 发现正式 `skills/**/SKILL.md`
- dry-run 预演同步计划
- 执行真实同步
- 输出最小 summary

但脚本仍缺少一个“先看状态”的模式：在真正执行同步前，使用者仍无法一眼看清当前发现到了哪些 skill、映射到了哪些目标路径、目标当前是否存在、如果执行同步会面对怎样的新建/已存在状态。

## 目标

在 `tools/sync_claude_code_skills.py` 上新增一个 inspect 增强模式。

目标是让脚本在真正执行同步前，能够清楚回答：

- 发现了哪些正式 skill
- 每个 skill 的来源路径是什么
- 每个 skill 的目标路径是什么
- 目标当前是否已存在
- 当前整体将面临怎样的同步状态分布

## 非目标

本轮明确不做：

- 不新增 selective sync
- 不新增 prune / delete
- 不新增 docs / templates / cases / golden 同步
- 不新增 JSON / YAML manifest 文件输出
- 不新增内容 hash、mtime 比较或内容 diff 摘要
- 不新增多 host inspect 逻辑
- 不把 inspect 变成通用仓库扫描器

## 总体方案

采用“inspect / dry-run / sync 三段能力分离”的方案：

1. 默认模式：真实同步
2. `--dry-run`：执行前预演 copy 动作
3. `--inspect`：执行前静态盘点当前状态

其中：

- `inspect` 不写文件
- `inspect` 只关注“当前看到了什么、会映射成什么、目标现在是什么状态”
- `dry-run` 继续关注“如果执行同步，会做什么 copy”

## CLI 设计

在现有 CLI 基础上新增：

- `--inspect`

并固定以下关系：

- `--inspect` 与 `--dry-run` 互斥
- `--inspect` 与 `--force` 互斥
- 默认仍然是 sync

因此增强后脚本形成三种清晰模式：

- inspect
- dry-run
- sync

## inspect 模式职责

inspect 模式只承担以下职责：

1. 列出发现到的正式 skill
2. 列出每个 skill 的来源路径
3. 列出每个 skill 的目标路径
4. 列出目标当前状态
5. 给出统一 summary

## inspect 输出结构

推荐采用文本优先的三段结构：

### 1. 头部摘要

至少包含：

- `INSPECT`
- `SOURCE ROOT: <path>`
- `TARGET ROOT: <path>`
- `FOUND <n> skills`

### 2. 逐项清单

每个 skill 至少输出：

- `skill name`
- `source`
- `target`
- `status`

第一轮状态值建议只保留：

- `missing`
- `exists`

### 3. 尾部 summary

至少输出：

- `SUMMARY`
- `total: <n>`
- `existing: <n>`
- `missing: <n>`

## 推荐文本形态

```text
INSPECT
SOURCE ROOT: skills
TARGET ROOT: .claude-sync-preview
FOUND 12 skills

- orchestration
  source: skills/orchestration/SKILL.md
  target: .claude-sync-preview/skills/orchestration/SKILL.md
  status: missing

SUMMARY
- total: 12
- existing: 0
- missing: 12
```

## 行为边界

### inspect

- 不写文件
- 不创建目录
- 不执行复制
- 不做内容差异计算

### dry-run

- 不写文件
- 继续输出 `PLAN COPY ...`
- 继续站在“准备执行同步”的角度预演动作

### sync

- 继续执行真实文件同步
- 继续支持 `--force`

## 错误边界

本轮只做最小错误边界处理：

- 缺少 `--target-root` → 报错
- `--inspect` 与 `--dry-run` 同时出现 → 报错
- `--inspect` 与 `--force` 同时出现 → 报错
- 没发现任何正式 `skills/**/SKILL.md` → 报错

## 与现有文档的关系

- `docs/CLAUDE_CODE_SETUP.md`
  - 可把 inspect 作为“先盘点再执行”的 setup 辅助动作
- `docs/CLAUDE_CODE_HOST.md`
  - 继续说明 direct-consumption 层，不承担脚本细节
- `docs/CONSISTENCY_VALIDATION.md`
  - 若后续纳管 inspect，只应校验模式边界与输出职责，不扩展到内容 diff

## 建议的后续实施范围

若基于本设计推进实现，建议最小触达这些文件：

- 修改：`tools/sync_claude_code_skills.py`
- 修改：`docs/CLAUDE_CODE_SETUP.md`
- 视需要修改：`docs/CONSISTENCY_VALIDATION.md`
- 视需要修改：`docs/ROADMAP.md`

## 验收标准

当以下条件同时满足时，可认为 Claude Code skills sync inspect 基线完成：

- `tools/sync_claude_code_skills.py` 支持 `--inspect`
- `--inspect` 与 `--dry-run`、`--force` 正确互斥
- inspect 模式输出包含头部摘要、逐项清单与尾部 summary
- inspect 只处理正式 `skills/**/SKILL.md`
- inspect 不写文件、不创建目录
- dry-run 与 sync 的既有行为不被破坏
