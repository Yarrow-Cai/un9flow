# un9flow 功率板 bring-up 流程示例设计稿

日期：2026-04-24
主题：围绕一个“功率板首次上电后预充完成但 PWM 输出建立不稳定”的场景，定义 v6 第二份端到端 bring-up 示例的结构、边界与完成标准。

## 1. 设计结论摘要

本轮设计采用 **端到端主案例文档 + 内嵌关键 artifact 摘要** 的方向，而不是完整功率电子教材、硬件调试手册或多文件案例包。

设计结论如下：

- 新增一份主案例文档，放在 `docs/cases/` 下，作为 v6 第二份示例与实战载体。
- 案例选题固定为：**功率板首次上电后，预充完成但 PWM 输出建立不稳定，需先建立安全基线，再判断是否升级到更深层路径。**
- 案例主线固定围绕 `bringup-path`，并在必要处展示何时升级到 `incident-investigation` 或 `design-safety-review`。
- 文档中嵌入少量关键 artifact 摘要块，但不拆成大规模案例包。
- 本轮目标是证明 `bringup-path` 如何被实际使用，而不是覆盖全部功率电子控制理论。

一句话总结：

> 用一个“功率板首次上电后 PWM 输出建立不稳定”的场景，做一份可回放、可阅读、可展示的 bring-up 主案例文档，证明 `bringup-path` 在功率板场景中的实际用法。

---

## 2. 当前状态与缺口

仓库当前已经具备：

- `skills/bringup-path/SKILL.md`：首次拉通主场景入口。
- `docs/templates/daisy-chain-isospi-afe-bringup-template.md`：链路类 bring-up 模板。
- `docs/DESIGN_SAFETY_REVIEW.md`：design-time safety review 主场景真源。
- `docs/cases/bms-daisy-chain-afe-end-to-end-example.md`：v6 第一份端到端方法链示例。
- `docs/templates/watchdog-timeout-audit-findings.md`、`docs/templates/watchdog-timeout-audit-report.md`：专项 artifact 载体。

但当前仍存在 3 个明确缺口：

1. `v6` 虽已有一份端到端 BMS 示例，但还没有一份明显偏**功率板 bring-up** 的场景示例。
2. `bringup-path` 目前已有模板和主场景定义，但缺少一个“功率级控制建立”方向的展示案例。
3. 仓库对外仍缺一个说明“安全基线 → bring-up 动作 → 控制建立 → 升级判断”如何串起来的功率板样例。

因此，本轮设计的核心不是增加新的场景或模板，而是新增一份 bring-up 实战案例。

---

## 3. 设计目标

本轮只解决以下问题：

1. 选一个足够真实且范围可控的功率板 bring-up 场景。
2. 展示 `bringup-path` 如何处理“预充完成但 PWM 输出建立不稳定”这一类问题。
3. 用一份主案例文档串起安全基线、bring-up 动作、控制建立与升级判断。
4. 让 v6 第二份示例具备对外展示与内部复盘价值。

本轮不解决：

- 完整电机控制理论
- 完整 PWM 调制策略说明
- 全量示波器数据与实验数据包
- 功率板完整调试手册
- 多板型对比

---

## 4. 边界规则

本轮固定采用以下边界：

1. 这是 **bring-up 案例文档**，不是功率电子教材。
2. 重点展示 `bringup-path` 的使用方式，不展开完整控制理论。
3. 文中可嵌入关键 artifact 摘要，但不拆成大规模案例包。
4. 必须明确安全基线与升级边界，不能把问题写成“继续试试看就好”。
5. 不把案例写成完美解决故事，必须保留未闭合项与下一步建议。

---

## 5. 案例选题设计

建议固定案例题目为：

> **功率板首次上电后，预充完成但 PWM 输出建立不稳定。**

选择这个题目的原因是：

- 能自然展示功率板 bring-up 中“先钉安全边界，再尝试控制建立”的顺序。
- 能体现 `bringup-path` 对“建立 deterministic baseline”的价值。
- 能自然展示何时应该继续留在 bring-up，何时需要升级到 incident 或 design review。
- 范围足够小，不需要展开完整功率控制闭环理论。

