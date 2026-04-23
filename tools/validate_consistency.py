from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import re
import sys


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


LEVEL_ORDER = ("L1", "L2", "L3")
LEVEL_NO_FINDINGS_MESSAGE = {
    "L1": "No blocking issues found.",
    "L2": "No important issues found.",
    "L3": "No cleanup issues found.",
}


@dataclass(frozen=True)
class Finding:
    level: str
    category: str
    file: str
    summary: str
    why_it_matters: str
    suggested_action: str


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SCENARIOS = (
    "incident-investigation",
    "bringup-path",
    "design-safety-review",
)
CANONICAL_PHASES = (
    "hazard-analysis",
    "link-diagnostics",
    "deterministic-foundation",
    "failsafe-validation",
)
CANONICAL_SPECIALISTS = (
    "signal-path-tracer",
    "register-state-auditor",
    "state-machine-tracer",
    "timing-watchdog-auditor",
    "failsafe-convergence-reviewer",
)
CANONICAL_SPECIALIST_SKILL_FILES = {
    "skills/signal-path-tracer/SKILL.md": "signal-path-tracer",
    "skills/register-state-auditor/SKILL.md": "register-state-auditor",
    "skills/state-machine-tracer/SKILL.md": "state-machine-tracer",
    "skills/timing-watchdog-auditor/SKILL.md": "timing-watchdog-auditor",
    "skills/failsafe-convergence-reviewer/SKILL.md": "failsafe-convergence-reviewer",
}


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _get_yaml_frontmatter_block(text: str) -> str | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index])
    return None


def _extract_frontmatter_keys(frontmatter_block: str) -> set[str]:
    keys: set[str] = set()
    for line in frontmatter_block.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        match = re.match(r"^([A-Za-z0-9_-]+)\s*:", stripped)
        if match is not None:
            keys.add(match.group(1))
    return keys


def _check_skill_frontmatter(label: str, content: str) -> list[Finding]:
    findings: list[Finding] = []
    frontmatter_block = _get_yaml_frontmatter_block(content)
    if frontmatter_block is None:
        findings.append(
            Finding(
                level="L1",
                category="skills",
                file=label,
                summary="SKILL.md 缺少 YAML frontmatter。",
                why_it_matters="宿主侧技能加载器会直接跳过缺少 frontmatter 的 skill 文件，导致正式 skill 不能被发现或使用。",
                suggested_action="在文件顶部补齐由 --- 包裹的 YAML frontmatter，至少声明 name 与 description。",
            )
        )
        return findings

    missing_keys = [
        key for key in ("name", "description") if key not in _extract_frontmatter_keys(frontmatter_block)
    ]
    if missing_keys:
        findings.append(
            Finding(
                level="L2",
                category="skills",
                file=label,
                summary=f"SKILL.md frontmatter 缺少字段：{', '.join(missing_keys)}。",
                why_it_matters="frontmatter 字段不完整会降低技能元数据的可发现性，也容易让不同宿主对 skill 的识别行为不一致。",
                suggested_action="为每个正式 SKILL.md 补齐最小 frontmatter 字段 name 与 description。",
            )
        )

    return findings


def _find_missing_semantics(
    text: str,
    requirements: dict[str, str | tuple[str, ...]],
) -> list[str]:
    missing: list[str] = []
    for semantic, candidates in requirements.items():
        candidate_values = (candidates,) if isinstance(candidates, str) else candidates
        if not any(candidate in text for candidate in candidate_values):
            missing.append(semantic)
    return missing


def is_incident_orchestrator_scoped(text: str) -> bool:
    anchor = "incident-orchestrator"
    lines = text.splitlines()
    all_anchor_line_indexes = [index for index, line in enumerate(lines) if anchor in line]
    if not all_anchor_line_indexes:
        return True

    tightening_keywords = (
        "示例",
        "模板",
        "仅承担",
        "仅作",
        "仅为",
        "只对应",
        "仅是",
        "仅用于",
        "仅限",
    )
    meta_description_keywords = (
        "定义",
        "规则",
        "职责边界",
        "检查",
        "运行",
        "补齐",
        "修改",
        "创建",
        "实现",
    )
    definition_predicate_pattern = re.compile(
        rf"(?:`?{re.escape(anchor)}`?[^。\n，,；;:：]{{0,24}}(?:是|为|作为|仅作|仅为|仅用于|仅限|仅承担|只作|只用于|负责|属于|仅是|只对应)|(?:是|为|作为|仅作|仅为|仅用于|仅限|仅承担|只作|只用于|负责|属于|仅是|只对应)[^。\n，,；;:：]{{0,24}}`?{re.escape(anchor)}`?)"
    )

    def has_scenario_scope(local_block: str) -> bool:
        return any(
            keyword in local_block
            for keyword in ("场景内", "incident-investigation", "incident 场景", "incident场景")
        )

    def has_restricted_role(local_block: str) -> bool:
        return any(keyword in local_block for keyword in tightening_keywords)

    def is_inside_fenced_code(line_index: int) -> bool:
        fence_count = 0
        for prior_line in lines[:line_index]:
            if prior_line.strip().startswith("```"):
                fence_count += 1
        return fence_count % 2 == 1

    def is_command_example_line(stripped: str) -> bool:
        lowered = stripped.lower()
        return (
            lowered.startswith("run:")
            or lowered.startswith("expected:")
            or lowered.startswith("python ")
            or lowered.startswith("grep ")
            or re.fullmatch(r"`[^`].*`", stripped) is not None
        )

    def is_flow_diagram_line(stripped: str) -> bool:
        if "->" not in stripped:
            return False
        return (
            re.fullmatch(
                r"[A-Za-z0-9_\-\u4e00-\u9fff`|:：./()\s]+(?:->[A-Za-z0-9_\-\u4e00-\u9fff`|:：./()\s]+)+",
                stripped,
            )
            is not None
        )

    def is_definition_candidate_line(line: str) -> bool:
        stripped = line.strip()
        if not stripped or stripped.startswith("```"):
            return False
        if is_command_example_line(stripped):
            return False
        if is_flow_diagram_line(stripped):
            return False
        return True

    def is_block_boundary(line: str) -> bool:
        stripped = line.strip()
        return not stripped or stripped.startswith("#")

    def is_local_block_hard_stop_line(line: str) -> bool:
        stripped = line.strip()
        return is_command_example_line(stripped) or is_flow_diagram_line(stripped)

    def get_list_indent(line: str) -> int | None:
        list_item_match = re.match(r"^(\s*)(?:[-*+]|\d+[.)])\s+", line)
        if not list_item_match:
            return None
        return len(list_item_match.group(1))

    def strip_list_marker(stripped: str) -> str:
        return re.sub(r"^(?:[-*+]|\d+[.)])\s+", "", stripped, count=1)

    def normalize_listing_text(text: str) -> str:
        without_links = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        return without_links.replace("`", "").strip()

    def is_name_listing_text(text: str) -> bool:
        normalized = normalize_listing_text(text)
        if not normalized:
            return False
        if ":" in normalized or "：" in normalized:
            return False

        tokens = [token.strip() for token in re.split(r"[,，、/|]", normalized) if token.strip()]
        if not tokens:
            return False

        for token in tokens:
            if token.lower() in {"and", "or"}:
                continue
            if not re.fullmatch(r"[A-Za-z0-9_.\-/]+", token):
                return False
        return True

    def has_definition_predicate(text: str) -> bool:
        return definition_predicate_pattern.search(text) is not None

    def is_meta_description_line(text: str) -> bool:
        return any(keyword in text for keyword in meta_description_keywords)

    def is_heading_or_section_label_line(stripped: str) -> bool:
        return stripped.startswith("#") and anchor in stripped

    def is_heading_definition_anchor_line(stripped: str) -> bool:
        if not is_heading_or_section_label_line(stripped):
            return False

        heading_text = re.sub(r"^#+\s*", "", stripped).replace("`", "").strip()
        lowered = heading_text.lower()
        if anchor not in lowered:
            return False

        # 章节标题经常只是目录标签；没有本地定义性谓词时不应单独触发定义判定。
        return has_definition_predicate(heading_text)

    def is_process_plan_meta_mention_line(stripped: str) -> bool:
        normalized = strip_list_marker(stripped)
        return (
            re.search(
                rf"定义\s*`?{re.escape(anchor)}`?\s*(?:职责边界|的\s*调度规则)",
                normalized,
            )
            is not None
            or re.search(
                rf"`?{re.escape(anchor)}`?\s*的\s*(?:职责边界|调度规则)",
                normalized,
            )
            is not None
        )

    def is_flow_reference_mention_line(stripped: str) -> bool:
        normalized = strip_list_marker(stripped)
        return "->" in normalized and anchor in normalized

    def is_non_heading_definition_anchor_line(stripped: str) -> bool:
        if stripped.startswith("#"):
            return False
        if is_meta_description_line(stripped) and not has_definition_predicate(stripped):
            return False
        return has_definition_predicate(stripped)

    def is_definition_anchor_line(line: str) -> bool:
        if anchor not in line:
            return False

        stripped = line.strip()
        if not is_definition_candidate_line(line):
            return False
        if is_heading_or_section_label_line(stripped):
            return is_heading_definition_anchor_line(stripped)
        if is_process_plan_meta_mention_line(stripped):
            return False
        if is_flow_reference_mention_line(stripped):
            return False
        return is_non_heading_definition_anchor_line(stripped)

    anchor_line_indexes = [
        index
        for index in all_anchor_line_indexes
        if not is_inside_fenced_code(index) and is_definition_anchor_line(lines[index])
    ]
    if not anchor_line_indexes:
        return True

    for anchor_line_index in anchor_line_indexes:
        local_lines: list[str] = []
        anchor_line = lines[anchor_line_index]
        local_lines.append(anchor_line)
        anchor_list_indent = get_list_indent(anchor_line)

        for next_index in range(anchor_line_index + 1, len(lines)):
            next_line = lines[next_index]
            if is_block_boundary(next_line):
                break
            if anchor in next_line:
                break

            next_list_indent = get_list_indent(next_line)
            if (
                anchor_list_indent is not None
                and next_list_indent is not None
                and next_list_indent == anchor_list_indent
            ):
                break

            if is_inside_fenced_code(next_index):
                continue
            if is_local_block_hard_stop_line(next_line):
                break
            if is_definition_candidate_line(next_line):
                local_lines.append(next_line)

        local_block = "\n".join(local_lines)
        if not local_block.strip():
            continue

        is_scoped = has_scenario_scope(local_block) and has_restricted_role(local_block)
        if not is_scoped:
            return False

    return True


