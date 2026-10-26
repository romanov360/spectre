"""Adversarial probe of boundary_certificate/spectre_window.py (prepublication review).

1. Key soundness.  spectre_window.py identifies contact types by rounding the relative translation d to 1e-40
   (60-digit arithmetic).  It computes the set of distinct translations but never checks that distinct keys are
   far apart.  Here we recompute the closure and report the smallest distance between distinct rounded
   translations that share (S1, S2, p, B): if it is >> 1e-40 the rounding cannot have merged or split types.
2. Positivity of the margin.  Pruning keeps a type iff |d| <= 2*RAD; report how close pruned/kept |d| come to the
   threshold (a type exactly at the threshold would be a float-sensitive decision).
3. Numerical box count of the boundary of the attractor Z_0(O), from a depth-m enumeration of the graph-directed
   system, as a sanity check of 1.110977 that does not use the contact-matrix argument.

Usage:  python3 window_probe.py    (imports spectre_window, which re-runs the boundary certificate: ~5 min)
Run from boundary_certificate/ on the PYTHONPATH:  PYTHONPATH=../../../boundary_certificate python3 window_probe.py
"""
import io
import contextlib
import math
import numpy as np
import mpmath as mp

with contextlib.redirect_stdout(io.StringIO()):
    import spectre_window as sw

LAM, RAD = sw.LAM, sw.RAD
margin = mp.mpf(10) ** -20
live, stack = {}, sw.start_types()
dmin_thresh = mp.mpf(10) ** 9
while stack:
    t = stack.pop()
    nd = mp.norm(t[4])
    dmin_thresh = min(dmin_thresh, abs(nd - 2 * RAD))
    if nd > 2 * RAD + margin:
        continue
    k = sw.tkey(*t)
    if k in live:
        # same key: check the unrounded translations agree to far better than the rounding unit
        assert mp.norm(live[k][4] - t[4]) < mp.mpf(10) ** -45, "same key, different translation"
        assert mp.norm(live[k][3] - t[3]) < mp.mpf(10) ** -25
        continue
    live[k] = t
    stack.extend(sw.children(*t))
print("live types:", len(live))
print("closest approach of |d| to the pruning threshold 2*RAD: %s (RAD = %s)" % (mp.nstr(dmin_thresh, 5), mp.nstr(RAD, 8)))
groups = {}
for k, t in live.items():
    groups.setdefault(k[:4], []).append(t[4])
best = mp.mpf(10) ** 9
for g, ds in groups.items():
    for i in range(len(ds)):
        for j in range(i + 1, len(ds)):
            best = min(best, mp.norm(ds[i] - ds[j]))
print("smallest distance between distinct translations with the same (S1,S2,p,B): %s" % mp.nstr(best, 5))
Bkeys = {}
for k, t in live.items():
    Bkeys.setdefault(k[3], t[3])
bl = list(Bkeys.values())
bb = min(mp.norm(bl[i] - bl[j]) for i in range(len(bl)) for j in range(i + 1, len(bl))) if len(bl) > 1 else None
print("distinct linear parts B: %d, smallest distance between them %s" % (len(bl), mp.nstr(bb, 5) if bb else '-'))

# ---------------- numerical box count of Z_0(O) ----------------
O = {k: np.array([[float(v[r, c]) for c in range(2)] for r in range(2)]) for k, v in sw.O.items()}
GA = {k: np.array([float(v[0]), float(v[1])]) for k, v in sw.GA.items()}
lam = float(LAM)


def points(S, p, depth):
    """points of Z_p(S) at the given depth: images of the origin"""
    if depth == 0:
        return np.zeros((1, 2))
    out = []
    for (i, S2) in sw.MAPS[(S, p)]:
        pts = points(S2, 1 - p, depth - 1)
        y = GA[(i, p)][None, :] + pts / lam
        out.append(y @ O[(i, p)])          # O^{-1} = O^T for orthogonal O: x -> O^T x is row @ O
    return np.vstack(out)


depth = 7
Z = points('O', 0, depth)
print("depth %d: %d points; extent %.4f" % (depth, len(Z), np.abs(Z).max()))
lo = Z.min(axis=0)
res = []
for e in [0.4, 0.2, 0.1, 0.05, 0.025]:
    idx = np.floor((Z - lo) / e).astype(np.int64)
    occ = set(map(tuple, idx))
    bd = 0
    for (a, b) in occ:
        if any((a + da, b + db) not in occ for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            bd += 1
    res.append((e, len(occ), bd))
print("box counts (eps, occupied, boundary):", res)
for (e1, o1, b1), (e2, o2, b2) in zip(res, res[1:]):
    print("  eps %.3f -> %.3f: boundary slope %.3f, area slope %.3f" % (e1, e2, math.log(b2 / b1) / math.log(e1 / e2),
                                                                         math.log(o2 / o1) / math.log(e1 / e2)))
print("point spacing at this depth is about lam^-%d * scale = %.4f; counts at eps below a few times this are unreliable"
      % (depth, RAD / lam ** depth))
