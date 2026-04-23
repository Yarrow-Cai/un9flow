# keil scatter / linker review template

## template gap checklist
- 已有 `design-safety-review`，但缺少面向静态内存布局的专项模板。
- 当前仓库还没有一个可审查、可对照、可升级的 scatter / linker script 审查骨架。
- 需要先把 memory region、section 落点、静态约束、证据输入与升级规则固定下来。

## review scope
- 项目 / 模块：
- MCU / SoC：
- 工具链：
- 审核目标：
- 当前使用的 scatter / linker 文件：
- 边界说明（静态布局态）：
  - 本模板仅审查 scatter / linker 定义与 map 结果体现的静态内存布局一致性。
  - 本模板不直接覆盖运行时行为（如任务调度/中断时序引发的行为变化）与动态内存时序问题（如 malloc/free 时序与碎片演化）。
  - 运行态异常线索应转交对应运行态评审路径或 `incident-investigation` 处理。

## memory region map
- Flash：
- SRAM：
- CCM / TCM / ITCM / DTCM：
- backup / noinit / retention：
- bootloader / app 分区：
- 外设 / DMA 专用区：

## section placement review
- vector table：
- startup / init：
- code / rodata：
- data / bss：
- stack / heap：
- noinit / backup：
- DMA buffer / special section：

## deterministic invariants
- 不重叠：任意 section 的地址区间在 map 中不得重叠，除非脚本中有显式覆盖/复用声明且有证据说明。
- 对齐正确：关键 section 的起始地址与脚本声明对齐约束一致，并可在 map 中逐项核对。
- 关键区稳定：关键 section（如 vector table、startup、boot metadata）地址或大小在构建间不得发生未解释变化。
- 保留区不被侵占：noinit / backup / retention 等保留区边界不得被其他 section 占用。
- bootloader / app 边界不冲突：两者地址范围满足分区定义且不存在交叉或越界。
- stack / heap 可解释：stack / heap 边界、预留量与相关静态风险判断可由 linker script 与 map 结果直接解释。

## evidence inputs
- scatter / linker script：
- map file：
- startup file：
- memory usage 输出：
- 关键编译配置：

## common risk signatures
- section 放错内存域：
- noinit / backup 区被初始化破坏：
- bootloader / app 边界冲突：
- vector table 位置异常：
- stack / heap 规划不清：
- DMA buffer 放在错误 region：
- map file 与脚本意图不一致：

## review outcome / escalation
- 通过当前 review：
  - 所有静态约束项均可由脚本与 map 证据闭环；
  - 无未解释地址/尺寸漂移；
  - 未发现静态分区冲突、保留区侵占或放置错误。
- 留在 `design-safety-review` 继续补证据：
  - 当前仅存在证据缺口（如缺少关键构建 map、分区基线或变更说明），但未观察到明确静态冲突；
  - 结论依赖补充证据后可判定，不涉及已发生异常事件。
- 升级到 `incident-investigation`：
  - 已发生或高置信关联到静态布局错误的现场异常，且现有脚本/map 证据无法解释；
  - 发现跨版本关键区异常漂移并与故障时间窗口一致，需要按事件路径追溯。
- 回到更具体的 specialist 深挖：
  - 问题已定位到特定专题但超出本模板深度（如 boot chain 分区策略、芯片厂商特定 memory alias/overlay 规则、DMA 专用区硬件约束）；
  - 需由对应 linker/toolchain/平台 specialist 输出专项结论，再回填本 review。
