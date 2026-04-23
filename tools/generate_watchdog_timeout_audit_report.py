from __future__ import annotations

import argparse
from pathlib import Path


def read_text_file(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def extract_section(text: str, heading: str) -> str:
    lines = text.splitlines()
    target = f"## {heading}".strip()

    start_index: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == target:
            start_index = index + 1
            break

    if start_index is None:
        return ""

    end_index = len(lines)
    for index in range(start_index, len(lines)):
        if lines[index].startswith("## "):
            end_index = index
            break

    return "\n".join(lines[start_index:end_index]).strip()


def _fallback(content: str, default: str = "- （未提供对应内容）") -> str:
    stripped = content.strip()
    return stripped if stripped else default


def generate_report(findings_text: str, pack_text: str) -> str:
    audit_summary = extract_section(findings_text, "audit summary")
    key_findings = extract_section(findings_text, "key findings")
    evidence_highlights = extract_section(pack_text, "evidence used")
    risk_assessment = extract_section(findings_text, "risk assessment")
    recommended_actions = extract_section(findings_text, "recommended actions")
    verification_gaps = extract_section(findings_text, "verification gaps")

    if not key_findings:
        key_findings = findings_text.strip()

    return "\n".join(
        [
            "# watchdog-timeout-audit-report",
            "",
            "- 方法真源：docs/WATCHDOG_TIMEOUT_AUDIT.md",
            "- 主输入：watchdog-timeout-audit-findings",
            "- 补充输入：timing-watchdog-audit-pack",
            "",
            "## audit summary",
            _fallback(audit_summary),
            "",
            "## key findings",
            _fallback(key_findings),
            "",
            "## evidence highlights",
            _fallback(evidence_highlights),
            "",
            "## risk assessment",
            _fallback(risk_assessment),
            "",
            "## recommended actions",
            _fallback(recommended_actions),
            "",
            "## verification gaps",
            _fallback(verification_gaps),
            "",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate watchdog-timeout-audit-report from "
            "watchdog-timeout-audit-findings and timing-watchdog-audit-pack"
        )
    )
    parser.add_argument(
        "--findings",
        required=True,
        help="Path to watchdog-timeout-audit-findings markdown",
    )
    parser.add_argument(
        "--pack",
        required=False,
        help="Path to timing-watchdog-audit-pack markdown",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to output watchdog-timeout-audit-report markdown",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    findings_text = read_text_file(args.findings)
    pack_text = read_text_file(args.pack) if args.pack else ""

    report_text = generate_report(findings_text, pack_text)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_text, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