def check_docs() -> list[Finding]:
    findings: list[Finding] = []

    primary_truth_docs = (
        "docs/ORCHESTRATION.md",
        "docs/INCIDENT_WORKFLOW.md",
        "docs/DESIGN_SAFETY_REVIEW.md",
        "docs/SKILL_ARCHITECTURE.md",
        "docs/ORCHESTRATOR_PROMPT_CONTRACT.md",
        "docs/DOMAIN_SPECIALIST_CONTRACTS.md",
        "docs/CONSISTENCY_VALIDATION.md",
    )
    constrained_docs = (
        "README.md",
        "docs/ROADMAP.md",
        "docs/WORKFLOW.md",
        "docs/PLATFORMS.md",
        "docs/WATCHDOG_TIMEOUT_AUDIT.md",
        "docs/REGISTER_STATE_AUDIT.md",
    )

    docs_content: dict[str, str] = {}

    for doc in primary_truth_docs:
        content = _read_text(ROOT / Path(doc))
        if content is None:
            findings.append(
                Finding(
                    level="L1",
                    category="docs",
                    file=doc,
                    summary="主真源 docs 文件缺失或无法读取。",
                    why_it_matters="主真源不可读会让 docs scope 的一致性校验失去可信依据。",
                    suggested_action=f"恢复 {doc} 并确保 UTF-8 可读。",
                )
            )
            continue
        docs_content[doc] = content

    for doc in constrained_docs:
        content = _read_text(ROOT / Path(doc))
        if content is None:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=doc,
                    summary="受约束 docs 文件缺失或无法读取。",
                    why_it_matters="受约束 docs 不可读会降低 docs scope 的边界一致性可审查性。",
                    suggested_action=f"恢复 {doc} 并确保 UTF-8 可读。",
                )
            )
            continue
        docs_content[doc] = content

    orchestration_label = "docs/ORCHESTRATION.md"
    orchestration_content = docs_content.get(orchestration_label)
    if orchestration_content is not None:
        for keyword in ("Scenario", "Phase", "Domain Specialist", "Artifact"):
            if keyword not in orchestration_content:
                findings.append(
                    Finding(
                        level="L1",
                        category="docs",
                        file=orchestration_label,
                        summary=f"缺少关键术语：{keyword}。",
                        why_it_matters="对象层级命名不完整会破坏总调度规则的可判定性。",
                        suggested_action="补齐 Scenario / Phase / Domain Specialist / Artifact 的明确表述。",
                    )
                )

        if not is_incident_orchestrator_scoped(orchestration_content):
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=orchestration_label,
                    summary="incident-orchestrator 未被约束为场景内调度器示例。",
                    why_it_matters="未限定语义会误导为全局总路由名，造成边界越权。",
                    suggested_action="在同一文档中明确其仅为场景内调度器示例。",
                )
            )

        if "docs/ORCHESTRATOR_PROMPT_CONTRACT.md" not in orchestration_content:
            findings.append(
                Finding(
                    level="L1",
                    category="docs",
                    file=orchestration_label,
                    summary="缺少对 ORCHESTRATOR_PROMPT_CONTRACT 的回指。",
                    why_it_matters="总调度规则与 prompt 契约无法建立双文档锚点，容易出现双重真源。",
                    suggested_action="在 ORCHESTRATION.md 中加入对 docs/ORCHESTRATOR_PROMPT_CONTRACT.md 的引用。",
                )
            )
        if "docs/DOMAIN_SPECIALIST_CONTRACTS.md" not in orchestration_content:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=orchestration_label,
                    summary="缺少对 DOMAIN_SPECIALIST_CONTRACTS 的回指。",
                    why_it_matters="如果总调度规则不回指 specialist 契约真源，specialist 分派与 specialist 内部输入输出协议就容易漂移。",
                    suggested_action="在 ORCHESTRATION.md 中加入对 docs/DOMAIN_SPECIALIST_CONTRACTS.md 的引用。",
                )
            )

    readme_label = "README.md"
    readme_content = docs_content.get(readme_label)
    if readme_content is not None and "docs/CONSISTENCY_VALIDATION.md" not in readme_content:
        findings.append(
            Finding(
                level="L2",
                category="docs",
                file=readme_label,
                summary="缺少 docs/CONSISTENCY_VALIDATION.md 的入口引用。",
                why_it_matters="README 缺少入口引用会增加一致性校验规范的发现成本。",
                suggested_action="在 README.md 中加入 docs/CONSISTENCY_VALIDATION.md 的入口链接。",
            )
        )
    if readme_content is not None and "docs/DOMAIN_SPECIALIST_CONTRACTS.md" not in readme_content:
        findings.append(
            Finding(
                level="L2",
                category="docs",
                file=readme_label,
                summary="缺少 docs/DOMAIN_SPECIALIST_CONTRACTS.md 的入口引用。",
                why_it_matters="README 若缺少 specialist 契约真源入口，使用者就很难快速发现 Domain Specialist 的稳定输入输出边界。",
                suggested_action="在 README.md 中加入 docs/DOMAIN_SPECIALIST_CONTRACTS.md 的入口链接。",
            )
        )
    if readme_content is not None and "docs/REGISTER_STATE_AUDIT.md" not in readme_content:
        findings.append(
            Finding(
                level="L2",
                category="docs",
                file=readme_label,
                summary="缺少 docs/REGISTER_STATE_AUDIT.md 的入口引用。",
                why_it_matters="README 若缺少 register 方法真源入口，使用者就难以快速定位 register-state-auditor 的规范来源。",
                suggested_action="在 README.md 中加入 docs/REGISTER_STATE_AUDIT.md 的入口链接。",
            )
        )

    roadmap_label = "docs/ROADMAP.md"
    roadmap_content = docs_content.get(roadmap_label)
    if roadmap_content is not None:
        has_consistency_validation_ref = "docs/CONSISTENCY_VALIDATION.md" in roadmap_content
        has_validation_template_anchor = (
            "validation-findings" in roadmap_content
            or "consistency-review-checklist" in roadmap_content
        )
        if not (has_consistency_validation_ref or has_validation_template_anchor):
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=roadmap_label,
                    summary="缺少一致性校验文档或 validation 模板锚点引用。",
                    why_it_matters="ROADMAP 无校验锚点会削弱路线图与一致性治理流程的对齐。",
                    suggested_action="在 docs/ROADMAP.md 中加入 docs/CONSISTENCY_VALIDATION.md 或 validation 模板锚点引用。",
                )
            )

    consistency_validation_label = "docs/CONSISTENCY_VALIDATION.md"
    consistency_validation_content = docs_content.get(consistency_validation_label)
    if consistency_validation_content is not None:
        if "docs 真源层" not in consistency_validation_content:
            findings.append(
                Finding(
                    level="L1",
                    category="docs",
                    file=consistency_validation_label,
                    summary="缺少“docs 真源层”锚点。",
                    why_it_matters="一致性规范若缺失真源层锚点，会导致 docs scope 判定基准不稳定。",
                    suggested_action="在 docs/CONSISTENCY_VALIDATION.md 中补充“docs 真源层”表述。",
                )
            )
        if not all(level in consistency_validation_content for level in LEVEL_ORDER):
            findings.append(
                Finding(
                    level="L1",
                    category="docs",
                    file=consistency_validation_label,
                    summary="缺少 L1/L2/L3 分级锚点。",
                    why_it_matters="未声明完整分级集合会削弱一致性校验结果的可对齐性。",
                    suggested_action="在 docs/CONSISTENCY_VALIDATION.md 中补齐 L1 / L2 / L3 明确表述。",
                )
            )
        if "docs/DOMAIN_SPECIALIST_CONTRACTS.md" not in consistency_validation_content:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=consistency_validation_label,
                    summary="docs 真源层缺少 DOMAIN_SPECIALIST_CONTRACTS 锚点。",
                    why_it_matters="若一致性校验基线不把 specialist 契约真源纳入 docs 层，specialist 输入输出规则就会游离在校验范围之外。",
                    suggested_action="在 docs/CONSISTENCY_VALIDATION.md 中把 docs/DOMAIN_SPECIALIST_CONTRACTS.md 纳入 docs 真源层。",
                )
            )

    prompt_contract_label = "docs/ORCHESTRATOR_PROMPT_CONTRACT.md"
    prompt_contract_content = docs_content.get(prompt_contract_label)
    if prompt_contract_content is not None:
        missing_prompt_semantics = _find_missing_semantics(
            prompt_contract_content,
            {
                "Scenario layer": ("primary_scenario", "Scenario"),
                "Phase layer": ("Phase Plan", "phase"),
                "Domain Specialist layer": ("Dispatch Plan", "specialist"),
                "Artifact layer": ("expected artifacts", "expected_artifacts", "Artifact"),
            },
        )
        if missing_prompt_semantics:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=prompt_contract_label,
                    summary=f"prompt contract 缺少命名层锚点：{', '.join(missing_prompt_semantics)}。",
                    why_it_matters="若 prompt 契约不能稳定承载 Scenario / Phase / Domain Specialist / Artifact 层，后续 prompt 与 skill 边界就容易重新混层。",
                    suggested_action="在 ORCHESTRATOR_PROMPT_CONTRACT.md 中补齐四层命名对应的输入输出锚点。",
                )
            )
        missing_prompt_contract_anchors = _find_missing_semantics(
            prompt_contract_content,
            {
                "protocol positioning": "## 调度协议定位",
                "host binding preconditions": "## host 侧 prompt 绑定前置约束",
                "routing result": "### Routing Result",
                "phase plan": "### Phase Plan",
                "dispatch plan": "### Dispatch Plan",
                "control result": "### Control Result",
            },
        )
        if missing_prompt_contract_anchors:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=prompt_contract_label,
                    summary=f"prompt contract 缺少协议锚点：{', '.join(missing_prompt_contract_anchors)}。",
                    why_it_matters="若调度协议文档没有显式声明协议定位与 host 绑定前置约束，后续 host 接入时就容易重新发明字段或控制信号。",
                    suggested_action="在 ORCHESTRATOR_PROMPT_CONTRACT.md 中补齐调度协议定位、host 侧 prompt 绑定前置约束，以及四段输出协议标题。",
                )
            )

    skill_architecture_label = "docs/SKILL_ARCHITECTURE.md"
    skill_architecture_content = docs_content.get(skill_architecture_label)
    if skill_architecture_content is not None:
        missing_skill_architecture_semantics = _find_missing_semantics(
            skill_architecture_content,
            {
                "entry positioning": "## 入口规范定位",
                "entry boundary matrix": "## 入口边界矩阵",
                "protocol split": "## 与调度协议的分工",
                "orchestration entry": "总入口 / orchestration",
                "sub-entry boundary": "三子入口 / 场景入口",
                "auxiliary boundary": "辅助 skill",
                "specialist boundary": "Domain Specialist",
                "prompt contract ref": "docs/ORCHESTRATOR_PROMPT_CONTRACT.md",
            },
        )
        if missing_skill_architecture_semantics:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=skill_architecture_label,
                    summary=f"skill architecture 缺少入口规范锚点：{', '.join(missing_skill_architecture_semantics)}。",
                    why_it_matters="若入口规范文档没有显式声明总入口 / 子入口 / 辅助 skill / specialist 的边界矩阵，正式 SKILL.md 的前置入口规范就无法被稳定复核。",
                    suggested_action="在 docs/SKILL_ARCHITECTURE.md 中补齐入口规范定位、入口边界矩阵与与调度协议的分工段落。",
                )
            )

    workflow_label = "docs/WORKFLOW.md"
    workflow_content = docs_content.get(workflow_label)
    if workflow_content is not None:
        missing_workflow_refs = _find_missing_semantics(
            workflow_content,
            {
                "incident workflow ref": "docs/INCIDENT_WORKFLOW.md",
                "domain specialist contracts ref": "docs/DOMAIN_SPECIALIST_CONTRACTS.md",
            },
        )
        if missing_workflow_refs:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=workflow_label,
                    summary=f"WORKFLOW 缺少真源回指：{', '.join(missing_workflow_refs)}。",
                    why_it_matters="WORKFLOW 作为方法入口文档，若不回指 incident 真源与 specialist 契约真源，就容易重新长出第二套边界口径。",
                    suggested_action="在 docs/WORKFLOW.md 中加入对 docs/INCIDENT_WORKFLOW.md 与 docs/DOMAIN_SPECIALIST_CONTRACTS.md 的引用。",
                )
            )

    platforms_label = "docs/PLATFORMS.md"
    platforms_content = docs_content.get(platforms_label)
    if platforms_content is not None:
        missing_platform_alignment_semantics = _find_missing_semantics(
            platforms_content,
            {
                "workflow orchestration alignment": "workflow orchestration 思路",
                "Claude Code / skill entry alignment": "Claude Code / skill 入口习惯",
                "directory organization alignment": "后续目录组织方式",
                "orchestration ref": "docs/ORCHESTRATION.md",
                "incident workflow ref": "docs/INCIDENT_WORKFLOW.md",
            },
        )
        if missing_platform_alignment_semantics:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=platforms_label,
                    summary=f"PLATFORMS 缺少 host 对齐锚点：{', '.join(missing_platform_alignment_semantics)}。",
                    why_it_matters="平台说明文档若没有固定第一阶段 host 对齐层与总调度 / 场景真源回指，就容易把 host 接入扩张成另一套入口规则。",
                    suggested_action="在 docs/PLATFORMS.md 中补齐 workflow orchestration、Claude Code / skill 入口习惯、后续目录组织方式，以及 ORCHESTRATION / INCIDENT_WORKFLOW 双真源回指。",
                )
            )

        has_gstack_boundary = (
            "gstack-compatible first" in platforms_content
            and "不承诺现阶段具备安装器、分发、目录映射或广泛 host 兼容能力" in platforms_content
        )
        if not has_gstack_boundary:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=platforms_label,
                    summary="PLATFORMS 缺少 gstack-compatible first 非承诺边界声明。",
                    why_it_matters="若平台文档只写兼容方向、不写非承诺边界，host 接入范围就会被误解为已经覆盖安装、分发与广泛兼容能力。",
                    suggested_action="在 docs/PLATFORMS.md 中明确 gstack-compatible first 仅指对齐层，并补齐不承诺安装器、分发、目录映射或广泛 host 兼容能力的声明。",
                )
            )

        has_openclaw_placeholder = "OpenClaw 作为外层调度预留位" in platforms_content
        if not has_openclaw_placeholder:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=platforms_label,
                    summary="PLATFORMS 缺少 OpenClaw 外层调度预留位声明。",
                    why_it_matters="若平台文档没有把 OpenClaw 固定为预留位，后续 host 优先级与外层调度边界就会重新漂移。",
                    suggested_action="在 docs/PLATFORMS.md 中补充 OpenClaw 作为外层调度预留位的明确表述。",
                )
            )

    incident_workflow_label = "docs/INCIDENT_WORKFLOW.md"
    incident_workflow_content = docs_content.get(incident_workflow_label)
    if incident_workflow_content is not None:
        missing_incident_boundary_semantics = _find_missing_semantics(
            incident_workflow_content,
            {
                "incident pipeline boundary section": "incident pipeline 输入输出边界",
                "domain specialist contracts ref": "docs/DOMAIN_SPECIALIST_CONTRACTS.md",
            },
        )
        if missing_incident_boundary_semantics:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=incident_workflow_label,
                    summary=f"incident workflow 缺少边界锚点：{', '.join(missing_incident_boundary_semantics)}。",
                    why_it_matters="若 incident 场景文档没有固定 incident pipeline 交接边界，skill、specialist 与 Artifact 角色就会重新混层。",
                    suggested_action="在 docs/INCIDENT_WORKFLOW.md 中加入 incident pipeline 输入输出边界章节，并回指 docs/DOMAIN_SPECIALIST_CONTRACTS.md。",
                )
            )

        has_skill_artifact_boundary = (
            "`skill` 名称不等于 `Artifact` 名称" in incident_workflow_content
            or "skill 名称不等于 `Artifact` 名称" in incident_workflow_content
            or "skill 名称不等于 Artifact 名称" in incident_workflow_content
        )
        if not has_skill_artifact_boundary:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=incident_workflow_label,
                    summary="incident workflow 缺少 skill / Artifact 分层声明。",
                    why_it_matters="若不显式禁止把 skill 名称与 Artifact 名称混用，incident pipeline 输入输出边界就无法稳定复核。",
                    suggested_action="在 docs/INCIDENT_WORKFLOW.md 中明确声明 skill 名称不等于 Artifact 名称。",
                )
            )

        has_specialist_handoff_boundary = (
            "只消费 `incident-orchestrator` 交付" in incident_workflow_content
            or "回交给 `incident-orchestrator`" in incident_workflow_content
        )
        if not has_specialist_handoff_boundary:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=incident_workflow_label,
                    summary="incident workflow 缺少 specialist 回交边界声明。",
                    why_it_matters="specialist 若没有被约束为消费 dispatch 上下文并回交给 incident-orchestrator，就容易越级篡改场景路由或辅助 skill 角色。",
                    suggested_action="在 docs/INCIDENT_WORKFLOW.md 中明确 specialist 只消费 incident-orchestrator 交付，并在需要补证据或换轨时回交给 incident-orchestrator。",
                )
            )

    design_safety_label = "docs/DESIGN_SAFETY_REVIEW.md"
    design_safety_content = docs_content.get(design_safety_label)
    if design_safety_content is not None:
        missing_design_safety_semantics = _find_missing_semantics(
            design_safety_content,
            {
                "entry boundary section": "## 进入边界与换轨",
                "phase backbone section": "## 默认 Phase 骨架",
                "specialist dispatch section": "## 默认 specialist 装配",
                "artifact alignment section": "## 主 Artifact 与 specialist 输出对齐",
                "review gate section": "## Review Gate",
                "watchdog timeout audit ref": "docs/WATCHDOG_TIMEOUT_AUDIT.md",
                "domain specialist contracts ref": "docs/DOMAIN_SPECIALIST_CONTRACTS.md",
                "orchestration ref": "docs/ORCHESTRATION.md",
                "prompt contract ref": "docs/ORCHESTRATOR_PROMPT_CONTRACT.md",
            },
        )
        if missing_design_safety_semantics:
            findings.append(
                Finding(
                    level="L1",
                    category="docs",
                    file=design_safety_label,
                    summary=f"design-safety-review 真源缺少关键结构锚点：{', '.join(missing_design_safety_semantics)}。",
                    why_it_matters="若 design-safety-review 没有独立场景真源，功能安全复核仍会停留在 skill 描述层，无法稳定复核 phase / specialist / Artifact 对齐关系。",
                    suggested_action="在 docs/DESIGN_SAFETY_REVIEW.md 中补齐进入边界、Phase、specialist、Artifact 对齐、Review Gate 以及对上游真源与 watchdog 专项方法的引用。",
                )
            )

        missing_design_safety_artifacts = [
            artifact
            for artifact in (
                "design-review-summary",
                "risk-boundary-note",
                "convergence-strategy-review",
                "failsafe-check-matrix",
            )
            if artifact not in design_safety_content
        ]
        if missing_design_safety_artifacts:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=design_safety_label,
                    summary=f"design-safety-review 真源缺少主 Artifact：{', '.join(missing_design_safety_artifacts)}。",
                    why_it_matters="若场景真源不固定 design-time safety review 的主 Artifact，specialist 输出就无法稳定回交到统一复核载体。",
                    suggested_action="在 docs/DESIGN_SAFETY_REVIEW.md 中补齐 design-review-summary、risk-boundary-note、convergence-strategy-review 与 failsafe-check-matrix。",
                )
            )

        missing_design_safety_specialists = [
            specialist
            for specialist in (
                "signal-path-tracer",
                "state-machine-tracer",
                "register-state-auditor",
                "failsafe-convergence-reviewer",
                "timing-watchdog-auditor",
            )
            if specialist not in design_safety_content
        ]
        if missing_design_safety_specialists:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=design_safety_label,
                    summary=f"design-safety-review 真源缺少默认 specialist 锚点：{', '.join(missing_design_safety_specialists)}。",
                    why_it_matters="若设计安全复核真源不固定默认 specialist 装配，功能安全 review 的 phase / specialist 对齐就会退化为口头约定。",
                    suggested_action="在 docs/DESIGN_SAFETY_REVIEW.md 中补齐默认 specialist 装配与 phase 对应关系。",
                )
            )

    watchdog_timeout_label = "docs/WATCHDOG_TIMEOUT_AUDIT.md"
    watchdog_timeout_content = docs_content.get(watchdog_timeout_label)
    if watchdog_timeout_content is not None:
        missing_watchdog_timeout_refs = _find_missing_semantics(
            watchdog_timeout_content,
            {
                "domain specialist contracts ref": "docs/DOMAIN_SPECIALIST_CONTRACTS.md",
                "main scenario ref": "docs/DESIGN_SAFETY_REVIEW.md",
                "watchdog template ref": "docs/templates/timing-watchdog-audit-pack.md",
            },
        )
        if missing_watchdog_timeout_refs:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=watchdog_timeout_label,
                    summary=f"watchdog 专项方法真源缺少必要回指：{', '.join(missing_watchdog_timeout_refs)}。",
                    why_it_matters="方法真源若不回指 specialist 契约、主场景与对应模板，docs/skills/templates 三层映射就无法形成闭环。",
                    suggested_action="在 docs/WATCHDOG_TIMEOUT_AUDIT.md 中补齐对 DOMAIN_SPECIALIST_CONTRACTS、DESIGN_SAFETY_REVIEW 与 timing-watchdog-audit-pack 模板的引用。",
                )
            )

        missing_watchdog_formal_refs = _find_missing_semantics(
            watchdog_timeout_content,
            {
                "watchdog formal skill ref": "skills/watchdog-timeout-audit/SKILL.md",
                "watchdog findings template ref": "docs/templates/watchdog-timeout-audit-findings.md",
                "watchdog report template ref": "docs/templates/watchdog-timeout-audit-report.md",
            },
        )
        if missing_watchdog_formal_refs:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=watchdog_timeout_label,
                    summary=f"watchdog 专项方法真源缺少 formal skill / findings / report 回指：{', '.join(missing_watchdog_formal_refs)}。",
                    why_it_matters="若方法真源不回指 formal skill、findings 模板与最终 report 模板，watchdog 专项入口与结果收口对象将无法形成闭环映射。",
                    suggested_action="在 docs/WATCHDOG_TIMEOUT_AUDIT.md 中补齐对 skills/watchdog-timeout-audit/SKILL.md、docs/templates/watchdog-timeout-audit-findings.md 与 docs/templates/watchdog-timeout-audit-report.md 的引用。",
                )
            )

        if "tools/generate_watchdog_timeout_audit_report.py" not in watchdog_timeout_content:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=watchdog_timeout_label,
                    summary="watchdog 专项方法真源缺少自动报告生成器脚本回指。",
                    why_it_matters="若方法真源不回指 watchdog 报告生成器脚本，watchdog findings/pack 到最终报告输出链路就无法在 docs 层形成闭环映射。",
                    suggested_action="在 docs/WATCHDOG_TIMEOUT_AUDIT.md 中补充 tools/generate_watchdog_timeout_audit_report.py 的引用。",
                )
            )

        if "ISR / main loop 职责冲突" not in watchdog_timeout_content:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=watchdog_timeout_label,
                    summary="watchdog 专项方法真源缺少 ISR / main loop 职责冲突专项说明。",
                    why_it_matters="若方法真源未显式覆盖 ISR / main loop 职责冲突，isr-mainloop-conflict-note 的归属边界就无法被稳定审计。",
                    suggested_action="在 docs/WATCHDOG_TIMEOUT_AUDIT.md 中补充 ISR / main loop 职责冲突专项说明，并与 timing-watchdog-auditor 的 canonical Artifact 保持一致。",
                )
            )

    register_state_label = "docs/REGISTER_STATE_AUDIT.md"
    register_state_content = docs_content.get(register_state_label)
    if register_state_content is not None:
        missing_register_state_refs = _find_missing_semantics(
            register_state_content,
            {
                "domain specialist contracts ref": "docs/DOMAIN_SPECIALIST_CONTRACTS.md",
                "incident workflow ref": "docs/INCIDENT_WORKFLOW.md",
                "design safety review ref": "docs/DESIGN_SAFETY_REVIEW.md",
                "register template ref": "docs/templates/register-state-audit-pack.md",
            },
        )
        if missing_register_state_refs:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=register_state_label,
                    summary=f"register 专项方法真源缺少必要回指：{', '.join(missing_register_state_refs)}。",
                    why_it_matters="方法真源若不回指 specialist 契约、主场景与对应模板，docs/skills/templates 三层映射就无法形成闭环。",
                    suggested_action="在 docs/REGISTER_STATE_AUDIT.md 中补齐对 DOMAIN_SPECIALIST_CONTRACTS、INCIDENT_WORKFLOW、DESIGN_SAFETY_REVIEW 与 register-state-audit-pack 模板的引用。",
                )
            )

    domain_contracts_label = "docs/DOMAIN_SPECIALIST_CONTRACTS.md"
    domain_contracts_content = docs_content.get(domain_contracts_label)
    if domain_contracts_content is not None:
        missing_contract_semantics = _find_missing_semantics(
            domain_contracts_content,
            {
                "uniform contract rules": "## 统一契约规则",
                "input contract": "#### 输入契约",
                "output artifact": "#### 输出 Artifact",
                "not-responsible section": "#### 不负责什么",
                "handoff conditions": "#### 回交条件",
            },
        )
        if missing_contract_semantics:
            findings.append(
                Finding(
                    level="L1",
                    category="docs",
                    file=domain_contracts_label,
                    summary=f"Domain Specialist 契约真源缺少结构锚点：{', '.join(missing_contract_semantics)}。",
                    why_it_matters="如果 specialist 契约真源缺少统一结构，输入 / 输出 / 禁止项与回交流程就无法被稳定判定。",
                    suggested_action="在 docs/DOMAIN_SPECIALIST_CONTRACTS.md 中补齐统一契约规则、输入契约、输出 Artifact、不负责什么与回交条件结构。",
                )
            )

        missing_specialists = [
            specialist for specialist in CANONICAL_SPECIALISTS if specialist not in domain_contracts_content
        ]
        if missing_specialists:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=domain_contracts_label,
                    summary=f"Domain Specialist 契约真源未覆盖全部 canonical specialist：{', '.join(missing_specialists)}。",
                    why_it_matters="若 specialist 真源未覆盖完整 canonical 集合，不同场景与模板中的 specialist 命名就会失去统一基线。",
                    suggested_action="在 docs/DOMAIN_SPECIALIST_CONTRACTS.md 中补齐全部 canonical specialist 的契约条目。",
                )
            )

        missing_domain_contract_refs = _find_missing_semantics(
            domain_contracts_content,
            {
                "orchestration ref": "docs/ORCHESTRATION.md",
                "prompt contract ref": "docs/ORCHESTRATOR_PROMPT_CONTRACT.md",
                "incident workflow ref": "docs/INCIDENT_WORKFLOW.md",
            },
        )
        if missing_domain_contract_refs:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=domain_contracts_label,
                    summary=f"Domain Specialist 契约真源缺少上游回指：{', '.join(missing_domain_contract_refs)}。",
                    why_it_matters="specialist 真源若不回指总调度、prompt 契约与 incident 场景边界，文档层之间就无法形成闭环。",
                    suggested_action="在 docs/DOMAIN_SPECIALIST_CONTRACTS.md 中加入对 ORCHESTRATION、ORCHESTRATOR_PROMPT_CONTRACT 与 INCIDENT_WORKFLOW 的引用。",
                )
            )

        has_isr_ownership = (
            "isr-mainloop-conflict-note" in domain_contracts_content
            and "timing-watchdog-auditor" in domain_contracts_content
            and "不得拆成新的 specialist" in domain_contracts_content
        )
        if not has_isr_ownership:
            findings.append(
                Finding(
                    level="L2",
                    category="docs",
                    file=domain_contracts_label,
                    summary="Domain Specialist 契约真源缺少 ISR 归属不拆分声明。",
                    why_it_matters="若 contracts 未同时声明 isr-mainloop-conflict-note 归属 timing-watchdog-auditor 且不得拆分为新 specialist，specialist 边界会在后续扩展中漂移。",
                    suggested_action="在 docs/DOMAIN_SPECIALIST_CONTRACTS.md 中明确 isr-mainloop-conflict-note 归属 timing-watchdog-auditor，且不得拆成新的 specialist。",
                )
            )

    return findings


