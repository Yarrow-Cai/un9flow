# un9flow 正式 SKILL.md 与 prompt 契约设计稿

日期：2026-04-16
主题：围绕总入口 skill、三子入口 skill 与 orchestrator prompt 契约，定义方法边界、协议边界与文档落点

## 1. 设计结论摘要

本轮设计采用如下方向：

- 采用 **总入口 + 三子入口 + 辅助 skill** 的正式 skill 版图
- 第一批覆盖三个场景：
  - `incident-investigation`
  - `bringup-path`
  - `design-safety-review`
- 同时保留场景内辅助 skill：
  - `evidence-pack`
  - `incident-review`
- 正式 `SKILL.md` 采用 **方法论文档型**，重点写目标、边界、输入、默认路径、Artifact 与协作关系
- orchestrator prompt 契约文档采用 **协议文档型**，重点写输入协议、输出协议、控制信号、硬约束与扩展点
- 二者分工明确：
  - `SKILL.md` 负责入口规范
  - prompt 契约负责调度协议

一句话总结：

> un9flow 的下一阶段，不是直接写 host 绑定的 skill 文件，而是先定义“总入口 skill + 三子入口 skill + 辅助 skill”的方法边界，再定义 orchestrator prompt 的协议边界；前者负责入口规范，后者负责调度协议。

---

## 2. 总入口 skill 与三子入口 skill 的版图结构

建议正式 skill 体系分为两层：

- 总入口层
- 场景入口层

并明确：**总入口负责调度，子入口负责场景边界。**

### 2.1 总入口 skill

总入口 skill 不是第四个场景 skill，而是 skill 层的 orchestrator 入口。

建议职责：

1. 接收不明确或跨场景请求
2. 判断用户是要显式进入某个场景，还是交给总调度裁决
3. 调用 orchestrator 总 prompt 契约
4. 产出统一的路由结果与后续动作建议

### 2.2 三个子入口 skill

三个场景入口 skill：

- `incident-investigation`
- `bringup-path`
- `design-safety-review`

共同职责：

1. 声明各自场景边界
2. 规范最小输入要求
3. 整理场景内的关键初始 Artifact
4. 把请求送入对应的 orchestrator / scenario prompt 契约
5. 约束输出应落到哪些场景工件上

### 2.3 辅助 skill

辅助 skill 不进入主入口层，而是挂在场景下：

- `evidence-pack`
- `incident-review`

它们是：

- 辅助 skill
- 不参与总路由竞争
- 只在特定场景内被显式调用或被主入口引导调用

### 2.4 版图关系

建议先固定结构：

```text
总入口 skill
  -> 三个场景入口 skill
    -> 场景专属 Artifact 组织
      -> orchestrator / scenario prompt 契约
        -> specialist dispatch
```

更具体地：

```text
[orchestration entry]
    ├── [incident-investigation]
    │      ├── evidence-pack
    │      └── incident-review
    ├── [bringup-path]
    └── [design-safety-review]
```

### 2.5 版图纪律

建议写死以下纪律：

1. 总入口不直接伪装成场景 skill
2. 场景 skill 不吞掉总调度职责
3. 辅助 skill 不参与主场景路由竞争
4. prompt 契约不取代 skill 文档边界

---

## 3. 总入口 skill 与子入口 skill 的职责切分

### 3.1 总入口 skill 应承担的规则

总入口 skill 只负责跨场景共性规则：

1. 入口裁决
2. 总路由规则
3. 总控制信号
4. 总输出骨架

#### 入口裁决

判断当前请求属于：

- 显式场景请求
- 不明确请求
- 多场景交叉请求

#### 总路由规则

只处理跨场景共性逻辑：

- 证据特征优先
- 建立中 vs 退化中
- 解释现象 vs 复核方案
- 冲突时选择最可执行场景

#### 总控制信号

回退、换轨、升级、进入 review gate 等控制信号在总入口统一定义。

#### 总输出骨架

至少统一：

- routing result
- phase backbone
- dispatch plan
- control result

### 3.2 子入口 skill 必须承担的规则

子入口 skill 只负责场景内规则：

1. 场景边界声明
2. 场景输入要求
3. 场景 Artifact 组织
4. 场景内默认 specialist 偏向

### 3.3 不该放在总入口的内容

总入口不负责：

1. 场景专属 Artifact 模板细节
2. 场景专属输入缺口清单
3. 场景专属 specialist 例外规则

### 3.4 不该放在子入口的内容

子入口不负责：

1. 重新定义主路由原则
2. 重新发明控制信号
3. 重新定义四层命名纪律

### 3.5 切分总句

建议用一句硬规则收口：

> 总入口 skill 负责“跨场景怎么裁决”，子入口 skill 负责“进入该场景后怎么约束”。

---

## 4. 正式 SKILL.md 的文档骨架

本轮正式 `SKILL.md` 采用 **方法论文档型**，重点不是命令说明，而是：

- 场景边界文档
- 输入 / 输出契约文档
- Artifact 约束文档
- 调度关系文档

### 4.1 总入口 `SKILL.md` 骨架

建议至少有 6 段：

1. 目标
2. 适用情况
3. 裁决原则
4. 输出骨架
5. 不负责什么
6. 与子入口的关系

### 4.2 子入口 `SKILL.md` 骨架

三个子入口统一采用 7 段骨架：

1. 目标
2. 适用边界
3. 最小输入要求
4. 默认 Phase 骨架
5. 默认 specialist 偏向
6. 主要 Artifact
7. 与总入口 / prompt 契约的关系

### 4.3 辅助 skill 的 `SKILL.md` 骨架

