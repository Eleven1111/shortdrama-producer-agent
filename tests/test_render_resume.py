import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'eval/render_loop'))
import render_adapter
import run_ab


CONFIG = {'model': 'test-endpoint', 'ratio': '9:16', 'duration': 8}


class RenderResumeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        key = patch.dict(os.environ, {'ARK_API_KEY': 'test-only'})
        key.start()
        self.addCleanup(key.stop)

    def render(self):
        return render_adapter.render_ark('A quiet street.', 'c01A', self.tmp.name, **CONFIG)

    def test_restart_only_polls_and_preserves_settings(self):
        with patch.object(render_adapter.urllib.request, 'urlopen', side_effect=[
            io.BytesIO(b'{"id":"task-01"}'), KeyboardInterrupt(),
        ]) as request:
            with self.assertRaises(KeyboardInterrupt):
                self.render()
        post = request.call_args_list[0].args[0]
        self.assertEqual(post.get_method(), 'POST')
        payload = json.loads(post.data)
        self.assertEqual(payload, {**CONFIG, 'content': [{'type': 'text', 'text': 'A quiet street.'}]})

        with patch.object(render_adapter.urllib.request, 'urlopen', side_effect=[
            io.BytesIO(b'{"status":"succeeded","duration":8,"content":{"video_url":"https://example.test/v"}}'),
            io.BytesIO(b'simulated video'),
        ]) as request:
            result = self.render()
            self.assertEqual(self.render(), result)
        self.assertEqual(request.call_count, 2)
        poll = request.call_args_list[0].args[0]
        self.assertEqual(poll.get_method(), 'GET')
        self.assertTrue(poll.full_url.endswith('/task-01'))
        self.assertEqual(result['config'], CONFIG)
        self.assertEqual(result['reported'], {'duration': 8})
        self.assertEqual(Path(result['video']).read_bytes(), b'simulated video')

    def test_lost_post_response_never_reposts(self):
        with patch.object(render_adapter.urllib.request, 'urlopen', side_effect=TimeoutError) as request:
            with self.assertRaises(TimeoutError):
                self.render()
            with self.assertRaisesRegex(render_adapter.RenderError, '提交状态未知'):
                self.render()
        self.assertEqual(request.call_count, 1)

    def test_run_refuses_parameter_drift_before_network_call(self):
        (self.root / 'prompts.todo.json').write_text('[]', encoding='utf-8')
        with patch.object(run_ab, 'OUT', self.tmp.name):
            run_ab.do_render('ark', config=CONFIG)
            with self.assertRaisesRegex(SystemExit, '参数已冻结'):
                run_ab.do_render('ark', config={**CONFIG, 'duration': 10})
            (self.root / 'prompts.todo.json').write_text(
                '[{"prompt":"changed after the first run"}]', encoding='utf-8'
            )
            with self.assertRaisesRegex(SystemExit, '参数已冻结'):
                run_ab.do_render('ark', config=CONFIG)
