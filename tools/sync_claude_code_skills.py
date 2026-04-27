#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"


class SingleOnlyAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest, None) is not None:
            parser.exit(2, "Cannot specify --only more than once.\n")
        setattr(namespace, self.dest, values)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sync skills/**/SKILL.md into a Claude Code target root."
    )
    parser.add_argument(
        "--target-root",
        required=True,
        help="Destination root that will receive mirrored skills/**/SKILL.md files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned copy operations without writing files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing target files instead of skipping them.",
    )
    parser.add_argument(
        "--inspect",
        action="store_true",
        help="Print a static inventory of source and target skill files without writing files.",
    )
    parser.add_argument(
        "--only",
        action=SingleOnlyAction,
        help="Sync or inspect only the skill whose directory name exactly matches <skill-name>.",
    )
    parser.add_argument(
        "--stale-check",
        action="store_true",
        help="Inspect target skills/**/SKILL.md files and report whether each one is managed or stale.",
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Delete stale target skills/**/SKILL.md files without removing directories or other files.",
    )
    parser.add_argument(
        "--prune-advice",
        action="store_true",
        help="Inspect target skills/**/SKILL.md files and print cleanup advice for stale targets only.",
    )
    return parser


def display_path(path: Path) -> str:
    return path.as_posix()


def discover_skill_files() -> list[Path]:
    return sorted(path for path in SKILLS_ROOT.rglob("SKILL.md") if path.is_file())


def skill_name_for(skill_file: Path) -> str:
    return skill_file.parent.name


def select_skill_files(skill_files: list[Path], only: str | None) -> list[Path]:
    if only is None:
        return skill_files

    selected = [skill_file for skill_file in skill_files if skill_name_for(skill_file) == only]
    if selected:
        return selected

    available_skills = ", ".join(skill_name_for(skill_file) for skill_file in skill_files)
    print(f"Unknown skill: {only}", file=sys.stderr)
    print(f"Available skills: {available_skills}", file=sys.stderr)
    raise SystemExit(2)


def target_path_for(skill_file: Path, target_root: Path) -> Path:
    return target_root / skill_file.relative_to(ROOT)


def discover_target_skill_files(target_root: Path) -> list[Path]:
    target_skills_root = target_root / "skills"
    return sorted(path for path in target_skills_root.rglob("SKILL.md") if path.is_file())


def inspect_skill_files(skill_files: list[Path], target_root: Path) -> int:
    if not skill_files:
        print("No skill files found.", file=sys.stderr)
        return 2

    existing = 0
    missing = 0

    print("INSPECT")
    print(f"SOURCE ROOT: {display_path(SKILLS_ROOT.relative_to(ROOT))}")
    print(f"TARGET ROOT: {display_path(target_root)}")
    print(f"FOUND {len(skill_files)} skills")

    for skill_file in skill_files:
        destination = target_path_for(skill_file, target_root)
        source_label = display_path(skill_file.relative_to(ROOT))
        target_label = display_path(destination)
        status = "existing" if destination.exists() else "missing"
        if status == "existing":
            existing += 1
        else:
            missing += 1
        print(f"- source: {source_label}")
        print(f"  target: {target_label}")
        print(f"  status: {status}")

    print("SUMMARY")
    print(f"- total: {len(skill_files)}")
    print(f"- existing: {existing}")
    print(f"- missing: {missing}")
    return 0


def stale_check_skill_files(skill_files: list[Path], target_root: Path) -> int:
    target_skill_files = discover_target_skill_files(target_root)
    managed_targets = {
        target_path_for(skill_file, target_root).resolve() for skill_file in skill_files
    }

    managed = 0
    stale = 0

    print("STALE-CHECK")
    print(f"TARGET ROOT: {display_path(target_root)}")
    print(f"FOUND TARGET SKILLS: {len(target_skill_files)}")
    print(f"CURRENT SOURCE SKILLS: {len(skill_files)}")

    for target_skill_file in target_skill_files:
        target_label = display_path(target_skill_file)
        status = "managed" if target_skill_file.resolve() in managed_targets else "stale"
        if status == "managed":
            managed += 1
        else:
            stale += 1
        print(f"- target: {target_label}")
        print(f"  status: {status}")

    print("SUMMARY")
    print(f"- total: {len(target_skill_files)}")
    print(f"- managed: {managed}")
    print(f"- stale: {stale}")
    return 0


def prune_advice_skill_files(skill_files: list[Path], target_root: Path) -> int:
    target_skill_files = discover_target_skill_files(target_root)
    managed_targets = {
        target_path_for(skill_file, target_root).resolve() for skill_file in skill_files
    }
    stale_targets = [
        target_skill_file
        for target_skill_file in target_skill_files
        if target_skill_file.resolve() not in managed_targets
    ]

    print("PRUNE-ADVICE")
    print(f"TARGET ROOT: {display_path(target_root)}")
    print(f"TOTAL TARGET SKILLS: {len(target_skill_files)}")
    print(f"STALE TARGETS: {len(stale_targets)}")

    for target_skill_file in stale_targets:
        print(f"- target: {display_path(target_skill_file)}")
        print("  status: stale")
        print("  advice: consider-cleanup")

    print("SUMMARY")
    print(f"- total: {len(target_skill_files)}")
    print(f"- stale: {len(stale_targets)}")
    print(f"- consider-cleanup: {len(stale_targets)}")
    return 0


