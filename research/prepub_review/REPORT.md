# Prepublication referee report

**Paper:** B. Hartshorn and T. Romanov, *The Internal Space and Boundary Growth of the Spectre and Tsiokos's Chair44
Tilings*.
**Reviewed:** romanov360/spectre, branch `paper-review-fixes`, head `989ef7f`. The review covers the generated
`spectre_substrate.tex` (30 pages), `spectre_supplement.tex` (4 pages), the ledgers, `boundary_certificate/`,
`hierarchy_certificate/` and `lean_rebuild/`.
**Date:** 2026-10-26.

**Ground rules.**
- Everything in the repository was treated as a claim. This includes the notes, the self-tests and the
  certificates written by the previous AI reviewer.
- "Verified" below means I checked the claim myself, either by reading the proof or by recomputing the number
  with my own code in `code/`.
- Re-running a repository certificate counts only as reproduction. Where I relied on reading such a certificate,
  the verdict says so.
- The Lean build of Tsiokos's development and the 4D search were not re-run, as instructed.

---

## 1. Summary

The core results survive:
- **The Spectre boundary.** The perimeter theorem and its corollaries are correct. I verified the certificate's
  method by reading it, re-ran it, and recomputed the sequence exactly to k = 8 with independent code in a
  different coordinate basis.
- **The Chair44 results.** The hull and symmetry theorems are logically sound given (R). I independently
  recomputed every finite input I could reach: the contacts, the 30 hierarchical contacts, the substitution, the
  coincidence, the legal-block language, the fixed seeds, the axial graphs G_K, and Lemma 2: 360,189 admissible
  blocks, 15,214 orbits, no illegal child window.

The problems that need fixing before submission:

1. **Theorem 3 (window dimension) is not proved as written.** This is a major issue.
   - The upper-bound argument counts only contacts generated from *sibling* pieces. That covers the internal seams
     of the window, not its outer boundary ∂W. Covering ∂W needs the neighbouring windows of a covering of
     internal space, and nothing in the paper or the certificate supplies one.
   - The regularity inputs are cited from BGMS without identifying the paper's W with BGMS's CASPr window system.
     The paper's W is read in the tile frame, merges orientations, and uses parity-dependent planes.
   - The value is probably right: my numerical box count gives local slopes 1.07–1.14, and BGMS state 1.110977
     for the CASPr windows, to which the Spectre's are related by reprojection. But the theorem, and the abstract
     sentence built on it, overstate what is shown.
2. **Leftover false statements in the supplement.**
   - It still says the perimeter recurrence "beyond k = 6 … is a conjecture". Theorem 1 now proves it for all k.
   - It still lists the window dimension as "≈ 1.2".
   - It says it lists "all 71" Facts of the paper. The paper has 25 Facts and the table has 73 rows.
3. **Leftover inconsistencies in the paper.**
   - It still says the hull theorem rests on "two quoted inputs" (Sec. 1) and on "two unrefereed inputs"
     (Sec. 9). Since Lemma 1 proves (H), only (R) remains.
   - It says "on the orders computed" right after proving all orders (Sec. 5).
   - Figure 3 and the text disagree on the patch level.
4. **The 4D-search paragraph misreports Kamenetsky.**
   - 1566 is his plateau for coordinate descent from random starts. It is not a "structured-family plateau": his
     structured families sit at 158 and 840, and the reported 273 does not beat 158.
   - "None is coarsening-closed" overstates a test capped at 400 poses.
   - "Exactly 3 of the 2187 close" omits Kamenetsky's own cap (|P*| ≤ 300).
5. **The Lean-rebuild sentence says more than the record shows.** The paper says the dependency report "is
   identical to the published one". The record shows agreement theorem by theorem, up to a name prefix, on the
   162 freshly printed theorems; it does not show identity. The script copies the "committed" log *after*
   `lake build`, although its comment says before. The record's control summary is `CONTROLS: FAIL`, and the
   README's 67/67 diff-audit pass has no recorded output.

**Recommendation:** major revision, though a short one. No result is wrong in a way that changes the paper's
conclusions:
- Theorem 3 can be repaired, or downgraded to "the contact computation reproduces BGMS's value".
- The remaining items are wording and consistency fixes.

---

## 2. Reproducibility (run on this machine)

| step | result |
|---|---|
| `python3 spectrepaper.py --selftest` | **pass**: 112 checks, "all checks pass", 5 min |
| `python3 spectrepaper.py` | regenerated `spectre_substrate.tex` **byte-identical** to the committed file |
| `python3 spectre_supplement.py --selftest`, then generate | **pass**; regenerated `.tex` byte-identical |
| `make facts` | **pass**: spectrefacts 62 facts, monotilefacts 8, chair44facts 43, `chair44_hull --tests`, `chair44_lines --tests`. The pyCICY cross-check was **skipped** ("pyCICY not on the path, so the perimeter is counted only with a rounding key"). |
| `pdflatex` ×2, `spectre_substrate` | 30 pages, no errors, no undefined references. **Pass 2 still prints "Label(s) may have changed. Rerun"**; a third pass is clean. Text identical to the committed PDF. |
| `pdflatex` ×2, `spectre_supplement` | 4 pages, no errors; 10 overfull hboxes, up to 135 pt (table rows, lines 114–156) |
| `boundary_certificate/check_spectre_boundary_proof.py` | reproduces: 93 live, 1270 pruned, margin 0.0971, P and Q to k=9, "PROVED"; 1 m 56 s |
| `check_spectre_fractal.py` | reproduces; output identical to committed `out_spectre_fractal.txt` |
| `spectre_window.py` | reproduces: 1192 types, charpoly (x−1)³⁵(x+1)³⁵x¹¹¹⁴(x⁴−10x²+1)², 142 intersecting, block of 14 |
| `hierarchy_certificate/check_chair44_hierarchy.py` | reproduces: 2388/44, P1 = 21, P0 = 30, P* = 44 = legal, 135 facet triples, 33 enclosures (18/15), (U) 15/15, (Pr) 1 + 14; 1 m 04 s |
| `spectrelean.py` + Lean 4.33.1 (bare toolchain) | `SpectreFacts.lean`: 67 theorems, accepted. Axiom audit: 43 axiom-free, 24 use `propext` and `Quot.sound`; no `sorryAx`, no `Classical.choice`. *This is the Spectre Facts file, not Tsiokos's development.* |

