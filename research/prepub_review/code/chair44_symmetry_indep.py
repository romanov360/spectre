"""Independent recomputation of the finite inputs of the symmetry classification (Theorem thm:sym).

Re-uses the first half of chair44_blocks_indep.py (atlas, cell substitution, legal blocks, fixed seeds) by executing
it up to the admissible-block section, then builds, for each candidate cyclic group K about an axis direction e,
the graph G_K: vertices = legal blocks w with Stab(w) n O_e = K, edges w -> W_j(w) (j = -1, 0, 1), where W_j(w) is
the 2x2x2 window of sigma(w) centred at j*e.  It reports the number of blocks in G_K and whether some strongly
connected component carries two distinct shift labels (the paper: C2^diag yes, 14 blocks on each face-diagonal
axis; C4 yes, 4 blocks; C2 about a coordinate axis: 18 blocks, only constant-shift components).

Usage: python3 -I chair44_symmetry_indep.py path/to/r44_solid.json
"""
import sys
import os
import networkx as nx
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chair44_blocks_indep.py')).read()
src = src.split('# ---------------------------------------------------------------- admissible blocks')[0]
exec(compile(src, 'chair44_blocks_indep.py', 'exec'))


def window_at(w, off):
    e = sigma_block({b: w[i] for i, b in enumerate(BITS)}, 2)
    return tuple(e[(off[0] + b[0], off[1] + b[1], off[2] + b[2])] for b in BITS)


def rotation_about(e, order):
    """the proper rotations R with R e = e, of the given order (as elements of ROT)"""
    res = []
    for R in ROT:
        if mv(R, e) != e:
            continue
        k, P = 1, R
        while P != I:
            P = mm(P, R)
            k += 1
        if k == order:
            res.append(R)
    return res


def group(gens):
    G = {I}
    frontier = [I]
    while frontier:
        new = []
        for g in frontier:
            for h in gens:
                x = mm(h, g)
                if x not in G:
                    G.add(x)
                    new.append(x)
        frontier = new
    return frozenset(G)


cases = []
for e, order, name in (((0, 0, 1), 2, 'C2 coordinate axis z'), ((0, 0, 1), 4, 'C4 about z'),
                       ((1, 1, 0), 2, 'C2 face diagonal (1,1,0)'), ((1, -1, 0), 2, 'C2 face diagonal (1,-1,0)')):
    R = rotation_about(e, order)[0]
    K = group([R])
    Oe = frozenset(g for g in ROT if mv(g, e) == e)
    verts = [w for w in LEGALB if frozenset(g for g in Oe if act(g, w) == w) == K]
    vs = set(verts)
    Gr = nx.DiGraph()
    Gr.add_nodes_from(verts)
    for w in verts:
        for j in (-1, 0, 1):
            off = tuple(1 + j * x for x in e)
            u = window_at(w, off)
            if u in vs:
                Gr.add_edge(w, u, j=j)
    mixed = []
    for comp in nx.strongly_connected_components(Gr):
        labels = {d['j'] for a, b, d in Gr.subgraph(comp).edges(data=True)}
        if len(labels) >= 2:
            mixed.append((len(comp), sorted(labels)))
    full = Counter(sum(1 for g in ROT if act(g, w) == w) for w in verts)
    print("%-28s |K|=%d: %d blocks in G_K (full stabiliser orders %s); SCCs with >= 2 shift labels: %s"
          % (name, len(K), len(verts), dict(full), mixed if mixed else 'none'))
