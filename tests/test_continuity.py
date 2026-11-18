"""Regression cases for the sequence gate."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.continuity_check import check, parse_shots


def shot(n, total, start="钥匙在桌上", end="钥匙在桌上", transition="—"):
    lines = [f"# shot {n} / {total} | 场 1 | 衔接: {transition}"]
    if start is not None:
        lines.append(f"# start state: {start}")
    if end is not None:
        lines.append(f"# end state: {end}")
    return "\n".join(lines)


class ContinuityTest(unittest.TestCase):
    def test_checks_both_required_states_on_single_shot(self):
        errors, _ = check(parse_shots(shot(1, 1, start=None, end=" ")))
        self.assertEqual(2, len(errors))
        self.assertIn("start state", errors[0])
        self.assertIn("end state", errors[1])

    def test_accepts_indented_later_batch_and_ignores_body_reference(self):
        block = "\n".join([
            shot(7, 9, transition="延续 from shot 6"),
            shot(8, 9, transition="延续 from shot 7"),
            "Match the lighting from shot 3.",
        ])
        errors, warnings = check(parse_shots("\r\n".join(f"  {line}" for line in block.splitlines())))
        self.assertEqual([], errors)
        self.assertIn("本批解析到 2 镜", warnings[0])

    def test_rejects_gaps_repeats_and_reverse_order(self):
        for left, right in [(1, 3), (2, 2), (3, 2)]:
            with self.subTest(pair=(left, right)):
                errors, _ = check(parse_shots(f"{shot(left, 3)}\n{shot(right, 3)}"))
                self.assertTrue(any("批次内镜号必须连续" in error for error in errors))

    def test_rejects_wrong_source_on_first_shot_in_later_batch(self):
        errors, _ = check(parse_shots(shot(7, 9, transition="延续 from shot 3")))
        self.assertTrue(any("from shot 3" in error for error in errors))

    def test_rejects_inconsistent_totals_and_out_of_range_shots(self):
        errors, _ = check(parse_shots(f"{shot(2, 3)}\n{shot(3, 2)}"))
        self.assertTrue(any("与首镜" in error for error in errors))
        self.assertTrue(any("镜号必须在" in error for error in errors))

    def test_detects_structured_conflict_even_with_shared_anchors(self):
        first = shot(1, 2) + '\n# end continuity: {"prop.key.holder":"table"}\n<<<girl>>>'
        second = shot(2, 2) + '\n# start continuity: {"prop.key.holder":"girl"}\n<<<girl>>>'
        errors, _ = check(parse_shots(f"{first}\n{second}"))
        self.assertTrue(any("prop.key.holder 状态冲突" in error for error in errors))

    def test_accepts_explicit_time_jump_with_changed_prop_holder(self):
        first = shot(1, 2) + '\n# end continuity: {"prop.key.holder":"table"}'
        second = shot(2, 2, transition="时间跳跃 from shot 1")
        second += '\n# start continuity: {"prop.key.holder":"girl"}'
        self.assertEqual(([], []), check(parse_shots(f"{first}\n{second}")))

    def test_rejects_invalid_structured_values_and_duplicate_state_lines(self):
        prompt = shot(1, 1) + '\n# start state: 女孩闭眼\n# end continuity: {"item":23}'
        errors, _ = check(parse_shots(prompt))
        self.assertEqual(2, len(errors))

    def test_reports_different_prose_as_for_human_review(self):
        first = shot(1, 2, end="Peter lowers the lantern")
        second = shot(2, 2, start="He drops his lamp")
        errors, warnings = check(parse_shots(f"{first}\n{second}"))
        self.assertEqual([], errors)
        self.assertTrue(any("人工核对" in warn for warn in warnings))

    def test_allows_version_changes_and_detects_case_changes(self):
        first = shot(1, 2) + "\n<<<girl>>>"
        second = shot(2, 2) + "\n<<<girl_v2>>>"
        self.assertEqual(([], []), check(parse_shots(f"{first}\n{second}")))
        _, warnings = check(parse_shots(f"{first}\n{second.replace('girl', 'Girl')}"))
        self.assertTrue(any("大小写漂移" in warn for warn in warnings))


if __name__ == "__main__":
    unittest.main()
