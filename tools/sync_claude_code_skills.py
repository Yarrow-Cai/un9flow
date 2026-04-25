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
    return parser


def display_path(path: Path) -> str:
    return path.as_posix()


def discover_skill_files() -> list[Path]:
    return sorted(path for path in SKILLS_ROOT.rglob("SKILL.md") if path.is_file())


def target_path_for(skill_file: Path, target_root: Path) -> Path:
    return target_root / skill_file.relative_to(ROOT)


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
        print("DRY-RUN")
        print(f"FOUND {len(skill_files)} skills")
        for skill_file in skill_files:
            source_label = display_path(skill_file.relative_to(ROOT))
            target_label = display_path(target_path_for(skill_file, target_root))
            print(f"PLAN COPY {source_label} -> {target_label}")
        return 0

    synced = 0
    skipped = 0
    failed = 0

    for skill_file in skill_files:
        destination = target_path_for(skill_file, target_root)
        source_label = display_path(skill_file.relative_to(ROOT))
        target_label = display_path(destination)

        if destination.exists() and not force:
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
    target_root = Path(args.target_root)
    skill_files = discover_skill_files()
    return sync_skill_files(
        skill_files=skill_files,
        target_root=target_root,
        dry_run=bool(args.dry_run),
        force=bool(args.force),
    )


if __name__ == "__main__":
    raise SystemExit(main())
