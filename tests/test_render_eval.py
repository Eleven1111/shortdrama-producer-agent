"""Local regression cases for the rendering A/B score pipeline."""

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'eval' / 'render_loop'))
import aggregate
import run_ab


class RenderEvalTest(unittest.TestCase):
    def setUp(self):
        stack = contextlib.ExitStack()
        self.addCleanup(stack.close)
        temp = stack.enter_context(tempfile.TemporaryDirectory())
        self.output = Path(temp)
        stack.enter_context(patch.object(run_ab, 'OUT', temp))
        stack.enter_context(patch.object(aggregate, 'OUT', temp))
        stack.enter_context(contextlib.redirect_stdout(io.StringIO()))

    def write(self, name, data):
        (self.output / name).write_text(json.dumps(data), encoding='utf-8')

    def read(self, name):
        return json.loads((self.output / name).read_text(encoding='utf-8'))

    def make_sheet(self, slots):
        results = []
        for case, arm, available in slots:
            tag = f'{case}{arm}-original'
            path = self.output / f'{tag}.mp4'
            if available:
                path.write_bytes(tag.encode())
            results.append({
                'case_id': case, 'arm': arm, 'job_id': tag,
                'status': 'ok' if available else 'awaiting_human',
                'video': str(path),
            })
        self.write('render_results.json', results)
        run_ab.sheet()
        return self.read('grading_sheet.json'), self.read('_blind_key.json')

    def test_sheet_uses_anonymous_paths_for_available_videos(self):
        rows, key = self.make_sheet([('c01', 'A', True), ('c01', 'B', False)])
        for row in rows:
            sid = row['sample_id']
            entry = key[sid]
            self.assertNotIn('arm', row)
            self.assertNotIn('case_id', row)
            if entry['arm'] == 'A':
                path = self.output / row['video']
                self.assertEqual(path.name, f'{sid}.mp4')
                self.assertNotIn('c01', row['video'])
                self.assertEqual(path.read_bytes(), b'c01A-original')
            else:
                self.assertIsNone(row['video'])

    def test_only_complete_matched_cases_affect_the_result(self):
        rows, key = self.make_sheet([
            ('complete', 'A', True), ('complete', 'B', True),
            ('partial', 'A', True), ('partial', 'B', True),
            ('absent', 'A', True), ('absent', 'B', False),
            ('left', 'A', True), ('right', 'B', True),
            ('mismatch', 'A', True), ('mismatch', 'B', True),
        ])
        for row in rows:
            entry = key[row['sample_id']]
            case, arm = entry['case_id'], entry['arm']
            row['grader_type'] = 'human'
            row['scores'] = {item: 'n/a' for item in run_ab.RUBRIC_ITEMS}
            row['scores']['duration'] = 'pass' if arm == 'A' else 'fail'
            if case == 'partial' and arm == 'B':
                row['scores']['shot_count'] = ''
            if case == 'mismatch' and arm == 'B':
                row['scores']['shot_count'] = 'pass'
        self.write('grading_sheet.json', rows)

        aggregate.main()

        result = self.read('ab_summary.json')
        self.assertEqual(result['pair_count'], 1)
        self.assertEqual(result['mean_defects'], {'A': 0.0, 'B': 1.0})
        self.assertEqual(set(result['incomplete_cases']),
                         {'partial', 'absent', 'left', 'right', 'mismatch'})

    def test_no_paired_cases_produces_no_effect_estimate(self):
        self.make_sheet([('left', 'A', True), ('right', 'B', True)])
        aggregate.main()
        result = self.read('ab_summary.json')
        self.assertEqual(result['pair_count'], 0)
        self.assertEqual(result['mean_defects'], {})
        self.assertEqual(set(result['incomplete_cases']), {'left', 'right'})

    def test_each_probe_is_scored(self):
        for case in run_ab.load_cases():
            self.assertLessEqual(set(case['probes']), set(run_ab.RUBRIC_ITEMS))


if __name__ == '__main__':
    unittest.main()
