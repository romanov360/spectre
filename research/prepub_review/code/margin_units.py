"""Which part of check_spectre_boundary_proof.separated() attains the reported smallest margin 0.0971?
The finite part is in units of the quad diagonal |q2-q0| (sc[k]); the tail part (k > K) is in units of lam^k/... .
Re-evaluates the two parts separately for every pruned type."""
import io, contextlib
import mpmath as mp
with contextlib.redirect_stdout(io.StringIO()):
    import check_spectre_boundary_proof as bp
fin, tl = [], []
for kk, mg in bp.pruned.items():
    pass
# reconstruct pruned types by re-running closure, keeping the tuples
live, pruned, stack = {}, {}, bp.start['O'] + bp.start['G']
while stack:
    t = stack.pop()
    kk = bp.tkey(*t)
    if kk in live or kk in pruned:
        continue
    X, Y, Am, L = t
    Cy = bp.cen_fun(Am, L) - bp.C_ID
    m1 = min((abs(bp.val(Cy, k)) - bp.r[X][k] - bp.r[Y][k]) / bp.sc[k] for k in range(bp.K))
    lim, eps = bp.tail(Cy)
    m2 = min(float((abs(lim[p]) - eps) / 4 - bp.RB[(X, p)] - bp.RB[(Y, p)]) for p in (0, 1))
    if min(m1, m2) > 0:
        pruned[kk] = (m1, m2)
        continue
    live[kk] = t
    stack.extend(bp.children(*t))
m1s = min(v[0] for v in pruned.values()); m2s = min(v[1] for v in pruned.values())
print("pruned:", len(pruned), "live:", len(live))
print("smallest finite-range margin (k < K, units of the quad diagonal): %.4f" % m1s)
print("smallest tail margin (k >= K, units of lam^k): %.4f" % m2s)
lam = float(bp.lam)
print("quad diagonal / lam^k at k = K: %.4f" % (bp.sc[bp.K] / lam ** bp.K))
