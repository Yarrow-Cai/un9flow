# un9flow OpenClaw host design

## 背景

当前仓库已经完成：

- `docs/PLATFORMS.md` 中的多 host 方向与 OpenClaw 预留位说明
- `docs/ORCHESTRATION.md` 作为仓库内部总调度真源
- 三个主场景真源
- Claude Code host / setup / sync / inspect / selective sync / stale detect / prune advice / explicit prune 这条宿主接入链

但 OpenClaw 当前仍主要停留在 `docs/PLATFORMS.md` 里的“外层调度预留位”描述，还没有一份专门文档明确说明：OpenClaw 作为仓库外层调度器时，在 un9flow 体系中的角色边界、与内部总调度的关系、可以做什么和不能做什么。

## 目标

新增正式外层调度真源：

- `docs/OPENCLAW_HOST.md`

把 OpenClaw 从平台预留位推进成一个角色已定义的外层调度真源。

## 非目标

本轮明确不做：

- 不设计 OpenClaw 可执行接入脚本
- 不设计安装器或桥接脚本
- 不定义完整外层 API / schema
- 不把 OpenClaw 升级为新的主场景
- 不重写仓库内部总调度真源
- 不直接实现 host-to-host 运行链路

## 总体方案

采用“外层调度角色真源先行”的方式：

1. 新增 `docs/OPENCLAW_HOST.md`
2. 明确 OpenClaw 只是仓库外层的调度包裹者
3. 固定其与内部总调度、场景真源、正式 skill 入口的关系
4. 把“如何包裹并交给 un9flow”写清楚，但不进入可执行接入实现

## 文档分工

### `docs/PLATFORMS.md`

继续负责：

- 多 host 方向
- host 优先级
- OpenClaw 作为外层调度预留位
- 平台战略与非承诺边界

### `docs/ORCHESTRATION.md`

继续负责：

- 仓库内部总调度外壳
- 三主场景的统一主路由与分派规则

### `docs/OPENCLAW_HOST.md`

新增后负责：

- OpenClaw 作为外层调度器时，在 un9flow 体系中的角色边界
- 可负责的动作
- 不负责的动作
- 与内部总调度、场景真源、正式 skill 入口的关系
- 当前明确不承诺的 OpenClaw 能力边界

### `skills/orchestration/SKILL.md`

继续负责：

- 当前仓库内最稳的正式总入口对象

## OpenClaw 可负责的动作

建议 OpenClaw 只负责以下包裹层动作：

1. 外部请求承接
2. 是否进入 un9flow 的高层决策
3. 外部上下文的最小归一化
4. 将 un9flow 返回结果再回交给外层宿主链

## OpenClaw 不应负责的动作

必须明确禁止：

1. 不重写 `docs/ORCHESTRATION.md`
2. 不直接发明新场景
3. 不篡改：
   - `docs/INCIDENT_WORKFLOW.md`
   - `docs/BRINGUP_PATH.md`
   - `docs/DESIGN_SAFETY_REVIEW.md`
4. 不重写正式 `skills/**/SKILL.md` 的入口含义

## 权力分层

建议固定为：

- 外层：OpenClaw
  - 决定是否调用 un9flow
  - 负责外部请求 → 仓库入口 的承接
- 内层：un9flow orchestration
  - 决定三场景内部主路由
  - 决定 phase / specialist / artifact 主线

这意味着：OpenClaw 负责“包裹和承接”，un9flow 负责“内部规则与判定”。

## 最小交接关系

第一轮建议只定义最小交接：

### OpenClaw → un9flow

- 默认优先交给 `orchestration`
- 只有在证据极明确时，才考虑直接交给主场景入口
- 不建议由 OpenClaw 直接替仓库做三场景内部主判定

### un9flow → OpenClaw

- 返回场景选择结果
- 返回当前 control / result 结论
- 返回需要回外层继续处理的说明

本轮不把这些交接写成完整字段协议。

## `docs/OPENCLAW_HOST.md` 建议章节结构

建议至少固定以下章节：

1. `## 目标`
2. `## 外层调度定位`
3. `## 可负责的动作`
4. `## 不负责的动作`
5. `## 与仓库内总调度的关系`
6. `## 与场景真源和 skill 的关系`
7. `## 当前明确不承诺`

## 当前明确不承诺

至少应明确：

- 当前不代表已完成 OpenClaw 可执行接入
- 不代表已有 OpenClaw 安装器或桥接脚本
- 不代表已定义完整外层 API / schema
- 不代表当前仓库已支持 OpenClaw 直连运行
- 不代表 OpenClaw 已拥有仓库内部规则解释权

## 建议的后续实施范围

若基于本设计推进实现，建议最小触达这些文件：

- 新增：`docs/OPENCLAW_HOST.md`
- 修改：`docs/PLATFORMS.md`
- 视需要修改：`README.md`
- 视需要修改：`docs/CONSISTENCY_VALIDATION.md`

本设计本身不要求同步进入 OpenClaw 协议工程、接入清单或可执行桥接实现。

## 验收标准

当以下条件同时满足时，可认为 OpenClaw 外层调度真源基线完成：

- 仓库存在 `docs/OPENCLAW_HOST.md`
- 文档中明确 OpenClaw 是仓库外层调度包裹者，而不是内部规则拥有者
- 文档中明确可负责动作与不负责动作
- 文档中明确与 `docs/ORCHESTRATION.md`、场景真源与正式 `SKILL.md` 的关系
- 文档中明确当前不承诺 OpenClaw 可执行接入、安装器、桥接脚本与完整外层协议
