# un9flow Template Generation

## 目标

将模板生成体系固定在 docs 真源层内，避免额外长出独立的 generation_system 层。`docs/TEMPLATE_GENERATION.md` 负责声明允许被生成的对象、输入最小集合、输出文件命名规则、生成器输入/输出责任、缺字段时的处理原则，以及单文件 / bundle 输出约定。

## 首批接入对象

- watchdog report（单文件）：`watchdog-timeout-audit-report`
- incident case bundle（bundle）：`incident case bundle`

## 后续预留对象

- `v6 example skeleton`：当前仅作为后续接入预留对象，不属于本轮首批接入，也不属于当前允许被生成的对象

## 允许被生成的对象

当前允许被生成的对象仅包括：
- `watchdog-timeout-audit-report`
- `incident case bundle`

`v6 example skeleton` 目前仍停留在后续预留对象；新增对象只有在本文件明确纳入后，才允许被生成。未在本文件声明的对象，不应由模板生成器擅自扩展接入。

## 输入最小集合

不同对象的输入可以不同，但生成器必须显式声明自己的输入最小集合，并保证输入命名可追溯。

- 对于 watchdog report，最小输入是 `findings`，可选补充输入是 `pack`；最小示例可理解为：一份 findings markdown，加上一份可选 pack 作为补充证据
- 对于 incident case bundle，最小输入是 `templates`、`case metadata`、`scenario`；最小示例可理解为：一组模板文件、一个 case metadata 条目、一个目标场景名
- 若对象还依赖额外输入，必须在对应生成器脚本顶部说明

生成器对象与生成约定仍受 `docs/CONSISTENCY_VALIDATION.md` 定义的现有 consistency / CI 门禁纳管；本轮先保证“可生成、可校验”链条闭合。更完整的输出回归（如 golden files / snapshot / output regression）仍留待后续补齐，不在本文件额外展开。

## 输出约定

### 单文件输出

- 单文件输出约定适用于 `watchdog-timeout-audit-report`
- 生成器应明确输出为一个 `report` 文件，而不是目录 bundle
- 输出内容应保持可审查、可归档、可回指输入来源

### bundle 输出

- bundle 输出约定适用于 `incident case bundle`
- 生成器应明确输出为一个 bundle 目录，内部文件顺序和命名应稳定
- bundle 内每个文件都应能追溯到模板来源与 case metadata

## 输出文件命名规则

- 单文件输出应使用目标对象语义稳定的文件名，例如：`watchdog-timeout-audit-report.md`
- bundle 输出应使用稳定的 bundle root 命名，并在 bundle 内保持固定文件顺序，例如：`docs/cases/generated/case-001/`
- 输出命名一旦进入真源，不应在脚本中随意漂移

## 缺字段时的处理原则

- 若缺少非关键字段，生成器应使用明确占位文本，而不是静默省略
- 若缺少关键输入字段，生成器应尽早失败或给出可定位的错误
- 不允许把缺字段默默解释成任意业务含义

## 生成器输入/输出责任

- 生成器必须声明自己服务的对象
- 生成器必须声明输入是什么、输出是什么
- 生成器必须声明输出属于单文件还是 bundle
- 生成器依赖 `tools/generation_core.py`
- 生成器遵循 `docs/TEMPLATE_GENERATION.md`
- 生成器只能做受约束的文本读取、字段替换与结果写出，不负责重新定义 docs 真源