Logs are in `outputs/repo_runs/`. The PDFs were restored to their committed versions after the build check. Nothing
in the reviewed repository was modified.

Notes:
- `REVIEW_FIXES.md` says the build gives 28 pages and needs two passes with no warnings. It gives 30 pages, and a
  clean cross-reference state needs three passes.
- The `boundary_exact` ledger entry cites an implementation (pyCICY) that `make facts` does not run. Its content
  is covered by the certificate's exact recount and by my own recount to k = 8.

---

## 3. Claims and verdicts

Numbering follows the PDF: Facts F1–F25, Propositions P1–P4, Theorems T1–T5, Lemmas L1–L3, Corollaries C1–C2.

Verdict key:
- **V**: verified by me.
- **V(r)**: verified by reading the proof or certificate code and re-running it.
- **P**: plausible, not checked.
- **W**: wrong.
- **O**: overclaimed.
- **U**: unsupported.

| # | claim (short) | verdict | evidence |
|---|---|---|---|
| F1 | λ² = 4+√15 is the fundamental unit; λ = (√6+√10)/2; minimal polynomial x⁴−8x²+1; (λ∓λ⁻¹)² = 6, 10 | V | `algebra_checks.py` |
| F2 | χ_M = x⁵(x−1)(x+1)(x²−8x+1); rank M = 5, rank Mⁿ = 4; Jordan block sizes 1,1,1,2; convergence rates | V | `spectre_indep.py`; rates follow from the spectrum |
| F3 | Row Γ is all ones; T_geom = T(n)+T(n−1); 1ᵀ(M²−8M+I) = 0 | V | matrix check; geometric census 1, 9, 71, 559, 4401 recounted from placed tiles |
| F4 | Q± are left eigenvectors; values −1 and +1,−1,+1,−1 | V | |
| P1 | Determinant (−1)ⁿ; equals −Q₋(n) for seed Δ; Q₋ vanishes on Λ, Σ, Ψ | V | handedness alternates (my build); Q₋ entries 0 |
| F5 | N_Θ(n) = N_Γ(n−1), N_Λ(n) = N_Σ(n−1) | V | rows of M |
| F6 | Twist: not similar at finite levels; limit rotation ∓θ_S; tan θ_S, cos 2θ_S; correction ~ λ⁻²; B charpoly | V (numbers and fields), P (B charpoly) | `algebra_checks.py`. My diagonal ratios give arg −11.565082° at k=7 and +11.565047° at k=8, against 11.565051°: errors shrink by about λ² per level. The two-level ratio is real to 3·10⁻⁵ °. |
| (text) | θ_S irrational: cos 2θ_S has minimal polynomial 100x²−80x−11, so 2cos 2θ_S is not an algebraic integer | V | argument correct |
| T1 | P(k+3) = 5P(k+2)−3P(k+1)−P(k) and P(k) = 2F_{3k+5}+4 for all k; Q recurrence from k ≥ 1 | V(r) + V for k ≤ 8 | see §4.1 |
| F7 | recurrence, values to P(6) = 57318 | V | |
| F8 | exact recount k ≤ 6 | V | my exact recount to k = 8: 242790, 1028462 |
| F9 | P(k+2)−4P(k+1)−P(k) = −16 for all k | V | follows from T1; checked to k = 8 |
| F10, F11 | χ_∂ = (x−1)(x²−4x−1); ν = 2+√5 | V | |
| T2 | λ⁻ᵏS_k → K_p, closure of its interior, dim_B ∂K_p = log ν/log λ | V(r), with a minor gap | §4.2: citation used beyond "existence"; proof terse but correct |
| (text) | P(k+3) ≥ 4P(k+2)+30; P(k+1)/P(k) > 4 > λ for k ≥ 2 | V | from F9 |
| F12 | closed form | V | |
| eq. (dirsplit), Table 2 | even = F_{3k+4}+1, odd = F_{3k+3}+1 (k ≤ 6); max other amplitude 3.61 | V | all rows reproduced. Extended to k = 7, 8 (75026/46369, 317812/196419): the split holds, and the amplitudes 2.65 and 1.00 stay ≤ √13. |
| P2 | interface count; growth μ = λ²/ν; s* = 1−log ν/log λ² = 0.300373393044 | V (formula and number), modelling step stated | |
| (text) | s* transcendental: irrational ratio of logs of algebraic numbers, by Gelfond–Schneider | V | correct use of the corollary |
| F13 | x²−4x−1 divides neither χ_M nor χ_H | V | remainders non-zero |
| F14 | Lucas quadratics | V | |
| (text) | μ has minimal polynomial x⁴+32x³−46x²−32x+1 and lies in ℚ(√3,√5) | V | |
| F15 | lift; 3734 vertices at level 3; rank 4 | V (count) | `spectre_patch_facts.py` |
| F16 | Φ is 16×16 with χ_Φ = (x−1)⁴(x+1)⁴(x⁴−8x²+1)²; minimal polynomial of q₀; companion block | V (charpoly, in my own basis; exact on 6 levels) | |
| F17 | internal plane matrix; extents 9.77, 9.84, 2.89, 50; cosines | P | numerical; not recomputed |
| T3 | window = GD attractor; 1192 types; charpoly; dim_B ∂W = log(5+2√6)/log(4+√15) | **O / proof incomplete** | §4.3. The linear algebra is reproduced (residuals ~10⁻⁵⁸), the keys are sound (min separation 1.91 ≫ 10⁻⁴⁰), and the box count gives 1.07–1.14. The upper bound and the regularity inputs are missing. |
| (text) | earlier box count "about 1.2" | O (wording) | my depth-7 count gives slopes 1.08, 1.07, 1.11, 1.14 at the same halvings, so "about 1.2" is a poor estimate |
| L1 | (H): unique hierarchy of atlas tilings | V(r) | §4.4. Logic checked line by line against Kamenetsky's Prop. 7.1. Certificate read and re-run; 44 and 30 independently recomputed by me. C3 was not re-implemented by me. |
| L2 | 360,189 admissible blocks, 15,214 O-orbits, all 27 child windows legal | **V** | `chair44_blocks_indep.py`: an independent enumeration over all blocks, not orbit representatives, gives 360,189 blocks, 15,214 orbits and 0 illegal child windows. All 1410 legal blocks are admissible. 14 min. |
| T4 | every atlas tiling lies in Ω_σ; by (R), every tiling by Q | V(r) given L1, L2 | proof correct |
| C1 | only the 30 hierarchical contacts occur | V(r) | follows from T4 and the language; 30 recomputed |
| C2 | minimal, uniquely ergodic, pure point, regular model set over ℤ₂³ | V(r) (cited theorems used within scope) | primitivity at power 3 and coincidence at depth 3 (336/512, includes (0,0,2)) recomputed |
| (text) | 1410 legal blocks (168, 600, 1278, 1398, 1410, 1410); closed; 27 fixed seeds; stabilisers 1 (24×) and 8 (3×) | V | `chair44_blocks_indep.py`, independent |
| T5 | Sym(T) ∈ {1, C₂^diag, C₄, D₄} up to conjugacy, each occurs | V(r) + V (finite inputs) | §4.6. G_K recomputed: C₂ coordinate axis has 18 blocks and constant-shift components only; C₄ has 4 blocks with a mixed SCC; C₂^diag has 14 blocks with a mixed SCC |
| L3 | positions of axes | V | algebra checked |
| R1 | \|Sym\| ≤ 8 | V | from T5 |
| P3 | chair stacks: lines of length 2ⁿ−2 | P (14 cases × 6 not re-run by me) | proof structure correct |
| P4 | T^v not uniquely ergodic | V (conditional on the stated assumption) | proof correct |
| Table 4 | corner lines | P | |
| F18 | chair has 6 symmetries (3 mirrors); decorated has 1; 1194 mirror contacts, none legal | V (contact counts) | `chair44_blocks_indep.py`: 2388/1194/44, legal mirror 0 |
| F19 | twist 0; mean frame I/4; all 24 rotations at depth 2 | P | |
| (text) | 168×168 matrix: every row and column sum 8; c(M) = 28·2ᴹ−48; 209 reachable states, 41 non-singleton; spectral radius 2 | V | `chair44_coincidence_rate.py`. Every label occurs 8 times as a child. |
| (text) | nets: 261,434,325,600 spanning trees; 1253/1747 of 3000 sampled; the cube's 11 nets | P | not recomputed |
| F20 | centres; notch sum 2ⁿ(1,1,1); interface 4ⁿ⁺¹−4·2ⁿ | V (arithmetic), P (counts) | |
| F21 | orientation sums 1.4413 … 1.4489 | V (numerically) | my patches: \|S₁\| = 252 at level 5, so 252/λ⁵ = 1.449 |
| F22 | centre-set amplitudes; Parseval sum to 1/7 | V (algebra) | J = 1 amplitudes and the level sums check; the closed form of the Parseval sum is correct |
| F23 | S_{n+1} = C S̄_n; growth λⁿ | P; c² closed form is a root of the stated quartic, √c² = 1.44892 | |
| F24 | channels: chair 8 and 2; Spectre h = 2 (m = 0, 6), 1 (±1, ±5), ≤ 0 otherwise | V (Spectre, numerically) | `spectre_channels.py`. Note that \|S_{±4}\| grows *linearly* (1.73, 2.65, 3.61, 4.58, 5.57). "h ≤ 0" is true but hides a polynomial growth. |
| F25 | Spectre: 29,208 contacts, 62 non-zeros, rank 14, bipartite, connected, symmetric spectrum; Chair44 24×24 | V (Spectre), P (chair) | `spectre_patch_facts.py` |
| Sec. 8 | exact tail 0.394, 0.498, 0.528, 0.536 → ν/λ² | V | `lookback_tail.py`, with the Mystic's internal edges at level 0 (the paper does not state this convention) |
| Sec. 8 | other hierarchy numerics (C_S, records, parity statistics) | P | labelled "Computation, not Fact" |
| Sec. 9 | 4D search | **O** | §5, item M4 |
| (R) | registration theorem quoted; audited; Lean rebuilt | quoted; Lean sentence **O** | §5, item M5 |

