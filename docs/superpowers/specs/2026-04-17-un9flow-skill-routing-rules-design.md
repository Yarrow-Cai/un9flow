# un9flow skill 入口路由执行规则设计稿

日期：2026-04-17
主题：围绕正式 `skills/*/SKILL.md` 文件，定义总入口优先级、子入口直进边界、辅助 skill 受控进入条件，以及这些规则在总文档与 skill 文件中的分层落点

## 1. 设计结论摘要

本轮设计采用如下方向：

- 入口路由默认采用 **混合优先**：
  - 明确场景时直进子入口
  - 模糊、交叉或跨场景请求时先走总入口 `orchestration`
- incident 辅助 skill 保持 **受控进入**：
  - `evidence-pack`
  - `incident-review`
  都不参与全局首路由竞争
- 入口路由规则采用三层落文档方式：
  - `docs/ORCHESTRATION.md`：总规则真源
  - `skills/orchestration/SKILL.md`：路由摘要
  - 子入口与辅助 skill：只写自身进入边界
- 这轮不扩新 skill，不写 host-specific routing 逻辑，也不写自动化脚本，只把规则本身讲清

一句话总结：

> 在正式 `SKILL.md` 文件已经落地之后，下一步优先定义 skill 之间的入口路由规则：明确总入口优先级、子入口直进边界、辅助 skill 受控进入条件，以及这些规则在总文档与 skill 文件中的分层落点。

---

## 2. 入口路由判定规则本体

核心原则：

> 明确场景时直进子入口；模糊、交叉或跨场景请求时先走总入口；辅助 skill 不参与全局首路由竞争。

### 2.1 一级判定：主入口 vs 辅助 skill

主入口候选：

- `orchestration`
- `incident-investigation`
- `bringup-path`
- `design-safety-review`

辅助 skill：

- `evidence-pack`
- `incident-review`

强约束：

- 辅助 skill 默认不参与全局首路由竞争
- 辅助 skill 只在显式点名或主场景内受控切换时进入

### 2.2 什么时候直进子入口

满足以下条件时，直接进入对应子入口：

1. 用户目标明确
2. 证据模式与目标一致
3. 当前不需要跨场景裁决

### 2.3 什么时候必须先走总入口

以下情况统一先进 `orchestration`：

1. 请求模糊
2. 场景交叉
3. 用户显式要求总调度（例如一开始就要求 routing result / phase backbone / dispatch plan / control result）

### 2.4 辅助 skill 的进入规则

#### `evidence-pack`

只允许两种进入方式：

1. 用户显式要求先整理证据 / 补证据
2. `incident-investigation` 主链明确要求先补证据

#### `incident-review`

只允许两种进入方式：

1. 用户显式要求复核当前 incident 结论
2. incident 主链已经形成初步结论，准备进入 review gate

### 2.5 路由优先级顺序

建议优先级固定为：

1. 显式总调度请求 -> `orchestration`
2. 显式主场景且证据一致
3. 模糊 / 交叉 / 跨场景 -> `orchestration`
4. 显式辅助 skill 点名（仅在 incident 语义上下文中成立）
5. 低置信度判断时，宁可走总入口，不误塞子入口

### 2.6 禁止规则

明确禁止：

1. `evidence-pack` 参与全局主路由竞争
2. `incident-review` 充当通用 review skill
3. 子入口重写总入口路由原则
4. 在场景冲突时直接拍脑袋塞进某个子入口

---

## 3. 总入口与三子入口的路由判定示例矩阵

建议配一组典型示例矩阵，用于后续文档校验与 host 适配。

### 3.1 典型直进子入口样例

#### 直进 `incident-investigation`

- 用户明确说在排查故障
- 系统原本能工作
- 当前有运行期异常
- 存在掉线、复位、watchdog 异常等现象

#### 直进 `bringup-path`

- 用户明确说是新板 / 新链路 / 新模块
- 当前任务是首次拉通
- 问题集中在上电、初始化、首次通信建立失败

#### 直进 `design-safety-review`

- 用户明确说是 design review / safety audit
- 当前没有活跃故障排查压力
- 材料主要是设计说明、状态机、timeout/watchdog/failsafe 方案

### 3.2 必须先进总入口的样例

