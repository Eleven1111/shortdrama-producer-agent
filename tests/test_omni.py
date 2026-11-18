import json
from pathlib import Path
import subprocess
import sys
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/omni_check.py"
PROMPT = "Single continuous shot. 16:9. Duration: 12s. [0-12s] The light dims."


class OmniDeliveryTests(unittest.TestCase):
    def run_check(self, text, version):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--version", version, "--json"],
            input=text, capture_output=True, text=True, check=False,
        )
        return result.returncode, json.loads(result.stdout)

    def test_same_prompt_checked_against_target_version(self):
        self.assertEqual(self.run_check(PROMPT, "1.1")[0], 1)
        self.assertEqual(self.run_check(PROMPT, "1.2-flash")[0], 0)

    def test_short_invalid_shot_is_not_silently_dropped(self):
        status, report = self.run_check(f"# shot 1\n{PROMPT}\n# shot 2\nHard cut.", "1.2-flash")
        self.assertEqual(status, 1)
        self.assertEqual(report["prompts"], 2)

    def test_extend_does_not_bypass_single_generation_limit(self):
        self.assertEqual(self.run_check(f"{PROMPT} Extend later.", "1.1")[0], 1)