def prune_skill_files(skill_files: list[Path], target_root: Path) -> int:
    target_skill_files = discover_target_skill_files(target_root)
    managed_targets = {
        target_path_for(skill_file, target_root).resolve() for skill_file in skill_files
    }

    pruned = 0
    skipped = 0
    failed = 0

    for target_skill_file in target_skill_files:
        target_label = display_path(target_skill_file)
        if target_skill_file.resolve() in managed_targets:
            print(f"SKIPPED {target_label}: managed")
            skipped += 1
            continue

        try:
            target_skill_file.unlink()
        except OSError as exc:
            print(f"FAILED {target_label}: {exc}")
            failed += 1
            continue

        print(f"PRUNED {target_label}")
        pruned += 1

    print(f"SUMMARY: pruned {pruned}, skipped {skipped}, failed {failed}")
    return 0 if failed == 0 else 1


def classify_sync_action(destination: Path, force: bool) -> str:
    if not destination.exists():
        return "copy"
    if force:
        return "overwrite"
    return "skip"


def sync_skill_files(
    skill_files: list[Path],
    target_root: Path,
    dry_run: bool,
    force: bool,
) -> int:
    if not skill_files:
        print("No skill files found.", file=sys.stderr)
        return 2

    if dry_run:
        planned_copy = 0
        planned_skip = 0
        planned_overwrite = 0

        print("DRY-RUN")
        print(f"FOUND {len(skill_files)} skills")
        for skill_file in skill_files:
            destination = target_path_for(skill_file, target_root)
            source_label = display_path(skill_file.relative_to(ROOT))
            target_label = display_path(destination)
            action = classify_sync_action(destination, force)

            if action == "copy":
                print(f"PLAN COPY {source_label} -> {target_label}")
                planned_copy += 1
            elif action == "overwrite":
                print(f"PLAN OVERWRITE {source_label} -> {target_label}")
                planned_overwrite += 1
            else:
                print(f"PLAN SKIP {source_label} -> {target_label}")
                planned_skip += 1

        print(
            "SUMMARY: "
            f"planned_copy {planned_copy}, "
            f"planned_skip {planned_skip}, "
            f"planned_overwrite {planned_overwrite}"
        )
        return 0

    synced = 0
    skipped = 0
    failed = 0

    for skill_file in skill_files:
        destination = target_path_for(skill_file, target_root)
        source_label = display_path(skill_file.relative_to(ROOT))
        target_label = display_path(destination)
        action = classify_sync_action(destination, force)

        if action == "skip":
            print(f"SKIPPED {source_label} -> {target_label}", file=sys.stderr)
            skipped += 1
            continue

        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(skill_file, destination)
        except OSError as exc:
            print(
                f"FAILED {source_label} -> {target_label}: {exc}",
                file=sys.stderr,
            )
            failed += 1
            continue

        print(f"SYNCED {source_label} -> {target_label}")
        synced += 1

    print(f"SUMMARY: synced {synced}, skipped {skipped}, failed {failed}")
    return 0 if failed == 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.inspect and args.dry_run:
        print("Cannot combine --inspect and --dry-run.", file=sys.stderr)
        return 2
    if args.inspect and args.force:
        print("Cannot combine --inspect and --force.", file=sys.stderr)
        return 2
    if args.prune and args.inspect:
        print("Cannot combine --prune and --inspect.", file=sys.stderr)
        return 2
    if args.prune and args.dry_run:
        print("Cannot combine --prune and --dry-run.", file=sys.stderr)
        return 2
    if args.prune and args.stale_check:
        print("Cannot combine --prune and --stale-check.", file=sys.stderr)
        return 2
    if args.prune and args.prune_advice:
        print("Cannot combine --prune and --prune-advice.", file=sys.stderr)
        return 2
    if args.prune and args.force:
        print("Cannot combine --prune and --force.", file=sys.stderr)
        return 2
    if args.prune and args.only is not None:
        print("Cannot combine --prune and --only.", file=sys.stderr)
        return 2
    if args.stale_check and args.inspect:
        print("Cannot combine --stale-check and --inspect.", file=sys.stderr)
        return 2
    if args.stale_check and args.dry_run:
        print("Cannot combine --stale-check and --dry-run.", file=sys.stderr)
        return 2
    if args.stale_check and args.force:
        print("Cannot combine --stale-check and --force.", file=sys.stderr)
        return 2
    if args.stale_check and args.only is not None:
        print("Cannot combine --stale-check and --only.", file=sys.stderr)
        return 2
    if args.prune_advice and args.stale_check:
        print("Cannot combine --prune-advice and --stale-check.", file=sys.stderr)
        return 2
    if args.prune_advice and args.inspect:
        print("Cannot combine --prune-advice and --inspect.", file=sys.stderr)
        return 2
    if args.prune_advice and args.dry_run:
        print("Cannot combine --prune-advice and --dry-run.", file=sys.stderr)
        return 2
    if args.prune_advice and args.force:
        print("Cannot combine --prune-advice and --force.", file=sys.stderr)
        return 2
    if args.prune_advice and args.only is not None:
        print("Cannot combine --prune-advice and --only.", file=sys.stderr)
        return 2

    target_root = Path(args.target_root)
    all_skill_files = discover_skill_files()

    if args.stale_check:
        return stale_check_skill_files(skill_files=all_skill_files, target_root=target_root)
    if args.prune_advice:
        return prune_advice_skill_files(skill_files=all_skill_files, target_root=target_root)
    if args.prune:
        return prune_skill_files(skill_files=all_skill_files, target_root=target_root)

    skill_files = select_skill_files(all_skill_files, args.only)

    if args.inspect:
        return inspect_skill_files(skill_files=skill_files, target_root=target_root)

    return sync_skill_files(
        skill_files=skill_files,
        target_root=target_root,
        dry_run=bool(args.dry_run),
        force=bool(args.force),
    )


if __name__ == "__main__":
    raise SystemExit(main())
