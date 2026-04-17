# consistency-review-checklist

- review id：`CR-YYYYMMDD-__`
- reviewer：`________`
- review date：`YYYY-MM-DD`
- review scope：`例如：docs + skills + templates + cases + process docs`
- 基线真源版本：`例如：docs/CONSISTENCY_VALIDATION.md@<commit/tag>`

## docs 真源层

- [ ] `ORCHESTRATION.md` 规则边界清楚（总调度职责、禁止项、输出契约明确）
- [ ] `INCIDENT_WORKFLOW.md` 未越权重写总规则（仅补充 incident 场景，不改总规则）
- [ ] `SKILL_ARCHITECTURE.md` 与正式 skill 文件一致（目录、入口、边界、依赖关系一致）
- [ ] `ORCHESTRATOR_PROMPT_CONTRACT.md` 未重写场景边界（仅定义契约，不覆盖场景规则）
- [ ] `README.md` 作为入口文档不越权定义规则（受 docs 真源层约束）
- [ ] `docs/ROADMAP.md` 作为派生文档不引入冲突口径（受 docs 真源层约束）
- [ ] `docs/WORKFLOW.md` 作为派生文档不引入冲突口径（受 docs 真源层约束）
- [ ] `docs/PLATFORMS.md` 作为派生文档不引入冲突口径（受 docs 真源层约束）
- [ ] docs 真源层结论：`通过 / 带 concern 通过 / 不通过`
- [ ] docs 真源层备注：`________`

## skills 映射层

- [ ] 正式 skill 文件未越权重写真源（无新增主规则、无改写等级定义）
- [ ] 总入口只承接，不重写真源（仅路由与编排，不复制或改写规则）
- [ ] 子入口与辅助 skill 边界清楚（输入/输出、职责、回退路径明确）
- [ ] skills 映射层结论：`通过 / 带 concern 通过 / 不通过`
- [ ] skills 映射层备注：`________`

## 模板层

- [ ] 字段完整（覆盖执行、校验、记录、追踪所需字段）
- [ ] 允许值与真源一致（对象层级、失败等级、状态值均一致）
- [ ] 模板可直接填写（含示例格式、无需二次解释）
- [ ] 模板层结论：`通过 / 带 concern 通过 / 不通过`
- [ ] 模板层备注：`________`

## 案例层

- [ ] 典型 case 覆盖足够（正例/反例/边界例）
- [ ] 路由可解释（每个 case 可追溯到明确规则）
- [ ] 与当前真源一致（无引用过期规则或旧字段）
- [ ] 案例层结论：`通过 / 带 concern 通过 / 不通过`
- [ ] 案例层备注：`________`

## 过程文档层

- [ ] spec 未保留旧规则（已清理历史冲突口径）
- [ ] plan 未保留旧字段（字段名、枚举值、流程节点为最新）
- [ ] 不会误导后续实现（交付口径清晰，可直接执行）
- [ ] 过程文档层结论：`通过 / 带 concern 通过 / 不通过`
- [ ] 过程文档层备注：`________`

## overall result

- [ ] 通过
- [ ] 带 concern 通过
- [ ] 不通过
- summary：`________`
- blocker / concern：`________`
- follow-up owner：`________`
- due date：`YYYY-MM-DD`
