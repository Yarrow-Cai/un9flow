# un9flow 统一校验体系设计稿

日期：2026-04-17
主题：围绕 docs 为主真源，建立覆盖 docs / skills / templates / routing cases / 过程文档 的统一一致性校验体系

## 1. 设计结论摘要

本轮设计采用如下方向：

- 采用 **docs 为主真源** 的统一校验体系
- 第一批强校验对象采取 **全量纳入**：
  - docs
  - skills
  - templates
  - routing cases
  - 过程文档
- 校验体系采用 **双层型**：
  - 第一层：人工 / 规则文档
  - 第二层：后续可脚本化的机器可读预留结构
- 引入 3 级失败模型：
  - L1 阻断级
  - L2 重要级
  - L3 整理级
- 第一轮只落文档与模板，不做自动校验脚本、CI 校验器、生成器或 host-specific 校验流程

一句话总结：

> 先建立 docs 为主真源的统一校验体系，用一个总校验文档、一个 review checklist、一个 findings 模板，把 docs / skills / templates / routing cases / 过程文档纳入同一套一致性检查流程。

---

## 2. 统一校验体系的对象分层与真源关系

建议先把校验对象固定成五层结构：

```text
Level 1: docs 真源层
Level 2: 正式 skills 映射层
Level 3: 模板层
Level 4: 案例层
Level 5: 过程文档层
```

### 2.1 docs 真源层

主真源文件：

