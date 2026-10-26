"""Growth exponents of the orientation harmonics of the Spectre (Fact 24), from placed patches built by
spectre_indep.py.  For harmonic m, S_m(n) = sum over tiles of exp(i m theta), theta = 30 deg * (rotation index of the
tile's placement); h_m is estimated as log(|S_m(n)|/|S_m(n-2)|) / (2 log lambda) (two levels, to cancel the mirror)."""
import math, cmath
import spectre_indep as S
lam = math.sqrt(4 + math.sqrt(15))
t = {'O': [S.ID], 'G': [S.ID, S.MYSTIC2]}
quad = S.QUAD0
hist = []
for lev in range(1, 8):
    Ts, nq = S.slot_transforms(quad)
    # count tiles by (rotation index, reflection) only: multiplicities suffice
    t = {'O': [S.compose(Ts[i], x) for i in range(7) for x in t['O']] + [S.compose(Ts[7], x) for x in t['G']],
         'G': [S.compose(Ts[i], x) for i in (0, 1, 3, 4, 5, 6) for x in t['O']] + [S.compose(Ts[7], x) for x in t['G']]} if lev <= 5 else None
    if t is None:
        break
    quad = nq
    cnt = [0] * 12
    for x in t['O']:
        cnt[x[0]] += 1
    hist.append(cnt)
for m in range(7):
    S_ = [abs(sum(c * cmath.exp(1j * math.radians(30 * k * m)) for k, c in enumerate(cnt))) for cnt in hist]
    h = [math.log(S_[n] / S_[n - 2]) / (2 * math.log(lam)) if S_[n - 2] > 1e-9 and S_[n] > 1e-9 else float('nan') for n in range(2, len(S_))]
    print("m=%d |S_m(n)|, n=1..5: %s ; h estimates: %s" % (m, ["%.3g" % v for v in S_], ["%.3f" % v for v in h]))
