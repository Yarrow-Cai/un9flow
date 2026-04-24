# un9flow 模板生成体系设计稿

日期：2026-04-24
主题：围绕现有 report、case、bundle 等对象，定义“共享生成约定 + 薄包装脚本”的模板生成体系，以及与 consistency / 回归校验的最小挂接方式。

## 1. 设计结论摘要

本轮设计采用 **共享生成约定 + 薄包装脚本** 的方向，而不是先做单一大一统生成平台，也不是继续让每个生成器完全各自演化。

设计结论如下：

- 新增一份模板生成约定真源文档：`docs/TEMPLATE_GENERATION.md`。
- 新增一个小型共享生成内核：`tools/generation_core.py`。
- 保留“每类对象一个入口脚本”的外形，但让生成逻辑逐步共用。
- 首批只纳入 3 类对象：
  - watchdog report
  - incident case bundle
  - v6 示例骨架
- consistency CLI 与现有 GitHub workflow 继续沿用最小门禁模式；本轮只增加“生成体系对象存在性与映射关系”的检查，不在 CI 中直接执行所有生成器。

一句话总结：

> 先把现有零散生成器收束成“共享约定 + 薄包装脚本”的最小体系，让对象关系和输入输出规则稳定下来，再在下一轮扩展更完整的输出回归校验。

---

## 2. 当前状态与缺口

仓库当前已经具备：

- `tools/generate_incident_case_bundle.py`：incident workflow 主线文档 bundle 生成脚本。
- `tools/generate_watchdog_timeout_audit_report.py`：watchdog report 生成脚本。
- 多类模板对象：
  - report
  - findings
  - specialist pack
  - bring-up 模板
  - v6 案例文档
- `docs/CONSISTENCY_VALIDATION.md` 与 `tools/validate_consistency.py`：对象存在性与映射关系的统一校验基线。

但当前仍存在 4 个明确缺口：

1. 生成器之间还没有统一的“输入/输出/模板/命名”约定文档。
2. 生成逻辑仍是各脚本分散实现，公共能力尚未抽出。
3. 现有 consistency / CI 还不能明确检查“生成体系对象”本身。
4. v6 示例骨架尚未进入生成体系。

因此，本轮设计的核心不是“让所有内容都自动生成”，而是先把生成体系本身对象化、规则化。

---

## 3. 设计目标

本轮只解决以下问题：

1. 模板生成体系的最小对象集合应该是什么。
2. 共享生成约定文档应该写什么。
3. 共享生成内核应该负责什么，哪些能力仍留给薄包装脚本。
4. 首批接入对象是哪 3 类。
5. consistency / CI 如何以最小成本纳管这些对象。

本轮不解决：

- 单一大一统内容平台
- 所有模板对象一次性接入生成体系
- 在 CI 中批量执行全部生成器
- 输出 golden files / snapshot 回归
- 自动修复或自动覆盖已有文档

---

## 4. 边界规则

本轮固定采用以下边界：

1. 生成体系不是“大一统文档平台”。
2. 保留“每类对象一个入口脚本”的外形。
3. 共性只下沉到最小内核，不做过度抽象。
4. 首批只接 3 类对象，不追求全仓一次性接入。
5. 本轮不在 CI 中直接跑所有生成器，只纳管生成体系对象与关系。

---

## 5. 对象形态设计

### 5.1 生成约定真源文档

建议新增：

- `docs/TEMPLATE_GENERATION.md`

它负责定义：

- 哪些对象允许被生成
- 输入最小集合
- 输出文件命名规则
- 生成器的输入/输出责任
- 缺字段时的处理原则
- 哪些对象是单文件输出，哪些对象是 bundle 输出

一句话：

- `TEMPLATE_GENERATION.md` 负责回答“生成体系怎么约定”。

### 5.2 共享生成内核

建议新增：

- `tools/generation_core.py`

它只负责共性动作：

- 读取模板
- 读取输入
- 渲染占位
- 写出输出
- 做最小字段检查

它不负责：

- 决定每类对象的业务规则
- 决定每类对象的默认路径与语义
- 取代对象级入口脚本

一句话：

- `generation_core.py` 负责回答“生成时公共能力是什么”。

### 5.3 薄包装脚本

继续保留对象级入口脚本，例如：

- `tools/generate_watchdog_timeout_audit_report.py`
- `tools/generate_incident_case_bundle.py`
- 后续新增：`tools/generate_example_case.py`

这些脚本负责：

- 声明自己服务哪个对象
- 组装输入
- 调用共享生成内核

一句话：

- 外面分脚本，里面共内核。

---

## 6. 首批接入对象

本轮建议只接以下 3 类对象：

### 6.1 watchdog report
原因：
- 已有 report 模板
- 已有 findings / pack 输入
- 已有生成脚本
- 最适合先验证“共享生成约定”是否可行

### 6.2 incident case bundle
原因：
- 已有 `generate_incident_case_bundle.py`
- 代表 bundle 类型输出
- 能验证“单文件输出”和“bundle 输出”两种类型的差异

### 6.3 v6 示例骨架
原因：
- 当前 v6 已开始积累多个示例
- 先支持示例骨架生成，比直接接所有案例更稳
- 也最能体现生成体系对未来新案例的维护价值

---

## 7. consistency / CI 最小挂接

### 7.1 consistency

本轮建议新增以下检查：

1. `docs/TEMPLATE_GENERATION.md` 必须存在并可读。
2. `tools/generation_core.py` 必须存在并可读。
3. 各生成脚本必须回指：
   - 自己服务的模板/对象
   - `docs/TEMPLATE_GENERATION.md`
   - `tools/generation_core.py`
4. 首批接入对象必须能看出：
   - 输入是什么
   - 输出是什么
   - 脚本和模板之间如何对应

### 7.2 CI

本轮继续保持：
- PR / main 只跑 `python tools/validate_consistency.py`
- 不在 CI 中批量执行全部生成器

这意味着本轮 CI 的目标是：

> 先把“生成体系对象关系”钉稳，而不是先跑批量生成。

### 7.3 下一轮再做的内容

更完整回归校验留到下一轮：
- 生成结果快照比对
- golden files
- 输出结构回归
- 示例骨架生成回归

---

## 8. 文件落点建议

### 新增

- `docs/TEMPLATE_GENERATION.md`
- `tools/generation_core.py`
- `docs/superpowers/specs/2026-04-24-un9flow-template-generation-design.md`

### 修改

- `tools/generate_incident_case_bundle.py`
- `tools/generate_watchdog_timeout_audit_report.py`
- `docs/CONSISTENCY_VALIDATION.md`
- `tools/validate_consistency.py`
- `docs/ROADMAP.md`

### 后续再考虑新增

- `tools/generate_example_case.py`

---

## 9. 实现顺序建议

建议固定为：

1. 先写 `TEMPLATE_GENERATION.md`
2. 再写 `generation_core.py`
3. 再让 watchdog report / incident case bundle 接入共享内核
4. 最后同步 consistency / 路线图

原因是：
- 先把约定写清楚
- 再实现公共能力
- 再迁移现有脚本
- 最后让校验和路线图跟上

---

## 10. 最终结论

本轮推荐方向固定为：

> 先把现有零散生成器收束成“共享约定 + 薄包装脚本”的最小生成体系，首批接入 watchdog report、incident case bundle 与 v6 示例骨架，并通过 consistency / 现有 CI 只纳管体系对象与关系，为下一轮更完整回归校验打底。