---

## 4. Proofs

### 4.1 Theorem 1 (perimeter recurrence, all k): correct

I read `check_spectre_boundary_proof.py` line by line. The argument is sound:

- **Pair types.** The relative placement of a child pair is computed correctly:
  `A_i⁻¹ A A_j`, `A_i⁻¹(A M_j + LΦ − M_i)`.
- **Key canonicalisation.** L q_k is fixed for all k by L applied to the Krylov basis q₀, …, Φ⁵q₀, because the
  minimal polynomial of q₀ has degree 6. This is exact integer arithmetic.
- **Separation.**
  - Pruning compares the centroid distance with the sum of radius bounds. That is conservative.
  - The radius recursion r_{k+1} ≤ maxᵢ(|offᵢ| + r_child) is valid.
  - The tail bound accounts for the ±1 eigencomponents (λ⁻ᵏ) and the ±λ⁻¹ eigencomponents (λ⁻²ᵏ). The fixed-point
    iteration converges (factor 1/λ, 400 steps, 10⁻³⁰ slack at 60 digits).
- **Margin units.** The reported 0.0971 is the finite-range margin (k < 60) in units of the quad diagonal, as the
  paper says. The tail margin is 0.537 in units of λᵏ, which is about 0.15 diagonals (`margin_units.py`).