def check_skills() -> list[Finding]:
    findings: list[Finding] = []
    skill_contents: dict[str, str] = {}

    skill_files = {
        "skills/orchestration/SKILL.md": ROOT / "skills" / "orchestration" / "SKILL.md",
        "skills/incident-investigation/SKILL.md": ROOT / "skills" / "incident-investigation" / "SKILL.md",
        "skills/bringup-path/SKILL.md": ROOT / "skills" / "bringup-path" / "SKILL.md",
        "skills/design-safety-review/SKILL.md": ROOT / "skills" / "design-safety-review" / "SKILL.md",
        "skills/evidence-pack/SKILL.md": ROOT / "skills" / "evidence-pack" / "SKILL.md",
        "skills/incident-review/SKILL.md": ROOT / "skills" / "incident-review" / "SKILL.md",
        "skills/signal-path-tracer/SKILL.md": ROOT / "skills" / "signal-path-tracer" / "SKILL.md",
        "skills/register-state-auditor/SKILL.md": ROOT / "skills" / "register-state-auditor" / "SKILL.md",
        "skills/state-machine-tracer/SKILL.md": ROOT / "skills" / "state-machine-tracer" / "SKILL.md",
        "skills/timing-watchdog-auditor/SKILL.md": ROOT / "skills" / "timing-watchdog-auditor" / "SKILL.md",
        "skills/failsafe-convergence-reviewer/SKILL.md": ROOT / "skills" / "failsafe-convergence-reviewer" / "SKILL.md",
        "skills/watchdog-timeout-audit/SKILL.md": ROOT / "skills" / "watchdog-timeout-audit" / "SKILL.md",
    }

    for label, path in skill_files.items():
        content = _read_text(path)
        if content is None:
            findings.append(
                Finding(
                    level="L1",
                    category="skills",
                    file=label,
                    summary="正式 skill 文件缺失或无法读取。",
                    why_it_matters="skills 映射层对象缺失时，docs 真源无法稳定映射到正式 skill 文件集合。",
                    suggested_action=f"恢复 {label} 并确保 UTF-8 可读。",
                )
            )
            continue

        skill_contents[label] = content
        findings.extend(_check_skill_frontmatter(label, content))

    main_scenario_skills = (
        "skills/incident-investigation/SKILL.md",
        "skills/bringup-path/SKILL.md",
        "skills/design-safety-review/SKILL.md",
    )
    for label in main_scenario_skills:
        content = skill_contents.get(label)
        if content is None:
            continue

        missing_skill_layers = _find_missing_semantics(
            content,
            {
                "Phase layer": "Phase",
                "Domain Specialist layer": "specialist",
                "Artifact layer": "Artifact",
            },
        )
        if missing_skill_layers:
            findings.append(
                Finding(
                    level="L2",
                    category="skills",
                    file=label,
                    summary=f"主场景 skill 缺少命名层骨架：{', '.join(missing_skill_layers)}。",
                    why_it_matters="主场景 skill 若不显式声明 Phase、specialist 与 Artifact，Scenario 与执行层的边界会退化成口头约定。",
                    suggested_action="在主场景 SKILL.md 中补齐默认 Phase、specialist 偏向与主要 Artifact 段落。",
                )
            )

    orchestration_label = "skills/orchestration/SKILL.md"
    orchestration_content = skill_contents.get(orchestration_label)
    if orchestration_content is not None and "入口路由摘要" not in orchestration_content:
        findings.append(
            Finding(
                level="L2",
                category="skills",
                file=orchestration_label,
                summary="缺少“入口路由摘要”段。",
                why_it_matters="总入口路由规则缺少摘要锚点会降低映射层可审查性。",
                suggested_action="补充“入口路由摘要”并与 docs 真源保持一致。",
            )
        )

    evidence_label = "skills/evidence-pack/SKILL.md"
    evidence_content = skill_contents.get(evidence_label)
    if evidence_content is not None:
        has_no_global_competition_statement = (
            "不参与全局主路由竞争" in evidence_content
            or (
                "不作为全局主路由入口" in evidence_content
                and "不参与总路由竞争" in evidence_content
            )
        )
        if not has_no_global_competition_statement:
            findings.append(
                Finding(
                    level="L2",
                    category="skills",
                    file=evidence_label,
                    summary="缺少“不参与全局主路由竞争”声明。",
                    why_it_matters="辅助 skill 若无竞争限制，可能被误当全局入口。",
                    suggested_action="补充“不参与全局主路由竞争”的明确约束。",
                )
            )

    review_label = "skills/incident-review/SKILL.md"
    review_content = skill_contents.get(review_label)
    if review_content is not None:
        has_no_replace_statement = (
            "不替代 `design-safety-review`" in review_content
            or "不替代 design-safety-review" in review_content
        )
        if not has_no_replace_statement:
            findings.append(
                Finding(
                    level="L2",
                    category="skills",
                    file=review_label,
                    summary="缺少“不替代 design-safety-review”声明。",
                    why_it_matters="若不声明边界，incident review 容易越权承担设计复核职责。",
                    suggested_action="补充“不替代 design-safety-review”的明确表述。",
                )
            )

    for label, specialist_name in CANONICAL_SPECIALIST_SKILL_FILES.items():
        content = skill_contents.get(label)
        if content is None:
            continue

        missing_specialist_semantics = _find_missing_semantics(
            content,
            {
                "default Phase": "## 默认落点 Phase",
                "input contract": "## 输入契约",
                "output Artifact": "## 输出 Artifact",
                "not-responsible section": "## 不负责什么",
                "handoff conditions": "## 回交条件",
            },
        )
        if missing_specialist_semantics:
            findings.append(
                Finding(
                    level="L2",
                    category="skills",
                    file=label,
                    summary=f"specialist skill 缺少契约骨架：{', '.join(missing_specialist_semantics)}。",
                    why_it_matters="如果 specialist skill 没有稳定的输入 / 输出 / 禁止项 / 回交流程骨架，Domain Specialist 层就会重新退化成口头约定。",
                    suggested_action="在 specialist SKILL.md 中补齐默认 Phase、输入契约、输出 Artifact、不负责什么与回交条件段落。",
                )
            )

        has_domain_specialist_boundary = (
            "只作为 `Domain Specialist` 使用" in content
            or "只作为 Domain Specialist 使用" in content
        )
        if not has_domain_specialist_boundary:
            findings.append(
                Finding(
                    level="L2",
                    category="skills",
                    file=label,
                    summary=f"{specialist_name} 缺少 Domain Specialist 身份边界声明。",
                    why_it_matters="若 specialist skill 没有明确声明自己只属于 Domain Specialist 层，宿主侧就可能把它误当成新的场景入口。",
                    suggested_action="在 specialist SKILL.md 中明确声明其只作为 Domain Specialist 使用。",
                )
            )

        has_no_global_routing_boundary = (
            "不作为总路由入口" in content or "不参与总路由竞争" in content
        )
        if not has_no_global_routing_boundary:
            findings.append(
                Finding(
                    level="L2",
                    category="skills",
                    file=label,
                    summary=f"{specialist_name} 缺少总路由边界声明。",
                    why_it_matters="若 specialist skill 没有限定自己不参与总路由竞争，入口层与 specialist 层就会发生混层。",
                    suggested_action="在 specialist SKILL.md 中补充不作为总路由入口或不参与总路由竞争的声明。",
                )
            )

        missing_specialist_refs = _find_missing_semantics(
            content,
            {
                "domain contracts ref": "docs/DOMAIN_SPECIALIST_CONTRACTS.md",
                "incident workflow ref": "docs/INCIDENT_WORKFLOW.md",
                "orchestration ref": "docs/ORCHESTRATION.md",
            },
        )
        if missing_specialist_refs:
            findings.append(
                Finding(
                    level="L2",
                    category="skills",
                    file=label,
                    summary=f"specialist skill 缺少真源回指：{', '.join(missing_specialist_refs)}。",
                    why_it_matters="如果 specialist skill 不回指 specialist 契约真源、incident 场景边界与总调度规则，skill 层与 docs 层之间就无法保持单一真源关系。",
                    suggested_action="在 specialist SKILL.md 中加入对 DOMAIN_SPECIALIST_CONTRACTS、INCIDENT_WORKFLOW 与 ORCHESTRATION 的引用。",
                )
            )

    watchdog_skill_label = "skills/timing-watchdog-auditor/SKILL.md"
    watchdog_skill_content = skill_contents.get(watchdog_skill_label)
    if watchdog_skill_content is not None:
        missing_watchdog_skill_refs = _find_missing_semantics(
            watchdog_skill_content,
            {
                "watchdog method truth doc ref": "docs/WATCHDOG_TIMEOUT_AUDIT.md",
                "watchdog template ref": "docs/templates/timing-watchdog-audit-pack.md",
            },
        )
        if missing_watchdog_skill_refs:
            findings.append(
                Finding(
                    level="L2",
                    category="skills",
                    file=watchdog_skill_label,
                    summary=f"timing-watchdog-auditor 缺少 watchdog 方法真源回指：{', '.join(missing_watchdog_skill_refs)}。",
                    why_it_matters="若 specialist skill 不回指独立方法真源与其输出模板，watchdog 方法约束将无法在 skills 层闭环映射。",
                    suggested_action="在 skills/timing-watchdog-auditor/SKILL.md 中补齐 docs/WATCHDOG_TIMEOUT_AUDIT.md 与 docs/templates/timing-watchdog-audit-pack.md 的引用。",
                )
            )

        has_isr_inline_expansion = (
            "线内专项扩展" in watchdog_skill_content
            and "ISR / main loop" in watchdog_skill_content
            and "timing-watchdog-auditor" in watchdog_skill_content
        )
        if not has_isr_inline_expansion:
            findings.append(
                Finding(
                    level="L2",
                    category="skills",
                    file=watchdog_skill_label,
                    summary="timing-watchdog-auditor 缺少 ISR / main loop 冲突线内专项扩展声明。",
                    why_it_matters="若 skill 未同时声明 ISR / main loop 冲突检查属于 timing-watchdog-auditor 的线内专项扩展，归属边界会被误解为需要新建 specialist。",
                    suggested_action="在 skills/timing-watchdog-auditor/SKILL.md 中补充 ISR / main loop 冲突检查属于 timing-watchdog-auditor 线内专项扩展的明确表述。",
                )
            )

    register_skill_label = "skills/register-state-auditor/SKILL.md"
    register_skill_content = skill_contents.get(register_skill_label)
    if register_skill_content is not None:
        missing_register_skill_refs = _find_missing_semantics(
            register_skill_content,
            {
                "register method truth doc ref": "docs/REGISTER_STATE_AUDIT.md",
            },
        )
        if missing_register_skill_refs:
            findings.append(
                Finding(
                    level="L2",
                    category="skills",
                    file=register_skill_label,
                    summary=f"register-state-auditor 缺少 register 方法真源回指：{', '.join(missing_register_skill_refs)}。",
                    why_it_matters="若 specialist skill 不回指独立方法真源，register 方法约束将无法在 skills 层闭环映射。",
                    suggested_action="在 skills/register-state-auditor/SKILL.md 中补齐 docs/REGISTER_STATE_AUDIT.md 的引用。",
                )
            )

    watchdog_formal_skill_label = "skills/watchdog-timeout-audit/SKILL.md"
    watchdog_formal_skill_content = skill_contents.get(watchdog_formal_skill_label)
    if watchdog_formal_skill_content is not None:
        missing_watchdog_formal_skill_refs = _find_missing_semantics(
            watchdog_formal_skill_content,
            {
                "watchdog method truth doc ref": "docs/WATCHDOG_TIMEOUT_AUDIT.md",
                "watchdog audit pack template ref": "docs/templates/timing-watchdog-audit-pack.md",
                "watchdog findings template ref": "docs/templates/watchdog-timeout-audit-findings.md",
            },
        )
        if missing_watchdog_formal_skill_refs:
            findings.append(
                Finding(
                    level="L2",
                    category="skills",
                    file=watchdog_formal_skill_label,
                    summary=(
                        "watchdog-timeout-audit formal skill 缺少必要回指："
                        f"{', '.join(missing_watchdog_formal_skill_refs)}。"
                    ),
                    why_it_matters="若 formal skill 不回指方法真源与模板闭环对象，watchdog 专项能力的 docs/skills/templates 映射将不可审计。",
                    suggested_action="在 skills/watchdog-timeout-audit/SKILL.md 中补齐对 WATCHDOG_TIMEOUT_AUDIT、timing-watchdog-audit-pack 与 watchdog-timeout-audit-findings 的引用。",
                )
            )

        has_not_new_main_scenario_boundary = (
            "不是新的主场景" in watchdog_formal_skill_content
            or "不作为新的主场景" in watchdog_formal_skill_content
        )
        has_not_new_domain_specialist_boundary = (
            "不是新的 Domain Specialist" in watchdog_formal_skill_content
            or "不作为新的 Domain Specialist" in watchdog_formal_skill_content
            or "不是新的 `Domain Specialist`" in watchdog_formal_skill_content
            or "不作为新的 `Domain Specialist`" in watchdog_formal_skill_content
        )
        if not (has_not_new_main_scenario_boundary and has_not_new_domain_specialist_boundary):
            findings.append(
                Finding(
                    level="L2",
                    category="skills",
                    file=watchdog_formal_skill_label,
                    summary="watchdog-timeout-audit formal skill 缺少边界声明：未同时声明不是新的主场景且不是新的 Domain Specialist。",
                    why_it_matters="若 formal skill 不声明双边界，watchdog 专项入口会被误解为新增场景或新增 specialist，破坏既有层级。",
                    suggested_action="在 skills/watchdog-timeout-audit/SKILL.md 中明确声明其不是新的主场景，且不是新的 Domain Specialist。",
                )
            )

    return findings


