# OpenClaw Host Foundation

## 目标

OpenClaw host foundation 的目标是为外层调度提供统一的真源文档，明确其职责边界、与仓库内总调度的协作关系，以及对场景真源和 skill 的引用方式。本文档作为外层调度的唯一入口，确保所有参与者对调度范围有一致理解。

## 外层调度定位

外层调度是 OpenClaw host 的协调层，负责在仓库外部或跨仓库场景下发起、监控和完成复杂任务。它不替代仓库内的总调度，而是作为总调度的发起方或结果接收方，承担跨边界协调职责。

## 可负责的动作

- 发起并跟踪需要多仓库协作的任务流程
- 调用并解释以下文档以指导调度行为：
  - `docs/ORCHESTRATION.md`
  - `docs/INCIDENT_WORKFLOW.md`
  - `docs/BRINGUP_PATH.md`
  - `docs/DESIGN_SAFETY_REVIEW.md`
  - `skills/orchestration/SKILL.md`
- 在任务完成后进行结果汇总和状态同步
- 在出现阻塞时升级问题并触发 incident 流程

## 不负责的动作

- 不直接执行仓库内的具体构建、测试或部署命令
- 不修改仓库源代码或配置文件
- 不替代仓库内 CI/CD 系统的判断逻辑
- 不维护技能（skill）本身的实现细节

## 与仓库内总调度的关系

外层调度通过引用 `docs/ORCHESTRATION.md` 与仓库内总调度建立契约。外层调度负责定义"做什么"和"何时完成"，仓库内总调度负责定义"怎么做"和"何时可以开始"。两者通过状态检查点和结果回传机制保持同步。

## 与场景真源和 skill 的关系

外层调度依赖场景真源文档来理解各仓库的专用流程，并通过 skill 接口执行标准化操作。具体而言：

- `docs/INCIDENT_WORKFLOW.md` 提供异常处理真源
- `docs/BRINGUP_PATH.md` 提供环境启动真源
- `docs/DESIGN_SAFETY_REVIEW.md` 提供安全审查真源
- `skills/orchestration/SKILL.md` 提供可复用的调度 skill 接口

外层调度不拥有这些文档的维护权，但必须在执行相关流程时严格引用它们。

此外，平台优先级、预留位背景与非承诺边界继续以 `docs/PLATFORMS.md` 为准；本文档只负责 OpenClaw 作为外层调度器的角色边界，不重写平台战略。

## 当前明确不承诺

- 不承诺支持实时调度或毫秒级响应场景
- 不承诺自动解决所有跨仓库依赖冲突
- 不承诺替代任何仓库内部的治理流程
- 不承诺对尚未纳入 `docs/ORCHESTRATION.md` 的仓库进行调度
