# un9flow Keil Scatter / Linker Script 审核模板设计稿

日期：2026-04-23
主题：围绕 `design-safety-review` 主场景，定义 Keil Scatter / Linker Script 静态内存布局审查模板的结构、边界与升级关系。

## 1. 设计结论摘要

本轮设计采用 **挂在 `design-safety-review` 下的专项模板** 方向，而不是先做独立主场景、通用链接脚本教程或自动分析器。

设计结论如下：

- 新增一个 Keil Scatter / Linker Script 审核模板，默认服务 `design-safety-review`。
- 该模板面向**静态内存布局审查**：固定 memory region、section 落点、deterministic 约束、证据输入与升级规则。
- 模板重点固定：
  - review scope
  - memory region map
  - section placement review
  - deterministic invariants
  - evidence inputs
  - common risk signatures
  - review outcome / escalation
- 本轮不绑定具体 MCU 厂商专有语法，不做 map file 自动解析器，也不做自动修复建议引擎。

一句话总结：

> 先把 Keil Scatter / Linker Script 做成一个挂在 `design-safety-review` 下的静态内存布局审查模板，用来固定内存域、section 落点、静态约束、证据输入和升级规则，而不是先做自动分析器或新的场景/角色。

---

## 2. 当前状态与缺口

仓库当前已经具备：

- `docs/DESIGN_SAFETY_REVIEW.md`：design-time safety review 主场景真源。
- `docs/DOMAIN_SPECIALIST_CONTRACTS.md`：specialist 契约真源。
- `docs/REGISTER_STATE_AUDIT.md`：寄存器审计方法真源。
- `docs/templates/*-pack.md`：多类 specialist 输出模板。
- `docs/CONSISTENCY_VALIDATION.md` 与 `tools/validate_consistency.py`：已覆盖当前 docs / skills / templates / cases / 过程文档的一致性基线。

但当前仍存在 3 个明确缺口：

1. `design-safety-review` 虽已存在，但还缺少一个**面向静态内存布局的专项模板**。
2. 当前仓库对 scatter / linker script 的讨论仍停留在高层理念，没有一个模板级交付物来固定“该看什么、怎么判风险、何时升级”。
3. 路线图中的“Keil Scatter / Linker Script 审核模板”尚未落地。

因此，本轮设计的核心不是新建新的场景，而是为 `design-safety-review` 增加一个静态资源布局审查模板。

---

## 3. 设计目标

本轮只解决以下问题：

1. Keil Scatter / Linker Script 审核模板应该放在哪里。
2. 模板要固定哪些内存域、section、静态约束与证据输入。
3. 模板与 `design-safety-review`、`register-state-auditor`、`bringup-path`、`incident-investigation` 如何分工。
4. 路线图和必要入口文档如何同步。

本轮不解决：

- 具体厂商 linker 语法大全
- map file 自动解析器
- 自动 linker 规则修复器
- 新的主场景设计
- 新的 `Domain Specialist` 设计

---

## 4. 边界规则

本轮固定采用以下边界：

1. 该模板默认挂在 `design-safety-review` 下，不是新的主场景。
2. 该模板不是新的 `Domain Specialist`。
3. 该模板审查**静态布局态**，不替代运行态寄存器审计。
4. 该模板不直接替代 `bringup-path` 或 `incident-investigation`。
5. 该模板不绑定某个具体 MCU 厂商的完整语法手册。

---

## 5. 模板对象设计

### 5.1 定位

建议新增：

- `docs/templates/keil-scatter-linker-review-template.md`

这个对象的定位是：

- `design-safety-review` 下的专项模板
- 用于审查静态内存布局是否满足 deterministic 工程约束
- 用于记录 memory region、section 落点、保留区 / noinit / bootloader / DMA 区边界与静态风险

### 5.2 为什么挂在 `design-safety-review`

原因是：

- Scatter / linker script 审查本质上是**设计边界问题**，不是首次拉通步骤问题。
- 它关心的是：section 是否落在正确内存域、保留区是否被侵占、启动区与 app 边界是否清楚、stack/heap 是否可解释。
- 这类问题更接近 `design-safety-review` 的“风险边界 / 资源布局 / failsafe 前提”审查语义，而不是 `bringup-path` 的“先建立基线”语义。

---

## 6. 模板结构设计

建议模板至少包含以下 7 段：

### 6.1 `review scope`
记录：
- 项目 / 模块
- MCU / SoC
- 工具链
- 审核目标
- 当前使用的 scatter / linker 文件