def check_templates() -> list[Finding]:
    findings: list[Finding] = []

    findings_label = "docs/templates/validation-findings.md"
    findings_path = ROOT / "docs" / "templates" / "validation-findings.md"
    findings_content = _read_text(findings_path)
    if findings_content is None:
        findings.append(
            Finding(
                level="L1",
                category="templates",
                file=findings_label,
                summary="validation-findings 模板缺失或无法读取。",
                why_it_matters="findings 分级模板不可用会阻断一致性问题的统一记录。",
                suggested_action="恢复 docs/templates/validation-findings.md 并确保 UTF-8 可读。",
            )
        )
    elif "L1 / L2 / L3" not in findings_content:
        findings.append(
            Finding(
                level="L2",
                category="templates",
                file=findings_label,
                summary="缺少 L1 / L2 / L3 等级锚点。",
                why_it_matters="模板若未声明等级集，校验输出无法与分级规则对齐。",
                suggested_action="在模板中补充 L1 / L2 / L3 的明确允许值。",
            )
        )

    checklist_label = "docs/templates/consistency-review-checklist.md"
    checklist_path = ROOT / "docs" / "templates" / "consistency-review-checklist.md"
    checklist_content = _read_text(checklist_path)
    if checklist_content is None:
        findings.append(
            Finding(
                level="L1",
                category="templates",
                file=checklist_label,
                summary="consistency-review-checklist 模板缺失或无法读取。",
                why_it_matters="review 执行模板缺失会导致统一收口流程不可执行。",
                suggested_action="恢复 docs/templates/consistency-review-checklist.md 并确保 UTF-8 可读。",
            )
        )
    elif "overall result" not in checklist_content:
        findings.append(
            Finding(
                level="L2",
                category="templates",
                file=checklist_label,
                summary="缺少 overall result 收口段。",
                why_it_matters="缺失总体结论段会影响 review 结果的统一归档。",
                suggested_action="补充 overall result 结论区块。",
            )
        )

    watchdog_findings_label = "docs/templates/watchdog-timeout-audit-findings.md"
    watchdog_findings_path = ROOT / "docs" / "templates" / "watchdog-timeout-audit-findings.md"
    watchdog_findings_content = _read_text(watchdog_findings_path)
    if watchdog_findings_content is None:
        findings.append(
            Finding(
                level="L1",
                category="templates",
                file=watchdog_findings_label,
                summary="watchdog-timeout-audit-findings 模板缺失或无法读取。",
                why_it_matters="watchdog / timeout 轻量 findings 模板缺失会阻断专项检查结果的统一收口。",
                suggested_action="恢复 docs/templates/watchdog-timeout-audit-findings.md 并确保 UTF-8 可读。",
            )
        )
    else:
        missing_watchdog_findings_refs = _find_missing_semantics(
            watchdog_findings_content,
            {
                "watchdog method truth doc ref": "docs/WATCHDOG_TIMEOUT_AUDIT.md",
                "watchdog formal skill ref": "skills/watchdog-timeout-audit/SKILL.md",
            },
        )
        if missing_watchdog_findings_refs:
            findings.append(
                Finding(
                    level="L2",
                    category="templates",
                    file=watchdog_findings_label,
                    summary=f"watchdog-timeout-audit-findings 缺少必要回指：{', '.join(missing_watchdog_findings_refs)}。",
                    why_it_matters="若轻量 findings 模板不回指方法真源与 formal skill，watchdog 专项结果就无法与 docs/skills 层形成闭环映射。",
                    suggested_action="在 docs/templates/watchdog-timeout-audit-findings.md 中补齐对 WATCHDOG_TIMEOUT_AUDIT 与 skills/watchdog-timeout-audit/SKILL.md 的引用。",
                )
            )

    watchdog_report_label = "docs/templates/watchdog-timeout-audit-report.md"
    watchdog_report_path = ROOT / "docs" / "templates" / "watchdog-timeout-audit-report.md"
    watchdog_report_content = _read_text(watchdog_report_path)
    if watchdog_report_content is None:
        findings.append(
            Finding(
                level="L1",
                category="templates",
                file=watchdog_report_label,
                summary="watchdog-timeout-audit-report 模板缺失或无法读取。",
                why_it_matters="watchdog / timeout 最终专项报告模板缺失会阻断专项审计结果的正式收口。",
                suggested_action="恢复 docs/templates/watchdog-timeout-audit-report.md 并确保 UTF-8 可读。",
            )
        )
    else:
        missing_watchdog_report_refs = _find_missing_semantics(
            watchdog_report_content,
            {
                "watchdog method truth doc ref": "docs/WATCHDOG_TIMEOUT_AUDIT.md",
                "watchdog findings template ref": "docs/templates/watchdog-timeout-audit-findings.md",
                "watchdog audit pack template ref": "docs/templates/timing-watchdog-audit-pack.md",
            },
        )
        if missing_watchdog_report_refs:
            findings.append(
                Finding(
                    level="L2",
                    category="templates",
                    file=watchdog_report_label,
                    summary=f"watchdog-timeout-audit-report 缺少必要回指：{', '.join(missing_watchdog_report_refs)}。",
                    why_it_matters="若最终 report 模板不回指方法真源、findings 模板与 audit pack，专项结论将无法形成可追溯闭环。",
                    suggested_action="在 docs/templates/watchdog-timeout-audit-report.md 中补齐对 WATCHDOG_TIMEOUT_AUDIT、watchdog-timeout-audit-findings 与 timing-watchdog-audit-pack 的引用。",
                )
            )

        missing_watchdog_report_sections = _find_missing_semantics(
            watchdog_report_content,
            {
                "audit summary": "## audit summary",
                "key findings": "## key findings",
                "evidence highlights": "## evidence highlights",
                "risk assessment": "## risk assessment",
                "recommended actions": "## recommended actions",
                "verification gaps": "## verification gaps",
            },
        )
        if missing_watchdog_report_sections:
            findings.append(
                Finding(
                    level="L2",
                    category="templates",
                    file=watchdog_report_label,
                    summary=f"watchdog-timeout-audit-report 缺少固定结构段：{', '.join(missing_watchdog_report_sections)}。",
                    why_it_matters="若最终 report 模板缺少固定结构段，专项审计结果就无法保持统一的可审查格式。",
                    suggested_action="在 docs/templates/watchdog-timeout-audit-report.md 中补齐 audit summary、key findings、evidence highlights、risk assessment、recommended actions 与 verification gaps 六个段落。",
                )
            )

    watchdog_report_generator_label = "tools/generate_watchdog_timeout_audit_report.py"
    watchdog_report_generator_path = ROOT / "tools" / "generate_watchdog_timeout_audit_report.py"
    watchdog_report_generator_content = _read_text(watchdog_report_generator_path)
    if watchdog_report_generator_content is None:
        findings.append(
            Finding(
                level="L1",
                category="tools",
                file=watchdog_report_generator_label,
                summary="watchdog 自动报告生成器脚本缺失或无法读取。",
                why_it_matters="缺少自动报告生成器会让 watchdog findings/pack 到最终报告模板的收口链路无法执行。",
                suggested_action="补充 tools/generate_watchdog_timeout_audit_report.py 并确保 UTF-8 可读。",
            )
        )
    else:
        missing_watchdog_report_generator_anchors = _find_missing_semantics(
            watchdog_report_generator_content,
            {
                "watchdog findings input anchor": "watchdog-timeout-audit-findings",
                "watchdog pack input anchor": "timing-watchdog-audit-pack",
                "watchdog report output anchor": "watchdog-timeout-audit-report",
            },
        )
        if missing_watchdog_report_generator_anchors:
            findings.append(
                Finding(
                    level="L2",
                    category="tools",
                    file=watchdog_report_generator_label,
                    summary=(
                        "watchdog 自动报告生成器脚本缺少输入/输出锚点："
                        f"{', '.join(missing_watchdog_report_generator_anchors)}。"
                    ),
                    why_it_matters="若脚本未显式体现 findings 主输入、pack 补充输入与 report 输出锚点，生成链路将不可审计。",
                    suggested_action="在脚本中补齐 watchdog-timeout-audit-findings、timing-watchdog-audit-pack、watchdog-timeout-audit-report 三个锚点。",
                )
            )

    boundary_label = "docs/templates/skill-boundary-checklist.md"
    boundary_path = ROOT / "docs" / "templates" / "skill-boundary-checklist.md"
    boundary_content = _read_text(boundary_path)
    if boundary_content is None:
        findings.append(
            Finding(
                level="L1",
                category="templates",
                file=boundary_label,
                summary="skill-boundary-checklist 模板缺失或无法读取。",
                why_it_matters="缺少边界模板会让 skill 层的命名规则无法被统一复核。",
                suggested_action="恢复 docs/templates/skill-boundary-checklist.md 并确保 UTF-8 可读。",
            )
        )
    else:
        missing_boundary_semantics = _find_missing_semantics(
            boundary_content,
            {
                "skill name": "skill name",
                "default Phase": "default Phase",
                "default specialist bias": "default specialist bias",
                "main Artifacts": "main Artifacts",
            },
        )
        if missing_boundary_semantics:
            findings.append(
                Finding(
                    level="L2",
                    category="templates",
                    file=boundary_label,
                    summary=f"skill-boundary-checklist 缺少字段锚点：{', '.join(missing_boundary_semantics)}。",
                    why_it_matters="如果边界模板不能显式承载 Phase / specialist / Artifact 语义，skill 设计就无法被稳定复核。",
                    suggested_action="在 skill-boundary-checklist 中补齐 skill name、default Phase、default specialist bias 与 main Artifacts 字段。",
                )
            )

    dispatch_label = "docs/templates/orchestrator-dispatch-plan.md"
    dispatch_path = ROOT / "docs" / "templates" / "orchestrator-dispatch-plan.md"
    dispatch_content = _read_text(dispatch_path)
    if dispatch_content is None:
        findings.append(
            Finding(
                level="L1",
                category="templates",
                file=dispatch_label,
                summary="orchestrator-dispatch-plan 模板缺失或无法读取。",
                why_it_matters="调度计划模板缺失会让 Scenario / Phase / specialist / Artifact 的派发关系无法形成统一载体。",
                suggested_action="恢复 docs/templates/orchestrator-dispatch-plan.md 并确保 UTF-8 可读。",
            )
        )
    else:
        missing_dispatch_semantics = _find_missing_semantics(
            dispatch_content,
            {
                "scenario field": "## scenario",
                "phase field": "## phase plan",
                "specialist field": "specialist:",
                "artifact field": ("expected output artifacts", "expected artifacts"),
                "control field": "## next control signal",
            },
        )
        if missing_dispatch_semantics:
            findings.append(
                Finding(
                    level="L2",
                    category="templates",
                    file=dispatch_label,
                    summary=f"orchestrator-dispatch-plan 缺少调度字段：{', '.join(missing_dispatch_semantics)}。",
                    why_it_matters="调度模板若不能同时承载场景、Phase、specialist、Artifact 与控制信号，编排结果就无法闭环落表。",
                    suggested_action="在 orchestrator-dispatch-plan 中补齐 scenario、phase、specialist、expected artifacts 与 next control signal 字段。",
                )
            )

        missing_scenarios = [scenario for scenario in CANONICAL_SCENARIOS if scenario not in dispatch_content]
        if missing_scenarios:
            findings.append(
                Finding(
                    level="L2",
                    category="templates",
                    file=dispatch_label,
                    summary=f"orchestrator-dispatch-plan 未覆盖全部主场景：{', '.join(missing_scenarios)}。",
                    why_it_matters="调度模板若缺少主场景枚举，Scenario 层的规范值就会在落表时发生漂移。",
                    suggested_action="在 orchestrator-dispatch-plan 中补齐全部主场景的允许值。",
                )
            )

        missing_phases = [phase for phase in CANONICAL_PHASES if phase not in dispatch_content]
        if missing_phases:
            findings.append(
                Finding(
                    level="L2",
                    category="templates",
                    file=dispatch_label,
                    summary=f"orchestrator-dispatch-plan 未覆盖全部 canonical phase：{', '.join(missing_phases)}。",
                    why_it_matters="如果模板没有列出 canonical phase 集合，Phase 层会在不同载体间出现命名漂移。",
                    suggested_action="在 orchestrator-dispatch-plan 中补齐全部 canonical phase 允许值。",
                )
            )

        missing_specialists = [
            specialist for specialist in CANONICAL_SPECIALISTS if specialist not in dispatch_content
        ]
        if missing_specialists:
            findings.append(
                Finding(
                    level="L2",
                    category="templates",
                    file=dispatch_label,
                    summary=f"orchestrator-dispatch-plan 未覆盖全部 canonical specialist：{', '.join(missing_specialists)}。",
                    why_it_matters="如果模板没有列出 canonical specialist 集合，Domain Specialist 层就无法稳定复用同一套命名。",
                    suggested_action="在 orchestrator-dispatch-plan 中补齐全部 canonical specialist 允许值。",
                )
            )

    specialist_pack_templates = {
        "docs/templates/signal-path-trace-pack.md": (
            "signal-path-tracer",
            ("segmented-failure-path", "observability-point-list", "path-suspicion-ranking"),
        ),
        "docs/templates/register-state-audit-pack.md": (
            "register-state-auditor",
            ("register-bitfield-map", "register-anomaly-list", "config-mismatch-note"),
        ),
        "docs/templates/state-machine-trace-pack.md": (
            "state-machine-tracer",
            ("state-transition-chain", "stuck-state-list", "safety-state-gap-note"),
        ),
        "docs/templates/timing-watchdog-audit-pack.md": (
            "timing-watchdog-auditor",
            ("timeout-watchdog-risk-table", "isr-mainloop-conflict-note", "timing-instability-hypothesis"),
        ),
        "docs/templates/failsafe-convergence-review-pack.md": (
            "failsafe-convergence-reviewer",
            ("failsafe-convergence-note", "unsafe-persistence-risk", "convergence-expectation-check"),
        ),
    }
    watchdog_isr_evidence_fields = (
        "- ISR 侧职责:",
        "- main loop 侧职责:",
        "- 被破坏的确定性约束:",
        "- 可能导致的 reset / timeout / 饥饿风险:",
        "- 仍缺的证据:",
    )
    specialist_pack_truth_refs = {
        "docs/templates/timing-watchdog-audit-pack.md": "docs/WATCHDOG_TIMEOUT_AUDIT.md",
        "docs/templates/register-state-audit-pack.md": "docs/REGISTER_STATE_AUDIT.md",
    }
    for label, (specialist_name, expected_artifacts) in specialist_pack_templates.items():
        path = ROOT / Path(label)
        content = _read_text(path)
        if content is None:
            findings.append(
                Finding(
                    level="L1",
                    category="templates",
                    file=label,
                    summary="specialist 输出模板缺失或无法读取。",
                    why_it_matters="若没有可填写的 specialist 输出模板，v4 的模板化能力文档就无法真正承接 Domain Specialist 的 Artifact 产出。",
                    suggested_action=f"恢复 {label} 并确保 UTF-8 可读。",
                )
            )
            continue

        truth_ref = specialist_pack_truth_refs.get(label)
        if truth_ref is not None and truth_ref not in content:
            findings.append(
                Finding(
                    level="L2",
                    category="templates",
                    file=label,
                    summary=f"specialist 输出模板缺少方法真源回指：{truth_ref}。",
                    why_it_matters="若模板不回指对应的方法真源文档，Domain Specialist 的方法规则与模板填写规范就无法保持单一真源。",
                    suggested_action=f"在 {label} 中加入对 {truth_ref} 的引用。",
                )
            )

        missing_pack_semantics = _find_missing_semantics(
            content,
            {
                "input snapshot": "## input snapshot",
                "evidence used": "## evidence used",
                "primary artifacts": "## primary artifacts",
                "confidence": "## confidence",
                "unresolved gaps": "## unresolved gaps",
                "evidence backlinks": "## evidence backlinks",
                "next suggestion": "## next suggestion for orchestrator",
                "domain specialist contracts ref": "docs/DOMAIN_SPECIALIST_CONTRACTS.md",
            },
        )
        if missing_pack_semantics:
            findings.append(
                Finding(
                    level="L2",
                    category="templates",
                    file=label,
                    summary=f"specialist 输出模板缺少结构锚点：{', '.join(missing_pack_semantics)}。",
                    why_it_matters="若 specialist 输出模板没有输入、证据、Artifact、置信度与回交建议结构，模板层就无法稳定承接 specialist 契约。",
                    suggested_action="在 specialist 输出模板中补齐 input snapshot、evidence used、primary artifacts、confidence、unresolved gaps、evidence backlinks 与 next suggestion for orchestrator。",
                )
            )

        if specialist_name not in content:
            findings.append(
                Finding(
                    level="L2",
                    category="templates",
                    file=label,
                    summary=f"specialist 输出模板缺少 specialist 名称锚点：{specialist_name}。",
                    why_it_matters="模板若不显式标注对应 specialist，后续填写时就容易发生 Domain Specialist 与 Artifact 模板错配。",
                    suggested_action=f"在模板顶部显式标注其对应的 specialist：{specialist_name}。",
                )
            )

        missing_artifacts = [artifact for artifact in expected_artifacts if artifact not in content]
        if missing_artifacts:
            findings.append(
                Finding(
                    level="L2",
                    category="templates",
                    file=label,
                    summary=f"specialist 输出模板缺少预期 Artifact：{', '.join(missing_artifacts)}。",
                    why_it_matters="若模板未覆盖该 specialist 的 canonical Artifact，填写产物时就无法稳定对齐 Domain Specialist 契约。",
                    suggested_action="在 specialist 输出模板中补齐该 specialist 的全部 canonical Artifact 占位段。",
                )
            )

        if label == "docs/templates/timing-watchdog-audit-pack.md":
            missing_watchdog_isr_fields = [
                field for field in watchdog_isr_evidence_fields if field not in content
            ]
            if missing_watchdog_isr_fields:
                findings.append(
                    Finding(
                        level="L2",
                        category="templates",
                        file=label,
                        summary=(
                            "timing-watchdog-audit-pack 缺少 ISR / main loop 冲突专属证据字段："
                            f"{', '.join(missing_watchdog_isr_fields)}。"
                        ),
                        why_it_matters="若模板缺少 ISR / main loop 冲突专属证据字段，isr-mainloop-conflict-note 将无法稳定承载可审计证据。",
                        suggested_action="在 docs/templates/timing-watchdog-audit-pack.md 中补齐 ISR 侧职责、main loop 侧职责、确定性约束破坏、reset/timeout/饥饿风险与缺失证据字段。",
                    )
                )

    return findings


