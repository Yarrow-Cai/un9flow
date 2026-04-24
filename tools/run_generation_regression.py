#!/usr/bin/env python3
"""Run generation regression against golden inputs and outputs."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_OBJECTS = ("watchdog-timeout-audit-report", "incident-case-bundle")
WATCHDOG_OUTPUT_NAME = "watchdog-timeout-audit-report.md"
WATCHDOG_GENERATOR = ROOT / "tools" / "generate_watchdog_timeout_audit_report.py"
INCIDENT_GENERATOR = ROOT / "tools" / "generate_incident_case_bundle.py"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run generation regression against golden inputs."
    )
    parser.add_argument(
        "--object",
        choices=ALLOWED_OBJECTS,
        help="Object type to test. If omitted, run all supported objects.",
    )
    parser.add_argument(
        "--case",
        default="minimal",
        help="Test case name",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check mode (compare against golden)",
    )
    parser.add_argument(
        "--update-golden",
        action="store_true",
        help="Update golden files",
    )
    return parser


def compare_file(actual_path: Path, golden_path: Path) -> list[str]:
    if not actual_path.exists():
        return [f"Missing generated file: {actual_path}"]
    if not golden_path.exists():
        return [f"Missing golden file: {golden_path}"]

    actual_text = actual_path.read_text(encoding="utf-8")
    golden_text = golden_path.read_text(encoding="utf-8")
    if actual_text == golden_text:
        return []
    return [f"Content mismatch: {golden_path}"]


def compare_bundle(actual_dir: Path, golden_dir: Path) -> list[str]:
    if not actual_dir.exists():
        return [f"Missing generated bundle: {actual_dir}"]
    if not golden_dir.exists():
        return [f"Missing golden bundle: {golden_dir}"]

    expected_files = sorted(
        path.relative_to(golden_dir).as_posix()
        for path in golden_dir.rglob("*")
        if path.is_file()
    )
    actual_files = sorted(
        path.relative_to(actual_dir).as_posix()
        for path in actual_dir.rglob("*")
        if path.is_file()
    )
    if actual_files != expected_files:
        return [
            "Bundle file set mismatch: "
            f"expected={expected_files}, actual={actual_files}"
        ]

    mismatches: list[str] = []
    for relative_name in expected_files:
        actual_text = (actual_dir / relative_name).read_text(encoding="utf-8")
        golden_text = (golden_dir / relative_name).read_text(encoding="utf-8")
        if actual_text != golden_text:
            mismatches.append(f"Bundle content mismatch: {relative_name}")
    return mismatches


def parse_case_metadata(metadata_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in metadata_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("-") or ":" not in stripped:
            continue
        key, raw_value = stripped[1:].split(":", 1)
        values[key.strip()] = raw_value.strip().strip("`")
    return values


def run_python(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )


def ensure_success(result: subprocess.CompletedProcess[str], object_name: str, case: str) -> list[str]:
    if result.returncode == 0:
        return []

    errors = [
        f"Generator failed for {object_name}/{case} with exit code {result.returncode}"
    ]
    if result.stdout.strip():
        errors.append(f"stdout:\n{result.stdout.rstrip()}")
    if result.stderr.strip():
        errors.append(f"stderr:\n{result.stderr.rstrip()}")
    return errors


def run_watchdog_regression(case: str, update_golden: bool) -> list[str]:
    sample_dir = ROOT / "docs" / "golden-inputs" / "watchdog-timeout-audit-report" / case
    if not sample_dir.exists():
        return [f"Missing golden input sample: {sample_dir}"]

    findings_path = sample_dir / "findings.md"
    pack_path = sample_dir / "pack.md"
    golden_path = (
        ROOT
        / "docs"
        / "golden-outputs"
        / "watchdog-timeout-audit-report"
        / case
        / WATCHDOG_OUTPUT_NAME
    )

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_dir = Path(tmp_dir_name)
        actual_path = tmp_dir / WATCHDOG_OUTPUT_NAME
        result = run_python(
            [
                sys.executable,
                str(WATCHDOG_GENERATOR),
                "--findings",
                str(findings_path),
                "--pack",
                str(pack_path),
                "--output",
                str(actual_path),
            ]
        )
        errors = ensure_success(result, "watchdog-timeout-audit-report", case)
        if errors:
            return errors

        if update_golden:
            golden_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(actual_path, golden_path)
            return []

        return compare_file(actual_path, golden_path)


def run_incident_bundle_regression(case: str, update_golden: bool) -> list[str]:
    sample_dir = ROOT / "docs" / "golden-inputs" / "incident-case-bundle" / case
    if not sample_dir.exists():
        return [f"Missing golden input sample: {sample_dir}"]

    metadata_path = sample_dir / "case-metadata.md"
    metadata = parse_case_metadata(metadata_path)
    case_id = metadata.get("case id")
    title = metadata.get("case title")
    scenario = metadata.get("primary scenario")
    missing_fields = [
        field
        for field, value in (
            ("case id", case_id),
            ("case title", title),
            ("primary scenario", scenario),
        )
        if not value
    ]
    if missing_fields:
        return [
            f"Missing case metadata fields in {metadata_path}: {', '.join(missing_fields)}"
        ]

    golden_dir = ROOT / "docs" / "golden-outputs" / "incident-case-bundle" / case

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        output_root = Path(tmp_dir_name)
        result = run_python(
            [
                sys.executable,
                str(INCIDENT_GENERATOR),
                case_id,
                "--title",
                title,
                "--scenario",
                scenario,
                "--output-root",
                str(output_root),
                "--force",
            ]
        )
        errors = ensure_success(result, "incident-case-bundle", case)
        if errors:
            return errors

        actual_dir = output_root / case_id
        if update_golden:
            if golden_dir.exists():
                shutil.rmtree(golden_dir)
            shutil.copytree(actual_dir, golden_dir)
            return []

        return compare_bundle(actual_dir, golden_dir)


def run_single_object(object_name: str, case: str, update_golden: bool) -> list[str]:
    if object_name == "watchdog-timeout-audit-report":
        return run_watchdog_regression(case=case, update_golden=update_golden)
    if object_name == "incident-case-bundle":
        return run_incident_bundle_regression(case=case, update_golden=update_golden)
    return [f"Unsupported object: {object_name}"]


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.check and args.update_golden:
        print("Cannot combine --check and --update-golden", file=sys.stderr)
        return 2

    case = args.case or "minimal"
    selected_objects = [args.object] if args.object else list(ALLOWED_OBJECTS)
    update_golden = bool(args.update_golden)
    success_prefix = "UPDATED" if update_golden else "PASS"

    overall_errors: list[str] = []
    for object_name in selected_objects:
        errors = run_single_object(
            object_name=object_name,
            case=case,
            update_golden=update_golden,
        )
        if errors:
            overall_errors.extend(errors)
            continue
        print(f"{success_prefix} {object_name}/{case}")

    if overall_errors:
        for error in overall_errors:
            print(error, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
