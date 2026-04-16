# orchestrator-dispatch-plan

## scenario
- 仅允许：`incident-investigation` / `bringup-path` / `design-safety-review`

## phase plan
- 可选值：`hazard-analysis` / `link-diagnostics` / `deterministic-foundation` / `failsafe-validation`

## dispatch items
- **item-1**
  - phase: 可选值：`hazard-analysis` / `link-diagnostics` / `deterministic-foundation` / `failsafe-validation`
  - specialist: 可选值：`signal-path-tracer` / `register-state-auditor` / `state-machine-tracer` / `timing-watchdog-auditor` / `failsafe-convergence-reviewer`
  - input artifacts / evidence:
  - dispatch reason:
  - expected output artifacts: 可选值：`segmented-failure-path` / `observability-point-list` / `path-suspicion-ranking` / `register-bitfield-map` / `register-anomaly-list` / `config-mismatch-note` / `state-transition-chain` / `stuck-state-list` / `safety-state-gap-note` / `timeout-watchdog-risk-table` / `isr-mainloop-conflict-note` / `timing-instability-hypothesis` / `failsafe-convergence-note` / `unsafe-persistence-risk` / `convergence-expectation-check`
  - exit condition or review gate:

## unresolved gaps
- 

## next control signal
- 可选值：`continue-current-route` / `fallback-for-more-evidence` / `fallback-route-assumption-invalid` / `fallback-specialist-explanation-failed` / `fallback-reorder-specialists` / `reroute-to-bringup-path` / `reroute-to-incident-investigation` / `upgrade-to-design-safety-review` / `upgrade-to-incident-investigation` / `enter-review-gate`