- **Floating-point error.** It is far below the margins: integer vectors are converted to floats with relative
  error of order 10⁻¹⁶.
- **Overlap.** Interior overlap is subadditive over child pairs, so zero overlap at level 0 for the live types
  propagates by induction. Disjointness of siblings, and hence that the supertiles are patches, follows. Common
  boundary length is additive once interiors are disjoint.
- **Cayley–Hamilton.** It is applied correctly: dim B = 95 and the first 95 terms of e B^k p(B) V₀ vanish.

Independent confirmation: `spectre_indep.py` uses a different exact representation and Kaplan's float outline as
its only geometric input. It gives:
- P = 14, 46, 182, 758, 3198, 13534, 57318, 242790, 1028462;
- Q = 20, 44, 160, 652, 2736, 11564, 48960, 207372, 878416.

Both sequences match the certificate. The Q recurrence fails at k = 0 and holds from k = 1, as stated.

### 4.2 Theorem 2 (box dimension of ∂K_p): correct, two gaps in exposition

- **Convergence, area and measure-disjointness are fine.** Lebesgue measure is upper semicontinuous under
  Hausdorff limits, and the Perron argument with [[7,1],[6,1]] forces equality in a ≤ N a′/λ² when a > 0.
- **Interior.** The certificate shows that grandchild (7,3) is separated from every grandchild of every live
  neighbour type at every order. If a ball about it left S, it would meet a touching supertile, and touching
  supertiles are live types. That is a contradiction, so the argument is right.
  - **Gap (minor).** The paper cites Smith et al. only for "existence of Spectre tilings of the plane". The proof
    actually needs more: a tiling in which the order-k supertiles are the construction's supertiles, and in which
    every pair of adjacent supertiles occurs, with its placement, inside some larger supertile. Only then are
    neighbour placements live types.
  - Smith et al. (Thm 2.2 and 5.1, §6) give the hierarchical structure combinatorially, and a compactness argument
    supplies such a tiling. The paper should say so in one sentence.
- **Upper bound.** ∂K lies in the ε-neighbourhood of ∂(λ⁻ᵏS_k) for large k; I checked this. Neighbour contacts are
  counted by the 93×93 contact matrix, whose dominant root ν is simple. Correct.
- **Lower bound.** The meeting points of two sibling pieces lie on the boundary of each piece. With
  measure-disjointness and closure of interior, a common point cannot be interior to either piece. But the pieces
  are copies of K_{p+1} (and of the Mystic limit), so the bound is for ∂ of the *children*, and transfers to ∂K by
  similarity. The text says only "each in a point of both boundaries", and should say which boundaries. Not an
  error.

### 4.3 Theorem 3 (window dimension): proof incomplete; statement overclaimed

The following parts are reproduced:
- The plane E_p, the intertwining, the coboundary and the invariant metric: residuals ≤ 10⁻⁵⁸.
- The closure on 1192 types and its characteristic polynomial.
- `window_probe.py` confirms that the rounded keys cannot merge or split types. Distinct translations with the same
  (S₁, S₂, p, B) are at least 1.91 apart. `spectre_window.py` computes this set (`ds`) but never checks it.
- No type lies near the pruning threshold. The closest is 0.026 from 2·RAD, which is far above the 10⁻²⁰ margin.

The gaps:

1. **Upper bound.**
   - The contact closure starts only from *sibling* pairs of pieces of Z_p(S). Its pairs therefore describe where
     pieces of the same window meet each other: the internal seams.
   - A point of ∂W need not lie near any such seam. To cover ∂W by pieces that are counted, one needs the pieces
     of *neighbouring* windows in a covering of internal space. In Theorem 2 this role was played by the
     neighbouring supertiles of a tiling of the plane.
   - BGMS show that the CASPr window and its lattice translates tile the plane (caption of their Fig. 8). That is
     exactly the missing input, but neither the paper nor the certificate uses it, and the neighbour types of that
     lattice tiling are not shown to lie in the 1192.
   - "At depth m there are O(m(√2+√3)^m) contact pairs" therefore bounds the seams, not ∂W.
