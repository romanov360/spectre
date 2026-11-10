"""Γ8: does any orientation class of vortices carry the 7.7295 peak?

Each vortex vertex (sheared_index centring, as in refine_seeded) is labelled by the orientation of its lowest-index
incident spectre piece: rotation r in 0..11 (angle of the piece's first basis image) and reflection (det sign of its
linear map in the plane). For every class with at least MIN members, and for the union over reflection, the strong
K4 families (and their conj) are refined as in refine_seeded and the height is compared with the full vortex set.

Usage: python research/orient_subsets.py OUT.json K [K ...]
"""
import sys, json
sys.path.insert(0, "."); sys.path.insert(0, "research")
import numpy as np
from gap_collared import build
from ollivier_ricci import vortices
from module_fit import sf

MIN = 300
SEEDS = [(7.7294, -32.05), (6.0925, 17.89), (7.9372, 162.78)]
Z = np.exp(1j * np.pi / 6 * np.arange(4))


def refine(k0, pts):
    for step in (0.05, 0.005, 0.0005, 0.00005):
        d = np.arange(-10, 11) * step; DX, DY = np.meshgrid(d, d)
        cand = (k0 + DX + 1j * DY).ravel(); hh = sf(cand, pts); k0 = cand[np.argmax(hh)]
    return k0, float(hh.max())


def peaks(pts, odd):
    out = []
    for km, ang in SEEDS:
        k = km * np.exp(1j * np.radians(ang))
        k, h = refine(np.conj(k) if odd else k, pts)
        out.append(dict(seed=km, k=float(abs(k)), ang=float(np.degrees(np.angle(k))), h=h))
    return out


def run(K):
    _, _, V, _ = build(K)
    flat = V.reshape(-1, 4)
    u, inv = np.unique(flat, axis=0, return_inverse=True); inv = inv.ravel()
    x = (u.astype(float) / 28) @ Z; c = x.mean(); R = np.abs(x - c); keep = R < 0.8 * R.max()
    vm = keep & vortices(K, len(x))
    # orientation of each piece from its edge vectors in the plane
    P = V.astype(float) @ Z
    e0 = P[:, 1] - P[:, 0]; e1 = P[:, 2] - P[:, 1]
    rot = np.round(np.angle(e0) / (np.pi / 6)).astype(int) % 12
    refl = (np.imag(e1 * np.conj(e0)) < 0).astype(int)
    piece = np.repeat(np.arange(len(V)), V.shape[1])
    first = np.full(len(u), len(V)); np.minimum.at(first, inv, piece)
    cr, cf = rot[first], refl[first]
    odd = K % 2 == 1
    pts_all = x - c
    res = dict(K=K, N=int(vm.sum()), all=peaks(pts_all[vm], odd), classes=[])
    print(K, "all", res["N"], [round(p["h"], 3) for p in res["all"]], flush=True)
    groups = [("r%d_f%d" % (r, f), vm & (cr == r) & (cf == f)) for r in range(12) for f in (0, 1)]
    groups += [("f%d" % f, vm & (cf == f)) for f in (0, 1)]
    groups += [("r%d" % r, vm & (cr == r)) for r in range(12)]
    for name, m in groups:
        if m.sum() < MIN:
            continue
        pk = peaks(pts_all[m], odd)
        res["classes"].append(dict(name=name, N=int(m.sum()), peaks=pk))
        print(K, name, int(m.sum()), [(round(p["k"], 4), round(p["h"], 3)) for p in pk], flush=True)
    return res


def main():
    out = sys.argv[1]; res = []
    for K in map(int, sys.argv[2:]):
        res.append(run(K)); json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main()