---

## 6. 文档形态设计

建议新增：

- `docs/cases/power-board-bringup-example.md`

该文档的定位是：

- v6 第二份主案例文档
- 面向阅读与展示
- 用正文串起 bring-up 路径，并嵌入关键 artifact 摘要

### 为什么不拆成多文件

本轮不建议拆成多文件，原因是：

- 第二份示例依然更需要可读性，而不是案例包复杂度。
- 一份主案例更容易展示“安全基线、bring-up、控制建立、升级判断”之间的关系。
- 若先拆成多个文件，会削弱 `bringup-path` 的流程直观性。

---

## 7. 案例结构设计

建议主文档至少包含以下 6 段：

### 7.1 `case overview`
说明：
- 功率板背景
- 当前硬件阶段
- 初始现象
- 为什么这是典型 bring-up 问题

### 7.2 `safety baseline`
展示：
- 供电条件
- 预充条件
- 关键联锁
- 默认安全态
- 禁止动作

### 7.3 `bring-up path usage`
展示：
- 为什么当前仍属于 `bringup-path`
- 建立了什么 baseline
- 哪些步骤已打通
- 哪些步骤仍不稳定

### 7.4 `control establishment`
展示：
- 预充完成后如何逐步建立 PWM / 驱动输出
- 观察哪些信号
- 如何判断“控制未建立”还是“建立了但不稳定”

### 7.5 `escalation decision`
展示：
- 什么时候继续留在 bring-up
- 什么时候升级到 `incident-investigation`
- 什么时候升级到 `design-safety-review`

### 7.6 `final outcome`
收口：
- 当前确认了什么
- 哪些问题还没闭合
- 下一步建议是什么

---

## 8. artifact 呈现方式

本轮建议嵌入少量关键 artifact 摘要，而不是拆成完整案例包。

建议至少嵌入：

- `bringup-baseline` 摘要
- `link-qualification-log` 或等价基线日志摘要
- `initial-diagnosis-conclusion` 摘要
- 如有必要，可再嵌一个 `risk-boundary-note` 摘要

这些摘要的目标是帮助读者理解：
- 每一步看了什么
- 每一步得出了什么
- 为什么下一步继续留在 bring-up 或升级

---

## 9. 完成标准

这份 v6 第二份示例建议满足以下 4 条：

1. **能完整读通**
   - 不跳很多文件也能理解 bring-up 主线。

2. **能看出安全基线作用**
   - 读者能理解为什么先做安全边界约束，再做控制建立。

3. **能看出升级判断**
   - 读者能理解什么时候还留在 bring-up，什么时候必须升级。

4. **能看出结论边界**
   - 明确什么已确认、什么未确认、下一步怎么做。

---

## 10. 范围控制

### 本轮做

- 一份主案例文档
- 少量关键 artifact 摘要块
- bring-up 过程与升级判断说明

### 本轮不做

- 不展开完整控制理论
- 不做真实示波器数据全集
- 不写完整硬件调试手册
- 不拆成十几个独立样例文件
- 不扩成培训教材

---

## 11. 文件落点建议

### 新增

- `docs/cases/power-board-bringup-example.md`
- `docs/superpowers/specs/2026-04-24-un9flow-power-board-bringup-example-design.md`

### 修改

- `docs/ROADMAP.md`
- `README.md`（如需入口）

---

## 12. 实现顺序建议

建议固定为：

1. 先写主案例文档
2. 再补最小入口与路线图同步
3. 最后确认文档自洽与对外可读性

原因是：
- 先把案例本体写清楚
- 再决定如何暴露入口
- 最后让路线图跟上

---

## 13. 最终结论

本轮推荐方向固定为：

> 用“功率板首次上电后预充完成但 PWM 输出建立不稳定”这个场景，新增一份 `bringup-path` 端到端主案例文档，重点展示安全基线、首次拉通、控制建立与升级判断，作为 v6 第二份示例。