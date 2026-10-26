# Prepublication review: code

Everything here was written for this review. Nothing imports the paper's build, except where noted. Those
scripts are probes of the repository's certificates and say so.

Requirements: Python 3 with numpy, sympy, mpmath, networkx. Chair44 scripts need Tsiokos's solid,
`r44_solid.json` from ioannist/six-birds-tiles at commit d53d2245bc91c01cf81b6490a1cd6732e7f73bd3 (sha256
`f320d7a0c2d784a3eb29f001dc035808f67591d9ea8d3dd45949e66442f0ed55`). It is byte-identical to
`chair44_data/r44_solid.json` in the reviewed repository. Run scripts that read it with `python3 -I`.

Outputs of the runs are in `../outputs/`.

| script | what it checks | run | time |
|---|---|---|---|
| `spectre_indep.py` | Independent exact Spectre build. Points are stored as (a,b,c,d) with x=(a+b√3)/2, y=(c+d√3)/2, which is not the repository's Z⁴ basis. It covers: M, χ_M, ranks, censuses, Q±, P(k) and Q(k) for k ≤ 8 (mod-2 outlines, cross-checked against all placed tiles for k ≤ 5), the recurrence, closed form, −16 invariant, growth bound, the even/odd direction split (Table 2, extended to k=8), Φ and its characteristic polynomial, and the twist angle. | `python3 spectre_indep.py 8` | 2 min |
| `spectre_patch_facts.py` | Fact 15 (3734 vertices at level 3) and Fact 25 (Spectre 14×14 contact matrix: 29,208 contacts, 62 non-zeros, rank 14, bipartite). Imports `spectre_indep.py`. | `python3 spectre_patch_facts.py` | 1 min |
| `spectre_channels.py` | Fact 24, Spectre harmonics: growth exponents h_m from placed patches. | `python3 spectre_channels.py` | 1 min |
| `algebra_checks.py` | The exact algebraic numbers: θ_S and its minimal polynomials, λ, μ, s*, D_b, the window value, Lucas quadratics, the Fibonacci identity, and the c² quartic. | `python3 algebra_checks.py` | seconds |
| `lookback_tail.py` | The exact common-ancestor tail ratios of Sec. 8 (0.394, 0.498, 0.528, 0.536 → ν/λ²), from P and Q. | `python3 lookback_tail.py` | seconds |
| `chair44_blocks_indep.py` | Independent Chair44 computation. Legal contacts are decided by geometric coincidence of the pyramids. It reports: 2388/1194/44 contacts, the 30 hierarchical contacts, the 168-label substitution, primitivity, the modular coincidence (336/512, (0,0,2)), the legal-block language (168…1410), the 27 fixed seeds and their stabilisers, and **Lemma 2**: the admissible blocks, their O-orbits, and legality of all 27 child windows. | `python3 -I chair44_blocks_indep.py r44_solid.json` | 14 min |
| `chair44_symmetry_indep.py` | The graphs G_K of the proof of Theorem 5: the numbers of blocks and the strongly connected components with two shift labels, for C2 about a coordinate axis, C4, and C2 about face diagonals. Executes the first half of `chair44_blocks_indep.py`. | `python3 -I chair44_symmetry_indep.py r44_solid.json` | 3 min |
| `chair44_coincidence_rate.py` | The subset automaton: 209/41 states, c(M), and spectral radius 2. | `python3 -I chair44_coincidence_rate.py r44_solid.json` | 1 min |
| `window_probe.py` | Probe of `boundary_certificate/spectre_window.py`: soundness of its rounded contact keys, closeness to the pruning threshold, and a numerical box count of ∂Z₀(O) from a depth-7 enumeration (3.1M points). | `PYTHONPATH=<repo>/boundary_certificate python3 window_probe.py` | 6 min |
| `margin_units.py` | Probe of `check_spectre_boundary_proof.py`: splits the reported smallest separation margin into its finite-range part (units of the quad diagonal) and its tail part (units of λ^k). | `PYTHONPATH=<repo>/boundary_certificate python3 margin_units.py` | 3 min |

The arXiv texts used for the bibliography check were fetched as PDFs from arxiv.org and converted with `pdftotext`.
They are not redistributed here.
