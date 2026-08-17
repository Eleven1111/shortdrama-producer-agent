#!/usr/bin/env python3
"""渲染适配层：把「提交一段 prompt → 拿到一个视频文件」这件事收敛到一个接口。

提供三种后端：
  dry      —— 不调任何 API，产出占位结果。用于验证整条管道跑通（默认）。
  ark      —— 火山方舟 Seedance（环境变量 ARK_API_KEY）。
  manual   —— 人工在平台粘 prompt、把成片放进 out/videos/<job_id>.mp4，脚本负责登记与校验。

刻意不内置任何绕过鉴权的路径。没有凭据就用 manual —— 慢，但不滥用他人配额。
"""
import hashlib, json, os, time, urllib.request, urllib.error

ARK_ENDPOINT = 'https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks'


class RenderError(RuntimeError):
    pass


def _job_id(prompt, tag):
    return '%s-%s' % (tag, hashlib.sha1(prompt.encode('utf-8')).hexdigest()[:10])


def render_dry(prompt, tag, outdir, **kw):
    """不出片，只登记。用于验证管道结构、用例覆盖、盲测映射是否正确。"""
    jid = _job_id(prompt, tag)
    return {'job_id': jid, 'backend': 'dry', 'status': 'skipped',
            'video': None, 'prompt_len': len(prompt),
            'note': 'dry-run：未渲染，管道结构验证用'}


def render_ark(prompt, tag, outdir, model='doubao-seedance-1-0-pro', ratio='21:9',
               duration=10, poll_interval=10, timeout=900, **kw):
    """火山方舟 Seedance。需要 ARK_API_KEY。

    注意：真实调用会消耗付费额度 —— 调用方必须已获得使用者明确同意。
    """
    key = os.environ.get('ARK_API_KEY')
    if not key:
        raise RenderError('缺少 ARK_API_KEY；改用 --backend manual 或先配置凭据')

    jid = _job_id(prompt, tag)
    body = json.dumps({
        'model': model,
        'content': [{'type': 'text',
                     'text': '%s --ratio %s --duration %d' % (prompt, ratio, duration)}],
    }).encode('utf-8')
    req = urllib.request.Request(ARK_ENDPOINT, data=body, method='POST', headers={
        'Authorization': 'Bearer %s' % key, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            task = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RenderError('提交失败 HTTP %s: %s' % (e.code, e.read()[:300]))

    task_id = task.get('id')
    if not task_id:
        raise RenderError('响应缺少任务 id: %s' % json.dumps(task)[:300])

    # 轮询
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(poll_interval)
        q = urllib.request.Request('%s/%s' % (ARK_ENDPOINT, task_id),
                                   headers={'Authorization': 'Bearer %s' % key})
        with urllib.request.urlopen(q, timeout=60) as r:
            st = json.loads(r.read())
        status = st.get('status')
        if status == 'succeeded':
            url = (st.get('content') or {}).get('video_url')
            if not url:
                raise RenderError('任务成功但无 video_url: %s' % json.dumps(st)[:300])
            path = os.path.join(outdir, 'videos', '%s.mp4' % jid)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            urllib.request.urlretrieve(url, path)
            return {'job_id': jid, 'backend': 'ark', 'status': 'ok', 'video': path,
                    'task_id': task_id, 'model': model}
        if status in ('failed', 'cancelled'):
            return {'job_id': jid, 'backend': 'ark', 'status': status, 'video': None,
                    'task_id': task_id, 'error': st.get('error')}
    raise RenderError('轮询超时（%ds）task_id=%s' % (timeout, task_id))


def render_manual(prompt, tag, outdir, **kw):
    """人工渲染：脚本只登记 prompt 与期望落盘路径，成片由人放进去。

    重跑时若文件已存在则标记 ok —— 支持分批人工补齐。
    """
    jid = _job_id(prompt, tag)
    path = os.path.join(outdir, 'videos', '%s.mp4' % jid)
    prompt_path = os.path.join(outdir, 'prompts', '%s.txt' % jid)
    os.makedirs(os.path.dirname(prompt_path), exist_ok=True)
    with open(prompt_path, 'w', encoding='utf-8') as f:
        f.write(prompt)
    exists = os.path.exists(path)
    return {'job_id': jid, 'backend': 'manual',
            'status': 'ok' if exists else 'awaiting_human',
            'video': path if exists else None,
            'prompt_file': prompt_path,
            'note': None if exists else '请把成片保存为 %s' % path}


BACKENDS = {'dry': render_dry, 'ark': render_ark, 'manual': render_manual}


def render(prompt, tag, outdir, backend='dry', **kw):
    fn = BACKENDS.get(backend)
    if not fn:
        raise RenderError('未知后端 %r，可选：%s' % (backend, ', '.join(BACKENDS)))
    return fn(prompt, tag, outdir, **kw)