辅助 skill 骨架更短，但更硬。至少包含：

1. 目标
2. 仅适用于哪个场景
3. 输入要求
4. 输出 Artifact
5. 何时应返回主场景 skill
6. 不参与全局路由

### 4.4 写法统一约束

整个 `SKILL.md` 体系统一遵守：

1. 先写边界，再写能力
2. 先写输入，再写输出
3. 先写默认路径，再写例外
4. 先写不负责什么，再写如何协作

### 4.5 目录落点建议

建议后续正式 `SKILL.md` 落点：

- `skills/orchestration/SKILL.md`
- `skills/incident-investigation/SKILL.md`
- `skills/bringup-path/SKILL.md`
- `skills/design-safety-review/SKILL.md`
- `skills/evidence-pack/SKILL.md`
- `skills/incident-review/SKILL.md`

---

## 5. orchestrator prompt 契约文档骨架

prompt 契约文档不是 `SKILL.md` 的替代品，也不是 host 绑定文档，而是 orchestrator / scenario prompt 的统一协议层。

### 5.1 输入协议

建议固定为 4 段：

1. Case Input
2. Normalized Case
3. Routing Context
4. Control Context

#### Case Input
- 用户目标
- 原始症状
- 当前约束
- 当前给定证据

#### Normalized Case
- `stated_goal`
- `observed_symptoms`
- `evidence_inventory`
- `current_risk_state`
- `system_stage`
- `missing_evidence`

#### Routing Context
- 已候选 scenario
- 当前主路由
- 当前已有 phase
- 当前已有 specialist 输出
- 当前是否已有 review 结果

#### Control Context
- 是否允许继续
- 是否必须补证据
- 是否已触发换轨
- 是否已触发升级
- 是否已满足 review gate 条件

### 5.2 输出协议

建议固定为 4 段：

1. Routing Result
2. Phase Plan
3. Dispatch Plan
4. Control Result

#### Routing Result
- `primary_scenario`
- `secondary_candidates`
- `routing_rationale`

#### Phase Plan
- phase 顺序
- 哪些 phase 被跳过
- 哪些 phase 被补充
- 为什么这样排

#### Dispatch Plan
- specialist 列表
- dispatch reason
- expected artifacts

#### Control Result
- `control_signal`
- `next_actions`
- `unresolved_gaps`

### 5.3 硬约束

建议写死以下规则：

1. 不允许跳过 risk framing
2. 不允许把用户措辞直接当主路由
3. 不允许把 `Scenario / Phase / Domain Specialist / Artifact` 混成一层
4. 不允许证据不足时给高置信根因
5. 不允许跳过 review gate 直接收口
6. 不允许让场景内调度器越权承担总路由裁决

### 5.4 场景扩展点

需要明确：

- 哪些字段是三场景共用
- 哪些字段允许场景子 prompt 补充
- 哪些字段不能被场景子 prompt 改写

例如：
- 主路由规则不能被场景子 prompt 重写
- 场景专属 Artifact 可以由子 prompt 细化
- specialist 偏向可以被子 prompt 补强，但不能破坏总控制信号协议

### 5.5 落点建议

建议优先落成：

- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`

而不是直接落成某个 host 绑定的 prompt 文件。

---

## 6. 正式 SKILL.md 与 prompt 契约文档的配合关系

### 6.1 `SKILL.md` 负责什么

正式 `SKILL.md` 只负责：

1. 场景目标
2. 适用边界
3. 最小输入要求
4. 主要 Artifact 与协作关系

它更像 **入口规范**。

### 6.2 prompt 契约文档负责什么

prompt 契约文档只负责：

1. 输入协议
2. 输出协议
3. 控制信号
4. 硬约束与扩展点

它更像 **调度协议**。

### 6.3 两者边界

建议明确：

- `SKILL.md` 不重写调度协议
- prompt 契约文档不重写场景边界

### 6.4 在总入口和子入口上的具体配合

#### 总入口 skill
- `SKILL.md`：写总路由目标、适用边界、跨场景裁决原则
- prompt 契约：写总输入协议、总输出协议、总控制信号

#### 三个子入口 skill
- `SKILL.md`：写场景边界、最小输入、默认 Phase、主要 Artifact
- prompt 契约：写场景子 prompt 允许补充哪些字段、不能改写哪些总规则

#### 辅助 skill
- `SKILL.md`：写辅助目标、输入、输出、返回主场景条件
- prompt 契约：只保留很薄的输入 / 输出协议，不参与总路由

### 6.5 最终切分句

建议收口为：

> `SKILL.md` 决定“用户如何进入”，prompt 契约决定“agent 如何处理进入后的 case”。

---

## 7. 这轮 spec 的最终落点

建议这轮不要先散成很多 host 绑定文件，而是先落两类方法文档：

- `docs/SKILL_ARCHITECTURE.md`
  - 解释总入口、三子入口、辅助 skill 的结构关系

- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
  - 定义 orchestrator prompt 协议

然后再进入正式 skill 文件实现阶段：

- `skills/orchestration/SKILL.md`
- `skills/incident-investigation/SKILL.md`
- `skills/bringup-path/SKILL.md`
- `skills/design-safety-review/SKILL.md`
- `skills/evidence-pack/SKILL.md`
- `skills/incident-review/SKILL.md`

也就是说，这轮先把 **方法与协议** 讲清，再写真正的 `SKILL.md`。

---

## 8. 最终结论

本轮设计的推荐方向是：

> 先定义“总入口 skill + 三子入口 skill + 辅助 skill”的方法边界，再定义 orchestrator prompt 的协议边界；前者负责入口规范，后者负责调度协议。