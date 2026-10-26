"""Exact tail P(h>=k+1)/P(h>=k) of the common-ancestor level of edge-adjacent Spectre tiles (Sec. 8 of the paper).

Uses only the perimeters P(k) (non-Mystic) and Q(k) (Mystic) of Theorem 1, recomputed in spectre_indep.py.
Edges shared by tiles whose lowest common ancestor is a level-l supertile are the glue edges between different
children of the level-l supertiles: G_O(l) = (7P(l-1)+Q(l-1)-P(l))/2 and G_G(l) = (6P(l-1)+Q(l-1)-Q(l))/2.
The number of level-l supertiles of each shape inside a level-N O-supertile is (1,0) [[7,6],[1,1]]^(N-l)... computed
directly.  The two halves of each Mystic share (28-Q(0))/2 = 4 edges; convention A gives them level 0, convention B
level 1 (the paper does not say)."""
from fractions import Fraction as Fr
F = [0, 1]
while len(F) < 200:
    F.append(F[-1] + F[-2])
P = [2 * F[3 * k + 5] + 4 for k in range(60)]
Q = [20, 44]
while len(Q) < 60:
    k = len(Q)
    Q.append(5 * Q[k - 1] - 3 * Q[k - 2] - Q[k - 3] if k >= 4 else [20, 44, 160, 652][k])
GO = [None] + [(7 * P[l - 1] + Q[l - 1] - P[l]) // 2 for l in range(1, 60)]
GG = [None] + [(6 * P[l - 1] + Q[l - 1] - Q[l]) // 2 for l in range(1, 60)]
assert all(7 * P[l - 1] + Q[l - 1] - P[l] >= 0 for l in range(1, 60))


def counts(N):
    """number of (O, G) supertiles of level l inside a level-N O-supertile, l = 0..N"""
    c = {N: (1, 0)}
    for l in range(N, 0, -1):
        o, g = c[l]
        c[l - 1] = (7 * o + 6 * g, o + g)
    return c


for conv in ('A', 'B'):
    N = 40
    c = counts(N)
    E = {l: c[l][0] * GO[l] + c[l][1] * GG[l] for l in range(1, N + 1)}
    if conv == 'A':
        E[0] = c[0][1] * 4
    else:
        E[1] += c[0][1] * 4
        E[0] = 0
    tail = lambda k: sum(E[l] for l in range(k, N + 1))
    print("convention", conv, "ratios P(h>=k+1)/P(h>=k), k=1..6:",
          ["%.3f" % (tail(k + 1) / tail(k)) for k in range(1, 7)])
import math
lam2 = 4 + math.sqrt(15)
print("nu/lam^2 = %.4f" % ((2 + math.sqrt(5)) / lam2))