- `docs/ORCHESTRATION.md`
- `docs/INCIDENT_WORKFLOW.md`
- `docs/SKILL_ARCHITECTURE.md`
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`

职责：

1. 总调度规则真源
2. incident 场景真源
3. skill 架构真源
4. prompt 协议真源

受 docs 真源层约束的入口/派生文档：

- `README.md`（入口文档）
- `docs/ROADMAP.md`（派生文档）
- `docs/WORKFLOW.md`（派生文档）
- `docs/PLATFORMS.md`（派生文档）

说明：上述文档受 docs 真源层约束，属于 docs 层需要显式纳入校验范围的对象，不是平级主真源。

### 2.2 正式 skills 映射层

对应文件：

- `skills/orchestration/SKILL.md`
- `skills/incident-investigation/SKILL.md`
- `skills/bringup-path/SKILL.md`
- `skills/design-safety-review/SKILL.md`
- `skills/evidence-pack/SKILL.md`
- `skills/incident-review/SKILL.md`

角色：

> docs 真源在正式 skill 文件中的映射层。

### 2.3 模板层

包括：

- checklist 模板
- artifact 模板
- routing matrix 模板
- prompt checklist 模板
- skill boundary checklist 模板

角色：

> 把规则变成可填写、可校验、可复核的工件结构。

### 2.4 案例层

包括：

- routing cases
- 示例 case
- review 用例
- 路由矩阵实例

角色：

> 验证规则是否能解释真实输入。

### 2.5 过程文档层

包括：

- `docs/superpowers/specs/*.md`
- `docs/superpowers/plans/*.md`

角色：

> 受控从属层。

它们不是真源，但不能长期与真源冲突。

### 2.6 三条硬规则

建议写死：

1. 主真源只在 docs 层
2. skills 层只能映射，不得反向定义规则
3. 模板 / 案例 / 过程文档只允许继承或验证，不允许发明新规则

---

## 3. 每一层各自要校验什么

### 3.1 docs 真源层

重点校验：

1. 职责边界
2. 术语一致性
3. 规则完整性

它更像：**规则完整性检查**。

### 3.2 正式 skills 层

重点校验：

1. 边界映射
2. 结构映射
3. 规则不越权

它更像：**真源映射正确性检查**。

### 3.3 模板层

重点校验：

1. 字段完整性
2. 允许值约束
3. 可填写性

它更像：**结构可承载性检查**。

### 3.4 案例层

重点校验：

1. 典型 case 覆盖
2. 路由可解释性
3. 回归稳定性

它更像：**规则可解释性与回归稳定性检查**。

### 3.5 过程文档层

重点校验：

1. 是否仍与主真源冲突
2. 是否需要同步
3. 是否仍可作为历史依据

它更像：**历史一致性检查**。

---

## 4. 统一校验体系的失败等级与处理动作

### 4.1 L1 阻断级失败

定义：

> 直接破坏真源、层级、路由或控制信号一致性的错误。

典型例子：

- docs 真源互相矛盾
- skills 重写总调度规则
- 出现未定义新 `control_signal`
- 辅助 skill 被写成全局主路由入口
- 模板允许值和真源冲突

处理动作：

- 必须先修
- 禁止进入下一步
- 禁止提交 / push / 继续扩展

### 4.2 L2 重要级失败

定义：

> 不会立刻破坏真源，但会明显削弱一致性或让后续实现偏航。

典型例子：

- 路由矩阵示例不足
- 场景 “不负责什么” 写得太弱
- Artifact 命名不够结构化
- 文档落点说明不清

处理动作：

- 原则上本轮修掉
- 若不修，必须显式记录为 concern

### 4.3 L3 整理级问题

定义：

> 不直接影响规则正确性，更像文档质量或整洁度问题。

典型例子：

- 表达重复
- 列表顺序不统一
- 用词略微不稳但未改变含义

处理动作：

- 可顺手修
- 可留待后续整理
- 不阻断主流程

### 4.4 处理表

| 等级 | 含义 | 处理动作 |
|------|------|----------|
| L1 | 阻断级 | 立即修复，未修不得继续 |
| L2 | 重要级 | 本轮优先修；若不修必须显式记录 |
| L3 | 整理级 | 可顺手修，不阻断流程 |

---

## 5. 这套统一校验体系应该落成哪些文档与模板

建议采用 **一主两辅** 结构：

### 5.1 总校验文档

建议新增：

- `docs/CONSISTENCY_VALIDATION.md`

职责：

1. 校验对象五层结构
2. docs 为主真源的规则
3. 每层校验职责
4. 失败等级与处理动作
5. 校验顺序
6. 允许忽略什么 / 不允许忽略什么

### 5.2 模板 1：一致性检查清单

建议新增：

- `docs/templates/consistency-review-checklist.md`

职责：

> 一轮 review 的执行清单。

### 5.3 模板 2：失败记录模板

建议新增：

- `docs/templates/validation-findings.md`

职责：

> 问题记录、分级与关闭跟踪。

### 5.4 案例层模板

本轮不新增新模板，继续使用：

- `docs/templates/skill-routing-matrix.md`

作为案例层模板。

### 5.5 推荐落点

```text
docs/
├── CONSISTENCY_VALIDATION.md
└── templates/
    ├── consistency-review-checklist.md
    ├── validation-findings.md
    └── skill-routing-matrix.md
```

---

## 6. 这轮 spec 的最终落点与实现顺序

### 6.1 这轮 spec 的最终落点

本轮不是做自动校验器，而是先把人工可执行、后续可脚本化的统一校验体系讲清。

### 6.2 后续实现落点

建议优先落地：

1. `docs/CONSISTENCY_VALIDATION.md`
2. `docs/templates/consistency-review-checklist.md`
3. `docs/templates/validation-findings.md`
4. 继续复用 `docs/templates/skill-routing-matrix.md`

### 6.3 实现顺序建议

建议固定为：

1. 总校验文档
2. review checklist
3. findings 模板

### 6.4 这轮明确不做

- 不做自动校验脚本
- 不做 CI 校验器
- 不做文档生成器
- 不做 host-specific 校验流程
- 不做额外案例模板

也就是：文档与模板先行，为脚本化预留结构。

---

## 7. 最终结论

本轮统一校验体系设计的推荐方向是：

> 先建立 docs 为主真源的统一校验体系，用一个总校验文档、一个 review checklist、一个 findings 模板，把 docs / skills / templates / routing cases / 过程文档纳入同一套一致性检查流程。