### 6.2 `memory region map`
记录内存域与用途：
- Flash
- SRAM
- CCM / TCM / ITCM / DTCM
- backup / noinit / retention
- bootloader / app 分区
- 外设 / DMA 专用区

### 6.3 `section placement review`
记录关键 section 的落点：
- vector table
- startup / init
- code / rodata
- data / bss
- stack / heap
- noinit / backup
- DMA buffer / special section

### 6.4 `deterministic invariants`
记录必须满足的静态约束：
- 不重叠
- 对齐正确
- 关键区不漂移
- 保留区不被侵占
- bootloader / app 边界不冲突
- stack / heap 不形成不可解释风险

### 6.5 `evidence inputs`
记录审核依赖的输入：
- scatter / linker script
- map file
- startup file
- memory usage 输出
- 关键编译配置

### 6.6 `common risk signatures`
记录常见风险：
- section 放错内存域
- noinit / backup 区被初始化破坏
- bootloader / app 边界冲突
- vector table 位置异常
- stack / heap 规划不清
- DMA buffer 放在错误 region
- map file 与脚本意图不一致

### 6.7 `review outcome / escalation`
明确什么时候：
- 通过当前 review
- 留在 `design-safety-review` 继续补证据
- 升级到 `incident-investigation`
- 回到更具体的 specialist 深挖

---

## 7. 与现有对象的分工关系

### 7.1 与 `design-safety-review` 的关系

- 该模板是 `design-safety-review` 下的专项模板。
- 用来回答“静态内存布局是否破坏 deterministic 资源模型”。
- 不替代 `design-safety-review` 的主收口物，只作为其下的专题审查载体。

### 7.2 与 `register-state-auditor` 的关系

- `register-state-auditor` 关注**运行态 / 配置态**：寄存器快照、位域、默认值 / 目标值 / 当前值 / 复位后值。
- `keil-scatter-linker-review-template` 关注**静态布局态**：section、region、noinit、bootloader/app 边界、stack/heap、DMA 区。
- 一个审运行态配置，一个审静态布局边界，两者不互相替代。

### 7.3 与 `bringup-path` 的关系

- `bringup-path` 负责发现首次拉通中的异常征象。
- 若 bring-up 过程中发现 vector table、noinit、DMA region、bootloader/app 边界等静态布局问题，应升级到该模板所在的设计审查路径，而不是反复停留在 bring-up 动作内试错。

### 7.4 与 `incident-investigation` 的关系

- `incident-investigation` 可在运行期异常已明显指向 linker / scatter 布局时引用该模板。
- 但该模板不接管 incident 主流程。

---

## 8. consistency / 路线图最小同步

### 8.1 consistency

本轮不要求为该模板增加复杂脚本或新 workflow，但建议最小同步：

- `docs/CONSISTENCY_VALIDATION.md` 暂不新增专门结构检查，只要模板在 docs / templates 体系中被入口文档引用即可。
- 若后续同类模板增多，再考虑为静态布局审查模板增加单独规则。

### 8.2 路线图

`docs/ROADMAP.md` 应把：

- `[ ] Keil Scatter / Linker Script 审核模板`

推进为已落地基线条目，并明确其作为 `design-safety-review` 下模板的定位。

### 8.3 视需要同步 README

若模板需要对外可发现对象，`README.md` 可补最小入口：

- `docs/templates/keil-scatter-linker-review-template.md`

---

## 9. 文件落点建议

### 新增

- `docs/templates/keil-scatter-linker-review-template.md`
- `docs/superpowers/specs/2026-04-23-un9flow-keil-scatter-linker-review-design.md`

### 修改

- `docs/ROADMAP.md`
- `README.md`（如需入口）
- `docs/DESIGN_SAFETY_REVIEW.md`（如需最小挂接说明）

---

## 10. 实现顺序建议

建议固定为：

1. 先新增审查模板
2. 再在 `design-safety-review` 或 README 中补最小入口/挂接说明
3. 最后同步 `ROADMAP.md`

原因是：
- 先把模板对象定义清楚
- 再决定如何暴露入口
- 最后让路线图跟上实际状态

---

## 11. 最终结论

本轮推荐方向固定为：

> 把 Keil Scatter / Linker Script 审核先落成一个挂在 `design-safety-review` 下的静态内存布局审查模板，重点固定内存域、section 落点、静态约束、证据输入和升级规则，而不是先做自动分析器、通用教程或新的场景/角色。