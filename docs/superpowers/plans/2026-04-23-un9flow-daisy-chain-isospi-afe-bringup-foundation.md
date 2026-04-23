# Daisy Chain isoSPI AFE Bring-up Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 增加一个挂在 `bringup-path` 下的菊花链 / isoSPI / AFE 首次拉通模板，用于固定 bring-up 步骤、观测点、基线判据与升级规则。

**Architecture:** 本轮不做新的主场景、specialist 或自动脚本，而是新增一个 bring-up 专项模板 `docs/templates/daisy-chain-isospi-afe-bringup-template.md`，并只做最小入口/路线图同步。当前 `.github/workflows/consistency-validation.yml` 不改结构，且本轮默认不为该模板增加新的专门校验器；只要入口文档与路线图对齐即可。

**Tech Stack:** Markdown, git, Claude Code

---

## File Structure

### Existing files to modify

- `docs/ROADMAP.md` — 把“菊花链 / isoSPI / AFE bring-up 模板”从未开始推进为已落地基线。
- `README.md`（如需入口）— 若模板需要对外可发现入口，则补最小入口说明。
- `skills/bringup-path/SKILL.md`（如需最小挂接说明）— 若需要显式点名该模板归属到 bringup-path，则做最小补充。

### Existing files to read but not modify

- `docs/ORCHESTRATION.md` — 主场景与分层边界真源。
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` — 场景输入输出协议基线。
- `docs/DOMAIN_SPECIALIST_CONTRACTS.md` — 现有 specialist 契约真源。
- `docs/templates/*-pack.md` — 现有 specialist 输出模板，用于参考结构风格。

### New files to create

- `docs/templates/daisy-chain-isospi-afe-bringup-template.md` — bring-up 专项模板。
- `docs/superpowers/plans/2026-04-23-un9flow-daisy-chain-isospi-afe-bringup-foundation.md` — 当前 implementation plan。

### No new scripts/workflows

本计划不新增自动 bring-up 脚本、实验报告生成器或新的 GitHub workflow。

---

### Task 1: 先创建 bring-up 模板主体

**Files:**
- Create: `docs/templates/daisy-chain-isospi-afe-bringup-template.md`
- Test: `docs/templates/daisy-chain-isospi-afe-bringup-template.md`

- [ ] **Step 1: 写出模板缺口清单**

```md
当前缺口：
- bringup-path 已存在，但缺少面向菊花链 / isoSPI / AFE 首次拉通的专项模板。
- 当前仓库还没有一个可重复、可回归、可审查的硬件链路 bring-up 骨架。
- 需要先把 bring-up 的步骤、观测点、基线判据与升级规则固定下来。
```

- [ ] **Step 2: 运行检查，确认当前还没有该模板文件**

Run: `git ls-files "docs/templates/daisy-chain-isospi-afe-bringup-template.md"`
Expected: 无输出

- [ ] **Step 3: 创建 `docs/templates/daisy-chain-isospi-afe-bringup-template.md`**

```md
# daisy-chain-isospi-afe-bringup-template

## bring-up scope
- 板卡 / 模块名称:
- AFE 型号:
- 菊花链拓扑:
- 当前硬件版本:
- 当前 bring-up 目标:

## prerequisites
- 供电条件:
- 复位条件:
- 时钟 / 唤醒条件:
- 关键引脚状态:
- 安全限制:

## chain establishment steps
1. 上电
2. 唤醒
3. 基本通信探测
4. 链路寻址 / 枚举
5. AFE 基本寄存器读回
6. 首次健康检查

## observability points
- 关键寄存器:
- 关键状态位:
- 关键波形 / 引脚:
- 错误码 / timeout 现象:

## baseline qualification
- 最小可重复读写条件:
- 链路稳定条件:
- AFE 状态一致性条件:
- 可进入下一阶段的判据:

## common failure signatures
- 完全无响应:
- 链路偶发掉线:
- 节点数不对:
- 唤醒后状态异常:
- 读回值不稳定:
- timeout / CRC / framing 异常:

## escalation rules
- 继续停留在 `bringup-path`:
- 升级到 `incident-investigation`:
- 升级到 `design-safety-review`:
```

- [ ] **Step 4: 运行最小文本检查，确认 7 段结构已落地**

Run: `grep -n "bring-up scope\|prerequisites\|chain establishment steps\|observability points\|baseline qualification\|common failure signatures\|escalation rules" docs/templates/daisy-chain-isospi-afe-bringup-template.md`
Expected: 7 个段名全部命中

---

### Task 2: 给模板补最小入口 / 归属说明

**Files:**
- Modify: `README.md`
- Modify: `skills/bringup-path/SKILL.md`
- Test: `README.md`
- Test: `skills/bringup-path/SKILL.md`

- [ ] **Step 1: 在 `README.md` 增加模板入口**

```md
- `docs/templates/daisy-chain-isospi-afe-bringup-template.md`：`bringup-path` 下的菊花链 / isoSPI / AFE 首次拉通模板，固定步骤、观测点、基线判据与升级规则
```

- [ ] **Step 2: 在 `skills/bringup-path/SKILL.md` 加最小挂接说明**

```md
在“场景特化段”或末尾补一条：
- 对于菊花链 / isoSPI / AFE 的首次拉通，可优先使用 `docs/templates/daisy-chain-isospi-afe-bringup-template.md` 固定 bring-up 步骤、观测点、基线判据与升级规则。
```

- [ ] **Step 3: 运行最小文本检查**

Run: `grep -n "daisy-chain-isospi-afe-bringup-template" README.md skills/bringup-path/SKILL.md`
Expected: README 与 bringup-path/SKILL.md 均命中该模板路径

---

### Task 3: 同步 ROADMAP 并确认工作区文本状态

**Files:**
- Modify: `docs/ROADMAP.md`
- Test: `docs/ROADMAP.md`
- Test: `README.md`
- Test: `skills/bringup-path/SKILL.md`

- [ ] **Step 1: 在 `docs/ROADMAP.md` 把 bring-up 模板标记为已落地基线**

```md
将：
- [ ] 菊花链 / isoSPI / AFE bring-up 模板

改成：
- [x] 菊花链 / isoSPI / AFE bring-up 模板已落地：`docs/templates/daisy-chain-isospi-afe-bringup-template.md` 作为 `bringup-path` 下的专项模板
```

- [ ] **Step 2: 运行最小文本检查，确认模板已被入口文档与路线图引用**

Run: `grep -n "daisy-chain-isospi-afe-bringup-template" README.md docs/ROADMAP.md skills/bringup-path/SKILL.md docs/templates/daisy-chain-isospi-afe-bringup-template.md`
Expected: 4 个文件都命中该模板路径

- [ ] **Step 3: 提交 bring-up 模板基线**

```bash
git add docs/templates/daisy-chain-isospi-afe-bringup-template.md README.md docs/ROADMAP.md skills/bringup-path/SKILL.md
git commit -m "feat: add daisy-chain bringup template"
```

---

## Verification Notes

- 本计划不新增自动 bring-up 脚本；本轮目标只到模板级交付物。
- 本计划默认不扩展 `tools/validate_consistency.py`；当前目标是模板对象落地与入口同步，而不是新增专门校验器。
- 该模板必须始终保持 `bringup-path` 下的专项模板定位；若实现中把它写成新的主场景、specialist 或 incident 分析模板，必须回退。