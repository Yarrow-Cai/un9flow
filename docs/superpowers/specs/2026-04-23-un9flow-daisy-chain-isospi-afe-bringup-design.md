# un9flow 菊花链 / isoSPI / AFE bring-up 模板设计稿

日期：2026-04-23
主题：围绕 `bringup-path` 主场景，定义菊花链 / isoSPI / AFE 首次拉通模板的结构、边界与收口方式。

## 1. 设计结论摘要

本轮设计采用 **挂在 `bringup-path` 下的专项模板** 方向，而不是先做独立主场景或通用硬件 bring-up 手册。

设计结论如下：

- 新增一个菊花链 / isoSPI / AFE bring-up 模板，默认服务 `bringup-path`。
- 该模板面向“首次拉通、建立 deterministic baseline、记录可重复 bring-up 步骤与观测点”，不直接承担深层根因分析。
- 模板重点固定：
  - bring-up 范围
  - 前置条件
  - 建链步骤
  - 观测点
  - 基线判据
  - 常见失败特征
  - 升级规则
- 本轮不绑定具体 AFE 型号寄存器表，不做自动 bring-up 脚本，也不引入新的主场景或 `Domain Specialist`。

一句话总结：

> 先把菊花链 / isoSPI / AFE 首次拉通做成一个 `bringup-path` 下的可执行、可重复、可回归、可审查模板，而不是先做成通用知识手册或自动化脚本。

---

## 2. 当前状态与缺口

仓库当前已经具备：

- `skills/bringup-path/SKILL.md`：bring-up 主场景入口。
- `docs/ORCHESTRATION.md`、`docs/ORCHESTRATOR_PROMPT_CONTRACT.md`：总路由与输入输出协议基线。
- `docs/DOMAIN_SPECIALIST_CONTRACTS.md`：specialist 契约真源。
- `docs/templates/*-pack.md`：多类 specialist pack 模板。
- `docs/CONSISTENCY_VALIDATION.md` 与 `tools/validate_consistency.py`：已覆盖主场景 / specialist / 模板 / 路由案例的一致性基线。

但当前仍存在 3 个明确缺口：

1. `bringup-path` 虽然已作为主场景存在，但还缺少一个**面向菊花链 / isoSPI / AFE 首次拉通的专项模板**。
2. 当前仓库对 bring-up 的描述仍停留在场景边界与高层方法，不足以支持具体 bring-up 过程的重复执行与对照复盘。
3. 路线图中的“菊花链 / isoSPI / AFE bring-up 模板”尚未落地，对真实硬件 bring-up 仍缺一个模板级交付物。

因此，本轮设计的核心不是新建新的场景，而是给 `bringup-path` 增加一个硬件 bring-up 专项模板。

---

## 3. 设计目标

本轮只解决以下问题：

1. 菊花链 / isoSPI / AFE bring-up 模板应该放在哪里。
2. 模板要固定哪些步骤、观测点、基线判据与升级规则。
3. 模板与 `bringup-path` 主场景如何挂接。
4. 路线图和必要入口文档如何同步。

本轮不解决：

- 具体 AFE 型号的完整寄存器地图
- 自动 bring-up 脚本
- 自动实验报告体系
- 新的主场景设计
- 新的 `Domain Specialist` 设计

---

## 4. 边界规则

本轮固定采用以下边界：

1. 该模板默认挂在 `bringup-path` 下，不是新的主场景。
2. 该模板不是新的 `Domain Specialist`。
3. 该模板面向“首次拉通与建立基线”，不是深度根因分析模板。
4. 该模板不绑定具体 AFE 型号寄存器细节。
5. 该模板不直接替代 `incident-investigation` 或 `design-safety-review`。

---

## 5. 模板对象设计

### 5.1 定位

建议新增：

- `docs/templates/daisy-chain-isospi-afe-bringup-template.md`

这个对象的定位是：

- `bringup-path` 下的专项 bring-up 模板
- 用于首次拉通菊花链 / isoSPI / AFE 链路
- 用于记录 bring-up 的固定步骤、观测点、判据与升级规则

### 5.2 为什么挂在 `bringup-path`

原因是：

- `bringup-path` 当前就用于“新板 / 新链路 / 新模块的首次拉通与重复建立过程”。
- 菊花链 / isoSPI / AFE 首次拉通的本质，是“建立 deterministic baseline”，而不是解释既有系统退化异常。
- 若把它做成独立模板而不挂场景，会让读者难以判断何时该走 `bringup-path`、何时该走 `incident-investigation`。