def check_routing_cases() -> list[Finding]:
    findings: list[Finding] = []
    matrix_label = "docs/templates/skill-routing-matrix.md"
    matrix_path = ROOT / "docs" / "templates" / "skill-routing-matrix.md"
    matrix_content = _read_text(matrix_path)

    if matrix_content is None:
        findings.append(
            Finding(
                level="L1",
                category="routing_cases",
                file=matrix_label,
                summary="案例层 routing 载体对象缺失或无法读取。",
                why_it_matters="案例层若没有可读取的路由载体对象，真实输入将无法沉淀为可审计 route case。",
                suggested_action="恢复 docs/templates/skill-routing-matrix.md 并确保 UTF-8 可读。",
            )
        )
        return findings

    is_case_layer_carrier = "案例层模板" in matrix_content
    if not is_case_layer_carrier:
        findings.append(
            Finding(
                level="L2",
                category="routing_cases",
                file=matrix_label,
                summary="routing 载体对象未声明为案例层模板。",
                why_it_matters="载体层级不明确会让案例层校验与模板层校验混淆。",
                suggested_action="在载体对象中补充“案例层模板”定位说明。",
            )
        )

    missing_route_semantics = [
        semantic
        for semantic in ("route decision", "route type")
        if semantic not in matrix_content
    ]
    if missing_route_semantics:
        findings.append(
            Finding(
                level="L1",
                category="routing_cases",
                file=matrix_label,
                summary=f"routing 载体对象缺少判定语义：{', '.join(missing_route_semantics)}。",
                why_it_matters="案例层载体若不能承载 route decision / route type，路由结论将无法形成闭环证据。",
                suggested_action="在案例层载体中补齐 route decision 与 route type 语义字段。",
            )
        )

    if "incident 语义上下文" not in matrix_content:
        findings.append(
            Finding(
                level="L2",
                category="routing_cases",
                file=matrix_label,
                summary="routing 载体对象缺少 incident 语义上下文承载约束。",
                why_it_matters="缺失 incident 语义上下文会弱化辅助 skill 的受控进入边界。",
                suggested_action="在案例层载体中补充“incident 语义上下文”约束说明。",
            )
        )

    cases_root = ROOT / "docs" / "cases"
    cases_root_label = "docs/cases"
    if not cases_root.is_dir():
        findings.append(
            Finding(
                level="L1",
                category="routing_cases",
                file=cases_root_label,
                summary="incident workflow 回归案例目录缺失。",
                why_it_matters="只有模板没有真实回归案例时，incident workflow 的示例任务无法被稳定复查。",
                suggested_action="创建 docs/cases 目录并放置 incident workflow 的实际回归案例文档。",
            )
        )
        return findings

    routing_regression_label = "docs/cases/incident-workflow-routing-regression.md"
    routing_regression_content = _read_text(cases_root / "incident-workflow-routing-regression.md")
    if routing_regression_content is None:
        findings.append(
            Finding(
                level="L1",
                category="routing_cases",
                file=routing_regression_label,
                summary="incident workflow 路由回归基线缺失或无法读取。",
                why_it_matters="若没有真实入口路由回归样本，后续规则调整时无法确认 direct entry / orchestration / auxiliary 进入边界是否被破坏。",
                suggested_action="恢复 docs/cases/incident-workflow-routing-regression.md 并确保 UTF-8 可读。",
            )
        )
    else:
        missing_routing_case_semantics = _find_missing_semantics(
            routing_regression_content,
            {
                "route decision": "route decision",
                "route type": "route type",
                "incident context": "incident context",
            },
        )
        if missing_routing_case_semantics:
            findings.append(
                Finding(
                    level="L1",
                    category="routing_cases",
                    file=routing_regression_label,
                    summary=f"路由回归基线缺少核心字段：{', '.join(missing_routing_case_semantics)}。",
                    why_it_matters="回归样本若不能稳定承载 route decision / route type / incident context，案例层就无法验证辅助 skill 的受控进入规则。",
                    suggested_action="在路由回归基线中补齐 route decision、route type 与 incident context 字段。",
                )
            )

        missing_route_decisions = [
            decision
            for decision in ("orchestration", "incident-investigation", "evidence-pack", "incident-review")
            if decision not in routing_regression_content
        ]
        if missing_route_decisions:
            findings.append(
                Finding(
                    level="L2",
                    category="routing_cases",
                    file=routing_regression_label,
                    summary=f"路由回归基线未覆盖关键 route decision：{', '.join(missing_route_decisions)}。",
                    why_it_matters="若关键入口与辅助 skill 的真实任务样本未被覆盖，后续规则回归就无法发现边界漂移。",
                    suggested_action="在路由回归基线中补齐 orchestration、incident-investigation、evidence-pack 与 incident-review 的样本。",
                )
            )

        missing_route_types = [
            route_type
            for route_type in ("直进子入口", "先走总入口", "辅助 skill 受控进入")
            if route_type not in routing_regression_content
        ]
        if missing_route_types:
            findings.append(
                Finding(
                    level="L2",
                    category="routing_cases",
                    file=routing_regression_label,
                    summary=f"路由回归基线未覆盖全部 route type：{', '.join(missing_route_types)}。",
                    why_it_matters="缺少 route type 覆盖会让总入口、直进与辅助进入三类行为无法做稳定回归。",
                    suggested_action="在路由回归基线中补齐直进子入口、先走总入口与辅助 skill 受控进入三类样本。",
                )
            )

    dispatch_regression_label = "docs/cases/incident-workflow-dispatch-regression.md"
    dispatch_regression_content = _read_text(cases_root / "incident-workflow-dispatch-regression.md")
    if dispatch_regression_content is None:
        findings.append(
            Finding(
                level="L1",
                category="routing_cases",
                file=dispatch_regression_label,
                summary="incident workflow dispatch 回归基线缺失或无法读取。",
                why_it_matters="若没有 dispatch 回归样本，phase / specialist / Artifact / control signal 的组合就无法被真实任务回放验证。",
                suggested_action="恢复 docs/cases/incident-workflow-dispatch-regression.md 并确保 UTF-8 可读。",
            )
        )
    else:
        missing_dispatch_case_semantics = _find_missing_semantics(
            dispatch_regression_content,
            {
                "primary scenario": "primary scenario",
                "expected phase backbone": "expected phase backbone",
                "expected specialists": "expected specialists",
                "expected artifacts": "expected artifacts",
                "expected control signal": "expected control signal",
            },
        )
        if missing_dispatch_case_semantics:
            findings.append(
                Finding(
                    level="L1",
                    category="routing_cases",
                    file=dispatch_regression_label,
                    summary=f"dispatch 回归基线缺少核心字段：{', '.join(missing_dispatch_case_semantics)}。",
                    why_it_matters="若真实 dispatch 样本没有 phase / specialist / Artifact / control signal 这些字段，incident workflow 主链就无法做闭环回归。",
                    suggested_action="在 dispatch 回归基线中补齐 primary scenario、expected phase backbone、expected specialists、expected artifacts 与 expected control signal。",
                )
            )

        if "incident-investigation" not in dispatch_regression_content:
            findings.append(
                Finding(
                    level="L2",
                    category="routing_cases",
                    file=dispatch_regression_label,
                    summary="dispatch 回归基线缺少 incident-investigation 主场景锚点。",
                    why_it_matters="当前回归目标围绕 incident workflow，若主场景锚点缺失，就无法确认主链仍然落在 incident-investigation。",
                    suggested_action="在 dispatch 回归基线中明确 primary scenario 为 incident-investigation。",
                )
            )

        missing_phases = [phase for phase in CANONICAL_PHASES if phase not in dispatch_regression_content]
        if missing_phases:
            findings.append(
                Finding(
                    level="L2",
                    category="routing_cases",
                    file=dispatch_regression_label,
                    summary=f"dispatch 回归基线未覆盖完整 incident phase backbone：{', '.join(missing_phases)}。",
                    why_it_matters="若 dispatch 样本未覆盖四段 phase backbone，主链重排或阶段遗漏就无法在回归时暴露。",
                    suggested_action="在 dispatch 回归基线中补齐 hazard-analysis、link-diagnostics、deterministic-foundation 与 failsafe-validation。",
                )
            )

        missing_specialists = [
            specialist for specialist in CANONICAL_SPECIALISTS if specialist not in dispatch_regression_content
        ]
        if missing_specialists:
            findings.append(
                Finding(
                    level="L2",
                    category="routing_cases",
                    file=dispatch_regression_label,
                    summary=f"dispatch 回归基线未覆盖完整 specialist 集合：{', '.join(missing_specialists)}。",
                    why_it_matters="若回归样本不触达完整 specialist 集合，specialist 契约漂移就难以及时暴露。",
                    suggested_action="在 dispatch 回归基线中补齐全部 canonical specialist 的期望装配。",
                )
            )

        missing_artifacts = [
            artifact
            for artifact in ("incident-summary", "evidence-package", "incident-diagnosis-pack")
            if artifact not in dispatch_regression_content
        ]
        if missing_artifacts:
            findings.append(
                Finding(
                    level="L2",
                    category="routing_cases",
                    file=dispatch_regression_label,
                    summary=f"dispatch 回归基线未覆盖关键 Artifact：{', '.join(missing_artifacts)}。",
                    why_it_matters="若关键 incident Artifact 没有进入回归样本，skill / specialist / review 的产物边界就无法被连续验证。",
                    suggested_action="在 dispatch 回归基线中补齐 incident-summary、evidence-package 与 incident-diagnosis-pack 的期望产物。",
                )
            )

    return findings


