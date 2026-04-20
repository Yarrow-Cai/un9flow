# un9flow 自动校验脚本设计稿

日期：2026-04-17
主题：围绕 docs / skills / templates / routing cases / 过程文档，设计第一代本地可运行的一致性校验 CLI

## 1. 设计结论摘要

本轮设计采用如下方向：

- 第一代自动校验器采用 **Python 单入口 CLI**
- 覆盖范围第一版直接走 **全量**：
  - docs 真源层
  - 正式 skills 层
  - 模板层
  - routing cases
  - 过程文档层
- 内部按五层对象拆成分层检查器，但对外只有一个 CLI 入口
- 输出以 **人类 review 友好** 为主，先按 L1 / L2 / L3 展示 findings，再给总结果
- 退出码采用三档：
  - `0`：无 L1 / L2
  - `1`：存在 L1
  - `2`：无 L1，但存在 L2
- 第一轮不接 CI，不做自动修复，不做 host-specific 检查器

一句话总结：

> 先实现一个本地可运行的 Python 一致性校验 CLI：单入口、分层检查器、统一 findings、清晰退出码；第一版直接覆盖 docs / skills / templates / routing cases / 过程文档，但暂不接 CI。

---

## 2. Python 校验 CLI 的整体结构

建议第一版校验器采用：

> 一个入口 CLI + 一组分层检查器 + 一个统一 findings 模型。

### 2.1 CLI 入口层

CLI 入口只负责：

1. 收集检查目标路径
2. 调度各检查器
3. 汇总 findings
4. 输出终端结果
5. 设置退出码

### 2.2 检查器层

内部按五层对象拆成五类检查器：

- `check_docs`
- `check_skills`
- `check_templates`
- `check_routing_cases`
- `check_process_docs`

每个检查器只负责一层，不跨层乱判。

### 2.3 findings 输出层

各检查器不直接打印结果，而统一返回 findings 结构，由 CLI 汇总输出。

### 2.4 目录落点建议

第一版先落：

- `tools/validate_consistency.py`

后续如果复杂，再拆成：

- `tools/validation/cli.py`
- `tools/validation/check_docs.py`
- `tools/validation/check_skills.py`
- ...

但第一版先不拆模块。

---

## 3. 五个检查器各自应该检查什么

### 3.1 `check_docs`

检查 docs 真源层：

1. 职责边界
2. 术语一致性
3. 真源冲突

### 3.2 `check_skills`

检查正式 skill 层：

1. 入口层级是否正确
2. 结构是否对齐
3. 规则是否越权

### 3.3 `check_templates`

检查模板层：

1. 字段完整性
2. 枚举一致性
3. 模板角色正确性

### 3.4 `check_routing_cases`

检查 routing matrix / 案例层：

1. case 字段完整性
2. route decision 合法性
3. route type 合法性
4. 与当前真源规则一致

### 3.5 `check_process_docs`

检查过程文档层：

1. 旧控制信号
2. 旧层级关系
3. 旧模板示例

---

## 4. 统一 findings 数据结构

建议第一版 findings 至少固定为：

- `level`
- `category`
- `file`
- `summary`
- `why_it_matters`
- `suggested_action`

### 4.1 字段说明

#### `level`
- `L1`
- `L2`
- `L3`

#### `category`
- `docs`
- `skills`
- `templates`
- `routing_cases`
- `process_docs`

#### `file`
问题对应文件路径。

#### `summary`
一句话问题概述。

#### `why_it_matters`
说明问题为什么不能忽略。

#### `suggested_action`
给出最小可执行修复动作。

### 4.2 可选预留字段

建议结构上预留：

- `source_of_truth`
- `conflicts_with`

但第一版不强制打印。

### 4.3 与 `validation-findings.md` 的关系

两者可映射：

- `level` ↔ `level`
- `file` ↔ `file`
- `summary` ↔ `issue`
- `why_it_matters` ↔ `impact`
- `suggested_action` ↔ `required action`

---

## 5. CLI 的输出流程与退出码策略

### 5.1 输出流程

建议固定成 5 段：

1. 运行范围
2. L1 findings
3. L2 findings
4. L3 findings
5. 整体结论

### 5.2 范围输出

例如：

```text
Validation scope:
- docs
- skills
- templates
- routing_cases
- process_docs
```

### 5.3 findings 展示顺序

严格按等级：

1. L1
2. L2
3. L3

### 5.4 无问题时的输出

建议显式打印：

- `No blocking issues found`
- `No important issues found`
- `No cleanup issues found`

### 5.5 整体结论

建议输出：

- `Validation result: PASS`
- `Validation result: FAIL`

并附每级数量。

### 5.6 退出码策略

建议第一版只用三种退出码：

- `0`：没有 L1 / L2
- `1`：存在 L1
- `2`：无 L1，但存在 L2

L3 不影响退出码。

---

## 6. 这轮 spec 的最终落点与实现顺序

### 6.1 最终落点

这轮不是做完整平台工具链，而是先做：

- 一个 Python 单入口 CLI
- 五个分层检查器
- 一套统一 findings 结构
- 一套清晰输出流程与退出码规则

### 6.2 后续实现落点

建议优先落：

- `tools/validate_consistency.py`

第一版先单文件；后续再视复杂度拆分。

### 6.3 第一版明确不做

- CI 集成
- GitHub Action
- JSON 输出优先
- 规则 DSL
- 自动修复
- host-specific 检查器

### 6.4 实现顺序建议

建议固定为：

1. 统一 findings 结构
2. CLI 主流程
3. docs / skills / templates 三个检查器
4. routing cases 检查器
5. process docs 检查器

---

## 7. 最终结论

本轮自动校验脚本设计的推荐方向是：

> 先做一个本地可运行、后续可接 CI 的 Python 一致性校验 CLI：单入口、分层检查器、统一 findings、清晰退出码；第一版直接覆盖 docs / skills / templates / routing cases / 过程文档。