# un9flow Consistency CI Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 把当前本地一致性校验 CLI 接成一个最小但严格的 GitHub Actions 门禁。

**Architecture:** 这一轮聚焦 `.github/workflows/consistency-validation.yml` 的最小严格门禁结构。workflow 在 `pull_request` 与 `push` 到 `main` 时始终触发；相关路径通过 job 内 `Detect relevant changes` 做 diff 检测：有相关改动时执行 `python tools/validate_consistency.py`，无相关改动时输出 `No relevant changes, skipping validation.` 并成功退出；严格依赖 CLI 退出码作为门禁，不增加 artifact、summary、matrix、reusable workflow 等增强层。

**Tech Stack:** GitHub Actions YAML, Python 3.11, git, GitHub

---

## File Structure

### Existing files to read/validate against

- `tools/validate_consistency.py` — 当前本地一致性校验 CLI，本轮 workflow 的唯一执行目标。
- `docs/CONSISTENCY_VALIDATION.md` — 统一校验体系真源，用于确认 L1/L2/L3 退出码语义。
- `docs/ROADMAP.md` — 当前 roadmap，用于后续同步 v4 / CI 基线状态（本轮如需微调）。

### New files to create

- `docs/superpowers/plans/2026-04-17-un9flow-consistency-ci-foundation.md` — 当前 implementation plan。
- `.github/workflows/consistency-validation.yml` — 第一版一致性校验 workflow。

### Optional follow-up files (only if scope expands later)

- artifact 上传
- GitHub summary
- matrix / multi-job
- reusable workflow
- host-specific 校验 workflow

当前计划默认**不**创建 optional files；这一轮只建立一个最小门禁 workflow。

---

### Task 1: 创建最小门禁 workflow

**Files:**
- Create: `.github/workflows/consistency-validation.yml`
- Test: `.github/workflows/consistency-validation.yml`

- [x] **Step 1: 写出 workflow 落地缺口清单**

```md
当前缺口：
- 需要让 workflow 在 `pull_request` 与 `push` 到 `main` 时稳定触发。
- 需要把相关路径过滤放进 job 内 `Detect relevant changes`（diff 检测），而不是顶层 `on.paths`。
- 需要把“有改动执行 CLI / 无改动成功跳过”与严格阻断写死。
```

- [x] **Step 2: 记录与真源对齐点（以现有 workflow 为准）**

Run: `grep -n "pull_request\|push\|main\|Detect relevant changes\|No relevant changes, skipping validation\." .github/workflows/consistency-validation.yml`
Expected: 触发与步骤关键字可检出

- [x] **Step 3: 同步文档中的 workflow 示例（与真源一致）**

```yaml
name: consistency-validation

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  validate-consistency:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Detect relevant changes
        id: changes
        shell: bash
        run: |
          if [ "${{ github.event_name }}" = "pull_request" ]; then
            base_sha="${{ github.event.pull_request.base.sha }}"
          else
            base_sha="${{ github.event.before }}"
          fi

          if [ -z "$base_sha" ] || [ "$base_sha" = "0000000000000000000000000000000000000000" ]; then
            base_sha="$(git rev-list --max-parents=0 HEAD)"
          fi

          relevant_paths_regex='(docs/|skills/|tools/|\.github/workflows/|(^|[[:space:]])README\.md([[:space:]]|$))'

          if git diff --name-status --find-renames "$base_sha" "${{ github.sha }}" | grep -E "(^|[[:space:]])$relevant_paths_regex" >/dev/null; then
            echo "has_relevant_changes=true" >> "$GITHUB_OUTPUT"
          else
            echo "has_relevant_changes=false" >> "$GITHUB_OUTPUT"
          fi

      - uses: actions/setup-python@v5
        if: steps.changes.outputs.has_relevant_changes == 'true'
        with:
          python-version: '3.11'

      - name: Run consistency validation
        if: steps.changes.outputs.has_relevant_changes == 'true'
        run: python tools/validate_consistency.py

      - name: Skip consistency validation when no relevant changes
        if: steps.changes.outputs.has_relevant_changes != 'true'
        run: echo "No relevant changes, skipping validation."
```

- [x] **Step 4: 运行结构检查**

Run: `grep -n "pull_request\|push\|main\|Detect relevant changes\|actions/setup-python\|python tools/validate_consistency.py\|No relevant changes, skipping validation\." .github/workflows/consistency-validation.yml`
Expected: workflow 关键触发、检测步骤、执行与跳过语义均能检出

- [x] **Step 5: 本任务不做 commit**

---

### Task 2: 校验 workflow 与 CLI 阻断语义一致

**Files:**
- Modify: `.github/workflows/consistency-validation.yml` (如需微调)
- Test: `.github/workflows/consistency-validation.yml`, `tools/validate_consistency.py`

- [x] **Step 1: 写出阻断语义检查清单**

```md
需要确认：
- workflow 顶层只保留 `pull_request` 与 `push` 到 `main` 触发
- 相关路径通过 `Detect relevant changes` 做 job 内 diff 检测
- 有相关改动时运行 CLI，非 0 退出码直接让 job fail
- 无相关改动时输出 `No relevant changes, skipping validation.` 并成功退出
```

- [x] **Step 2: 检查顶层触发与分支约束是否正确**