def check_process_docs() -> list[Finding]:
    findings: list[Finding] = []
    scan_roots = (
        ROOT / "docs" / "superpowers" / "specs",
        ROOT / "docs" / "superpowers" / "plans",
    )

    for scan_root in scan_roots:
        root_label = scan_root.relative_to(ROOT).as_posix()
        if not scan_root.is_dir():
            findings.append(
                Finding(
                    level="L1",
                    category="process_docs",
                    file=root_label,
                    summary="过程文档目录缺失。",
                    why_it_matters="目录缺失会让 process_docs 校验范围被静默跳过，无法保证覆盖性。",
                    suggested_action="恢复目录并放置可校验的过程文档。",
                )
            )
            continue

        process_docs = sorted(scan_root.rglob("*.md"))
        if not process_docs:
            findings.append(
                Finding(
                    level="L2",
                    category="process_docs",
                    file=root_label,
                    summary="过程文档目录存在但没有 .md 文件。",
                    why_it_matters="process_docs 范围没有实际对象时，相关语义约束会处于未验证状态。",
                    suggested_action="在目录中补充至少一个可读的过程文档。",
                )
            )
            continue

        for process_doc in process_docs:
            content = _read_text(process_doc)
            file_label = process_doc.relative_to(ROOT).as_posix()
            if content is None:
                findings.append(
                    Finding(
                        level="L1",
                        category="process_docs",
                        file=file_label,
                        summary="过程文档无法读取。",
                        why_it_matters="过程文档不可读会导致 incident 语义约束无法校验。",
                        suggested_action="修复文件编码或权限，确保过程文档可被一致性脚本读取。",
                    )
                )
                continue

            if not is_incident_orchestrator_scoped(content):
                findings.append(
                    Finding(
                        level="L2",
                        category="process_docs",
                        file=file_label,
                        summary="incident-orchestrator 表述未收紧为场景内调度器示例。",
                        why_it_matters="过程文档语义若未收紧，容易回退为全局总路由角色定义。",
                        suggested_action="将 incident-orchestrator 明确为“场景内调度器示例”或等价表述。",
                    )
                )

    return findings


