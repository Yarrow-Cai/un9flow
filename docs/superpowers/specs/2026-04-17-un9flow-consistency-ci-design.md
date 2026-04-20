# un9flow 一致性校验 CI / GitHub Action 设计稿

日期：2026-04-17
主题：围绕本地一致性校验 CLI，定义第一版 PR / main 严格门禁型 GitHub Action 接入方案

## 1. 设计结论摘要

本轮设计采用如下方向：

- 第一版 CI 接入采用 **最小门禁型 GitHub Action**
- 只运行当前已有的本地 CLI：
  - `python tools/validate_consistency.py`
- 触发方式固定为：
  - `pull_request`
  - `push` 到 `main`
- 顶层触发不使用 `on.paths` 过滤，始终在以下事件触发：
  - `pull_request`
  - `push` 到 `main`
- 相关路径过滤改为在 job 内通过 diff 检测（`Detect relevant changes`）实现，覆盖：
  - `docs/**`
  - `skills/**`
  - `tools/**`
  - `.github/workflows/**`
  - `README.md`
- 无相关改动时打印并成功跳过：
  - `No relevant changes, skipping validation.`
- 采用 **严格阻断**：
  - CLI 返回非 0 即让 job fail
- 第一版不做 artifact、summary、matrix、reusable workflow、观察模式或 host-specific 校验流程

一句话总结：

> 用一个最小但严格的 `.github/workflows/consistency-validation.yml`，把当前本地一致性校验 CLI 接成 PR / main 的真实门禁。

---

## 2. CI workflow 的文件落点与基本结构

### 2.1 文件落点

建议新增：

- `.github/workflows/consistency-validation.yml`

命名应和当前概念保持一致：

- docs：`CONSISTENCY_VALIDATION`
- CLI：`validate_consistency.py`
- workflow：`consistency-validation`

### 2.2 触发方式

第一版固定为：

- `pull_request`
- `push` 到 `main`

### 2.3 相关路径检测方式

第一版不在 `on:` 顶层使用 `paths` 过滤，保留事件级稳定触发：

- `pull_request`
- `push` 到 `main`

相关路径过滤放在 job 内通过 `Detect relevant changes` 的 diff 检测完成，固定覆盖：

- `docs/**`
- `skills/**`
- `tools/**`
- `.github/workflows/**`
- `README.md`

无相关改动时显式打印并成功跳过：

- `No relevant changes, skipping validation.`

### 2.4 job 结构

第一版只保留一个 job：

- `validate-consistency`

不拆多 job，不做 matrix，不做并行。

---

## 3. workflow 里的 job 步骤定义

第一版最小 workflow 建议固定成以下结构：

1. `actions/checkout`
2. `Detect relevant changes`
3. `actions/setup-python`（固定 Python 3.11）
4. `Run consistency validation` / `Skip consistency validation when no relevant changes`

其中最后一步语义是：

- 有相关改动：

```bash
python tools/validate_consistency.py
```

- 无相关改动：

```bash
echo "No relevant changes, skipping validation."
```

### 3.1 为什么不加更多步骤

第一版明确不加：

- pip install
- requirements.txt
- cache
- artifact upload
- summary generation
- multi-job split

原因：

- 当前脚本无第三方依赖
- 当前最重要的是门禁先跑通

---

## 4. 相关路径检测与严格阻断规则

### 4.1 相关路径检测规则

第一版采用 job 内 diff 检测，不把顶层 `on.paths` 作为实现方式。

检测覆盖路径固定为：

- `docs/**`
- `skills/**`
- `tools/**`
- `.github/workflows/**`
- `README.md`

### 4.2 跳过规则

- 若无相关改动，输出：`No relevant changes, skipping validation.`
- 跳过分支必须成功退出，确保 required check 不会处于 skipped/pending

### 4.3 阻断规则

采用严格阻断：

- `python tools/validate_consistency.py` 返回非 0
- job 自动失败

### 4.4 当前退出码与门禁关系

- `0`：通过
- `1`：存在 L1，阻断
- `2`：存在 L2，阻断

L3 不影响退出码。

### 4.4 为什么 L2 也要阻断

因为统一校验体系已定义 L2 为：

> 本轮应优先修，否则必须显式记录的重要级问题。

所以第一版 CI 中：
- L1 阻断
- L2 也阻断
- 只有 L3 可通过

---

## 5. 这轮 CI / GitHub Action 的最终落点与实现顺序

### 5.1 最终落点

第一版只落：

- `.github/workflows/consistency-validation.yml`

目标是把本地 CLI 变成真实门禁。

### 5.2 第一版明确不做

- artifact 上传
- GitHub summary 美化
- matrix job
- 并行 job
- reusable workflow
- host-specific 检查
- 观察模式

### 5.3 实现顺序建议

建议固定为：

1. 写 workflow 文件本体
2. 本地做 YAML / 结构检查
3. 在远端通过 PR / main 真正跑一次

### 5.4 这轮与下一轮的边界

- 这轮解决：**能不能阻断**
- 下一轮再解决：**怎样更好看、更易读、更可下载**

---

## 6. 最终结论

本轮 CI / GitHub Action 接入的推荐方向是：

> 先把当前本地一致性校验 CLI 以最小成本接进 GitHub Actions：单 workflow、单 job、PR/main 触发、path filter、严格阻断。