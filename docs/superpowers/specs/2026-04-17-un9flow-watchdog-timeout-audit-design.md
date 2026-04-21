# un9flow watchdog / timeout 审计方法设计稿

日期：2026-04-17
主题：围绕 `design-safety-review` 下的 watchdog / timeout 专项能力，定义方法边界、核心检查项与 checklist 落点

## 1. 设计结论摘要

本轮设计采用如下方向：

- 将 watchdog / timeout 审计能力定义为 **`design-safety-review` 下的专项能力**
- 第一版采用 **方法文档 + checklist** 组合，而不是直接落正式 skill 文件
- 覆盖范围采用 **全链路但限主题**：
  - timeout 触发源
  - 计时基线
  - 喂狗路径
  - 阻塞 / 饥饿风险
  - 复位链
  - failsafe 收敛
- 每组检查项统一输出：
  - `finding`
  - `evidence`
  - `risk`
  - `next action`
- 第一版只限 watchdog / timeout，不扩到其他保护链专题

一句话总结：

> 先把 watchdog / timeout 审计能力作为 `design-safety-review` 下的专项方法真源落成 `docs/WATCHDOG_TIMEOUT_AUDIT.md`，并同步配一份可填写的 audit checklist 模板，让后续 skill / findings / CI 都有可继承的 embedded 专项基线。

---

## 2. 方法文档的定位与边界

建议将 watchdog / timeout 审计定义成：

- `design-safety-review` 下的专项能力
- 面向 watchdog / timeout 这一主题
- 重点审查系统是否具备可解释、可验证、可收敛的时间保护机制

### 2.1 它属于什么

它是：

- `design-safety-review` 的专项能力
- 围绕时间保护与复位收敛机制展开的审计方法
- 用于验证系统在异常情况下是否能阻止继续错下去

### 2.2 它不属于什么

第一版明确排除：

1. 不是独立主场景
2. 不是通用性能分析
3. 不是任意异常排障入口
4. 不是所有保护逻辑的大杂烩

### 2.3 审计对象范围

第一版固定为 6 类对象：

1. timeout 触发源
2. 计时基线
3. 喂狗路径
4. 阻塞 / 饥饿风险
5. 复位链
6. failsafe 收敛

### 2.4 关键边界句

建议用一句硬规则收口：

> watchdog / timeout 审计能力的核心，不是解释“哪里坏了”，而是验证“时间保护机制是否足以在坏掉时阻止系统继续错下去”。

---

## 3. 核心检查项骨架

建议第一版 checklist 固定为 6 组：

```text
1. timeout definition
2. timing baseline
3. watchdog feed path
4. blocking / starvation risk
5. reset chain
6. failsafe convergence
```

### 3.1 timeout definition

重点检查：

- timeout 由谁定义
- 单位和基准是否明确
- 默认值是否有依据

### 3.2 timing baseline

重点检查：

- 时基来源
- 时基是否单一且可解释
- 计时是否受阻塞影响

### 3.3 watchdog feed path

重点检查：

- 谁在喂狗
- 喂狗发生在什么条件下
- 喂狗是全局健康证明还是局部成功证明
- 是否存在假健康设计

### 3.4 blocking / starvation risk

重点检查：

- 长时间阻塞路径
- 长时间不退出路径
- 调度 / 饥饿风险
- timeout 与 watchdog 是否可能因此失效

### 3.5 reset chain

重点检查：

- watchdog 到 reset 的路径是否闭合
- reset 后进入什么状态
- reset 后是否回默认安全态
- sticky flag / noinit / backup 状态是否可能导致危险回返

### 3.6 failsafe convergence

重点检查：

- timeout / watchdog 触发后是否存在明确定义的收敛路径
- 收敛到哪里
- 是否存在危险中间态
- 是否会继续冒险运行

---

## 4. 每组检查项的输出结构

建议每组检查项统一输出：

1. `finding`
2. `evidence`
3. `risk`
4. `next action`

### 4.1 `finding`

一句话写主判断。

### 4.2 `evidence`

列支撑该判断的关键证据。

### 4.3 `risk`

说明问题后果、风险类别和阻断程度。

### 4.4 `next action`

给出最小可执行动作。

### 4.5 审计结果的最小形态

建议后续至少形成：

- checklist 主表
- findings 清单
- 阻断项列表
- 建议动作列表

---

## 5. 这轮文档落点与实现顺序

### 5.1 方法文档落点

建议新增：

- `docs/WATCHDOG_TIMEOUT_AUDIT.md`

职责：

- 作为 watchdog / timeout 审计方法真源
- 承接定位、边界、检查项、输出结构

### 5.2 checklist 模板落点

建议新增：

- `docs/templates/watchdog-timeout-audit-checklist.md`

职责：

- 将 6 组检查项落成可填写模板
- 服从方法文档真源，不自行发明新规则

### 5.3 第一版明确不做

- 正式 skill 文件
- 自动校验脚本
- CI 门禁
- 报告生成器
- 其他保护链专题

### 5.4 实现顺序建议

建议固定为：

1. 先写方法文档 `WATCHDOG_TIMEOUT_AUDIT.md`
2. 再写 checklist 模板
3. findings 模板留给下一轮，如有需要再补

---

## 6. 最终结论

本轮 watchdog / timeout 审计能力的推荐方向是：

> 先落 `docs/WATCHDOG_TIMEOUT_AUDIT.md` 作为专项方法真源，再落 `docs/templates/watchdog-timeout-audit-checklist.md` 作为可执行审计模板；暂不扩成独立主场景或正式 skill 文件。