2. **Regularity.**
   - The proof cites BGMS for "pieces overlap in measure zero and the window is the closure of its interior".
     BGMS prove this for *their* window system of the CASPr control points.
   - The Spectre is MLD to a *reprojection* of CASPr (BGMS §6), with the same total space, lattice and acceptance
     strip. So the internal windows should agree up to a linear map, but the paper does not make this
     identification.
   - The paper's W differs from BGMS's windows in three ways: it is read "in the frame of each tile", so it is a
     union of rotated subwindows; it is attached to tile positions rather than BGMS's control points; and it lives
     on parity-dependent planes.
   - Measure-disjointness actually follows from the Perron argument once W has positive area: the shape matrix
     [[7,6],[1,1]] has root λ². Positive area is what needs the citation.
3. **Comparison with BGMS.** BGMS give the value as a Hausdorff dimension, "as can be extracted from the orbit
   separation dimension" (their eq. (7) and Theorem 9). The paper's paraphrase, "they note that it deserves a
   closer analysis", is accurate only in part: BGMS's remark is about whether the dimension is the same
   everywhere along the boundary.

**Proposed fix (either of these):**
- (a) Add the covering argument. Use the lattice tiling of internal space by window translates, either from BGMS
  after identifying W with their windows, or proved directly. Extend the certificate's start set to the
  neighbour pairs of that covering.
- (b) Restate Theorem 3 as two parts. First, a proved lower bound: dim ∂W ≥ log(√2+√3)/log λ, given positive area
  and regularity. Second, an upper bound that holds conditionally on a covering. Rephrase the abstract to match.

My numerical box count of ∂Z₀(O) supports the value: depth 7, 3.1·10⁶ points, local slopes 1.084, 1.066, 1.106,
1.135 over ε = 0.4 … 0.025.

### 4.4 Lemma 1 (Kamenetsky's criterion): correct

- The paper's proof is Kamenetsky's Prop. 7.1, and the step "the true supertile is compatible with everything
  present" is correctly made explicit. The partition, uniqueness, and the halving through (C1) are correct.
- I read `check_chair44_hierarchy.py`:
  - Enclosure enumeration has no duplicates, because each branch fixes the tile covering the first uncovered panel.
  - Liveness is an exhaustive DFS with a hard node-limit assertion, not a silent cutoff.
  - The (U) candidates are all eight placements of A as a child.
  - (Pr) quantifies over enclosures of T₀ compatible with A ∪ E.
  - Σ(P) enumerates every supertile with a child touching a reference child.
- The paper's lemma labels (C1) and (C3) and folds C2 (tightness) into C1. Kamenetsky's labels are C1–C3. Use his
  labels or say that C2 is included.
- I independently recomputed the 44 legal contacts and the 30 hierarchical contacts, from pyramid geometry rather
  than coefficients. I did not re-implement C3 (33 enclosures, 18/15, U, Pr). Its numbers agree with Kamenetsky's
  published Table 1.

### 4.5 Lemma 2 and Theorem 4 (hull): correct given L2

- The proof of Theorem 4 is right. The block at the vertex nearest P covers a cube of half-side 2ⁿ ≥ the extent of
  P. The offset v − v′ + (1,1,1) lies in {0,1,2}³. Admissibility of β′ comes from D^{n+1}(T) being an atlas
  tiling.
- **Lemma 2 is verified independently.** `chair44_blocks_indep.py` decides legal contacts from pyramid geometry and
  enumerates admissible blocks with a pairwise-compatibility bitset search. It gives exactly 360,189 admissible
  blocks in 15,214 O-orbits, and none has an illegal window among the 27 windows of its substitution. As a
  consistency check, the 1410 legal blocks are all admissible. This was the one input of the main theorem that the
  paper's build does not recompute.

### 4.6 Theorem 5 and Lemma 3 (symmetry): correct

- **The order-3 exclusion is valid.** The three bad intervals of t have total length 0.06 < 1. The pyramid height
  12·10⁻⁴ < 0.01.
- **The vertex-centred case is valid.** The stabilisers decrease, a block recurs, so it is Φ-periodic; the only
  periodic legal blocks are the 27 fixed seeds (recomputed: 27 periodic, all fixed, stabilisers {1: 24, 8: 3}).
- **The axial case is valid.** j_n ∈ {−1,0,1}; an eventually constant shift gives a common vertex; and the converse
  construction works. I checked |J_i| < 2^p−1, that J_i ≠ 0, the formula xₙ = y₀ − 2ⁿy_{n mod p}, and the
  covering radius.
- **Finite inputs recomputed independently.**
  - C₂ about a coordinate axis: 18 blocks, stabiliser orders {2: 12, 4: 2, 8: 4}, no SCC with two labels.
  - C₄: 4 blocks, with an SCC carrying shifts {−1, 0, 1}.
  - C₂ about either face diagonal: 14 blocks, with an SCC carrying shifts {−1, 0, 1}.

### 4.7 Other arguments

- **Proposition 2 (s\*).** Transcendence via Gelfond–Schneider is correct. The interface formula is right, given
  that T(c) counts order-(N−c) supertiles with the Mystic as one Γ.
