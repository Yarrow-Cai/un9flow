# AGENTS.md

本仓库是 **un9flow** 的源仓库：一个面向嵌入式开发、功能安全与电力电子场景的项目。

当前阶段仓库以**方法论文档**为主，尚未发布正式可安装 skills。

## 工作原则

1. **确定性优先于优雅**
   - 优先可预测、可验证、可复盘的方案
   - 不为了“抽象好看”牺牲时序、状态可见性或故障可定位性

2. **安全优先于便利**
   - 任何设计都必须先考虑 Failsafe 默认态
   - 如果无法证明安全，就默认按不安全处理

3. **静态优先于动态**
   - 默认禁止引入 `malloc` / `free`
   - 默认禁止无必要的动态任务调度
   - 默认要求显式内存布局、显式状态转移、显式超时策略

4. **单向数据流优先于双向耦合**
   - 避免相互等待、双向握手嵌套、隐式共享状态
   - 优先把系统设计成可分段诊断、可单向追踪

## 文档与实现要求

- 修改工作流或哲学相关内容时，优先同步更新：
  - `README.md`
  - `docs/PHILOSOPHY.md`
  - `docs/WORKFLOW.md`
  - `docs/PLATFORMS.md`
  - `docs/ROADMAP.md`
- 不要把生成式空话写进文档；优先写可执行约束、检查项和失败态
- 任何涉及寄存器、时序、状态机、看门狗、故障注入的内容，都应写清默认条件与边界

## 风格偏好

- 中文优先，术语可中英混写
- 少讲虚话，多讲约束、步骤、输出物
- 不要把嵌入式问题抽象成空洞的软件工程口号
- 保持专业、克制、可验证

## 设计禁区

除非用户明确要求，否则不要轻易引入：

- 动态内存分配
- RTOS 依赖型方案
- 复杂回调地狱
- 隐式共享状态
- 魔法数字
- 无超时保护的等待逻辑
- 没有默认安全态的状态机

## 推荐默认产物

在进行嵌入式方案设计、review 或文档编写时，优先产出：

- 系统生存清单（System Survival Checklist）
- 寄存器位域地图（Register Bitfield Map）
- 通信链路健康诊断表
- 高风险失效路径清单（Critical Failure Path List）
- 跛行模式 / Failsafe 验证项

## incident-first 分层纪律

涉及 un9flow 后续 skill / agent 设计时，统一使用四层命名：

- Scenario：用户任务入口，例：`incident-investigation`
- Phase：方法论骨架，例：`hazard-analysis`
- Domain Specialist：证据域与分析动作，例：`register-state-auditor`
- Artifact：可审计输出物，例：`register-bitfield-map`

执行结构为五层（Scenario / Orchestrator / Phase / Domain Specialist / Artifact），命名纪律仍是四层（Scenario / Phase / Domain Specialist / Artifact）；Orchestrator 仅为执行拓扑中的调度角色。

- 编写或修改文档/流程时必须遵守：
  - 不要把 phase 名称当作用户入口名
  - 不要让 orchestrator 吞掉 specialist 的专业判断
  - 不要只写抽象结论，必须明确输出物（例如 `state-transition-chain`、`register-anomaly-list`）
  - 涉及 `incident-investigation` 时，优先同步 `docs/INCIDENT_WORKFLOW.md`
