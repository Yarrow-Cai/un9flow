# incident-workflow-routing-regression

- 角色说明：本文件在统一校验体系中作为 incident workflow 的案例层回归基线，用于验证入口路由与辅助 skill 受控进入规则是否仍能解释真实任务。
- 规则来源：`docs/ORCHESTRATION.md`、`docs/INCIDENT_WORKFLOW.md`、`docs/DOMAIN_SPECIALIST_CONTRACTS.md`

## regression cases

### `INC-ROUTE-001`
- `user phrasing`: `这套 BMS 柜已经稳定运行三个月，最近开始偶发 isoSPI 掉线和 CRC 错误，帮我定位根因。`
- `incident context`: `yes`
- `evidence profile`: 已有运行期日志、CRC 错误计数、AFE 快照、reset reason 与当前安全态记录
- `route decision`: `incident-investigation`
- `route type`: `直进子入口`
- `why this route`: 系统原本可运行，当前目标是解释现象、缩小故障半径并定位根因。
- `why not others`: 不是首次 bringup；也不是纯设计评审任务。
- `expected next artifact`: `incident-summary`
- `expected next control signal`: `continue-current-route`

### `INC-ROUTE-002`
- `user phrasing`: `这个 incident 的日志、寄存器快照和波形描述太乱了，先帮我整理证据缺口再继续。`
- `incident context`: `yes`
- `evidence profile`: 已有零散日志、快照与实验备注，但时间窗与引用关系尚未归一
- `route decision`: `evidence-pack`
- `route type`: `辅助 skill 受控进入`
- `why this route`: 用户在 incident 语义上下文中显式要求先整理证据与补证据。
- `why not others`: `evidence-pack` 不能脱离 incident 语义单独作为全局主入口。
- `expected next artifact`: `evidence-package`
- `expected next control signal`: `fallback-for-more-evidence`

### `INC-ROUTE-003`
- `user phrasing`: `当前 diagnosis pack 已经形成，帮我做 second opinion，再决定这次 incident 能不能收口。`
- `incident context`: `yes`
- `evidence profile`: 已有 `incident-diagnosis-pack`、specialist 输出与当前风险边界说明
- `route decision`: `incident-review`
- `route type`: `辅助 skill 受控进入`
- `why this route`: 当前目标是进入 review gate 前复核证据链与结论链。
- `why not others`: `incident-review` 不替代 `design-safety-review`，也不应该重新承担主场景排查入口职责。
- `expected next artifact`: `incident-review-memo`
- `expected next control signal`: `enter-review-gate`

### `INC-ROUTE-004`
- `user phrasing`: `新板第一次联调就出现 AFE 掉线和 watchdog reset，先帮我判断该走 bringup 还是 incident。`
- `incident context`: `partial`
- `evidence profile`: 尚无稳定运行基线，场景信号同时指向 bringup 与 incident
- `route decision`: `orchestration`
- `route type`: `先走总入口`
- `why this route`: 当前请求跨场景且证据不足，必须先由总入口做主路由判定。
- `why not others`: 还不能直接直进 `incident-investigation` 或 `bringup-path`。
- `expected next artifact`: `routing-rationale`
- `expected next control signal`: `reroute-to-bringup-path`
