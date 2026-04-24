# generation regression design

## 背景

当前仓库已建立模板生成体系基线：

- `docs/TEMPLATE_GENERATION.md` 作为生成约定真源
- `tools/generation_core.py` 作为共享最小内核
- 首批已接入对象仅包括：
  - `watchdog-timeout-audit-report`
  - `incident case bundle`

`docs/ROADMAP.md` 的 v4 仍保留一项未完成内容：更完整的输出回归校验（golden files / snapshot / output regression）。本设计用于以最小闭环方式补齐这一缺口，并继续沿用现有“docs 真源 + tools 脚本 + consistency / CI 门禁”的结构，不额外引入独立框架层。

## 目标

建立一条最小但严格的 generation regression 链路，用于固定“给定输入 → 生成输出”的稳定性。

本轮目标：

- 采用 golden files first 方案
- 仅覆盖当前允许被生成的两个对象
- 提供统一 regression runner
- 支持本地显式更新 golden
- 在 CI 中仅做严格校验，不允许更新 golden

## 非目标

本轮明确不做以下事项：

- 不引入 snapshot 测试框架
- 不引入模糊匹配、宽松容错或 hash-only 校验
- 不自动发现并纳管新生成对象
- 不扩展到 `v6 example skeleton`
- 不对所有 docs 模板建立全覆盖生成回归
- 不自动批准或自动刷新 golden 变更

## 方案概览

采用 `golden files first + local update + CI check-only`：

- 本地开发时，允许通过显式 `--update-golden` 刷新 golden 输出
- 默认行为为严格校验，等价于 check-only
- CI 永远只做校验，不允许刷新 golden
- golden 的覆盖范围由 `docs/TEMPLATE_GENERATION.md` 已声明对象决定，而不是由脚本自动扩张

这样可以把“预期输出”固定为仓库契约，同时避免把 golden 当成掩盖漂移的工具。

## 覆盖范围

首批 generation regression 只覆盖以下两个对象：

1. `watchdog-timeout-audit-report`
2. `incident case bundle`

这与 `docs/TEMPLATE_GENERATION.md` 当前声明的允许生成对象保持一致。

`v6 example skeleton` 继续视为后续预留对象，不纳入本轮 regression。

## 目录布局

建议新增并固定以下目录布局：

- `docs/golden-inputs/`
  - 存放回归样例输入
- `docs/golden-outputs/`
  - 存放期望生成结果（golden outputs）
- `tools/run_generation_regression.py`
  - 统一 generation regression 入口脚本

目录布局按对象名分层，并先只建立 `minimal` 样例，避免一开始样例矩阵失控。

### 建议样例路径

输入样例：

- `docs/golden-inputs/watchdog-timeout-audit-report/minimal/`
- `docs/golden-inputs/incident-case-bundle/minimal/`

期望输出：

- `docs/golden-outputs/watchdog-timeout-audit-report/minimal/watchdog-timeout-audit-report.md`
- `docs/golden-outputs/incident-case-bundle/minimal/`
  - `README.md`
  - `01-skill-routing-matrix.md`
  - `02-orchestrator-dispatch-plan.md`
  - `03-incident-summary.md`
  - `04-evidence-package.md`
  - `05-incident-diagnosis-pack.md`
  - `06-incident-review-memo.md`

## 回归执行模型

统一由 `tools/run_generation_regression.py` 调度各对象回归。

脚本职责：

- 根据已声明对象找到对应输入样例
- 调用现有生成器生成临时输出
- 将生成结果与 golden outputs 严格比对
- 在显式请求时刷新 golden
- 输出可定位的失败信息

脚本不负责：

- 自动扩张对象集合
- 重新定义生成真源
- 引入新的对象发现机制

## CLI 设计

`tools/run_generation_regression.py` 的最小 CLI 语义建议如下：

- 默认：运行全部已纳管对象的 generation regression
- `--object <name>`：只运行某一个对象
- `--case <name>`：只运行某一组样例（如 `minimal`）
- `--update-golden`：显式刷新对应 golden outputs
- `--check`：显式只校验、不更新

默认行为等价于 `--check`，以避免误刷新 golden。

## Golden 更新策略

`--update-golden` 仅允许在“已声明对象 + 已声明样例”范围内，用最新生成结果覆盖现有 golden outputs。

边界约束：

- 不能通过更新命令隐式创建新对象纳管范围
- 不能自动发现新的生成对象
- 不能把范围之外的生成结果写入 golden 体系

因此：

- golden 的覆盖范围由 docs 真源决定
- golden 的内容由显式命令刷新
- CI 不具备 golden 刷新能力

## 比对规则

### 单文件对象

对 `watchdog-timeout-audit-report`：

- 重新生成目标 markdown 文件
- 与对应 golden markdown 做全文严格一致比对

### Bundle 对象

对 `incident case bundle`：

- bundle 根目录结构必须稳定
- 文件集合必须严格一致
- 文件命名必须严格一致
- 文件顺序必须按脚本约定稳定
- 每个文件内容必须全文严格一致

也就是说，bundle 需要同时比较：

1. 目录结构
2. 文件列表
3. 文件内容

不能只比较其中任意一层。

## 失败输出要求

回归失败时，runner 必须输出足够可定位的信息。

至少包括：

- 哪个对象失败
- 哪组样例失败
- 失败类型是：缺文件 / 多文件 / 内容不一致
- 对内容不一致给出可定位 diff

这样失败信息可直接服务于修复，而不是只提供模糊的 pass / fail。

## CI 接入方式

CI 不新增独立框架层，只在现有 consistency / validation 门禁旁补入一条最小命令：

- 运行 generation regression check
- 仅允许校验
- 任一对象任一样例不一致即失败

职责分层为：

- `consistency validation`：检查命名、引用、一致性、入口矩阵等规则
- `generation regression`：检查给定输入下的生成输出是否发生漂移

两条线并列，但都继续服务于 docs 真源。

## 维护规则

维护责任固定如下：

- 若修改模板或生成器，并且输出变化是预期变化：本地显式更新 golden，再提交
- 若修改代码但不应改变输出：generation regression 必须保持通过，不能用更新 golden 掩盖问题
- 若 CI 发现漂移：优先判断是模板误改、生成器缺陷，还是预期变更未同步 golden

golden 在此体系中的作用是“固定预期输出契约”，而不是“帮助 CI 变绿”。

## 实施顺序建议

后续实现建议按以下顺序进行：

1. 建立 `docs/golden-inputs/` 与 `docs/golden-outputs/` 的最小样例骨架
2. 为两个已纳管对象各补一组 `minimal` 样例
3. 实现 `tools/run_generation_regression.py`
4. 接入本地校验命令
5. 接入现有 CI 门禁
6. 在 `docs/CONSISTENCY_VALIDATION.md` 与 `docs/ROADMAP.md` 中更新说明

## 验收标准

当以下条件同时满足时，可认为本轮 generation regression 基线完成：

- 仓库存在统一 regression runner
- 两个已声明对象均有最小 golden 输入与 golden 输出样例
- 本地可运行 check-only regression
- 本地可显式更新 golden
- CI 可运行严格 check-only regression
- regression 失败时可定位到对象、样例与具体 diff
- `docs/ROADMAP.md` 中 v4 的输出回归项可被标记完成
