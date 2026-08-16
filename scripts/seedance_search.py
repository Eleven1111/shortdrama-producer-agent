#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seedance_search.py — 零依赖 BM25 检索器（纯 Python stdlib）。
随 skill 分发，检索打包的 seedance_corpus.jsonl.gz（4,348 docs 真实生产范例）。

用法：
  python3 seedance_search.py "场景描述一句话" [topk]
  python3 seedance_search.py --style "风格关键词"
  python3 seedance_search.py --ref "角色/道具描述"

输出：JSON（stdout），含命中的真实范例（prompt 全文 + 结构字段 + gold 标记）。
"""
import gzip, json, math, os, re, sys
from collections import Counter

CORPUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seedance_corpus.jsonl.gz')
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
        self.df = Counter()
        self.doc_toks = []
        self.doc_lens = []
        for d in self.docs:
            toks = tokenize(d['prompt'])
            self.df.update(set(toks))
            self.doc_toks.append(Counter(toks))
            self.doc_lens.append(len(toks))
        self.avgdl = sum(self.doc_lens) / self.N if self.N else 1.0
        self.k1, self.b = 1.5, 0.75

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

def strip_copyright(prompt):
    """剥离源项目版权内容：角色卡/道具引用段（ACTIVE REFERENCES/USE FOR 等）"""
    cut = re.split(r'\n(?:ACTIVE REFERENCES|CHARACTER ACTING|DIALOGUE|SOUND|MUSIC)\b', prompt, maxsplit=1)[0]
    cut = re.split(r'<<<[0-9a-f\-]{36}>>>|\bUSE FOR:|\bIGNORE:', cut, maxsplit=1)[0]
    return cut.strip()

def main():
    args = sys.argv[1:]
    if not args:
        print(json.dumps({'error': 'usage: seedance_search.py "<query>" [topk]'}, ensure_ascii=False))
        return
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
        r = {
            'folder': h['folder'],
            'gold': h['gold'],
            'job_set_type': h['job_set_type'],
            'structure': h['structure'],
            'prompt_clean': strip_copyright(h['prompt'])[:2500],
            'prompt_len': len(h['prompt']),
            'score': h['score'],
        }
        result.append(r)
    print(json.dumps({'query': query, 'hits': result}, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