Run: `grep -n "^on:\|pull_request:\|push:\|branches:\|main" .github/workflows/consistency-validation.yml`
Expected: 顶层触发包含 `pull_request` 与 `push`，并限定 `main`

- [x] **Step 3: 检查 job 内相关路径检测与跳过语义**

Run: `grep -n "Detect relevant changes\|docs/\|skills/\|tools/\|\.github/workflows/\|README\.md\|No relevant changes, skipping validation\." .github/workflows/consistency-validation.yml`
Expected: 检测步骤、五类路径模式与跳过提示均存在

- [x] **Step 4: 检查 workflow 是否严格依赖 CLI 退出码**

Run: `grep -n "python tools/validate_consistency.py\|continue-on-error" .github/workflows/consistency-validation.yml`
Expected: 有 CLI 执行命令；不应存在放宽失败的 `continue-on-error`

- [x] **Step 5: 本任务不做 commit**

---

### Task 3: 同步 spec/plan 到 workflow 真源

**Files:**
- Modify: `docs/superpowers/specs/2026-04-17-un9flow-consistency-ci-design.md`
- Modify: `docs/superpowers/plans/2026-04-17-un9flow-consistency-ci-foundation.md`
- Test: 上述两个文件

- [x] **Step 1: 写出文档同步缺口清单**

```md
当前缺口：
- 文档仍把顶层 `on.paths` 过滤写成主实现。
- 文档仍是“3 步结构”，未包含 `Detect relevant changes` 与 skip 分支。
- 文档未明确“无相关改动成功跳过”语义。
```

- [x] **Step 2: 在 spec 更新触发、检测、跳过与最小结构描述**

```md
对齐真源：
- 顶层不使用 `on.paths`
- 保留 `pull_request` / `push main`
- job 内 `Detect relevant changes`
- 无相关改动输出 `No relevant changes, skipping validation.` 并成功退出
- 最小结构更新为 checkout / detect / setup python / run-or-skip
```

- [x] **Step 3: 在 plan 更新 YAML 示例、检查项与自审描述**

```md
对齐真源：
- YAML 示例改为顶层无 `paths`、job 内 diff 检测
- 结构检查项改为 trigger + detect + run-or-skip
- 自审结论改为“相关路径检测采用 job 内 diff”
```

- [x] **Step 4: 运行一致性检查**

Run: `grep -n "Detect relevant changes\|No relevant changes, skipping validation\.\|pull_request\|push\|main" docs/superpowers/specs/2026-04-17-un9flow-consistency-ci-design.md docs/superpowers/plans/2026-04-17-un9flow-consistency-ci-foundation.md`
Expected: 两个文件均命中关键字段

- [x] **Step 5: 本任务不做 commit**

---

### Task 4: 自审、验证与收口

**Files:**
- Modify: `docs/superpowers/specs/2026-04-17-un9flow-consistency-ci-design.md` (如需微调)
- Modify: `docs/superpowers/plans/2026-04-17-un9flow-consistency-ci-foundation.md` (如需微调)
- Test: 上述两个过程文档

- [x] **Step 1: 运行过程文档关键字段检查**

Run: `grep -n "Detect relevant changes\|No relevant changes, skipping validation\.\|pull_request\|push\|main" docs/superpowers/specs/2026-04-17-un9flow-consistency-ci-design.md docs/superpowers/plans/2026-04-17-un9flow-consistency-ci-foundation.md`
Expected: 两个过程文档都命中关键字段

- [x] **Step 2: 检查文档已不再把顶层 `paths` 当作唯一实现方式**

Run: `grep -n "top-level paths only\|仅靠 on\.paths\|顶层.*paths.*唯一" docs/superpowers/specs/2026-04-17-un9flow-consistency-ci-design.md docs/superpowers/plans/2026-04-17-un9flow-consistency-ci-foundation.md`
Expected: 无命中

- [x] **Step 3: 运行 git diff 范围审核**

Run: `git diff -- docs/superpowers/specs/2026-04-17-un9flow-consistency-ci-design.md docs/superpowers/plans/2026-04-17-un9flow-consistency-ci-foundation.md`
Expected: 仅两份过程文档有改动

- [x] **Step 4: 如发现问题，做最小修正**

```md
允许的修正类型：
- 修正 trigger / 检测 / skip 描述
- 修正 YAML 示例与检查项口径
- 修正自审结论口径
```

- [x] **Step 5: 本任务不做 commit**

---

## Self-Review

### Spec coverage

- 规格第 2 节 workflow 结构：Task 1 覆盖
- 规格第 3 节 job 步骤：Task 1 与 Task 2 覆盖
- 规格第 4 节相关路径检测与严格阻断：Task 2 覆盖
- 规格第 5 节最终落点与实现顺序：Task 1、Task 2、Task 3 覆盖

### Placeholder scan

本计划没有使用 “TBD / TODO / implement later / similar to Task N” 作为执行步骤占位语，所有步骤都包含明确文件、命令或文档内容。

### Type consistency

计划中统一使用以下关键名词：

- workflow：`.github/workflows/consistency-validation.yml`
- CLI：`python tools/validate_consistency.py`
- 触发：`pull_request` / `push` to `main`
- 相关路径检测：job 内 diff（覆盖 `docs/**` / `skills/**` / `tools/**` / `.github/workflows/**` / `README.md`）
- 失败策略：非 0 严格阻断

未使用冲突命名。