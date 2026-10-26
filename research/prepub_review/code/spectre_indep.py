"""Independent exact rebuild of the Spectre supertiles (prepublication review).

Written from Kaplan's published construction (the JavaScript reference code accompanying
Smith-Myers-Kaplan-Goodman-Strauss, arXiv:2305.17743), without using the repository's code or its
Z^4 basis.  A point is stored as four integers (a, b, c, d) meaning
    x = (a + b*sqrt3)/2,   y = (c + d*sqrt3)/2,
so every coordinate is exact.  An isometry is (k, m, t): x -> t + Rot(30k) Ref^m x, Ref(x, y) = (-x, y).

What it computes (all exact integer arithmetic):
  * the substitution matrix M, its characteristic polynomial, ranks of M^n, censuses, Q+/Q- charges;
  * the outline of the non-Mystic (O) and Mystic (G) supertiles, level by level, as the multiset of unit
    edges counted mod 2 (edges shared by two children cancel), for k = 0..KMAX;
  * the perimeters P(k), Q(k), the recurrence P(k+3)=5P(k+2)-3P(k+1)-P(k), the closed form 2F(3k+5)+4,
    the invariant P(k+2)-4P(k+1)-P(k) = -16, and the even/odd direction split of Table 2;
  * a cross-check, for k <= 5, that the mod-2 outline equals the outline counted from all placed tiles
    (each boundary edge used exactly once, no edge used three or more times);
  * the 16x16 quad map Phi in this (different) basis and its characteristic polynomial;
  * the twist angle of the supertile quadrilateral, numerically, against tan(theta) = (5 sqrt3 - 6)/13.

Usage:  python3 spectre_indep.py [KMAX]     (KMAX default 8; k = 8 takes about a minute)
"""
import sys
import math
from collections import Counter
import numpy as np
import sympy as sp

S3 = math.sqrt(3)


