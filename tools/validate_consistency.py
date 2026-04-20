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


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


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
        rf"`?{re.escape(anchor)}`?\s*(?:[:：]\s*)?(?:是|为|作为|仅作|仅为|仅用于|仅限|仅承担|只作|只用于|负责|属于)"
    )

    def has_scenario_scope(local_block: str) -> bool:
        return "场景内" in local_block

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
            return False
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
    file_label = "docs/ORCHESTRATION.md"
    file_path = ROOT / "docs" / "ORCHESTRATION.md"
    content = _read_text(file_path)

    if content is None:
        findings.append(
            Finding(
                level="L1",
                category="docs",
                file=file_label,
                summary="ORCHESTRATION 真源文件缺失或无法读取。",
                why_it_matters="docs 真源层不可读时，后续映射层和模板层都无法被可信校验。",
                suggested_action="恢复 docs/ORCHESTRATION.md 并确保 UTF-8 可读。",
            )
        )
        return findings

    for keyword in ("Scenario", "Phase", "Domain Specialist", "Artifact"):
        if keyword not in content:
            findings.append(
                Finding(
                    level="L1",
                    category="docs",
                    file=file_label,
                    summary=f"缺少关键术语：{keyword}。",
                    why_it_matters="对象层级命名不完整会破坏总调度规则的可判定性。",
                    suggested_action="补齐 Scenario / Phase / Domain Specialist / Artifact 的明确表述。",
                )
            )

    if not is_incident_orchestrator_scoped(content):
        findings.append(
            Finding(
                level="L2",
                category="docs",
                file=file_label,
                summary="incident-orchestrator 未被约束为场景内调度器示例。",
                why_it_matters="未限定语义会误导为全局总路由名，造成边界越权。",
                suggested_action="在同一文档中明确其仅为场景内调度器示例。",
            )
        )

    if "docs/ORCHESTRATOR_PROMPT_CONTRACT.md" not in content:
        findings.append(
            Finding(
                level="L1",
                category="docs",
                file=file_label,
                summary="缺少对 ORCHESTRATOR_PROMPT_CONTRACT 的回指。",
                why_it_matters="总调度规则与 prompt 契约无法建立双文档锚点，容易出现双重真源。",
                suggested_action="在 ORCHESTRATION.md 中加入对 docs/ORCHESTRATOR_PROMPT_CONTRACT.md 的引用。",
            )
        )

    return findings


def check_skills() -> list[Finding]:
    findings: list[Finding] = []

    orchestration_label = "skills/orchestration/SKILL.md"
    orchestration_path = ROOT / "skills" / "orchestration" / "SKILL.md"
    orchestration_content = _read_text(orchestration_path)
    if orchestration_content is None:
        findings.append(
            Finding(
                level="L1",
                category="skills",
                file=orchestration_label,
                summary="orchestration 技能文件缺失或无法读取。",
                why_it_matters="总入口技能不可读会导致 skills 映射层无法校验总路由承接。",
                suggested_action="恢复 skills/orchestration/SKILL.md 并确保 UTF-8 可读。",
            )
        )
    elif "入口路由摘要" not in orchestration_content:
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
    evidence_path = ROOT / "skills" / "evidence-pack" / "SKILL.md"
    evidence_content = _read_text(evidence_path)
    if evidence_content is None:
        findings.append(
            Finding(
                level="L1",
                category="skills",
                file=evidence_label,
                summary="evidence-pack 技能文件缺失或无法读取。",
                why_it_matters="辅助 skill 的边界声明不可校验会引发主路由竞争歧义。",
                suggested_action="恢复 skills/evidence-pack/SKILL.md 并确保 UTF-8 可读。",
            )
        )
    else:
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
    review_path = ROOT / "skills" / "incident-review" / "SKILL.md"
    review_content = _read_text(review_path)
    if review_content is None:
        findings.append(
            Finding(
                level="L1",
                category="skills",
                file=review_label,
                summary="incident-review 技能文件缺失或无法读取。",
                why_it_matters="incident 辅助 review 边界缺失会影响场景职责隔离。",
                suggested_action="恢复 skills/incident-review/SKILL.md 并确保 UTF-8 可读。",
            )
        )
    else:
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
