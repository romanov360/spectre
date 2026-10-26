"""Fact lift (vertex count of the level-3 patch) and Fact contacts (Spectre 14x14 edge-contact matrix on the level-4
patch), recomputed with the independent builder spectre_indep.py.  Tiles of the Mystic count as tiles."""
from collections import Counter, defaultdict
import numpy as np
import networkx as nx
import spectre_indep as S


def tiles(level):
    t = {'O': [S.ID], 'G': [S.ID, S.MYSTIC2]}
    quad = S.QUAD0
    for _ in range(level):
        Ts, nq = S.slot_transforms(quad)
        t = {'O': [S.compose(Ts[i], x) for i in range(7) for x in t['O']] + [S.compose(Ts[7], x) for x in t['G']],
             'G': [S.compose(Ts[i], x) for i in (0, 1, 3, 4, 5, 6) for x in t['O']] + [S.compose(Ts[7], x) for x in t['G']]}
        quad = nq
    return t['O']


for lev in range(0, 5):
    T = tiles(lev)
    V = {S.apply(t, p) for t in T for p in S.SPEC}
    print("level %d: %d tiles, %d distinct vertices" % (lev, len(T), len(V)))
T = tiles(4)
# edge contacts: native edge index a of one tile meets native edge index b of another
owner = defaultdict(list)
for ti, t in enumerate(T):
    pts = [S.apply(t, p) for p in S.SPEC]
    for a in range(14):
        owner[S.ekey(pts[a], pts[(a + 1) % 14])].append((ti, a))
C = np.zeros((14, 14), dtype=np.int64)
n = 0
for e, lst in owner.items():
    assert len(lst) <= 2
    if len(lst) == 2:
        (t1, a), (t2, b) = lst
        C[a, b] += 1
        C[b, a] += 1
        n += 1
print("level-4 patch: %d tiles, %d shared edges" % (len(T), n))
nz = int((C != 0).sum())
G = nx.Graph()
G.add_nodes_from(range(14))
G.add_edges_from((a, b) for a in range(14) for b in range(14) if C[a, b])
ev = np.linalg.eigvalsh(C.astype(float))
print("nonzero entries %d, rank %d, bipartite %s, connected %s, spectrum symmetric %s"
      % (nz, np.linalg.matrix_rank(C), nx.is_bipartite(G), nx.is_connected(G),
         np.allclose(sorted(ev), sorted(-ev), atol=1e-8)))
