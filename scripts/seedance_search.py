#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seedance_search.py — 零依赖 BM25 检索器（纯 Python stdlib）。
随 skill 分发，检索打包的 seedance_corpus.jsonl.gz（7,824 docs 真实生产范例）。

用法：
  python3 seedance_search.py "场景描述一句话" [topk]
  python3 seedance_search.py --style "风格关键词"
  python3 seedance_search.py --ref "角色/道具描述"

输出：JSON（stdout），含命中的真实范例（prompt 全文 + 结构字段 + gold 标记）。
"""
import gzip, json, math, os, pickle, re, sys
from collections import Counter

_HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(_HERE, 'seedance_corpus.jsonl.gz')
REGISTRY = os.path.join(_HERE, '..', 'references', 'reference_registry.json')
INDEX_CACHE = os.path.join(_HERE, '.bm25_index.pkl')
INDEX_VERSION = 2
MAX_CLEAN = 6000  # 单条范例默认给模型的字符上限；--full 输出全文
TOKEN_RE = re.compile(r"[A-Za-z0-9_\-']+")

def tokenize(text):
    return [t.lower() for t in TOKEN_RE.findall(text) if len(t) > 1]

class BM25:
    def __init__(self, corpus_path):
        self.docs = []
        with gzip.open(corpus_path, 'rt', errors='replace') as f:
            for line in f:
                if line.strip():
                    self.docs.append(json.loads(line))
        self.N = len(self.docs)
        self.k1, self.b = 1.5, 0.75
        if not self._load_cache(corpus_path):
            self._build()
            self._save_cache(corpus_path)

    def _build(self):
        self.df = Counter()
        self.doc_toks = []
        self.doc_lens = []
        for d in self.docs:
            toks = tokenize(d['prompt'])
            self.df.update(set(toks))
            self.doc_toks.append(Counter(toks))
            self.doc_lens.append(len(toks))
        self.avgdl = sum(self.doc_lens) / self.N if self.N else 1.0

    def _stamp(self, corpus_path):
        st = os.stat(corpus_path)
        return {'v': INDEX_VERSION, 'size': st.st_size, 'mtime': int(st.st_mtime), 'n': self.N}

    def _load_cache(self, corpus_path):
        """索引缓存命中则跳过重建。缓存损坏/过期一律静默回退到重建。"""
        try:
            with open(INDEX_CACHE, 'rb') as f:
                c = pickle.load(f)
            if c.get('stamp') != self._stamp(corpus_path):
                return False
            self.df, self.doc_toks = c['df'], c['doc_toks']
            self.doc_lens, self.avgdl = c['doc_lens'], c['avgdl']
            return True
        except Exception:
            return False

    def _save_cache(self, corpus_path):
        try:
            tmp = INDEX_CACHE + '.tmp'
            with open(tmp, 'wb') as f:
                pickle.dump({'stamp': self._stamp(corpus_path), 'df': self.df,
                             'doc_toks': self.doc_toks, 'doc_lens': self.doc_lens,
                             'avgdl': self.avgdl}, f, protocol=pickle.HIGHEST_PROTOCOL)
            os.replace(tmp, INDEX_CACHE)
        except Exception:
            pass  # 只读环境下降级为每次重建，不影响正确性

    def _idf(self, term):
        n = self.df.get(term, 0)
        return math.log(1 + (self.N - n + 0.5) / (n + 0.5))

    def search(self, query, topk=5):
        qw = Counter(tokenize(query))
        if not qw:
            return []
        scores = []
        for i in range(self.N):
            s = 0.0
            L = self.doc_lens[i]
            ct = self.doc_toks[i]
            for term, qtf in qw.items():
                tf = ct.get(term, 0)
                if tf:
                    idf = self._idf(term)
                    s += idf * (tf * (self.k1 + 1)) / (tf + self.k1 * (1 - self.b + self.b * L / self.avgdl)) * qtf
            if s > 0:
                scores.append((s, i))
        scores.sort(reverse=True)
        seen_folder = set()
        out = []
        for s, i in scores:
            d = self.docs[i]
            k = d['folder']
            if k in seen_folder:
                continue
            seen_folder.add(k)
            out.append({'score': round(s, 1), **d})
            if len(out) >= topk:
                break
        return out

# 只有「具体内容」段是版权风险（台词/歌词/发音表）；技术结构段全部保留 —— 它们正是学习目标。
_REDACT_SECTIONS = (
    'LYRICS AND MOUTH OWNERSHIP', 'LYRICS', 'DIALOGUE', 'SPEECH', 'VOICE LINES',
    'PRONUNCIATION GUIDE', 'SUBTITLES', 'SCRIPT',
)
_SECTION_RE = re.compile(r'^([A-Z][A-Z0-9 &/\'()-]{3,44})\s*$', re.M)
# 引号包裹的口语片段 —— 台词/歌词的内容特征。
# 必须「左引号起始 → 右引号结束」：英文所有格撇号(character's)用的是右单引号，
# 若把它当配对起点会把大量正常描写误判成台词。
_SPOKEN_RE = re.compile(r'“([^”\n]{6,160})”|"([^"\n]{6,160})"|‘([^’\n]{6,160})’')


def _spoken_hits(text):
    return [next(g for g in m.groups() if g is not None) for m in _SPOKEN_RE.finditer(text)]


def _redact_spoken(block, _title=''):
    """逐行剥离台词/歌词原文，保留结构骨架。

    段名黑名单穷举不完（APPROXIMATE AUDIO PHRASE MAP 这类会漏），故按内容特征判定。
    只替换引号内的文本，行本身与段头保留 —— 时间码结构（"0.0–1.0 SECONDS:"）正是
    模型要学的东西，不能连带删掉。
    """
    if len(_spoken_hits(block)) < 3:
        return block
    return _SPOKEN_RE.sub('“[lyrics omitted]”', block)
# 锚点内一定是资产标识符（完整 UUID / 8 位短 UUID / 资产名如 museum_after），
# 在锚点位置替换是精确的、不会误伤正文。
_ANCHOR_RE = re.compile(r'<<<([^<>]{1,80})>>>')
# video_1 / image_2 是 Seedance 语法占位符（音频载体、首帧图），必须原样保留
_SYNTAX_ANCHOR_RE = re.compile(r'^(?:video|image|frame|audio)_\d+$', re.I)

_CATEGORY_LABEL = {'character': 'CHARACTER', 'prop': 'PROP', 'environment': 'ENVIRONMENT'}
_registry = None
_proper_names = None

# registry 的 name 形如 char_CB_Vernon_v9 / loc_CB_kal_corridor_s135。中段既有专名
# (Vernon/Horace/Tika)，也有普通场景词 (corridor/office/night) —— 后者绝不能替换，
# 否则会毁掉正文语义。只匿名化专名。
_GENERIC_TOKENS = set('''
back front left right top side inner outer interior exterior int ext wide close full
workshop office commons corridor livingroom living room kitchen bathroom bedroom hall
lobby stair stairs street road park lot yard roof door window wall floor gate fence
night day dawn dusk morning evening insert test temp final draft copy alt new old
phone car cars van truck bike boat helicopter chopper gun guns knife bag moneybag bottle
glass table chair bed sofa desk box crate barrel poster sign light lights lamp
goon goons extras extra crowd guard guards cop cops police player players club house home
scene shot shots cut cuts take takes version final master main base ref refs
grain filmlook look element elements texture tone color colour contrast
king queen detective homeless builders dealers boss man woman boy girl kid
archi bomj mus rice lee
'''.split())


def _load_proper_names():
    """抽出正文中需要匿名化的角色专名。

    只取 char_* 条目里首字母大写的 token（人名特征：char_CB_Vernon_v9 → Vernon）。
    刻意不覆盖 loc_/prop_ 类：那些 token 与普通英文大量重合（apartment / pink /
    loft / opened），按名字替换会毁掉正文语义，而地点道具的身份敏感度远低于角色。
    这两类在 <<<uuid>>> 锚点层面已被精确匿名化，无误伤风险。

    词频不能用来做这个判断 —— 实测主角 cal 的文档频率 43.9%，比误伤词 pink 的
    8.5% 还高。
    """
    global _proper_names
    if _proper_names is not None:
        return _proper_names
    buckets = {}
    for v in _load_registry().values():
        name = v.get('name') or ''
        if not re.match(r'char', name, re.I):
            continue
        for tok in re.split(r'[_\-]', name)[1:]:      # 跳过 char 前缀本身
            t = tok.strip()
            if len(t) < 3 or not t[:1].isupper():      # 人名首字母大写
                continue
            if t.lower() in _GENERIC_TOKENS or t.upper() == 'CB':
                continue
            if not re.fullmatch(r"[A-Za-z][A-Za-z']*", t) or re.fullmatch(r'[vs]\d+\w*', t, re.I):
                continue
            buckets.setdefault(t.lower(), 'CHARACTER')
    _proper_names = buckets
    return _proper_names


def _load_registry():
    """uuid → category 映射（reference_registry.json）。缺失则退化为通用锚点标签。"""
    global _registry
    if _registry is None:
        try:
            with open(REGISTRY, encoding='utf-8') as f:
                _registry = json.load(f).get('refs', {})
        except Exception:
            _registry = {}
    return _registry


def anonymize_anchors(prompt):
    """把 <<<uuid>>> 换成 <<<CHARACTER_1>>> / <<<PROP_2>>> 之类的匿名锚点。

    保留「锚点在这个位置起结构作用」这一信息（模型要学的），同时不泄露源项目的
    具体角色/道具身份。同一 uuid 在同一文档内编号稳定。
    """
    reg = _load_registry()
    seen, counters = {}, Counter()

    def label_for(key, label):
        if key not in seen:
            counters[label] += 1
            seen[key] = '%s_%d' % (label, counters[label])
        return seen[key]

    def sub(m):
        key = m.group(1).strip()
        if _SYNTAX_ANCHOR_RE.match(key):
            return m.group(0)                       # Seedance 语法占位符，原样保留
        cat = (reg.get(key, {}).get('category') or '').replace('auto:', '')
        if not cat:                                 # registry 查不到（短 UUID / 资产名）时按前缀推断
            k = key.lower()
            cat = ('character' if k.startswith('char') else
                   'environment' if k.startswith(('loc', 'env')) else
                   'prop' if k.startswith('prop') else '')
        return '<<<%s>>>' % label_for(key, _CATEGORY_LABEL.get(cat, 'REF'))

    text = _ANCHOR_RE.sub(sub, prompt)

    # 正文里直接出现的源项目专名（Vernon / Horace / Tika…）同样要匿名化 ——
    # 否则保留正文就等于把源项目的人物身份一并交出去。
    names = _load_proper_names()
    if names:
        pat = re.compile(r"\b(%s)\b" % '|'.join(sorted(map(re.escape, names), key=len, reverse=True)),
                         re.I)
        text = pat.sub(lambda m: label_for(m.group(1).lower(), names[m.group(1).lower()]), text)
    return text


def strip_copyright(prompt):
    """剥离版权内容，保留全部技术结构段。

    旧实现遇到第一个 <<<uuid>>> 或 ACTIVE REFERENCES 就整段截断，实测中位仅保留
    原文 6.7%，检索到的「真实范例」实际只剩 header。现改为：
      1) 按段落黑名单剔除台词/歌词/发音表（真正的版权风险）
      2) 其余段落全部保留（SCENE CONTEXT / OPTICS / LIGHTING / PHYSICS … 是学习目标）
      3) 角色/道具锚点匿名化，不泄露源项目身份
    """
    text = anonymize_anchors(prompt)

    # 按段落标题切块，丢弃黑名单段
    marks = [(m.start(), m.group(1).strip()) for m in _SECTION_RE.finditer(text)]
    if marks:
        kept, bounds = [], [p for p, _ in marks] + [len(text)]
        if marks[0][0] > 0:
            kept.append(text[:marks[0][0]])          # 首个标题前的引导段（START FRAME 等）
        for i, (pos, title) in enumerate(marks):
            if title in _REDACT_SECTIONS:
                continue
            kept.append(text[pos:bounds[i + 1]])
        text = '\n'.join(kept)

    # 台词判定放在全文层面：分散在多段时每段都不到阈值，逐段判会整体漏掉
    text = _redact_spoken(text)

    # 兜底：无段落标题时按行内关键词剔除
    text = re.sub(r'^(?:USE FOR|IGNORE):.*$', '', text, flags=re.M)
    return re.sub(r'\n{3,}', '\n\n', text).strip()

def main():
    args = sys.argv[1:]
    if not args:
        print(json.dumps({'error': 'usage: seedance_search.py "<query>" [topk]'}, ensure_ascii=False))
        return
    full = '--full' in args
    args = [a for a in args if a != '--full']
    bm = BM25(CORPUS)
    topk = 5
    if len(args) >= 2 and args[-1].isdigit():
        topk = int(args[-1])
        query = ' '.join(args[:-1])
    else:
        query = ' '.join(args)

    hits = bm.search(query, topk)
    result = []
    for h in hits:
        clean = strip_copyright(h['prompt'])
        st = dict(h['structure'])
        # anchors 原样是裸 UUID，对模型零价值 —— 从匿名化后的正文取标签并去重
        st['anchors'] = sorted(set(re.findall(r'<<<([A-Z]+_\d+)>>>', clean)))[:12]
        r = {
            'folder': h['folder'],
            'gold': h['gold'],
            'job_set_type': h['job_set_type'],
            'structure': st,
            'prompt_clean': clean if full else clean[:MAX_CLEAN],
            'clean_len': len(clean),
            'prompt_len': len(h['prompt']),
            'truncated': (not full) and len(clean) > MAX_CLEAN,
            'score': h['score'],
        }
        result.append(r)
    print(json.dumps({'query': query, 'hits': result}, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
