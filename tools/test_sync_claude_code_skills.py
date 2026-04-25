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