VALIDATION_CHECKS = (
    ("docs", check_docs),
    ("skills", check_skills),
    ("templates", check_templates),
    ("routing_cases", check_routing_cases),
    ("process_docs", check_process_docs),
)


def filter_findings_by_level(findings: Iterable[Finding], level: str) -> list[Finding]:
    return [finding for finding in findings if finding.level == level]


def print_findings_section(level: str, findings: list[Finding]) -> None:
    print(f"\n=== {level} Findings ===")
    if not findings:
        print(LEVEL_NO_FINDINGS_MESSAGE[level])
        return

    for index, finding in enumerate(findings, start=1):
        print(f"{index}. [{finding.level}][{finding.category}] {finding.file}")
        print(f"   Summary: {finding.summary}")
        print(f"   Why it matters: {finding.why_it_matters}")
        print(f"   Suggested action: {finding.suggested_action}")


def compute_exit_code(findings: Iterable[Finding]) -> int:
    has_l1 = any(finding.level == "L1" for finding in findings)
    has_l2 = any(finding.level == "L2" for finding in findings)

    if has_l1:
        return 1
    if has_l2:
        return 2
    return 0


def main() -> int:
    print("Validation scope")
    for scope_name, _ in VALIDATION_CHECKS:
        print(f"- {scope_name}")

    all_findings: list[Finding] = []
    for _, checker in VALIDATION_CHECKS:
        all_findings.extend(checker())

    findings_count_by_level = {
        level: len(filter_findings_by_level(all_findings, level)) for level in LEVEL_ORDER
    }

    for level in LEVEL_ORDER:
        findings_for_level = filter_findings_by_level(all_findings, level)
        print_findings_section(level, findings_for_level)

    exit_code = compute_exit_code(all_findings)
    validation_result = "PASS" if exit_code == 0 else "FAIL"
    print(f"\nValidation result: {validation_result}")
    for level in LEVEL_ORDER:
        print(f"- {level}: {findings_count_by_level[level]}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
