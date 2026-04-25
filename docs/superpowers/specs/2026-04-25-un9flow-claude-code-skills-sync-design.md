# un9flow Claude Code skills sync design

## 背景

当前仓库已经完成：

- Claude Code host 接入真源：`docs/CLAUDE_CODE_HOST.md`
- Claude Code setup 真源：`docs/CLAUDE_CODE_SETUP.md`
- 正式 `skills/**/SKILL.md` 入口集合
- 一致性校验与 generation regression 基线

但目前仍停留在“有文档真源、有 setup 说明”的阶段，还没有一个真正可执行的最小 host 接入动作，能够把正式 skill 入口同步到 Claude Code 消费目录模型中。

## 目标

新增一个最小可执行同步器：

- `tools/sync_claude_code_skills.py`

把正式 `skills/**/SKILL.md` 入口，同步到一个 Claude Code 消费目录骨架中。

## 非目标

本轮明确不做：

- 不设计自动安装器
- 不设计多 host 同步器
- 不同步 docs 真源
- 不同步 templates
- 不同步 cases
- 不同步 golden / regression 文件
- 不做双向同步
- 不改写 `SKILL.md` 内容
- 不做复杂 diff / prune / watch / config file

## 总体方案

采用“skills-only 最小同步器”方案：

1. 新增 `tools/sync_claude_code_skills.py`
2. 只发现并同步 `skills/**/SKILL.md`
3. 目标目录结构尽量镜像仓库内 skill 结构
4. 用最小 CLI 支持：
   - `--target-root <path>`
   - `--dry-run`
   - `--force`

## 脚本职责

本轮脚本只承担四件事：

1. 发现正式 skill 入口
2. 构建稳定目标路径映射
3. 执行最小同步
4. 输出可审查 summary

## 目标目录模型

推荐固定为：

- `<target-root>/skills/<skill-name>/SKILL.md`

也就是保留和仓库内一致的 skill 目录结构。

示例：

- 来源：`skills/orchestration/SKILL.md`
- 目标：`<target-root>/skills/orchestration/SKILL.md`

- 来源：`skills/bringup-path/SKILL.md`
- 目标：`<target-root>/skills/bringup-path/SKILL.md`

## 路径规则

- 来源路径模式：`skills/**/SKILL.md`
- 目标路径：按来源相对路径直接拼接到 `--target-root`
- 不重命名 skill 目录名
- 不重命名文件名 `SKILL.md`

## CLI 设计

本轮推荐最小 CLI：

- `--target-root <path>`
- `--dry-run`
- `--force`

其中：

- `--target-root` 是必填参数
- `--dry-run` 用于预演同步结果但不写文件
- `--force` 用于显式允许覆盖已存在目标文件

## 最小行为

### 默认行为

若不传 `--dry-run`，则执行真实同步。

### `--dry-run`

输出：

- `DRY-RUN`
- `FOUND <n> skills`
- `PLAN COPY <source> -> <target>`

但不真正写文件。

### `--force`

若目标文件已存在：

- 未传 `--force`：失败或标记 failed
- 传入 `--force`：允许覆盖

## 输出格式

推荐最小输出：

### dry-run

- `DRY-RUN`
- `FOUND <n> skills`
- `PLAN COPY <source> -> <target>`

### 真实同步成功

- `SYNCED <source> -> <target>`

### 汇总

- `SUMMARY: synced <n>, skipped <m>, failed <k>`

## 错误边界

本轮只做最小错误边界处理：

- 缺少 `--target-root` → 报错
- 没找到任何 `skills/**/SKILL.md` → 报错
- 目标文件已存在且未传 `--force` → 报错或 failed
- 允许自动创建目标父目录
- 不做复杂恢复逻辑

## 与现有文档的关系

- `docs/CLAUDE_CODE_HOST.md`
  - 定义 `skills/**/SKILL.md` 是 Claude Code 的直接消费层
- `docs/CLAUDE_CODE_SETUP.md`
  - 定义 Claude Code 如何最小接起来
  - 本脚本可以作为 setup 真源的第一批可执行落点
- `docs/PLATFORMS.md`
  - 保持平台战略层，不承担该脚本细节

## 建议的后续实施范围

若基于本设计推进实现，建议最小触达这些文件：

- 新增：`tools/sync_claude_code_skills.py`
- 修改：`docs/CLAUDE_CODE_SETUP.md`
- 视需要修改：`docs/CLAUDE_CODE_HOST.md`
- 视需要修改：`docs/CONSISTENCY_VALIDATION.md`
- 视需要修改：`docs/ROADMAP.md`

## 验收标准

当以下条件同时满足时，可认为 Claude Code skills-only 同步脚本基线完成：

- 仓库存在 `tools/sync_claude_code_skills.py`
- 脚本只发现并处理 `skills/**/SKILL.md`
- 脚本支持 `--target-root`、`--dry-run`、`--force`
- 目标目录路径按来源相对路径稳定镜像
- dry-run 可输出清晰计划
- 真实同步可输出逐项结果与 summary
- 不同步 docs / templates / cases / golden / regression 文件
