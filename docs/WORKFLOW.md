# un9flow 工作流

`un9flow` 的默认流程如下：

```text
Hazard Analysis -> Deterministic Foundation -> Link Diagnostics -> Failsafe Validation
```

## 1. Hazard Analysis

### 目标
先定义风险边界、失效模式和默认安全态，再进入具体实现。

### 核心问题
- 最坏后果是什么？
- 哪些非功能约束比功能本身更高优先级？
- 默认安全态是什么？
- 哪些失效模式绝对不可接受？

### 推荐输出
- 生存清单
- 失效模式清单
- 非功能约束基线
- 看门狗与超时策略草案

## 2. Deterministic Foundation

### 目标
把寄存器、内存、状态机、ISR 与主循环职责固化为确定性结构。

### 核心问题
- 是否引入了动态内存？
- 是否存在难以观察的隐式状态？
- ISR 是否过长、过重或可阻塞？
- RAM / Flash / noinit / backup 区域是否明确？

### 推荐输出
- 寄存器位域地图
- 静态内存布局
- 状态机图
- ISR / 主循环职责表

## 3. Link Diagnostics

### 目标
让通信链路、采样路径与板级接口具备明确的可观测性与可诊断性。

### 核心问题
- 某一段掉线时，是否能定位到具体区段或器件？
- 是否定义了链路健康度、重试、降级、超时与恢复策略？
- 是否提前确定了示波器 / 逻辑分析仪观测点？

### 推荐输出
- 通信链路健康诊断表
- 分段定位步骤
- 波形观测计划
- 链路故障注入点

## 4. Failsafe Validation

### 目标
主动制造异常，验证系统是否能够进入预定义的安全收敛状态。

### 核心问题
- 缺压、过压、过温、超时、CRC 错误、掉线、漂移时会怎样？
- 会不会进入 Limp Home？
- 会不会错误驱动功率器件？
- 看门狗会不会按预期复位？

### 推荐输出
- 故障注入矩阵
- 跛行模式验证表
- 热 / 压 / 时序 / 通信故障注入清单
- 安全态收敛验证记录

## 推荐执行节奏

### 新功能 / 新板卡 bring-up
```text
hazard-analysis -> deterministic-foundation -> link-diagnostics -> failsafe-validation
```

### 已有系统问题排查
```text
hazard-analysis -> link-diagnostics -> failsafe-validation -> deterministic-foundation
```

### 功能安全复核
```text
hazard-analysis -> deterministic-foundation -> failsafe-validation
```

## 核心信条

- 不先讨论抽象层次，先定义系统边界
- 不先讨论功能完成度，先定义异常收敛路径
- 不先讨论复用与扩展，先保证可预测、可定位、可验证