---

## 6. 模板结构设计

建议模板至少包含以下 7 段：

### 6.1 `bring-up scope`
记录：
- 板卡 / 模块名称
- AFE 型号
- 菊花链拓扑
- 当前硬件版本
- 当前 bring-up 目标

### 6.2 `prerequisites`
记录进入 bring-up 前必须确认的前提：
- 供电条件
- 复位条件
- 时钟 / 唤醒条件
- 关键引脚状态
- 安全限制

### 6.3 `chain establishment steps`
记录首次拉通步骤：
- 上电
- 唤醒
- 基本通信探测
- 链路寻址 / 枚举
- AFE 基本寄存器读回
- 首次健康检查

这一段必须偏步骤化，而不是解释性 prose。

### 6.4 `observability points`
记录每一步要观测的对象：
- 哪些寄存器
- 哪些状态位
- 哪些波形 / 引脚
- 哪些错误码 / timeout 现象

### 6.5 `baseline qualification`
记录什么算“拉通成功”：
- 最小可重复读写条件
- 链路稳定条件
- AFE 状态一致性条件
- 可进入下一阶段的判据

### 6.6 `common failure signatures`
记录常见失败特征：
- 完全无响应
- 链路偶发掉线
- 节点数不对
- 唤醒后状态异常
- 读回值不稳定
- timeout / CRC / framing 异常

### 6.7 `escalation rules`
明确什么时候：
- 继续停留在 `bringup-path`
- 升级到 `incident-investigation`
- 升级到 `design-safety-review`

---

## 7. 与现有场景 / specialist 的关系

### 与 `bringup-path` 的关系

- 该模板服务 `bringup-path`，用于把首次拉通动作从高层场景描述推进到可执行模板。
- 它应被视为 `bringup-path` 的专项模板，而不是新的对外 skill 入口。

### 与 `Domain Specialist` 的关系

- 该模板不替代 `register-state-auditor`、`signal-path-tracer`、`timing-watchdog-auditor` 等 specialist。
- 当 bring-up 进入具体证据域分析时，仍由现有 specialist 契约接手。

### 与 `incident-investigation` 的关系

- 若问题属于“既有系统退化异常”，不应继续停留在 bring-up 模板内。
- 模板应明确“升级到 incident”的规则，避免把退化异常误当首次拉通问题反复尝试。

### 与 `design-safety-review` 的关系

- 若问题暴露为架构性设计边界、failsafe 策略、默认安全态缺口，则应升级到 `design-safety-review`。

---

## 8. consistency / 路线图最小同步

### 8.1 consistency

本轮不要求为 bring-up 模板增加复杂脚本或新 workflow，但建议最小同步：

- `docs/CONSISTENCY_VALIDATION.md` 可以先不新增专门校验规则，只要模板在 docs / templates 体系中被入口文档引用即可。
- 若后续模板逐步增多，再考虑为 bring-up 专项模板加单独的结构检查。

### 8.2 路线图

`docs/ROADMAP.md` 应把：

- `[ ] 菊花链 / isoSPI / AFE bring-up 模板`

推进为已落地基线条目，并明确其作为 `bringup-path` 下模板的定位。

### 8.3 视需要同步 README

若模板成为对外可发现对象，`README.md` 可补最小入口：

- `docs/templates/daisy-chain-isospi-afe-bringup-template.md`

---

## 9. 文件落点建议

### 新增

- `docs/templates/daisy-chain-isospi-afe-bringup-template.md`
- `docs/superpowers/specs/2026-04-23-un9flow-daisy-chain-isospi-afe-bringup-design.md`

### 修改

- `docs/ROADMAP.md`
- `README.md`（如需入口）
- `skills/bringup-path/SKILL.md`（如需最小挂接说明）

---

## 10. 实现顺序建议

建议固定为：

1. 先新增 bring-up 模板
2. 再在 `bringup-path` 或 README 中补最小入口/挂接说明
3. 最后同步 `ROADMAP.md`

原因是：
- 先把模板对象定义清楚
- 再决定如何暴露入口
- 最后让路线图跟上实际状态

---

## 11. 最终结论

本轮推荐方向固定为：

> 把“菊花链 / isoSPI / AFE bring-up”先落成一个挂在 `bringup-path` 下的专项模板，重点固定步骤、观测点、基线判据与升级规则，而不是先做通用手册、自动脚本或新的场景/角色。