# ---------------------------------------------------------------- exact points
def rot30(p):
    """rotate (a,b,c,d) by +30 degrees: x' = (sqrt3/2) x - (1/2) y, y' = (1/2) x + (sqrt3/2) y"""
    a, b, c, d = p
    # 2x' = (sqrt3/2)(a + b s) - (1/2)(c + d s) = (3b - c)/2 + (a - d)/2 s
    # 2y' = (1/2)(a + b s) + (sqrt3/2)(c + d s) = (a + 3d)/2 + (b + c)/2 s
    n = (3 * b - c, a - d, a + 3 * d, b + c)
    assert all(v % 2 == 0 for v in n), p
    return tuple(v // 2 for v in n)


def rot(p, k):
    for _ in range(k % 12):
        p = rot30(p)
    return p


def ref(p):
    a, b, c, d = p
    return (-a, -b, c, d)


def add(p, q):
    return tuple(x + y for x, y in zip(p, q))


def sub(p, q):
    return tuple(x - y for x, y in zip(p, q))


def fl(p):
    a, b, c, d = p
    return complex((a + b * S3) / 2, (c + d * S3) / 2)


def exact_from_float(x):
    """find integers (a, b) with (a + b sqrt3)/2 == x (to 1e-9), small search"""
    for b in range(-20, 21):
        a = round(2 * x - b * S3)
        if abs((a + b * S3) / 2 - x) < 1e-9:
            return a, b
    raise ValueError(x)


# Kaplan's published float outline of Tile(1,1)
KAPLAN = [(0, 0), (1.0, 0.0), (1.5, -0.8660254037844386), (2.366025403784439, -0.36602540378443865),
          (2.366025403784439, 0.6339745962155614), (3.366025403784439, 0.6339745962155614),
          (3.866025403784439, 1.5), (3.0, 2.0), (2.133974596215561, 1.5),
          (1.6339745962155614, 2.3660254037844393), (0.6339745962155614, 2.3660254037844393),
          (-0.3660254037844386, 2.3660254037844393), (-0.866025403784439, 1.5), (0.0, 1.0)]
SPEC = [exact_from_float(x) + exact_from_float(y) for x, y in KAPLAN]
for i in range(14):
    e = fl(sub(SPEC[(i + 1) % 14], SPEC[i]))
    assert abs(abs(e) - 1) < 1e-12           # unit edges
    assert abs((math.degrees(math.atan2(e.imag, e.real)) / 30) - round(math.degrees(math.atan2(e.imag, e.real)) / 30)) < 1e-9


# ---------------------------------------------------------------- isometries (k, m, t)
def apply(T, p):
    k, m, t = T
    if m:
        p = ref(p)
    return add(rot(p, k), t)


def compose(T1, T2):
    """T1 o T2"""
    k1, m1, t1 = T1
    k2, m2, t2 = T2
    # T1(T2 x) = t1 + R1 F1 (t2 + R2 F2 x);  F1 R2 = R(-k2) F1 when F1 is a reflection
    k = (k1 + (-k2 if m1 else k2)) % 12
    return (k, m1 ^ m2, apply(T1, t2))


ID = (0, 0, (0, 0, 0, 0))


def trot(k):
    return (k % 12, 0, (0, 0, 0, 0))


def ttrans(v):
    return (0, 0, v)


REFL = (0, 1, (0, 0, 0, 0))     # Kaplan's R = [-1,0,0, 0,1,0]

SPECIES = ['Gamma', 'Delta', 'Theta', 'Lambda', 'Xi', 'Pi', 'Sigma', 'Phi', 'Psi']
# Kaplan's superRules (supertile species -> species in the eight slots; Gamma has a null slot)
RULES = {
    'Gamma':  ['Pi', 'Delta', None, 'Theta', 'Sigma', 'Xi', 'Phi', 'Gamma'],
    'Delta':  ['Xi', 'Delta', 'Xi', 'Phi', 'Sigma', 'Pi', 'Phi', 'Gamma'],
    'Theta':  ['Psi', 'Delta', 'Pi', 'Phi', 'Sigma', 'Pi', 'Phi', 'Gamma'],
    'Lambda': ['Psi', 'Delta', 'Xi', 'Phi', 'Sigma', 'Pi', 'Phi', 'Gamma'],
    'Xi':     ['Psi', 'Delta', 'Pi', 'Phi', 'Sigma', 'Psi', 'Phi', 'Gamma'],
    'Pi':     ['Psi', 'Delta', 'Xi', 'Phi', 'Sigma', 'Psi', 'Phi', 'Gamma'],
    'Sigma':  ['Xi', 'Delta', 'Xi', 'Phi', 'Sigma', 'Pi', 'Lambda', 'Gamma'],
    'Phi':    ['Psi', 'Delta', 'Psi', 'Phi', 'Sigma', 'Pi', 'Phi', 'Gamma'],
    'Psi':    ['Psi', 'Delta', 'Psi', 'Phi', 'Sigma', 'Psi', 'Phi', 'Gamma'],
}
TRULES = [(60, 3, 1), (0, 2, 0), (60, 3, 1), (60, 3, 1), (0, 2, 0), (60, 3, 1), (-120, 3, 3)]


def slot_transforms(quad):
    Ts = [ID]
    total = 0
    rotation = ID
    tquad = list(quad)
    for ang, frm, to in TRULES:
        if ang != 0:
            total += ang
            rotation = trot(total // 30)
            tquad = [apply(rotation, p) for p in quad]
        ttt = ttrans(sub(apply(Ts[-1], quad[frm]), tquad[to]))
        Ts.append(compose(ttt, rotation))
    Ts = [compose(REFL, T) for T in Ts]
    newq = [apply(Ts[6], quad[2]), apply(Ts[5], quad[1]), apply(Ts[3], quad[2]), apply(Ts[0], quad[1])]
    return Ts, newq


QUAD0 = [SPEC[3], SPEC[5], SPEC[7], SPEC[11]]
MYSTIC2 = compose(ttrans(SPEC[8]), trot(1))


# ---------------------------------------------------------------- substitution matrix
def matrix_facts(out):
    M = sp.zeros(9, 9)
    for j, s in enumerate(SPECIES):
        for c in RULES[s]:
            if c:
                M[SPECIES.index(c), j] += 1
    x = sp.symbols('x')
    out.append("M =\n" + str(M.tolist()))
    out.append("charpoly(M) = %s" % sp.factor(M.charpoly(x).as_expr()))
    out.append("rank M^n, n=1..4: %s" % [(M ** n).rank() for n in range(1, 5)])
    e = sp.zeros(9, 1)
    e[1] = 1                        # seed Delta
    T = []
    v = e
    for n in range(7):
        T.append(int(sum(v)))
        v = M * v
    out.append("matrix census from Delta, depth 0..6: %s" % T)
    out.append("T(n+1) = 8T(n) - T(n-1): %s" % all(T[n + 1] == 8 * T[n] - T[n - 1] for n in range(1, 6)))
    ones = sp.ones(1, 9)
    out.append("1^T (M^2 - 8M + I) == 0: %s" % (ones * (M ** 2 - 8 * M + sp.eye(9)) == sp.zeros(1, 9)))
    Qp = sp.Matrix([[-3, -1, 0, 0, 1, 1, -2, 1, 2]])
    Qm = sp.Matrix([[-1, -1, 2, 0, 1, -1, 0, 1, 0]])
    out.append("Q+ M == Q+: %s ; Q- M == -Q-: %s" % (Qp * M == Qp, Qm * M == -Qm))
    v = e
    qp, qm = [], []
    for n in range(1, 5):
        v = M * v
        qp.append(int((Qp * v)[0]))
        qm.append(int((Qm * v)[0]))
    out.append("Q+ on depth 1..4 census: %s ; Q- : %s" % (qp, qm))
    out.append("Q- on single tiles of Lambda, Sigma, Psi: %s" % [int(Qm[0, SPECIES.index(s)]) for s in ('Lambda', 'Sigma', 'Psi')])
    out.append("Q-(Delta) = %d" % int(Qm[0, 1]))
    # Gamma seed census
    g = sp.zeros(9, 1)
    g[0] = 1
    G = []
    for n in range(4):
        g = M * g
        G.append(int(sum(g)))
    out.append("matrix census from Gamma, depth 1..4: %s" % G)
    return M


# ---------------------------------------------------------------- outlines mod 2
def edges_of_tile(T):
    pts = [apply(T, p) for p in SPEC]
    return [(pts[i], pts[(i + 1) % 14]) for i in range(14)]


def ekey(p, q):
    return (p, q) if p < q else (q, p)


def mod2(edge_lists):
    c = Counter()
    for el in edge_lists:
        for (p, q) in el:
            c[ekey(p, q)] += 1
    assert max(c.values()) <= 2
    return [e for e, n in c.items() if n == 1]


def transform_edges(T, edges):
    return [(apply(T, p), apply(T, q)) for p, q in edges]


def direction(p, q):
    z = fl(sub(q, p))
    return round(math.degrees(math.atan2(z.imag, z.real)) / 30) % 6


def main():
    KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    out = []
    matrix_facts(out)

    # level 0 outlines
    O = edges_of_tile(ID)
    G = mod2([edges_of_tile(ID), edges_of_tile(MYSTIC2)])
    quad = QUAD0
    P, Q, dirs, quads = [len(O)], [len(G)], [], [quad]
    tiles = {'O': [ID], 'G': [ID, MYSTIC2]}      # placed tiles, kept for k <= 5 for the cross-check

    def dirsplit(edges):
        h = Counter(direction(p, q) for p, q in edges)
        return h
    dirs.append(dirsplit(O))
    for k in range(KMAX):
        Ts, nq = slot_transforms(quad)
        Ochildren = [transform_edges(Ts[i], O) for i in range(7)] + [transform_edges(Ts[7], G)]
        Gchildren = [transform_edges(Ts[i], O) for i in (0, 1, 3, 4, 5, 6)] + [transform_edges(Ts[7], G)]
        O, G = mod2(Ochildren), mod2(Gchildren)
        if k + 1 <= 5:
            tiles = {'O': [compose(Ts[i], t) for i in range(7) for t in tiles['O']] + [compose(Ts[7], t) for t in tiles['G']],
                     'G': [compose(Ts[i], t) for i in (0, 1, 3, 4, 5, 6) for t in tiles['O']] + [compose(Ts[7], t) for t in tiles['G']]}
            for X, outl in (('O', O), ('G', G)):
                c = Counter()
                for t in tiles[X]:
                    for (p, q) in edges_of_tile(t):
                        c[ekey(p, q)] += 1
                assert max(c.values()) <= 2
                assert sorted(e for e, n in c.items() if n == 1) == sorted(outl)
                # no two tiles share a vertex-set (no duplicate tile)
                assert len(set(tuple(sorted(apply(t, p) for p in SPEC)) for t in tiles[X])) == len(tiles[X])
        quad = nq
        quads.append(quad)
        P.append(len(O))
        Q.append(len(G))
        dirs.append(dirsplit(O))
        print("level", k + 1, "P =", P[-1], "Q =", Q[-1], flush=True)
    out.append("P(k), k=0..%d: %s" % (KMAX, P))
    out.append("Q(k), k=0..%d: %s" % (KMAX, Q))
    out.append("tile-level cross-check of the mod-2 outline for k <= 5: passed (edges used at most twice; outline = edges used once; tiles distinct)")
    F = [0, 1]
    while len(F) < 3 * KMAX + 10:
        F.append(F[-1] + F[-2])
    out.append("P(k) == 2F(3k+5)+4 for k<=KMAX: %s" % all(P[k] == 2 * F[3 * k + 5] + 4 for k in range(KMAX + 1)))
    out.append("P recurrence holds for k+3<=KMAX: %s" % all(P[k + 3] == 5 * P[k + 2] - 3 * P[k + 1] - P[k] for k in range(KMAX - 2)))
    out.append("P(k+2)-4P(k+1)-P(k): %s" % [P[k + 2] - 4 * P[k + 1] - P[k] for k in range(KMAX - 1)])
    out.append("Q recurrence from k=1: %s ; at k=0: %s" % (all(Q[k + 3] == 5 * Q[k + 2] - 3 * Q[k + 1] - Q[k] for k in range(1, KMAX - 2)),
                                                          Q[3] == 5 * Q[2] - 3 * Q[1] - Q[0]))
    out.append("growth bound P(k+3) >= 4P(k+2)+30: %s" % [P[k + 3] - 4 * P[k + 2] for k in range(KMAX - 2)])
    rows = []
    for k in range(KMAX + 1):
        h = dirs[k]
        hj = [h[j] / 2 for j in range(6)]
        even = hj[0] + hj[2] + hj[4]
        odd = hj[1] + hj[3] + hj[5]
        # characters of Z/6 on the folded histogram
        amps = []
        for chi in (1, 2, 4, 5):          # Z/3 characters (2,4) and faithful ones (1,5)
            amps.append(abs(sum(hj[j] * complex(math.cos(2 * math.pi * chi * j / 6), math.sin(2 * math.pi * chi * j / 6)) for j in range(6))))
        rows.append((k, P[k], even, odd, even - odd, max(amps), even == F[3 * k + 4] + 1, odd == F[3 * k + 3] + 1))
    out.append("direction split (k, P, even, odd, even-odd, max |Z/3 or faithful amplitude|, even==F(3k+4)+1, odd==F(3k+3)+1):")
    for r in rows:
        out.append("  %d %d %g %g %g %.2f %s %s" % r)

    # the quad map Phi in this basis: linear in the 16 integer coordinates of the quad
    def flat(qd):
        return [v for p in qd for v in p]

    def unflat(v):
        return [tuple(v[4 * i:4 * i + 4]) for i in range(4)]
    # slot_transforms needs points of Z[zeta12] (parity conditions); use 2*basis vectors scaled to stay integral
    cols = []
    base = flat(QUAD0)
    for m in range(16):
        # finite difference on a lattice direction known to stay in the ring: use multiples of 2
        v = list(base)
        v[m] += 2
        try:
            _, nq1 = slot_transforms(unflat(v))
        except AssertionError:
            nq1 = None
        cols.append(nq1)
    # Linear map: Phi(q) = new quad; compute it on 16 independent quads q_j = Phi^j q0 is not enough (rank 6),
    # so instead identify Phi via the finite differences above (scaled by 2, parity-safe).
    _, nq0 = slot_transforms(QUAD0)
    ok = all(c is not None for c in cols)
    if ok:
        Phi = sp.Matrix(16, 16, lambda i, j: sp.Rational(flat(cols[j])[i] - flat(nq0)[i], 2))
        x = sp.symbols('x')
        out.append("charpoly(Phi) in the (a,b,c,d) basis: %s" % sp.factor(Phi.charpoly(x).as_expr()))
        # check linearity on the actual iterates
        qq = QUAD0
        for k in range(6):
            _, nq = slot_transforms(qq)
            assert list(Phi * sp.Matrix(flat(qq))) == flat(nq)
            qq = nq
        out.append("Phi reproduces 6 actual levels exactly: True")
    else:
        out.append("Phi: finite differences left the ring; skipped")

    # twist: angle between consecutive quad diagonals (q[2]-q[0]) at large k
    def diag(qd):
        return fl(sub(qd[2], qd[0]))
    tw = []
    for k in range(KMAX - 1, KMAX + 1):
        r = diag(quads[k]) / diag(quads[k - 1])
        r2 = diag(quads[k]) / diag(quads[k - 2])
        tw.append((k, round(abs(r), 7), round(math.degrees(math.atan2(r.imag, r.real)), 6),
                   round(abs(r2), 6), round(math.degrees(math.atan2(r2.imag, r2.real)), 9)))
    th = math.degrees(math.atan((5 * S3 - 6) / 13))
    out.append("quad diagonal ratio at the last two levels (k, |r|, arg deg): %s ; theta_S from tan formula = %.6f; lambda = %.7f"
               % (tw, th, math.sqrt(4 + math.sqrt(15))))
    print("\n".join(out))


if __name__ == '__main__':
    main()
