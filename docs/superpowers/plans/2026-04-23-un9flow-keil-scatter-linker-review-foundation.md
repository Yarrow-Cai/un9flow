# Keil Scatter Linker Review Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 增加一个挂在 `design-safety-review` 下的 Keil Scatter / Linker Script 静态内存布局审查模板，并同步最小入口与路线图状态。

**Architecture:** 本轮不做自动分析器、map file 解析器或新的场景/角色，而是新增 `docs/templates/keil-scatter-linker-review-template.md`，并以 `design-safety-review` 为默认挂接点。当前 `.github/workflows/consistency-validation.yml` 不改结构，且本轮默认不为该模板增加新的专门校验器；只要入口文档与路线图对齐即可。

**Tech Stack:** Markdown, git, Claude Code

---

## File Structure

### Existing files to modify

- `docs/ROADMAP.md` — 把“Keil Scatter / Linker Script 审核模板”从未开始推进为已落地基线。
- `README.md`（如需入口）— 若模板需要对外可发现入口，则补最小入口说明。
- `docs/DESIGN_SAFETY_REVIEW.md`（如需最小挂接说明）— 若需要显式点名该模板归属到 `design-safety-review`，则做最小补充。

### Existing files to read but not modify

- `docs/ORCHESTRATION.md` — 主场景与分层边界真源。
- `docs/DOMAIN_SPECIALIST_CONTRACTS.md` — 现有 specialist 契约真源。
- `docs/REGISTER_STATE_AUDIT.md` — 运行态寄存器审查真源，用于和静态布局审查做边界区分。
- `docs/templates/*-pack.md` — 现有 specialist 输出模板，用于参考结构风格。

### New files to create

- `docs/templates/keil-scatter-linker-review-template.md` — Keil Scatter / Linker Script 审核模板。
- `docs/superpowers/plans/2026-04-23-un9flow-keil-scatter-linker-review-foundation.md` — 当前 implementation plan。

### No new scripts/workflows

本计划不新增自动分析脚本、map file 解析器或新的 GitHub workflow。

---

### Task 1: 先创建 Keil Scatter / Linker Script 审核模板主体

**Files:**
- Create: `docs/templates/keil-scatter-linker-review-template.md`
- Test: `docs/templates/keil-scatter-linker-review-template.md`

- [ ] **Step 1: 写出模板缺口清单**

```md
当前缺口：
- design-safety-review 已存在，但缺少面向静态内存布局的专项模板。
- 当前仓库还没有一个可审查、可对照、可升级的 scatter / linker script 审查骨架。
- 需要先把 memory region、section 落点、静态约束、证据输入与升级规则固定下来。
```

- [ ] **Step 2: 运行检查，确认当前还没有该模板文件**

Run: `git ls-files "docs/templates/keil-scatter-linker-review-template.md"`
Expected: 无输出

- [ ] **Step 3: 创建 `docs/templates/keil-scatter-linker-review-template.md`**

```md
# keil-scatter-linker-review-template

## review scope
- 项目 / 模块:
- MCU / SoC:
- 工具链:
- 审核目标:
- 当前使用的 scatter / linker 文件:

## memory region map
- Flash:
- SRAM:
- CCM / TCM / ITCM / DTCM:
- backup / noinit / retention:
- bootloader / app 分区:
- 外设 / DMA 专用区:

## section placement review
- vector table:
- startup / init:
- code / rodata:
- data / bss:
- stack / heap:
- noinit / backup:
- DMA buffer / special section:

## deterministic invariants
- 不重叠:
- 对齐正确:
- 关键区不漂移:
- 保留区不被侵占:
- bootloader / app 边界不冲突:
- stack / heap 不形成不可解释风险:

## evidence inputs
- scatter / linker script:
- map file:
- startup file:
- memory usage 输出:
- 关键编译配置:

## common risk signatures
- section 放错内存域:
- noinit / backup 区被初始化破坏:
- bootloader / app 边界冲突:
- vector table 位置异常:
- stack / heap 规划不清:
- DMA buffer 放在错误 region:
- map file 与脚本意图不一致:

## review outcome / escalation
- 通过当前 review:
- 留在 `design-safety-review` 继续补证据:
- 升级到 `incident-investigation`:
- 回到更具体的 specialist 深挖:
```

- [ ] **Step 4: 运行最小文本检查，确认 7 段结构已落地**

Run: `grep -n "review scope\|memory region map\|section placement review\|deterministic invariants\|evidence inputs\|common risk signatures\|review outcome / escalation" docs/templates/keil-scatter-linker-review-template.md`
Expected: 7 个段名全部命中

---

### Task 2: 给模板补最小入口 / 归属说明

**Files:**
- Modify: `README.md`
- Modify: `docs/DESIGN_SAFETY_REVIEW.md`
- Test: `README.md`
- Test: `docs/DESIGN_SAFETY_REVIEW.md`

- [ ] **Step 1: 在 `README.md` 增加模板入口**

```md
- `docs/templates/keil-scatter-linker-review-template.md`：`design-safety-review` 下的静态内存布局审查模板，固定 memory region、section 落点、静态约束与升级规则
```

- [ ] **Step 2: 在 `docs/DESIGN_SAFETY_REVIEW.md` 加最小挂接说明**

```md
在合适位置补一条：
- 对于 Keil Scatter / Linker Script 的静态内存布局审查，可优先使用 `docs/templates/keil-scatter-linker-review-template.md` 固定 memory region、section placement、deterministic invariants、evidence inputs 与升级规则。
```

- [ ] **Step 3: 运行最小文本检查**

Run: `grep -n "keil-scatter-linker-review-template" README.md docs/DESIGN_SAFETY_REVIEW.md`
Expected: README 与 DESIGN_SAFETY_REVIEW.md 均命中该模板路径

---

### Task 3: 同步 ROADMAP 并确认模板已被入口文档引用

**Files:**
- Modify: `docs/ROADMAP.md`
- Test: `docs/ROADMAP.md`
- Test: `README.md`
- Test: `docs/DESIGN_SAFETY_REVIEW.md`
- Test: `docs/templates/keil-scatter-linker-review-template.md`

- [ ] **Step 1: 在 `docs/ROADMAP.md` 把审核模板标记为已落地基线**

```md
将：
- [ ] Keil Scatter / Linker Script 审核模板

改成：
- [x] Keil Scatter / Linker Script 审核模板已落地：`docs/templates/keil-scatter-linker-review-template.md` 作为 `design-safety-review` 下的专项模板
```

- [ ] **Step 2: 运行最小文本检查，确认模板已被入口文档与路线图引用**

Run: `grep -n "keil-scatter-linker-review-template" README.md docs/ROADMAP.md docs/DESIGN_SAFETY_REVIEW.md docs/templates/keil-scatter-linker-review-template.md`
Expected: 4 个文件都命中该模板路径

- [ ] **Step 3: 提交 scatter / linker 审核模板基线**

```bash
git add docs/templates/keil-scatter-linker-review-template.md README.md docs/ROADMAP.md docs/DESIGN_SAFETY_REVIEW.md
git commit -m "feat: add linker review template"
```

---

## Verification Notes

- 本计划不新增自动分析器；本轮目标只到模板级交付物。
- 本计划默认不扩展 `tools/validate_consistency.py`；当前目标是模板对象落地与入口同步，而不是新增专门校验器。
- 该模板必须始终保持 `design-safety-review` 下的专项模板定位；若实现中把它写成新的主场景、specialist 或运行态排障模板，必须回退。