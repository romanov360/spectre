"""Subset automaton of the Chair44 cell substitution: reachable label sets and c(M), the number of digit words of
length M that have not yet fixed the label (paper: 209 reachable, 41 with more than one label;
c(M) = 1, 8, 64, 176, 400, 848, 1744, ...; c(M) = 28*2^M - 48 from M = 3; spectral radius 2 on non-singletons).
Usage: python3 -I chair44_coincidence_rate.py path/to/r44_solid.json"""
import os
import numpy as np
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chair44_blocks_indep.py')).read()
src = src.split('# ---------------------------------------------------------------- legal blocks')[0]
exec(compile(src, 'chair44_blocks_indep.py', 'exec'))
start = frozenset(range(168))
seen, frontier = {start}, [start]
while frontier:
    new = []
    for s in frontier:
        for bi in range(8):
            t = frozenset(SUB[j][bi] for j in s)
            if t not in seen:
                seen.add(t)
                new.append(t)
    frontier = new
multi = [s for s in seen if len(s) > 1]
print("reachable label sets:", len(seen), " with more than one label:", len(multi))
cnt = {start: 1}
c = []
for M in range(12):
    c.append(sum(v for s, v in cnt.items() if len(s) > 1))
    nxt = {}
    for s, v in cnt.items():
        for bi in range(8):
            t = frozenset(SUB[j][bi] for j in s)
            nxt[t] = nxt.get(t, 0) + v
    cnt = nxt
print("c(M), M = 0..11:", c)
print("c(M) == 28*2^M - 48 for M >= 3:", all(c[M] == 28 * 2 ** M - 48 for M in range(3, 12)))
idx = {s: i for i, s in enumerate(multi)}
A = np.zeros((len(multi), len(multi)))
for s in multi:
    for bi in range(8):
        t = frozenset(SUB[j][bi] for j in s)
        if t in idx:
            A[idx[t], idx[s]] += 1
print("spectral radius on non-singleton states: %.10f" % max(abs(np.linalg.eigvals(A))))
