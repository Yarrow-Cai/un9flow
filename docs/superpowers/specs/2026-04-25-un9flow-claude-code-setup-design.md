# un9flow Claude Code setup design

## 背景

当前仓库已经完成：

- 正式 `skills/**/SKILL.md` 入口集合
- 三场景真源与总调度真源
- 模板生成体系与 generation regression 基线
- Claude Code host 接入真源：`docs/CLAUDE_CODE_HOST.md`

但当前仍缺少一份专门面向 Claude Code 的 setup 真源文档，说明使用者在本地最小需要准备什么、setup 必须关心哪些对象、最小步骤是什么、setup 后如何验证，以及当前 setup 明确不覆盖什么。

## 目标

新增正式 setup 真源：

- `docs/CLAUDE_CODE_SETUP.md`

把 Claude Code 从“如何消费仓库”的说明推进到“如何最小把仓库接起来”的 setup 骨架说明。

## 非目标

本轮明确不做：

- 不设计自动安装器
- 不设计自动目录同步脚本
- 不设计一键 setup
- 不设计多 host setup
- 不设计发布系统或分发流程
- 不自动复制 `skills/**/SKILL.md` 到宿主目录
- 不自动生成 Claude Code 本地配置

## 总体方案

采用“Claude Code setup 真源单独落地”的方式：

1. 新增 `docs/CLAUDE_CODE_SETUP.md`
2. 把 setup 视角下的对象分成三类：
   - 必须关心的对象
   - 可选关心的对象
   - 明确不属于 setup 的对象
3. 固定最小 setup 步骤与 setup 后验证标准
4. 让 `docs/CLAUDE_CODE_HOST.md` 继续负责“怎么理解并消费”，而 `docs/CLAUDE_CODE_SETUP.md` 负责“怎么最小接起来”

## 文档分工

### `docs/PLATFORMS.md`

继续负责：

- 平台战略
- host 优先级
- 非承诺边界

### `docs/CLAUDE_CODE_HOST.md`

继续负责：

- Claude Code 如何消费本仓库
- 目录映射
- 当前可消费能力
- 当前不承诺边界

### `docs/CLAUDE_CODE_SETUP.md`

新增后负责：

- Claude Code 本地最小 setup 前提
- setup 必须关心的对象
- setup 的最小步骤
- setup 后的最小验证方式
- 当前 setup 不覆盖的范围

### `skills/**/SKILL.md`

继续负责：

- 正式 skill 入口对象

## setup 视角下的对象边界

### 1. 必须关心的对象

- `skills/**/SKILL.md`
- `docs/CLAUDE_CODE_HOST.md`
- `docs/SKILL_ARCHITECTURE.md`
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
- `docs/ORCHESTRATION.md`
- `tools/validate_consistency.py`
- `tools/run_generation_regression.py`

这些对象共同构成“能最小接起来并验证”的基础材料。

### 2. 可选关心的对象

- `docs/INCIDENT_WORKFLOW.md`
- `docs/BRINGUP_PATH.md`
- `docs/DESIGN_SAFETY_REVIEW.md`
- `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- `docs/REGISTER_STATE_AUDIT.md`
- `docs/templates/**`
- `docs/cases/**`

这层不是 setup 成立的第一步硬前提，但在真实使用中具有很高价值。

### 3. 明确不属于 setup 的对象

- 自动安装器
- 自动目录同步脚本
- 多 host setup
- 分发包 / 发布产物
- CI 平台配置自动注入
- 外部平台专用目录映射

## `docs/CLAUDE_CODE_SETUP.md` 建议章节结构

建议至少固定以下章节：

1. `## 目标`
2. `## setup 前提`
3. `## 最小 setup 对象`
4. `## 最小 setup 步骤`
5. `## setup 后验证`
6. `## 当前明确不做`
7. `## 与其他文档的关系`

## setup 前提

`docs/CLAUDE_CODE_SETUP.md` 应明确至少以下前提：

- 本地已获取仓库完整内容
- 正式 `skills/**/SKILL.md` 存在
- Python 环境可运行 `tools/validate_consistency.py` 与 `tools/run_generation_regression.py`
- 使用者理解 `docs/CLAUDE_CODE_HOST.md`、`docs/SKILL_ARCHITECTURE.md` 与 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 的角色分工

## 最小 setup 步骤

建议固定 5 步：

1. 准备仓库
2. 确认正式入口来自 `skills/**/SKILL.md`
3. 确认规则支撑文档
4. 运行最小验证：
   - `python tools/validate_consistency.py`
   - `python tools/run_generation_regression.py --check`
5. 从总入口或三个主场景 skill 开始消费

## setup 后验证

建议把 setup 成立的最小条件定义为：

1. 本地存在正式 `skills/**/SKILL.md`
2. Claude Code host 真源与关键 docs 可读
3. consistency validation 通过
4. generation regression check 通过
5. `README.md` / `docs/PLATFORMS.md` / `docs/CLAUDE_CODE_HOST.md` / `docs/CLAUDE_CODE_SETUP.md` 之间入口关系可追溯

## 当前明确不做

至少应明确：

- 不自动复制 skill 到宿主目录
- 不自动生成 Claude Code 本地配置
- 不自动注入 slash command
- 不自动处理跨仓库映射
- 不提供一键 setup
- 不保证 setup 文档之外的 host 也成立

## 与其他文档的关系

`docs/CLAUDE_CODE_SETUP.md` 应明确回指：

- `docs/CLAUDE_CODE_HOST.md`
- `docs/PLATFORMS.md`
- `docs/SKILL_ARCHITECTURE.md`
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`

并说明：

- host 接入语义问题回 `docs/CLAUDE_CODE_HOST.md`
- 平台战略与非承诺边界问题回 `docs/PLATFORMS.md`
- skill 入口边界问题回 `docs/SKILL_ARCHITECTURE.md`
- prompt 协议问题回 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`

## 建议的后续实施范围

若基于本设计推进实现，建议最小触达这些文件：

- 新增：`docs/CLAUDE_CODE_SETUP.md`
- 修改：`docs/CLAUDE_CODE_HOST.md`
- 修改：`README.md`
- 视需要修改：`docs/CONSISTENCY_VALIDATION.md`
- 视需要修改：`docs/ROADMAP.md`

但本设计本身不要求同步实现自动安装器或 setup 脚本。

## 验收标准

当以下条件同时满足时，可认为 Claude Code 最小 setup 骨架基线完成：

- 仓库存在 `docs/CLAUDE_CODE_SETUP.md`
- 文档中明确区分必须关心对象、可选关心对象、明确不属于 setup 的对象
- 文档中固定最小 setup 步骤
- 文档中固定 setup 后验证标准
- 文档中明确当前 setup 不覆盖自动安装、自动映射、多 host 与分发系统
- `README.md` 或 host 入口文档已能把 Claude Code setup 真源暴露为可发现入口
