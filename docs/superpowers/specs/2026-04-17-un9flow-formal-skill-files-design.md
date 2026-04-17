# un9flow 正式 skills/*/SKILL.md 文件设计稿

日期：2026-04-17
主题：围绕总入口、三主场景与 incident 辅助 skill，定义第一批正式 `skills/*/SKILL.md` 文件的版图、骨架与实现顺序

## 1. 设计结论摘要

本轮设计采用如下方向：

- 第一批正式 skill 文件采用 **1 个总入口 + 3 个主场景入口 + 2 个 incident 辅助 skill** 的最小完整体系
- 三个主场景入口全部正式落地：
  - `incident-investigation`
  - `bringup-path`
  - `design-safety-review`
- incident 辅助 skill 同时正式落地：
  - `evidence-pack`
  - `incident-review`
- 所有正式 `SKILL.md` 文件采用 **双层写法**：
  - 正文保持方法论文档风格
  - 文末单独补一小节 Claude Code 宿主约束
- 总入口采用 **双模式入口**：
  - 自动路由模式
  - 显式总调度模式
- 三个主场景采用 **统一主骨架 + 场景特化段**
- `evidence-pack` 强调 **主动找证据 / 补证据**，而不是被动整理输入

一句话总结：

> un9flow 的下一阶段，不是继续停留在架构与协议文档，而是按“总入口 → 三主场景 → incident 辅助”的顺序，落一组方法正文稳定、宿主附录很薄的正式 `skills/*/SKILL.md` 文件。

---

## 2. 正式 `skills/*/SKILL.md` 文件版图与目录结构

建议这一轮只落最小但完整可用的 6 个正式 skill 文件：

```text
skills/
├── orchestration/
│   └── SKILL.md
├── incident-investigation/
│   └── SKILL.md
├── bringup-path/
│   └── SKILL.md
├── design-safety-review/
│   └── SKILL.md
├── evidence-pack/
│   └── SKILL.md
└── incident-review/
    └── SKILL.md
```

### 2.1 总入口

- `skills/orchestration/SKILL.md`

它是唯一总入口 skill，不是第四个场景，而是：

- 接收模糊请求
- 接收跨场景请求
- 允许显式走总调度
- 把请求送入 orchestrator 总调度外壳

### 2.2 三个主场景入口

- `skills/incident-investigation/SKILL.md`
- `skills/bringup-path/SKILL.md`
- `skills/design-safety-review/SKILL.md`

它们是：

- 用户可直接进入的主场景 skill
- 有明确边界、输入要求、默认 Phase 与 Artifact 约束
- 不重写总调度协议

### 2.3 incident 辅助 skill

- `skills/evidence-pack/SKILL.md`
- `skills/incident-review/SKILL.md`

这一轮只正式落 incident 辅助，不继续扩更多辅助 skill。

### 2.4 当前明确不落的内容

本轮明确不做：

- 更多辅助 skill
- host-specific 变体 skill
- 自动生成脚本
- 安装器
- prompt 文件本体

本轮只落正式 `SKILL.md` 文件本身。

---

## 3. 总入口 `skills/orchestration/SKILL.md` 的正式骨架

这个文件必须支持两种用法：

1. 用户没想清楚，交给它裁决
2. 用户明确要求先走总调度

### 3.1 文档定位

开头需明确：

- 它不是第四个场景
- 它不是 incident 的别名
- 它是总入口 skill
- 它负责把请求接入总调度外壳，而不是重写场景规则

### 3.2 正文骨架

建议至少包含：

1. 目标
2. 进入条件（自动路由模式 / 显式总调度模式）
3. 裁决原则
4. 输出骨架
5. 不负责什么
6. 与子入口的关系

### 3.3 裁决原则

这里应只写总入口独有规则：

- 证据特征优先
- 建立中 vs 退化中
- 解释现象 vs 复核方案
- 冲突时选最可执行场景

### 3.4 输出骨架

至少写清：

- `Routing Result`
- `Phase Plan`
- `Dispatch Plan`
- `Control Result`

### 3.5 Claude Code 宿主附录

作为文末单独附录写明：

- 在 Claude Code 下可作为总入口 skill 使用
- 当用户请求场景不清、跨场景或显式要求调度时，优先使用它
- 应把请求送入 orchestrator 规则，而不是临时发明新路由原则

### 3.6 与现有总调度文档的关系

需明确写出：

- 入口边界以本文件为准
- 总调度规则以 `docs/ORCHESTRATION.md` 为准
- 输入 / 输出协议以 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 为准