- **Twist and irrationality.** Correct; see F6.
- **Proposition 4.** Correct as a conditional statement.
- **Fact 3 / census recurrence for all seeds.** Correct: it reduces to 1ᵀ(M²−8M+I) = 0.

---

## 5. Issues, ranked

### Fatal
None found.

### Major

**M1. Theorem 3 overclaims (Sec. 6 and abstract).**
- Location: `thm:window` and its proof; the abstract ("the window is the attractor of contracting similarities,
  with boundary dimension …"); the conclusion.
- Evidence: §4.3. The upper bound covers only sibling seams. Regularity is cited from BGMS without identifying the
  windows.
- Fix: §4.3 (a) or (b). At minimum, weaken the abstract and state the theorem's hypotheses explicitly.

**M2. The supplement contradicts the paper.**
- Location: `spectre_supplement.tex` lines 60–66, the generated text in `spectre_supplement.py`.
  - "Two of the Facts are inputs … `boundary_recurrence` on perimeters counted from placed tiles for k ≤ 6; beyond
    k = 6 the recurrence is a conjecture." This is false since Theorem 1. It also contradicts the table row for
    the same key, which reads "proved for every k by the finite certificate".
- `internal_plane` row: "dim of the window ≈ 1.2". This is stale against Theorem 3's 1.110977; the source is
  `monotilefacts.py` lines 169 and 183–184, and its docstring line 13 ("The window dimension is a box-counting
  estimate").
- Line 29: "lists every Fact of the paper — all 71". The paper has 25 Facts and the table has 73 rows. The ledger
  keys are not the paper's Facts. The counts of 71, 24 and 67 are not mutually consistent with
  `spectrefacts.py --selftest` ("62 facts, 18 with a Lean rendering"), although the 24 marked rows and the 67 Lean
  theorems do check out.
- The `chair_hull_theorem` row lists the groups as {1, C₂, C₄, D₄}, dropping the essential "diag" qualifier.
  Theorem 5 and Remark 1 exclude C₂ about a coordinate axis.
- Fix:
  - Regenerate the paragraph to say that the recurrence is proved for all k (Theorem 1).
  - Update `internal_plane` to the exact value with a pointer to Theorem 3.
  - Say "ledger entries" rather than "Facts of the paper", or map keys to Fact numbers.
  - Write C₂^diag.

**M3. Stale and inconsistent statements in the paper.**
- Sec. 1, line 77: "with a proof, resting on two quoted inputs, that every Chair44 tiling lies in the substitution
  hull". Only (R) is quoted now; (H) is Lemma 1.
- Sec. 9, line 1583: "conditional on two unrefereed inputs". There is one unrefereed input, (R), plus the
  computations of Lemmas 1–2.
- Sec. 5, line 401: "So, on the orders computed, the area … and its perimeter by 2+√5". This is now proved for
  all orders.
- Sec. 6, lines 703–704 against Figure 3: the text says the box count is from a "level-5 patch (Figure 3)". The
  caption and panel title say level 4.
- Scope paragraph, line 1098: "on the theorem of Lee, Moody and Solomyak". The proof of Corollary 2 invokes Lee–Moody
  [LeeMoody] (with [LMS] for the hull). Name one consistently.
- Sec. 8 look-back paragraph: "Their number in a level-N patch is T(N−ℓ) times the glue". There are two shapes
  with different glue, G_O(ℓ) ≠ G_G(ℓ), so the count is c_O(ℓ)G_O(ℓ) + c_G(ℓ)G_G(ℓ). The convention for the 4
  edges inside each Mystic is not stated: it changes the first ratio from 0.394 to 0.368 (`lookback_tail.py`).
- Abstract: "the tail … decays exactly by ν/λ²". Only the limit ratio is ν/λ²; the ratios are 0.394, 0.498, ….
  Say "with ratio tending exactly to ν/λ²".

**M4. The 4D-search paragraph misreports the cited source (Sec. 9, lines 1604–1610).**
- "It got below his structured-family plateau of 1566, to 273". In Kamenetsky (arXiv:2610.00916, Table 2 and
  p. 13), 1566 is the plateau of "coordinate descent on |Σ(P₀)|, random starts", i.e. generic assignments. The
  structured families (D₄-, ⟨(03),(12)⟩-, Z₄-invariant) sit at **158**, and the suspension of the 3D solution at
  840. A value of 273 is below the random-start plateau but **above** the structured-family value.
- "None is coarsening-closed, and every one exceeds 400 contact poses". The test stops at 400 poses, so it
  establishes only "no assignment closed below a cap of 400". Kamenetsky makes the same caveat for his own
  Theorem B ("the cap is part of the statement").
- "Exactly 3 of the 2187 homochiral assignments close". Kamenetsky's Theorem B says exactly three are
  coarsening-closed *with |P*| ≤ 300*. Add the cap.
- The search records (`chair_nd.py`, `chair_nd_fast.py`, the annealing logs) are not in this repository. I could
  not access the cited review branch (see §8), so the counts 12,784 and about 12,100 are unverified.
- Fix: correct the plateau sentence, state the caps, and cite the location of the records.

**M5. The Lean-rebuild sentence (input (R), lines 887–890) claims more than the record shows.**
- Paper: "the dependency report of the theorem lists only the three standard axioms … and named decision steps …;
  the report is identical to the published one (`lean_rebuild/`)".
- What `r44_build_result.json` shows:
  - The build succeeded: Lean 4.31.0, `lake build` rc 0.
  - `registration_of_tiling` depends on `propext`, `Classical.choice`, `Quot.sound` and 13 `native_decide` hooks.
    The other key theorems: `tiling_homochiral` 3 + 13 hooks, `geometric_hierarchy_unique` 3 + 17 hooks,
    `r44_einstein` 3 + 21 hooks.
  - No `sorryAx` appears.
  - The 162 freshly printed reports agree with the log entries of the same theorems, **up to the `R44.` prefix**.
    The log holds 169 entries.
- What the record does not support:
  - "Identical". No hash or diff is recorded. Moreover, `r44_build.py` copies `build_axioms.log` *after*
    `lake build`, although its comment says "copied before anything rewrites it". If the build regenerates that
    file, as the README says, the "committed" copy is post-build. Byte-identity is asserted in the README, not
    recorded.
  - The control run ends `CONTROLS: FAIL (… discharge_diff=0/1 …)`. The README's "PASS (67/67)" diff audit via
    `r44_diff_audit.py` has no recorded output.
- Not addressed: a successful build shows that the Lean theorem holds. It does not show that the Lean statement
  formalises (R) as used in the paper. The `native_decide` hooks also trust the compiler; the paper does say this.
- Fix:
  - Write "the regenerated dependency reports agree, theorem by theorem, with the published log", or record a hash
    or diff and keep "identical".
  - Commit the diff-audit output if the README's claim is to stand.
  - Add one sentence on statement fidelity.

### Minor

- **m1. Theorem 2: the citation is used beyond "existence".** See §4.2. Add a sentence that the tiling used is
  hierarchical with the construction's supertiles. Also say that the lower bound is for the children's
  boundaries, transferred by similarity.
- **m2. Kamenetsky's labels.** Lemma 1's proof says "(C1)" and "(C3)" only. Use Kamenetsky's C1–C3 or say that C2
  is folded in.
- **m3. `spectre_window.py` computes `ds` and never asserts on it.** The key-separation check is missing. It holds
  with margin 1.91 (`window_probe.py`); add the assertion.
- **m4. The BGMS paraphrase.** "They note that it deserves a closer analysis" (Sec. 6). BGMS's remark concerns
  whether the Hausdorff dimension is uniform along the boundary. Also say that BGMS's value is a Hausdorff
  dimension and the paper's is a box dimension.
- **m5. Fact 24, h ≤ 0.** |S_{±4}| grows linearly in n (1.73, 2.65, 3.61, 4.58, 5.57), which suggests a non-trivial
  Jordan block on the unit circle. "h ≤ 0" is accurate but could say "h = 0, with linear growth".
- **m6. Build notes.** Two pdflatex passes leave "Label(s) may have changed"; a third is needed. `REVIEW_FIXES.md`
  says 28 pages, but the build has 30. The supplement has overfull boxes up to 135 pt.
- **m7. The pyCICY cross-check is skipped by `make facts`,** although the ledger method for `boundary_exact` cites
  pyCICY. Cite the boundary certificate's exact recount instead (`exact_perimeter`, k ≤ 6).
- **m8. The generated `SpectreFacts.lean` comment says** "The second is that the boundary is fractal … Both halves
  are proved below." The Lean file proves P(k+3) ≥ 4P(k+2)+30 and λ² < 16, which is not fractality. Reword the
  comment in `spectrelean.py`.
- **m9. Conclusion: "One problem remains open".** Several remain: the einstein property itself is quoted, as are
  (R) and the identification in M1. Say "one further problem".
- **m10. Supplement author name.** It reads "Brent S. Hartshorn", the paper "Brent Hartshorn".
- **m11. `chair44_data/ATTRIBUTION.md`** cites arXiv:2609.23783 (Flicker) among the sources for Tsiokos's data.
  This is a repository issue, not a paper issue.
- **m12. The lemma credited to a third implementation (lines 934–937)** is cited to a URL in another repository,
  `romanov360/big-bang-monotile`. That repository appears to be private: unauthenticated `git clone` fails. A
  reader cannot follow the citation.
- **m13. Figure 2 caption: "asserted equal to the recurrence".** Since Theorem 1 this is proved, so say "equal, by
  Theorem 1".

---

## 6. Bibliography check

Each arXiv entry was checked against its arXiv abstract page (export.arxiv.org). The full text was read where
noted.

| key | check | result |
|---|---|---|
| SmithEtAl | arXiv:2303.10798, Smith, Myers, Kaplan, Goodman-Strauss, "An aperiodic monotile"; Combinatorial Theory 4(1) 2024 | correct |
| SmithEtAl2 | arXiv:2305.17743, same authors, "A chiral aperiodic monotile"; Comb. Theory 4(2) 2024 (arXiv jref matches) | correct. Full text: Thm 2.2 (existence, hierarchy) and Thm 5.1 (composition). It supports "Spectre tilings of the plane exist" and the hierarchical structure (see m1). |
| BangNote | companion note in the repo | exists (`spectre_bigbang_note.tex`) |
| Tsiokos1 | arXiv:2609.19214, I. Tsiokos, "A Strongly Aperiodic Monotile in Three Dimensions" (16 Sep 2026) | correct. Full text: Lemma 5.3 and Thm 5.6 (registration) ✓; Thms 6.4 and 6.5 (unique parent, coarsening) ✓; Thm 8.1 (coincidence at (0,0,2), depth 3, primitive exponent 3) ✓; 27 fixed seeds, orbits 24 + 3, stabilisers of orders 1 and 8 (Prop. 8.2) ✓; \|Sym\| ≤ 24 (Thm 7.2) ✓; §10 Q(1) and Q(2) leave open the symmetry groups and whether every tiling lies in the hull ✓ |
| GoodmanStrauss | arXiv:2609.24779, C. Goodman-Strauss, "Notes on a strongly aperiodic monotile in E³" | correct; "Berger-style" account ✓ |
| Flicker | arXiv:2609.23783, F. Flicker, "Matching Rules for a Three-Dimensional Strongly Aperiodic Monotile" (v2) | correct; the slide argument (p. 2) and "only 30 of these can appear" (l. 148) ✓; simpler equivalent rules ✓ |
| Romanov | draft and repository files | the `chair44_independent/` files exist in the repo. The draft itself is unpublished. |
| BaakeHat | arXiv:2502.03268, Baake, Gähler, Mazáč, **Mitchell**, "Diffraction of the Hat and Spectre tilings and some of their relatives" | authors and title correct. **Missing journal reference: J. Math. Phys. 66 (2025) 092707.** |
| BaakeSpectre | arXiv:2411.15503, Baake, Gähler, Mazáč, Sadun, "On the long-range order of the Spectre tilings"; Discr. Comput. Geom. 78 (2026) 739–762 | correct (matches the arXiv jref). Content: pure point and a 4:2 CPS with regular Rauzy-type windows ✓; CASPr value 1.110977 as Hausdorff dimension ✓; caveat paraphrased imprecisely (m4); used beyond scope in T3 (M1) |
| BGS | arXiv:2305.05639, Baake, Gähler, Sadun, "Dynamics and topology of the Hat family of tilings", Israel J. Math. 270 (2025) 449–485 | correct |
| CheritatMa | web page, 2023 | not fetched; plausible |
| Kamenetsky | arXiv:2610.00916, D. Kamenetsky, "Towards Strongly Aperiodic Monotiles in Higher Dimensions" | correct. Full text: Prop. 7.1 ✓ (C1–C3 as described, with C2 tightness); Theorem A ✓ (2388→44→33→15→one supertile); Problem 9.1 ✓ (4D). **Theorem B is capped at \|P*\| ≤ 300, and the 1566 plateau belongs to random-start descent, not structured families (M4).** |
| LeeMoody | Lee, Moody, "Lattice substitution systems and model sets", DCG 25 (2001) 173–201 | correct (standard reference) |
| BMS | Baake, Moody, Schlottmann, J. Phys. A 31 (1998) 5755–5765 | correct |
| Robinson | E. A. Robinson Jr., "On the table and the chair", Indag. Math. (N.S.) 10 (1999) 581–599 | correct |
| Gelfond | Gelfond 1934, Izv. Akad. Nauk SSSR 7, 623–630; Schneider 1935, J. Reine Angew. Math. 172, 65–69 | correct |
| Schlottmann | CRM Monograph Series 13, AMS 2000, 143–159 | correct |
| LMS | Lee, Moody, Solomyak, DCG 29 (2003) 525–560 | correct |
| BKM | Barbour, Koslowski, Mercati, PRL 113, 181101 (2014); arXiv:1409.0917 | correct (matches arXiv) |

Attribution statements checked:
- "Tsiokos proves (H) for tilings by Q [Thms 6.4, 6.5]" ✓.
- "(R) is [Thm 5.6, Lemma 5.3]" ✓.
- "recorded in [Thm 8.1]" ✓.
- "he exhibited orders 1 and 8" ✓.
- "Flicker argues informally … states 30 of 44" ✓.
- "Kamenetsky … finds that the obvious four-dimensional analogues fail a closure test" ✓.
- "BGMS prove that Spectre tilings arise from a 4:2 cut-and-project scheme with such windows" ✓ as in their
  abstract. Precisely, the Spectre is MLD to a reprojection.

Novelty: none of Tsiokos, Kamenetsky, Flicker or Goodman-Strauss states the hull theorem or the symmetry
classification. Tsiokos poses both as open questions. The novelty claim stands.

---

## 7. Consistency sweep

Searched the paper, the supplement and the ledgers for "conjecture", "not proved", "estimate", "on the orders",
"two quoted", "≈1.2" and "fractal". The hits that need action are in M2, M3, m8 and m13. These are fine:
- Sec. 5 "the split … is not proved beyond k = 6": correct, it concerns the direction split, not the recurrence.
- "the conjecture that the Spectre's boundary combinatorics are the Hat's": rhetorical.
- "identified, not proved": the c² closed form.

The abstract, introduction and conclusion agree with the body except at these points: the window (M1), the
ancestor tail ("exactly", M3), "two quoted/unrefereed inputs" (M3), and the 4D search (M4).

---

## 8. Notes on the review environment

- The task asked for this report on a branch of `romanov360/big-bang-monotile`. That private repository could not
  be attached to the session, so I could not read the prior review there; nothing here relies on it.
- At the author's request, the report is instead on branch `paper-prepub-review` of `romanov360/spectre`. The branch
  is based on `paper-review-fixes` at `989ef7f` and adds only `research/prepub_review/`. The paper, its generators
  and the certificates are unchanged.
- I did not use Modal.
