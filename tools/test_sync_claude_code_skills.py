from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "sync_claude_code_skills.py"
PYTHON = sys.executable


class SyncClaudeCodeSkillsOnlyTests(unittest.TestCase):
    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, str(SCRIPT), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
        )

    def test_stale_check_reports_managed_and_stale_target_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target_root = Path(temp_dir)
            managed_source = ROOT / "skills" / "orchestration" / "SKILL.md"
            managed_target = target_root / "skills" / "orchestration" / "SKILL.md"
            stale_target = target_root / "skills" / "stale-skill" / "SKILL.md"
            ignored_target = target_root / "other" / "ignored" / "SKILL.md"

            managed_target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(managed_source, managed_target)
            stale_target.parent.mkdir(parents=True, exist_ok=True)
            stale_target.write_text("# stale\n", encoding="utf-8")
            ignored_target.parent.mkdir(parents=True, exist_ok=True)
            ignored_target.write_text("# ignored\n", encoding="utf-8")

            result = self.run_script("--target-root", temp_dir, "--stale-check")

        current_source_skills = len(list((ROOT / "skills").rglob("SKILL.md")))

        self.assertEqual(result.returncode, 0)
        self.assertIn("STALE-CHECK", result.stdout)
        self.assertIn(f"TARGET ROOT: {target_root.as_posix()}", result.stdout)
        self.assertIn("FOUND TARGET SKILLS: 2", result.stdout)
        self.assertIn(f"CURRENT SOURCE SKILLS: {current_source_skills}", result.stdout)
        self.assertIn(f"- target: {managed_target.as_posix()}", result.stdout)
        self.assertIn("  status: managed", result.stdout)
        self.assertIn(f"- target: {stale_target.as_posix()}", result.stdout)
        self.assertIn("  status: stale", result.stdout)
        self.assertNotIn(ignored_target.as_posix(), result.stdout)
        self.assertIn("SUMMARY", result.stdout)
        self.assertIn("- total: 2", result.stdout)
        self.assertIn("- managed: 1", result.stdout)
        self.assertIn("- stale: 1", result.stdout)

    def test_stale_check_on_missing_target_root_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target_root = Path(temp_dir) / "missing-root"

            result = self.run_script("--target-root", str(target_root), "--stale-check")

            self.assertEqual(result.returncode, 0)
            self.assertIn("FOUND TARGET SKILLS: 0", result.stdout)
            self.assertIn("- total: 0", result.stdout)
            self.assertIn("- managed: 0", result.stdout)
            self.assertIn("- stale: 0", result.stdout)
            self.assertFalse(target_root.exists())

    def test_stale_check_conflicts_with_inspect(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(
                "--target-root",
                temp_dir,
                "--stale-check",
                "--inspect",
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("Cannot combine --stale-check and --inspect.", result.stderr)

    def test_stale_check_conflicts_with_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(
                "--target-root",
                temp_dir,
                "--stale-check",
                "--dry-run",
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("Cannot combine --stale-check and --dry-run.", result.stderr)

    def test_stale_check_conflicts_with_force(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(
                "--target-root",
                temp_dir,
                "--stale-check",
                "--force",
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("Cannot combine --stale-check and --force.", result.stderr)

    def test_stale_check_conflicts_with_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(
                "--target-root",
                temp_dir,
                "--stale-check",
                "--only",
                "orchestration",
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("Cannot combine --stale-check and --only.", result.stderr)

    def test_inspect_only_filters_to_named_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(
                "--target-root",
                temp_dir,
                "--inspect",
                "--only",
                "orchestration",
            )

        self.assertEqual(result.returncode, 0)
        self.assertIn("FOUND 1 skills", result.stdout)
        self.assertIn("skills/orchestration/SKILL.md", result.stdout)
        self.assertNotIn("skills/incident-investigation/SKILL.md", result.stdout)

    def test_dry_run_only_filters_to_named_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(
                "--target-root",
                temp_dir,
                "--dry-run",
                "--only",
                "orchestration",
            )

        self.assertEqual(result.returncode, 0)
        self.assertIn("FOUND 1 skills", result.stdout)
        self.assertIn("PLAN COPY skills/orchestration/SKILL.md", result.stdout)
        self.assertNotIn("skills/incident-investigation/SKILL.md", result.stdout)

    def test_sync_only_copies_named_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target_root = Path(temp_dir)
            result = self.run_script(
                "--target-root",
                temp_dir,
                "--only",
                "orchestration",
                "--force",
            )

            copied_skill = target_root / "skills" / "orchestration" / "SKILL.md"
            other_skill = target_root / "skills" / "incident-investigation" / "SKILL.md"

            self.assertTrue(copied_skill.exists())
            self.assertFalse(other_skill.exists())

        self.assertEqual(result.returncode, 0)
        self.assertIn("SYNCED skills/orchestration/SKILL.md", result.stdout)
        self.assertNotIn("skills/incident-investigation/SKILL.md", result.stdout)

    def test_unknown_only_skill_fails_with_available_list(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(
                "--target-root",
                temp_dir,
                "--dry-run",
                "--only",
                "does-not-exist",
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unknown skill: does-not-exist", result.stderr)
        self.assertIn("Available skills:", result.stderr)
        self.assertIn("orchestration", result.stderr)

    def test_duplicate_only_fails_with_clear_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(
                "--target-root",
                temp_dir,
                "--dry-run",
                "--only",
                "orchestration",
                "--only",
                "incident-investigation",
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("Cannot specify --only more than once.", result.stderr)

    def test_dry_run_without_only_preserves_full_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script("--target-root", temp_dir, "--dry-run")

        self.assertEqual(result.returncode, 0)
        self.assertIn("FOUND 12 skills", result.stdout)
        self.assertIn("skills/orchestration/SKILL.md", result.stdout)
        self.assertIn("skills/incident-investigation/SKILL.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
