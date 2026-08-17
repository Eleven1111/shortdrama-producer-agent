"""P0.3 检索评测：已知项召回（客观、可复现、无需人工判断）。

方法：从语料随机抽 N 条文档，取其 SCENE CONTEXT 段的实词作为查询，
检验该文档能否被自己的内容召回。召不回 = 检索器坏了。

指标：Recall@1 / @3 / @5、MRR。种子固定，可跨版本对比。
"""
import gzip, json, os, random, re, sys, math
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from seedance_search import BM25, CORPUS, tokenize

STOP = set('''the a an and or of to in on at is are was were be been with for from by as it its
this that these those there here shot scene camera frame keep use exactly same not no only all
every each any some one two three'''.split())

SCENE_RE = re.compile(r'^SCENE CONTEXT\s*$(.*?)(?=^[A-Z][A-Z0-9 &/\'()-]{3,44}\s*$|\Z)',
                      re.M | re.S)


def make_query(doc, nwords=14):
    """从 SCENE CONTEXT 取内容词做查询；没有该段则用正文中段。"""
    m = SCENE_RE.search(doc['prompt'])
    src = m.group(1) if m else doc['prompt'][len(doc['prompt']) // 3: len(doc['prompt']) // 3 + 1200]
    toks = [t for t in tokenize(src) if t not in STOP and not t.isdigit() and len(t) > 2]
    if len(toks) < 6:
        return None
    # 取文档内相对高频的内容词，模拟用户用自己的话描述场景
    top = [w for w, _ in Counter(toks).most_common(nwords)]
    return ' '.join(top)


def main(n=120, seed=7):
    bm = BM25(CORPUS)
    random.seed(seed)
    idx = list(range(bm.N))
    random.shuffle(idx)

    cases, ranks, folder_ranks = 0, [], []
    for i in idx:
        if cases >= n:
            break
        q = make_query(bm.docs[i])
        if not q:
            continue
        cases += 1
        hits = bm.search(q, 10)
        rank = fold = None
        for r, h in enumerate(hits, 1):
            if rank is None and h['id'] == bm.docs[i]['id']:
                rank = r
            if fold is None and h['folder'] == bm.docs[i]['folder']:
                fold = r
        ranks.append(rank)
        folder_ranks.append(fold)

    def rec(rs, k):
        return sum(1 for r in rs if r and r <= k) / len(rs)
    mrr = sum(1.0 / r for r in ranks if r) / len(ranks)

    print('评测用例: %d (seed=%d)' % (len(ranks), seed))
    # search() 对同一 folder 只返回一条，故文档级会系统性低估：目标文档常被
    # 同 folder 的兄弟文档挤掉。folder 级才是生产中的实际语义，读数以它为准。
    print('  [folder 级 · 生产语义]  Recall@1 %.1f%%  @3 %.1f%%  @5 %.1f%%'
          % (rec(folder_ranks, 1) * 100, rec(folder_ranks, 3) * 100, rec(folder_ranks, 5) * 100))
    print('  [文档级 · 受去重低估]  Recall@1 %.1f%%  @5 %.1f%%  MRR %.3f'
          % (rec(ranks, 1) * 100, rec(ranks, 5) * 100, mrr))
    print('  folder 未进 top10: %d (%.1f%%)'
          % (sum(1 for r in folder_ranks if not r),
             sum(1 for r in folder_ranks if not r) / len(folder_ranks) * 100))
    return rec(folder_ranks, 1), rec(folder_ranks, 5), mrr


if __name__ == '__main__':
    main()