---

## 4. 三个主场景 `SKILL.md` 的统一主骨架 + 场景特化段

三个主场景 skill 应采用统一主骨架，避免风格漂移；同时每个场景允许 1~2 段特化内容。

### 4.1 共用主骨架

建议三份文件统一顺序：

1. 目标
2. 适用边界
3. 最小输入要求
4. 默认 Phase 骨架
5. 默认 specialist 偏向
6. 主要 Artifact
7. 不负责什么
8. 与总入口 / prompt 契约的关系
9. Claude Code 宿主附录

### 4.2 `incident-investigation` 的特化段

建议增加：

#### 证据流转与收敛说明

强调：

- `evidence_inventory`
- `evidence-pack`
- `incident-orchestrator`
- `incident-review`

之间的流转关系。

### 4.3 `bringup-path` 的特化段

建议增加：

#### 建立基线优先说明

强调：

- 先建立确定性基线
- 再验证链路拉通
- 再进入异常验证

### 4.4 `design-safety-review` 的特化段

建议增加：

#### 方案复核与边界审查说明

强调：

- 审风险边界
- 审状态收敛
- 审 timeout / watchdog / failsafe
- 审设计是否可验证

### 4.5 “不负责什么”的差异化

三者必须在“不负责什么”这一段明显不同：

- `incident-investigation`：不负责把系统从零拉通；不替代完整设计评审
- `bringup-path`：不把所有运行期异常都当 incident 解释；不在未建立基线前给过度诊断结论
- `design-safety-review`：不替代活跃故障排查；不在缺乏证据时充当 incident 根因定位器

---

## 5. incident 辅助 skill 的正式 `SKILL.md` 骨架

### 5.1 `evidence-pack/SKILL.md`

它不是被动整理器，而是：

> 证据侦察与补证据入口。

建议骨架至少包含：

1. 目标
2. 仅适用于哪个场景
3. 何时应使用
4. 输入要求
5. 核心动作
6. 输出 Artifact
7. 何时返回主场景
8. 不负责什么

关键强调：

- 主动识别证据缺口
- 生成下一轮取证 / 观测建议
- 形成 `evidence-package`

### 5.2 `incident-review/SKILL.md`

它不是继续分析，而是：

> 对 incident 当前结论做 second opinion 和收口前复核。

建议骨架至少包含：

1. 目标
2. 仅适用于哪个场景
3. 何时应使用
4. 输入要求
5. 输出 Artifact
6. 何时返回主场景
7. 不负责什么

关键强调：

- 检查当前证据链是否完整
- 如果不完整，明确退回主链或退回 `evidence-pack`

### 5.3 两个辅助 skill 的共同纪律

建议写死：

1. 不参与全局路由竞争
2. 必须写清回到主场景的条件
3. 必须写清不负责什么

---

## 6. 这轮正式 `SKILL.md` 文件的整体落点与实现顺序

### 6.1 第一批正式落地文件

```text
skills/
├── orchestration/
│   └── SKILL.md
├── incident-investigation/
│   └── SKILL.md
├── bringup-path/
│   └── SKILL.md
├── design-safety-review/
│   └── SKILL.md
├── evidence-pack/
│   └── SKILL.md
└── incident-review/
    └── SKILL.md
```

### 6.2 实现顺序建议

建议按依赖顺序写：

1. `skills/orchestration/SKILL.md`
2. `skills/incident-investigation/SKILL.md`
3. `skills/bringup-path/SKILL.md`
4. `skills/design-safety-review/SKILL.md`
5. `skills/evidence-pack/SKILL.md`
6. `skills/incident-review/SKILL.md`

### 6.3 本轮明确不做

- 自动生成脚本
- 安装器
- host-specific 多版本 skill
- 更多辅助 skill
- prompt 文件本体

### 6.4 写法统一建议

所有正式 `SKILL.md` 采用双层写法：

#### 正文
- 方法边界
- 输入输出
- 默认路径
- Artifact
- 不负责什么
- 协作关系

#### 文末附录
- Claude Code 下的最小宿主约束
- slash / 入口语气
- 使用提醒

---

## 7. 最终结论

本轮正式 skill 文件设计的推荐方向是：

> 先按“总入口 → 三主场景 → incident 辅助”顺序，落一组方法正文稳定、宿主附录很薄的正式 `skills/*/SKILL.md` 文件；其中总入口采用双模式，主场景采用统一骨架 + 场景特化，incident 辅助强调主动找证据与证据链复核。