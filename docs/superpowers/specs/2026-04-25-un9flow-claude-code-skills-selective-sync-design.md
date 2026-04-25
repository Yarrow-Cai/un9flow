# un9flow Claude Code selective skills sync design

## 背景

当前仓库已经完成：

- Claude Code host 接入真源：`docs/CLAUDE_CODE_HOST.md`
- Claude Code setup 真源：`docs/CLAUDE_CODE_SETUP.md`
- skills-only 最小同步脚本：`tools/sync_claude_code_skills.py`
- inspect / dry-run / sync 三段能力分离

但当前同步脚本仍然只能“全量处理全部正式 skill”，不能在用户只想同步某一个 skill 时提供受约束的最小选择能力。

## 目标

在 `tools/sync_claude_code_skills.py` 上新增第一轮 selective sync 能力：

- `--only <skill-name>`

让用户在 inspect / dry-run / sync 三种模式下，能够精确点名只处理某一个正式 skill。

## 非目标

本轮明确不做：

- 不支持多个 `--only`
- 不支持逗号列表或重复 `--only`
- 不支持按组过滤
- 不支持路径模式过滤
- 不支持模糊匹配、正则、通配符
- 不支持 exclude 逻辑
- 不支持 alias 或大小写宽容匹配

## 总体方案

采用“按 skill name 精确过滤”的最小方案：

1. 新增 `--only <skill-name>`
2. 只接受与 `skills/<skill-name>/SKILL.md` 目录名完全一致的值
3. 过滤逻辑在 inspect / dry-run / sync 三种模式之前统一生效
4. 若 skill 名不存在，则明确报错，不做 silent skip

## CLI 设计

在现有 CLI 基础上新增：

- `--only <skill-name>`

第一轮规则固定为：

- 最多传一次
- 只接受一个 skill 名
- 区分大小写

推荐合法示例：

- `--only orchestration`
- `--only bringup-path`

## 模式关系

`--only` 不是独立模式，而是过滤参数。

因此：

- `--inspect --only orchestration` → 只盘点 `orchestration`
- `--dry-run --only orchestration` → 只预演 `orchestration`
- `--only orchestration --force` → 只同步 `orchestration`，且允许覆盖

## 匹配规则

- 按目录名精确匹配
- 与 `skills/<skill-name>/SKILL.md` 中的 `<skill-name>` 完全一致
- 若用户输入不存在的 skill 名，必须硬失败

建议错误形态：

- `Unknown skill: <name>`
- `Available skills: orchestration, incident-investigation, ...`

## 输出行为

selective sync 不引入新的输出格式，只缩小对象集合。

### inspect

- 仍输出 `INSPECT`
- 仍输出 `FOUND <n> skills`
- 但当 `--only orchestration` 时，应只输出 1 个 skill
- `SUMMARY` 中的 `total` 也应变为 `1`

### dry-run

- 仍输出 `DRY-RUN`
- 仍输出 `PLAN COPY / PLAN SKIP / PLAN OVERWRITE`
- 但只针对 1 个 skill
- summary 中只统计该 1 个 skill

### sync

- 仍输出 `SYNCED / SKIPPED / FAILED`
- summary 只统计该 1 个 skill

## 验收方式

第一轮 selective sync 至少验证四类行为：

1. 精确命中：
   - `--only orchestration`
   - 结果只处理 1 个 skill
2. 不存在 skill 硬失败：
   - `--only does-not-exist`
   - 返回非零并输出 `Unknown skill: does-not-exist`
3. 三种模式都生效：
   - `--inspect --only orchestration`
   - `--dry-run --only orchestration`
   - `--only orchestration --force`
4. 全量模式不回归：
   - 不带 `--only` 的 inspect / dry-run / sync 仍保持当前 12-skill 行为

## 错误边界

本轮只做最小错误边界处理：

- 缺少 `--target-root` → 继续报错
- `--only` 未提供值 → argparse 报错
- `--only` 指向不存在 skill → 报错并返回非零
- `--inspect` / `--dry-run` / `sync` 的既有互斥与行为边界不变

## 与现有文档的关系

- `docs/CLAUDE_CODE_SETUP.md`
  - 可把 selective sync 记为“最小可控同步”的下一步能力
- `docs/CONSISTENCY_VALIDATION.md`
  - 若后续纳管，应只校验 `--only` 的精确匹配边界，而不是扩展到通用过滤器
- `docs/ROADMAP.md`
  - 可作为下一阶段从 skills-only 全量同步推进到“精确单 skill 同步”的落点

## 建议的后续实施范围

若基于本设计推进实现，建议最小触达这些文件：

- 修改：`tools/sync_claude_code_skills.py`
- 修改：`docs/CLAUDE_CODE_SETUP.md`
- 视需要修改：`docs/CONSISTENCY_VALIDATION.md`
- 视需要修改：`docs/ROADMAP.md`

## 验收标准

当以下条件同时满足时，可认为 Claude Code selective sync 基线完成：

- `tools/sync_claude_code_skills.py` 支持 `--only <skill-name>`
- `--only` 按 skill 目录名精确匹配
- `--only` 在 inspect / dry-run / sync 三种模式下都生效
- 不存在的 skill 会硬失败并给出清楚错误
- 不带 `--only` 时，全量 12-skill 行为不被破坏
- 不引入多值过滤、组过滤、模式匹配或 exclude 逻辑