#### 模糊请求

- “帮我看看这个系统为什么不太对”
- “你觉得我应该从哪查”

#### 场景交叉：incident vs bringup

- 通信不通，但还无法判断是新板首次拉通还是既有系统退化掉线

#### 用户说 review，但证据像 active incident

- 用户措辞是“review”，但材料全是现网掉线、CRC 错误、watchdog reset

### 3.3 辅助 skill 进入样例

#### 进入 `evidence-pack`

- 用户显式要求先整理证据 / 补证据
- incident 主链判断并明确要求“当前证据不足，先补证据”

#### 进入 `incident-review`

- 用户明确要求复核 incident 结论
- incident 已形成初步诊断包，准备进入 review gate

### 3.4 推荐矩阵字段

建议后续写成固定表格：

- case id
- user phrasing
- evidence profile
- route decision
- why this route
- why not others

---

## 4. 辅助 skill 的受控进入与禁止规则

### 4.1 `evidence-pack`

定位：

> incident 场景内的证据侦察 / 补证据入口。

只允许：

1. 用户显式要求先整理证据或补证据
2. incident 主链内回退进入

禁止：

1. 参与全局主路由竞争
2. 单独充当 incident 主入口
3. 在没有 incident 语义时被误当成通用证据整理器
4. 直接输出根因结论

### 4.2 `incident-review`

定位：

> incident 场景内的收口前复核入口。

只允许：

1. 用户显式要求复核当前 incident 结论
2. incident 主链进入 review gate 前触发

禁止：

1. 参与全局主路由竞争
2. 充当通用 review / audit skill
3. 替代 `design-safety-review`
4. 在证据链明显不足时给“通过”结论

### 4.3 与主场景的关系

建议显式写明：

```text
incident-investigation
  -> evidence-pack（证据不足时前置补证据）
  -> incident-orchestrator
  -> incident-review（收口前复核）
```

---

## 5. 入口路由执行规则的文档落点方式

建议采用三层落文档方式：

### 5.1 `docs/ORCHESTRATION.md`

写完整总规则：

- 路由原则
- 判定矩阵
- 例外
- 禁止规则

### 5.2 `skills/orchestration/SKILL.md`

写路由摘要：

- 进入条件
- 路由原则
- 输出骨架
- 指向总文档

### 5.3 子入口 `SKILL.md`

只写自身边界：

- 何时允许被直进
- 何时不该被误进
- 和其他场景的分界

### 5.4 辅助 skill `SKILL.md`

只写受控进入规则：

- 不能抢主入口
- 何时能进
- 何时必须退回主链

### 5.5 总结规则

建议用一句硬规则收口：

> 总规则只在 `docs/ORCHESTRATION.md` 完整定义；`skills/orchestration/SKILL.md` 只承接；子入口和辅助 skill 只声明自己的边界。

---

## 6. 这轮 spec 的最终落点与实现顺序

### 6.1 这轮 spec 的最终落点

这一轮不再扩新 skill，而是专注定义：

- 总入口与子入口的路由优先级
- 辅助 skill 的受控进入规则
- 典型直进 / 必须总入口 / 辅助进入的判定矩阵
- 各类禁止规则
- 这些规则分别落在哪类文档里

### 6.2 后续实现落点

如果这轮 spec 通过，建议后面实现时优先动：

1. `docs/ORCHESTRATION.md`
2. `skills/orchestration/SKILL.md`
3. 三个主场景 `SKILL.md`
4. 两个辅助 `SKILL.md`

### 6.3 实现顺序建议

建议顺序固定为：

1. 总规则
2. 总入口
3. 三个主场景
4. incident 辅助

### 6.4 这轮明确不做

- 不扩新 skill
- 不写 host-specific routing 逻辑
- 不写自动路由脚本
- 不写生成器
- 不写安装器

也就是：只写规则，不写自动化。

---

## 7. 最终结论

本轮 skill 路由执行规则的推荐方向是：

> 在正式 `SKILL.md` 文件已经落地之后，下一步优先定义 skill 之间的入口路由规则：明确总入口优先级、子入口直进边界、辅助 skill 受控进入条件，以及这些规则在总文档与 skill 文件中的分层落点。