#!/usr/bin/env python3
"""渲染适配层：把「提交一段 prompt → 拿到一个视频文件」这件事收敛到一个接口。

提供三种后端：
  dry      —— 不调任何 API，产出占位结果。用于验证整条管道跑通（默认）。
  ark      —— 火山方舟 Seedance（环境变量 ARK_API_KEY）。
  manual   —— 人工在平台粘 prompt、把成片放进 out/videos/<job_id>.mp4，脚本负责登记与校验。

刻意不内置任何绕过鉴权的路径。没有凭据就用 manual —— 慢，但不滥用他人配额。
"""
import hashlib, json, os, shutil, tempfile, time, urllib.request

ARK_ENDPOINT = 'https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks'


class RenderError(RuntimeError):
    pass


def write_json(path, value):
    """Replace a checkpoint only after the complete JSON has been flushed."""
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                     dir=os.path.dirname(path), delete=False) as f:
        tmp = f.name
        try:
            json.dump(value, f, ensure_ascii=False, indent=1)
            f.flush()
            os.fsync(f.fileno())
            os.replace(tmp, path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)


def _job_id(prompt, tag, config=None):
    payload = json.dumps([prompt, config], sort_keys=True).encode('utf-8') if config else prompt.encode('utf-8')
    return '%s-%s' % (tag, hashlib.sha256(payload).hexdigest()[:16])


def render_dry(prompt, tag, outdir, **kw):
    """不出片，只登记。用于验证管道结构、用例覆盖、盲测映射是否正确。"""
    jid = _job_id(prompt, tag)
    return {'job_id': jid, 'backend': 'dry', 'status': 'skipped',
            'video': None, 'prompt_len': len(prompt),
            'note': 'dry-run：未渲染，管道结构验证用'}


def render_ark(prompt, tag, outdir, model, ratio, duration, poll_interval=10, timeout=900):
    """Submit once, checkpoint the task ID, and resume polling on the next run."""
    key = os.environ.get('ARK_API_KEY')
    if not key:
        raise RenderError('缺少 ARK_API_KEY')

    config = {'model': model, 'ratio': ratio, 'duration': duration}
    jid = _job_id(prompt, tag, config)
    journal_dir = os.path.join(outdir, 'ark-tasks')
    os.makedirs(journal_dir, exist_ok=True)
    checkpoint = os.path.join(journal_dir, jid + '.json')
    base = {'job_id': jid, 'backend': 'ark', 'config': config, 'video': None}
    headers = {'Authorization': 'Bearer %s' % key}

    if os.path.exists(checkpoint):
        with open(checkpoint, encoding='utf-8') as f:
            saved = json.load(f)
        task_id = saved.get('task_id')
        if not task_id:
            raise RenderError('提交状态未知，请在方舟控制台核对后恢复任务：%s' % checkpoint)
        if saved['status'] in ('failed', 'cancelled', 'expired'):
            return saved
        if saved['status'] == 'ok' and os.path.isfile(saved['video']):
            return saved
    else:
        # A lost POST response does not establish that the server rejected the request.
        # Reserve the slot before POST so a retry cannot create a second paid task.
        write_json(checkpoint, {**base, 'status': 'submitting'})
        body = json.dumps({**config, 'content': [{'type': 'text', 'text': prompt}]}).encode('utf-8')
        req = urllib.request.Request(ARK_ENDPOINT, data=body, method='POST', headers={
            **headers, 'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=60) as response:
            task_id = json.load(response).get('id')
        if not task_id:
            raise RenderError('提交响应缺少任务 ID，请核对方舟控制台：%s' % checkpoint)
        write_json(checkpoint, {**base, 'status': 'submitted', 'task_id': task_id})

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        req = urllib.request.Request('%s/%s' % (ARK_ENDPOINT, task_id), headers=headers)
        with urllib.request.urlopen(req, timeout=60) as response:
            task = json.load(response)
        status = task.get('status')
        if status == 'succeeded':
            url = (task.get('content') or {}).get('video_url')
            if not url:
                raise RenderError('任务成功但无 video_url：%s' % task_id)
            path = os.path.join(outdir, 'videos', '%s.mp4' % jid)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            # Publish only a complete download. A retry reuses the remote task.
            with urllib.request.urlopen(url, timeout=60) as source, open(path + '.part', 'wb') as target:
                shutil.copyfileobj(source, target)
            os.replace(path + '.part', path)
            result = {**base, 'status': 'ok', 'video': path, 'task_id': task_id,
                      'reported': {k: task[k] for k in config if k in task}}
            write_json(checkpoint, result)
            return result
        if status in ('failed', 'cancelled', 'expired'):
            result = {**base, 'status': status, 'task_id': task_id, 'error': task.get('error')}
            write_json(checkpoint, result)
            return result
        time.sleep(poll_interval)
    raise RenderError('轮询超时（%ds）task_id=%s；重跑会继续查询' % (timeout, task_id))


def render_manual(prompt, tag, outdir, **kw):
    """人工渲染：脚本只登记 prompt 与期望落盘路径，成片由人放进去。

    重跑时若文件已存在则标记 ok —— 支持分批人工补齐。
    """
    jid = _job_id(prompt, tag, kw or None)
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
